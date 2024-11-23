from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from app.models.user import User
from app.models.task import Task
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderResponse
from app.core.database import get_db
from app.routers.dependencies.jwt_functions import get_current_user

router = APIRouter(
    tags=["User"],
    prefix="/user",    
)

@router.get("/reminders", status_code=status.HTTP_200_OK)
async def get_user_reminders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Получение напоминаний для пользователя по его задачам.
    """
    # Текущее время
    now = datetime.now(timezone.utc)

    # Запрос напоминаний, связанных с задачами пользователя
    result = await db.execute(
        select(Reminder, Task)
        .join(Task, Reminder.task_id == Task.id)
        .where(
            Task.assigned_to == current_user.id,  # Только задачи пользователя
            Reminder.reminder_time <= now,       # Напоминания с прошедшим временем
            Reminder.is_sent == False           # Напоминания, которые ещё не отправлены
        )
        .options(selectinload(Reminder.task))   # Подгружаем связанные задачи
    )
    reminders = result.fetchall()

    # Преобразование результатов в список словарей
    reminders_data = [
        {
            "reminder_id": reminder.id,
            "reminder_time": reminder.reminder_time,
            "due_date": task.due_date,
            "task_id": task.id,
            "task_name": task.name,
            "project_id": task.project_id,
            "need_notification": now > reminder.reminder_time,
        }
        for reminder, task in reminders
    ]

    return reminders_data
