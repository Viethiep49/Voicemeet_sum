# 🚀 Voicemeet_sum - Deployment Guide

Hướng dẫn triển khai Voicemeet_sum trên các môi trường khác nhau.

---

## 📋 Table of Contents

1. [Docker Deployment (Recommended)](#docker-deployment)
2. [Manual Deployment (GitHub Clone)](#manual-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Troubleshooting](#troubleshooting)

---

## 🐳 Docker Deployment (Recommended)

### Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- 8GB+ RAM available
- 10GB+ disk space

### Quick Start

```bash
# 1. Clone repository
git clone <your-repo-url>
cd Voicemeet_sum

# 2. Start all services
docker-compose up -d

# 3. Wait for models to download (~2-3 minutes first time)
docker-compose logs -f model_init

# 4. Open browser
open http://localhost:8000
```

### Detailed Steps

#### 1. Installation

**Windows:**
```powershell
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Start Docker Desktop (check system tray icon)

# Clone repository
git clone <your-repo-url>
cd Voicemeet_sum

# Start services
docker-compose up -d
```

**Mac:**
```bash
# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop
open -a Docker

# Clone repository
git clone <your-repo-url>
cd Voicemeet_sum

# Start services
docker-compose up -d
```

**Linux:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Clone repository
git clone <your-repo-url>
cd Voicemeet_sum

# Start services
sudo docker-compose up -d
```

#### 2. Verify Services

```bash
# Check all containers are running
docker-compose ps

# Should see:
# voicemeet_app     running   0.0.0.0:8000->8000/tcp
# voicemeet_ollama  running   0.0.0.0:11434->11434/tcp
# voicemeet_model_init exited (0)  # This is OK - one-time setup

# Check logs
docker-compose logs -f voicemeet

# Check health
curl http://localhost:8000/api/health
```

#### 3. Access Application

```
Web UI: http://localhost:8000
API Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/api/health
```

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Update and rebuild
git pull
docker-compose up -d --build

# Clean up everything (WARNING: deletes data!)
docker-compose down -v
```

### Customization

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - OLLAMA_BASE_URL=http://ollama:11434
  - LOG_LEVEL=DEBUG  # Change to DEBUG for more logs
  - MAX_UPLOAD_SIZE=1073741824  # Change max file size (1GB example)

ports:
  - "8080:8000"  # Change port if 8000 is taken
```

---

## 💻 Manual Deployment (GitHub Clone)

### For Mac M1/M2

```bash
# 1. Clone repository
git clone <your-repo-url>
cd Voicemeet_sum

# 2. Run automated setup
chmod +x quick_setup_mac.sh
./quick_setup_mac.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start Ollama (if not running)
ollama serve &

# 5. Start FastAPI server
uvicorn app.backend:app --reload --host 0.0.0.0 --port 8000

# 6. Open browser
open http://localhost:8000
```

### For Windows (GPU)

```powershell
# 1. Prerequisites
# - Python 3.10+ (https://www.python.org/downloads/)
# - FFmpeg (https://ffmpeg.org/download.html) - Add to PATH
# - Ollama (https://ollama.ai/download)
# - NVIDIA GPU with CUDA 11.8+ (https://developer.nvidia.com/cuda-downloads)

# 2. Clone repository
git clone <your-repo-url>
cd Voicemeet_sum

# 3. Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements_fastapi.txt

# 5. Install PyTorch with CUDA
pip install torch==2.1.0+cu121 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 6. Start Ollama
ollama serve

# 7. Download Qwen model (in new terminal)
ollama pull qwen2.5:7b  # Use 7b on high-RAM Windows

# 8. Start FastAPI server (in new terminal)
.\venv\Scripts\activate
uvicorn app.backend:app --reload --host 0.0.0.0 --port 8000

# 9. Open browser
start http://localhost:8000
```

### For Linux (GPU)

```bash
# 1. Install system dependencies
sudo apt-get update
sudo apt-get install -y python3.10 python3-pip python3-venv ffmpeg curl

# 2. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 3. Clone repository
git clone <your-repo-url>
cd Voicemeet_sum

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements_fastapi.txt

# 6. Install PyTorch with CUDA
pip install torch==2.1.0+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 7. Start Ollama
ollama serve &

# 8. Download Qwen model
ollama pull qwen2.5:7b

# 9. Start FastAPI server
uvicorn app.backend:app --reload --host 0.0.0.0 --port 8000

# 10. Open browser
xdg-open http://localhost:8000
```

---

## ☁️ Cloud Deployment

### Option 1: Docker on Cloud VM (AWS, GCP, Azure)

```bash
# 1. Provision VM (Ubuntu 22.04, 8GB+ RAM, 50GB+ disk)
# 2. SSH into VM
# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose-plugin

# 4. Clone and deploy
git clone <your-repo-url>
cd Voicemeet_sum
sudo docker-compose up -d

# 5. Configure firewall to allow port 8000
# AWS: Security Groups
# GCP: Firewall Rules
# Azure: Network Security Groups

# 6. Access via public IP
http://<VM-PUBLIC-IP>:8000
```

### Option 2: Kubernetes (Advanced)

See `k8s/` directory for Kubernetes manifests (coming soon).

---

## 🐛 Troubleshooting

### Docker Issues

**Problem: Port 8000 already in use**
```bash
# Solution 1: Stop conflicting service
lsof -ti:8000 | xargs kill -9

# Solution 2: Change port in docker-compose.yml
ports:
  - "8080:8000"  # Use port 8080 instead
```

**Problem: Ollama model not found**
```bash
# Check if model downloaded
docker exec voicemeet_ollama ollama list

# If not, manually pull
docker exec voicemeet_ollama ollama pull qwen2.5:3b
```

**Problem: Container keeps restarting**
```bash
# Check logs
docker-compose logs voicemeet

# Common causes:
# - Ollama not ready (wait 30s)
# - Insufficient RAM (need 8GB+)
# - Port conflict (change port)
```

### Manual Deployment Issues

**Problem: FFmpeg not found**
```bash
# Mac
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Add to PATH

# Linux
sudo apt-get install ffmpeg
```

**Problem: Ollama connection error**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve &

# Verify
curl http://localhost:11434/api/tags
```

**Problem: CUDA not available**
```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# If False, reinstall PyTorch with CUDA
pip install torch==2.1.0+cu121 --index-url https://download.pytorch.org/whl/cu121
```

**Problem: Out of memory**
```bash
# Close other apps
# Or use smaller models in config/settings.py:
# - Whisper: "small" → "tiny"
# - Qwen: "qwen2.5:3b" → "qwen2.5:1.5b"
```

---

## 📊 Performance Tuning

### For Low-RAM Systems (8GB)

Edit `config/settings.py`:
```python
TRANSCRIPTION.model = "tiny"  # Instead of "small"
SUMMARIZATION.model = "qwen2.5:1.5b"  # Instead of "3b"
APP.max_file_size = 25 * 1024 * 1024  # 25MB max
```

### For High-RAM Systems (16GB+)

Edit `config/settings.py`:
```python
TRANSCRIPTION.model = "medium"  # Better accuracy
SUMMARIZATION.model = "qwen2.5:7b"  # Better summaries
APP.max_file_size = 2 * 1024 * 1024 * 1024  # 2GB max
```

---

## 🔒 Security Notes

### For Production Deployment:

1. **Change default ports** (avoid 8000)
2. **Add authentication** (see `app/backend.py` TODO)
3. **Use HTTPS** (nginx reverse proxy with SSL)
4. **Limit file uploads** (already implemented: 2GB max)
5. **Rate limiting** (add with `slowapi`)
6. **Firewall rules** (only allow necessary ports)

Example nginx config:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📞 Support

**Issues?** Create an issue on GitHub: `<your-repo-url>/issues`

**Questions?** Email: truongviethiep49@gmail.com

**Documentation:** See `/docs` folder for detailed guides

---

**Happy Deploying! 🚀**
