import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_create_workspace(async_client, setup_database, auth_headers):
    """Тест создания нового рабочего пространства."""
    workspace_data = {
        "name": "Test Workspace",
        "created_by": 4
    }

    # Отправляем POST-запрос с токеном
    response = await async_client.post("/workspaces/", json=workspace_data, headers=auth_headers)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == workspace_data["name"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_list_user_workspaces(async_client, setup_database, auth_headers):
    """Тест получения списка рабочих пространств."""
    # Создаём несколько пространств
    workspace_data_1 = {"name": "Workspace 1", "created_by": 1}
    workspace_data_2 = {"name": "Workspace 2", "created_by": 1}

    await async_client.post("/workspaces/", json=workspace_data_1, headers=auth_headers)
    await async_client.post("/workspaces/", json=workspace_data_2, headers=auth_headers)

    # Запрос списка всех пространств
    response = await async_client.get("/workspaces/", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    # Проверяем структуру одного из элементов
    assert "id" in data[0]
    assert "name" in data[0]
    assert "created_by" in data[0]
    assert "created_at" in data[0]
    assert "updated_at" in data[0]


@pytest.mark.asyncio
async def test_get_workspace_details(async_client, setup_database, auth_headers):
    """Тест получения деталей рабочего пространства."""
    # Создаём новое пространство
    workspace_data = {
        "name": "Detail Workspace",
        "created_by": 1
    }
    response = await async_client.post("/workspaces/", json=workspace_data, headers=auth_headers)
    workspace = response.json()

    # Запрос деталей пространства по ID
    response = await async_client.get(f"/workspaces/{workspace['id']}", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == workspace["id"]
    assert data["name"] == workspace["name"]


@pytest.mark.asyncio
async def test_update_workspace(async_client, setup_database, auth_headers):
    """Тест обновления рабочего пространства."""
    # Создаём новое пространство
    workspace_data = {
        "name": "Old Workspace",
        "created_by": 1
    }
    response = await async_client.post("/workspaces/", json=workspace_data, headers=auth_headers)
    workspace = response.json()

    # Обновляем имя рабочего пространства
    updated_data = {"name": "Updated Workspace"}
    response = await async_client.patch(f"/workspaces/{workspace['id']}", json=updated_data, headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["workspace_id"] == workspace["id"]
    assert data["name"] == updated_data["name"]
