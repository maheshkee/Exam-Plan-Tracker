#!/bin/bash
echo "Running migrations..."
PYTHONPATH=. alembic upgrade head
echo "Running seed..."
PYTHONPATH=. python3 scripts/seed.py
echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
