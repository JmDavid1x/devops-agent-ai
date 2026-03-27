# Quick Start Guide

## 1️⃣ Run Services Only (Recommended for Windows)

```bash
docker compose -f docker-compose.services.yml up
```

Wait for "backend" to be ready. See all services:
- Backend: http://localhost:8000
- Grafana: http://localhost:3001 (admin/admin)
- Prometheus: http://localhost:9090

## 2️⃣ Run Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## 3️⃣ Test It

### Register & Login
1. Go to http://localhost:3000/register
2. Create account: email, username, password
3. Login at http://localhost:3000/login
4. Dashboard loads! 🎉

### Try Features
- **Chat**: Send message to AI in /chat
- **Docker**: Manage containers in /docker
- **Services**: Add health checks in /services
- **Monitoring**: View metrics in /monitoring

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| API not responding | Wait 30s for DB to be ready, check: `docker compose -f docker-compose.services.yml logs backend` |
| Frontend won't start | `cd frontend && npm install` then `npm run dev` |
| Port already in use | Kill existing process or change port in docker-compose |
| Can't login | Check backend logs, ensure DB is healthy |

## 🚀 Full Docker Deployment

If Docker Desktop has 8GB+ memory:

```bash
docker compose up
```

All services in containers (takes ~2 min to start).

## 📚 Full Documentation

- **Local Setup**: `LOCAL_SETUP.md`
- **Implementation Details**: `IMPLEMENTATION_COMPLETE.md`
- **Backend**: `backend/README.md`
- **Frontend**: `frontend/README.md`

## Environment Variables

Create `.env` file:

```env
CLAUDE_API_KEY=your-key
OPENAI_API_KEY=your-key
JWT_SECRET_KEY=change-me
```

Or leave blank for mock mode.

---

**That's it!** You now have a full-featured DevOps AI Agent running locally. 🚀
