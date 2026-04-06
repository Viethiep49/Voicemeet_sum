"""
Configuration settings for Voicemeet_sum
Auto-detects platform and optimizes for GPU (RTX 4050) or Mac M1 8GB.
Supports two model profiles via MODEL_PROFILE env var:
  - optimized (default): Whisper large-v3-turbo + Gemma 4 E4B
  - legacy: Whisper small/medium + Qwen 2.5
"""
import os
import platform
import psutil
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ============================================
# Platform & Hardware Detection
# ============================================

def detect_system():
    """Detect system platform and specs"""
    sys_platform = platform.system()
    machine = platform.machine()
    ram_gb = psutil.virtual_memory().total / (1024 ** 3)

    # Detect if Mac M1/M2/M3 (Apple Silicon)
    is_mac_arm = sys_platform == "Darwin" and machine == "arm64"

    # Detect if low RAM (< 12GB)
    is_low_ram = ram_gb < 12

    return {
        "platform": sys_platform,
        "machine": machine,
        "ram_gb": ram_gb,
        "is_mac_arm": is_mac_arm,
        "is_low_ram": is_low_ram
    }

SYSTEM_INFO = detect_system()

# ============================================
# Model Profile (Rollback Support)
# ============================================

class ModelProfile(Enum):
    """Model profile selection for easy rollback"""
    LEGACY = "legacy"       # Whisper small/medium + Qwen 2.5
    OPTIMIZED = "optimized" # Whisper large-v3-turbo + Gemma 4

# Set via env: MODEL_PROFILE=legacy python app.py
try:
    ACTIVE_PROFILE = ModelProfile(os.getenv("MODEL_PROFILE", "optimized"))
except ValueError:
    ACTIVE_PROFILE = ModelProfile.OPTIMIZED

# ============================================
# Whisper Configuration (Auto-optimized)
# ============================================

@dataclass
class TranscriptionConfig:
    """Faster-Whisper configuration (profile-aware).

    OPTIMIZED: large-v3-turbo on GPU float16, auto language detect
    LEGACY   : small/medium, int8 on low RAM, hardcoded vi
    """

    # Model: large-v3-turbo (~3GB VRAM float16) for optimized, small/medium for legacy
    model: str = field(default_factory=lambda:
        "large-v3-turbo" if ACTIVE_PROFILE == ModelProfile.OPTIMIZED
        else ("small" if SYSTEM_INFO["is_low_ram"] or SYSTEM_INFO["is_mac_arm"] else "medium")
    )

    # Device: Mac M1 CPU, otherwise CUDA (auto-fallback to CPU)
    device: str = field(default_factory=lambda:
        "cpu" if SYSTEM_INFO["is_mac_arm"]
        else "cuda"
    )

    # Compute type: float16 on GPU (4050), int8 on Mac ARM
    compute_type: str = field(default_factory=lambda:
        "int8" if SYSTEM_INFO["is_mac_arm"]
        else "float16"
    )

    # Language: None = auto-detect (required for Việt-Nhật code-switching)
    language: Optional[str] = field(default_factory=lambda:
        None if ACTIVE_PROFILE == ModelProfile.OPTIMIZED
        else "vi"
    )

    beam_size: int = 5
    vad_filter: bool = True

    # Bilingual prompt for marketing F&B Việt-Nhật meetings
    initial_prompt: str = field(default_factory=lambda:
        (
            "Cuộc họp marketing F&B song ngữ Việt-Nhật. "
            "Thuật ngữ: phở, bún, bánh mì, ramen (ラーメン), sushi (寿司), "
            "マーケティング (marketing), 売上 (doanh thu), キャンペーン (campaign), "
            "ターゲット (target), 顧客 (khách hàng). "
            "Tên riêng giữ nguyên. Có chuyển đổi ngôn ngữ giữa tiếng Việt và tiếng Nhật."
        ) if ACTIVE_PROFILE == ModelProfile.OPTIMIZED
        else (
            "Cuộc họp công ty F&B bằng tiếng Việt, "
            "có từ tiếng Nhật về thực phẩm như phở, bún, ramen (ラーメン), sushi (寿司)."
        )
    )

    # Workers: reduce on low RAM
    num_workers: int = field(default_factory=lambda:
        2 if SYSTEM_INFO["is_low_ram"] else 4
    )

# ============================================
# Qwen LLM Configuration (Auto-optimized)
# ============================================

@dataclass
class SummarizationConfig:
    """LLM summarization configuration (profile-aware).

    OPTIMIZED: Gemma 4 E4B (~4GB VRAM, 140+ languages, native Việt-Nhật)
    LEGACY   : Qwen 2.5 3B/7B via Ollama
    """

    # Model: Gemma 4 E4B for optimized (fits 6GB VRAM), Qwen 2.5 for legacy
    model: str = field(default_factory=lambda:
        "gemma4:e4b" if ACTIVE_PROFILE == ModelProfile.OPTIMIZED
        else ("qwen2.5:3b" if SYSTEM_INFO["is_low_ram"] or SYSTEM_INFO["is_mac_arm"] else "qwen2.5:7b")
    )

    # Lower temperature = faster, more deterministic
    temperature: float = 0.2

    # Gemma 4 supports longer context; keep 4000 for both profiles on GPU
    max_tokens: int = field(default_factory=lambda:
        4000 if ACTIVE_PROFILE == ModelProfile.OPTIMIZED
        else (2000 if SYSTEM_INFO["is_low_ram"] else 4000)
    )

    base_url: str = "http://localhost:11434"

@dataclass
class FFmpegConfig:
    """FFmpeg preprocessing configuration - SPEED OPTIMIZED"""
    sample_rate: int = 16000
    channels: int = 1
    # loudnorm disabled = 2x faster (was taking 30-60s)
    normalize: bool = False
    # silence removal disabled = faster
    remove_silence: bool = False

@dataclass
class AppConfig:
    """Application configuration (auto-optimized per platform)"""
    name: str = "Voicemeet_sum"
    version: str = "1.0.0"
    language: str = "vi"

    # Paths
    base_dir: Path = Path(__file__).parent.parent
    output_dir: Path = base_dir / "output"
    models_cache: Path = base_dir / "models"
    logs_dir: Path = base_dir / "logs"
    temp_dir: Path = base_dir / "temp"

    # Performance (auto-tuned based on RAM)
    max_audio_length: int = 7200  # 2 hours in seconds

    # Chunk size: smaller for low RAM
    chunk_size: int = field(default_factory=lambda:
        8192 if SYSTEM_INFO["is_low_ram"] else 15000
    )

    num_workers: int = field(default_factory=lambda:
        2 if SYSTEM_INFO["is_low_ram"] else 4
    )

    # Max file size: 50MB for Mac M1 8GB, 2GB for high-end systems
    max_file_size: int = field(default_factory=lambda:
        50 * 1024 * 1024 if SYSTEM_INFO["is_low_ram"]  # 50 MB
        else 2 * 1024 * 1024 * 1024  # 2 GB
    )

    # Output
    output_formats: list = None
    include_metadata: bool = True

    def __post_init__(self):
        """Initialize paths and create directories"""
        if self.output_formats is None:
            self.output_formats = ["txt", "docx"]  # Added DOCX support

        # Create necessary directories
        self.output_dir.mkdir(exist_ok=True)
        self.models_cache.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

# Global configuration instances (auto-configured)
TRANSCRIPTION = TranscriptionConfig()
SUMMARIZATION = SummarizationConfig()
FFMPEG = FFmpegConfig()
APP = AppConfig()

# ============================================
# Runtime Info & Diagnostics
# ============================================

def print_config_info():
    """Print current configuration for debugging"""
    print("\n" + "="*60)
    print("🔧 VOICEMEET_SUM CONFIGURATION")
    print("="*60)
    print(f"Platform:        {SYSTEM_INFO['platform']} ({SYSTEM_INFO['machine']})")
    print(f"RAM:            {SYSTEM_INFO['ram_gb']:.1f} GB")
    print(f"Mac M1 Mode:    {SYSTEM_INFO['is_mac_arm']}")
    print(f"Low RAM Mode:   {SYSTEM_INFO['is_low_ram']}")
    print(f"Model Profile:  {ACTIVE_PROFILE.value.upper()} (set MODEL_PROFILE env to change)")
    print("-"*60)
    print(f"Whisper Model:  {TRANSCRIPTION.model}")
    print(f"Whisper Device: {TRANSCRIPTION.device}")
    print(f"Compute Type:   {TRANSCRIPTION.compute_type}")
    print(f"Language:       {TRANSCRIPTION.language or 'auto-detect'}")
    print(f"Workers:        {TRANSCRIPTION.num_workers}")
    print("-"*60)
    print(f"LLM Model:      {SUMMARIZATION.model}")
    print(f"Max Tokens:     {SUMMARIZATION.max_tokens}")
    print("-"*60)
    print(f"Chunk Size:     {APP.chunk_size}")
    print(f"Max File Size:  {APP.max_file_size / (1024*1024):.0f} MB")
    print(f"Output Formats: {', '.join(APP.output_formats)}")
    print("="*60 + "\n")

def load_config_from_file(config_path: Optional[Path] = None):
    """
    Load configuration from INI file if needed
    For now, using auto-detected configs
    """
    pass

# ============================================
# Auto-print config on import (for debugging)
# ============================================
if os.getenv("DEBUG_CONFIG", "").lower() == "true":
    print_config_info()
