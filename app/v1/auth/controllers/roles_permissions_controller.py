from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.v1.utils.db_services import get_db
from app.v1.auth.models.db_models import UserDB, RoleDB, PermissionDB
from app.v1.auth.models.role_model import RoleCreateModel
from app.v1.auth.models.permission_model import PermissionCreateModel

from app.v1.auth.security import AuthSecurity
from app.v1.auth.permissions import PermissionRequired, RoleRequired

router = APIRouter(tags=["Admin"])

auth = AuthSecurity()


@router.post(
    "/permissions/",
    response_model=PermissionCreateModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleRequired("superuser"))],
)
def create_permission(permission: PermissionCreateModel, db: Session = Depends(get_db)):
    db_permission = (
        db.query(PermissionDB).filter(PermissionDB.name == permission.name).first()
    )
    if db_permission:
        raise HTTPException(status_code=400, detail="A permissão já existe")
    new_permission = PermissionDB(
        name=permission.name, description=permission.description
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission


@router.post(
    "/",
    response_model=RoleCreateModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleRequired("superuser"))],
)
def create_role(role: RoleCreateModel, db: Session = Depends(get_db)):
    db_role = db.query(RoleDB).filter(RoleDB.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="O perfil já existe")

    permissions = (
        db.query(PermissionDB).filter(PermissionDB.name.in_(role.permissions)).all()
    )
    if len(permissions) != len(role.permissions):
        raise HTTPException(status_code=400, detail="Pemissões não existem")

    new_role = RoleDB(
        name=role.name, description=role.description, permissions=permissions
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.post(
    "/users/{user_id}/roles/",
    response_model=RoleCreateModel,
    dependencies=[Depends(RoleRequired("superuser"))],
)
def assign_role_to_user(user_id: int, role_name: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    role = db.query(RoleDB).filter(RoleDB.name == role_name).first()
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
    dependencies=[Depends(RoleRequired("superuser"))],
)
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(RoleDB).all()
    return roles


@router.get(
    "/permissions/",
    response_model=List[PermissionCreateModel],
    dependencies=[Depends(RoleRequired("superuser"))],
)
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(PermissionDB).all()
    return permissions
