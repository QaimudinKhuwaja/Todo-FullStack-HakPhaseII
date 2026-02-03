import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()
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
    from app.models.task import Task # Import the Task model
    SQLModel.metadata.create_all(engine)

    # Ensure the `completed` column exists on the `task` table. If the table
    # was created previously without this column, add it now to match the
    # current model definition. This is a lightweight, safe fix for
    # development environments; for production use Alembic migrations.
    alter_sql = """
    ALTER TABLE task
    ADD COLUMN IF NOT EXISTS completed BOOLEAN DEFAULT false
    """
    with engine.begin() as conn:
        conn.execute(text(alter_sql))
    
    # Remove the unused `status` column that causes NOT NULL constraint violations.
    # The backend Task model does not include a status field, so this column is
    # leftover from previous schema iterations. Dropping it fixes schema misalignment.
    drop_status_sql = """
    ALTER TABLE task
    DROP COLUMN IF EXISTS status
    """
    with engine.begin() as conn:
        conn.execute(text(drop_status_sql))

def get_session() -> Generator[Session, None, None]:
    """Dependency to provide a database session."""
    with Session(engine) as session:
        yield session
