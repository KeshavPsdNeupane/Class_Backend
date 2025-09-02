from pydantic import BaseModel

class ReturnMessage(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    message: str
    role:str
    is_first_login: bool


