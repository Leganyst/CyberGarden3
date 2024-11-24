from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.schemas.project_user import ProjectUserCreate, ProjectUserResponse, ProjectUserUpdate
from app.crud.project_user import (
    create_project_user,
    is_project_admin,
    update_project_user_role,
    remove_user_from_project,
    get_users_in_project
)
from app.routers.dependencies.jwt_functions import get_current_user
from typing import List

router = APIRouter(prefix="/projects/users", tags=["Project Users"])


@router.post("/", response_model=ProjectUserResponse, status_code=status.HTTP_201_CREATED)
async def add_user_to_project(
    project_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Добавление пользователя в проект.

    Доступно только администраторам проекта.
    - **project_id**: ID проекта.
    - **user_id**: ID пользователя, которого нужно добавить.
    """
    # Проверяем, что текущий пользователь — администратор проекта
    if not await is_project_admin(db, project_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only project administrators can add users.",
        )

    # Присваиваем пользователю роль "member" по умолчанию
    access_level = "member"

    # Создаем связь пользователя с проектом
    try:
        project_user = await create_project_user(db, project_id, user_id, access_level)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return project_user


@router.get("/{project_id}", response_model=List[ProjectUserResponse], status_code=status.HTTP_200_OK)
async def list_project_users(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение списка пользователей проекта.
    Доступно только администраторам.
    """
    if not await is_project_admin(db, project_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrators can view project users.",
        )
    return await get_users_in_project(db, project_id)


@router.patch("/{project_id}/users/{user_id}", response_model=ProjectUserResponse, status_code=status.HTTP_200_OK)
async def update_user_role_in_project(
    project_id: int,
    user_id: int,
    update_data: ProjectUserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление роли пользователя в проекте.
    Доступно только администраторам.
    """
    if not await is_project_admin(db, project_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrators can update roles.",
        )

    # Обновляем роль пользователя
    try:
        return await update_project_user_role(
            db, project_id, user_id, new_role=update_data.access_level
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{project_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_project(
    project_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаление пользователя из проекта.
    Доступно только администраторам.
    """
    if not await is_project_admin(db, project_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrators can remove users.",
        )

    if not await remove_user_from_project(db, project_id, user_id):
        raise HTTPException(status_code=404, detail="User not found in the project.")
