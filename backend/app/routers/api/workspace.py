from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.models.workspace import Workspace
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceResponse,
)
from app.crud.workspace import (
    create_workspace,
    update_workspace,
    delete_workspace,
    get_workspace_by_id,
    get_workspaces_user
)
from app.routers.dependencies.jwt_functions import get_current_user
from app.routers.dependencies.permissions import check_workspace_owner
from app.models.user import User

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_workspace_endpoint(
    workspace_data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создание нового рабочего пространства.
    """
    workspace = await create_workspace(db, workspace_data, current_user)
    return workspace
    
    return workspace
@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace_endpoint(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение информации о рабочем пространстве. Только для владельцев.
    """
    workspace = await get_workspace_by_id(db, workspace_id, current_user)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Проверяем, является ли пользователь владельцем
    if workspace.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return workspace


@router.get("/", response_model=List[WorkspaceResponse])
async def list_user_workspaces(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение списка всех рабочих пространств текущего пользователя.
    """
    # Здесь предполагается, что CRUD-функция list_user_workspaces реализована.
    user_workspaces = await get_workspaces_user(db, current_user)
    return user_workspaces


@router.patch("/{workspace_id}")
async def update_workspace_endpoint(
    workspace_id: int,
    workspace_data: WorkspaceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление рабочего пространства. Только для владельцев.
    """
    workspace = await get_workspace_by_id(db, workspace_id, current_user)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Проверяем, является ли пользователь владельцем
    if workspace.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")


    return {"workspace_id": workspace_id,
            "name": workspace_data.name}

