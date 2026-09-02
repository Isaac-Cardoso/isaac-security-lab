from fastapi import FastAPI
from app.database import get_all_users
from app.database import create_user
import sqlite3
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Isaac security Lab"}

@app.get("/users")
def get_users():
    return get_all_users()

class User(BaseModel):
    userID: str
    firstName: str
    lastName: str
    department: str
    jobTitle: str

@app.post("/users")
def add_user(user: User):
    return create_user(user.userID, user.firstName, user.lastName, user.department, user.jobTitle)


