import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import (
    create_task,
    update_task,
    delete_task,
    get_task_by_id,
    get_tasks_for_project,
    get_user_tasks_by_date
)
from app.routers.dependencies.jwt_functions import get_current_user
from app.routers.dependencies.permissions import (
    check_workspace_access,
    check_workspace_editor_or_owner,
)
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создание новой задачи. Доступно для создателя и редактора рабочего пространства.
    """
    # Проверка прав доступа (создатель или редактор рабочего пространства)
    await check_workspace_editor_or_owner(task_data.project_id, current_user, db)

    # Устанавливаем текущего пользователя как создателя задачи
    task_data.created_by = current_user.id

    # Создание задачи (и напоминания, если указано reminder_time)
    task = await create_task(db, task_data)

    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение информации о задаче. Доступно для всех уровней доступа.
    """
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Проверка прав доступа через рабочее пространство
    if not await check_workspace_access(task.project.workspace_id, current_user, db):
        raise HTTPException(status_code=403, detail="Access denied")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Редактирование задачи. Доступно для создателя и редактора рабочего пространства.
    """
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Проверяем права на редактирование
    await check_workspace_editor_or_owner(task.project.workspace_id, current_user, db)

    updated_task = await update_task(db, task_id, task_data)
    return updated_task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_as_completed(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Отметить задачу выполненной. Читатель может только для своих задач.
    """
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Проверяем права на рабочее пространство
    if not await check_workspace_access(task.project.workspace_id, current_user, db):
        raise HTTPException(status_code=403, detail="Access denied")

    # Читатель может отметить только свои задачи
    if task.assigned_to != current_user.id and not await check_workspace_editor_or_owner(
        task.project.workspace_id, current_user, db
    ):
        raise HTTPException(status_code=403, detail="Access denied to complete this task")

    task.is_completed = True
    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаление задачи. Доступно для создателя и редактора рабочего пространства.
    """
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Проверяем права на удаление
    await check_workspace_editor_or_owner(task.project.workspace_id, current_user, db)

    await delete_task(db, task_id)
    return {"message": "Task deleted successfully"}


@router.get("/user/today", status_code=status.HTTP_200_OK)
async def get_user_tasks_today(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение задач пользователя на сегодня.
    """
    tasks = await get_user_tasks_by_date(db, current_user.id, target_date=datetime.date.today())
    return tasks