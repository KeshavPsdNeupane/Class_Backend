from fastapi import APIRouter , status
from database import DB
from .model import AssignSubCreate,AssignSubUpdate,AssigSubRead
from .crud import (
    get_assignment_subs,
    get_assign_sub_by_id,
    create_new_assign_sub,
    update_assign_sub_by_id,
    delete_assignment_by_id,
)


assign_sub_route = APIRouter(
    prefix="/assignsub",
    tags=["Assignment Submission"]
)


@assign_sub_route.post("/" , response_model= AssignSubCreate)
async def create_assgn_sub(data:AssignSubCreate, db:DB):
    return create_new_assign_sub(data , db)



@assign_sub_route.get("" , response_model= list[AssigSubRead])
async def read_assign_subs(db:DB):
    return await get_assignment_subs(db)

@assign_sub_route.get("/{assign_sub_id}" , response_model= AssigSubRead)
async def read_assign_sub(assign_sub_id:int , db:DB):
    return await get_assign_sub_by_id(assign_sub_id , db)


@assign_sub_route.put("/{assign_sub_id}" , response_model= AssignSubUpdate)
async def update_assign_sub(assign_sub_id:int, data:AssignSubUpdate , db:DB):
    return await update_assign_sub_by_id(assign_sub_id , data , db)

@assign_sub_route.delete("/{assign_sub_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_assign_sub(assign_sub_id:int , db:DB):
    await delete_assignment_by_id(assign_sub_id ,db)