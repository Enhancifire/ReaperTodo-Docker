from pydantic import BaseModel
from typing import Union, List
from datetime import datetime

class TaskBase(BaseModel):
    title: str

class TaskCreate(TaskBase):
    owner_id: int
    due: Union[datetime, None] = None

class Task(TaskBase):
    id: int
    auth_token: str
    due: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    tasks: List[Task] = []

    class Config:
        orm_mode = True
