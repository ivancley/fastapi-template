from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from decouple import config
from app.auth.services import (
    authenticate_user,
    create_user,
    get_db,
    valida_create_user
)
from app.auth.security import create_access_token, get_current_user
from app.auth.models import UsuarioCreateModel, UsuarioViewModel, TokenModel
from app.models.usuario import UsuarioDB

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
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenModel(access_token=access_token, token_type="bearer")


@router.post("/usuarios/novo/", response_model=UsuarioViewModel)
async def create_new_user(
    user: UsuarioCreateModel, 
    db: Session = Depends(get_db)
):
    error = valida_create_user(db, user)
    if error: 
        raise HTTPException(status_code=400, detail=error)

    return create_user(db=db, user=user)


@router.get("/usuarios/eu/", response_model=UsuarioViewModel)
async def read_users_me(
    current_user: Annotated[UsuarioDB, Depends(get_current_user)],
):
    return current_user