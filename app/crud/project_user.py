from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project_user import ProjectUser
from app.schemas.project_user import ProjectUserResponse


async def create_project_user(db: AsyncSession, project_id: int, user_id: int, access_level: str):
    existing = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        )
    )
    if existing.scalar():
        raise ValueError("User already exists in the project.")

    new_user = ProjectUser(
        project_id=project_id,
        user_id=user_id,
        access_level=access_level,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return ProjectUserResponse.model_validate(new_user)


async def is_project_admin(db: AsyncSession, project_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id,
            ProjectUser.access_level == "admin"
        )
    )
    return result.scalar() is not None


async def update_project_user_role(db: AsyncSession, project_id: int, user_id: int, new_role: str):
    result = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        )
    )
    project_user = result.scalar_one_or_none()
    if not project_user:
        raise ValueError("User not found in the project.")

    project_user.access_level = new_role
    await db.commit()
    await db.refresh(project_user)
    return ProjectUserResponse.model_validate(project_user)


async def remove_user_from_project(db: AsyncSession, project_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        )
    )
    project_user = result.scalar_one_or_none()
    if not project_user:
        return False

    await db.delete(project_user)
    await db.commit()
    return True


async def get_users_in_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(ProjectUser).where(ProjectUser.project_id == project_id))
    project_users = result.scalars().all()
    return [ProjectUserResponse.model_validate(pu) for pu in project_users]
