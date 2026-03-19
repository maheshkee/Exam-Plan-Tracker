# Project Context

## 1. What the app does

Exam Plan Tracker is a FastAPI-based study planning application for exam preparation. Users can register, log in, enroll in one exam, view that exam's syllabus, create daily study tasks from syllabus topics, log completed or skipped work, and track progress against the target exam date. The backend also stores end-of-day progress snapshots and sends reminder emails to enrolled users who have not logged activity.

## 2. Full tech stack

### Backend

- Python 3
- FastAPI
- Uvicorn
- SQLAlchemy 2.0 ORM
- Alembic migrations
- Pydantic / `pydantic-settings`
- APScheduler

### Authentication and security

- JWT access tokens via `python-jose`
- Password hashing via `passlib[bcrypt]` and `bcrypt`
- OAuth2 bearer token dependency in FastAPI

### Database

- Development: SQLite
- Production: PostgreSQL on Render
- Current local `.env` default: `sqlite:///./exam_tracker.db`

### Email and notifications

- Gmail SMTP using Python `smtplib`
- Daily reminder scheduling with APScheduler cron job

### Frontend

- Static HTML, CSS, and JavaScript served by FastAPI from the `frontend/` directory
- Planned future frontend hosting: Vercel

### Testing and tooling

- Pytest
- FastAPI `TestClient`
- HTTPX
- Local virtual environment at `.venv`

## 3. Database schema

The ORM models and the Alembic migration define the same nine-table core schema.

### `users`

- `id` — integer primary key, autoincrement
- `email` — string(255), unique, indexed, not null
- `password_hash` — string(255), not null
- `created_at` — datetime, default `datetime.utcnow`, not null

Relationships:

- One-to-one with `user_exams` through `User.user_exam`

### `exams`

- `id` — integer primary key, autoincrement
- `name` — string(100), not null
- `description` — text, nullable

Relationships:

- One-to-many with `subjects`
- One-to-many with `user_exams`

### `subjects`

- `id` — integer primary key, autoincrement
- `exam_id` — foreign key to `exams.id`, not null
- `name` — string(100), not null

Relationships:

- Many-to-one to `exams`
- One-to-many with `topics`

### `topics`

- `id` — integer primary key, autoincrement
- `subject_id` — foreign key to `subjects.id`, not null
- `name` — string(150), not null
- `estimated_hours` — float, not null

Relationships:

- Many-to-one to `subjects`
- One-to-many with `daily_tasks`

### `user_exams`

- `id` — integer primary key, autoincrement
- `user_id` — foreign key to `users.id`, unique, not null
- `exam_id` — foreign key to `exams.id`, not null
- `exam_date` — date, not null
- `study_hours_per_day` — float, not null
- `created_at` — datetime, default `datetime.utcnow`, not null

Relationships:

- One-to-one / many-to-one link from `users`
- Many-to-one to `exams`
- One-to-many with `daily_tasks`
- One-to-many with `progress_snapshots`
- One-to-many with `notification_logs`

Important constraint:

- `user_id` is unique, so the current product supports only one active exam enrollment per user

### `daily_tasks`

- `id` — integer primary key, autoincrement
- `user_exam_id` — foreign key to `user_exams.id`, not null
- `topic_id` — foreign key to `topics.id`, not null
- `task_date` — date, not null
- `planned_hours` — float, not null

Relationships:

- Many-to-one to `user_exams`
- Many-to-one to `topics`
- One-to-one with `task_logs` through `DailyTask.task_log`

### `task_logs`

- `id` — integer primary key, autoincrement
- `daily_task_id` — foreign key to `daily_tasks.id`, unique, not null
- `actual_hours` — float, nullable
- `status` — string(20), not null
  - Allowed in code: `COMPLETED`, `SKIPPED`
- `updated_at` — datetime, default and on-update `datetime.utcnow`, not null

Relationships:

- One-to-one to `daily_tasks`

Important constraint:

- `daily_task_id` is unique, so each task can have only one current log record

### `progress_snapshots`

- `id` — integer primary key, autoincrement
- `user_exam_id` — foreign key to `user_exams.id`, not null
- `snapshot_date` — date, not null
- `topics_completed` — integer, default 0, not null
- `hours_completed` — float, default 0.0, not null
- `pace_status` — string(20), not null
  - Used in code: `AHEAD`, `ON_TRACK`, `BEHIND`

Relationships:

- Many-to-one to `user_exams`

### `notification_logs`

- `id` — integer primary key, autoincrement
- `user_exam_id` — foreign key to `user_exams.id`, not null
- `notification_type` — string(50), not null
- `sent_at` — datetime, default `datetime.utcnow`, not null

Relationships:

- Many-to-one to `user_exams`

Used value in code:

- `REMINDER`

### Relationship summary

- One `Exam` has many `Subject`
- One `Subject` has many `Topic`
- One `User` has at most one `UserExam`
- One `UserExam` belongs to one `Exam`
- One `UserExam` has many `DailyTask`
- One `DailyTask` belongs to one `Topic`
- One `DailyTask` has at most one `TaskLog`
- One `UserExam` has many `ProgressSnapshot`
- One `UserExam` has many `NotificationLog`

## 4. API routes

### Auth routes

- `POST /auth/register` — Auth required: No — Register a new user with email and password
- `POST /auth/login` — Auth required: No — Authenticate a user and return a bearer JWT
- `GET /auth/me` — Auth required: Yes — Return the currently authenticated user

### Exam routes

- `GET /exams` — Auth required: No — List available exams
- `GET /exams/{exam_id}` — Auth required: No — Return one exam with subjects and topics
- `POST /exams/enroll` — Auth required: Yes — Create the current user's exam enrollment
- `GET /exams/my-enrollment` — Auth required: Yes — Return the current user's active enrollment summary

### Task routes

- `POST /tasks` — Auth required: Yes — Create a daily task for a syllabus topic in the enrolled exam
- `GET /tasks?task_date=YYYY-MM-DD` — Auth required: Yes — List the current user's tasks for a specific date
- `PATCH /tasks/{task_id}/log` — Auth required: Yes — Mark a task completed or skipped and store actual hours

### Progress routes

- `GET /progress/dashboard` — Auth required: Yes — Return summary metrics for enrollment, syllabus completion, pace, and today's tasks
- `POST /progress/end-of-day?target_date=YYYY-MM-DD` — Auth required: Yes — Generate or update the end-of-day progress snapshot for a date
- `GET /progress/history` — Auth required: Yes — Return historical progress snapshots in descending date order
- `POST /progress/trigger-reminders` — Auth required: Yes — Manually run the reminder check for testing

### System and static routes

- `GET /health` — Auth required: No — Basic service health check
- `GET /` and other frontend paths served from `frontend/` — Auth required: No at FastAPI layer — Serve the static frontend

## 5. Key design decisions

### Single active exam per user

Reasoning:

- The `user_exams.user_id` unique constraint simplifies planning, dashboard aggregation, reminders, and the current frontend flow.
- This is also why “Multiple exams per user” is already called out as the next phase.

### Syllabus-first planning model

Reasoning:

- Tasks are always tied to a `Topic`, and topics roll up to `Subject` and `Exam`.
- This prevents free-form task drift and allows the app to compute total syllabus hours, completion percentage, and required daily pace from structured data.

### Keep task logs separate from planned tasks

Reasoning:

- `daily_tasks` stores the plan.
- `task_logs` stores actual execution and can be created later or updated independently.
- This separation makes it easier to distinguish pending tasks from completed or skipped work.

### Derived pace instead of storing too much state

Reasoning:

- Dashboard metrics are computed from enrollment data, syllabus totals, and completed logs rather than denormalizing everything into the database.
- This keeps the source of truth in the normalized tables and reduces sync risk.

### Snapshotting end-of-day progress

Reasoning:

- `progress_snapshots` captures cumulative progress by date so historical trends can be displayed without replaying every task at read time.
- The service uses an upsert-style pattern for the same `snapshot_date`.

### Scheduler-driven reminders with logging

Reasoning:

- Reminder delivery is decoupled from the request/response cycle and runs daily at 20:00 through APScheduler.
- `notification_logs` prevents duplicate reminder sends for the same day.

### Render-friendly deployment

Reasoning:

- The repo is set up to migrate and seed on startup via `start.sh`, which reduces manual setup friction after deploy.
- The database layer supports both SQLite and PostgreSQL using the same SQLAlchemy models.

### Serve the static frontend from the backend for now

Reasoning:

- `app.main` mounts `frontend/` directly, which keeps local development simple.
- The deployment docs already anticipate splitting the frontend later, with Vercel planned.

### Important implementation note

The app currently mixes Alembic migrations with `Base.metadata.create_all(bind=engine)` during startup. That is convenient in development, but it means schema management is not purely migration-driven yet.

## 6. Current phase status

All phases from Phase 0 through Phase 10 are complete in the current codebase.

Current state by area:

- Core FastAPI backend: complete
- Auth and JWT flow: complete
- Exam catalog and syllabus APIs: complete
- Single-exam enrollment flow: complete
- Task planning and task logging: complete
- Dashboard, end-of-day snapshots, and history: complete
- Reminder emails and scheduler: complete
- Seed data, tests, and Render deployment setup: complete

## 7. Planned future phases

- Multiple exams per user
- Complete CA + SSC syllabus
- AI syllabus confirmation using Gemini API
- AI pacing guide
- Gmail OAuth and forgot password flows

## 8. Deployment info

### Backend

- Target platform: Render web service
- Render config file: `render.yaml`
- Build command: `pip install -r requirements.txt`
- Start command in Render config: `bash start.sh`
- `start.sh` behavior:
  - Runs `PYTHONPATH=. alembic upgrade head`
  - Runs `PYTHONPATH=. python3 scripts/seed.py`
  - Starts Uvicorn on `${PORT:-8000}`

### Database

- Production database: Render PostgreSQL
- Development database: SQLite
- Database URL comes from environment variable `DATABASE_URL`

### Required environment variables

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`

### Frontend

- Current state: static frontend inside `frontend/`
- Current backend serves it directly with `StaticFiles`
- Planned deployment direction: Vercel frontend, Render backend
- Frontend API base URL must be changed from localhost to the Render backend URL before separate frontend deployment

## 9. What Claude Code must know to work on this project

### Runtime and commands

- Project root should usually be on `PYTHONPATH`, especially for Alembic, seed, and test commands:
  - `PYTHONPATH=. alembic upgrade head`
  - `PYTHONPATH=. python3 scripts/seed.py`
  - `PYTHONPATH=. pytest tests/ -v`
- Local virtual environment exists at `.venv`
- Standard local dev server:
  - `uvicorn app.main:app --reload`

### Database files currently present in the repo root

- `exam_tracker.db` — current local default from `.env`
- `test.db` — pytest database from `tests/conftest.py`
- `exam_plan_tracker.db` — extra SQLite file present in the root; verify whether it is stale before relying on it

### Startup behavior

- App startup runs:
  - `Base.metadata.create_all(bind=engine)`
  - exam seeding for a minimal set of exams in `app.main.seed_exams()`
  - APScheduler startup via `start_scheduler()`
- Production startup script separately runs Alembic and the full syllabus seed script

### Seed behavior

- `app.main.seed_exams()` only ensures a small base exam list exists
- `scripts/seed.py` seeds structured syllabus content for:
  - `GATE CS`
  - `SSC CGL`
  - `Banking (IBPS PO)`
- If routes depending on subjects/topics look empty, check whether `scripts/seed.py` has been run

### Auth model assumptions

- JWT payload contains `user_id`
- Protected endpoints rely on `Authorization: Bearer <token>`
- `OAuth2PasswordBearer` is configured with `tokenUrl="/auth/login"`

### Product constraints that affect future work

- One user can only have one active `user_exams` row
- Tasks must belong to topics under the user's enrolled exam
- Progress is measured from completed `TaskLog` rows and distinct completed topic IDs
- Reminder emails depend on SMTP credentials and currently send a plain-text Gmail reminder

### Known operational nuances

- CORS is fully open right now: `allow_origins=["*"]`
- The app mounts the frontend at `/`, so route collisions with future SPA/frontend paths need care
- The codebase currently uses both Alembic migrations and `create_all`, so schema changes should be handled deliberately
- Scheduler startup happens inside the FastAPI app lifecycle; tests and local runs may trigger it unless isolated

### Main code areas

- `app/routers/` — API entrypoints
- `app/services/` — business logic
- `app/models/` — SQLAlchemy models
- `app/schemas/` — request and response contracts
- `app/utils/` — auth, dependency injection, email helpers
- `scripts/seed.py` — full syllabus seed
- `tests/` — backend test coverage
