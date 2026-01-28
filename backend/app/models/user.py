from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    is_active: bool = Field(default=True)

    # Relationship to Todo model (will be defined in Todo model as well)
    # This creates a one-to-many relationship where one User can have many Todos.
    todos: List["Todo"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class UserCreate(SQLModel):
    email: str
    password: str


class UserOut(SQLModel):
    id: int
    email: str
