import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError

from app.models.user import User
from app.models.task import Task
from app.core.security import get_password_hash


@pytest.fixture(name="user_in_db")
def user_in_db_fixture(session: Session):
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user = User(email="task_test_user@example.com", password_hash=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_create_task(session: Session, user_in_db: User):
    task = Task(title="Test Task", description="This is a test description.", owner_id=user_in_db.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "This is a test description."
    assert task.completed is False
    assert task.owner_id == user_in_db.id
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)
    assert task.created_at.replace(tzinfo=None) <= datetime.now(timezone.utc).replace(tzinfo=None) # Compare naive
    assert task.updated_at.replace(tzinfo=None) <= datetime.now(timezone.utc).replace(tzinfo=None) # Compare naive






def test_task_updated_at_on_creation(session: Session, user_in_db: User):
    initial_time = datetime.now(timezone.utc) - timedelta(seconds=1)
    task = Task(title="Timed Task", owner_id=user_in_db.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.created_at is not None
    assert task.updated_at is not None
    assert task.created_at.replace(tzinfo=None) >= initial_time.replace(tzinfo=None) # Compare naive
    assert task.updated_at.replace(tzinfo=None) >= initial_time.replace(tzinfo=None) # Compare naive
    # updated_at should be very close to created_at on initial creation
    assert task.updated_at >= task.created_at