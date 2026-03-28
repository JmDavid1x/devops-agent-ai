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
| Database | SQLite (dev) / PostgreSQL (prod) |
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
- Python 3.11+
- (Optional) Docker & Docker Compose for containerized deployment

### Option 1: Local Development (Recommended for Development)

This is the easiest way to run the project locally without Docker. Uses SQLite for the database.

**1. Clone and Setup:**
```bash
git clone https://github.com/JmDavid1x/devops-ai-agent.git
cd devops-ai-agent
```

**2. Configure Environment:**
```bash
# Create .env file in backend directory with your API keys
cat > backend/.env << EOF
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
DATABASE_URL=sqlite:///devops_agent.db
DEBUG=true
EOF
```

**3. Backend (Terminal 1):**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**4. Frontend (Terminal 2):**
```bash
cd frontend
npm install  # Only needed first time
npm run dev
```

**5. Access the app:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Docker Deployment (Production)

```bash
# Clone the repository
git clone https://github.com/JmDavid1x/devops-ai-agent.git
cd devops-ai-agent

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys and PostgreSQL credentials

# Start all services (includes PostgreSQL, Redis)
docker-compose up -d
```

**Access the app:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

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

## Chat Examples

Try these commands in the Chat interface to interact with your DevOps infrastructure:

```
📦 Docker Management:
- "List my running containers"
- "What containers are running on staging?"
- "Restart the api-gateway container"

🔍 Monitoring:
- "Check the health of web-api"
- "What services are currently down?"
- "Give me a summary of all services"

📊 Logs & Analysis:
- "Analyze logs for the backend service"
- "What errors are in the production logs?"
- "Show me recent warnings in the database logs"

🚀 Deployments:
- "Deploy myapp:latest to staging"
- "Rollback the last deployment"
- "What's the status of ongoing deployments?"
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/chat` | Send message to AI agent |
| POST | `/api/chat/stream` | Stream chat response |
| GET | `/api/conversations/` | List all conversations |
| GET | `/api/conversations/{conversation_id}` | Get conversation details |
| DELETE | `/api/conversations/{conversation_id}` | Delete conversation |
| GET | `/api/services` | List monitored services |
| GET | `/api/services/{id}/health` | Check service health |
| GET | `/api/docker/containers` | List Docker containers |
| POST | `/api/docker/containers/{id}/restart` | Restart container |

## Environment Variables

### Required
- `OPENAI_API_KEY` or `CLAUDE_API_KEY` - API key for your chosen AI provider
- `AI_PROVIDER` - Set to `openai` or `claude` (default: `claude`)

### Optional (Development)
- `DATABASE_URL` - Database connection string (default: SQLite)
- `DEBUG` - Enable debug logging (default: `true`)

## Troubleshooting

**Port already in use:**
```bash
# Change port when running uvicorn
python -m uvicorn app.main:app --reload --port 8001

# Change port when running Next.js
npm run dev -- -p 3001
```

**Module not found errors:**
```bash
# Backend: reinstall dependencies
pip install -r requirements.txt

# Frontend: reinstall node modules
npm install
```

**Database locked (SQLite):**
- SQLite locks the database file when in use. Ensure only one backend process is running.

## Authors

This project was built by:

- **Jose David Mayor** (@JmDavid1x) - Full-stack development, architecture, and project lead
- **Claude** (AI Assistant by Anthropic) - AI implementation, bug fixes, documentation, and feature development

Special thanks to the open source community for the amazing tools and libraries used in this project.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
