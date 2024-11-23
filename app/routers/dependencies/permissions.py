from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.crud.workspace import get_workspace_by_id
from app.core.database import get_db
from app.routers.dependencies.jwt_functions import get_current_user
from app.crud.project import get_workspace_id_by_project_id
from app.crud.workspace_user import get_users_in_workspace
from app.models.workspace_user import WorkspaceUser


async def check_workspace_owner(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Проверяет, является ли текущий пользователь владельцем рабочего пространства (admin).
    """
    # Проверяем, есть ли запись о доступе пользователя к рабочему пространству
    result = await db.execute(
        select(WorkspaceUser)
        .where(
            WorkspaceUser.workspace_id == workspace_id,
            WorkspaceUser.user_id == current_user.id,
            WorkspaceUser.access_level == "admin",  # Проверяем, что пользователь — admin
        )
    )
    workspace_user = result.scalar_one_or_none()

    if not workspace_user:
        raise HTTPException(status_code=403, detail="Access denied")

    return workspace_user.workspace


async def check_workspace_access(
    workspace_id: int,
    current_user: User,
    db: AsyncSession,
    roles: list[str] = None,
) -> bool:
    """
    Проверяет, имеет ли пользователь доступ к рабочему пространству с определенными ролями.
    :param workspace_id: ID рабочего пространства.
    :param current_user: Объект текущего авторизованного пользователя.
    :param db: Сессия базы данных.
    :param roles: Список допустимых ролей (например, ["admin", "member"]).
    :return: True, если доступ есть, иначе False.
    """
    roles = roles or ["admin", "member", "viewer"]  # По умолчанию разрешаем все роли
    result = await db.execute(
        select(WorkspaceUser)
        .where(
            WorkspaceUser.workspace_id == workspace_id,
            WorkspaceUser.user_id == current_user.id,
            WorkspaceUser.access_level.in_(roles),
        )
    )
    workspace_user = result.scalar_one_or_none()
    return workspace_user is not None


async def check_workspace_editor_or_owner(
    project_id: int, current_user: User, db: AsyncSession
):
    """
    Проверяет, является ли пользователь редактором или создателем рабочего пространства.
    """
    workspace_id = await get_workspace_id_by_project_id(db, project_id)

    # Проверяем доступ для ролей "admin" и "member" (можно адаптировать роли при необходимости)
    if not await check_workspace_access(workspace_id, current_user, db, roles=["admin", "member"]):
        raise HTTPException(status_code=403, detail="Access denied")