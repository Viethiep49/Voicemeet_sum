"""
Main pipeline for meeting transcription and summarization
"""
from pathlib import Path
from typing import Optional, Callable, Tuple
from datetime import datetime

from ..transcription.audio_processor import AudioProcessor
from ..transcription.whisper_service import WhisperService
from ..summarization.qwen_service import QwenService
from ..utils.logger import logger
from ..utils.file_handler import (
    ensure_dir, save_text_file, generate_output_filename,
    is_valid_audio_file, get_file_size, format_file_size
)
from ..utils.text_processor import clean_text
from config.settings import APP, TRANSCRIPTION, SUMMARIZATION


class MeetingPipeline:
    """Main processing pipeline"""
    
    def __init__(self):
        """Initialize pipeline components"""
        self.audio_processor = AudioProcessor()
        self.whisper_service = WhisperService()
        self.qwen_service = QwenService()
        
    def process(
        self,
        audio_file: Path,
        progress_callback: Optional[Callable[[float, str], None]] = None,
        remove_temp: bool = True
    ) -> Tuple[Path, Path]:
        """
        Process audio file: preprocess, transcribe, summarize
        
        Args:
            audio_file: Input audio file path
            progress_callback: Callback function(progress: float, status: str)
            remove_temp: Whether to remove temporary files
            
        Returns:
            Tuple of (transcript_path, summary_path)
        """
        logger.info(f"Starting pipeline: {audio_file.name}")
        start_time = datetime.now()
        
        # Validate input file
        is_valid, error_msg = is_valid_audio_file(audio_file)
        if not is_valid:
            raise ValueError(error_msg)
        
        file_size = get_file_size(audio_file)
        logger.info(f"Input file: {audio_file.name} ({format_file_size(file_size)})")
        
        try:
            # Step 1: Preprocess audio
            if progress_callback:
                progress_callback(5, "Đang chuẩn bị audio...")
            
            logger.info("Step 1/3: Preprocessing audio")
            preprocessed_path = self.audio_processor.preprocess(audio_file)
            
            if progress_callback:
                progress_callback(10, "Đang chuyển đổi speech sang text...")
            
            # Step 2: Transcribe
            logger.info("Step 2/3: Transcribing")
            transcript = self.whisper_service.transcribe(
                preprocessed_path,
                progress_callback=progress_callback
            )
            
            # Clean transcript
            transcript = clean_text(transcript)
            
            if progress_callback:
                progress_callback(80, "Đang tạo tóm tắt...")
            
            # Step 3: Summarize
            logger.info("Step 3/3: Summarizing")
            summary = self.qwen_service.summarize(
                transcript,
                progress_callback=progress_callback
            )
            
            # Save outputs
            logger.info("Saving outputs")
            transcript_path, summary_path = self._save_outputs(audio_file.stem, transcript, summary)
            
            if progress_callback:
                progress_callback(100, "Hoàn thành!")
            
            # Cleanup
            if remove_temp:
                from ..utils.file_handler import clean_temp_files
                clean_temp_files(preprocessed_path.parent)
                if preprocessed_path.exists():
                    preprocessed_path.unlink()
            
            # Log completion
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Pipeline completed in {duration:.2f}s")
            
            return transcript_path, summary_path
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
        finally:
            # Unload Whisper model to free memory
            self.whisper_service.unload_model()
    
    def _save_outputs(
        self,
        base_name: str,
        transcript: str,
        summary: str
    ) -> Tuple[Path, Path]:
        """
        Save transcript and summary to files
        
        Args:
            base_name: Base filename
            transcript: Transcript text
            summary: Summary text
            
        Returns:
            Tuple of (transcript_path, summary_path)
        """
        ensure_dir(APP.output_dir)
        
        # Generate filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        transcript_file = APP.output_dir / f"transcript_{base_name}_{timestamp}.txt"
        summary_file = APP.output_dir / f"summary_{base_name}_{timestamp}.txt"
        
        # Add metadata to transcript
        full_transcript = self._format_transcript(transcript)
        
        # Save files
        save_text_file(full_transcript, transcript_file)
        save_text_file(summary, summary_file)
        
        logger.info(f"Transcript saved: {transcript_file.name}")
        logger.info(f"Summary saved: {summary_file.name}")
        
        return transcript_file, summary_file
    
    def _format_transcript(self, text: str) -> str:
        """
        Format transcript with metadata
        
        Args:
            text: Raw transcript
            
        Returns:
            Formatted transcript with header
        """
        header = "# TRANSCRIPT CUỘC HỌP\n\n"
        header += f"Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        header += f"Độ dài: {len(text)} ký tự\n"
        header += "-" * 80 + "\n\n"
        
        return header + text
    
    def get_stats(self) -> dict:
        """
        Get pipeline statistics
        
        Returns:
            Dictionary with stats
        """
        return {
            "transcription_config": {
                "model": TRANSCRIPTION.model,
                "device": TRANSCRIPTION.device,
                "compute_type": TRANSCRIPTION.compute_type
            },
            "summarization_config": {
                "model": SUMMARIZATION.model,
                "base_url": SUMMARIZATION.base_url
            },
            "output_dir": str(APP.output_dir)
        }

