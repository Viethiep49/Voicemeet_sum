@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Change to project root
cd /d "%~dp0.."

echo.
echo ╔════════════════════════════════════════════════╗
echo ║   🎤 Voicemeet_sum - FastAPI Backend          ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Check if venv exists
if not exist "venv\" (
    echo [ERROR] Không tìm thấy virtual environment (venv)
    echo [INFO] Vui lòng chạy: python -m venv venv
    pause
    exit /b 1
)

:: Activate virtual environment
echo [INFO] Kích hoạt virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Không thể kích hoạt virtual environment
    pause
    exit /b 1
)

:: Check if Ollama is running
echo [INFO] Kiểm tra Ollama...
curl -s http://localhost:11434 > nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama chưa chạy. Đang khởi động Ollama...
    start /B ollama serve
    timeout /t 3 /nobreak > nul
    echo [INFO] Đã khởi động Ollama
) else (
    echo [OK] Ollama đang chạy
)

:: Create temp directory
if not exist "temp\" (
    echo [INFO] Tạo thư mục temp...
    mkdir temp
)

:: Display startup info
echo.
echo [INFO] Backend đang khởi động trên port 8000
echo [INFO] Mở trình duyệt và truy cập:
echo [INFO]   - http://127.0.0.1:8000
echo [INFO]   - http://127.0.0.1:8000/static/index.html
echo.
echo [INFO] Nhấn Ctrl+C để dừng server
echo.

:: Run FastAPI backend
python app\backend.py

:: On exit
echo.
echo [INFO] Server đã dừng
pause

