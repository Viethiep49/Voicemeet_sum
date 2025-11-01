# 🎤 Voicemeet_sum

Ứng dụng chuyển đổi audio cuộc họp Zoom thành văn bản và tóm tắt tự động.

## 🎯 Tính năng

- ✅ **Transcription**: Chuyển đổi audio sang văn bản với [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) (medium model)
- ✅ **Summarization**: Tạo tóm tắt tự động với [Qwen 2.5 7B](https://ollama.ai/library/qwen2.5:7b)
- ✅ **FFmpeg**: Xử lý audio preprocessing (normalize, resample, remove silence)
- ✅ **GUI**: Giao diện web với Gradio
- ✅ **Progress Tracking**: Theo dõi tiến trình real-time
- ✅ **Multilingual**: Hỗ trợ tiếng Việt + tiếng Nhật

## 🎯 Yêu cầu hệ thống

```yaml
OS: Windows 10/11 (64-bit)
CPU: Intel i5 trở lên
RAM: 16GB trở lên
GPU: NVIDIA RTX 4070 (khuyên dùng, 12GB VRAM)
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

3. **Cài đặt Ollama và Qwen**
   ```bash
   # Cài đặt Ollama
   DEPLOYMENT\install_ollama.bat
   
   # Download Qwen model
   ollama pull qwen2.5:7b
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
   - Chạy: `ollama pull qwen2.5:7b`

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

Chỉnh sửa `config/settings.py`:

```python
# Whisper config
TRANSCRIPTION.model = "medium"          # medium, large-v2, large-v3
TRANSCRIPTION.compute_type = "float16"  # float16, float32, int8
TRANSCRIPTION.language = "vi"           # vi, ja, en

# Qwen config
SUMMARIZATION.model = "qwen2.5:7b"      # qwen2.5:7b, qwen2.5:14b
SUMMARIZATION.temperature = 0.3         # 0.0 - 1.0
```

## 📊 Performance

### Processing Time (2-hour audio)

```
FFmpeg preprocessing:     30-60 sec
Whisper transcription:    6-8 min
Qwen summarization:       2-3 min
──────────────────────────────────
Total:                    9-12 min
Speed:                    10-13x realtime
```

### Resource Usage

```
VRAM: 5-6 GB (Whisper medium)
RAM:  10-12 GB total
  - Whisper: 3-4 GB
  - Qwen: 7-8 GB
  - System: 2 GB
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
│   └── settings.py         # Configuration
├── src/
│   ├── pipeline/
│   │   └── meeting_pipeline.py    # Main pipeline
│   ├── transcription/
│   │   ├── whisper_service.py     # Faster-Whisper
│   │   └── audio_processor.py     # FFmpeg
│   ├── summarization/
│   │   └── qwen_service.py        # Qwen via Ollama
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

# Trong terminal khác
ollama pull qwen2.5:7b
```

### GPU không được sử dụng
```bash
# Kiểm tra CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Cài đặt PyTorch với CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory
- Giảm model size: `medium` → `small`
- Giảm `chunk_size` trong config
- Đóng các ứng dụng khác

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact
- Issues: https://github.com/Viethiep49/voicemeet_sum/issues
- Email: truongviethiep49@gmail.com
