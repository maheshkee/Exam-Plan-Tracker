# Development Log

This log is retroactively reconstructed from the current repository state on 2026-03-19.

## 2026-03-19 — Phase 0: Project foundation
**What was built:** FastAPI app bootstrapping, backend package layout, static frontend mounting from `frontend/`, health endpoint, dependency setup, and initial local run flow with Uvicorn.
**Issues encountered:** The app needed a simple way to support both API development and a lightweight frontend without introducing a separate frontend deployment requirement too early.
**Key decisions:** The backend serves the static frontend directly through `StaticFiles`, and the repository keeps a minimal HTML/CSS/JS frontend alongside the Python app to reduce early integration friction.
**Status:** Complete

## 2026-03-19 — Phase 1: Data model and persistence
**What was built:** SQLAlchemy models, session management, environment-driven database configuration, and the initial Alembic migration for the core schema.
**Issues encountered:** The project needed to work in local SQLite development while remaining deployable to PostgreSQL in production.
**Key decisions:** The database layer branches connection args by database type, and the schema was normalized around users, exams, syllabus, tasks, logs, snapshots, and notifications.
**Status:** Complete

## 2026-03-19 — Phase 2: Authentication and user identity
**What was built:** User registration, login, password hashing, JWT creation and decoding, and authenticated user lookup through FastAPI dependencies.
**Issues encountered:** The app needed basic account security and a clean way to protect later routes without duplicating auth logic in every router.
**Key decisions:** JWT bearer auth was chosen with `OAuth2PasswordBearer`, passwords are hashed with bcrypt through Passlib, and `/auth/me` provides the canonical authenticated-user check.
**Status:** Complete

## 2026-03-19 — Phase 3: Exam catalog and syllabus structure
**What was built:** Public exam listing, exam detail retrieval with nested subjects and topics, model relationships for syllabus content, and initial exam seeding on startup.
**Issues encountered:** The planning engine needed structured syllabus content rather than flat exam names to support pacing and task generation.
**Key decisions:** Exams, subjects, and topics were modeled as separate tables, and exam detail queries eager-load the full syllabus tree for a single response payload.
**Status:** Complete

## 2026-03-19 — Phase 4: Single-exam enrollment and pacing baseline
**What was built:** User enrollment into an exam, enrollment summary retrieval, future-date validation, and derived metrics such as days remaining and required hours per day.
**Issues encountered:** The app needed a stable planning baseline before adding tasks, but multi-exam support would have added complexity early.
**Key decisions:** Each user is limited to one active `user_exams` row via a unique constraint on `user_id`, making progress and reminder logic simpler in the current phase.
**Status:** Complete

## 2026-03-19 — Phase 5: Daily task planning
**What was built:** Daily task creation and date-based task listing for the enrolled user, with denormalized response fields for topic and subject names.
**Issues encountered:** Tasks had to be constrained so users could not schedule content outside their enrolled exam's syllabus.
**Key decisions:** Every task is tied to a syllabus topic, and task creation validates that the chosen topic belongs to the current user's enrolled exam before saving.
**Status:** Complete

## 2026-03-19 — Phase 6: Task logging and execution tracking
**What was built:** Task log creation and updates, `COMPLETED` or `SKIPPED` status handling, actual study hours tracking, and one-log-per-task enforcement.
**Issues encountered:** Planned work and actual work needed to be represented separately so the app could distinguish pending tasks from completed or skipped effort.
**Key decisions:** `task_logs` was split from `daily_tasks`, and `daily_task_id` was made unique so each planned task has one current execution record.
**Status:** Complete

## 2026-03-19 — Phase 7: Progress dashboard and historical snapshots
**What was built:** Dashboard aggregation, cumulative syllabus completion metrics, pace classification, end-of-day snapshot generation, and snapshot history retrieval.
**Issues encountered:** The app needed both live derived metrics and a historical view without recalculating every past day from scratch in the UI.
**Key decisions:** The dashboard is computed dynamically from tasks and logs, while `progress_snapshots` stores date-level cumulative progress for history and reporting.
**Status:** Complete

## 2026-03-19 — Phase 8: Notifications and scheduler
**What was built:** Daily reminder scheduling at 20:00, email sending through Gmail SMTP, notification deduplication, and a manual reminder trigger endpoint for testing.
**Issues encountered:** Reminder sending needed to avoid duplicate messages and avoid coupling background behavior to normal request handling.
**Key decisions:** APScheduler runs the reminder job in-process, and `notification_logs` records sent reminders so the service can suppress repeat sends on the same day.
**Status:** Complete

## 2026-03-19 — Phase 9: Seed data and deployment workflow
**What was built:** Full syllabus seed script, Render deployment configuration, startup migration and seed flow, and production environment variable setup.
**Issues encountered:** Production needed richer syllabus data than the minimal startup seeding, plus a repeatable deploy sequence for database setup.
**Key decisions:** `scripts/seed.py` handles the real syllabus dataset, while `start.sh` runs migrations and seeding before starting Uvicorn on Render.
**Status:** Complete

## 2026-03-19 — Phase 10: Testing and completion hardening
**What was built:** Pytest coverage for auth, exams, tasks, and progress flows using a SQLite test database and dependency overrides.
**Issues encountered:** The codebase needed confidence across the main user journeys while keeping test setup simple and isolated from production services.
**Key decisions:** Tests run against `test.db` with FastAPI dependency overrides, and the covered flows line up with the current milestone where Phases 0 through 10 are considered complete.
**Status:** Complete
