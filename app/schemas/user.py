from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate (BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr
    password: str
    is_disabled: bool = False

class UserLogin (BaseModel):
    email: EmailStr
    password: str

class UserUpdate (BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserDelete(BaseModel):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead (BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    
    
