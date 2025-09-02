from fastapi import FastAPI
from table_crud import basic_table_route
from auth import auth_route
import uvicorn
app = FastAPI()
from auth import (
    Any_Role_Scope,
    Admin_Scope,
    Teacher_Scope,
    Student_Scope
)

@app.get("/")
def getapp():
    return {"hello":"world"}



@app.get("/test/")
def test2456(User:Any_Role_Scope ):
    return User

@app.get("/test2/")
def test24562(User:Admin_Scope):
    return User

@app.get("/test3/")
def test24563(User:Teacher_Scope):
    return User

@app.get("/test4/")
def test24564(User:Student_Scope):
    return User

app.include_router(auth_route)
app.include_router(basic_table_route)


if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0',port=8000,reload=True)