@echo off
title Noor Zaman Portfolio Server
cd /d "%~dp0"

echo ===================================================
echo   Starting Noor Zaman Portfolio Web Server
echo ===================================================
echo.

echo [1/3] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in your PATH!
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b
)

echo.
echo [2/3] Installing/verifying dependencies...
python -m pip install -r requirements.txt

echo.
echo [3/3] Seeding database...
python seed_db.py

echo.
echo ===================================================
echo   SERVER STARTING at http://localhost:5000
echo   Admin Panel: http://localhost:5000/auth/login
echo ===================================================
echo.

python run.py

pause
