"""
Download models for Voicemeet_sum
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import TRANSCRIPTION, APP
from src.utils.logger import logger

def download_whisper_model():
    """
    Download Faster-Whisper model
    """
    model_name = TRANSCRIPTION.model
    
    print(f"Downloading Whisper model: {model_name}")
    logger.info(f"Downloading Whisper model: {model_name}")
    
    try:
        from faster_whisper import WhisperModel
        
        model = WhisperModel(
            model_name,
            device=TRANSCRIPTION.device,
            compute_type=TRANSCRIPTION.compute_type,
            download_root=str(APP.models_cache.parent)
        )
        
        print("✅ Whisper model downloaded successfully")
        logger.info("Whisper model downloaded successfully")
        
    except Exception as e:
        print(f"❌ Failed to download Whisper model: {e}")
        logger.error(f"Failed to download Whisper model: {e}")
        return False
    
    return True

def main():
    """
    Main function to download all models
    """
    print("=" * 60)
    print("DOWNLOADING MODELS")
    print("=" * 60)
    
    # Download Whisper
    download_whisper_model()
    
    # Note about Qwen
    print("\n" + "=" * 60)
    print("NOTE: Qwen model needs to be downloaded via Ollama")
    print("Run: ollama pull qwen2.5:7b")
    print("=" * 60)
    
    print("\n✅ Model download complete!")

if __name__ == "__main__":
    main()

