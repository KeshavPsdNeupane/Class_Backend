from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PermissionCreate(BaseModel):
    permission_name: str

class PermissionRead(BaseModel):
    permission_name: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class PermissionUpdate(BaseModel):
    permission_name: Optional[str] = None
