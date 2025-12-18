#!/bin/bash

# Quick Setup Script for Mac M1 8GB RAM
# Voicemeet_sum - IT GOTTALENT Competition

set -e  # Exit on error

echo "🍎 Starting Mac M1 Setup for Voicemeet_sum..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo "📋 Step 1: Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install from python.org${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3 found: $(python3 --version)${NC}"

if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}⚠️  Homebrew not found. Installing...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
echo -e "${GREEN}✅ Homebrew found${NC}"

# Step 2: Install system dependencies
echo ""
echo "📦 Step 2: Installing FFmpeg and Ollama..."

if ! command -v ffmpeg &> /dev/null; then
    echo "Installing FFmpeg..."
    brew install ffmpeg
else
    echo -e "${GREEN}✅ FFmpeg already installed${NC}"
fi

if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    brew install ollama
else
    echo -e "${GREEN}✅ Ollama already installed${NC}"
fi

# Step 3: Create virtual environment
echo ""
echo "🐍 Step 3: Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Step 4: Install Python dependencies
echo ""
echo "📚 Step 4: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements_mac_m1.txt

echo ""
echo "🔥 Step 5: Installing PyTorch with MPS support..."
pip3 install torch torchvision torchaudio

# Verify PyTorch MPS
echo ""
echo "🧪 Verifying PyTorch installation..."
python3 -c "import torch; print('PyTorch version:', torch.__version__)"
python3 -c "import torch; print('MPS available:', torch.backends.mps.is_available())"

# Step 6: Start Ollama and download model
echo ""
echo "🤖 Step 6: Setting up Ollama and downloading Qwen model..."

# Start Ollama in background
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    OLLAMA_PID=$!
    sleep 5
else
    echo -e "${GREEN}✅ Ollama already running${NC}"
fi

# Pull Qwen 3B model
if ! ollama list | grep -q "qwen2.5:3b"; then
    echo "Downloading Qwen 2.5 3B model (this may take 5-10 minutes)..."
    ollama pull qwen2.5:3b
else
    echo -e "${GREEN}✅ Qwen 2.5 3B already downloaded${NC}"
fi

# Step 7: Verify configuration
echo ""
echo "🔧 Step 7: Verifying system configuration..."
DEBUG_CONFIG=true python3 -c "from config.settings import print_config_info; print_config_info()"

# Create necessary directories
echo ""
echo "📁 Creating project directories..."
mkdir -p output models logs temp

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start the server: uvicorn app.backend:app --reload"
echo "3. Open browser: http://localhost:8000"
echo ""
echo "For more details, see: SETUP_MAC_M1.md"
echo ""
