from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.v1.auth.security import AuthSecurity
from app.v1.auth.models import UsuarioDB
from app.v1.utils.db_services import get_db


def PermissionRequired(permission: str):
    auth = AuthSecurity()

    def permission_checker(
        current_user: UsuarioDB = Depends(auth.get_current_user),
        db: Session = Depends(get_db),
    ):
        if not auth.has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para essa ação",
            )
        return True

    return permission_checker
