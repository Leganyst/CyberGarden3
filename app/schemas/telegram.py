from pydantic import BaseModel, Field

class TelegramAuthRequest(BaseModel):
    """
    Схема запроса для авторизации через Telegram.
    """
    id: int = Field(..., description="Уникальный идентификатор пользователя Telegram")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str | None = Field(None, description="Фамилия пользователя")
    username: str | None = Field(None, description="Никнейм пользователя в Telegram")
    photo_url: str | None = Field(None, description="URL аватара пользователя")
    auth_date: int = Field(..., description="Время авторизации пользователя в формате Unix timestamp")
    hash: str = Field(..., description="Подпись данных, переданных Telegram")

class TelegramAuthResponse(BaseModel):
    """
    Схема ответа для авторизации через Telegram.
    """
    id: int = Field(..., description="Уникальный идентификатор пользователя в системе")
    username: str = Field(..., description="Имя пользователя")
    access_token: str = Field(..., description="JWT токен для доступа к защищённым ресурсам")
    refresh_token: str = Field(..., description="JWT токен для обновления доступа")
    token_type: str = Field("bearer", description="Тип токена")