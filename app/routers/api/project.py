from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
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
from app.routers.dependencies.permissions import check_workspace_owner, check_workspace_access
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project_endpoint(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создание нового проекта. Только для создателя рабочего пространства.
    """
    # Проверяем, что пользователь является владельцем рабочего пространства
    await check_workspace_owner(project_data.workspace_id, current_user, db)

    project_data.created_by = current_user.id
    project = await create_project(db, project_data)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение информации о проекте. Доступно для всех пользователей, имеющих доступ к рабочему пространству.
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Проверка прав доступа на уровне рабочего пространства
    workspace_id = project.workspace_id
    # Здесь предполагается функция check_workspace_access для редакторов/читателей
    if not await check_workspace_access(workspace_id, current_user, db, roles=["admin", "editor", "viewer"]):
        raise HTTPException(status_code=403, detail="Access denied")

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project_endpoint(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление проекта. Только для создателя рабочего пространства.
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Проверяем, что пользователь является владельцем рабочего пространства
    await check_workspace_owner(project.workspace_id, current_user, db)

    updated_project = await update_project(db, project_id, project_data)
    return updated_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаление проекта. Только для создателя рабочего пространства.
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Проверяем, что пользователь является владельцем рабочего пространства
    await check_workspace_owner(project.workspace_id, current_user, db)

    await delete_project(db, project_id)
    return {"message": "Project deleted successfully"}


@router.get("/{project_id}/tasks", response_model=List[dict])
async def get_project_tasks_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение задач проекта. Доступно для всех пользователей, имеющих доступ к рабочему пространству.
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Проверка прав доступа на уровне рабочего пространства
    workspace_id = project.workspace_id
    if not await check_workspace_access(workspace_id, current_user, db, roles=["admin", "editor", "viewer"]):
        raise HTTPException(status_code=403, detail="Access denied")

    tasks = await get_tasks_for_project(db, project_id)
    return tasks


@router.get("/{workspace_id}/projects/all", response_model=List[ProjectResponse])
async def get_all_projects_for_user(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение всех проектов для пользователя. Доступно для всех пользователей.
    """
    projects = await get_all_projects(db, current_user, workspace_id)
    return projects
