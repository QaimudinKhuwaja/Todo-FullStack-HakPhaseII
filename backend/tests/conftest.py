import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.event import listen as sqlalchemy_listen
from httpx import AsyncClient, ASGITransport
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Models
from app.models.user import User
from app.models.task import Task

# Resolve forward references for models after all are imported
User.model_rebuild()
Task.model_rebuild()

# Routers
from app.api.endpoints import health, users, auth, protected, tasks
# from app.api.endpoints import items # Removed

from app.core.db import get_session
from app.core.security import get_password_hash
from app.core.auth_utils import delete_session


# ---------------- DB ----------------

@pytest.fixture(name="db_engine", scope="function")
def db_engine_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    def enable_fk(dbapi_conn, _):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    sqlalchemy_listen(engine, "connect", enable_fk)

    yield engine

@pytest.fixture(name="setup_test_db", autouse=True, scope="function")
def setup_test_db_fixture(db_engine):
    from app.models.user import User
    from app.models.task import Task
    SQLModel.metadata.create_all(db_engine)
    yield
    SQLModel.metadata.drop_all(db_engine)




@pytest.fixture(name="session")
def session_fixture(db_engine):
    with Session(db_engine) as session:
        yield session


# ---------------- APP ----------------

import app.core.db # Import db module to patch its engine

@pytest.fixture(name="app")
def app_fixture(session: Session, db_engine): # Add db_engine as a dependency
    fastapi_app = FastAPI()

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers (EXACT COPY OF main.py + tasks)
    fastapi_app.include_router(health.router)
    fastapi_app.include_router(users.router)
    fastapi_app.include_router(auth.router)
    fastapi_app.include_router(protected.router)
    # fastapi_app.include_router(items.router) # Removed
    fastapi_app.include_router(tasks.tasks_router)  # ✅ REQUIRED

    def get_session_override():
        yield session

    fastapi_app.dependency_overrides[get_session] = get_session_override

    # Temporarily patch app.core.db.engine to use the test db_engine
    import app.core.db
    original_engine = app.core.db.engine
    app.core.db.engine = db_engine

    try:
        yield fastapi_app
    finally:
        fastapi_app.dependency_overrides.clear()
        app.core.db.engine = original_engine # Revert the engine patch


# ---------------- CLIENTS ----------------

@pytest.fixture(name="client")
async def client_fixture(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    user = User(
        email=f"test_{uuid.uuid4()}@example.com",
        password_hash=get_password_hash("testpassword"),
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="authenticated_client")
async def authenticated_client_fixture(
    app: FastAPI,
    test_user: User,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        res = await client.post(
            "/login",
            json={"email": test_user.email, "password": "testpassword"},
        )
        assert res.status_code == 200

        session_id = res.json()["session_id"]
        client.headers["X-Session-ID"] = session_id

        yield client
        delete_session(session_id)


@pytest.fixture(name="another_user")
def another_user_fixture(session: Session):
    user = User(
        email=f"another_{uuid.uuid4()}@example.com",
        password_hash=get_password_hash("testpassword"),
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="another_authenticated_client")
async def another_authenticated_client_fixture(
    app: FastAPI,
    another_user: User,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        res = await client.post(
            "/login",
            json={"email": another_user.email, "password": "testpassword"},
        )
        assert res.status_code == 200

        session_id = res.json()["session_id"]
        client.headers["X-Session-ID"] = session_id

        yield client
        delete_session(session_id)
