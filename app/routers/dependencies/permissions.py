from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.project import get_project_by_id
from app.models.user import User
from app.models.project import Project
from app.core.database import get_db
from app.models.workspace import Workspace
from app.routers.dependencies.jwt_functions import get_current_user
from typing import Optional
from app.models.project_user import ProjectUser
from app.models.task import Task


async def get_user_project_access_level(
    db: AsyncSession, project_id: int, user_id: int
) -> Optional[str]:
    """
    Получает уровень доступа пользователя в проекте.
    """
    result = await db.execute(
        select(ProjectUser.access_level)
        .where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        )
    )
    access_level = result.scalar_one_or_none()
    return access_level


async def check_project_owner(
    project_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, является ли текущий пользователь администратором проекта.
    """
    access_level = await get_user_project_access_level(db, project_id, current_user.id)

    if access_level == 'admin':
        return True  # Пользователь является администратором проекта

    raise HTTPException(status_code=403, detail="Доступ запрещён.")


async def check_project_editor_or_owner(
    project_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, является ли пользователь администратором или членом проекта (editor).
    """
    
    access_level = await get_user_project_access_level(db, project_id, current_user.id)

    if access_level in ['admin', 'member']:
        return True  # Пользователь имеет права редактирования

    raise HTTPException(status_code=403, detail="Доступ запрещён.")


async def check_project_access(
    project_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, имеет ли пользователь доступ к проекту (admin, member или viewer).
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден.")
    
    access_level = await get_user_project_access_level(db, project_id, current_user.id)

    if access_level in ['admin', 'member', 'viewer']:
        return True  # Пользователь имеет доступ к проекту

    raise HTTPException(status_code=403, detail="Доступ запрещён.")


async def check_project_viewer_or_higher(
    project_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, имеет ли пользователь уровень доступа как минимум viewer.
    """
    access_level = await get_user_project_access_level(db, project_id, current_user.id)

    if access_level in ['admin', 'member', 'viewer']:
        return True  # Пользователь имеет права просмотра

    raise HTTPException(status_code=403, detail="Доступ запрещён.")


async def check_task_completion_permission(
    task_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, может ли пользователь отметить задачу как выполненную.
    """
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    # Проверяем уровень доступа пользователя к проекту
    access_level = await get_user_project_access_level(db, task.project_id, current_user.id)

    if access_level == 'admin':
        return True  # Администратор может отметить любую задачу

    if access_level == 'member':
        return True  # Член проекта может отметить любую задачу

    if access_level == 'viewer' and task.assigned_to == current_user.id:
        return True  # Читатель может отметить только свои задачи

    raise HTTPException(status_code=403, detail="Доступ запрещён.")


async def check_workspace_owner(
    workspace_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, является ли текущий пользователь владельцем рабочего пространства.
    """
    result = await db.execute(
        select(Workspace).where(Workspace.id == workspace_id)
    )
    workspace = result.scalar_one_or_none()

    if not workspace:
        raise HTTPException(status_code=404, detail="Рабочее пространство не найдено.")

    if workspace.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="У вас нет прав для выполнения этого действия.")

    return True  # Пользователь является владельцем рабочего пространства