"""Test CUDA setup for Whisper"""
import sys
import os
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

# Setup cuDNN path
if sys.platform == 'win32':
    try:
        import torch
        torch_lib = os.path.join(os.path.dirname(torch.__file__), 'lib')
        if os.path.exists(torch_lib):
            current_path = os.environ.get('PATH', '')
            if torch_lib not in current_path:
                os.environ['PATH'] = torch_lib + os.pathsep + current_path
                print(f"[OK] Added PyTorch lib to PATH: {torch_lib}")
    except ImportError:
        print("[ERROR] PyTorch not installed")

print("\n" + "="*60)
print("CUDA Setup Test")
print("="*60)

# Check PyTorch CUDA
try:
    import torch
    print(f"\n[PyTorch]")
    print(f"  Version: {torch.__version__}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  CUDA version: {torch.version.cuda}")
        print(f"  cuDNN version: {torch.backends.cudnn.version()}")
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
except ImportError:
    print("[ERROR] PyTorch not installed")
    sys.exit(1)

# Check ctranslate2
try:
    import ctranslate2
    print(f"\n[ctranslate2]")
    print(f"  Version: {ctranslate2.__version__}")
    print(f"  CUDA devices: {ctranslate2.get_cuda_device_count()}")
except ImportError:
    print("[ERROR] ctranslate2 not installed")

# Test faster-whisper
try:
    from faster_whisper import WhisperModel
    print(f"\n[faster-whisper]")
    print("  Testing model load...")
    
    # Try loading tiny model to test
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("  [OK] Model loaded successfully on CUDA!")
    del model
except Exception as e:
    print(f"  [ERROR] Failed to load model: {e}")
    print("  Trying CPU...")
    try:
        model = WhisperModel("tiny", device="cpu", compute_type="float32")
        print("  [WARNING] Model loaded on CPU (CUDA failed)")
        del model
    except Exception as e2:
        print(f"  [ERROR] CPU also failed: {e2}")

print("\n" + "="*60)
print("Test completed!")
print("="*60)

