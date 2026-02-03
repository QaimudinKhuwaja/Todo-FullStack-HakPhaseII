import pytest
from httpx import AsyncClient
import uuid
from sqlmodel import Session, select

from app.api.endpoints.tasks import create_task # Import the endpoint function for direct testing (optional but useful)
from app.core.db import get_session
from app.models.user import User
from app.models.task import Task
from app.core.security import get_password_hash
from app.core.auth_utils import delete_session # Import for session cleanup


# Fixtures are already defined in conftest.py and test_items.py, but for clarity and isolated testing,
# we might redefine some or ensure they are available through conftest.
# For this task, we assume conftest.py provides 'app', 'session', 'test_user', 'authenticated_client', 'another_user', 'another_authenticated_client'

@pytest.fixture(name="test_user_tasks")
def test_user_tasks_fixture(session: Session, test_user: User):
    task1 = Task(title="Test Task 1", description="Desc 1", owner_id=test_user.id)
    task2 = Task(title="Test Task 2", description="Desc 2", owner_id=test_user.id)
    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task1)
    session.refresh(task2)
    return [task1, task2]

@pytest.fixture(name="another_user_tasks")
def another_user_tasks_fixture(session: Session, another_user: User):
    task3 = Task(title="Another User Task 1", description="Desc 3", owner_id=another_user.id)
    session.add(task3)
    session.commit()
    session.refresh(task3)
    return [task3]

@pytest.mark.asyncio
async def test_create_task(authenticated_client: AsyncClient, session: Session, test_user: User):
    task_data = {"title": "New Task", "description": "Description for new task"}
    response = await authenticated_client.post("/tasks/", json=task_data) # Changed to /tasks/

    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["owner_id"] == test_user.id
    assert created_task["completed"] is False
    assert "id" in created_task
    assert "created_at" in created_task
    assert "updated_at" in created_task

    # Verify the task is in the database
    db_task = session.get(Task, created_task["id"])
    assert db_task is not None
    assert db_task.title == task_data["title"]
    assert db_task.owner_id == test_user.id

@pytest.mark.asyncio
async def test_create_task_unauthenticated(client: AsyncClient):
    task_data = {"title": "Unauthenticated Task", "description": "Should not be created"}
    response = await client.post("/tasks/", json=task_data) # Changed to /tasks/
    assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_create_task_without_title(authenticated_client: AsyncClient):
    task_data = {"title": "", "description": "Task without title"}
    response = await authenticated_client.post("/tasks/", json=task_data) # Changed to /tasks/
    assert response.status_code == 422  # Unprocessable Entity
    assert "String should have at least 1 character" in response.json()["detail"][0]["msg"]

@pytest.mark.asyncio
async def test_read_tasks(authenticated_client: AsyncClient, another_authenticated_client: AsyncClient, test_user: User, another_user: User, test_user_tasks, another_user_tasks):
    # test_user_tasks and another_user_tasks are created by fixtures

    response = await authenticated_client.get("/tasks/") # Changed to /tasks/
    assert response.status_code == 200
    tasks = response.json()

    assert len(tasks) == len(test_user_tasks)
    assert all(task["owner_id"] == test_user.id for task in tasks)
    assert {task["title"] for task in tasks} == {"Test Task 1", "Test Task 2"}

    # Verify another user only sees their tasks
    response = await another_authenticated_client.get("/tasks/") # Changed to /tasks/
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == len(another_user_tasks)
    assert all(task["owner_id"] == another_user.id for task in tasks)
    assert {task["title"] for task in tasks} == {"Another User Task 1"}

@pytest.mark.asyncio
async def test_read_tasks_unauthenticated(client: AsyncClient):
    response = await client.get("/tasks/") # Changed to /tasks/
    assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_read_single_task(authenticated_client: AsyncClient, test_user_tasks: list[Task]):
    task = test_user_tasks[0]
    response = await authenticated_client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task.id
    assert retrieved_task["title"] == task.title
    assert retrieved_task["owner_id"] == task.owner_id

@pytest.mark.asyncio
async def test_read_single_task_not_found(authenticated_client: AsyncClient):
    non_existent_id = 999999
    response = await authenticated_client.get(f"/tasks/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

@pytest.mark.asyncio
async def test_read_single_task_of_another_user_forbidden(authenticated_client: AsyncClient, another_user_tasks: list[Task]):
    task = another_user_tasks[0]
    response = await authenticated_client.get(f"/tasks/{task.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to access this task"

@pytest.mark.asyncio
async def test_update_task_full(authenticated_client: AsyncClient, session: Session, test_user_tasks: list[Task]):
    task = test_user_tasks[0]
    update_data = {"title": "Updated Title", "description": "Updated Description", "completed": True}
    response = await authenticated_client.patch(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["id"] == task.id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    assert updated_task["completed"] == update_data["completed"]

    db_task = session.get(Task, task.id)
    assert db_task.title == update_data["title"]
    assert db_task.description == update_data["description"]
    assert db_task.completed == update_data["completed"]

@pytest.mark.asyncio
async def test_update_task_partial(authenticated_client: AsyncClient, session: Session, test_user_tasks: list[Task]):
    task = test_user_tasks[1]
    update_data = {"description": "Only description updated"}
    response = await authenticated_client.patch(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["id"] == task.id
    assert updated_task["description"] == update_data["description"]
    assert updated_task["title"] == task.title # Title should remain unchanged

    db_task = session.get(Task, task.id)
    assert db_task.description == update_data["description"]
    assert db_task.title == task.title

@pytest.mark.asyncio
async def test_update_task_not_found(authenticated_client: AsyncClient):
    non_existent_id = 999999
    update_data = {"title": "Should not update"}
    response = await authenticated_client.patch(f"/tasks/{non_existent_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

@pytest.mark.asyncio
async def test_update_task_of_another_user_forbidden(authenticated_client: AsyncClient, another_user_tasks: list[Task]):
    task = another_user_tasks[0]
    update_data = {"title": "Attempt to update another user's task"}
    response = await authenticated_client.patch(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to update this task"

@pytest.mark.asyncio
async def test_delete_task(authenticated_client: AsyncClient, session: Session, test_user_tasks: list[Task]):
    task_to_delete = test_user_tasks[0]
    response = await authenticated_client.delete(f"/tasks/{task_to_delete.id}")
    assert response.status_code == 204

    db_task = session.get(Task, task_to_delete.id)
    assert db_task is None

@pytest.mark.asyncio
async def test_delete_task_not_found(authenticated_client: AsyncClient):
    non_existent_id = 999999
    response = await authenticated_client.delete(f"/tasks/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

@pytest.mark.asyncio
async def test_delete_task_of_another_user_forbidden(authenticated_client: AsyncClient, session: Session, another_user_tasks: list[Task]):
    task_to_delete = another_user_tasks[0]
    response = await authenticated_client.delete(f"/tasks/{task_to_delete.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to delete this task"

    # Verify task still exists in DB
    db_task = session.get(Task, task_to_delete.id)
    assert db_task is not None
