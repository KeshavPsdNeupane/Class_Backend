from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TeacherCreate(BaseModel):
    user_id:int

class TeacherRead(BaseModel):
    user_id:int
    created_at: datetime
    model_config = {"from_attributes": True}