import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session

# Define the database URL. This should ideally come from environment variables.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True) # echo=True for logging SQL statements

def create_db_and_tables():
    """Creates all tables defined in SQLModel metadata."""
    # This should be called once, e.g., at application startup or in a migration script.
    # We will import the models here to ensure they are registered with SQLModel's metadata
    # for table creation.
    from app.models.user import User
    from app.models.todo import Todo
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency to provide a database session."""
    with Session(engine) as session:
        yield session
