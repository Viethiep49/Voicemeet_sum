@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════╗
echo ║   Restart Voicemeet_sum Server                ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Change to project root
cd /d "%~dp0.."

:: Step 1: Stop existing server
echo [1/3] Dang dung server hien tai...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Voicemeet*" >nul 2>&1
Get-Process python* -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*Voicemeet_sum*" } | Stop-Process -Force -ErrorAction SilentlyContinue 2>nul

:: Check port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo [INFO] Dang dung process tren port 8000: PID %%a
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul
echo [OK] Da dung server
echo.

:: Step 2: Check venv
echo [2/3] Kiem tra virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment khong tim thay
    echo [INFO] Vui long chay: DEPLOYMENT\setup.bat
    pause
    exit /b 1
)
echo [OK] Virtual environment san sang
echo.

:: Step 3: Start server
echo [3/3] Khoi dong lai server...
echo.
call venv\Scripts\activate.bat

:: Check Ollama
curl -s http://localhost:11434 > nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama chua chay. Dang khoi dong...
    start /B ollama serve
    timeout /t 3 /nobreak > nul
)

echo.
echo ═══════════════════════════════════════════════
echo  Server dang khoi dong...
echo ═══════════════════════════════════════════════
echo.
echo [INFO] Backend dang khoi dong tren port 8000
echo [INFO] Mo trinh duyet va truy cap:
echo [INFO]   - http://127.0.0.1:8000
echo [INFO]   - http://127.0.0.1:8000/static/index.html
echo.
echo [INFO] Nhan Ctrl+C de dung server
echo.

:: Run server
python app\backend.py

:: On exit
echo.
echo [INFO] Server da dung
pause

