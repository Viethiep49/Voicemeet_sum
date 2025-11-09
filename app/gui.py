"""
Gradio GUI for Voicemeet_sum - Simplified Version
"""
import sys
import os
import warnings
from pathlib import Path
from typing import Tuple, Optional
from contextlib import redirect_stderr, redirect_stdout
import io

# Suppress all warnings and cuDNN messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_LAUNCH_BLOCKING'] = '0'
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'  # Suppress cuDNN workspace warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

# Redirect stderr globally to suppress cuDNN messages
_original_stderr = sys.stderr
try:
    import io
    _devnull = io.StringIO()
    # Don't redirect immediately, will do it during processing
except:
    pass

# Suppress stderr for cuDNN messages
class SuppressStderr:
    """Context manager to suppress stderr output"""
    def __init__(self):
        self.original_stderr = None
        self.devnull = None
    
    def __enter__(self):
        self.original_stderr = sys.stderr
        try:
            self.devnull = open(os.devnull, 'w', encoding='utf-8')
            sys.stderr = self.devnull
        except:
            pass
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_stderr:
            sys.stderr = self.original_stderr
        if self.devnull:
            try:
                self.devnull.close()
            except:
                pass
        return False  # Don't suppress exceptions

import gradio as gr

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline.meeting_pipeline import MeetingPipeline
from src.utils.logger import setup_logger, logger
from src.utils.file_handler import is_valid_audio_file, format_file_size, get_file_size
from config.settings import APP

# Setup logger
setup_logger("voicemeet_sum", APP.logs_dir)

# Initialize pipeline
pipeline = MeetingPipeline()


def process_audio(audio_file) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Process audio file and return results with robust error handling
    """
    try:
        if audio_file is None:
            return "Vui long chon file audio", None, None
        
        # Get file path
        try:
            if hasattr(audio_file, 'name'):
                audio_path = Path(audio_file.name)
            elif isinstance(audio_file, (str, Path)):
                audio_path = Path(audio_file)
            else:
                return "Loi: Khong doc duoc file", None, None
        except Exception as e:
            logger.error(f"File path error: {e}")
            return f"Loi khi doc file: {str(e)}", None, None
        
        # Validate file exists
        if not audio_path.exists():
            return f"Loi: File khong ton tai: {audio_path}", None, None
        
        # Validate file type
        is_valid, error_msg = is_valid_audio_file(audio_path)
        if not is_valid:
            return f"Loi: {error_msg}", None, None
        
        # Process with error handling and suppress cuDNN warnings
        try:
            # Progress tracking for Gradio - update frequently to prevent timeout
            _progress_state = {"last_update": 0, "time": 0}
            
            def progress_callback(progress: float, status: str):
                """Progress callback that updates Gradio frequently"""
                import time
                current_time = time.time()
                # Update every 0.5% or every 2 seconds to keep connection alive
                if progress - _progress_state["last_update"] >= 0.5 or current_time - _progress_state.get("time", 0) >= 2.0:
                    _progress_state["last_update"] = progress
                    _progress_state["time"] = current_time
                    # Log progress to keep connection alive
                    logger.info(f"Progress: {progress:.1f}% - {status}")
                    # Force flush to ensure log is written
                    try:
                        import sys
                        sys.stdout.flush()
                    except:
                        pass
            
            logger.info(f"Starting processing: {audio_path.name}")
            
            # Process with stderr suppression and robust error handling
            import io
            _stderr_backup = sys.stderr
            _suppressed_stderr = None
            try:
                # Suppress stderr during entire processing
                _suppressed_stderr = io.StringIO()
                sys.stderr = _suppressed_stderr
                
                logger.info(f"Processing started, suppressing stderr")
                transcript_path, summary_path = pipeline.process(
                    audio_file=audio_path,
                    progress_callback=progress_callback
                )
                logger.info(f"Processing completed successfully")
            except KeyboardInterrupt:
                logger.warning("Processing interrupted")
                raise
            except MemoryError:
                logger.error("Out of memory during processing")
                raise
            except Exception as e:
                logger.error(f"Processing exception: {e}", exc_info=True)
                raise
            finally:
                # Always restore stderr
                try:
                    sys.stderr = _stderr_backup
                    if _suppressed_stderr is not None:
                        _suppressed_stderr.close()
                except:
                    pass
            
            # Verify outputs exist
            if not transcript_path.exists() or not summary_path.exists():
                return "Loi: Khong tao duoc output files", None, None
            
            # Get file info
            try:
                transcript_size = format_file_size(get_file_size(transcript_path))
                summary_size = format_file_size(get_file_size(summary_path))
            except:
                transcript_size = "N/A"
                summary_size = "N/A"
            
            success_msg = (
                f"Hoan thanh!\n\n"
                f"Transcript: {transcript_path.name} ({transcript_size})\n"
                f"Summary: {summary_path.name} ({summary_size})\n\n"
                f"Luu tai: {APP.output_dir}"
            )
            
            logger.info(f"Processing completed successfully")
            return success_msg, str(transcript_path), str(summary_path)
            
        except KeyboardInterrupt:
            logger.warning("Processing interrupted by user")
            return "Da dung lai boi nguoi dung", None, None
        except MemoryError:
            logger.error("Out of memory")
            return "Loi: Het bo nho. Vui long dong cac ung dung khac va thu lai", None, None
        except Exception as e:
            logger.error(f"Processing error: {e}", exc_info=True)
            error_msg = str(e)
            # Truncate long error messages
            if len(error_msg) > 200:
                error_msg = error_msg[:200] + "..."
            return f"Loi khi xu ly: {error_msg}", None, None
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return f"Loi khong mong doi: {str(e)}", None, None


def create_interface():
    """Create simplified Gradio interface"""
    
    with gr.Blocks(title="Voicemeet_sum") as app:
        # Header
        gr.Markdown("# Voicemeet_sum\nChuyen doi audio cuoc hop thanh van ban")
        
        # File upload
        audio_input = gr.File(
            label="Chon file audio",
            file_types=[".m4a", ".mp4", ".mp3", ".wav", ".flac"]
        )
        
        # Process button
        process_btn = gr.Button("Bat dau xu ly", variant="primary", size="lg")
        
        # Status output
        status_output = gr.Textbox(
            label="Trang thai",
            lines=4,
            interactive=False
        )
        
        # Output files
        with gr.Row():
            transcript_download = gr.File(label="Transcript", visible=True)
            summary_download = gr.File(label="Summary", visible=True)
        
        # Process button click with queue to prevent timeout
        process_btn.click(
            fn=process_audio,
            inputs=[audio_input],
            outputs=[status_output, transcript_download, summary_download],
            show_progress=True,
            queue=True  # Use queue to prevent timeout
        )
    
    return app


def main():
    """Main entry point"""
    try:
        logger.info("Starting Voicemeet_sum GUI")
        
        app = create_interface()
        
        # Launch with error handling
        app.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            inbrowser=True,
            show_error=True,
            max_threads=1  # Single thread to avoid conflicts
        )
    except KeyboardInterrupt:
        logger.info("App stopped by user")
    except Exception as e:
        logger.error(f"App crashed: {e}", exc_info=True)
        print(f"App error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
