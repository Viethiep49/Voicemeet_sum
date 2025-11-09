@echo off
chcp 65001 > nul
title Voicemeet_sum

cd /d "%~dp0.."

REM Check if venv exists
if not exist venv (
    echo ❌ Virtual environment chưa được tạo
    echo Vui lòng chạy DEPLOYMENT\setup.bat trước
    pause
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check Ollama
echo Đang kiểm tra Ollama...
curl -s http://localhost:11434 > nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama không chạy. Đang khởi động...
    start /B ollama serve
    timeout /t 5 /nobreak > nul
)

REM Launch app
echo.
echo ╔════════════════════════════════════════════════╗
echo ║   🎤 Voicemeet_sum - Starting...              ║
echo ╚════════════════════════════════════════════════╝
echo.

REM Launch app (stderr redirected to suppress cuDNN warnings)
python app\gui.py 2>nul
if errorlevel 1 (
    echo.
    echo App co the bi loi. Xem logs trong thu muc logs\
    echo Hoac chay: python test_crash.py de xem chi tiet
    pause
)

echo.
echo App đã đóng. Nhấn phím bất kỳ để thoát...
pause > nul

