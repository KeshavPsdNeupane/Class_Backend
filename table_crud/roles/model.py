from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class RoleCreate(BaseModel):
    role_name: str

class RoleRead(BaseModel):
    role_name: str
    created_at: datetime
    updated_at: datetime 
    model_config = {"from_attributes": True}

class RoleUpdate(BaseModel):
    role_name: Optional[str] = None
