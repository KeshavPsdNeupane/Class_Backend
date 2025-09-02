# schemas.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class UserDetailCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    address_id: int
    ph_number: str
    ph_number_extra: Optional[str] = None
    age: int = Field(ge=0, le=150)
    gender: str



class UserDetailRead(BaseModel):
    user_detail_id: int
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    address_id: int
    ph_number: str
    ph_number_extra: Optional[str] = None
    age: int
    gender: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class UserDetailUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    address_id: Optional[int] = None
    ph_number: Optional[str] = None
    ph_number_extra: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)
    gender: Optional[str] = None
