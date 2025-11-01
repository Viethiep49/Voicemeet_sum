# Meeting Transcription App - Project Structure (Production Ready)

## 📁 GitHub Repository Structure

```
meeting-transcription-app/
│
├── 📄 README.md                        # Setup instructions (Vietnamese)
├── 📄 README_EN.md                     # English version (for you)
├── 📄 LICENSE
├── 📄 .gitignore
│
├── 🚀 DEPLOYMENT/
│   ├── setup.bat                       # ONE-CLICK SETUP (Main entry)
│   ├── install_python.bat              # Auto-install Python 3.11
│   ├── install_ollama.bat              # Auto-install Ollama
│   ├── install_ffmpeg.bat              # Auto-install FFmpeg
│   ├── download_models.py              # Download Whisper + Qwen
│   ├── run_app.bat                     # Launch app after setup
│   ├── config.template.ini             # Default configuration
│   └── check_system.py                 # System requirements check
│
├── 📦 requirements.txt                 # Python dependencies
├── 📦 requirements-dev.txt             # Dev dependencies (testing, etc.)
│
├── ⚙️ config/
│   ├── __init__.py
│   └── settings.py                     # Configuration management
│
├── 💻 src/
│   ├── __init__.py
│   │
│   ├── transcription/
│   │   ├── __init__.py
│   │   ├── whisper_service.py          # Whisper transcription (optimized)
│   │   └── audio_processor.py          # FFmpeg preprocessing
│   │
│   ├── summarization/
│   │   ├── __init__.py
│   │   └── qwen_service.py             # Qwen summarization (local)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_handler.py             # File operations
│   │   ├── text_processor.py           # Text processing (chunking)
│   │   ├── logger.py                   # Logging utility
│   │   └── system_checker.py           # Check GPU, RAM, etc.
│   │
│   └── pipeline/
│       ├── __init__.py
│       └── meeting_pipeline.py         # Main orchestration
│
├── 🎨 app/
│   ├── __init__.py
│   ├── gui.py                          # Gradio GUI (main app)
│   └── themes.py                       # Custom Gradio theme
│
├── 🧪 tests/
│   ├── __init__.py
│   ├── test_transcription.py
│   ├── test_summarization.py
│   ├── test_pipeline.py
│   └── test_data/
│       └── sample_zoom_1min.m4a        # 1-min sample for quick test
│
├── 📚 docs/
│   ├── USER_GUIDE_VI.pdf               # User guide (Vietnamese)
│   ├── DEVELOPER_GUIDE.md              # Developer documentation
│   └── TROUBLESHOOTING.md              # Common issues & fixes
│
├── 🎨 assets/
│   ├── icon.ico                        # App icon
│   ├── logo.png                        # Logo
│   └── screenshots/                    # App screenshots
│
└── 📂 examples/
    ├── sample_meeting.m4a              # 5-min sample audio
    └── expected_output/
        ├── transcript_full.txt
        └── summary.txt
```

## 🚀 Deployment Files (Critical)

### 1. setup.bat (Main Entry Point)
```batch
@echo off
chcp 65001 > nul
echo ╔════════════════════════════════════════════════╗
echo ║   Meeting Transcription App - Setup          ║
echo ║   Cài đặt tự động - Vui lòng đợi...          ║
echo ╚════════════════════════════════════════════════╝
echo.

REM Check system requirements
echo [1/7] Kiểm tra hệ thống...
python deployment\check_system.py
if errorlevel 1 (
    echo ❌ Hệ thống không đủ yêu cầu. Xem log để biết chi tiết.
    pause
    exit /b 1
)

REM Install Python if needed
echo [2/7] Kiểm tra Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo Python chưa cài. Đang cài đặt...
    call deployment\install_python.bat
)

REM Create virtual environment
echo [3/7] Tạo môi trường ảo...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [4/7] Cài đặt thư viện Python...
pip install --upgrade pip
pip install -r requirements.txt

REM Install FFmpeg
echo [5/7] Cài đặt FFmpeg...
call deployment\install_ffmpeg.bat

REM Install Ollama
echo [6/7] Cài đặt Ollama...
call deployment\install_ollama.bat

REM Download models
echo [7/7] Tải models (có thể mất 5-10 phút)...
python deployment\download_models.py

REM Create desktop shortcut
echo.
echo ✅ Cài đặt hoàn tất!
echo.
echo Tạo shortcut trên Desktop...
REM [Code to create shortcut]

echo.
echo ═══════════════════════════════════════════════
echo  🎉 HOÀN TẤT! Nhấn phím bất kỳ để mở app
echo ═══════════════════════════════════════════════
pause
call run_app.bat
```

### 2. run_app.bat (Launch App)
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat

REM Start Ollama in background
start /B ollama serve > nul 2>&1

REM Wait for Ollama to start
timeout /t 3 /nobreak > nul

REM Launch app
echo Đang khởi động app...
python app\gui.py

pause
```

### 3. config.template.ini
```ini
[APP]
name = Meeting Transcription
version = 1.0.0
language = vi

[PATHS]
output_dir = ./output
models_cache = ./models
logs_dir = ./logs

[TRANSCRIPTION]
model = medium
device = cuda
compute_type = float16
language = vi
beam_size = 5
vad_filter = true

[SUMMARIZATION]
model = qwen2.5:7b
temperature = 0.3
max_tokens = 2000

[FFMPEG]
sample_rate = 16000
channels = 1
normalize = true
remove_silence = true

[PERFORMANCE]
max_audio_length = 7200  # 2 hours in seconds
chunk_size = 4000
num_workers = 4

[OUTPUT]
formats = txt
include_metadata = true
```

## 📝 README.md (Vietnamese)

```markdown
# Meeting Transcription App

Ứng dụng chuyển đổi audio cuộc họp thành văn bản và tóm tắt tự động.

## 🎯 Yêu cầu hệ thống

- Windows 10/11 (64-bit)
- RAM: 16GB trở lên
- GPU: NVIDIA RTX 3060 trở lên (khuyên dùng)
- Dung lượng trống: 20GB
- Internet: Để tải models lần đầu

## 🚀 Cài đặt (5-10 phút)

1. **Tải ứng dụng**
   - Nhấn nút "Code" màu xanh → "Download ZIP"
   - Giải nén vào thư mục bất kỳ

2. **Chạy cài đặt**
   - Double-click file `setup.bat`
   - Đợi chương trình tự động cài đặt
   - Nhấn phím bất kỳ khi hoàn tất

3. **Xong!**
   - Ứng dụng sẽ tự động mở
   - Hoặc double-click `run_app.bat` để chạy sau này

## 📖 Hướng dẫn sử dụng

1. Kéo thả file audio (Zoom recording) vào ô "Drop file here"
2. Nhấn nút "Bắt đầu"
3. Đợi 10-15 phút (cho file 2 giờ)
4. Tải về 2 file kết quả:
   - `transcript_full.txt`: Nội dung đầy đủ
   - `summary.txt`: Tóm tắt chính

## ❓ Gặp vấn đề?

Xem file `docs/TROUBLESHOOTING.md` hoặc liên hệ support.

## 📧 Liên hệ

Email: your-email@example.com
```

## 🎯 Key Features

### Automated Setup
- ✅ One-click installation
- ✅ Auto-detect and install missing dependencies
- ✅ Auto-download models (with progress bar)
- ✅ Create desktop shortcut
- ✅ Vietnamese UI throughout

### Optimized for Target System
- ✅ RTX 4070: float16 compute type
- ✅ Medium model: Speed priority
- ✅ 16GB RAM: Qwen 7B (safe)
- ✅ FFmpeg: Handle all Zoom formats

### User Experience
- ✅ Drag & drop interface
- ✅ Real-time progress tracking
- ✅ Auto-open output folder
- ✅ Error messages in Vietnamese
- ✅ Processing history (last 5)

### Reliability
- ✅ Auto-retry on failure
- ✅ Checkpoint saving (resume if crash)
- ✅ Detailed logging
- ✅ System requirements check

## 🔄 Workflow: From GitHub to Working App

```
┌─────────────────────────────────────────────────┐
│  Step 1: Developer (You)                        │
├─────────────────────────────────────────────────┤
│  1. Write code                                  │
│  2. Test locally                                │
│  3. Push to GitHub (private repo)               │
│  4. Create release v1.0.0                       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│  Step 2: TeamViewer to Brother's PC             │
├─────────────────────────────────────────────────┤
│  1. Open browser → GitHub repo                  │
│  2. Download ZIP → Extract to Desktop           │
│  3. Double-click setup.bat                      │
│     → Auto-install everything (10 min)          │
│  4. App opens automatically                     │
│  5. Test with sample file                       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│  Step 3: Daily Use                              │
├─────────────────────────────────────────────────┤
│  1. Double-click "Meeting App" on desktop       │
│  2. Drag & drop Zoom file                       │
│  3. Click "Bắt đầu"                             │
│  4. Get results in ~/Documents/MeetingApp/      │
└─────────────────────────────────────────────────┘
```

## 📊 File Size Estimates

```
Repository (for download):     ~5 MB
After setup (with models):     ~8 GB
  - Whisper medium:            ~1.5 GB
  - Qwen 7B:                   ~4.5 GB
  - Dependencies:              ~2 GB

Per processed audio:
  - 2h M4A file:               ~50 MB
  - Temp WAV:                  ~200 MB (auto-deleted)
  - Output TXT:                ~30-50 KB
```

## 🎯 Next Steps

Ready to start coding? I'll create the files in this order:

1. ✅ Setup scripts (setup.bat, etc.)
2. ✅ Config files (settings.py)
3. ✅ Core services (whisper, qwen, ffmpeg)
4. ✅ Pipeline orchestration
5. ✅ Gradio GUI
6. ✅ Testing
7. ✅ Documentation

Say "ready" and I'll start generating the actual code! 🚀