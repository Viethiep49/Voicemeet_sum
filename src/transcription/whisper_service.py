"""
Faster-Whisper transcription service
"""
import os
import sys
import warnings
from pathlib import Path
from typing import Optional, Callable
import time

# Suppress all warnings before importing faster_whisper
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress stderr during import to catch cuDNN warnings
_original_stderr = sys.stderr
try:
    import io
    sys.stderr = io.StringIO()
    from faster_whisper import WhisperModel
    sys.stderr = _original_stderr
except:
    sys.stderr = _original_stderr
    from faster_whisper import WhisperModel

from ..utils.logger import logger
from config.settings import TRANSCRIPTION, APP

# Fix cuDNN DLL path for Windows and suppress warnings
def _setup_cudnn_path():
    """Add PyTorch lib path to PATH for cuDNN DLLs"""
    if sys.platform == 'win32':
        try:
            import torch
            torch_lib = os.path.join(os.path.dirname(torch.__file__), 'lib')
            if os.path.exists(torch_lib):
                current_path = os.environ.get('PATH', '')
                if torch_lib not in current_path:
                    os.environ['PATH'] = torch_lib + os.pathsep + current_path
                    logger.debug(f"Added PyTorch lib to PATH: {torch_lib}")
            
            # Suppress cuDNN warnings
            import warnings
            warnings.filterwarnings('ignore', message='.*cudnn.*')
            warnings.filterwarnings('ignore', message='.*cuDNN.*')
        except ImportError:
            pass

# Setup cuDNN path on import
_setup_cudnn_path()


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
        """Load Whisper model into memory with CUDA support"""
        if self.model is not None:
            logger.info("Model already loaded")
            return
        
        # Setup cuDNN path BEFORE any imports
        _setup_cudnn_path()
        
        logger.info(f"Loading Whisper model: {self.config.model}")
        logger.info(f"Device: {self.config.device}, Compute type: {self.config.compute_type}")
        
        # Check CUDA using ctranslate2 (faster-whisper uses this)
        device = self.config.device
        compute_type = self.config.compute_type
        
        if device == "cuda":
            try:
                import ctranslate2
                cuda_devices = ctranslate2.get_cuda_device_count()
                if cuda_devices > 0:
                    device = "cuda"
                    compute_type = self.config.compute_type
                    # Get GPU name from torch if available
                    try:
                        import torch
                        if torch.cuda.is_available():
                            logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
                    except:
                        logger.info(f"Using CUDA (devices: {cuda_devices})")
                else:
                    logger.warning("No CUDA devices found, using CPU")
                    device = "cpu"
                    compute_type = "float32"
            except ImportError:
                logger.warning("ctranslate2 not available, trying direct CUDA load...")
                device = "cuda"  # Try anyway
                compute_type = self.config.compute_type
        
        start_time = time.time()
        
        # Try loading with requested device
        try:
            self.model = WhisperModel(
                self.config.model,
                device=device,
                compute_type=compute_type,
                download_root=str(self.model_path.parent)
            )
            
            load_time = time.time() - start_time
            logger.info(f"Model loaded on {device.upper()} in {load_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to load model on {device}: {e}")
            # Try CPU fallback if CUDA fails
            if device == "cuda":
                logger.warning("CUDA load failed, trying CPU fallback...")
                try:
                    self.model = WhisperModel(
                        self.config.model,
                        device="cpu",
                        compute_type="float32",
                        download_root=str(self.model_path.parent)
                    )
                    load_time = time.time() - start_time
                    logger.warning(f"Model loaded on CPU (fallback) in {load_time:.2f}s")
                except Exception as e2:
                    logger.error(f"CPU fallback also failed: {e2}")
                    raise
            else:
                raise
    
    def transcribe(
        self,
        audio_path: Path,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> str:
        """
        Transcribe audio file with cuDNN warning suppression
        
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
        info = None  # Initialize info variable
        
        try:
            # Suppress stderr during transcription to hide cuDNN warnings
            import io
            _stderr_backup = sys.stderr
            _suppressed_stderr = None
            try:
                _suppressed_stderr = io.StringIO()
                sys.stderr = _suppressed_stderr
                
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
                logger.info("Starting segment processing (cuDNN warnings suppressed)...")
                
                # Process segments (keep stderr suppressed during iteration)
                # Note: cuDNN warnings may appear but won't crash the app
                last_update = 0
                segment_count = 0
                last_log_time = time.time()
                try:
                    logger.info("Iterating segments (cuDNN warnings may appear but are harmless)...")
                    logger.info("This may take several minutes for long audio files...")
                    logger.info("Processing will continue in background - please wait...")
                    
                    for idx, segment in enumerate(segments_iter):
                        try:
                            segments.append({
                                'start': segment.start,
                                'end': segment.end,
                                'text': segment.text.strip()
                            })
                            segment_count += 1
                            
                            # Log every 100 segments OR every 30 seconds
                            current_time = time.time()
                            if (idx > 0 and idx % 100 == 0) or (current_time - last_log_time >= 30):
                                logger.info(f"Processed {segment_count} segments ({segment.end/60:.1f} min of audio)...")
                                last_log_time = current_time
                            
                            # Progress callback (update every 2 seconds of audio to keep connection alive)
                            if progress_callback and info.duration:
                                try:
                                    current_time = segment.end
                                    # Update more frequently (every 2 seconds) to prevent timeout
                                    if current_time - last_update >= 2.0 or idx == 0 or idx % 10 == 0:
                                        estimated_progress = min(75.0, (current_time / info.duration) * 75.0)
                                        elapsed = time.time() - start_time
                                        speed = current_time / elapsed if elapsed > 0 else 0
                                        progress_callback(
                                            10 + estimated_progress,  # 10-85% range
                                            f"Transcribing... {current_time/60:.1f}/{info.duration/60:.1f} min (speed: {speed:.1f}x)"
                                        )
                                        last_update = current_time
                                        # Force flush to ensure progress is sent
                                        try:
                                            sys.stdout.flush()
                                        except:
                                            pass
                                except Exception as e:
                                    logger.warning(f"Progress callback error (non-critical): {e}")
                        except Exception as e:
                            logger.warning(f"Error processing segment {idx}: {e}")
                            # Continue with next segment - don't crash on single segment error
                            continue
                    
                    logger.info(f"Processed {segment_count} segments successfully")
                except StopIteration:
                    # Normal end of iteration
                    logger.info(f"Segment iteration completed ({segment_count} segments)")
                except Exception as e:
                    logger.error(f"Error iterating segments: {e}", exc_info=True)
                    # If we have some segments, continue with what we have
                    if not segments:
                        raise
                    logger.warning(f"Continuing with {len(segments)} segments despite error")
            finally:
                # Restore stderr after processing all segments
                sys.stderr = _stderr_backup
                if _suppressed_stderr is not None:
                    try:
                        _suppressed_stderr.close()
                    except:
                        pass
            
            # Combine segments
            if not segments:
                logger.warning("No segments processed")
                return ""
            
            full_text = self._combine_segments(segments)
            
            transcribe_time = time.time() - start_time
            logger.info(f"Transcription completed in {transcribe_time:.2f}s")
            logger.info(f"Total segments: {len(segments)}")
            
            # Calculate speed if info is available
            try:
                if info is not None and hasattr(info, 'duration') and info.duration and transcribe_time > 0:
                    logger.info(f"Speed: {info.duration/transcribe_time:.1f}x realtime")
            except Exception as e:
                logger.debug(f"Could not calculate speed: {e}")
            
            if progress_callback:
                progress_callback(85.0, "Transcription completed")
            
            return full_text
            
        except KeyboardInterrupt:
            logger.warning("Transcription interrupted by user")
            raise
        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            # Try to return partial result if we have some segments
            if segments:
                logger.warning(f"Returning partial transcript ({len(segments)} segments)")
                return self._combine_segments(segments)
            raise RuntimeError(f"Transcription failed: {e}") from e
    
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