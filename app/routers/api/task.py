from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
from app.models.project import Project
from app.models.workspace import Workspace
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
    # Проверка прав доступа (создатель или редактор проекта)
    await check_project_editor_or_owner(task_data.project_id, current_user, db)

    # Устанавливаем текущего пользователя как создателя задачи
    task_data.created_by = current_user.id

    # Создание задачи (и напоминания, если указано reminder_time)
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


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Редактирование задачи. Доступно для создателей и редакторов проекта.
    """
    # Извлечение задачи
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    # Проверяем права на редактирование
    await check_project_editor_or_owner(task.project_id, current_user, db)

    # Обновление задачи
    updated_task = await update_task(db, task_id, task_data)

    return updated_task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_as_completed(
    task_id: int,
    is_completed: bool = Query(True, description="Отметить задачу как выполненную или невыполненную"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Отметить задачу выполненной или невыполненной.
    Читатель может изменить только свои задачи.
    """
    # Извлечение задачи
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    # Проверка прав доступа к проекту
    has_access = await check_project_access(task.project_id, current_user, db)
    if not has_access:
        raise HTTPException(status_code=403, detail="Доступ запрещен.")

    # Читатель может изменить только свои задачи
    if task.assigned_to != current_user.id:
        await check_project_editor_or_owner(task.project_id, current_user, db)

    # Обновление статуса выполнения задачи
    task_update_data = TaskUpdate(is_completed=is_completed)
    updated_task = await update_task(db, task_id, task_update_data)

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаление задачи. Доступно для создателей и редакторов проекта.
    """
    # Извлечение задачи
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    # Проверяем права на удаление
    await check_project_editor_or_owner(task.project_id, current_user, db)

    # Удаление задачи
    await delete_task(db, task_id)
    return {"detail": "Задача успешно удалена."}


@router.get("/project/{project_id}", response_model=List[TaskResponse])
async def get_tasks_for_project_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение всех задач для проекта. Доступно для всех участников проекта.
    """
    # Проверка прав доступа к проекту
    await check_project_access(project_id, current_user, db)

    # Получение задач
    tasks = await get_tasks_for_project(db, project_id)

    return tasks


@router.get("/user/tasks", response_model=List[TaskResponse])
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


@router.get("/{task_id}/comments", response_model=CommentsListResponse)
async def get_task_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение всех комментариев к задаче.
    """
    # Извлечение задачи
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    # Проверка прав доступа к проекту
    await check_project_access(task.project_id, current_user, db)

    # Извлечение комментариев
    result = await db.execute(
        select(Comment).where(Comment.task_id == task_id).order_by(Comment.created_at)
    )
    comments = result.scalars().all()

    return CommentsListResponse(comments=comments)


@router.get("/{task_id}/with_reminders", response_model=TaskWithReminders)
async def get_task_with_reminders_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение задачи вместе с ее напоминаниями.
    """
    # Извлечение задачи с напоминаниями
    task = await get_task_with_reminders(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    # Проверка прав доступа к проекту
    await check_project_access(task.project_id, current_user, db)

    return task
