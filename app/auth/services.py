from sqlalchemy.orm import Session
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.auth.security import verify_password, get_password_hash
from app.auth.models import UsuarioCreateModel
from app.models.usuario import UsuarioDB

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_nome(db: Session, username: str):
    return db.query(UsuarioDB).filter(UsuarioDB.nome == username).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

def create_user(db: Session, user: UsuarioCreateModel):
    hashed_password = get_password_hash(user.password)
    db_user = UsuarioDB(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        disabled=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_nome(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def valida_create_user(db: Session, user: UsuarioCreateModel):
    resp = None
    db_email = get_usuario_by_email(db, user.email)
    if db_email:
        resp="E-mail já cadastrado"
    return resp
