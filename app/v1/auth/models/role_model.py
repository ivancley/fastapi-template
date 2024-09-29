from pydantic import BaseModel
from .permission_model import PermissionViewModel

class RoleCreateModel(BaseModel):
    name: str
    description: str | None = None
    permissions: list[PermissionViewModel] = []


class RoleViewModel(BaseModel):
    id: int
    name: str
    description: str | None = None
