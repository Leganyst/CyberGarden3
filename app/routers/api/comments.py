from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.comments import Comment
from app.schemas.comments import CommentResponse, CommentCreate
from app.models.task import Task
from app.models.user import User
from app.core.database import get_db
from app.routers.dependencies.jwt_functions import get_current_user
from app.routers.dependencies.permissions import check_project_access
from app.crud.task import get_task_by_id

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Создание нового комментария к задаче.
    """
    # Проверяем права доступа к задаче
    task = await get_task_by_id(db, comment_data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not await check_project_access(task.project.workspace_id, current_user, db):
        raise HTTPException(status_code=403, detail="Access denied")

    # Создаём комментарий
    new_comment = Comment(
        task_id=comment_data.task_id,
        user_id=current_user.id,
        content=comment_data.content,
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return CommentResponse.model_validate(new_comment)


