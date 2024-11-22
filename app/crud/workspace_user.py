from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.workspace_user import WorkspaceUser
from app.schemas.workspace_user import WorkspaceUserCreate, WorkspaceUserUpdate, WorkspaceUserResponse


async def create_workspace_user(db: AsyncSession, workspace_user_data: WorkspaceUserCreate) -> WorkspaceUserResponse:
    """
    Создает запись связи пользователя и рабочего пространства.
    :param db: Сессия базы данных.
    :param workspace_user_data: Данные для создания связи.
    :return: Созданная запись в формате Pydantic модели.
    """
    new_workspace_user = WorkspaceUser(
        workspace_id=workspace_user_data.workspace_id,
        user_id=workspace_user_data.user_id,
        access_level=workspace_user_data.access_level,
    )
    db.add(new_workspace_user)
    await db.commit()
    await db.refresh(new_workspace_user)
    return WorkspaceUserResponse.model_validate(new_workspace_user)


async def update_workspace_user(
    db: AsyncSession, workspace_user_id: int, workspace_user_data: WorkspaceUserUpdate
) -> Optional[WorkspaceUserResponse]:
    """
    Обновляет данные связи пользователя и рабочего пространства.
    :param db: Сессия базы данных.
    :param workspace_user_id: ID записи связи.
    :param workspace_user_data: Новые данные для обновления.
    :return: Обновленная запись в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(select(WorkspaceUser).where(WorkspaceUser.id == workspace_user_id))
    workspace_user = result.scalar_one_or_none()
    if not workspace_user:
        return None

    if workspace_user_data.access_level is not None:
        workspace_user.access_level = workspace_user_data.access_level

    await db.commit()
    await db.refresh(workspace_user)
    return WorkspaceUserResponse.model_validate(workspace_user)


async def delete_workspace_user(db: AsyncSession, workspace_user_id: int) -> bool:
    """
    Удаляет запись связи пользователя и рабочего пространства.
    :param db: Сессия базы данных.
    :param workspace_user_id: ID записи связи.
    :return: True, если удаление успешно, иначе False.
    """
    result = await db.execute(select(WorkspaceUser).where(WorkspaceUser.id == workspace_user_id))
    workspace_user = result.scalar_one_or_none()
    if not workspace_user:
        return False

    await db.delete(workspace_user)
    await db.commit()
    return True


async def get_users_in_workspace(
    db: AsyncSession, workspace_id: int
) -> List[WorkspaceUserResponse]:
    """
    Извлекает всех пользователей для рабочего пространства с уровнями доступа.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :return: Список пользователей и их уровней доступа в формате Pydantic моделей.
    """
    result = await db.execute(select(WorkspaceUser).where(WorkspaceUser.workspace_id == workspace_id))
    workspace_users = result.scalars().all()
    return [WorkspaceUserResponse.model_validate(wu) for wu in workspace_users]


async def get_users_in_workspace(db: AsyncSession, workspace_id: int) -> List[WorkspaceUserResponse]:
    """
    Извлекает всех пользователей для указанного рабочего пространства с их уровнями доступа.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :return: Список пользователей с уровнями доступа в формате Pydantic моделей.
    """
    result = await db.execute(select(WorkspaceUser).where(WorkspaceUser.workspace_id == workspace_id))
    workspace_users = result.scalars().all()

    # Преобразуем записи ORM в Pydantic-модели
    return [WorkspaceUserResponse.model_validate(user) for user in workspace_users]