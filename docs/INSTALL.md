# PyHammer 2.0 - Installation Guide

## Quick Install

### Method 1: Docker (Recommended - Easiest)

**Prerequisites:** Docker installed

```bash
# One command to start everything
docker-compose up
```

Open http://localhost:3000

**That's it!** Docker handles all dependencies automatically.

---

### Method 2: Local Development

**Prerequisites:**
- Python 3.11+
- Node.js 18+

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

---

### Method 3: Manual Setup

**Step 1: Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Step 2: Install Frontend Dependencies**
```bash
cd frontend
npm install
```

**Step 3: Start Backend** (Terminal 1)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Step 4: Start Frontend** (Terminal 2)
```bash
cd frontend
npm run dev
```

**Step 5: Open Browser**
```
http://localhost:3000
```

---

## Verify Installation

### Check Backend
```bash
curl http://localhost:8000/api/health
```
Should return: `{"status":"healthy"...}`

### Check Frontend
Open browser: http://localhost:3000

### Check API Docs
Open browser: http://localhost:8000/docs

---

## Troubleshooting

### "Port 8000 already in use"

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

### "Module not found" errors

**Backend:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "Cannot connect to backend"

1. Make sure backend is running on port 8000
2. Check: http://localhost:8000/api/health
3. Check CORS settings in `backend/main.py`

---

## Next Steps

After installation:

1. **Load existing data:** Your rosters in `roster_configs/` will be available
2. **Try the features:** Navigate through Dashboard, Roster Manager, Analysis, Charts
3. **Read the docs:** Check `README_MIGRATION.md` for detailed information

---

## Self-Hosting on LAN

To share on your local network:

1. Find your local IP address:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig`

2. Start the app (Docker or manual)

3. Other devices access: `http://YOUR_IP:3000`
   - Example: `http://192.168.1.100:3000`

---

## Production Build

For deployment without dev servers:

```bash
# Build frontend
cd frontend
npm run build

# This creates: frontend/build/

# Serve from FastAPI (uncomment lines in backend/main.py)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

Now everything runs on port 8000 only.

---

## System Requirements

**Minimum:**
- 2 GB RAM
- 500 MB disk space
- Any modern browser (Chrome, Firefox, Edge, Safari)

**Recommended:**
- 4 GB RAM
- 1 GB disk space
- Chrome or Firefox (for best performance)

---

## Getting Help

- **Quick Reference:** See `QUICKSTART.md`
- **Migration Guide:** See `README_MIGRATION.md`
- **API Docs:** http://localhost:8000/docs (when running)

---

**Ready?** Run `docker-compose up` and you're live! 🚀
