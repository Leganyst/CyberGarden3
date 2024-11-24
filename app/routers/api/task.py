from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import (
    create_task,
    get_project_tasks,
    get_user_assigned_tasks,
    get_task_by_id,
)
from app.routers.dependencies.jwt_functions import get_current_user
from app.models.user import User
from app.routers.dependencies.permissions import (
    check_project_access,
    check_project_editor_or_owner,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать задачу",
    description="Создаёт новую задачу в указанном проекте. Доступно для редакторов и администраторов проекта.",
    responses={
        201: {
            "description": "Задача успешно создана.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Complete project setup",
                        "description": "Setup initial structure",
                        "status": "OPEN",
                        "priority": "NORMAL",
                        "due_date": "2024-12-01",
                        "is_completed": False,
                        "created_by": 3,
                        "assigned_to": None,
                        "project_id": 1,
                        "created_at": "2024-11-24T06:00:00Z",
                        "updated_at": "2024-11-24T06:00:00Z",
                    }
                }
            },
        },
        403: {"description": "У пользователя нет прав для создания задачи в проекте."},
    },
)
async def create_task_endpoint(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создаёт новую задачу в проекте.

    Доступно только для редакторов и администраторов проекта. Перед созданием задачи
    проверяются права текущего пользователя на редактирование проекта.
    """
    await check_project_editor_or_owner(task_data.project_id, current_user, db)
    task = await create_task(db, task_data, current_user.id)
    return task


@router.get(
    "/assigned",
    response_model=List[TaskResponse],
    summary="Получить задачи пользователя",
    description="Возвращает список задач, которые назначены текущему пользователю.",
    responses={
        200: {
            "description": "Список задач успешно получен.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Write tests",
                            "description": "Cover all CRUD operations",
                            "status": "IN_PROGRESS",
                            "priority": "HIGH",
                            "due_date": "2024-11-30",
                            "is_completed": False,
                            "created_by": 3,
                            "assigned_to": 2,
                            "project_id": 1,
                            "created_at": "2024-11-23T12:00:00Z",
                            "updated_at": "2024-11-24T06:00:00Z",
                        }
                    ]
                }
            },
        },
        401: {"description": "Неавторизованный пользователь."},
    },
)
async def get_assigned_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Возвращает список задач, которые назначены текущему пользователю.

    Пользователь должен быть авторизован для выполнения данного запроса. Возвращается
    список задач, где поле `assigned_to` совпадает с ID текущего пользователя.
    """
    tasks = await get_user_assigned_tasks(db, current_user.id)
    return tasks


@router.get(
    "/project/{project_id}",
    response_model=List[TaskResponse],
    summary="Получить задачи проекта",
    description="Возвращает список всех задач для указанного проекта. Доступен для участников проекта.",
    responses={
        200: {
            "description": "Список задач успешно получен.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Setup CI/CD pipeline",
                            "description": "Implement Jenkins pipeline",
                            "status": "IN_PROGRESS",
                            "priority": "HIGH",
                            "due_date": "2024-11-30",
                            "is_completed": False,
                            "created_by": 3,
                            "assigned_to": 2,
                            "project_id": 1,
                            "created_at": "2024-11-23T12:00:00Z",
                            "updated_at": "2024-11-24T06:00:00Z",
                        }
                    ]
                }
            },
        },
        403: {"description": "У пользователя нет доступа к проекту."},
        404: {"description": "Проект не найден."},
    },
)
async def get_project_tasks_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Возвращает список всех задач для указанного проекта.

    Доступно для участников проекта. Перед возвратом списка задач проверяются права
    текущего пользователя на доступ к проекту.
    """
    await check_project_access(project_id, current_user, db)
    tasks = await get_project_tasks(db, project_id)
    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получить информацию о задаче",
    description="Возвращает данные задачи по её идентификатору. Доступно для всех участников проекта.",
    responses={
        200: {
            "description": "Данные задачи успешно получены.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Fix bugs",
                        "description": "Resolve issues from bug tracker",
                        "status": "OPEN",
                        "priority": "NORMAL",
                        "due_date": "2024-11-30",
                        "is_completed": False,
                        "created_by": 3,
                        "assigned_to": None,
                        "project_id": 1,
                        "created_at": "2024-11-23T12:00:00Z",
                        "updated_at": "2024-11-24T06:00:00Z",
                    }
                }
            },
        },
        403: {"description": "У пользователя нет доступа к задаче."},
        404: {"description": "Задача не найдена."},
    },
)
async def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получает данные задачи по её ID.

    Доступно для всех участников проекта, к которому относится задача. Перед возвратом данных
    проверяются права текущего пользователя на доступ к проекту задачи.
    """
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    await check_project_access(task.project_id, current_user, db)
    return task
