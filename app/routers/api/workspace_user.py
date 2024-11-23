from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.schemas.workspace_user import WorkspaceUserCreate, WorkspaceUserResponse, WorkspaceUserUpdate
from app.crud.workspace_user import create_workspace_user, is_workspace_admin, update_workspace_user_role, remove_user_from_workspace, get_users_in_workspace
from app.routers.dependencies.jwt_functions import get_current_user
from typing import List

router = APIRouter(prefix="/workspaces/users", tags=["Workspace Users"])

@router.post("/", response_model=WorkspaceUserResponse, status_code=status.HTTP_201_CREATED)
async def add_user_to_workspace(
    workspace_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Добавление пользователя в рабочее пространство.

    Доступно только администраторам рабочего пространства.
    - **workspace_id**: ID рабочего пространства.
    - **user_id**: ID пользователя, которого нужно добавить.
    """
    # Проверяем, что текущий пользователь — администратор рабочего пространства
    if not await is_workspace_admin(db, workspace_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only workspace administrators can add users.",
        )

    # Присваиваем пользователю роль "member" по умолчанию
    access_level = "member"

    # Создаем связь пользователя с рабочим пространством
    try:
        workspace_user = await create_workspace_user(db, workspace_id, user_id, access_level)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return workspace_user


@router.get("/{workspace_id}", response_model=List[WorkspaceUserResponse], status_code=status.HTTP_200_OK)
async def list_workspace_users(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение списка пользователей рабочего пространства.
    Доступно только администраторам.
    """
    if not await is_workspace_admin(db, workspace_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrators can view workspace users.",
        )
    return await get_users_in_workspace(db, workspace_id)


@router.patch("/{workspace_id}/users/{user_id}", response_model=WorkspaceUserResponse, status_code=status.HTTP_200_OK)
async def update_user_role(
    workspace_id: int,
    user_id: int,
    update_data: WorkspaceUserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление роли пользователя в рабочем пространстве.
    Доступно только администраторам.
    """
    if not await is_workspace_admin(db, workspace_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrators can update roles.",
        )

    # Обновляем роль пользователя
    try:
        return await update_workspace_user_role(
            db, workspace_id, user_id, new_role=update_data.access_level
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{workspace_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_workspace(
    workspace_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаление пользователя из рабочего пространства.
    Доступно только администраторам.
    """
    if not await is_workspace_admin(db, workspace_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrators can remove users.",
        )

    if not await remove_user_from_workspace(db, workspace_id, user_id):
        raise HTTPException(status_code=404, detail="User not found in the workspace.")