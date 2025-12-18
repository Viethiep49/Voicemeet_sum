"""
Configuration settings for Voicemeet_sum
Auto-detects platform and optimizes for Mac M1 8GB or Windows/Linux GPU
"""
import os
import platform
import psutil
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
# Whisper Configuration (Auto-optimized)
# ============================================

@dataclass
class TranscriptionConfig:
    """Faster-Whisper configuration (auto-optimized per platform)"""

    # Model selection based on RAM
    model: str = field(default_factory=lambda:
        "small" if SYSTEM_INFO["is_low_ram"] or SYSTEM_INFO["is_mac_arm"]
        else "medium"
    )

    # Device selection: Mac M1 uses CPU, Windows/Linux use CUDA if available
    device: str = field(default_factory=lambda:
        "cpu" if SYSTEM_INFO["is_mac_arm"]
        else "cuda"  # Will auto-fallback to CPU if CUDA not available
    )

    # Compute type: int8 for low RAM, float16 for GPU
    compute_type: str = field(default_factory=lambda:
        "int8" if SYSTEM_INFO["is_low_ram"] or SYSTEM_INFO["is_mac_arm"]
        else "float16"
    )

    language: str = "vi"
    beam_size: int = 5
    vad_filter: bool = True

    # Multi-language prompt (Việt + Nhật)
    initial_prompt: str = (
        "Cuộc họp công ty F&B bằng tiếng Việt, "
        "có từ tiếng Nhật về thực phẩm như phở, bún, ramen (ラーメン), sushi (寿司)."
    )

    # Mac M1 specific: reduce workers to save RAM
    num_workers: int = field(default_factory=lambda:
        2 if SYSTEM_INFO["is_low_ram"] else 4
    )

# ============================================
# Qwen LLM Configuration (Auto-optimized)
# ============================================

@dataclass
class SummarizationConfig:
    """Qwen configuration (auto-optimized per platform)"""

    # Model selection: 3B for low RAM, 7B for high RAM
    model: str = field(default_factory=lambda:
        "qwen2.5:3b" if SYSTEM_INFO["is_low_ram"] or SYSTEM_INFO["is_mac_arm"]
        else "qwen2.5:7b"
    )

    temperature: float = 0.3

    # Reduce max tokens on low RAM systems
    max_tokens: int = field(default_factory=lambda:
        2000 if SYSTEM_INFO["is_low_ram"] else 4000
    )

    base_url: str = "http://localhost:11434"

@dataclass
class FFmpegConfig:
    """FFmpeg preprocessing configuration"""
    sample_rate: int = 16000
    channels: int = 1
    normalize: bool = True
    remove_silence: bool = True

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
    print("-"*60)
    print(f"Whisper Model:  {TRANSCRIPTION.model}")
    print(f"Whisper Device: {TRANSCRIPTION.device}")
    print(f"Compute Type:   {TRANSCRIPTION.compute_type}")
    print(f"Workers:        {TRANSCRIPTION.num_workers}")
    print("-"*60)
    print(f"Qwen Model:     {SUMMARIZATION.model}")
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

