import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.security import get_password_hash

# Use an in-memory SQLite database for testing



def test_create_user(session: Session):
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user = User(email="test@example.com", password_hash=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"



def test_email_uniqueness(session: Session):
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user1 = User(email="unique@example.com", password_hash=hashed_password)
    session.add(user1)
    session.commit()

    user2 = User(email="unique@example.com", password_hash=hashed_password)
    session.add(user2)

    with pytest.raises(IntegrityError): # Expecting an integrity error
        session.commit()
