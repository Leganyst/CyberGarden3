from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Создает нового пользователя в базе данных.
    
    :param db: Сессия базы данных.
    :param user_data: Данные для создания пользователя.
    :return: Объект пользователя (ORM).
    """
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password=hashed_password
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise
    return new_user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Возвращает пользователя по его ID.
    
    :param db: Сессия базы данных.
    :param user_id: Уникальный идентификатор пользователя.
    :return: Объект пользователя (ORM) или None.
    """
    return await db.get(User, user_id)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Возвращает пользователя по его email.
    
    :param db: Сессия базы данных.
    :param email: Электронная почта пользователя.
    :return: Объект пользователя (ORM) или None.
    """
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User | None:
    """
    Обновляет данные пользователя в базе данных.
    
    :param db: Сессия базы данных.
    :param user_id: Уникальный идентификатор пользователя.
    :param user_data: Данные для обновления пользователя.
    :return: Обновленный объект пользователя (ORM) или None.
    """
    user = await db.get(User, user_id)
    if not user:
        return None

    # Обновляем только переданные данные
    for field, value in user_data.dict(exclude_unset=True).items():
        if field == "password":
            value = hash_password(value)  # Хэшируем новый пароль
        setattr(user, field, value)
    
    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        await db.rollback()
        raise
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    Удаляет пользователя из базы данных.
    
    :param db: Сессия базы данных.
    :param user_id: Уникальный идентификатор пользователя.
    :return: True, если пользователь удален, иначе False.
    """
    user = await db.get(User, user_id)
    if not user:
        return False
    
    await db.delete(user)
    await db.commit()
    return True
