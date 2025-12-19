@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Change to project root
cd /d "%~dp0.."

:: Debug: Show current directory
REM echo [DEBUG] Current directory: %CD%

echo.
echo ╔════════════════════════════════════════════════╗
echo ║   Cài đặt PyTorch với CUDA                    ║
echo ║   Tự động kiểm tra GPU và cài đặt phù hợp     ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Check if venv exists
if not exist "venv\Scripts\python.exe" (
    if not exist ".\venv\Scripts\python.exe" (
        echo [ERROR] Không tìm thấy virtual environment (venv)
        echo [INFO] Current directory: %CD%
        echo [INFO] Vui lòng chạy: python -m venv venv
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo [INFO] Kích hoạt virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Không thể kích hoạt virtual environment
    pause
    exit /b 1
)

:: Check if any Python process is running (might be using PyTorch)
echo [INFO] Kiểm tra process Python đang chạy...
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if %errorlevel% == 0 (
    echo [WARNING] Phát hiện Python process đang chạy
    echo [WARNING] Vui lòng đóng server FastAPI và các Python process khác trước khi cài đặt
    echo.
    pause
)

:: Run Python script
echo [INFO] Đang chạy script kiểm tra và cài đặt...
echo.
python DEPLOYMENT\install_pytorch_cuda.py

if errorlevel 1 (
    echo.
    echo [ERROR] Cài đặt thất bại
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════
echo  ✅ HOÀN TẤT!
echo ═══════════════════════════════════════════════
echo.
pause

