"""
Configuration settings for Voicemeet_sum
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class TranscriptionConfig:
    """Faster-Whisper configuration"""
    model: str = "medium"
    device: str = "cuda"  # cuda or cpu
    compute_type: str = "float16"  # float16, float32, int8
    language: str = "vi"
    beam_size: int = 5
    vad_filter: bool = True
    initial_prompt: str = "Cuộc họp công ty F&B bằng tiếng Việt, có từ tiếng Nhật về thực phẩm như phở, bún, hàng."

@dataclass
class SummarizationConfig:
    """Qwen configuration"""
    model: str = "qwen2.5:7b"
    temperature: float = 0.3
    max_tokens: int = 2000
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
    """Application configuration"""
    name: str = "Voicemeet_sum"
    version: str = "1.0.0"
    language: str = "vi"
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent
    output_dir: Path = base_dir / "output"
    models_cache: Path = base_dir / "models"
    logs_dir: Path = base_dir / "logs"
    
    # Performance
    max_audio_length: int = 7200  # 2 hours in seconds
    chunk_size: int = 4000  # For text chunking
    num_workers: int = 4
    
    # Output
    output_formats: list = None
    include_metadata: bool = True
    
    def __post_init__(self):
        """Initialize paths and create directories"""
        if self.output_formats is None:
            self.output_formats = ["txt"]
        
        # Create necessary directories
        self.output_dir.mkdir(exist_ok=True)
        self.models_cache.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

# Global configuration instances
TRANSCRIPTION = TranscriptionConfig()
SUMMARIZATION = SummarizationConfig()
FFMPEG = FFmpegConfig()
APP = AppConfig()

def load_config_from_file(config_path: Optional[Path] = None):
    """
    Load configuration from INI file if needed
    For now, using hardcoded configs above
    """
    pass

