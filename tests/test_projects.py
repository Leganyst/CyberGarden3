import pytest
import logging
from httpx import Response

# Настройка логгирования
logger = logging.getLogger("test_logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_request_response(response: Response, description: str):
    """Логирует запрос, ответ и описание теста."""
    logger.info(f"{description}")
    logger.debug(f"Request URL: {response.request.url}")
    logger.debug(f"Request Method: {response.request.method}")
    logger.debug(f"Request Headers: {response.request.headers}")
    logger.debug(f"Request Body: {response.request.content}")
    logger.debug(f"Response Status Code: {response.status_code}")
    logger.debug(f"Response Body: {response.text}")

@pytest.mark.asyncio
async def test_create_project(async_client, setup_database, auth_headers):
    """Тест создания проекта в рабочем пространстве."""
    # Создаём рабочее пространство
    workspace_data = {"name": "Workspace for Project"}
    response = await async_client.post("/workspaces/", json=workspace_data, headers=auth_headers)
    log_request_response(response, "Создание рабочего пространства")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"
    workspace = response.json()
    workspace_id = workspace.get("id")
    assert workspace_id, f"Response missing 'id': {workspace}"

    # Создаём проект в этом рабочем пространстве
    project_data = {"name": "Test Project", "workspace_id": workspace_id}
    response = await async_client.post("/projects/", json=project_data, headers=auth_headers)
    log_request_response(response, "Создание проекта в рабочем пространстве")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"

    project = response.json()
    assert project.get("name") == project_data["name"], f"Unexpected project data: {project}"
    assert project.get("workspace_id") == workspace_id, f"Unexpected workspace_id: {project}"


@pytest.mark.asyncio
async def test_get_all_projects_for_user(async_client, setup_database, auth_headers):
    """Тест получения всех проектов для пользователя."""
    # Создаём рабочее пространство
    workspace_data = {"name": "Workspace for Multiple Projects"}
    response = await async_client.post("/workspaces/", json=workspace_data, headers=auth_headers)
    log_request_response(response, "Создание рабочего пространства для нескольких проектов")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"
    workspace = response.json()
    workspace_id = workspace.get("id")
    assert workspace_id, f"Response missing 'id': {workspace}"

    # Создаём несколько проектов
    project_names = ["Project 1", "Project 2", "Project 3"]
    for name in project_names:
        project_data = {"name": name, "workspace_id": workspace_id}
        response = await async_client.post("/projects/", json=project_data, headers=auth_headers)
        log_request_response(response, f"Создание проекта {name}")
        assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"

    # Запрашиваем список всех проектов
    response = await async_client.get(f"/projects/{workspace_id}/projects/all", headers=auth_headers)
    log_request_response(response, "Получение всех проектов для пользователя")
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, Response: {response.text}"

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(project_names), f"Expected {len(project_names)} projects, got {len(data)}"
    for project in data:
        assert "name" in project
        assert "id" in project


@pytest.mark.asyncio
async def test_get_project_details(async_client, setup_database, auth_headers):
    """Тест получения деталей проекта."""
    # Создаём рабочее пространство
    workspace_data = {"name": "Workspace for Project Details"}
    response = await async_client.post("/workspaces/", json=workspace_data, headers=auth_headers)
    log_request_response(response, "Создание рабочего пространства для деталей проекта")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"
    workspace = response.json()
    workspace_id = workspace.get("id")
    assert workspace_id, f"Response missing 'id': {workspace}"

    # Создаём проект
    project_data = {"name": "Detail Project", "workspace_id": workspace_id}
    response = await async_client.post("/projects/", json=project_data, headers=auth_headers)
    log_request_response(response, "Создание проекта для проверки деталей")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"
    project = response.json()
    project_id = project.get("id")
    assert project_id, f"Response missing 'id': {project}"

    # Получаем детали проекта
    response = await async_client.get(f"/projects/{project_id}", headers=auth_headers)
    log_request_response(response, "Получение деталей проекта")
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, Response: {response.text}"
    data = response.json()
    assert data.get("id") == project_id, f"Unexpected project details: {data}"


@pytest.mark.asyncio
async def test_delete_project(async_client, setup_database, auth_headers):
    """Тест удаления проекта."""
    # Создаём рабочее пространство
    workspace_data = {"name": "Workspace for Deleting Project"}
    response = await async_client.post("/workspaces/", json=workspace_data, headers=auth_headers)
    log_request_response(response, "Создание рабочего пространства для удаления проекта")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"
    workspace = response.json()
    workspace_id = workspace.get("id")
    assert workspace_id, f"Response missing 'id': {workspace}"

    # Создаём проект
    project_data = {"name": "Project to Delete", "workspace_id": workspace_id}
    response = await async_client.post("/projects/", json=project_data, headers=auth_headers)
    log_request_response(response, "Создание проекта для удаления")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, Response: {response.text}"
    project = response.json()
    project_id = project.get("id")
    assert project_id, f"Response missing 'id': {project}"

    # Удаляем проект
    response = await async_client.delete(f"/projects/{project_id}", headers=auth_headers)
    log_request_response(response, "Удаление проекта")
    assert response.status_code == 204, f"Unexpected status: {response.status_code}, Response: {response.text}"
