from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DepartmentCreate(BaseModel):
    department_name: str
    department_code: str

class DepartmentRead(BaseModel):
    department_id: int
    department_name: str
    department_code:str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    department_code: Optional[str] = None
