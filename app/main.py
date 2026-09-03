from fastapi import FastAPI
from app.database import get_all_users
from app.database import create_user
from app.database import get_user_by_id
from app.database import update_user_by_id
import sqlite3
from fastapi import HTTPException
from app.models import User
from app.models import UserUpdate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Isaac security Lab"}

@app.get("/users")
def get_users():
    return get_all_users()

@app.post("/users", status_code=201)
def add_user(user: User):
    try:
        return create_user(user.userID, user.firstName, user.lastName, user.department, user.jobTitle)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

@app.patch("/users/{user_id}")
def update_user(user_id: str, user_update: UserUpdate):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    updates = user_update.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    update_user_by_id(user_id, updates)
    return get_user_by_id(user_id)