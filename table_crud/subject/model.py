from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SubjectCreate(BaseModel):
    subject_name: str
    subject_code: str
    semester_id:int
    resource_id: Optional[int] = None

class SubjectRead(BaseModel):
    subject_id:int
    subject_name: str
    subject_code: str
    semester_id:int
    resource_id: Optional[int] = None
    created_at:datetime
    updated_at:datetime
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class SubjectUpdate(BaseModel):
    subject_name: Optional[str] = None
    subject_code: Optional[str] = None
    semester_id: Optional[int] = None
    resource_id: Optional[int] = None

