from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import DB
from dmodels import Department
from .model import DepartmentCreate, DepartmentUpdate

async def create_new_department(data: DepartmentCreate, db: DB):
    cleaned_data = {
        field: (getattr(data, field).strip() if isinstance(getattr(data, field), str) else getattr(data, field))
        for field in type(data).model_fields
    }
    new_dept = Department(**cleaned_data)
    db.add(new_dept)
    try:
        await db.commit()
        await db.refresh(new_dept)
        return new_dept
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if 'unique' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                  detail="Department name must be unique"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
        )



async def get_departments(db: DB):
    result = await db.execute(select(Department).order_by(Department.department_id))
    return result.scalars().all()



async def get_department_by_id(dept_id: int, db: DB):
    result = await db.get(Department, dept_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id = {dept_id} not found"
        )
    return result



async def update_department_by_id(dept_id: int, data: DepartmentUpdate, db: DB):
    db_dept = await db.get(Department, dept_id)
    if not db_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id = {dept_id} not found"
        )
    updates = {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.model_dump(exclude_unset=True).items()
    }
    for key, value in updates.items():
        setattr(db_dept, key, value)
    try:
        await db.commit()
        await db.refresh(db_dept)
        return db_dept
    except IntegrityError as e:
        await db.rollback()
        error_msg:str = str(e.orig).lower()
        if 'unique' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                  detail=f"Department name {data.department_name} already exist"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database Error"
        )



async def delete_department_by_id(dept_id: int, db: DB):
    db_dept = await db.get(Department, dept_id)
    if not db_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id = {dept_id} not found"
        )
    try:
        await db.delete(db_dept)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete Department: related Semesters exist."
        )