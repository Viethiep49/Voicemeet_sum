# Troubleshooting Guide

## ❓ Common Issues and Solutions

### 1. FFmpeg không tìm thấy

**Lỗi:**
```
RuntimeError: FFmpeg không được cài đặt
```

**Giải pháp:**
1. Cài đặt FFmpeg:
   ```bash
   DEPLOYMENT\install_ffmpeg.bat
   ```

2. Hoặc thủ công:
   - Download từ https://ffmpeg.org/download.html
   - Giải nén và thêm vào PATH
   - Test: `ffmpeg -version`

### 2. Ollama không chạy

**Lỗi:**
```
RuntimeError: Ollama chưa được khởi động
```

**Giải pháp:**
1. Khởi động Ollama:
   ```bash
   ollama serve
   ```

2. Trong terminal khác, pull model:
   ```bash
   ollama pull qwen2.5:7b
   ```

3. Test:
   ```bash
   curl http://localhost:11434/api/tags
   ```

### 3. GPU không được sử dụng

**Lỗi:**
```
Whisper using CPU instead of CUDA
```

**Giải pháp:**
1. Kiểm tra CUDA:
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```

2. Cài PyTorch với CUDA:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. Kiểm tra GPU:
   ```bash
   nvidia-smi
   ```

### 4. Out of Memory

**Lỗi:**
```
CUDA out of memory
```

**Giải pháp:**
1. Giảm model size:
   - Edit `config/settings.py`
   - Change: `TRANSCRIPTION.model = "small"`

2. Giảm batch size:
   - Change: `TRANSCRIPTION.compute_type = "int8"`

3. Đóng các ứng dụng khác

4. Restart và thử lại

### 5. Audio file không hợp lệ

**Lỗi:**
```
File audio không hợp lệ
```

**Giải pháp:**
1. Kiểm tra format: M4A, MP4, MP3, WAV, FLAC
2. Kiểm tra file không corrupt
3. Chuyển đổi format nếu cần:
   ```bash
   ffmpeg -i input.m4a output.wav
   ```

### 6. Processing chậm

**Vấn đề:**
```
Processing mất quá nhiều thời gian
```

**Giải pháp:**
1. Sử dụng GPU
2. Giảm model size
3. Tắt các options không cần:
   - Normalize: False
   - Remove silence: False

### 7. Model không download

**Lỗi:**
```
Failed to download model
```

**Giải pháp:**
1. Kiểm tra kết nối internet
2. Thử download thủ công:
   ```bash
   python DEPLOYMENT\download_models.py
   ```

3. Hoặc download từ HuggingFace

### 8. Port 7860 đã được sử dụng

**Lỗi:**
```
Port 7860 is already in use
```

**Giải pháp:**
1. Đổi port trong `app/gui.py`:
   ```python
   app.launch(server_port=7861)
   ```

2. Hoặc đóng app đang chạy

### 9. Vietnamese text bị lỗi encoding

**Vấn đề:**
```
Vietnamese characters corrupted
```

**Giải pháp:**
1. Đảm bảo UTF-8 encoding
2. Kiểm tra terminal encoding:
   ```bash
   chcp 65001
   ```

### 10. Ollama model không tìm thấy

**Lỗi:**
```
Model qwen2.5:7b not found
```

**Giải pháp:**
1. List models:
   ```bash
   ollama list
   ```

2. Pull model:
   ```bash
   ollama pull qwen2.5:7b
   ```

3. Test:
   ```bash
   ollama run qwen2.5:7b "Hello"
   ```

## 🔧 System Requirements Check

Chạy script để kiểm tra hệ thống:

```bash
python DEPLOYMENT\check_system.py
```

Script sẽ kiểm tra:
- ✅ Python version
- ✅ FFmpeg
- ✅ GPU/CUDA
- ✅ Ollama

## 📞 Getting Help

Nếu vẫn gặp vấn đề:

1. Kiểm tra logs trong `logs/` folder
2. Chạy với debug mode:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. Mở issue trên GitHub với:
   - Error message
   - System specs
   - Log file

## 🔍 Debug Mode

Để bật debug logging:

```python
# In config/settings.py or src/utils/logger.py
setup_logger(level=logging.DEBUG)
```

## 📝 Log Locations

- Application logs: `logs/YYYYMMDD_HHMMSS.log`
- FFmpeg logs: Console output
- Whisper logs: Console output
- Ollama logs: `~/.ollama/logs/`

