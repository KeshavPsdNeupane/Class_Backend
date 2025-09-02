from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dmodels import AssignmentSubmission
from .model import AssignSubCreate, AssignSubUpdate
from database import DB



async def create_new_assign_sub(data:AssignSubCreate, db:DB):
    new_assign_sub = AssignmentSubmission(**data.model_dump())
    db.add(new_assign_sub)
    try:
        await db.commit()
        await db.refresh(new_assign_sub)
        return new_assign_sub
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "assignment_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Assignment with id = {data.assignment_id} not found."
                )  
            elif "student_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Student with id = {data.student_id} not found."
                )  
            elif "resource_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Resource with id = {data.resource_id} not found."
                ) 
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )



async def get_assignment_subs(db:DB):
    result = await db.execute(select(AssignmentSubmission).order_by(AssignmentSubmission.assignment_submission_id))
    return result.scalars().all()

async def get_assign_sub_by_id(assign_sub_id:int , db:DB):
    result = await db.get(AssignmentSubmission , assign_sub_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Assignment Submission with AssignmentSubmissionId = {assign_sub_id} not found"
        )
    return result



async def update_assign_sub_by_id(assign_sub_id:int,data:AssignSubUpdate , db:DB):
    db_assign_sub = db.get(AssignmentSubmission , assign_sub_id)
    if not db_assign_sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Assignment Submission with AssignmentSubmissionId = {assign_sub_id} not found"
        )
    for key,value in data.model_dump(exclude_unset=True):
        setattr(db_assign_sub , key, value)
    try:
        await db.commit()
        await db.refresh(db_assign_sub)
        return db_assign_sub
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if "foreign key" in error_msg:
            if "assignment_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Assignment with id = {data.assignment_id} not found."
                )  
            elif "student_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Student with id = {data.student_id} not found."
                )  
            elif "resource_id" in error_msg:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Resource with id = {data.resource_id} not found."
                ) 
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= "Referencial integerty invalid"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )
    

async def delete_assignment_by_id(assign_sub_id:int , db:DB):
    db_assign_sub = await db.get(AssignmentSubmission , assign_sub_id)
    if not db_assign_sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Assignment Submission with AssignmentSubmissionId = {assign_sub_id} not found"
        )
    try:
        await db.delete(db_assign_sub)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Database Error"
        )