"""
Faster-Whisper transcription service - Robust Version
"""
import os
import sys
import warnings
from pathlib import Path
from typing import Optional, Callable
import time

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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

def _setup_cudnn_path():
    """Setup cuDNN path"""
    if sys.platform == 'win32':
        try:
            import torch
            torch_lib = os.path.join(os.path.dirname(torch.__file__), 'lib')
            if os.path.exists(torch_lib):
                current_path = os.environ.get('PATH', '')
                if torch_lib not in current_path:
                    os.environ['PATH'] = torch_lib + os.pathsep + current_path
            import warnings
            warnings.filterwarnings('ignore', message='.*cudnn.*')
        except:
            pass

_setup_cudnn_path()

class WhisperService:
    """Whisper transcription with robust error handling"""
    
    def __init__(self, config=None):
        self.config = config or TRANSCRIPTION
        self.model = None
        self.model_path = APP.models_cache / self.config.model
        
    def load_model(self):
        """Load Whisper model"""
        if self.model is not None:
            return
        
        _setup_cudnn_path()
        
        logger.info(f"Loading Whisper model: {self.config.model}")
        
        device = self.config.device
        compute_type = self.config.compute_type
        
        if device == "cuda":
            try:
                import ctranslate2
                if ctranslate2.get_cuda_device_count() > 0:
                    try:
                        import torch
                        if torch.cuda.is_available():
                            logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
                    except:
                        pass
                else:
                    logger.warning("No CUDA, using CPU")
                    device = "cpu"
                    compute_type = "float32"
            except:
                pass
        
        start_time = time.time()
        
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
            if device == "cuda":
                logger.warning("CUDA failed, trying CPU...")
                self.model = WhisperModel(
                    self.config.model,
                    device="cpu",
                    compute_type="float32",
                    download_root=str(self.model_path.parent)
                )
                logger.warning("Model loaded on CPU (fallback)")
            else:
                raise
    
    def transcribe(
        self,
        audio_path: Path,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> str:
        """
        Transcribe with robust segment processing
        """
        if self.model is None:
            self.load_model()
        
        logger.info(f"Starting transcription: {audio_path.name}")
        start_time = time.time()
        
        try:
            # Suppress stderr completely
            import io
            _stderr_backup = sys.stderr
            sys.stderr = io.StringIO()
            
            # Step 1: Get segments iterator
            logger.info("Calling model.transcribe()...")
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
                condition_on_previous_text=True
            )
            
            logger.info(f"Language: {info.language} ({info.language_probability:.2f})")
            logger.info(f"Duration: {info.duration:.2f}s")
            
            # Step 2: Convert to list immediately (safer than iterating)
            logger.info("Converting segments to list...")
            segments_list = []
            
            try:
                # Use list() to consume iterator - faster and safer
                raw_segments = list(segments_iter)
                logger.info(f"Got {len(raw_segments)} raw segments")
                
                # Convert to our format
                for seg in raw_segments:
                    try:
                        segments_list.append({
                            'start': seg.start,
                            'end': seg.end,
                            'text': seg.text.strip()
                        })
                    except:
                        continue
                
            except Exception as e:
                logger.error(f"Error converting segments: {e}")
                # If list() fails, try manual iteration with timeout
                logger.info("Trying manual iteration...")
                segment_count = 0
                last_update = time.time()
                
                for seg in segments_iter:
                    try:
                        segments_list.append({
                            'start': seg.start,
                            'end': seg.end,
                            'text': seg.text.strip()
                        })
                        segment_count += 1
                        
                        # Progress update every 1 second
                        current = time.time()
                        if progress_callback and current - last_update >= 1.0:
                            if info.duration:
                                pct = min(75, (seg.end / info.duration) * 75)
                                progress_callback(10 + pct, f"Processing... {seg.end/60:.1f} min")
                            last_update = current
                        
                        # Safety: Break if taking too long
                        if time.time() - start_time > 600:  # 10 min timeout
                            logger.warning("Timeout, breaking")
                            break
                            
                    except StopIteration:
                        break
                    except Exception as e2:
                        logger.warning(f"Segment error: {e2}")
                        continue
            
            # Restore stderr
            sys.stderr = _stderr_backup
            
            logger.info(f"Processed {len(segments_list)} segments")
            
            if not segments_list:
                logger.error("No segments!")
                return ""
            
            # Combine
            full_text = self._combine_segments(segments_list)
            
            transcribe_time = time.time() - start_time
            logger.info(f"Completed in {transcribe_time:.2f}s")
            
            if info.duration:
                logger.info(f"Speed: {info.duration/transcribe_time:.1f}x")
            
            if progress_callback:
                progress_callback(85.0, "Transcription completed")
            
            return full_text
            
        except KeyboardInterrupt:
            sys.stderr = _stderr_backup
            logger.warning("Interrupted")
            raise
        except Exception as e:
            sys.stderr = _stderr_backup
            logger.error(f"FATAL: {e}", exc_info=True)
            raise RuntimeError(f"Transcription failed: {e}")
    
    def _combine_segments(self, segments: list) -> str:
        """Combine segments into text"""
        if not segments:
            return ""
        
        lines = []
        prev_end = 0
        
        for seg in segments:
            if seg['start'] - prev_end > 3.0:
                lines.append("")
            lines.append(seg['text'])
            prev_end = seg['end']
        
        return '\n'.join(lines).strip()
    
    def unload_model(self):
        """Unload model"""
        if self.model is not None:
            logger.info("Unloading model")
            del self.model
            self.model = None
            
            import gc
            gc.collect()
            
            if self.config.device == "cuda":
                try:
                    import torch
                    torch.cuda.empty_cache()
                except:
                    pass