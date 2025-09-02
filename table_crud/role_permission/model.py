from pydantic import BaseModel
from datetime import datetime

class RolePermissionCreateDelete(BaseModel):
    role_name:str
    permission_name:str

class RolePermissionRead(BaseModel):
    role_name:str
    permission_name:str
    created_at:datetime
    model_config = {"from_attributes": False}


class RolePermissionReadByRole(BaseModel):
    permission_name:str
    created_at:datetime
    updated_at:datetime
    model_config = {"from_attributes": True}


class RolePermissionReadByPermission(BaseModel):
    role_name:str
    created_at:datetime
    updated_at:datetime
    model_config = {"from_attributes": True}


