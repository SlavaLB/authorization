from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    ADMIN = 'admin'
    USER = 'user'


class UserResponse(BaseModel):
    username: str
    role: Role


class Token(BaseModel):
    access_token: str
    token_type: str
