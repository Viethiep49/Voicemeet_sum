"""
Faster-Whisper transcription service
"""
from pathlib import Path
from typing import Iterator, Optional, Callable
import time

from faster_whisper import WhisperModel

from ..utils.logger import logger
from config.settings import TRANSCRIPTION, APP


class WhisperService:
    """Handle transcription using Faster-Whisper"""
    
    def __init__(self, config=None):
        """
        Initialize Whisper service
        
        Args:
            config: TranscriptionConfig instance
        """
        self.config = config or TRANSCRIPTION
        self.model = None
        self.model_path = APP.models_cache / self.config.model
        
    def load_model(self):
        """Load Whisper model into memory"""
        if self.model is not None:
            logger.info("Model already loaded")
            return
        
        logger.info(f"Loading Whisper model: {self.config.model}")
        start_time = time.time()
        
        try:
            self.model = WhisperModel(
                self.config.model,
                device=self.config.device,
                compute_type=self.config.compute_type,
                download_root=str(self.model_path.parent)
            )
            
            load_time = time.time() - start_time
            logger.info(f"Model loaded in {load_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def transcribe(
        self,
        audio_path: Path,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> str:
        """
        Transcribe audio file
        
        Args:
            audio_path: Path to preprocessed audio file
            progress_callback: Callback function(progress: float, status: str)
            
        Returns:
            Full transcript text
        """
        if self.model is None:
            self.load_model()
        
        logger.info(f"Starting transcription: {audio_path.name}")
        start_time = time.time()
        
        segments = []
        
        try:
            # Transcribe with segments
            segments_iter, info = self.model.transcribe(
                str(audio_path),
                beam_size=self.config.beam_size,
                language=self.config.language,
                vad_filter=self.config.vad_filter,
                initial_prompt=self.config.initial_prompt,
                word_timestamps=False
            )
            
            logger.info(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")
            
            # Process segments
            for idx, segment in enumerate(segments_iter):
                segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip()
                })
                
                # Progress callback
                if progress_callback:
                    # Estimate progress based on segment times
                    # This is approximate since we don't know total duration upfront
                    if info.duration:
                        estimated_progress = min(80.0, (segment.end / info.duration) * 80.0)
                        progress_callback(estimated_progress, f"Đang xử lý... ({len(segments)} đoạn)")
            
            # Combine segments
            full_text = self._combine_segments(segments)
            
            transcribe_time = time.time() - start_time
            logger.info(f"Transcription completed in {transcribe_time:.2f}s")
            
            if progress_callback:
                progress_callback(80.0, "Hoàn thành transcription")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise RuntimeError(f"Transcription thất bại: {e}")
    
    def _combine_segments(self, segments: list) -> str:
        """
        Combine segments into full text
        
        Args:
            segments: List of segment dictionaries
            
        Returns:
            Combined text
        """
        if not segments:
            return ""
        
        # Simple combination with newlines
        lines = []
        prev_end = 0
        
        for seg in segments:
            # Add line break if there's a significant gap
            if seg['start'] - prev_end > 3.0:  # More than 3 seconds gap
                lines.append("")
            
            lines.append(seg['text'])
            prev_end = seg['end']
        
        return '\n'.join(lines).strip()
    
    def unload_model(self):
        """Unload model from memory to free resources"""
        if self.model is not None:
            logger.info("Unloading model")
            self.model = None

