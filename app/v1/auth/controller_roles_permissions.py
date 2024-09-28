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
from app.v1.auth.security import AuthSecurity
from app.v1.auth.permissions import PermissionRequired

router = APIRouter(tags=["Admin"])

auth = AuthSecurity()


# Exemplo: Apenas usuários com a permissão 'create_permission' podem criar permissões
@router.post(
    "/permissions/",
    response_model=PermissionCreateModel,
    status_code=status.HTTP_201_CREATED,
    #dependencies=[Depends(PermissionRequired("create_permission"))],
)
def create_permission(permission: PermissionCreateModel, db: Session = Depends(get_db)):
    db_permission = (
        db.query(Permission).filter(Permission.name == permission.name).first()
    )
    if db_permission:
        raise HTTPException(status_code=400, detail="A permissão já existe")
    new_permission = Permission(
        name=permission.name, description=permission.description
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission


# Similarmente, proteja outras rotas de administração
@router.post(
    "/",
    response_model=RoleCreateModel,
    status_code=status.HTTP_201_CREATED,
    #dependencies=[Depends(PermissionRequired("create_role"))],
)
def create_role(role: RoleCreateModel, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="O perfil já existe")

    permissions = (
        db.query(Permission).filter(Permission.name.in_(role.permissions)).all()
    )
    if len(permissions) != len(role.permissions):
        raise HTTPException(status_code=400, detail="Pemissões não existem")

    new_role = Role(
        name=role.name, description=role.description, permissions=permissions
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.post(
    "/users/{user_id}/roles/",
    response_model=RoleCreateModel,
    #dependencies=[Depends(PermissionRequired("assign_role"))],
)
def assign_role_to_user(user_id: int, role_name: str, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    if role in user.roles:
        raise HTTPException(
            status_code=400, detail="O usuário já possui essa permissão"
        )

    user.roles.append(role)
    db.commit()
    return role


@router.get(
    "/",
    response_model=List[RoleCreateModel],
    #dependencies=[Depends(PermissionRequired("view_roles"))],
)
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@router.get(
    "/permissions/",
    response_model=List[PermissionCreateModel],
    #dependencies=[Depends(PermissionRequired("view_permissions"))],
)
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return permissions
