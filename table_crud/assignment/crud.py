from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import Assignment
from .model import AssignmentUpdate, AssignmentCreate
from database import DB


async def create_new_assignment(data:AssignmentCreate , db:DB):
    new_assignment = Assignment(**data.model_dump())
    db.add(new_assignment)
    try:
        await db.commit()
        await db.refresh(new_assignment)
        return new_assignment
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "department_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Department with id = {data.department_id} not found."
                )  
            elif "teacher_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Teacher with id = {data.teacher_id} not found."
                )  
            elif "teacher_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Section with id = {data.teacher_id} not found."
                ) 
            elif "subject_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Subject with id = {data.subject_id} not found."
                ) 
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )



async def get_assignments(db:DB):
    result = await db.execute(select(Assignment).order_by(Assignment.assignment_id))
    return result.scalars().all()


async def get_assignment_by_id(assignment_id:int , db:DB):
    result = await db.get(Assignment , assignment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Assignment with AssignmentId = {assignment_id} not found"
        )
    return result


async def update_assignment_by_id(assignment_id:int , data:AssignmentUpdate, db:DB):
    db_assignment = await db.get(Assignment , assignment_id)
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Assignment with AssignmentId = {assignment_id} not found"
        )
    for key,value in data.model_dump(exclude_unset=True):
        setattr(db_assignment , key, value)
    try:
        await db.commit()
        await db.refresh(db_assignment)
        return db_assignment
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "department_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Department with id = {data.department_id} not found."
                )  
            elif "teacher_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Teacher with id = {data.teacher_id} not found."
                )  
            elif "teacher_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Section with id = {data.teacher_id} not found."
                ) 
            elif "subject_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Subject with id = {data.subject_id} not found."
                ) 
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )
    


async def delete_assignment_by_id(assignment_id:int , db:DB):
    db_assignment = await db.get(Assignment , assignment_id)
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Assignment with AssignmentId = {assignment_id} not found"
        )
    try:
        await db.delete(db_assignment)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete Assignment: related References exist"
        )