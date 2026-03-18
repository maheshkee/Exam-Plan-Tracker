from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth as auth_router
from app.routers import exam as exam_router
from app.routers import task as task_router
from app.routers import progress as progress_router

print("🔥 MAIN FILE LOADED")

app = FastAPI(title="exam-plan-tracker")

@app.on_event("startup")
def startup_event():
    print("🔥 STARTUP EVENT RUNNING")
    try:
        from app.database import Base, engine
        import app.models
        from app.models import user
        from app.scheduler import start_scheduler

        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
        start_scheduler()
    except Exception as e:
        print("DB INIT ERROR:", e)

@app.on_event("shutdown")
def shutdown_event():
    from app.scheduler import stop_scheduler

    stop_scheduler()

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

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "exam-plan-tracker"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
