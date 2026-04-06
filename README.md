# VoiceMeet Sum - Trợ Lý Họp Thông Minh AI 

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-enabled-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**VoiceMeet Sum** là hệ thống tự động hóa biên bản cuộc họp dành cho doanh nghiệp Việt Nam. Hệ thống sử dụng AI tiên tiến để chuyển đổi âm thanh thành văn bản và trích xuất thông tin quan trọng (quyết định, phân công nhiệm vụ) thành biên bản chuẩn format doanh nghiệp.

Ứng dụng chuyển đổi audio cuộc họp thành văn bản và tóm tắt tự động. Tối ưu cho cuộc họp **song ngữ Việt-Nhật** (marketing F&B tại Nhật Bản).

## ✨ Tính năng chính

- ✅ **Transcription**: Chuyển đổi audio sang văn bản với [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) (`large-v3-turbo` — nhanh ~3x, accuracy cao)
- ✅ **Summarization**: Tóm tắt tự động với [Gemma 4 E4B](https://ollama.com/library/gemma4) (140+ ngôn ngữ, native Việt-Nhật)
- ✅ **Bilingual**: Auto-detect ngôn ngữ — xử lý code-switching Việt ↔ Nhật trong cùng 1 audio
- ✅ **FFmpeg**: Xử lý audio preprocessing (normalize, resample, VAD)
- ✅ **GUI**: Giao diện web với Gradio
- ✅ **Rollback**: Quay về model cũ (Qwen 2.5 + Whisper small) qua `MODEL_PROFILE=legacy`

## 🏗️ Kiến Trúc Hệ Thống

Hệ thống được thiết kế theo mô hình Microservices-ready với pipeline xử lý dữ liệu song song:

```mermaid
graph TD
    A[Client UI/API] -->|Upload Audio| B(FastAPI Gateway)
    B -->|Task Queue| C{Job Manager}
    C -->|Progress Update| B
    
    subgraph "AI Processing Core"
        D[Audio Preprocessor] -->|Normalize 16kHz| E[Whisper Transcription]
        E -->|Raw Text| F[Text Chunker]
        F -->|Prompt Engineering| G[LLM Engine (Gemma 4 / Qwen 2.5)]
        G -->|Structured JSON| H[Template Engine]
    end
    
    C --> D
    H -->|Generate DOCX| I[Storage]
    I -->|Download| A
```

### Yêu cầu phần cứng

```yaml
OS: Windows 10/11 (64-bit) / macOS (Apple Silicon)
CPU: Intel i5 / Apple M1 trở lên
RAM: 16GB trở lên (Tối thiểu 8GB)
GPU: NVIDIA RTX 40-series (6GB+ VRAM) — khuyên dùng
Storage: 20GB trống
Internet: Cần kết nối để tải models lần đầu
```

## 🚀 Cài Đặt & Triển Khai

### Cách 1: Chạy Local (Dev Mode)

1. **Clone Repository**
   ```bash
   git clone https://github.com/Viethiep49/Voicemeet_sum.git
   cd Voicemeet_sum
   ```

2. **Cài Đặt Môi Trường**
   ```bash
   # Windows
   setup.bat
   
   # macOS/Linux
   ./quick_setup_mac.sh
   ```

3. **Cài đặt Ollama và Gemma 4**
   ```bash
   # Cài đặt Ollama
   # Tải từ https://ollama.ai/ hoặc chạy file bat
   DEPLOYMENT\install_ollama.bat

   # Download Gemma 4 (model mặc định)
   ollama pull gemma4:e4b
   ```

4. **Chạy Ứng Dụng**
   ```bash
   # Windows
   CHAY_APP.bat
   ```
   Truy cập: `http://localhost:8000`

### Cách 2: Triển Khai Docker

```bash
docker-compose up --build -d
```

## ⚙️ Cấu hình

### Model Profile (Rollback)

Chuyển đổi giữa model mới và cũ qua biến môi trường:

```bash
# Dùng model mới (mặc định): Whisper large-v3-turbo + Gemma 4 E4B
export MODEL_PROFILE=optimized

# Quay về model cũ: Whisper small + Qwen 2.5
export MODEL_PROFILE=legacy
```

### Cấu hình thủ công `config/settings.py`:

```python
# Whisper config
TRANSCRIPTION.model = "large-v3-turbo"  # hoặc "medium", "small"
TRANSCRIPTION.compute_type = "float16"   # float16 (GPU), int8 (CPU/Mac)
TRANSCRIPTION.language = None            # None = auto-detect, "vi", "ja"

# LLM config  
SUMMARIZATION.model = "gemma4:e4b"       # hoặc "gemma4:26b", "qwen2.5:7b"
SUMMARIZATION.temperature = 0.3          # 0.0 - 1.0
```

## 📊 Performance (RTX 4050, audio 2 giờ)

```
FFmpeg preprocessing:     30-60 sec
Whisper large-v3-turbo:   3-5 min   (↓ từ 6-8 min với medium)
Gemma 4 E4B summary:      1-2 min   (↓ từ 2-3 min với Qwen 2.5)
──────────────────────────────────────────
Total:                    5-8 min   (↓ ~40% so với trước)
Speed:                    15-24x realtime
```

### Resource Usage (optimized profile)

```
VRAM: ~5-6 GB total
  - Whisper large-v3-turbo: ~3 GB (float16)
  - Gemma 4 E4B: ~2-3 GB
RAM:  8-10 GB system
```

## 📝 License

MIT License. Copyright (c) 2025.

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.
