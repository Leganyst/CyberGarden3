import sys
from pathlib import Path

# Добавляем корень проекта в `sys.path`, чтобы Python мог находить пакеты
sys.path.append(str(Path(__file__).resolve().parent.parent / "app"))


import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.core.database import get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base

# Тестовая база данных SQLite в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Настройка движка и сессии для тестов
engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Переопределяем зависимость get_db
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def async_client():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="function")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def auth_headers(async_client):
    """Фикстура для получения заголовков авторизации."""
    # Регистрируем пользователя
    user_data = {
        "email": "testuser@example.com",
        "name": "testuser",
        "password": "testpassword"
    }
    response = await async_client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()

    # Возвращаем токен в заголовке
    return {"Authorization": f"Bearer {data['access_token']}"}
