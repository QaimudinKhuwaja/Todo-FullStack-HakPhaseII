import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine
from app.models.user import User
from app.models.todo import Todo

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

@pytest.fixture(name="user_in_db")
def user_in_db_fixture(session: Session):
    user = User(email="test_user@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_create_todo(session: Session, user_in_db: User):
    todo = Todo(title="Buy groceries", user_id=user_in_db.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    assert todo.id is not None
    assert todo.title == "Buy groceries"
    assert todo.user_id == user_in_db.id
    assert todo.created_at is not None
    assert todo.updated_at is not None
    assert not todo.completed


def test_todo_user_relationship(session: Session, user_in_db: User):
    todo1 = Todo(title="Read a book", user_id=user_in_db.id)
    todo2 = Todo(title="Write code", user_id=user_in_db.id)
    session.add(todo1)
    session.add(todo2)
    session.commit()
    session.refresh(user_in_db) # Refresh the user to load the relationship

    assert len(user_in_db.todos) == 2
    assert todo1 in user_in_db.todos
    assert todo2 in user_in_db.todos


def test_foreign_key_constraint(session: Session):
    # Attempt to create a todo with a non-existent user_id
    todo = Todo(title="Invalid todo", user_id=999) # Assuming 999 does not exist
    session.add(todo)

    with pytest.raises(IntegrityError): # Expecting an integrity error
        session.commit()

def test_cascade_delete(session: Session):
    user = User(email="cascade_user@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    todo1 = Todo(title="User's todo 1", user_id=user.id)
    todo2 = Todo(title="User's todo 2", user_id=user.id)
    session.add(todo1)
    session.add(todo2)
    session.commit()
    session.refresh(todo1)
    session.refresh(todo2)

    assert session.get(Todo, todo1.id) is not None
    assert session.get(Todo, todo2.id) is not None

    session.delete(user)
    session.commit()

    assert session.get(Todo, todo1.id) is None
    assert session.get(Todo, todo2.id) is None
