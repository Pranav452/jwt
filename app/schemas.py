from pydantic import BaseModel, EmailStr
from datetime import datetime
class UserBase(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class GroupsBase(BaseModel):
    name: str
    created_by: int
    members: list[int]
    created_at: datetime

class GroupsCreate(GroupsBase):
    pass

class GroupsOut(GroupsBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True