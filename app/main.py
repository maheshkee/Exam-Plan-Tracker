from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth as auth_router
from app.routers import exam as exam_router
from app.routers import task as task_router
from app.routers import progress as progress_router
from app.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(title="exam-plan-tracker", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(exam_router.router)
app.include_router(task_router.router)
app.include_router(progress_router.router)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h1>Exam Plan Tracker 🚀</h1>
    <p>Backend is running successfully.</p>
    <a href="/docs">Go to API Docs</a>
    """

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "exam-plan-tracker"}
