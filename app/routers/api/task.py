import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.models.project import Project
from app.models.workspace import Workspace
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
from datetime import date
from fastapi import Query

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
    # Извлечение задачи
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Извлечение проекта, к которому принадлежит задача
    result = await db.execute(
        select(Project).where(Project.id == task.project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Извлечение рабочего пространства, к которому принадлежит проект
    result = await db.execute(
        select(Workspace).where(Workspace.id == project.workspace_id)
    )
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Проверка прав доступа к рабочему пространству
    if not await check_workspace_access(workspace.id, current_user, db):
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


@router.patch("/{task_id}/complete/{mark_as_completed}", response_model=TaskResponse)
async def mark_task_as_completed(
    task_id: int,
    mark_as_completed: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Отметить задачу выполненной. Читатель может только для своих задач.
    """
    # Извлечение задачи
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Извлечение проекта, к которому принадлежит задача
    result = await db.execute(
        select(Project).where(Project.id == task.project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Извлечение рабочего пространства, к которому принадлежит проект
    result = await db.execute(
        select(Workspace).where(Workspace.id == project.workspace_id)
    )
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Проверяем права на рабочее пространство
    if not await check_workspace_access(workspace.id, current_user, db):
        raise HTTPException(status_code=403, detail="Access denied")

    # Читатель может отметить только свои задачи
    if task.assigned_to != current_user.id and not await check_workspace_editor_or_owner(
        workspace.id, current_user, db
    ):
        raise HTTPException(status_code=403, detail="Access denied to complete this task")

    # Отмечаем задачу выполненной
    task.is_completed = mark_as_completed
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


@router.get("/user/tasks", status_code=status.HTTP_200_OK)
async def get_user_tasks_by_date_endpoint(
    target_date: date = Query(..., description="Дата для получения задач (формат: YYYY-MM-DD)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение задач пользователя на указанную дату.
    """
    tasks = await get_user_tasks_by_date(db, current_user.id, target_date)
    return tasks
