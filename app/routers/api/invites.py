from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.routers.dependencies.jwt_functions import get_current_user
from app.crud.invites import (
    get_user_invites,
    send_invite_to_project,
    accept_project_invite,
    decline_project_invite,
)
from app.models.user import User

router = APIRouter(prefix="/projects/{project_id}/invites", tags=["Project Invites"])


@router.post(
    "/send",
    status_code=status.HTTP_200_OK,
    summary="Отправить инвайт пользователю",
    description=(
        "Отправляет инвайт пользователю с указанным `user_id` в проект с `project_id`. "
        "Доступно только для пользователей с ролью `admin` в проекте."
    ),
    responses={
        200: {
            "description": "Инвайт успешно отправлен.",
            "content": {
                "application/json": {
                    "example": {"message": "Инвайт отправлен."}
                }
            },
        },
        403: {
            "description": "Пользователь не имеет прав на отправку инвайтов.",
            "content": {
                "application/json": {
                    "example": {"detail": "Доступ запрещен."}
                }
            },
        },
        404: {
            "description": "Проект или пользователь не найден.",
            "content": {
                "application/json": {
                    "example": {"detail": "Проект или пользователь не найден."}
                }
            },
        },
    },
)
async def send_invite(
    project_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Отправляет инвайт пользователю на проект.

    **Параметры:**
    - `project_id`: ID проекта, в который отправляется инвайт.
    - `user_id`: ID пользователя, которому отправляется инвайт.

    **Требования:**
    - Текущий пользователь должен иметь роль `admin` в проекте.
    """
    await send_invite_to_project(db, project_id, user_id, current_user)
    return {"message": "Инвайт отправлен."}


@router.post(
    "/accept",
    status_code=status.HTTP_200_OK,
    summary="Принять инвайт",
    description="Принимает инвайт текущего пользователя в проект с указанным `project_id`.",
    responses={
        200: {
            "description": "Инвайт успешно принят.",
            "content": {
                "application/json": {
                    "example": {"message": "Инвайт принят."}
                }
            },
        },
        403: {
            "description": "Инвайт недействителен или доступ запрещен.",
            "content": {
                "application/json": {
                    "example": {"detail": "Доступ запрещен."}
                }
            },
        },
        404: {
            "description": "Инвайт не найден.",
            "content": {
                "application/json": {
                    "example": {"detail": "Инвайт не найден."}
                }
            },
        },
    },
)
async def accept_invite(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Принимает инвайт на проект.

    **Параметры:**
    - `project_id`: ID проекта, для которого принимается инвайт.

    **Требования:**
    - У пользователя должен быть статус `invited` для указанного проекта.
    """
    await accept_project_invite(db, project_id, current_user.id)
    return {"message": "Инвайт принят."}


@router.post(
    "/decline",
    status_code=status.HTTP_200_OK,
    summary="Отклонить инвайт",
    description="Отклоняет инвайт текущего пользователя в проект с указанным `project_id`.",
    responses={
        200: {
            "description": "Инвайт успешно отклонен.",
            "content": {
                "application/json": {
                    "example": {"message": "Инвайт отклонен."}
                }
            },
        },
        404: {
            "description": "Инвайт не найден.",
            "content": {
                "application/json": {
                    "example": {"detail": "Инвайт не найден."}
                }
            },
        },
    },
)
async def decline_invite(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Отклоняет инвайт на проект.

    **Параметры:**
    - `project_id`: ID проекта, для которого отклоняется инвайт.

    **Требования:**
    - У пользователя должен быть статус `invited` для указанного проекта.
    """
    await decline_project_invite(db, project_id, current_user.id)
    return {"message": "Инвайт отклонен."}


@router.get(
    "/invites",
    summary="Получить инвайты пользователя",
    description="Возвращает список проектов, на которые пользователь приглашен.",
    responses={
        200: {
            "description": "Инвайты успешно получены.",
            "content": {
                "application/json": {
                    "example": [
                        {"project_id": 1, "project_name": "Project Alpha"},
                        {"project_id": 2, "project_name": "Project Beta"}
                    ]
                }
            },
        },
        404: {"description": "Инвайты не найдены."},
        500: {"description": "Ошибка сервера."},
    },
)
async def get_user_invites_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение инвайтов пользователя.
    
    ### Поля ответа:
    - **project_id**: Уникальный идентификатор проекта.
    - **project_name**: Название проекта.
    """
    try:
        invites = await get_user_invites(db, current_user.id)
        if not invites:
            raise HTTPException(status_code=404, detail="Инвайты не найдены.")
        return invites
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))