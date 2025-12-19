@echo off
chcp 65001 > nul
color 0A

echo ========================================================================
echo    VOICEMEET_SUM - SYSTEM TEST CHECKLIST
echo    IT GOTTALENT 2025 - Pre-Demo System Check
echo ========================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment chưa được tạo!
    echo    Chạy SETUP.bat trước khi test
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Run test script
echo.
echo 🚀 Bắt đầu kiểm tra hệ thống...
echo.
python TEST_SYSTEM.py

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================================
    echo    ✅ TEST HOÀN THÀNH - HỆ THỐNG SẴN SÀNG!
    echo ========================================================================
) else (
    echo.
    echo ========================================================================
    echo    ⚠️  TEST PHÁT HIỆN VẤN ĐỀ
    echo    Xem báo cáo chi tiết ở trên và khắc phục
    echo ========================================================================
)

echo.
echo 📝 Báo cáo chi tiết: output\system_test_report.json
echo.
pause
