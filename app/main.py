from fastapi import FastAPI
from app.database import get_all_users
import sqlite3

app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Isaac security Lab"}

@app.get("/users")
def get_users():
    return get_all_users()

