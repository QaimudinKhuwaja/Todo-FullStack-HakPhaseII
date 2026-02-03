from __future__ import annotations
from datetime import datetime
from typing import  Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from app.models.task import Task


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    is_active: bool = Field(default=True)


class UserCreate(SQLModel):
    email: str
    password: str


class UserOut(SQLModel):
    id: int
    email: str
