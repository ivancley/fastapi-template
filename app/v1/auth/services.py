from sqlalchemy.orm import Session
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.v1.auth.security import verify_password, get_password_hash
from app.v1.auth.models import UsuarioCreateModel, UsuarioDB

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_nome(db: Session, nome: str):
    return db.query(UsuarioDB).filter(UsuarioDB.nome == nome).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

def create_user(db: Session, usuario: UsuarioCreateModel):
    hashed_password = get_password_hash(usuario.password)
    db_usuario = UsuarioDB(
        nome=usuario.nome,
        email=usuario.email,
        sobrenome=usuario.sobrenome,
        hashed_password=hashed_password,
        disabled=False
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def authenticate_user(db: Session, username: str, password: str):
    user = get_usuario_by_email(db, username)
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
