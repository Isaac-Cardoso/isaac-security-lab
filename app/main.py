import sqlite3
from fastapi import FastAPI, HTTPException
from app.database import (
    assign_role_to_user,
    create_user,
    get_all_roles,
    get_all_users,
    get_role_by_id,
    get_roles_for_user,
    get_user_by_id,
    remove_role_from_user,
    set_lifecycle_state,
    update_user_by_id,
)

from app.models import User, UserUpdate

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

@app.post("/users/{user_id}/disable")
def disable_user(user_id: str):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    set_lifecycle_state(user_id, "disabled")
    return get_user_by_id(user_id)

@app.post("/users/{user_id}/reactivate")
def enable_user(user_id: str):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    set_lifecycle_state(user_id, "active")
    return get_user_by_id(user_id)

@app.post("/users/{user_id}/roles/{role_id}")
def assign_role(user_id: str, role_id: int):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_role = get_role_by_id(role_id)
    if not existing_role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    try:
        assign_role_to_user(user_id, role_id)
        return get_roles_for_user(user_id)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Role already assigned to user"
        )

@app.get("/users/{user_id}/roles")
def get_user_roles(user_id: str):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return get_roles_for_user(user_id)

@app.delete("/users/{user_id}/roles/{role_id}")
def remove_role(user_id: str, role_id: int):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_role = get_role_by_id(role_id)
    if not existing_role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    removed =remove_role_from_user(user_id, role_id)
    if not removed:
        raise HTTPException(
            status_code=404,
            detail="Role not assigned to user"
        )
    
    return get_roles_for_user(user_id)

@app.get("/roles")
def get_roles():
    return get_all_roles()