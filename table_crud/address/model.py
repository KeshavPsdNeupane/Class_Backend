from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AddressCreate(BaseModel):
    province_name: str
    district_name: str
    village_city_name: str
    ward_number: int
    place_name: str


class AddressRead(BaseModel):
    address_id: int
    province_name: str
    district_name: str
    village_city_name: str
    ward_number: int
    place_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AddressUpdate(BaseModel):
    province_name: Optional[str] = None
    district_name: Optional[str] = None
    village_city_name: Optional[str] = None
    ward_number: Optional[int] = None
    place_name: Optional[str] = None
