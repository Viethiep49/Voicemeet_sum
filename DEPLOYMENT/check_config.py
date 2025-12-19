"""
Kiểm tra và hiển thị cấu hình tự động phát hiện
File: DEPLOYMENT/check_config.py
"""
import sys
import io
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import TRANSCRIPTION, auto_detect_whisper_model, auto_detect_device, auto_detect_compute_type

def main():
    print("=" * 70)
    print("  KIỂM TRA CẤU HÌNH TỰ ĐỘNG")
    print("=" * 70)
    print()
    
    # GPU Info
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"🎮 GPU: {gpu_name}")
            print(f"💾 VRAM: {vram_gb:.1f} GB")
        else:
            print("⚠️  GPU: Không có (sử dụng CPU)")
    except ImportError:
        print("⚠️  PyTorch chưa được cài đặt")
    except Exception as e:
        print(f"⚠️  Lỗi kiểm tra GPU: {e}")
    
    print()
    print("-" * 70)
    print("📋 CẤU HÌNH TỰ ĐỘNG PHÁT HIỆN:")
    print("-" * 70)
    print(f"  Model:        {TRANSCRIPTION.model}")
    print(f"  Device:       {TRANSCRIPTION.device}")
    print(f"  Compute Type: {TRANSCRIPTION.compute_type}")
    print(f"  Language:     {TRANSCRIPTION.language}")
    print(f"  Beam Size:    {TRANSCRIPTION.beam_size}")
    print()
    
    # Model recommendations
    print("-" * 70)
    print("💡 THÔNG TIN MODEL:")
    print("-" * 70)
    model_info = {
        "tiny": "Nhanh nhất, độ chính xác thấp (~39M params)",
        "base": "Nhanh, độ chính xác trung bình (~74M params)",
        "small": "Cân bằng tốc độ/chất lượng (~244M params) - KHUYÊN DÙNG cho RTX 3060",
        "medium": "Chất lượng tốt, chậm hơn (~769M params) - Cho GPU mạnh hơn",
        "large-v2": "Chất lượng cao nhất, rất chậm (~1550M params)",
        "large-v3": "Chất lượng cao nhất, rất chậm (~1550M params)"
    }
    
    current_model = TRANSCRIPTION.model
    if current_model in model_info:
        print(f"  {current_model}: {model_info[current_model]}")
    print()
    
    # Override instructions
    print("-" * 70)
    print("🔧 NẾU MUỐN THAY ĐỔI MODEL:")
    print("-" * 70)
    print("  Chỉnh sửa file: config/settings.py")
    print("  Tìm dòng: model: str = None")
    print("  Thay đổi thành: model: str = 'medium'  # hoặc 'small', 'base', 'tiny'")
    print()
    print("  Hoặc set trực tiếp trong code:")
    print("  from config.settings import TRANSCRIPTION")
    print("  TRANSCRIPTION.model = 'medium'")
    print()
    
    print("=" * 70)

if __name__ == "__main__":
    main()

