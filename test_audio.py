"""
Quick test script for Voicemeet_sum
"""
import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.pipeline.meeting_pipeline import MeetingPipeline
from src.utils.logger import setup_logger, logger
from config.settings import APP

# Setup logger
setup_logger("voicemeet_sum", APP.logs_dir, level=10)  # DEBUG level

def progress_callback(progress: float, status: str):
    """Simple progress callback"""
    bar_length = 30
    filled = int(bar_length * progress / 100)
    bar = '=' * filled + '-' * (bar_length - filled)
    print(f"\r[{bar}] {progress:.1f}% - {status}", end='', flush=True)

def main():
    """Main test function"""
    audio_file = Path("D:/test3.m4a")  # Your test file
    
    if not audio_file.exists():
        print(f"[ERROR] File khong ton tai: {audio_file}")
        return
    
    print(f"[FILE] Input: {audio_file}")
    print(f"[SIZE] {audio_file.stat().st_size / (1024*1024):.2f} MB")
    print()
    
    # Initialize pipeline
    pipeline = MeetingPipeline()
    
    try:
        # Process
        print("[START] Bat dau xu ly...")
        transcript_path, summary_path = pipeline.process(
            audio_file=audio_file,
            progress_callback=progress_callback
        )
        
        print()
        print("=" * 60)
        print("[SUCCESS] HOAN THANH!")
        print("=" * 60)
        print(f"[TRANSCRIPT] {transcript_path}")
        print(f"[SUMMARY] {summary_path}")
        print()
        
        # Show preview
        print("[PREVIEW] TRANSCRIPT:")
        print("-" * 60)
        print(transcript_path.read_text(encoding='utf-8')[:500] + "...")
        print()
        
        print("[PREVIEW] SUMMARY:")
        print("-" * 60)
        print(summary_path.read_text(encoding='utf-8')[:500] + "...")
        
    except Exception as e:
        logger.error(f"Processing failed: {e}", exc_info=True)
        print(f"[ERROR] Loi: {e}")

if __name__ == "__main__":
    main()

