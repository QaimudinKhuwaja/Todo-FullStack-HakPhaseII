# import os
# from typing import Generator
# from sqlmodel import SQLModel, create_engine, Session
# from sqlalchemy import text
# from dotenv import load_dotenv

# # Import models at the top to ensure they are registered early
# from app.models.user import User
# from app.models.task import Task  # Import the Task model

# load_dotenv()

# # Define the database URL. This should ideally come from environment variables.
# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is not set")

# # Create the engine with SSL support for Neon Postgres
# engine = create_engine(
#     DATABASE_URL,
#     echo=True,  # Set to False in production to avoid logging sensitive info
#     connect_args={"sslmode": "require"}  # Enforce SSL for production DBs like Neon
# )

# def create_db_and_tables():
#     """Creates all tables defined in SQLModel metadata."""
#     # Create tables based on models
#     SQLModel.metadata.create_all(engine)

#     # Ensure the `completed` column exists on the `task` table.
#     alter_sql = """
#     ALTER TABLE task
#     ADD COLUMN IF NOT EXISTS completed BOOLEAN DEFAULT false
#     """
#     with engine.begin() as conn:
#         conn.execute(text(alter_sql))
    
#     # Remove the unused `status` column if it exists.
#     drop_status_sql = """
#     ALTER TABLE task
#     DROP COLUMN IF EXISTS status
#     """
#     with engine.begin() as conn:
#         conn.execute(text(drop_status_sql))

# def get_session() -> Generator[Session, None, None]:
#     """Dependency to provide a database session."""
#     with Session(engine) as session:
#         yield session



import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from dotenv import load_dotenv

# Import models early
from app.models.user import User
from app.models.task import Task

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Engine with Neon pooled fixes
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("ENV", "development") == "development",  # Log SQL in dev only
    connect_args={
        "sslmode": "require",         # SSL forced
        "channel_binding": "require"  # Neon pooled ke liye zaroori
    }
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Safe ALTERs
    with engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE task
            ADD COLUMN IF NOT EXISTS completed BOOLEAN DEFAULT false
        """))
        conn.execute(text("""
            ALTER TABLE task
            DROP COLUMN IF EXISTS status
        """))

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session