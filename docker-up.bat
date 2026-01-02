@echo off
REM Wrapper script to run docker-compose from root directory

cd /d "%~dp0"
docker-compose -f docker\docker-compose.yml %*
