from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/index.html")
def serve_index():
    return FileResponse("frontend/index.html")

@app.get("/dashboard.html")
def serve_dashboard():
    return FileResponse("frontend/dashboard.html")

@app.get("/setup.html")
def serve_setup():
    return FileResponse("frontend/setup.html")

@app.get("/tasks.html")
def serve_tasks():
    return FileResponse("frontend/tasks.html")

@app.get("/history.html")
def serve_history():
    return FileResponse("frontend/history.html")

@app.get("/end-of-day.html")
def serve_end_of_day():
    return FileResponse("frontend/end-of-day.html")

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "exam-plan-tracker"}
