from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.v1.utils.db_services import get_db
from app.v1.auth.models import (
    Role,
    Permission,
    RoleCreateModel,
    PermissionCreateModel,
    UsuarioDB,
)

router = APIRouter( tags=["Admin"])


@router.post(
    "/",
    response_model=PermissionCreateModel,
    status_code=status.HTTP_201_CREATED,
)
def create_permission(permission: PermissionCreateModel, db: Session = Depends(get_db)):
    db_permission = (
        db.query(Permission).filter(Permission.name == permission.name).first()
    )
    if db_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")
    new_permission = Permission(
        name=permission.name, description=permission.description
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission


@router.post(
    "/roles/", response_model=RoleCreateModel, status_code=status.HTTP_201_CREATED
)
def create_role(role: RoleCreateModel, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Perfil já existe")

    permissions = (
        db.query(Permission).filter(Permission.name.in_(role.permissions)).all()
    )
    if len(permissions) != len(role.permissions):
        raise HTTPException(status_code=400, detail="Não existe esse perfil")

    new_role = Role(
        name=role.name, description=role.description, permissions=permissions
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.post("/users/{user_id}/roles/", response_model=RoleCreateModel)
def assign_role_to_user(user_id: int, role_name: str, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    if role in user.roles:
        raise HTTPException(status_code=400, detail="Usuário já possui o perfil")

    user.roles.append(role)
    db.commit()
    return role


@router.get("/roles/", response_model=List[RoleCreateModel])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@router.get("/", response_model=List[PermissionCreateModel])
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return permissions
