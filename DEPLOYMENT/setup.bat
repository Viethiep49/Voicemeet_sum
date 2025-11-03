@echo off
chcp 65001 > nul
echo ╔════════════════════════════════════════════════╗
echo ║   Voicemeet_sum - Setup                       ║
echo ║   Cài đặt tự động - Vui lòng đợi...          ║
echo ╚════════════════════════════════════════════════╝
echo.

cd /d "%~dp0.."

REM Check Python
echo [1/6] Kiểm tra Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt
    echo Vui lòng cài đặt Python 3.9+ từ https://www.python.org/
    pause
    exit /b 1
)
echo ✅ Python đã được cài đặt

REM Create virtual environment
echo [2/6] Tạo môi trường ảo...
if exist venv (
    echo Venv đã tồn tại, bỏ qua...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Không thể tạo venv
        pause
        exit /b 1
    )
)
echo ✅ Môi trường ảo sẵn sàng

REM Activate venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo [3/6] Cập nhật pip...
python -m pip install --upgrade pip --quiet
echo ✅ pip đã được cập nhật

REM Install dependencies
echo [4/6] Cài đặt thư viện Python...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Không thể cài đặt dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies đã được cài đặt
echo [5/7] Kiểm tra GPU...
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Không có')"
REM Check FFmpeg
echo [5/6] Kiểm tra FFmpeg...
ffmpeg -version > nul 2>&1
if errorlevel 1 (
    echo ⚠️  FFmpeg chưa được cài đặt
    echo Vui lòng cài đặt FFmpeg từ https://ffmpeg.org/
) else (
    echo ✅ FFmpeg đã được cài đặt
)

REM System check
echo [6/6] Kiểm tra hệ thống...
python DEPLOYMENT\check_system.py

echo.
echo ═══════════════════════════════════════════════
echo  🎉 CÀI ĐẶT HOÀN TẤT!
echo ═══════════════════════════════════════════════
echo.
echo Tiếp theo:
echo  1. Cài đặt Ollama từ https://ollama.ai/
echo  2. Chạy: ollama pull qwen2.5:7b
echo  3. Chạy: DEPLOYMENT\run_app.bat
echo.
pause

