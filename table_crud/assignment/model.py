from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AssignmentCreate(BaseModel):
    teacher_id:int
    department_id:int
    section_id:int
    subject_id:int
    title:str
    description:str
    deadline_time:Optional[str] = None
    has_deadline_reached:Optional[bool] = False


class AssignmentRead(BaseModel):
    assignment_id:int
    teacher_id:int
    department_id:int
    section_id:int
    subject_id:int
    title:str
    description:str
    has_deadline_reached:Optional[bool] = False
    deadline_time:Optional[str] = None
    created_at: datetime
    updated_at: datetime 
    model_config = {"from_attributes": True}



class AssignmentUpdate(BaseModel):
    teacher_id: Optional[int] = None
    department_id: Optional[int] = None
    section_id: Optional[int] = None
    subject_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    deadline_time: Optional[str] = None
    has_deadline_reached: Optional[bool] = None
