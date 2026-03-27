# Local Development Setup

## Quick Start (Recommended for Windows)

Due to Docker Desktop memory constraints on Windows, this setup runs services in Docker and the frontend locally:

### 1. Start Backend Services

```bash
# Terminal 1: Start database, Redis, Prometheus, Grafana, and backend API
docker compose -f docker-compose.services.yml up
```

Wait for all services to be healthy (you'll see "backend" ready at `http://localhost:8000`).

### 2. Start Frontend (Separate Terminal)

```bash
# Terminal 2: Navigate to frontend and start dev server
cd frontend
npm install  # if needed
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 3. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Register/Login |
| Backend API | http://localhost:8000 | API Key or JWT token |
| Grafana | http://localhost:3001 | admin / admin |
| Prometheus | http://localhost:9090 | - |
| PostgreSQL | localhost:5432 | postgres / postgres |
| Redis | localhost:6379 | - |

## Full Docker Setup (Production)

If you have enough Docker Desktop memory (8GB+ allocated), use:

```bash
docker compose up
```

This builds and runs all services in containers.

## Environment Variables

Create a `.env` file in the root directory:

```bash
CLAUDE_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-openai-api-key
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
API_KEY=your-api-key-optional
```

## Troubleshooting

### Frontend Build Issues in Docker
- Use the local development setup above
- Or increase Docker Desktop memory to 8GB+
- Or disable buildkit: `DOCKER_BUILDKIT=0 docker compose build frontend`

### Backend Connection Errors
- Ensure PostgreSQL is healthy: `docker compose -f docker-compose.services.yml logs db`
- Check Redis: `docker compose -f docker-compose.services.yml logs redis`

### Monitoring Not Working
- Ensure Prometheus scraping backend at `http://localhost:9090/targets`
- Grafana datasource should be auto-provisioned
- Check Grafana dashboards at `http://localhost:3001` (admin/admin)

## Features

✅ AI-powered chat with streaming responses
✅ Real Docker container management
✅ HTTP service health checks
✅ JWT authentication
✅ Rate limiting & API key auth
✅ Prometheus metrics + Grafana dashboards
✅ PostgreSQL persistence
