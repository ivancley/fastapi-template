from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataModel(BaseModel):
    nome: str | None = None
