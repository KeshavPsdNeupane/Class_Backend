# route.py

from fastapi import APIRouter, status
from typing import List
from database import DB
from .model import SectionCreate, SectionRead, SectionUpdate
from .crud import (
    create_section,
    get_sections,
    get_section_by_id,
    update_section_by_id,
    delete_section_by_id,
)

section_route = APIRouter(prefix="/sections", tags=["Sections"])


@section_route.post("/", response_model=SectionRead)
async def create_section_endpoint(data: SectionCreate, db: DB):
    return await create_section(data, db)


@section_route.get("/", response_model=List[SectionRead])
async def read_sections(db: DB):
    return await get_sections(db)


@section_route.get("/{section_id}", response_model=SectionRead)
async def read_section(section_id: int, db: DB):
    return await get_section_by_id(section_id, db)


@section_route.put("/{section_id}", response_model=SectionRead)
async def update_section(section_id: int, data: SectionUpdate, db: DB):
    return await update_section_by_id(section_id, data, db)


@section_route.delete("/{section_id}" ,status_code= status.HTTP_204_NO_CONTENT)
async def delete_section(section_id: int, db: DB):
    await delete_section_by_id(section_id, db)
