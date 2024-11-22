from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserResponse
from app.crud.user import get_user_by_id
from app.core.config import settings

# Конфигурация токенов
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = settings.jwt_secret_key


def create_access_token(data: dict) -> str:
    """
    Создает JWT-токен для доступа (access token).
    
    :param data: Данные, которые необходимо включить в токен.
    :return: Сгенерированный JWT-токен.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": str(data.get("sub", ""))})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """
    Создает рефреш-токен (refresh token).
    
    :param data: Данные, которые необходимо включить в токен.
    :return: Сгенерированный JWT-токен.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "sub": str(data.get("sub", ""))})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Декодирует JWT-токен.
    
    :param token: JWT-токен.
    :return: Декодированные данные из токена.
    """
    try:
        # token = token.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())] = None,
) -> UserResponse:
    """
    Зависимость для получения текущего пользователя по токену.

    :param db: Сессия базы данных.
    :param token: JWT-токен из заголовка Authorization.
    :return: Объект пользователя.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    try:
        token = token.credentials
        token = token.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token")

    payload = decode_token(token.credentials)
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = user.__dict__
    user_dict.pop("_sa_instance_state")
    user_dict.pop("password")

    return UserResponse.model_validate(user_dict)
