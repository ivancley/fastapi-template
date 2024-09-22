from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone


Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )


class UsuarioCreateModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None
    password: str


class UsuarioViewModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataModel(BaseModel):
    nome: str | None = None
