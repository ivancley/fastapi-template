from datetime import timedelta
from decouple import config
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from app.v1.utils.db_services import get_db
from app.v1.auth.security import AuthSecurity
from app.v1.auth.models import (
    UsuarioDB,
    UsuarioCreateModel,
    UsuarioViewModel,
    TokenModel,
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()


@router.post("/login", response_model=TokenModel)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> TokenModel:
    user = AuthSecurity().authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="e-mail ou senha inválida",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthSecurity().create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return TokenModel(access_token=access_token, token_type="bearer")


@router.post(
    "/usuarios/novo/",
    response_model=UsuarioViewModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(usuario: UsuarioCreateModel, db: Session = Depends(get_db)):
    error = AuthSecurity().valida_create_user(db, usuario)
    if error:
        raise HTTPException(status_code=400, detail=error)

    return AuthSecurity().create_user(db=db, usuario=usuario)


@router.get("/usuarios/eu/", response_model=UsuarioViewModel)
async def read_users_me(
    current_user: Annotated[UsuarioDB, Depends(AuthSecurity().get_current_user)],
):
    return current_user
