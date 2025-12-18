# 🍎 Setup Guide - Mac M1 8GB RAM

> **Tối ưu cho:** MacBook Air/Pro M1/M2/M3 với 8GB RAM
> **Mục đích:** Demo IT GOTTALENT Competition
> **Thời gian setup:** 15-20 phút

---

## ✅ Prerequisites Check

Trước khi bắt đầu, kiểm tra:

```bash
# Check macOS version (cần >= 12.3 cho MPS support)
sw_vers

# Check RAM
sysctl hw.memsize | awk '{print $2/1073741824 " GB"}'

# Check chip (phải là arm64)
uname -m
# Output: arm64 ✅
```

---

## 📦 Step 1: Install Homebrew Dependencies

```bash
# Install Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install FFmpeg (REQUIRED cho audio processing)
brew install ffmpeg

# Verify FFmpeg
ffmpeg -version
# Should show: ffmpeg version 6.x.x or higher

# Install Ollama (REQUIRED cho LLM)
brew install ollama

# Verify Ollama
ollama --version
```

---

## 🐍 Step 2: Setup Python Environment

```bash
# Navigate to project directory
cd /Users/kaito/Documents/Voicemeet_sum

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

---

## 📚 Step 3: Install Python Dependencies

```bash
# Install dependencies for Mac M1
pip install -r requirements_mac_m1.txt

# Install PyTorch with MPS (Metal Performance Shaders) support
pip3 install torch torchvision torchaudio

# Verify PyTorch installation
python3 -c "import torch; print('PyTorch:', torch.__version__)"
python3 -c "import torch; print('MPS Available:', torch.backends.mps.is_available())"
# Should output: MPS Available: True ✅
```

---

## 🤖 Step 4: Setup Ollama & Download Models

```bash
# Start Ollama service (in background)
ollama serve &

# Wait 5 seconds for service to start
sleep 5

# Pull Qwen 2.5 3B model (IMPORTANT: Use 3B not 7B!)
ollama pull qwen2.5:3b
# This will download ~2GB, takes 2-5 minutes

# Verify model is ready
ollama list
# Should show: qwen2.5:3b

# Test Qwen (optional)
ollama run qwen2.5:3b "Xin chào"
# Should respond in Vietnamese
```

**⚠️ CRITICAL:** Dùng `qwen2.5:3b` (3 billion params), KHÔNG dùng `qwen2.5:7b`!
7B model cần ~10GB RAM và sẽ làm crash máy 8GB.

---

## 🧪 Step 5: Verify System Configuration

```bash
# Check current config
DEBUG_CONFIG=true python3 -c "from config.settings import print_config_info; print_config_info()"
```

**Expected output:**
```
============================================================
🔧 VOICEMEET_SUM CONFIGURATION
============================================================
Platform:        Darwin (arm64)
RAM:            8.0 GB
Mac M1 Mode:    True
Low RAM Mode:   True
------------------------------------------------------------
Whisper Model:  small
Whisper Device: cpu
Compute Type:   int8
Workers:        2
------------------------------------------------------------
Qwen Model:     qwen2.5:3b
Max Tokens:     2000
------------------------------------------------------------
Chunk Size:     8192
Max File Size:  50 MB
Output Formats: txt, docx
============================================================
```

Nếu output khớp ✅ → Configuration tự động đã hoạt động!

---

## 🚀 Step 6: Run the Application

### Option A: FastAPI Backend (Recommended for Demo)

```bash
# Method 1: Using uvicorn directly
uvicorn app.backend:app --host 0.0.0.0 --port 8000 --reload

# Method 2: Using Python
python3 -m uvicorn app.backend:app --reload

# Access web UI
# Open browser: http://localhost:8000
```

### Option B: Test with Sample File

```bash
# Create test script
cat > test_mac_demo.py << 'EOF'
from src.pipeline.meeting_pipeline import MeetingPipeline
from config.settings import print_config_info

# Print config
print_config_info()

# Initialize pipeline
pipeline = MeetingPipeline()

# Process a short audio file (prepare 5-10 min file for demo)
audio_file = "examples/demo_5min.m4a"  # Put your demo file here
transcript, summary = pipeline.process(
    audio_file,
    progress_callback=lambda p, m: print(f"[{p}%] {m}")
)

print("\n✅ TRANSCRIPT:")
print(transcript[:500])

print("\n✅ SUMMARY:")
print(summary)
EOF

# Run test
python3 test_mac_demo.py
```

---

## 🎯 Demo Preparation Checklist

### 1. Pre-Demo System Optimization

```bash
# Free up RAM
sudo purge

# Close unnecessary apps
killall "Google Chrome" "Slack" "Discord" "Spotify" 2>/dev/null

# Check available memory
vm_stat | grep "Pages free"
# Should have at least 2GB free
```

### 2. Prepare Demo Files

**Recommended demo file specs:**
- **Duration:** 5-10 minutes (NOT 2 hours!)
- **Format:** M4A or MP3
- **Content:** Vietnamese + some Japanese words
- **Size:** < 20 MB

**Why short files?**
- Mac M1 8GB with CPU transcription: ~2-3x realtime
- 10-minute audio → ~3-4 minutes processing
- Perfect for live demo!

### 3. Pre-load Models (Before Judges Arrive!)

```bash
# Start Ollama
ollama serve &

# Warm-up Qwen (loads model into RAM)
ollama run qwen2.5:3b "test" && echo "✅ Qwen ready"

# Pre-download Whisper model (first run only)
python3 -c "
from src.transcription.whisper_service import WhisperService
ws = WhisperService()
print('✅ Whisper model cached')
"
```

### 4. Backup Plan

```bash
# Pre-process demo file and save results
mkdir -p demo_backup

# Process demo file beforehand
python3 test_mac_demo.py > demo_backup/demo_output.txt

# During demo: if live fails, show pre-processed results
cat demo_backup/demo_output.txt
```

---

## 📊 Expected Performance (Mac M1 8GB)

| Metric | Value | Note |
|--------|-------|------|
| **10-min audio** | 3-4 min processing | Acceptable for demo |
| **30-min audio** | 11-16 min processing | Too long for live demo |
| **RAM usage** | 6-7 GB peak | Close to limit |
| **Accuracy (Vi)** | 90-93% | Slightly lower than "medium" |
| **Accuracy (Ja)** | 85-88% | Acceptable |

**💡 Pro tip:** Use 5-10 minute demo files, NOT full 2-hour meetings!

---

## ⚠️ Common Issues & Fixes

### Issue 1: "Killed: 9" (Out of Memory)

**Symptoms:** Process crashes suddenly
**Cause:** RAM exhausted

**Solution:**
```bash
# Edit config/settings.py manually to force tiny model
echo "TRANSCRIPTION.model = 'tiny'" >> config/settings_override.py

# Or use even smaller Qwen
ollama pull qwen2.5:1.5b  # If 3b still too big
```

### Issue 2: Ollama Connection Failed

**Symptoms:** `Connection refused to localhost:11434`

**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not, start it
ollama serve &

# Wait and test
sleep 3
curl http://localhost:11434
# Should return: Ollama is running
```

### Issue 3: FFmpeg Not Found

**Symptoms:** `FileNotFoundError: ffmpeg`

**Solution:**
```bash
# Install FFmpeg
brew install ffmpeg

# Verify
which ffmpeg
# Should show: /opt/homebrew/bin/ffmpeg
```

### Issue 4: MPS Not Available

**Symptoms:** `MPS backend not available`

**Solution:**
```bash
# Check macOS version
sw_vers
# Needs macOS >= 12.3

# If older: upgrade macOS or force CPU mode
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

### Issue 5: Processing Too Slow

**Current:** 10-min audio takes 3-4 minutes
**Want faster?**

**Options:**
1. Use "tiny" Whisper model (2x faster, but -5% accuracy)
2. Reduce beam_size to 3 (slight speed up)
3. Disable VAD filter (faster but less accurate)

**Quick fix:**
```python
# Edit config/settings.py
TRANSCRIPTION.model = "tiny"  # Was: "small"
TRANSCRIPTION.beam_size = 3   # Was: 5
```

---

## 🎬 Demo Day Checklist

**1 Day Before:**
- [ ] Test full pipeline end-to-end
- [ ] Prepare 2-3 demo files (5, 10, 15 minutes)
- [ ] Pre-process files and save outputs as backup
- [ ] Charge MacBook to 100%

**2 Hours Before:**
- [ ] Close all unnecessary apps
- [ ] Run `sudo purge` to free RAM
- [ ] Start Ollama: `ollama serve &`
- [ ] Warm-up Qwen: `ollama run qwen2.5:3b "test"`
- [ ] Test FastAPI server: `uvicorn app.backend:app --reload`

**30 Minutes Before:**
- [ ] Open Activity Monitor → check available RAM (need 2GB+ free)
- [ ] Test upload 1 demo file to verify pipeline works
- [ ] Open browser to http://localhost:8000
- [ ] Have backup pre-processed results ready

**During Demo:**
- [ ] Smile and speak clearly
- [ ] Upload 5-10 min file (NOT 2 hours!)
- [ ] Show progress bar
- [ ] While processing: explain architecture
- [ ] Show results: transcript + summary + DOCX
- [ ] If fails: gracefully show pre-processed backup

---

## 🎓 Alternative: Cloud Demo (Fallback)

Nếu Mac M1 8GB không đủ mạnh cho smooth demo:

### Option 1: Google Colab (Free GPU)

```python
# Upload notebook với code
# Use free T4 GPU (16GB VRAM)
# Much faster: 10-min audio → 1 minute!
# Link: https://colab.research.google.com
```

### Option 2: Deploy to Render.com

```bash
# Free tier: 512MB RAM (too small)
# Paid tier: $7/month for 2GB RAM
# Show demo via URL instead of localhost
```

---

## ✅ Verification Script

Save and run này để test everything:

```bash
cat > verify_mac_setup.sh << 'EOF'
#!/bin/bash

echo "🔍 Verifying Mac M1 Setup for Voicemeet_sum..."
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python not found"
    exit 1
fi

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg: $(ffmpeg -version | head -n1)"
else
    echo "❌ FFmpeg not found - run: brew install ffmpeg"
    exit 1
fi

# Check Ollama
if command -v ollama &> /dev/null; then
    echo "✅ Ollama: $(ollama --version)"
else
    echo "❌ Ollama not found - run: brew install ollama"
    exit 1
fi

# Check virtual environment
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "⚠️  Virtual environment not found - run: python3 -m venv venv"
fi

# Check if Ollama is running
if curl -s http://localhost:11434 > /dev/null; then
    echo "✅ Ollama service running"
else
    echo "⚠️  Ollama not running - run: ollama serve &"
fi

# Check Qwen model
if ollama list | grep -q "qwen2.5:3b"; then
    echo "✅ Qwen 2.5 3B model downloaded"
else
    echo "⚠️  Qwen model not found - run: ollama pull qwen2.5:3b"
fi

# Check RAM
RAM_GB=$(sysctl hw.memsize | awk '{print int($2/1073741824)}')
echo "💾 RAM: ${RAM_GB} GB"
if [ $RAM_GB -lt 8 ]; then
    echo "⚠️  Low RAM detected"
fi

# Check architecture
ARCH=$(uname -m)
if [ "$ARCH" == "arm64" ]; then
    echo "✅ Apple Silicon (arm64)"
else
    echo "⚠️  Not Apple Silicon: $ARCH"
fi

echo ""
echo "🎉 Setup verification complete!"
EOF

chmod +x verify_mac_setup.sh
./verify_mac_setup.sh
```

---

## 📞 Support

**Issues?** Check:
1. This guide: SETUP_MAC_M1.md
2. Main README: README.md
3. Project plan: PROJECT_PLAN.md

**Still stuck?**
- GitHub Issues: https://github.com/Viethiep49/voicemeet_sum/issues
- Email: truongviethiep49@gmail.com

---

**Good luck with IT GOTTALENT! 🚀🏆**
