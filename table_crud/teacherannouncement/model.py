from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TeacherAnnouncementCreate(BaseModel):
    teacher_id:int
    department_id:int
    section_id:int
    subject_id:int
    title:str
    description:str

class TeacherAnnouncementRead(BaseModel):
    teacher_announcement_id:int
    teacher_id:int
    department_id:int
    section_id:int
    subject_id:int
    title:str
    description:str
    created_at: datetime
    updated_at: datetime 
    model_config = {"from_attributes": True}