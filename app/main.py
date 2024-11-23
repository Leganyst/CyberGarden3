# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.core.database import engine, Base
from app.models import user, workspace, workspace_user, project, task, reminder
from app.routers.api.auth import router as auth_router
from app.routers.api.ping import router as ping_router
from app.routers.api.workspace import router as workspace_router
from app.routers.api.project import router as project_router
from app.routers.api.task import router as task_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Разрешить все источники
#     allow_credentials=True,
#     # allow_methods=["*"],
#     # allow_headers=["*"],
# )


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"
    )

app.include_router(auth_router)
app.include_router(ping_router)
app.include_router(workspace_router)
app.include_router(project_router)
app.include_router(task_router)
