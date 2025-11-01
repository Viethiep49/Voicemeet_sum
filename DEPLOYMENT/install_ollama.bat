@echo off
echo ═══════════════════════════════════════════════
echo   Cài đặt Ollama
echo ═══════════════════════════════════════════════
echo.

REM Try winget first
echo Đang cài đặt Ollama qua winget...
winget install --id=Ollama.Ollama -e
if errorlevel 1 (
    echo.
    echo ⚠️  winget không khả dụng
    echo.
    echo Vui lòng cài đặt Ollama thủ công:
    echo 1. Tải từ: https://ollama.ai/download
    echo 2. Chạy installer
    echo 3. Sau khi cài xong, chạy: ollama pull qwen2.5:7b
)

pause

