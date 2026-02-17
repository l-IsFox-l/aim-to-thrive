# Schemas for user
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
import datetime

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
    created_at: datetime.datetime
    updated_at: datetime.datetime