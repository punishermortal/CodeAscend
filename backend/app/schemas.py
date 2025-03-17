from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class LinkBase(BaseModel):
    url: str
    description: Optional[str] = None

class LinkCreate(LinkBase):
    pass

class Link(LinkBase):
    id: int

    class Config:
        orm_mode = True

class UserLinkStatusBase(BaseModel):
    is_solved: bool

class UserLinkStatusCreate(UserLinkStatusBase):
    link_id: int
    user_id: int

class UserLinkStatus(UserLinkStatusBase):
    id: int
    link_id: int
    user_id: int
    updated_on: datetime
    link: Link
    user: User

    class Config:
        orm_mode = True
