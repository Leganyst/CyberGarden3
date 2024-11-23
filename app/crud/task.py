from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.orm import aliased
from typing import Optional, List
from app.models.task import Task
from app.models.project import Project
from app.models.workspace import Workspace
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithReminders
from datetime import date
from app.models.reminder import Reminder

async def create_task(db: AsyncSession, task_data: TaskCreate) -> TaskResponse:
    """
    Создает новую задачу с опциональным напоминанием.
    :param db: Сессия базы данных.
    :param task_data: Данные для создания задачи.
    :return: Созданная задача в формате Pydantic модели.
    """
    # Создание задачи
    new_task = Task(
        name=task_data.name,
        project_id=task_data.project_id,
        created_by=task_data.created_by,
        assigned_to=task_data.assigned_to,
        due_date=task_data.due_date,
        priority=task_data.priority,
    )
    db.add(new_task)
    await db.flush()  # Генерируем ID задачи без фиксации транзакции

    # Создание напоминания, если указано время
    if task_data.reminder_time:
        reminder = Reminder(
            task_id=new_task.id,
            reminder_time=task_data.reminder_time,
        )
        db.add(reminder)

    # Фиксируем изменения
    await db.commit()

    # Подгружаем данные задачи вместе с напоминаниями
    await db.refresh(new_task)

    # Преобразуем данные в формат Pydantic
    task_response = TaskResponse(
        id=new_task.id,
        name=new_task.name,
        project_id=new_task.project_id,
        created_by=new_task.created_by,
        assigned_to=new_task.assigned_to,
        is_completed=new_task.is_completed,
        due_date=new_task.due_date,
        priority=new_task.priority,
        created_at=new_task.created_at,
        updated_at=new_task.updated_at,
    )

    return task_response


async def update_task(
    db: AsyncSession, task_id: int, task_data: TaskUpdate
) -> Optional[TaskResponse]:
    """
    Обновляет данные задачи.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :param task_data: Новые данные для обновления задачи.
    :return: Обновленная задача в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        return None

    if task_data.name is not None:
        task.name = task_data.name

    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """
    Удаляет задачу.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: True, если удаление успешно, иначе False.
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True


async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[TaskResponse]:
    """
    Извлекает задачу по ID.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: Задача в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task:
        return TaskResponse.model_validate(task)
    return None


async def get_task_with_reminders(
    db: AsyncSession, task_id: int
) -> Optional[TaskWithReminders]:
    """
    Извлекает задачу с ее напоминаниями.
    :param db: Сессия базы данных.
    :param task_id: ID задачи.
    :return: Задача с напоминаниями в формате Pydantic модели или None, если не найдена.
    """
    result = await db.execute(
        select(Task).options(selectinload(Task.reminders)).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    if task:
        task_data = TaskWithReminders.model_validate(task)
        task_data.reminders = [
            {"id": reminder.id, "reminder_time": reminder.reminder_time, "is_sent": reminder.is_sent}
            for reminder in task.reminders
        ]
        return task_data
    return None


async def get_tasks_for_project(
    db: AsyncSession, project_id: int
) -> List[TaskResponse]:
    """
    Извлекает все задачи для проекта.
    :param db: Сессия базы данных.
    :param project_id: ID проекта.
    :return: Список задач в формате Pydantic моделей.
    """
    result = await db.execute(select(Task).where(Task.project_id == project_id))
    tasks = result.scalars().all()
    return [TaskResponse.model_validate(task) for task in tasks]


async def get_user_tasks_by_date(
    db: AsyncSession, user_id: int, target_date: date
) -> List[dict]:
    """
    Извлекает все задачи пользователя на указанную дату с указанием проектов и рабочих пространств.
    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :param target_date: Дата, для которой извлекаются задачи.
    :return: Список задач в виде словарей.
    """
    # Запрос задач пользователя на указанную дату
    tasks_query = (
        select(
            Task.id,
            Task.name,
            Task.due_date,
            Task.is_completed,
            Task.created_at,
            Task.updated_at,
            Project.name.label("project_name"),
            Workspace.name.label("workspace_name"),
        )
        .join(Project, Task.project_id == Project.id)
        .join(Workspace, Project.workspace_id == Workspace.id)
        .where(
            Task.assigned_to == user_id,  # Условие: задачи, назначенные пользователю
            Task.due_date == target_date,  # Условие: задачи на указанную дату
        )
        .order_by(Task.due_date, Task.id)  # Сортировка
    )

    # Выполнение запроса
    result = await db.execute(tasks_query)
    rows = result.fetchall()

    # Преобразование данных в список словарей
    tasks = [
        {
            "id": row.id,
            "name": row.name,
            "project": row.project_name,
            "workspace": row.workspace_name,
            "due_date": row.due_date.isoformat(),
            "is_completed": row.is_completed,
            "created_at": row.created_at.isoformat(),
            "updated_at": row.updated_at.isoformat(),
        }
        for row in rows
    ]

    return tasks