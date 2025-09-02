from pydantic import BaseModel
class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ReturnMessage(BaseModel):
    access_token: str
    token_type: str = "bearer"
    message: str