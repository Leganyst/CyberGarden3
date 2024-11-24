import pytest_asyncio
import pytest

@pytest.mark.asyncio
async def test_register(async_client, setup_database):
    # Данные для регистрации
    user_data = {
        "email": "testuser@example.com",
        "name": "testuser",
        "password": "testpassword"
    }
    # Отправка POST-запроса на регистрацию
    response = await async_client.post("/auth/register", json=user_data)
    assert response.status_code == 200  # Проверяем статус ответа
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["name"]
    assert "access_token" in data  # Проверяем наличие токена
    # Извлечение access токена
    access_token = data["access_token"]

    # Отправка токена в authorization хедере на ручку логина
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = await async_client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    
    
@pytest.mark.asyncio
async def test_login(async_client, setup_database):
    # Сначала регистрируем пользователя
    user_data = {
        "email": "testlogin@example.com",
        "name": "testlogin",
        "password": "testpassword"
    }
    await async_client.post("/auth/register", json=user_data)

    # Отправляем запрос на вход
    login_data = {
        "email": "testlogin@example.com",
        "password": "testpassword"
    }
    response = await async_client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data  # Проверяем токен
    assert data["token_type"] == "bearer"
