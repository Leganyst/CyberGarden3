from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.project import Project
from app.core.database import get_db
from app.models.workspace import Workspace
from app.routers.dependencies.jwt_functions import get_current_user


async def check_project_owner(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Проверяет, является ли текущий пользователь владельцем проекта.
    """
    # Проверяем, что текущий пользователь создал проект
    result = await db.execute(
        select(Project)
        .where(
            Project.id == project_id,
            Project.created_by == current_user.id
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=403, detail="Access denied")

    return project


async def check_workspace_owner(workspace_id: int,
                                current_user: User = Depends(get_current_user),
                                db: AsyncSession = Depends(get_db)):
    """
    Проверяет, является ли текущий пользователь владельцем рабочего пространства.

    :param workspace_id: ID рабочего пространства
    :param current_user: Объект текущего пользователя (модель User)
    :param db: Сессия базы данных (AsyncSession)
    :raises HTTPException: 404, если рабочее пространство не найдено
    :raises HTTPException: 403, если пользователь не является владельцем
    """
    # Получаем рабочее пространство из базы данных
    result = await db.execute(
        select(Workspace).where(Workspace.id == workspace_id)
    )
    workspace = result.scalar_one_or_none()

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рабочее пространство не найдено."
        )

    if workspace.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для выполнения этого действия."
        )


async def check_project_access(
    project_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, имеет ли пользователь доступ к проекту (как создатель или участник через воркспейс).
    """
    # Проверяем, что пользователь создал проект
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.created_by == current_user.id:
        return True  # Пользователь — создатель проекта

    # Проверяем, что пользователь имеет доступ через воркспейс
    result = await db.execute(
        select(Project)
        .where(
            Project.workspace_id == project.workspace_id,
            Project.created_by == current_user.id
        )
    )
    if result.scalar_one_or_none():
        return True  # Пользователь имеет доступ через воркспейс

    raise HTTPException(status_code=403, detail="Access denied")

async def check_project_editor_or_owner(
    project_id: int,
    current_user: User,
    db: AsyncSession,
):
    """
    Проверяет, является ли пользователь владельцем или редактором проекта.
    :param project_id: ID проекта.
    :param current_user: Объект текущего авторизованного пользователя.
    :param db: Сессия базы данных.
    :raises HTTPException: Если пользователь не имеет доступа.
    :return: True, если пользователь имеет доступ.
    """
    # Проверяем, что пользователь является создателем проекта
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.created_by == current_user.id:
        return True  # Пользователь — создатель проекта

    # Проверяем, что пользователь имеет доступ через воркспейс (как редактор)
    result = await db.execute(
        select(Project)
        .where(
            Project.workspace_id == project.workspace_id,
            Project.created_by == current_user.id
        )
    )
    if result.scalar_one_or_none():
        return True  # Пользователь имеет доступ через воркспейс

    # Если доступ не подтверждён, возвращаем ошибку
    raise HTTPException(status_code=403, detail="Access denied")
