# PyScroll

PyScroll is a Python learning app built around the familiar rhythm of a content feed. It combines short, practical Python tips with an AI tutor and an in-browser playground, so users can discover a concept, ask a follow-up question, and run a small example without leaving the app.

## Features

- Scrollable feed of Python tips covering core language features and popular libraries
- Categories, favorites, reposts, comments, streaks, and achievements
- AI Python tutor with streamed responses and conversation history
- Browser playground for running Python snippets through the local backend
- Local persistence with IndexedDB for user activity, preferences, and chat history
- Dark and light themes

## Tech Stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, Framer Motion, Lucide
- **Backend:** FastAPI, Uvicorn, Pydantic
- **AI:** Groq API, configured through an environment variable
- **Storage:** IndexedDB in the browser

## Project Structure

```text
backend/
  main.py              FastAPI application and API routes
  requirements.txt     Python dependencies
  tips/                Static Python tip content
frontend/
  src/app/             Next.js pages and routes
  src/components/      Shared UI components
  src/lib/             API, IndexedDB, theme, and domain helpers
  public/              Static frontend assets
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Node.js 20 or newer and npm
- A Groq API key for AI tutor responses (optional)

### 1. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env` if you want to enable the AI tutor:

```env
GROQ_API_KEY=your_groq_api_key
# Optional; the backend defaults to this model.
GROQ_MODEL=openai/gpt-oss-20b
```

Run the API:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000). FastAPI's interactive docs are at [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

The frontend uses `http://localhost:8000` by default. To point it at another backend, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/tips` | Return the Python tip feed |
| `GET` | `/api/tips/{tip_id}` | Return one tip |
| `POST` | `/api/run` | Run a Python snippet locally and return its output |
| `POST` | `/api/chat` | Stream a Python tutor response as server-sent events |

## Development Commands

Run these from `frontend/`:

```bash
npm run dev       # Start the development server
npm run lint      # Run ESLint
npm run build     # Create a production build
npm run start     # Serve the production build
```

## Notes

- Feed content is currently stored as static data in `backend/tips/`.
- User activity and chat history are stored locally in the browser; there is no account or server-side user database.
- The playground executes submitted Python code in a temporary directory with an eight-second timeout. It is intended for local development and should be isolated and hardened before being exposed to untrusted users in production.