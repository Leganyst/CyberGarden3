from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    """
    Базовая схема для пользователя.
    """
    name: str = Field(..., max_length=100, description="Имя пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.
    """
    password: str = Field(..., min_length=6, description="Пароль пользователя")


class UserUpdate(BaseModel):
    """
    Схема для обновления данных пользователя.
    """
    name: Optional[str] = Field(
        None, max_length=100, description="Новое имя пользователя"
    )
    email: Optional[EmailStr] = Field(
        None, description="Новая электронная почта пользователя"
    )
    password: Optional[str] = Field(
        None, min_length=6, description="Новый пароль пользователя"
    )


class UserResponse(UserBase):
    """
    Схема для ответа с данными пользователя.
    """
    id: int = Field(..., description="Уникальный идентификатор пользователя")
    created_at: datetime = Field(..., description="Дата создания пользователя")
    updated_at: datetime = Field(..., description="Дата последнего обновления пользователя")

    class Config:
        from_attributes = True
        exclude = {"password", "created_projects", "created_workspaces", "created_tasks"}


class UserWithWorkspaces(UserResponse):
    """
    Схема для ответа с данными пользователя и рабочими пространствами.
    """
    workspaces: List[dict] = Field(
        ..., description="Список рабочих пространств, связанных с пользователем"
    )


class UserLogin(BaseModel):
    """
    Схема для авторизации пользователя.
    """
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    password: str = Field(..., description="Пароль пользователя")
