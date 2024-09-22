from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from decouple import config
from app.v1.auth.services import (
    authenticate_user,
    create_user,
    get_db,
    valida_create_user
)
from app.v1.auth.security import create_access_token, get_current_user
from app.v1.auth.models import (
    UsuarioDB, 
    UsuarioCreateModel, 
    UsuarioViewModel, 
    TokenModel
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()

@router.post("/login", response_model=TokenModel)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> TokenModel:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="e-mail ou senha inválida",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return TokenModel(access_token=access_token, token_type="bearer")


@router.post("/usuarios/novo/", response_model=UsuarioViewModel)
async def create_new_user(
    usuario: UsuarioCreateModel, 
    db: Session = Depends(get_db)
):
    error = valida_create_user(db, usuario)
    if error: 
        raise HTTPException(status_code=400, detail=error)

    return create_user(db=db, usuario=usuario)


@router.get("/usuarios/eu/", response_model=UsuarioViewModel)
async def read_users_me(
    current_user: Annotated[UsuarioDB, Depends(get_current_user)],
):
    return current_user