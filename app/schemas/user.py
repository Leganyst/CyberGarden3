from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя. Должна быть уникальной.")
    username: str | None = Field(None, description="Необязательное имя пользователя. Уникальное.")


class UserCreate(UserBase):
    password: str = Field(..., description="Пароль пользователя.")


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(None, description="Новый email пользователя.")
    username: str | None = Field(None, description="Новое имя пользователя.")
    password: str | None = Field(None, description="Новый пароль пользователя.")


class UserResponse(UserBase):
    id: int = Field(..., description="Уникальный идентификатор пользователя.")

    class Config:
        orm_mode = True  # Включает поддержку ORM-объектов
