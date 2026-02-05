from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Field, Session, SQLModel, select

from ...core.db import get_session
from ...models.task import Task, TaskRead, TaskUpdate
from ...models.user import User
from ...api.middlewares.auth_middleware import get_current_user

router = APIRouter(tags=["Tasks"])

# Define a new TaskCreate model for the request body, excluding owner_id
class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=255, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

@router.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(*, session: Session = Depends(get_session), current_user: User = Depends(get_current_user), task: TaskCreate) -> TaskRead:
    """
    Create a new task for the current authenticated user.

    Args:
        session: The database session.
        current_user: The authenticated user creating the task.
        task: The task data to create.

    Returns:
        The newly created task.

    Raises:
        HTTPException: If the task title is empty (handled by Pydantic validation).
    """
    db_task = Task.model_validate(task, update={"owner_id": current_user.id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[TaskRead])
def read_tasks(*, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)) -> List[TaskRead]:
    """
    Retrieve all tasks owned by the current authenticated user.

    Args:
        session: The database session.
        current_user: The authenticated user whose tasks are to be retrieved.

    Returns:
        A list of tasks owned by the current user.
    """
    tasks = session.exec(
        select(Task).where(Task.owner_id == current_user.id)
    ).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(*, session: Session = Depends(get_session), current_user: User = Depends(get_current_user), task_id: int) -> TaskRead:
    """
    Retrieve a single task by its ID, ensuring it belongs to the current authenticated user.

    Args:
        session: The database session.
        current_user: The authenticated user requesting the task.
        task_id: The ID of the task to retrieve.

    Returns:
        The requested task.

    Raises:
        HTTPException: 404 Not Found if the task does not exist.
        HTTPException: 403 Forbidden if the task does not belong to the current user.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this task")
    return task

@router.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(*, session: Session = Depends(get_session), current_user: User = Depends(get_current_user), task_id: int, task_update: TaskUpdate) -> TaskRead:
    """
    Update an existing task, ensuring it belongs to the current authenticated user.
    Allows for partial updates.

    Args:
        session: The database session.
        current_user: The authenticated user attempting to update the task.
        task_id: The ID of the task to update.
        task_update: The task data to update.

    Returns:
        The updated task.

    Raises:
        HTTPException: 404 Not Found if the task does not exist.
        HTTPException: 403 Forbidden if the task does not belong to the current user.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this task")
    
    # Update task attributes with values from task_update
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(*, session: Session = Depends(get_session), current_user: User = Depends(get_current_user), task_id: int) -> None:
    """
    Delete a task, ensuring it belongs to the current authenticated user.

    Args:
        session: The database session.
        current_user: The authenticated user attempting to delete the task.
        task_id: The ID of the task to delete.

    Returns:
        A success message (204 No Content).

    Raises:
        HTTPException: 404 Not Found if the task does not exist.
        HTTPException: 403 Forbidden if the task does not belong to the current user.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this task")
    
    session.delete(task)
    session.commit()
























# from typing import List, Optional

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel import Field, Session, SQLModel, select

# from ...core.db import get_session
# from ...models.task import Task, TaskRead, TaskUpdate
# from ...models.user import User
# from ...api.middlewares.auth_middleware import get_current_user
# from app.core import db

# router = APIRouter(tags=["Tasks"])


# # Request model (owner_id intentionally excluded)
# class TaskCreate(SQLModel):
#     title: str = Field(min_length=1, max_length=255, index=True)
#     description: Optional[str] = Field(default=None, max_length=1000)
#     completed: bool = Field(default=False)


# # ✅ CREATE TASK
# @router.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
# def create_task(
#     *,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
#     task: TaskCreate,
# ) -> TaskRead:

#     db_task = Task.model_validate(
#         task,
#         update={"owner_id": current_user.id}
#     )

#     session.add(db_task)
#     session.commit()
#     session.refresh(db_task)

#     return db_task


# # ✅ GET ALL TASKS
# @router.get("/tasks/", response_model=List[TaskRead])
# def read_tasks(
#     *,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ) -> List[TaskRead]:

#     statement = select(Task).where(Task.owner_id == current_user.id)
#     tasks = session.exec(statement).all()

#     return tasks


# # ✅ GET SINGLE TASK
# @router.get("/tasks/{task_id}", response_model=TaskRead)
# def read_task(
#     *,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
#     task_id: int,
# ) -> TaskRead:

#     task = session.get(Task, task_id)

#     if not task:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Task not found"
#         )

#     if task.owner_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not allowed"
#         )

#     return task


# # ✅ UPDATE TASK
# @router.patch("/tasks/{task_id}", response_model=TaskRead)
# def update_task(
#     *,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
#     task_id: int,
#     task_update: TaskUpdate,
# ) -> TaskRead:

#     task = session.get(Task, task_id)

#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     if task.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not allowed")

#     update_data = task_update.model_dump(exclude_unset=True)

#     for key, value in update_data.items():
#         setattr(task, key, value)

#     session.add(task)
#     session.commit()
#     session.refresh(task)

#     return task


# # ✅ DELETE TASK
# @router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_task(
#     *,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
#     task_id: int
# ) -> None:
#     task = session.get(Task, task_id)
#     if not task:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
#     if task.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this task")
    
#     session.delete(task)
#     session.commit()
#     return {"message": "Task deleted"}



