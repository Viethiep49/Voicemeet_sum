@echo off
echo ═══════════════════════════════════════════════
echo   Cài đặt FFmpeg
echo ═══════════════════════════════════════════════
echo.

REM Try winget first
echo Đang cài đặt FFmpeg qua winget...
winget install --id=Gyan.FFmpeg -e
if errorlevel 1 (
    echo.
    echo ⚠️  winget không khả dụng
    echo.
    echo Vui lòng cài đặt FFmpeg thủ công:
    echo 1. Tải từ: https://ffmpeg.org/download.html
    echo 2. Giải nén và thêm vào PATH
)

pause

