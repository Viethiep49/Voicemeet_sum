@echo off
chcp 65001 > nul
title Voicemeet_sum - Setup Tu Dong
setlocal enabledelayedexpansion

:: Change to script directory
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🎤 Voicemeet_sum - Setup Tu Dong                        ║
echo ║     Chuyen doi audio thanh van ban va tom tat tu dong      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Bat dau setup tu dong...
echo [INFO] Qua trinh nay co the mat 10-15 phut
echo.
pause

:: ============================================
:: BUOC 1: KIEM TRA PYTHON
:: ============================================
echo.
echo ═══════════════════════════════════════════════
echo [1/6] Kiem tra Python...
echo ═══════════════════════════════════════════════
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo.
    echo [HUONG DAN] Vui long cai dat Python 3.11+:
    echo   1. Truy cap: https://www.python.org/downloads/
    echo   2. Tai Python 3.11 hoac 3.12 (64-bit)
    echo   3. Khi cai dat, NHO TICK vao "Add Python to PATH"
    echo   4. Sau do chay lai file SETUP.bat nay
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python da duoc cai dat
echo.

:: ============================================
:: BUOC 2: TAO VIRTUAL ENVIRONMENT
:: ============================================
echo ═══════════════════════════════════════════════
echo [2/6] Tao moi truong ao (venv)...
echo ═══════════════════════════════════════════════
if exist venv (
    echo [INFO] Venv da ton tai, bo qua...
) else (
    echo [INFO] Dang tao venv (mat 1-2 phut)...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Khong the tao venv
        pause
        exit /b 1
    )
)
echo [OK] Moi truong ao san sang
echo.

:: ============================================
:: BUOC 3: CAI DAT DEPENDENCIES
:: ============================================
echo ═══════════════════════════════════════════════
echo [3/6] Cai dat thu vien Python...
echo ═══════════════════════════════════════════════
echo [INFO] Qua trinh nay co the mat 5-10 phut...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements_fastapi.txt --quiet
if errorlevel 1 (
    echo [ERROR] Khong the cai dat dependencies
    echo [INFO] Vui long kiem tra ket noi internet
    pause
    exit /b 1
)
echo [OK] Dependencies da duoc cai dat
echo.

:: ============================================
:: BUOC 4: CAI DAT PYTORCH CUDA (TU DONG)
:: ============================================
echo ═══════════════════════════════════════════════
echo [4/6] Kiem tra va cai dat PyTorch CUDA...
echo ═══════════════════════════════════════════════
echo [INFO] Dang kiem tra GPU...
python DEPLOYMENT\install_pytorch_cuda.py
if errorlevel 1 (
    echo [WARNING] Co the co loi khi cai PyTorch, nhung co the tiep tuc
)
echo.

:: ============================================
:: BUOC 5: KIEM TRA FFMPEG
:: ============================================
echo ═══════════════════════════════════════════════
echo [5/6] Kiem tra FFmpeg...
echo ═══════════════════════════════════════════════
ffmpeg -version > nul 2>&1
if errorlevel 1 (
    echo [WARNING] FFmpeg chua duoc cai dat
    echo [INFO] Dang thu cai dat FFmpeg...
    call DEPLOYMENT\install_ffmpeg.bat
    echo [INFO] Neu khong cai duoc, ban co the cai thu cong:
    echo        https://ffmpeg.org/download.html
) else (
    echo [OK] FFmpeg da duoc cai dat
)
echo.

:: ============================================
:: BUOC 6: KIEM TRA OLLAMA
:: ============================================
echo ═══════════════════════════════════════════════
echo [6/6] Kiem tra Ollama...
echo ═══════════════════════════════════════════════
ollama --version > nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama chua duoc cai dat
    echo [INFO] Dang thu cai dat Ollama...
    call DEPLOYMENT\install_ollama.bat
    echo.
    echo [INFO] Sau khi cai Ollama, chay lenh sau de tai model:
    echo        ollama pull qwen2.5:7b
) else (
    echo [OK] Ollama da duoc cai dat
    echo [INFO] Dang kiem tra model Qwen...
    ollama list | findstr qwen2.5:7b > nul
    if errorlevel 1 (
        echo [INFO] Model chua duoc tai, dang tai model (mat 10-15 phut)...
        echo [INFO] Model size: ~4.7GB, can ket noi internet on dinh
        ollama pull qwen2.5:7b
    ) else (
        echo [OK] Model Qwen da duoc cai dat
    )
)
echo.

:: ============================================
:: HOAN TAT
:: ============================================
echo.
echo ═══════════════════════════════════════════════
echo  ✅ SETUP HOAN TAT!
echo ═══════════════════════════════════════════════
echo.
echo [INFO] De chay ung dung:
echo   1. Chay file: DEPLOYMENT\run_fastapi.bat
echo   2. Mo trinh duyet: http://127.0.0.1:8000/static/index.html
echo.
echo [INFO] Hoac chay truc tiep: DEPLOYMENT\run_fastapi.bat
echo.
pause

