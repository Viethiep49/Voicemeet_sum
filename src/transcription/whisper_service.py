"""
Faster-Whisper transcription service
"""
from pathlib import Path
from typing import Optional, Callable
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
                task="transcribe",
                vad_filter=self.config.vad_filter,
                vad_parameters=dict(
                    threshold=0.5,
                    min_speech_duration_ms=250,
                    min_silence_duration_ms=2000,
                    speech_pad_ms=400
                ),
                initial_prompt=self.config.initial_prompt,
                word_timestamps=False,
                condition_on_previous_text=True,
                compression_ratio_threshold=2.4,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6,
                language_detection_threshold=0.5,
                language_detection_segments=1
            )
            
            logger.info(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")
            logger.info(f"Audio duration: {info.duration:.2f}s")
            
            # Process segments
            last_update = 0
            for idx, segment in enumerate(segments_iter):
                segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip()
                })
                
                # Progress callback (update every 5 seconds of audio)
                if progress_callback and info.duration:
                    current_time = segment.end
                    if current_time - last_update >= 5.0 or idx == 0:
                        estimated_progress = min(75.0, (current_time / info.duration) * 75.0)
                        elapsed = time.time() - start_time
                        speed = current_time / elapsed if elapsed > 0 else 0
                        progress_callback(
                            10 + estimated_progress,  # 10-85% range
                            f"Transcribing... {current_time/60:.1f}/{info.duration/60:.1f} min (speed: {speed:.1f}x)"
                        )
                        last_update = current_time
            
            # Combine segments
            full_text = self._combine_segments(segments)
            
            transcribe_time = time.time() - start_time
            logger.info(f"Transcription completed in {transcribe_time:.2f}s")
            logger.info(f"Total segments: {len(segments)}")
            logger.info(f"Speed: {info.duration/transcribe_time:.1f}x realtime")
            
            if progress_callback:
                progress_callback(85.0, "Transcription completed")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise RuntimeError(f"Transcription failed: {e}")
    
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
            del self.model
            self.model = None
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Clear CUDA cache if using GPU
            if self.config.device == "cuda":
                try:
                    import torch
                    torch.cuda.empty_cache()
                    logger.info("CUDA cache cleared")
                except:
                    pass