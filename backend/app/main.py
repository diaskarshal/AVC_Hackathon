from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import (
    auth,
    users,
    projects,
    resources,
    tasks,
    budgets,
    analytics,
    import_data,
)
from app.middleware.error_handler import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handlers(app)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(
    resources.router, prefix="/api/resources", tags=["Resources"]
)
app.include_router(budgets.router, prefix="/api/budgets", tags=["Budgets"])
app.include_router(
    analytics.router, prefix="/api/analytics", tags=["Analytics"]
)
app.include_router(import_data.router, prefix="/api/import", tags=["Import"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to BuildFlow ERP API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}