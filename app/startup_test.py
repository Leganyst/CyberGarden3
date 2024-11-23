import requests

# URL API
BASE_URL = "https://cybergarden.leganyst.ru"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
WORKSPACE_URL = f"{BASE_URL}/workspaces/"
PROJECT_URL = f"{BASE_URL}/projects/"
TASK_URL = f"{BASE_URL}/tasks/"

# Регистрация пользователя
def register_user():
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword"
    }
    response = requests.post(REGISTER_URL, json=user_data)
    print("Register User Response:", response.json())
    return response.json()

# Авторизация пользователя
def login_user():
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }
    response = requests.post(LOGIN_URL, json=user_data)
    print("Login User Response:", response.json())
    return response.json()["access_token"]

# Получение всех рабочих пространств
def get_workspaces(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(WORKSPACE_URL, headers=headers)
    print("Get Workspaces Response:", response.json())
    workspaces = response.json()
    if not workspaces:
        print("No workspaces available!")
        return None
    return workspaces[0]["id"]  # Берём первый рабочий пространство

# Создание рабочего пространства
def create_workspace(token):
    workspace_data = {
        "name": "Test Workspace"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(WORKSPACE_URL, json=workspace_data, headers=headers)
    print("Create Workspace Response:", response.json())
    return response.json()["id"]

# Создание проекта
def create_project(token, workspace_id):
    project_data = {
        "name": "Test Project",
        "workspace_id": workspace_id
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(PROJECT_URL, json=project_data, headers=headers)
    print("Create Project Response:", response.json())
    return response.json()["id"]

# Создание задачи
def create_task(token, project_id):
    task_data = {
        "name": "Test Task",
        "due_date": "2024-11-23",
        "description": "This is a test task",
        "status": "In Progress",
        "priority": "High",
        "project_id": project_id,
        "reminder_time": "2024-11-23T18:30:00.000Z"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(TASK_URL, json=task_data, headers=headers)
    print("Create Task Response:", response.json())
    return response.json()

# Последовательность выполнения запросов
def main():
    # Регистрация пользователя
    register_user()
    
    # Авторизация пользователя
    token = login_user()
    
    # Получение всех доступных рабочих пространств
    workspace_id = get_workspaces(token)
    
    # Если нет рабочего пространства, создаём новое
    if not workspace_id:
        workspace_id = create_workspace(token)
    
    # Создание проекта
    project_id = create_project(token, workspace_id)
    
    # Создание задачи
    create_task(token, project_id)

