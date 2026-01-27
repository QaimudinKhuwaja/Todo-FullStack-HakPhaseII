from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, func

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
    )

    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="todos")
