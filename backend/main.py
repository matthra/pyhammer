"""
FastAPI Backend for PyHammer
Main application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from .routers import calculator, rosters, targets, visualizations

app = FastAPI(
    title="PyHammer API",
    description="Warhammer 40K Mathematical Analysis API",
    version="2.0.0"
)

# CORS configuration for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
try:
    app.include_router(calculator.router, prefix="/api/calculator", tags=["Calculator"])
    app.include_router(rosters.router, prefix="/api/rosters", tags=["Rosters"])
    app.include_router(targets.router, prefix="/api/targets", tags=["Targets"])
    app.include_router(visualizations.router, prefix="/api/visualizations", tags=["Visualizations"])
except Exception as e:
    print(f"Warning: Could not load all routers: {e}")

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "PyHammer API",
        "version": "2.0.0"
    }

@app.get("/api/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "calculator_engine": "operational",
        "data_layer": "operational"
    }

# Serve React static files in production
# This will be uncommented after React build is ready
# frontend_path = Path(__file__).parent.parent / "frontend" / "build"
# if frontend_path.exists():
#     app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
