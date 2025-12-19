# 🧪 VOICEMEET_SUM - SYSTEM TEST GUIDE

## 📋 Mục đích

File test này giúp bạn kiểm tra toàn diện hệ thống Voicemeet_sum trước khi demo cho IT GOTTALENT 2025.

---

## 🚀 Cách Sử Dụng

### Chạy Test

```bash
# Windows
TEST_SYSTEM.bat

# Hoặc trực tiếp với Python (đã activate venv)
python TEST_SYSTEM.py
```

---

## 🔍 Test Checklist

Script sẽ kiểm tra **6 categories chính**:

### 1. Python Environment ✅
- [x] Python version (>= 3.9)
- [x] Virtual environment activated
- [x] Required packages installed:
  - faster-whisper
  - ollama
  - torch
  - fastapi
  - python-docx
  - numpy, requests, psutil

### 2. GPU & CUDA 🎮
- [x] PyTorch installed
- [x] CUDA availability
- [x] GPU device detected
- [x] VRAM capacity (>= 6GB recommended)
- [x] cuDNN available

### 3. External Tools 🔧
- [x] FFmpeg installed & in PATH
- [x] Ollama service running
- [x] Qwen 2.5 model installed

### 4. Project Structure 📁
- [x] Required directories exist:
  - `app/` - FastAPI backend
  - `src/` - Source code
  - `config/` - Configuration
  - `temp/` - Temporary files
  - `output/` - Output files
  - `logs/` - Log files
  - `models_cache/` - Model cache
- [x] Key files present

### 5. Disk Space 💾
- [x] Free space >= 10GB

### 6. API Health Check 🌐
- [x] API server running (optional)
- [x] All components ready

---

## 📊 Kết Quả Test

### Success Rate

- **>= 90%**: ✅ Hệ thống sẵn sàng cho demo
- **70-89%**: ⚠️ Cần điều chỉnh một số vấn đề
- **< 70%**: ❌ Chưa sẵn sàng, cần khắc phục

### Báo Cáo Chi Tiết

Sau khi chạy test, một file JSON report sẽ được tạo tại:

```
output/system_test_report.json
```

Report bao gồm:
- Timestamp
- System info
- Chi tiết tất cả checks
- Summary statistics

---

## 🔧 Khắc Phục Vấn Đề Thường Gặp

### ❌ Python Version < 3.9

```bash
# Download Python 3.10+ từ python.org
# Sau đó tạo lại venv
python -m venv venv
```

### ❌ Virtual Environment Not Activated

```bash
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### ❌ Missing Packages

```bash
# Cài đặt lại tất cả dependencies
pip install -r requirements.txt
pip install -r requirements_fastapi.txt
```

### ❌ CUDA Not Available

```bash
# Cài đặt PyTorch với CUDA 12.1 (RTX 30/40 series)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Hoặc CUDA 11.8 (RTX 20 series)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### ❌ FFmpeg Not Found

**Windows:**
1. Download từ https://ffmpeg.org/download.html
2. Giải nén vào `C:\ffmpeg`
3. Thêm `C:\ffmpeg\bin` vào PATH:
   - Settings → System → About → Advanced system settings
   - Environment Variables → System Variables → Path → Edit → New
   - Thêm: `C:\ffmpeg\bin`

**Hoặc sử dụng script:**
```bash
DEPLOYMENT\install_ffmpeg.bat
```

### ❌ Ollama Not Running

```bash
# Cài đặt Ollama từ https://ollama.ai/

# Khởi động service
ollama serve

# Pull Qwen model (trong terminal khác)
ollama pull qwen2.5:7b
```

### ❌ Qwen Model Not Installed

```bash
ollama pull qwen2.5:7b
```

### ❌ Low Disk Space

- Xóa file temp cũ: `temp/*`
- Xóa logs cũ: `logs/*`
- Xóa output cũ không cần: `output/*`

---

## 🎯 Pre-Demo Checklist

Trước khi demo cho IT GOTTALENT 2025, đảm bảo:

- [ ] Chạy `TEST_SYSTEM.bat` và có success rate >= 90%
- [ ] Test thử với 1 file audio mẫu
- [ ] Kiểm tra API health: http://localhost:8000/api/health
- [ ] Chuẩn bị file audio demo (~2-5 phút)
- [ ] Đọc lại các tài liệu trong `docs/`:
  - `competition_strategy.md`
  - `technical_deep_dive.md`
  - `qa_preparation.md`

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề không giải quyết được:

1. Kiểm tra file báo cáo: `output/system_test_report.json`
2. Xem logs: `logs/voicemeet_api.log`
3. Chạy các check scripts riêng:
   - `python DEPLOYMENT/check_config.py`
   - `python DEPLOYMENT/check_cuda_libs.py`
   - `python DEPLOYMENT/check_system.py`

---

## 🏆 Mục Tiêu

**100% components READY** = **DEMO SUCCESS** = **IT GOTTALENT 2025 WIN!** 🎉

Good luck! 🍀
