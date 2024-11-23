from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    telegram_bot_token: str
    jwt_secret_key: str = secrets.token_urlsafe(32)  # Генерация уникального ключа

    class Config:
        env_file = ".env"

        fields = {
            "postgres_password": {'exclude': True},
            "postgres_user": {'exclude': True},
            "postgres_db": {'exclude': True},
        }

        
settings = Settings()