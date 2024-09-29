from pydantic import BaseModel, EmailStr
from .role_model import RoleViewModel


class UserCreateModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None
    password: str


class UserViewModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None
    roles: list[RoleViewModel] | None = []

