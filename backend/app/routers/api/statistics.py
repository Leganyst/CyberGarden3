from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from app.core.database import get_db
from app.routers.dependencies.jwt_functions import get_current_user
from app.models.user import User
from app.crud.statistics import get_user_task_statistics
import logging

from app.schemas.statistics import TaskStatistics

# Логирование
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter(prefix="/tasks/stats", tags=["Task Statistics"])

@router.get(
    "/",
    response_model=List[TaskStatistics],
    summary="Получить статистику задач пользователя",
    description=(
        "Возвращает статистику задач, назначенных текущему пользователю, "
        "в разрезе проектов. Включает общее количество задач, а также "
        "количество задач с каждым статусом ('OPEN', 'IN_PROGRESS', 'COMPLETED')."
    ),
    responses={
        200: {
            "description": "Статистика успешно получена.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "project_name": "Project A",
                            "total_tasks": 15,
                            "open_tasks": 5,
                            "in_progress_tasks": 7,
                            "completed_tasks": 3
                        },
                        {
                            "project_name": "Project B",
                            "total_tasks": 10,
                            "open_tasks": 3,
                            "in_progress_tasks": 4,
                            "completed_tasks": 3
                        }
                    ]
                }
            },
        },
        401: {"description": "Пользователь не авторизован."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_task_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Возвращает статистику задач для текущего пользователя в разрезе проектов.
    """
    try:
        logger.info("Fetching task statistics for user: %s", current_user.id)

        # Получение статистики
        stats = await get_user_task_statistics(db, current_user.id)
        
        logger.info("Task statistics fetched successfully for user: %s", current_user.id)
        return stats

    except Exception as e:
        logger.error("Failed to fetch task statistics for user: %s, Error: %s", current_user.id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось получить статистику задач."
        )
