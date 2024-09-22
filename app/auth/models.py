from pydantic import BaseModel, EmailStr


class UsuarioCreateModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None
    password: str


class UsuarioViewModel(BaseModel):
    nome: str
    email: EmailStr | None = None
    sobrenome: str | None = None
    
#    class Config:
#        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataModel(BaseModel):
    nome: str | None = None
