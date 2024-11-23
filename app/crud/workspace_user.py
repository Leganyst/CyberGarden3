from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.workspace_user import WorkspaceUser
from app.schemas.workspace_user import WorkspaceUserCreate, WorkspaceUserUpdate, WorkspaceUserResponse
from sqlalchemy.exc import IntegrityError

async def create_workspace_user(db: AsyncSession, workspace_id: int, user_id: int, access_level: str) -> WorkspaceUser:
    """
    Создаёт запись в таблице WorkspaceUser.
    """
    new_workspace_user = WorkspaceUser(
        workspace_id=workspace_id,
        user_id=user_id,
        access_level=access_level,
    )
    db.add(new_workspace_user)
    try:
        await db.commit()
        await db.refresh(new_workspace_user)
    except IntegrityError:
        await db.rollback()
        raise ValueError("User is already added to this workspace or invalid data.")
    return new_workspace_user


async def is_workspace_admin(db: AsyncSession, workspace_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором рабочего пространства.
    """
    result = await db.execute(
        select(WorkspaceUser)
        .where(
            WorkspaceUser.workspace_id == workspace_id,
            WorkspaceUser.user_id == user_id,
            WorkspaceUser.access_level == "admin",
        )
    )
    return result.scalar_one_or_none() is not None

async def update_workspace_user_role(
    db: AsyncSession, workspace_id: int, user_id: int, new_role: str
) -> WorkspaceUserResponse:
    """
    Обновляет уровень доступа пользователя в рабочем пространстве.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :param user_id: ID пользователя, чья роль обновляется.
    :param new_role: Новый уровень доступа.
    :return: Обновлённая связь пользователя и рабочего пространства.
    """
    result = await db.execute(
        select(WorkspaceUser).where(
            WorkspaceUser.workspace_id == workspace_id,
            WorkspaceUser.user_id == user_id,
        )
    )
    workspace_user = result.scalar_one_or_none()
    if not workspace_user:
        raise ValueError("User not found in the workspace.")

    # Обновляем роль
    workspace_user.access_level = new_role
    await db.commit()
    await db.refresh(workspace_user)

    return WorkspaceUserResponse.model_validate(workspace_user)

async def remove_user_from_workspace(db: AsyncSession, workspace_id: int, user_id: int) -> bool:
    """
    Удаляет пользователя из рабочего пространства.
    :param db: Сессия базы данных.
    :param workspace_id: ID рабочего пространства.
    :param user_id: ID пользователя.
    :return: True, если удаление успешно, иначе False.
    """
    result = await db.execute(
        select(WorkspaceUser).where(
            WorkspaceUser.workspace_id == workspace_id,
            WorkspaceUser.user_id == user_id,
        )
    )
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