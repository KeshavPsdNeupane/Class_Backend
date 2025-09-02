from fastapi import APIRouter , status
from database import DB
from .model import AssignmentCreate , AssignmentRead ,AssignmentUpdate
from .crud import(
    get_assignments,
    get_assignment_by_id,
    create_new_assignment,
    update_assignment_by_id,
    delete_assignment_by_id
)


assignment_route = APIRouter(
    prefix="/assignment",
    tags= ["Assignment"]
)

@assignment_route.post("/" , response_model= AssignmentCreate)
async def create_user(data:AssignmentCreate , db:DB):
    return await create_new_assignment(data , db)


@assignment_route.get("/", response_model= list[AssignmentRead])
async def read_assignments(db:DB):
    return await get_assignments(db)

@assignment_route.get("/{assignment_id}" , response_model= AssignmentRead)
async def read_assignment(assignment_id:int , db:DB):
    return await get_assignment_by_id(assignment_id , db)


@assignment_route.put("/{assignment_id}" , response_model= AssignmentUpdate)
async def update_assignment(assignment_id:int , data:AssignmentUpdate , db:DB):
    return await update_assignment_by_id(assignment_id , data ,db)


@assignment_route.delete("/{assignment_id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_assignment(assignment_id:int , db:DB):
    await delete_assignment_by_id(assignment_id , db)
