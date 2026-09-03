from pydantic import BaseModel

class User(BaseModel):
    userID: str
    firstName: str
    lastName: str
    department: str
    jobTitle: str

class UserUpdate(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    department: str | None = None
    jobTitle: str | None = None