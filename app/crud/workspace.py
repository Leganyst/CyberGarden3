from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse


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
    return WorkspaceResponse.model_validate(new_workspace)


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


async def get_workspace_by_id(db: AsyncSession, workspace_id: int) -> Optional[WorkspaceResponse]:
    """
    Извлекает рабочее пространство по ID.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :return: Рабочее пространство в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id))
    workspace = result.scalar_one_or_none()
    if workspace:
        return WorkspaceResponse.model_validate(workspace)
    return None
