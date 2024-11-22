from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.user import User
from app.schemas.user import UserResponse, UserWithWorkspaces, UserCreate
from app.core.security import hash_password, verify_password
from sqlalchemy.exc import IntegrityError


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[UserResponse]:
    """
    Извлекает пользователя по ID.
    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :return: Данные пользователя в формате Pydantic модели или None.
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user:
        return UserResponse.model_validate(user)
    return None


async def get_user_with_workspaces(db: AsyncSession, user_id: int) -> Optional[UserWithWorkspaces]:
    """
    Извлекает пользователя с его рабочими пространствами.
    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :return: Данные пользователя с рабочими пространствами в формате Pydantic модели или None.
    """
    result = await db.execute(
        select(User)
        .options(selectinload(User.workspaces))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user:
        # Преобразуем `workspaces` в список словарей
        workspaces = [
            {"workspace_id": workspace.workspace_id, "access_level": workspace.access_level}
            for workspace in user.workspaces
        ]
        user_data = UserWithWorkspaces.model_validate(user)
        user_data.workspaces = workspaces
        return user_data
    return None


async def create_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    """
    Создает нового пользователя.
    :param db: Сессия базы данных.
    :param user_data: Данные для создания пользователя.
    :return: Созданный пользователь в формате Pydantic модели.
    """
    hashed_password = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return UserResponse.model_validate(new_user)
    except IntegrityError:
        await db.rollback()
        raise IntegrityError("User with this email already exists.", params=None)


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    """
    Извлекает пользователя по email.
    :param db: Сессия базы данных.
    :param email: Email пользователя.
    :return: Пользователь или None, если не найден.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()