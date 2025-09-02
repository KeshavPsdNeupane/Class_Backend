from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SectionCreate(BaseModel):
    section_name: str
    semester_id: int

class SectionRead(BaseModel):
    section_id: int
    section_name: str
    semester_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class SectionUpdate(BaseModel):
    section_name: Optional[str] = None
    semester_id: Optional[int] = None
