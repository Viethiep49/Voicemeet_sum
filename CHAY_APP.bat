@echo off
chcp 65001 > nul
title Voicemeet_sum - Chay Ung Dung
setlocal enabledelayedexpansion

:: Change to script directory
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🎤 Voicemeet_sum - Chay Ung Dung                        ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check if setup has been done
if not exist "venv\Scripts\python.exe" (
    echo [WARNING] Chua thay setup!
    echo [INFO] Dang chay setup tu dong...
    echo.
    call SETUP.bat
    if errorlevel 1 (
        echo [ERROR] Setup that bai!
        pause
        exit /b 1
    )
    echo.
    echo [INFO] Setup hoan tat, dang khoi dong app...
    echo.
)

:: Activate venv
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Khong the kich hoat venv
    echo [INFO] Vui long chay SETUP.bat truoc
    pause
    exit /b 1
)

:: Check Ollama
echo [INFO] Kiem tra Ollama...
curl -s http://localhost:11434 > nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama chua chay. Dang khoi dong...
    start /B ollama serve
    timeout /t 5 /nobreak > nul
    echo [OK] Ollama da khoi dong
) else (
    echo [OK] Ollama dang chay
)

:: Create temp directory
if not exist "temp\" mkdir temp

:: Display info
echo.
echo ═══════════════════════════════════════════════
echo  🚀 DANG KHOI DONG SERVER...
echo ═══════════════════════════════════════════════
echo.
echo [INFO] Server se chay tren: http://127.0.0.1:8000
echo [INFO] Trinh duyet se tu dong mo sau 5 giay...
echo.
echo [INFO] Neu trinh duyet khong tu dong mo:
echo        Vao: http://127.0.0.1:8000/static/index.html
echo.
echo [INFO] Nhan Ctrl+C de dung server
echo.

:: Wait a bit then open browser
start /B timeout /t 5 /nobreak > nul && start http://127.0.0.1:8000/static/index.html

:: Run server
python app\backend.py

:: On exit
echo.
echo [INFO] Server da dung
pause

