# Voicemeet by Hiepne - Technical Specifications

## 🖥️ Target System

```yaml
Hardware:
  CPU: Intel i5
  RAM: 16GB
  GPU: RTX 4070 (12GB VRAM)
  Storage: SSD
  OS: Windows 11 64-bit
  Internet: Fast (for model download)

User Profile:
  Technical Level: Non-tech
  Use Case: Zoom meeting recordings
  Frequency: 5-6 files/week
  Audio Length: 1-2 hours per file
```

## 🎙️ Audio Characteristics

```yaml
Input:
  Source: Zoom recordings
  Format: M4A, MP4, MP3 (mixed)
  Duration: 1-2 hours
  Speakers: 5-6 people
  
Languages:
  Vietnamese: 80-90% (primary)
  Japanese: 10-20% (secondary)
  Domain: F&B industry (phở, food products)
  
Quality:
  Codec: Auto-detect
  Sample Rate: 44.1kHz or 48kHz (Zoom default)
  Channels: Stereo or Mono
```

## ⚙️ Model Configuration

### Transcription: Faster-Whisper
```yaml
Model: medium
Rationale:
  - RTX 4070: Can handle large-v3 BUT
  - Priority: SPEED (user requirement)
  - medium = 5x faster than large-v3
  - Accuracy: 90-92% (sufficient for Vietnamese)
  - VRAM: ~5GB (leaves headroom)
  
Performance:
  2-hour audio: 6-8 minutes
  Speed: 15-20x realtime
  
Settings:
  compute_type: float16 (RTX 4070 optimized)
  beam_size: 5
  vad_filter: true (critical for meetings)
  language: vi (primary)
  initial_prompt: "Cuộc họp công ty F&B, có từ tiếng Nhật về thực phẩm như phở"
```

### Summarization: Qwen
```yaml
Model: qwen2.5:7b
Rationale:
  - RAM: 8GB usage (16GB total = safe)
  - Speed: ~2-3 min for 2h transcript
  - Quality: Excellent for Vietnamese
  
Performance:
  Input: 30,000-50,000 chars
  Processing: 2-3 minutes
  Output: 2 summaries
```

## 📦 Architecture

### Core Pipeline
```
Zoom Recording (M4A/MP4)
    ↓
FFmpeg (Audio Extraction + Normalization)
    ↓
Faster-Whisper (Transcription)
    ↓
Text Processing (Chunking if needed)
    ↓
Qwen (Summarization)
    ↓
Output Files (2 TXT files)
```

### Processing Flow
```python
1. Upload audio file (drag & drop)
2. FFmpeg: Extract & normalize audio
   - Convert to 16kHz mono WAV
   - Normalize volume
   - Remove silence (optional)
3. Whisper: Transcribe
   - Progress: 0-80%
   - Real-time updates every 5 min
4. Qwen: Summarize
   - Progress: 80-100%
   - Generate 2 summaries
5. Save outputs
6. Display results
```

## 📄 Output Format

### File 1: Full Transcript
```
transcript_full.txt
-------------------
Chào mọi người. Hôm nay chúng ta sẽ thảo luận về menu mới cho quán phở.

Vâng, tôi nghĩ chúng ta nên thêm phở bò Úc vào menu. Khách hàng đang yêu cầu nhiều.

Nhưng giá bò Úc đang tăng cao. Chúng ta cần tính toán lại margin...

[... full content ...]
```

### File 2: Summary
```
summary.txt
-----------
# TÓM TẮT CUỘC HỌP

## NỘI DUNG CHÍNH
Cuộc họp bàn về việc mở rộng menu cho chuỗi quán phở. Các điểm chính:
- Đề xuất thêm phở bò Úc vào menu
- Lo ngại về giá nguyên liệu tăng cao
- Quyết định pilot tại 2 chi nhánh trước
- Timeline: Triển khai trong tháng 12

## CÁC QUYẾT ĐỊNH
1. Pilot phở bò Úc tại chi nhánh Quận 1 và Quận 7
2. Budget: 50 triệu cho marketing
3. Training nhân viên tuần tới

## HÀNH ĐỘNG CẦN LÀM
- Anh Minh: Liên hệ nhà cung cấp bò Úc (deadline: 10/11)
- Chị Lan: Thiết kế poster quảng cáo (deadline: 15/11)
- Team: Chuẩn bị training materials
```

## 🚀 Deployment Strategy

### Option: GitHub + One-Click Setup Script

#### Repository Structure
```
Voicemeet_sum/
├── README.md
├── setup.bat              # ← ONE-CLICK SETUP (Windows)
├── requirements.txt
├── install_ollama.bat     # Auto-install Ollama
├── download_models.bat    # Auto-download models
├── run_app.bat           # Launch app
├── [source code folders]
└── assets/
    └── user_guide.pdf
```

#### Setup Flow (One-Click)
```batch
setup.bat:
1. Check Python installed (if not, download & install)
2. Create virtual environment
3. Install dependencies (pip install -r requirements.txt)
4. Check Ollama (if not, run install_ollama.bat)
5. Download models (Whisper + Qwen)
6. Create desktop shortcut
7. Done! → Launch app
```

#### User Experience (Nguyen's Side)
```
1. TeamViewer vào máy
2. Open browser → GitHub repo
3. Click "Code" → Download ZIP
4. Extract to Desktop
5. Double-click setup.bat
   → Màn hình terminal xuất hiện
   → Tự động cài đặt mọi thứ (5-10 phút)
   → "Setup complete! Press any key to launch app"
6. App tự động mở trong browser
7. Done!
```

## 🎨 GUI Design (Gradio)

### Simple Interface (Japanese-style minimalism)
```
┌────────────────────────────────────────────────┐
│  🎤 Voicemeet_sum by Hiepne                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                │
│  📁 Chọn file audio                            │
│  ┌──────────────────────────────────────────┐ │
│  │  📎 Drop Zoom recording here             │ │
│  │     (M4A, MP4, MP3)                      │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ⚙️ Cài đặt (tùy chọn)                         │
│  ☐ Loại bỏ khoảng lặng                        │
│  ☐ Tối ưu âm lượng                            │
│                                                │
│  ┌─────────────┐                              │
│  │ 🚀 Bắt đầu  │                              │
│  └─────────────┘                              │
│                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  📊 Tiến độ                                    │
│  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░ 52%                   │
│  ⏱️ Đang xử lý... 3.2/6.0 phút dự kiến        │
│  🔄 Transcribing audio...                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                │
│  ✅ Hoàn thành!                                │
│  📄 transcript_full.txt (28.5 KB)            │
│  📋 summary.txt (3.2 KB)                     │
│                                                │
│  [📥 Tải cả 2 file]  [📂 Mở thư mục]         │
│  [🔄 Xử lý file mới]                          │
└────────────────────────────────────────────────┘
```

### Key Features
- **Auto-detect format**: M4A, MP4, MP3, WAV
- **Progress tracking**: Real-time percentage + ETA
- **Error handling**: Friendly messages (Vietnamese)
- **Auto-open output**: Folder opens when done
- **History**: Last 5 processed files (optional)

## ⚡ Performance Targets

### Processing Time (2-hour audio)
```
FFmpeg preprocessing:     30-60 sec
Whisper transcription:    6-8 min
Qwen summarization:       2-3 min
File writing:             5-10 sec
------------------------
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
CPU: 20-40% (preprocessing)
Disk: 200 MB temp files
```

## 🔧 FFmpeg Configuration

### Audio Preprocessing Pipeline
```bash
ffmpeg -i input.m4a \
  -ar 16000 \              # Resample to 16kHz (Whisper optimal)
  -ac 1 \                  # Convert to mono
  -af "loudnorm,silenceremove=1:0:-50dB" \  # Normalize + remove silence
  -f wav \
  output.wav
```

### Why FFmpeg?
- ✅ Handle all Zoom formats (M4A, MP4, etc.)
- ✅ Normalize volume (meetings have varying levels)
- ✅ Remove long silences (speed up transcription)
- ✅ Convert to optimal format for Whisper

## 🛡️ Error Handling

### Common Issues & Solutions
```python
1. FFmpeg not found
   → Auto-install ffmpeg via setup script

2. Ollama not running
   → Auto-start Ollama service

3. Model not downloaded
   → Auto-download on first run

4. Out of memory
   → Show message: "Đóng các ứng dụng khác và thử lại"

5. Audio file corrupt
   → "File audio không hợp lệ. Vui lòng kiểm tra lại."

6. Network error (model download)
   → Retry with progress bar
```

## 📊 Testing Checklist

- [ ] Zoom M4A file (1 hour)
- [ ] Zoom MP4 file (2 hours)
- [ ] MP3 file (90 minutes)
- [ ] Vietnamese only
- [ ] Vietnamese + Japanese mixed
- [ ] 2 speakers
- [ ] 6+ speakers
- [ ] Poor audio quality
- [ ] Background noise
- [ ] Multiple sessions (stability)

## 🚢 Deployment Checklist

### For Developer (You)
- [ ] Code complete & tested
- [ ] Create setup.bat script
- [ ] Create user guide (PDF)
- [ ] Test on clean Windows 11 VM
- [ ] Push to GitHub (private repo)
- [ ] Create release tag

### For End User (Brother)
- [ ] TeamViewer session
- [ ] Clone from GitHub
- [ ] Run setup.bat
- [ ] Test with sample file
- [ ] Walk through features
- [ ] Answer questions
- [ ] Done!

## 📈 Future Enhancements (v2)

- Speaker diarization (phân biệt người nói)
- Batch processing (nhiều file cùng lúc)
- Email auto-send summary
- Mobile app (iOS/Android)
- Cloud sync option
- Multi-language UI

## 🎯 Success Criteria

✅ Setup time: < 10 minutes
✅ Processing speed: < 15 minutes for 2h audio
✅ Accuracy: > 90% for Vietnamese
✅ User-friendly: Non-tech can use without help
✅ Reliable: No crashes, auto-recovery
✅ Offline: 100% local, no internet after setup