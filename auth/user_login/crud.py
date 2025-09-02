from sqlalchemy.future import select
from database import DB
from pydantic import EmailStr
from dmodels import User



async def get_user_by_email(email_id:EmailStr , db:DB):
    result = await db.execute(select(User).where(User.email_id == email_id))
    return result.scalar_one_or_none()



async def get_user_with_id(user_id:int , db:DB):
    return  await db.get(User, int(user_id))


async def handle_first_login(user: User, db: DB) -> bool:
    # if user.is_first_login:
    #     user.is_first_login = False
    #     await db.merge(user) 
    #     await db.commit()
    #     await db.refresh(user)
    #     return True
    return True    # this must be false for testing
