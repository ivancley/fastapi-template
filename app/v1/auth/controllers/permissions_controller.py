from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.v1.utils.db_services import get_db
from app.v1.auth.models.role_model import RoleCreateModel
from app.v1.auth.models.db_models import RoleDB, UserDB ,PermissionDB
from app.v1.auth.models.permission_model import PermissionCreateModel


router = APIRouter( tags=["Admin"])


@router.post(
    "/",
    response_model=PermissionCreateModel,
    status_code=status.HTTP_201_CREATED,
)
def create_permission(permission: PermissionCreateModel, db: Session = Depends(get_db)):
    db_permission = (
        db.query(PermissionDB).filter(PermissionDB.name == permission.name).first()
    )
    if db_permission:
        raise HTTPException(status_code=400, detail="Permissão já existente")
    new_permission = PermissionDB(
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
    db_role = db.query(RoleDB).filter(RoleDB.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Perfil já existe")

    permissions = (
        db.query(PermissionDB).filter(PermissionDB.name.in_(role.permissions)).all()
    )
    if len(permissions) != len(role.permissions):
        raise HTTPException(status_code=400, detail="Não existe esse perfil")

    new_role = RoleDB(
        name=role.name, description=role.description, permissions=permissions
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.post("/users/{user_id}/roles/", response_model=RoleCreateModel)
def assign_role_to_user(user_id: int, role_name: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    role = db.query(RoleDB).filter(RoleDB.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    if role in user.roles:
        raise HTTPException(status_code=400, detail="Usuário já possui o perfil")

    user.roles.append(role)
    db.commit()
    return role


@router.get("/roles/", response_model=List[RoleCreateModel])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(RoleDB).all()
    return roles


@router.get("/", response_model=List[PermissionCreateModel])
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(PermissionDB).all()
    return permissions
