from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.routers.dependencies.jwt_functions import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    decode_token
)
from app.crud.user import create_user, get_user_by_email, get_user_by_id
from app.core.security import verify_password
from app.core.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    response_description="Информация о зарегистрированном пользователе",
    responses={
        200: {
            "description": "Успешная регистрация",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "user",
                        "access_token": "access_token_example",
                        "refresh_token": "refresh_token_example",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Пользователь с таким email уже существует",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with this email already exists."
                    }
                }
            }
        }
    }
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Регистрация нового пользователя.
    
    Принимает данные для создания нового пользователя, создает запись в базе данных
    и возвращает информацию о зарегистрированном пользователе.

    - **email**: Электронная почта пользователя
    - **username**: Имя пользователя
    - **password**: Пароль пользователя
    """
    try:
        user = await create_user(db, user_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    # Создание токенов
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    
    # Возврат информации о пользователе
    return {
        "id": user.id,
        "email": user.email,
        "username": user.name,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/login", summary="Авторизация пользователя")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    Авторизация пользователя.
    
    Проверяет учетные данные пользователя и выдает JWT-токены.
    """
    user = await get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse, summary="Получить информацию о текущем пользователе")
async def read_current_user(
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Возвращает данные текущего авторизованного пользователя.
    """
    return current_user


@router.post("/refresh", summary="Обновление токена доступа")
async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Обновляет токен доступа (access token) с использованием рефреш-токена.
    """
    payload = decode_token(refresh_token)
    user_id: int = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token({"sub": user.id})
    return {"access_token": new_access_token, "token_type": "bearer"}