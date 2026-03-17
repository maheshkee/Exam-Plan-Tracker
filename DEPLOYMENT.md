# Deployment Guide — Exam Plan Tracker

## Platform: Render.com

### One-time Setup Steps

1. Push this repo to GitHub
2. Go to https://render.com and create a new account
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Render will auto-detect render.yaml
6. Add these environment variables manually in Render dashboard:
   - EMAIL_USERNAME → your Gmail address
   - EMAIL_PASSWORD → your Gmail App Password (not your login password)
     Get it at: Google Account → Security → App Passwords
7. Click "Deploy"

### After First Deploy

Run database migrations via Render Shell:
  PYTHONPATH=. alembic upgrade head

Run seed script via Render Shell:
  PYTHONPATH=. python3 scripts/seed.py

### Frontend Deployment

The frontend is plain HTML/CSS/JS.
Options:
- Render Static Site (free): point to /frontend folder
- GitHub Pages: enable in repo settings → Pages → /frontend folder
- Just open frontend/index.html locally for development

One required change before deploying frontend:
In frontend/js/api.js, change:
  const API = "http://127.0.0.1:8000";
To:
  const API = "https://your-render-app-name.onrender.com";

### Environment Notes
- Development: SQLite (automatic, no setup)
- Production: PostgreSQL (provisioned by Render automatically)
- Passwords: Always use environment variables, never hardcode

### Run Tests Locally
  PYTHONPATH=. pytest tests/ -v
