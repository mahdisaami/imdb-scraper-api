from typing import Union, Optional

from pydantic import BaseModel

class BaseUser(BaseModel):
    username: str
    email: str | None = None


class UserCreate(BaseUser):
    password: str

class UserRead(BaseUser):
    id : int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    message: str
    user: UserRead

class UserPatch(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None

    class Config:
        orm_mode = True