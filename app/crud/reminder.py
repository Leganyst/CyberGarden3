from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse


async def create_reminder(db: AsyncSession, reminder_data: ReminderCreate) -> ReminderResponse:
    """
    Создает новое напоминание.
    :param db: Сессия базы данных.
    :param reminder_data: Данные для создания напоминания.
    :return: Созданное напоминание в формате Pydantic модели.
    """
    new_reminder = Reminder(
        task_id=reminder_data.task_id,
        reminder_time=reminder_data.reminder_time,
        is_sent=reminder_data.is_sent or False,
    )
    db.add(new_reminder)
    await db.commit()
    await db.refresh(new_reminder)
    return ReminderResponse.model_validate(new_reminder)


async def update_reminder(
    db: AsyncSession, reminder_id: int, reminder_data: ReminderUpdate
) -> Optional[ReminderResponse]:
    """
    Обновляет данные напоминания.
    :param db: Сессия базы данных.
    :param reminder_id: ID напоминания.
    :param reminder_data: Новые данные для обновления напоминания.
    :return: Обновленное напоминание в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(select(Reminder).where(Reminder.id == reminder_id))
    reminder = result.scalar_one_or_none()
    if not reminder:
        return None

    if reminder_data.reminder_time is not None:
        reminder.reminder_time = reminder_data.reminder_time
    if reminder_data.is_sent is not None:
        reminder.is_sent = reminder_data.is_sent

    await db.commit()
    await db.refresh(reminder)
    return ReminderResponse.model_validate(reminder)


async def delete_reminder(db: AsyncSession, reminder_id: int) -> bool:
    """
    Удаляет напоминание.
    :param db: Сессия базы данных.
    :param reminder_id: ID напоминания.
    :return: True, если удаление успешно, иначе False.
    """
    result = await db.execute(select(Reminder).where(Reminder.id == reminder_id))
    reminder = result.scalar_one_or_none()
    if not reminder:
        return False

    await db.delete(reminder)
    await db.commit()
    return True


async def get_reminder_by_id(
    db: AsyncSession, reminder_id: int
) -> Optional[ReminderResponse]:
    """
    Извлекает напоминание по ID.
    :param db: Сессия базы данных.
    :param reminder_id: ID напоминания.
    :return: Напоминание в формате Pydantic модели или None, если не найдено.
    """
    result = await db.execute(select(Reminder).where(Reminder.id == reminder_id))
    reminder = result.scalar_one_or_none()
    if reminder:
        return ReminderResponse.model_validate(reminder)
    return None


async def get_reminders_for_task(
    db: AsyncSession, task_id: int
) -> List[ReminderResponse]:
    """
    Извлекает все напоминания для задачи.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: Список напоминаний в формате Pydantic моделей.
    """
    result = await db.execute(select(Reminder).where(Reminder.task_id == task_id))
    reminders = result.scalars().all()
    return [ReminderResponse.model_validate(reminder) for reminder in reminders]
