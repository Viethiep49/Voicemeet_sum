"""
System resource checker
"""
import platform
import sys
from typing import Tuple, List

def check_python_version() -> Tuple[bool, str]:
    """
    Check Python version
    
    Returns:
        Tuple of (is_valid, message)
    """
    version = sys.version_info
    required_version = (3, 9)
    
    if version.major >= required_version[0] and version.minor >= required_version[1]:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    
    return False, f"Python {required_version[0]}.{required_version[1]}+ required, found {version.major}.{version.minor}"

def check_gpu() -> Tuple[bool, str]:
    """
    Check if CUDA GPU is available
    
    Returns:
        Tuple of (is_available, message)
    """
    try:
        import torch
        
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            return True, f"GPU: {device_name} ({memory_gb:.1f} GB VRAM)"
        
        return False, "CUDA GPU không khả dụng"
    except ImportError:
        return False, "PyTorch chưa được cài đặt"

def check_ffmpeg() -> Tuple[bool, str]:
    """
    Check if FFmpeg is installed
    
    Returns:
        Tuple of (is_available, message)
    """
    import subprocess
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, f"FFmpeg: {version_line}"
        
        return False, "FFmpeg không khả dụng"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "FFmpeg chưa được cài đặt"

def check_ollama() -> Tuple[bool, str]:
    """
    Check if Ollama is running
    
    Returns:
        Tuple of (is_available, message)
    """
    import requests
    
    try:
        response = requests.get("http://localhost:11434", timeout=2)
        if response.status_code == 200:
            return True, "Ollama đang chạy"
        return False, "Ollama không phản hồi"
    except:
        return False, "Ollama chưa được cài đặt hoặc chưa chạy"

def check_system_resources() -> List[Tuple[str, bool, str]]:
    """
    Check all system resources
    
    Returns:
        List of (component, status, message)
    """
    checks = []
    
    # Check Python
    py_ok, py_msg = check_python_version()
    checks.append(("Python", py_ok, py_msg))
    
    # Check FFmpeg
    ffmpeg_ok, ffmpeg_msg = check_ffmpeg()
    checks.append(("FFmpeg", ffmpeg_ok, ffmpeg_msg))
    
    # Check GPU
    gpu_ok, gpu_msg = check_gpu()
    checks.append(("GPU", gpu_ok, gpu_msg))
    
    # Check Ollama (optional for now)
    ollama_ok, ollama_msg = check_ollama()
    checks.append(("Ollama", ollama_ok, ollama_msg))
    
    return checks

def print_system_check():
    """
    Print system check results
    """
    print("=" * 60)
    print("KIỂM TRA HỆ THỐNG / SYSTEM CHECK")
    print("=" * 60)
    
    checks = check_system_resources()
    
    for component, status, message in checks:
        status_symbol = "✅" if status else "❌"
        print(f"{status_symbol} {component:12s} : {message}")
    
    print("=" * 60)
    
    # Overall status
    all_ok = all(check[1] for check in checks if check[0] != "Ollama")  # Ollama optional
    
    if all_ok:
        print("✅ Hệ thống sẵn sàng")
    else:
        print("⚠️  Một số thành phần chưa sẵn sàng")
    
    return all_ok

if __name__ == "__main__":
    print_system_check()

