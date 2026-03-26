# DevOps AI Agent

An AI-powered dashboard for automating DevOps tasks through natural language. Analyze logs, monitor services, manage Docker containers, and automate deployments — all through conversation with an intelligent agent.

## Architecture

```
┌─────────────────────────────────────┐
│         Next.js Frontend            │
│  (Dashboard + Chat + Monitoring)    │
└──────────────┬──────────────────────┘
               │ REST / WebSocket
┌──────────────▼──────────────────────┐
│         FastAPI Backend             │
│  ┌─────────────────────────────┐    │
│  │     AI Agent Core           │    │
│  │  ┌───────┐  ┌───────────┐  │    │
│  │  │Claude │  │  OpenAI   │  │    │
│  │  │Adapter│  │  Adapter  │  │    │
│  │  └───────┘  └───────────┘  │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │     Tool System             │    │
│  │  • Log Analyzer             │    │
│  │  • Health Checker           │    │
│  │  • Docker Manager           │    │
│  │  • Deployment Runner        │    │
│  └─────────────────────────────┘    │
└──┬───────────┬──────────────────────┘
   │           │
┌──▼──┐  ┌────▼────┐  ┌──────────┐
│ PG  │  │  Redis  │  │  Docker  │
│ DB  │  │ +Celery │  │  Engine  │
└─────┘  └─────────┘  └──────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 + React + Tailwind CSS + shadcn/ui |
| Backend | Python + FastAPI |
| AI | Multi-provider: Claude API + OpenAI API |
| Database | PostgreSQL |
| Task Queue | Redis + Celery |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |

## Features

- **AI Chat Agent** — Interact with your infrastructure through natural language
- **Log Analysis** — Upload and analyze server/container logs with AI-powered insights
- **Health Monitoring** — Automated service health checks with intelligent alerting
- **Docker Management** — List, monitor, restart, and scale containers
- **Automated Deployments** — AI-assisted deploy, rollback, and post-deploy verification

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.12+
- Docker & Docker Compose

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/JmDavid1x/devops-ai-agent.git
cd devops-ai-agent

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Infrastructure (DB + Redis):**
```bash
docker-compose -f docker-compose.dev.yml up db redis -d
```

## Project Structure

```
devops-ai-agent/
├── frontend/                # Next.js application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   └── lib/             # Utilities & API client
│   └── Dockerfile
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/             # REST endpoints
│   │   ├── core/            # Config & AI providers
│   │   ├── agents/          # Agent tools & logic
│   │   ├── models/          # Pydantic schemas
│   │   └── services/        # Business logic
│   └── Dockerfile
├── docker-compose.yml       # Production compose
├── docker-compose.dev.yml   # Development compose
└── .github/workflows/       # CI/CD pipeline
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/chat` | Send message to AI agent |
| GET | `/api/services` | List monitored services |
| GET | `/api/services/{id}/health` | Check service health |
| GET | `/api/docker/containers` | List Docker containers |
| POST | `/api/docker/containers/{id}/restart` | Restart container |

## License

MIT
