from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone


Base = declarative_base()


class PacienteDB(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    telefone = Column(String, nullable=True)
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


class PacienteCreateModel(BaseModel):
    nome: constr(min_length=3)
    email: EmailStr
    telefone: str


class PacienteViewModel(PacienteCreateModel):
    id: int
    disabled: bool
