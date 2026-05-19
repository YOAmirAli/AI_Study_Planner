# Deployment Guide

## Quick fix checklist (Render / static hosting)

1. **Backend** (`ai-study-planner-api` on Render)
   - Set `DATABASE_URL` (Neon PostgreSQL connection string)
   - Set `OPENAI_API_KEY` **or** `GEMINI_API_KEY` (required for summarize, quiz, tutor)
   - Set `CORS_ORIGINS` to your frontend URL, e.g. `https://ai-study-planner-frontend.onrender.com`
   - Start command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

2. **Frontend** (static site on Render, Vercel, or Netlify)
   - Set `VITE_API_URL` to your backend URL, e.g. `https://ai-study-planner-api.onrender.com`
   - Rebuild after changing env vars (Vite bakes env at build time)

3. **Verify**
   - Open `https://YOUR-BACKEND.onrender.com/api/health` — should return `{"status":"ok"}`
   - Log in on the frontend, then test Courses and AI Summarizer

## Local development

```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
# copy .env.example to .env and fill in values
python run.py

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

Backend runs on port **10000** by default. Vite proxies `/api` to that port.

## One-click Render deploy

Connect this repo on [Render](https://render.com) and use the `render.yaml` blueprint, then add `DATABASE_URL` and an AI API key in the dashboard.
