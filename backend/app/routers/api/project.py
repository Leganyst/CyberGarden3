import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.crud.workspace import get_workspace_by_id
from app.models.workspace import Workspace
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.crud.project import (
    create_project,
    update_project,
    delete_project,
    get_project_by_id,
    get_tasks_for_project,
    get_all_projects
)
from app.routers.dependencies.jwt_functions import get_current_user
from app.routers.dependencies.permissions import check_project_access, check_project_owner
from app.models.user import User
from app.schemas.task import TaskResponse

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать проект",
    description="Создает новый проект в указанном рабочем пространстве. Доступно только владельцу рабочего пространства.",
    responses={
        201: {
            "description": "Проект успешно создан.",
            "content": {
                "application/json": {
                    "example": {"message": "Проект успешно создан."}
                }
            },
        },
        403: {"description": "Пользователь не является владельцем рабочего пространства."},
        404: {"description": "Рабочее пространство не найдено."},
    },
)
async def create_project_endpoint(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создание нового проекта. Только для владельца рабочего пространства.
    """
    logger.info(
        f"Попытка создания проекта. Пользователь: {current_user.id}, Рабочее пространство: {project_data.workspace_id}, Имя проекта: {project_data.name}"
    )

    # Проверяем существование рабочего пространства
    workspace = await get_workspace_by_id(db, project_data.workspace_id, current_user)
    if not workspace:
        logger.warning(
            f"Рабочее пространство не найдено. Пользователь: {current_user.id}, Рабочее пространство: {project_data.workspace_id}"
        )
        raise HTTPException(status_code=404, detail="Рабочее пространство не найдено.")

    # Проверяем, что пользователь является владельцем рабочего пространства
    if workspace.created_by != current_user.id:
        logger.warning(
            f"Доступ запрещен. Пользователь: {current_user.id} не является владельцем рабочего пространства: {project_data.workspace_id}"
        )
        raise HTTPException(status_code=403, detail="Доступ запрещен.")

    # Создание проекта
    await create_project(db, project_data, current_user)
    logger.info(
        f"Проект успешно создан. Пользователь: {current_user.id}, Рабочее пространство: {project_data.workspace_id}, Имя проекта: {project_data.name}"
    )

    return {"message": "Проект успешно создан."}


@router.get(
    "/{workspace_id}/all",
    response_model=List[ProjectResponse],
    summary="Получить проекты в рабочем пространстве",
    description="Возвращает список всех проектов в указанном рабочем пространстве, к которым текущий пользователь имеет доступ.",
    responses={
        200: {"description": "Список проектов успешно возвращен."},
        403: {"description": "Пользователь не имеет доступа к рабочему пространству."},
    },
)
async def get_all_projects_for_user(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение всех проектов, к которым пользователь имеет доступ.
    """
    logger.info("Пользователь ID %d запросил список проектов в рабочем пространстве ID %d",
                current_user.id, workspace_id)

    projects = await get_all_projects(db, current_user, workspace_id)
    logger.info("Найдено %d проектов в рабочем пространстве ID %d для пользователя ID %d",
                len(projects), workspace_id, current_user.id)

    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Получить проект",
    description="Возвращает подробную информацию о проекте. Доступно пользователям с любым уровнем доступа (admin, member, viewer).",
    responses={
        200: {"description": "Проект найден."},
        403: {"description": "Пользователь не имеет доступа к проекту."},
        404: {"description": "Проект не найден."},
    },
)
async def get_project_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение информации о проекте. Доступно для всех пользователей, имеющих доступ к проекту.
    """
    logger.info("Пользователь ID %d запросил данные проекта ID %d", current_user.id, project_id)

    await check_project_access(project_id, current_user, db)

    project = await get_project_by_id(db, project_id)
    if not project:
        logger.warning("Проект ID %d не найден для пользователя ID %d", project_id, current_user.id)
        raise HTTPException(status_code=404, detail="Проект не найден.")

    logger.info("Проект ID %d успешно получен для пользователя ID %d", project_id, current_user.id)
    return project


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Обновить проект",
    description="Обновляет информацию о проекте. Доступно только администраторам проекта (`admin`).",
    responses={
        200: {"description": "Проект успешно обновлен."},
        403: {"description": "Пользователь не является администратором проекта."},
        404: {"description": "Проект не найден."},
    },
)
async def update_project_endpoint(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление проекта. Только для администраторов проекта.
    """
    logger.info("Пользователь ID %d запросил обновление проекта ID %d", current_user.id, project_id)

    await check_project_owner(project_id, current_user, db)

    updated_project = await update_project(db, project_id, project_data)
    logger.info("Проект ID %d успешно обновлен пользователем ID %d", project_id, current_user.id)

    return updated_project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить проект",
    description="Удаляет проект. Доступно только администраторам проекта (`admin`).",
    responses={
        204: {"description": "Проект успешно удален."},
        403: {"description": "Пользователь не является администратором проекта."},
        404: {"description": "Проект не найден."},
    },
)
async def delete_project_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаление проекта. Только для администраторов проекта.
    """
    logger.info("Пользователь ID %d запросил удаление проекта ID %d", current_user.id, project_id)

    await check_project_owner(project_id, current_user, db)
    await delete_project(db, project_id)
    logger.info("Проект ID %d успешно удален пользователем ID %d", project_id, current_user.id)

    return {"message": "Проект успешно удален."}


@router.get(
    "/{project_id}/tasks",
    response_model=List[TaskResponse],
    summary="Получить задачи проекта",
    description="Возвращает список задач проекта. Доступно пользователям с любым уровнем доступа (admin, member, viewer).",
    responses={
        200: {"description": "Список задач успешно возвращен."},
        403: {"description": "Пользователь не имеет доступа к проекту."},
        404: {"description": "Проект не найден."},
    },
)
async def get_project_tasks_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение задач проекта. Доступно для всех пользователей, имеющих доступ к проекту.
    """
    logger.info("Пользователь ID %d запросил задачи проекта ID %d", current_user.id, project_id)

    await check_project_access(project_id, current_user, db)

    tasks = await get_tasks_for_project(db, project_id)
    logger.info("Найдено %d задач для проекта ID %d", len(tasks), project_id)

    return tasks
