from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.project_user import ProjectUser
from app.models.project import Project
from typing import List
from fastapi import HTTPException

async def send_invite_to_project(
    db: AsyncSession, project_id: int, user_id: int, invited_by: User
) -> bool:
    """
    Отправляет инвайт пользователю на проект.
    """
    # Проверяем, что пользователь не в проекте
    result = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id, ProjectUser.user_id == user_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже добавлен или приглашен в проект.")

    # Создаем инвайт
    invite = ProjectUser(
        project_id=project_id,
        user_id=user_id,
        access_level="invited",
    )
    db.add(invite)
    await db.commit()
    return True


async def accept_project_invite(
    db: AsyncSession, project_id: int, user_id: int
) -> bool:
    """
    Принимает инвайт на проект.
    """
    result = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id,
            ProjectUser.access_level == "invited",
        )
    )
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=404, detail="Инвайт не найден.")

    # Обновляем статус
    invite.access_level = "member"
    await db.commit()
    return True


async def decline_project_invite(
    db: AsyncSession, project_id: int, user_id: int
) -> bool:
    """
    Отклоняет инвайт на проект.
    """
    result = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id,
            ProjectUser.access_level == "invited",
        )
    )
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=404, detail="Инвайт не найден.")

    # Удаляем запись
    await db.delete(invite)
    await db.commit()
    return True

async def get_user_invites(
    db: AsyncSession, user_id: int
) -> List[dict]:
    """
    Возвращает список инвайтов пользователя на проекты.

    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :return: Список словарей с минимальной информацией об инвайтах.
    """
    result = await db.execute(
        select(ProjectUser, Project.name)
        .join(Project, ProjectUser.project_id == Project.id)
        .where(ProjectUser.user_id == user_id, ProjectUser.access_level == "invited")
    )
    invites = result.all()

    return [ 
        {"project_id": invite.ProjectUser.project_id, "project_name": invite.name}
        for invite in invites
    ]