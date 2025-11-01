"""
Audio preprocessing with FFmpeg
"""
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from ..utils.logger import logger
from config.settings import FFMPEG


class AudioProcessor:
    """Handle audio preprocessing with FFmpeg"""
    
    def __init__(self, config=None):
        """
        Initialize audio processor
        
        Args:
            config: FFmpegConfig instance
        """
        self.config = config or FFMPEG
        
    def preprocess(
        self,
        input_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Preprocess audio: resample, normalize, remove silence
        
        Args:
            input_path: Input audio file
            output_path: Output WAV file (auto-generated if None)
            
        Returns:
            Path to preprocessed file
        """
        if output_path is None:
            # Create temp file
            temp_dir = Path(tempfile.gettempdir()) / "voicemeet_sum"
            temp_dir.mkdir(exist_ok=True)
            output_path = temp_dir / f"preprocessed_{input_path.stem}.wav"
        
        logger.info(f"Preprocessing audio: {input_path.name}")
        
        # Build FFmpeg command
        cmd = self._build_ffmpeg_command(input_path, output_path)
        
        try:
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info(f"Audio preprocessed: {output_path.name}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise RuntimeError(f"Failed to preprocess audio: {e.stderr}")
        except FileNotFoundError:
            logger.error("FFmpeg not found. Please install FFmpeg.")
            raise RuntimeError("FFmpeg không được cài đặt")
    
    def _build_ffmpeg_command(
        self,
        input_path: Path,
        output_path: Path
    ) -> list:
        """
        Build FFmpeg command with filters
        
        Args:
            input_path: Input file
            output_path: Output file
            
        Returns:
            FFmpeg command list
        """
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output
            '-i', str(input_path),
            '-ar', str(self.config.sample_rate),  # Sample rate
            '-ac', str(self.config.channels),  # Channels
        ]
        
        # Apply audio filters
        filters = []
        
        if self.config.normalize:
            filters.append('loudnorm=I=-16:TP=-1.5:LRA=11')
        
        if self.config.remove_silence:
            filters.append('silenceremove=start_periods=1:start_silence=0.5:start_threshold=-50dB')
        
        if filters:
            cmd.extend(['-af', ','.join(filters)])
        
        cmd.append(str(output_path))
        
        return cmd
    
    def get_audio_info(self, file_path: Path) -> dict:
        """
        Get audio file information
        
        Args:
            file_path: Audio file path
            
        Returns:
            Dictionary with audio info
        """
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration,size,bit_rate',
            '-show_entries', 'stream=sample_rate,channels,codec_name',
            '-of', 'json',
            str(file_path)
        ]
        
        try:
            import json
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except:
            return {}

