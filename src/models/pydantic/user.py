# Schemas for user
from pydantic import BaseModel, EmailStr
import uuid

class UserCreate(BaseModel):
    """Creating user"""
    name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Read existing user"""
    id: uuid.UUID
    name: str
    email: str