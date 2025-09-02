from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    user_id:int
    section_id:int
    batch_name:str

class StudentRead(BaseModel):
    user_id:int
    section_id:int
    batch_name:str
    created_at: datetime
    model_config = {"from_attributes": True}