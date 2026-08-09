# WriteFlow

> **Write naturally. Post confidently.**

A full-stack AI-powered web application that generates posts that feel **natural, conversational, and personal** rather than generic AI slop. Built from scratch with React, Tailwind CSS, FastAPI, SQLite, and a modular LLM abstraction layer.

---

## Features

1. **Input Customization**: Enter topic/idea, select post type (Story, Listicle, Hot Take, How-To, etc.), tone of voice, personal experience, key points, and post length.
2. **Anti-AI Prompting**: Built-in prompts actively ban corporate buzzwords ("delve", "landscape", "tapestry", "transformative", "game-changer", "leverage", "ecosystem") and formulaic AI openings.
3. **1-Click Editorial Refinements**:
   - 🔄 **Fresh Rewrite**: Rephrase and restructure from scratch.
   - 🤝 **Make Personal**: Inject authentic first-person stories and lessons.
   - ✨ **Improve Hook**: Make the first 2 lines scroll-stopping.
   - ✂️ **Make Shorter**: Cut out 30-40% filler words while keeping the core message.
   - ⚡ **Remove Buzzwords**: Replace corporate jargon with plain, grounded language.
4. **Writing Style & Instructions**: Tell the AI how you want your post written (e.g. emoji count, hashtag count, sentence length, tone preferences).
5. **Modular LLM Integration**: Easily toggle between Groq (`llama-3.3-70b-versatile`), OpenAI, Gemini, or Mock Provider via `.env`.
6. **Live Preview Card**: Real-time rendering with word count, reading time estimation, and 1-click clipboard copy.

---

## Tech Stack

### Frontend
- **React 19** + **Vite**
- **Tailwind CSS v3** (Glassmorphism design system)
- **TanStack Query (React Query v5)**
- **Axios**
- **Lucide React** icons

### Backend
- **Python 3.13** + **FastAPI**
- **SQLAlchemy 2.0 (Async)** + **aiosqlite**
- **Pydantic v2** + **pydantic-settings**
- **Jinja2** Prompt Templates
- **Groq SDK** (`llama-3.3-70b-versatile`)

---

## Quick Start Guide

### 1. Backend Setup

```bash
# Navigate to project root
cd "e:\karan ka linkdin"

# Activate Python virtual environment
.\venv\Scripts\Activate.ps1

# Start FastAPI dev server
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --reload --port 8000
```

FastAPI Swagger API Documentation will be available at: http://localhost:8000/docs

### 2. Frontend Setup

```bash
# Navigate to frontend folder
cd "e:\karan ka linkdin\frontend"

# Start Vite dev server
npm run dev
```

Frontend application will be available at: http://localhost:5173

---

## Configuration (`.env`)

Backend `.env` file located at `backend/.env`:

```env
PROJECT_NAME="WriteFlow API"
ENVIRONMENT="development"
DEBUG=True

DATABASE_URL="sqlite+aiosqlite:///./linkedin_posts.db"

# LLM Provider Choice: "groq", "openai", "gemini", "mock"
LLM_PROVIDER="groq"

# API Keys
GROQ_API_KEY="your-groq-api-key"
OPENAI_API_KEY="your-openai-api-key"
GEMINI_API_KEY="your-gemini-api-key"
```

---

## Running Unit Tests

```bash
$env:PYTHONPATH="backend"
.\venv\Scripts\python.exe -m pytest backend/tests
```
