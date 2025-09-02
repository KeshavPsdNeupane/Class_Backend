from typing import Optional
from pydantic import BaseModel , EmailStr
from datetime import datetime
from table_crud.address.model import AddressCreate


class UserCreate(BaseModel):
    role_name:str
    user_detail_id:int
    email_id:EmailStr
    hashed_pw:str
    is_active:Optional[bool] = True
    

class UserRead(BaseModel):
    user_id:int
    role_name:str
    user_detail_id:int
    email_id:EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}



class UserUpdate(BaseModel):
    role_id:Optional[int] = None
    user_detail_id:Optional[int] = None
    email_id:Optional[EmailStr] = None
    is_active:Optional[bool] = True