from datetime import datetime, timedelta, timezone
from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from typing import Annotated, List
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.v1.auth.models.db_models import UserDB
from app.v1.auth.models.token_model import TokenDataModel
from app.v1.auth.models.user_model import UserCreateModel, UserViewModel
from app.v1.utils.db_services import get_db

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthSecurity:

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db),
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenDataModel(nome=username)
        except PyJWTError:
            raise credentials_exception

        user = self.get_usuario_by_email(db, token_data.nome)
        if user is None:
            raise credentials_exception
        return user

    def get_user_by_nome(self, db: Session, nome: str):
        return db.query(UserDB).filter(UserDB.nome == nome).first()

    def get_usuario_by_email(self, db: Session, email: str):
        return db.query(UserDB).filter(UserDB.email == email).first()

    def create_user(self, db: Session, usuario: UserCreateModel):
        hashed_password = AuthSecurity().get_password_hash(usuario.password)
        db_usuario = UserDB(
            nome=usuario.nome,
            email=usuario.email,
            sobrenome=usuario.sobrenome,
            hashed_password=hashed_password,
            disabled=False,
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def authenticate_user(self, db: Session, username: str, password: str):
        user = self.get_usuario_by_email(db, username)
        if not user:
            return False
        if not AuthSecurity().verify_password(password, user.hashed_password):
            return False
        return user

    def valida_create_user(self, db: Session, user: UserCreateModel):
        resp = None
        db_email = self.get_usuario_by_email(db, user.email)
        if db_email:
            resp = "E-mail já cadastrado"
        return resp

    def get_user_permissions(self, user: UserDB) -> List[str]:
        permissions = set()
        for role in user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)
        return list(permissions)

    def has_permission(self, user: UserDB, permission: str) -> bool:
        user_permissions = self.get_user_permissions(user)
        return permission in user_permissions

    def get_user_roles(self, user: UserDB) -> List[str]:
        roles = set()
        for role in user.roles:
            roles.add(role.name)
        return list(roles)

    def has_role(self, user: UserDB, role_name: str) -> bool:
        user_roles = self.get_user_roles(user)
        return role_name in user_roles
