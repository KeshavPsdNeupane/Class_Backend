from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AdminAnnouncementCreate(BaseModel):
    admin_id:int
    title:str
    description:str


class AdminAnnouncementRead(BaseModel):
    admin_id:int
    title:str
    description:str
    created_at: datetime
    updated_at: datetime 
    model_config = {"from_attributes": True}

