from pydantic import BaseModel


class PermissionCreateModel(BaseModel):
    name: str
    description: str | None = None


class PermissionViewModel(PermissionCreateModel):
    pass
