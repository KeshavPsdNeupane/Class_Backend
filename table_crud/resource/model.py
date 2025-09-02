from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResourceCreate(BaseModel):
    user_id:int
    path:str

class ResourceRead(BaseModel):
    resource_id:int
    user_id:int
    path:str
    created_at:datetime
    updated_at:datetime
    model_config = {"from_attributes": True}
