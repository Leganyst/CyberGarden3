from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Optional
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from app.models.workspace_user import WorkspaceUser


async def create_workspace(db: AsyncSession, workspace_data: WorkspaceCreate) -> WorkspaceResponse:
    """
    Создает новое рабочее пространство.
    :param db: Сессия базы данных.
    :param workspace_data: Данные для создания рабочего пространства.
    :return: Созданное рабочее пространство в формате Pydantic модели.
    """
    new_workspace = Workspace(
        name=workspace_data.name,
        created_by=workspace_data.created_by,
    )
    db.add(new_workspace)
    await db.commit()
    await db.refresh(new_workspace)
    
    owner_workspace = WorkspaceUser(
        user_id=workspace_data.created_by,
        workspace_id=new_workspace.id,
        access_level="admin"
    )
    db.add(owner_workspace)
    await db.commit()
    
    result_data = {
        "workspace_name": workspace_data.name,
        "owner_id": workspace_data.created_by
    }
    
    return result_data


async def update_workspace(
    db: AsyncSession, workspace_id: int, workspace_data: WorkspaceUpdate
) -> Optional[WorkspaceResponse]:
    """
    Обновляет данные рабочего пространства.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :param workspace_data: Новые данные для обновления рабочего пространства.
    :return: Обновленное рабочее пространство в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id))
    workspace = result.scalar_one_or_none()
    if not workspace:
        return None

    if workspace_data.name is not None:
        workspace.name = workspace_data.name

    await db.commit()
    await db.refresh(workspace)
    return WorkspaceResponse.model_validate(workspace)


async def delete_workspace(db: AsyncSession, workspace_id: int) -> bool:
    """
    Удаляет рабочее пространство.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :return: True, если удаление успешно, иначе False.
    """
    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id))
    workspace = result.scalar_one_or_none()
    if not workspace:
        return False

    await db.delete(workspace)
    await db.commit()
    return True


async def get_workspace_by_id(db: AsyncSession, workspace_id: int, user: User) -> Optional[WorkspaceResponse]:
    """
    Извлекает рабочее пространство по ID.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :return: Рабочее пространство в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id).where(Workspace.created_by == User.id))
    workspace = result.scalar_one_or_none()  
    if workspace:
        return WorkspaceResponse.model_validate(workspace)
    return None


async def get_workspaces_user(db: AsyncSession, user: User):
    """
    Получаем все воркспейсы юзера
    :param db: Сессия базы данных
    :param user: Объект пользователя из БД 
    """
    result = await db.execute(select(Workspace).where(Workspace.created_by == user.id))
    workspaces = result.scalars().all()
    return [WorkspaceResponse.model_validate(w) for w in workspaces]


async def get_user_workspaces(db: AsyncSession, user: User):
    """
    Получаем все воркспейсы юзера
    :param db: Сессия базы данных
    :param user: Объект пользователя из БД 
    """
    result = await db.execute(select(WorkspaceUser).where(WorkspaceUser.user_id == user.id))
    workspaces = result.scalars().all()
    return [WorkspaceUser.model_validate(w) for w in workspaces]