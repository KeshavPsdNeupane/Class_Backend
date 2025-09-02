from datetime import datetime
from pydantic import BaseModel

class AdminCreate(BaseModel):
    user_id:int

class AdminRead(BaseModel):
    user_id:int
    created_at: datetime
    model_config = {"from_attributes": True}