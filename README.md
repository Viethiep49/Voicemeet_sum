# 🎤 Voicemeet_sum

Ứng dụng chuyển đổi audio cuộc họp thành văn bản và tóm tắt tự động.
Tối ưu cho cuộc họp **song ngữ Việt-Nhật** (marketing F&B tại Nhật Bản).

## 🎯 Tính năng

- ✅ **Transcription**: Chuyển đổi audio sang văn bản với [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) (`large-v3-turbo` — nhanh ~3x, accuracy cao)
- ✅ **Summarization**: Tóm tắt tự động với [Gemma 4 E4B](https://ollama.com/library/gemma4) (140+ ngôn ngữ, native Việt-Nhật)
- ✅ **Bilingual**: Auto-detect ngôn ngữ — xử lý code-switching Việt ↔ Nhật trong cùng 1 audio
- ✅ **FFmpeg**: Xử lý audio preprocessing (normalize, resample, VAD)
- ✅ **GUI**: Giao diện web với Gradio
- ✅ **Rollback**: Quay về model cũ (Qwen 2.5 + Whisper small) qua `MODEL_PROFILE=legacy`

## 🎯 Yêu cầu hệ thống

```yaml
OS: Windows 10/11 (64-bit) / macOS (Apple Silicon)
CPU: Intel i5 / Apple M1 trở lên
RAM: 16GB trở lên
GPU: NVIDIA RTX 40-series (6GB+ VRAM) — khuyên dùng
Storage: 20GB trống
Internet: Cần kết nối để tải models lần đầu
```

## 🚀 Cài đặt

### Cách 1: Automated Setup (Khuyên dùng)

1. **Clone repository**
   ```bash
   git clone https://github.com/your-username/voicemeet_sum.git
   cd voicemeet_sum
   ```

2. **Chạy setup script**
   ```bash
   DEPLOYMENT\setup.bat
   ```

3. **Cài đặt Ollama và Gemma 4**
   ```bash
   # Cài đặt Ollama
   DEPLOYMENT\install_ollama.bat

   # Download Gemma 4 (model mặc định)
   ollama pull gemma4:e4b

   # Hoặc giữ Qwen 2.5 (legacy profile)
   # ollama pull qwen2.5:7b
   ```

4. **Chạy app**
   ```bash
   DEPLOYMENT\run_app.bat
   ```

### Cách 2: Manual Setup

1. **Cài đặt dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Cài đặt FFmpeg**
   - Download từ https://ffmpeg.org/
   - Thêm vào PATH

3. **Cài đặt Ollama**
   - Download từ https://ollama.ai/
   - Chạy: `ollama pull gemma4:e4b`

4. **Chạy app**
   ```bash
   python app\gui.py
   ```

## 📖 Hướng dẫn sử dụng

1. **Khởi động app**
   ```bash
   DEPLOYMENT\run_app.bat
   ```

2. **Upload file audio**
   - Kéo thả file Zoom recording (M4A, MP4, MP3)
   - Hoặc click vào ô upload

3. **Xử lý**
   - Click "Bắt đầu xử lý"
   - Đợi 10-15 phút (cho file 2 giờ)

4. **Tải kết quả**
   - `transcript_*.txt`: Nội dung đầy đủ
   - `summary_*.txt`: Tóm tắt

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

## 🧪 Testing

```bash
# Chạy tests
pytest tests/

# Coverage
pytest --cov=src tests/

# Lint
flake8 src/ app/
black --check src/ app/
```

## 📁 Project Structure

```
voicemeet_sum/
├── app/
│   ├── gui.py              # Gradio interface
│   └── themes.py           # Custom themes
├── config/
│   ├── settings.py         # Configuration (ModelProfile, auto-detect)
│   └── prompts.py          # Bilingual Việt-Nhật prompt templates
├── src/
│   ├── pipeline/
│   │   └── meeting_pipeline.py    # Main pipeline
│   ├── transcription/
│   │   ├── whisper_service.py     # Faster-Whisper (large-v3-turbo)
│   │   └── audio_processor.py     # FFmpeg
│   ├── summarization/
│   │   └── qwen_service.py        # LLMService: Gemma 4 / Qwen via Ollama
│   └── utils/
│       ├── logger.py
│       ├── file_handler.py
│       ├── system_checker.py
│       └── text_processor.py
├── tests/
├── DEPLOYMENT/
│   ├── setup.bat           # One-click setup
│   └── run_app.bat         # Launch app
└── requirements.txt
```

## 🐛 Troubleshooting

### FFmpeg không tìm thấy
```bash
# Cài đặt FFmpeg
DEPLOYMENT\install_ffmpeg.bat

# Hoặc download và thêm vào PATH
```

### Ollama không chạy
```bash
# Khởi động Ollama
ollama serve

# Pull Gemma 4 (optimized profile)
ollama pull gemma4:e4b

# Hoặc Qwen 2.5 (legacy profile)
# ollama pull qwen2.5:7b
```

### GPU không được sử dụng
```bash
# Kiểm tra CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Cài đặt PyTorch với CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory
- Dùng `MODEL_PROFILE=legacy` để về model nhỏ hơn
- Hoặc đổi sang `gemma4:e2b` (nhỏ hơn E4B)
- Đóng các ứng dụng khác
- Giảm `chunk_size` trong config

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact
- Issues: https://github.com/Viethiep49/voicemeet_sum/issues
- Email: truongviethiep49@gmail.com
