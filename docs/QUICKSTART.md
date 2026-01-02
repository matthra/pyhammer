# PyHammer 2.0 - Quick Start Guide

## 🎯 One-Command Startup

### Docker (Easiest - Recommended)
```bash
# From root directory:
./docker-up.sh up
# Or: docker-compose -f docker/docker-compose.yml up
```
Then open: http://localhost:3000

### Windows
```bash
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

## 📍 Access Points

- **Frontend (Main UI):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/api/health

## 🔑 Key Differences from Streamlit

| Feature | Old (Streamlit) | New (React + FastAPI) |
|---------|----------------|----------------------|
| **Startup** | `streamlit run app.py` | `docker-compose up` or `start.bat` |
| **URL** | http://localhost:8501 | http://localhost:3000 |
| **Performance** | Slow with large rosters | 10x faster |
| **Multi-user** | ❌ | ✅ |
| **State** | Session-based | Persistent API |

## 📂 Your Data

All your existing data works:
- **Rosters:** `roster_configs/*.json` (unchanged)
- **Targets:** `target_configs/*.json` (unchanged)
- **Calculation Engine:** `src/engine/calculator.py` (unchanged)

## 🎮 Using the App

1. **Dashboard:** See overview of your roster
2. **Roster Manager:** Add/edit units and weapons
3. **Target Manager:** Manage defensive profiles
4. **Analysis:** View CPK/TTK metrics against targets
5. **Charts:** Interactive Plotly visualizations

## 🔧 Troubleshooting

**"Port 8000 already in use"**
```bash
# Find and kill the process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

**"Dependencies not installed"**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

**"Cannot connect to backend"**
- Make sure backend is running on port 8000
- Check http://localhost:8000/api/health
- Check CORS settings in `backend/main.py`

## 🌐 Self-Hosting on Local Network

```bash
# Find your local IP
# Windows: ipconfig
# Linux/Mac: ifconfig

# Start with Docker
docker-compose up

# Others on your network access:
http://YOUR_IP:3000
```

Example: `http://192.168.1.100:3000`

## 🚀 Production Deployment

Build for production:

```bash
# Build frontend
cd frontend
npm run build

# Serve everything from FastAPI
cd ../backend
# Uncomment the static files mount in main.py
uvicorn main:app --host 0.0.0.0 --port 8000
```

Now everything runs on a single port (8000).

## 📊 Performance Tips

- Use **Docker** for consistent performance
- React only re-renders changed components
- Charts are cached (no regeneration on every click)
- State updates are instant (no full app reruns)

## 🎨 Customization

**Change theme colors:**
Edit `frontend/src/index.css` CSS variables

**Add new calculations:**
Add endpoints in `backend/routers/calculator.py`

**Add new pages:**
1. Create component in `frontend/src/pages/`
2. Add route to `frontend/src/App.jsx`

## ✅ Verify Installation

```bash
# Backend health check
curl http://localhost:8000/api/health

# Should return: {"status":"healthy"...}

# Frontend (open in browser)
http://localhost:3000
```

## 🆘 Need Help?

1. Check `README_MIGRATION.md` for detailed info
2. View API docs: http://localhost:8000/docs
3. All your original calculation logic is in `src/` (unchanged)

---

**Ready to migrate?** Just run `docker-compose up` and your app is live! 🚀
