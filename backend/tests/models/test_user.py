import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine
from app.models.user import User

# Use an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    
    # Enable foreign key constraints for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_create_user(session: Session):
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.created_at is not None


def test_email_uniqueness(session: Session):
    user1 = User(email="unique@example.com")
    session.add(user1)
    session.commit()

    user2 = User(email="unique@example.com")
    session.add(user2)

    with pytest.raises(IntegrityError): # Expecting an integrity error
        session.commit()
