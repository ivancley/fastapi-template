from pydantic import BaseModel, EmailStr
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    Table,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime, timezone


Base = declarative_base()

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class UsuarioDB(Base):
    __tablename__ = "users"

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

    roles = relationship('Role', secondary=user_roles, back_populates='users')


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    users = relationship('UsuarioDB', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')



class UsuarioCreateModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None
    password: str

class RoleViewModel(BaseModel):
    id: int
    name: str
    description: str | None = None


class UsuarioViewModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None
    roles: list[RoleViewModel] | None = []


class RoleCreateModel(BaseModel):
    name: str
    description: str | None = None
    permissions: list[str] = []



class PermissionCreateModel(BaseModel):
    name: str
    description: str | None = None


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataModel(BaseModel):
    nome: str | None = None
