from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AssignSubCreate(BaseModel):
    assignment_id: int
    student_id: int
    resource_id: int

class AssigSubRead(BaseModel):
    assignment_submission_id:int
    assignment_id: int
    student_id: int
    resource_id: int
    created_at: datetime
    updated_at: datetime 
    model_config = {"from_attributes": True}

class AssignSubUpdate(BaseModel):
    assignment_id: Optional[int]
    student_id: Optional[int]
    resource_id: Optional[int]

