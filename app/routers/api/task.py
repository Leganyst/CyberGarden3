from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithReminders
from app.schemas.comments import CommentsListResponse
from app.crud.task import (
    create_task,
    update_task,
    delete_task,
    get_task_by_id,
    get_tasks_for_project,
    get_user_tasks_by_date,
    get_task_with_reminders,
)
from app.routers.dependencies.jwt_functions import get_current_user
from app.models.user import User
from app.models.comments import Comment
from app.routers.dependencies.permissions import (
    check_project_access,
    check_project_editor_or_owner,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создание новой задачи. Доступно для создателей и редакторов проекта.
    """
    # Проверка прав доступа
    await check_project_editor_or_owner(task_data.project_id, current_user, db)

    # Создание задачи
    task = await create_task(db, task_data, current_user.id)

    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение информации о задаче. Доступно для всех участников проекта.
    """
    # Извлечение задачи
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    # Проверка прав доступа к проекту
    await check_project_access(task.project_id, current_user, db)

    return task

# Остальные эндпоинты остаются без изменений, так как они не обрабатывают подзадачи напрямую
