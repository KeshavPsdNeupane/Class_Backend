from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TeachAssignCreate(BaseModel):
    teacher_id: int
    subject_id: int
    section_id: int

class TeachAssignRead(BaseModel):
    teacher_id: int
    subject_id: int
    section_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class TeachAssignDelete(BaseModel):
    teacher_id: int
    subject_id: int
    section_id: int