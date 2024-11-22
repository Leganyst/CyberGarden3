from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.crud.workspace import get_workspace_by_id
from app.core.database import get_db
from app.routers.dependencies.jwt_functions import get_current_user
from app.crud.project import get_workspace_id_by_project_id
from app.crud.workspace_user import get_users_in_workspace


async def check_workspace_owner(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Проверяет, является ли текущий пользователь владельцем рабочего пространства.
    Если проверка успешна, возвращает объект рабочего пространства.
    Иначе вызывает исключение HTTP 403 (доступ запрещен).
    
    :param workspace_id: ID рабочего пространства.
    :param current_user: Объект текущего авторизованного пользователя.
    :param db: Сессия базы данных.
    :return: Объект рабочего пространства.
    """
    workspace = await get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if workspace.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return workspace

async def check_workspace_access(
    workspace_id: int,
    current_user: User,
    db: AsyncSession,
) -> bool:
    """
    Проверяет, имеет ли пользователь доступ к рабочему пространству как создатель, редактор или читатель.
    """
    workspace_users = await get_users_in_workspace(db, workspace_id)
    for workspace_user in workspace_users:
        if workspace_user.user_id == current_user.id:
            return True  # Доступ разрешен
    return False  # Доступ запрещен


async def check_workspace_editor_or_owner(
    project_id: int, current_user: User, db: AsyncSession
):
    """
    Проверяет, является ли пользователь редактором или создателем рабочего пространства.
    """
    workspace_id = await get_workspace_id_by_project_id(db, project_id)
    if not await check_workspace_access(workspace_id, current_user, db, roles=["editor", "owner"]):
        raise HTTPException(status_code=403, detail="Access denied")
