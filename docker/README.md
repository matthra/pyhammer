# Docker Configuration

This folder contains all Docker-related files for PyHammer.

## Files

- **docker-compose.yml** - Main orchestration file for multi-container setup
- **Dockerfile.backend** - Backend (FastAPI) container definition
- **Dockerfile.frontend** - Frontend (React/Vite) container definition
- **.dockerignore** - Files to exclude from Docker builds

## Quick Start

### From Root Directory

**Linux/Mac:**
```bash
./docker-up.sh up
```

**Windows:**
```bash
docker-up.bat
```

**Or manually:**
```bash
docker-compose -f docker/docker-compose.yml up
```

### From This Directory

```bash
cd docker
docker-compose up
```

## Common Commands

**Start services:**
```bash
docker-compose -f docker/docker-compose.yml up
```

**Start in background:**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

**Stop services:**
```bash
docker-compose -f docker/docker-compose.yml down
```

**View logs:**
```bash
docker-compose -f docker/docker-compose.yml logs -f
```

**Rebuild containers:**
```bash
docker-compose -f docker/docker-compose.yml build --no-cache
```

**Restart services:**
```bash
docker-compose -f docker/docker-compose.yml restart
```

## Service URLs

When running:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Volumes

The Docker setup mounts these directories for live development:
- `../src` → Backend calculation engine (live reload)
- `../frontend/src` → Frontend source code (hot reload)
- `../roster_configs` → Saved rosters (persisted)
- `../target_configs` → Target profiles (persisted)

## Production Deployment

For production, build optimized images:

```bash
# Build production frontend
cd ../frontend
npm run build

# Update docker-compose.yml to use production builds
# Then run:
docker-compose -f docker/docker-compose.yml up -d
```

## Troubleshooting

**Port already in use:**
```bash
# Change ports in docker-compose.yml
# Backend: "8001:8000" instead of "8000:8000"
# Frontend: "3001:3000" instead of "3000:3000"
```

**Containers won't start:**
```bash
# Check logs
docker-compose -f docker/docker-compose.yml logs

# Rebuild from scratch
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up
```

**Changes not reflecting:**
```bash
# Restart specific service
docker-compose -f docker/docker-compose.yml restart backend
docker-compose -f docker/docker-compose.yml restart frontend
```

## Network

All services run on the `pyhammer-network` Docker network, allowing inter-container communication.

## For Development

The current setup is optimized for development with:
- Hot reload for both frontend and backend
- Volume mounts for live code changes
- Debug-friendly logging

For production deployment, consider:
- Multi-stage Docker builds
- Production-optimized images
- Environment-specific configs
- Secrets management
