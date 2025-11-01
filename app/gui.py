"""
Gradio GUI for Voicemeet_sum
"""
import sys
from pathlib import Path
from typing import Tuple, Optional

import gradio as gr

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline.meeting_pipeline import MeetingPipeline
from src.utils.logger import setup_logger, logger
from src.utils.file_handler import is_valid_audio_file, format_file_size, get_file_size
from app.themes import get_voicemeet_theme
from config.settings import APP

# Setup logger
setup_logger("voicemeet_sum", APP.logs_dir)

# Initialize pipeline
pipeline = MeetingPipeline()


def process_audio(
    audio_file,
    show_status: bool = True
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Process audio file and return results
    
    Args:
        audio_file: Uploaded audio file from Gradio
        show_status: Show processing status
        
    Returns:
        Tuple of (status_msg, transcript_file, summary_file)
    """
    if audio_file is None:
        return "❌ Vui lòng chọn file audio", None, None
    
    # Gradio file upload returns a NamedTemporaryFile object with .name attribute
    audio_path = Path(audio_file.name) if isinstance(audio_file, object) and hasattr(audio_file, 'name') else Path(str(audio_file))
    
    # Validate file
    is_valid, error_msg = is_valid_audio_file(audio_path)
    if not is_valid:
        return f"❌ {error_msg}", None, None
    
    try:
        # Process
        transcript_path, summary_path = pipeline.process(
            audio_file=audio_path
        )
        
        # Get file info
        transcript_size = format_file_size(get_file_size(transcript_path))
        summary_size = format_file_size(get_file_size(summary_path))
        
        success_msg = (
            "✅ Hoàn thành!\n\n"
            f"📄 Transcript: {transcript_path.name} ({transcript_size})\n"
            f"📋 Summary: {summary_path.name} ({summary_size})\n\n"
            f"Files saved in: {APP.output_dir}"
        )
        
        return success_msg, str(transcript_path), str(summary_path)
        
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return f"❌ Lỗi: {str(e)}", None, None


def process_with_progress(audio_file) -> Tuple[str, str]:
    """
    Process audio with progress tracking
    
    Args:
        audio_file: Uploaded audio file
        
    Returns:
        Tuple of (status_msg, transcript_file)
    """
    # This will be called with gradio Progress
    pass


def create_interface():
    """Create and launch Gradio interface"""
    
    custom_theme = get_voicemeet_theme()
    
    with gr.Blocks(theme=custom_theme, title="Voicemeet_sum") as app:
        # Header
        gr.Markdown(
            "# 🎤 Voicemeet_sum\n"
            "Ứng dụng chuyển đổi audio cuộc họp thành văn bản và tóm tắt tự động"
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                # File upload
                gr.Markdown("## 📁 Upload Audio File")
                audio_input = gr.File(
                    label="Chọn file audio (M4A, MP4, MP3, WAV)",
                    file_types=[".m4a", ".mp4", ".mp3", ".wav", ".flac"]
                )
                
                # Settings
                gr.Markdown("## ⚙️ Cài đặt (tùy chọn)")
                with gr.Row():
                    remove_silence = gr.Checkbox(
                        label="Loại bỏ khoảng lặng",
                        value=True,
                        info="Tự động xóa các đoạn im lặng"
                    )
                    normalize = gr.Checkbox(
                        label="Tối ưu âm lượng",
                        value=True,
                        info="Chuẩn hóa âm lượng audio"
                    )
                
                # Process button
                process_btn = gr.Button(
                    "🚀 Bắt đầu xử lý",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=3):
                # Status and progress
                gr.Markdown("## 📊 Kết quả")
                status_output = gr.Textbox(
                    label="Trạng thái",
                    lines=5,
                    interactive=False,
                    placeholder="Kết quả sẽ hiển thị ở đây..."
                )
                
                # Progress bar
                progress_bar = gr.Progress()
                
                # Output files
                gr.Markdown("### 📥 Tải kết quả")
                with gr.Row():
                    transcript_download = gr.File(
                        label="Transcript (Full)",
                        visible=True
                    )
                    summary_download = gr.File(
                        label="Summary",
                        visible=True
                    )
        
        # Process button click
        process_btn.click(
            fn=process_audio,
            inputs=[audio_input],
            outputs=[status_output, transcript_download, summary_download],
            show_progress="full"
        )
        
        # Footer
        gr.Markdown(
            "---\n"
            "### ℹ️ Thông tin\n"
            f"- Output directory: `{APP.output_dir}`\n"
            "- Supported formats: M4A, MP4, MP3, WAV, FLAC\n"
            "- Processing time: ~10-15 phút cho file 2 giờ"
        )
    
    return app


def main():
    """Main entry point"""
    logger.info("Starting Voicemeet_sum GUI")
    
    app = create_interface()
    
    # Launch
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )


if __name__ == "__main__":
    main()

