@echo off
REM PyHammer Startup Script for Windows

echo Starting PyHammer...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.11+
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js 18+
    exit /b 1
)

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
call npm install
cd ..

REM Start backend
echo Starting FastAPI backend on port 8000...
start "PyHammer Backend" cmd /k "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting React frontend on port 3000...
cd frontend
npm run dev
