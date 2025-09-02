from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class AddressData(BaseModel):
    province_name: str
    district_name: str
    village_city_name: str
    ward_number: int
    place_name: str


class UserDetailData(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    ph_number: str
    ph_number_extra: Optional[str] = None
    age: int = Field(ge=0, le=150)
    gender: str


class UserRestDetail(BaseModel):
    email_id:EmailStr
    role_name:str
    is_active:Optional[bool] = True


class StudentOnlyDetail(BaseModel):
    batch_no:str
    section_id:int


class UserCreateData(BaseModel):
    user_detail_data:UserDetailData
    address_data:AddressData
    user_rest_detail:UserRestDetail
    studentOnly:Optional[StudentOnlyDetail] = None


class Respone(BaseModel):
    message:str