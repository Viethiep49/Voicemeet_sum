# 🎤 Voicemeet_sum

Automated meeting transcription and summarization application for Zoom recordings.

## 🎯 Features

- ✅ **Transcription**: Audio to text with [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) (medium model)
- ✅ **Summarization**: Auto-summary with [Qwen 2.5 7B](https://ollama.ai/library/qwen2.5:7b)
- ✅ **FFmpeg**: Audio preprocessing (normalize, resample, remove silence)
- ✅ **GUI**: Web interface with Gradio
- ✅ **Progress Tracking**: Real-time progress updates
- ✅ **Multilingual**: Supports Vietnamese + Japanese

## 🎯 System Requirements

```yaml
OS: Windows 10/11 (64-bit)
CPU: Intel i5 or better
RAM: 16GB or more
GPU: NVIDIA RTX 4070 (recommended, 12GB VRAM)
Storage: 20GB free space
Internet: Required for initial model download
```

## 🚀 Installation

### Method 1: Automated Setup (Recommended)

1. **Clone repository**
   ```bash
   git clone https://github.com/your-username/voicemeet_sum.git
   cd voicemeet_sum
   ```

2. **Run setup script**
   ```bash
   DEPLOYMENT\setup.bat
   ```

3. **Install Ollama and Qwen**
   ```bash
   # Install Ollama
   DEPLOYMENT\install_ollama.bat
   
   # Download Qwen model
   ollama pull qwen2.5:7b
   ```

4. **Run app**
   ```bash
   DEPLOYMENT\run_app.bat
   ```

### Method 2: Manual Setup

1. **Install dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install FFmpeg**
   - Download from https://ffmpeg.org/
   - Add to PATH

3. **Install Ollama**
   - Download from https://ollama.ai/
   - Run: `ollama pull qwen2.5:7b`

4. **Run app**
   ```bash
   python app\gui.py
   ```

## 📖 Usage

1. **Start app**
   ```bash
   DEPLOYMENT\run_app.bat
   ```

2. **Upload audio file**
   - Drag & drop Zoom recording (M4A, MP4, MP3)
   - Or click upload button

3. **Process**
   - Click "🚀 Bắt đầu xử lý"
   - Wait 10-15 minutes (for 2-hour file)

4. **Download results**
   - `transcript_*.txt`: Full content
   - `summary_*.txt`: Summary

## ⚙️ Configuration

Edit `config/settings.py`:

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
# Run tests
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

### FFmpeg not found
```bash
# Install FFmpeg
DEPLOYMENT\install_ffmpeg.bat

# Or download and add to PATH
```

### Ollama not running
```bash
# Start Ollama
ollama serve

# In another terminal
ollama pull qwen2.5:7b
```

### GPU not being used
```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory
- Reduce model size: `medium` → `small`
- Reduce `chunk_size` in config
- Close other applications

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact

- Issues: https://github.com/your-username/voicemeet_sum/issues
- Email: your-email@example.com

---

Made with ❤️ for efficient meeting transcription

