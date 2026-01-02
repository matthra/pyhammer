# PyHammer 2.0

**Warhammer 40K Mathematical Analysis Tool** - Analyze army roster efficiency with cost-per-kill (CPK) metrics, time-to-kill (TTK) calculations, and interactive visualizations.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

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

Then open: **http://localhost:3000**

### Option 2: Local Development

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 3: Manual

**Backend (Terminal 1):**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm install
npm run dev
```

Then open: **http://localhost:3000**

---

## 📋 What's New in 2.0

PyHammer 2.0 is a **complete rewrite** with React + FastAPI:

| Feature | v1.0 (Streamlit) | v2.0 (React + FastAPI) |
|---------|------------------|------------------------|
| **Performance** | Slow with 50+ units | 10x faster |
| **Multi-user** | ❌ | ✅ |
| **Architecture** | Monolithic | Separated frontend/backend |
| **State Management** | Session-based | Persistent API |
| **Deployment** | Streamlit Cloud only | Self-hostable, Docker-ready |

**Your calculation engine is unchanged** - all 26 tests still pass!

---

## 📂 Project Structure

```
pyhammer/
├── backend/              # FastAPI REST API
│   ├── main.py          # API entry point
│   ├── models.py        # Request/response models
│   └── routers/         # API endpoints
├── frontend/            # React UI
│   └── src/
│       ├── pages/       # Dashboard, Roster, Analysis, Charts
│       ├── components/  # Reusable components
│       └── store/       # State management
├── src/                 # Original calculation engine (UNCHANGED)
│   ├── engine/          # Calculator, grading, math core
│   ├── data/            # Roster & target management
│   └── visualizations/  # Chart generation
├── roster_configs/      # Saved rosters (JSON)
├── target_configs/      # Target profiles (JSON)
└── docs/                # Documentation
```

---

## 🎮 Features

- **Roster Manager** - Build and edit army rosters
- **Target Profiles** - Define defensive profiles (MEQ, TEQ, Vehicles, etc.)
- **Efficiency Analysis** - CPK, TTK, Lethality metrics with S-F grading
- **Interactive Charts** - Threat matrices, efficiency curves, heatmaps
- **Keywords Support** - Blast, Melta, Rapid Fire, Lethal Hits, Dev Wounds, Twin-Linked, etc.
- **Global Settings** - Cover modifier, half-range bonuses
- **Import/Export** - Save/load rosters and target lists

---

## 📚 Documentation

- **[Installation Guide](docs/INSTALL.md)** - Detailed setup instructions
- **[Quick Start](docs/QUICKSTART.md)** - Quick reference
- **[Migration Guide](docs/README_MIGRATION.md)** - v1 to v2 migration details
- **[Migration Summary](docs/MIGRATION_SUMMARY.md)** - Complete file listing
- **[Feature Docs](docs/)** - Keyword implementations, grading system, etc.

---

## 🔧 Technology Stack

**Frontend:**
- React 18.2
- Vite (build tool)
- Zustand (state management)
- TanStack Query (data fetching)
- Plotly.js (charts)
- React Router (navigation)

**Backend:**
- FastAPI 0.128
- Uvicorn (ASGI server)
- Pydantic (validation)
- Pandas & NumPy (calculations)

**Deployment:**
- Docker & Docker Compose
- Self-hostable on any platform

---

## 🧪 Testing

All original tests still pass:
```bash
cd src
python -m pytest
```

---

## 🌐 Self-Hosting

Perfect for tournament venues or gaming clubs:

1. **Start with Docker:**
   ```bash
   ./docker-up.sh up -d
   # Or: docker-compose -f docker/docker-compose.yml up -d
   ```

2. **Find your local IP:**
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig`

3. **Share the URL:**
   ```
   http://YOUR_IP:3000
   ```

---

## 📊 API Documentation

When running, visit: **http://localhost:8000/docs** for auto-generated API documentation.

### Key Endpoints

- `POST /api/calculator/calculate` - Calculate metrics
- `GET /api/rosters/list` - List saved rosters
- `POST /api/rosters/save` - Save roster
- `GET /api/targets/list` - List target profiles
- `POST /api/visualizations/chart` - Generate charts

---

## 🎨 Customization

**Theme Colors:** Edit `frontend/src/index.css`

**Add Features:**
- Backend: Add routes in `backend/routers/`
- Frontend: Add components in `frontend/src/`

---

## 🤝 Legacy Streamlit Version

The original Streamlit app (`app.py`) is still available:
```bash
streamlit run app.py
```

Both versions can coexist!

---

## 📝 Version History

- **v2.0** (2024) - React + FastAPI rewrite
- **v1.0** (2024) - Original Streamlit version

---

## 🆘 Support

**Issues?** Check the troubleshooting section in [INSTALL.md](docs/INSTALL.md)

**Questions?** Review the [Quick Start Guide](docs/QUICKSTART.md)

---

## ⚙️ Requirements

- **Python:** 3.11+ (backend)
- **Node.js:** 18+ (frontend)
- **Docker:** Optional but recommended

---

## 📄 License

MIT License - See LICENSE file for details

---

**Ready?** Run `docker-compose up` and start analyzing! 🚀
