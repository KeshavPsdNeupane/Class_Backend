from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SemesterCreate(BaseModel):
    semester_name: str
    department_id: int

class SemesterRead(BaseModel):
    semester_id: int
    semester_name: str
    department_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class SemesterUpdate(BaseModel):
    semester_name: Optional[str] = None
    department_id: Optional[int] = None
