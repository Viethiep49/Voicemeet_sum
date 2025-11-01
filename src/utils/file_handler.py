"""
File handling utilities
"""
import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime

def ensure_dir(path: Path) -> Path:
    """
    Ensure directory exists, create if not
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_audio_duration(file_path: Path) -> float:
    """
    Get audio file duration in seconds using ffprobe
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    import subprocess
    
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return 0.0

def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to file
        
    Returns:
        Size in bytes
    """
    return file_path.stat().st_size

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def clean_temp_files(temp_dir: Path, keep_files: Optional[List[Path]] = None):
    """
    Clean temporary files
    
    Args:
        temp_dir: Temporary directory
        keep_files: List of files to keep
    """
    if not temp_dir.exists():
        return
    
    keep_paths = set(keep_files) if keep_files else set()
    
    for item in temp_dir.iterdir():
        if item.is_file() and item not in keep_paths:
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item, ignore_errors=True)

def generate_output_filename(
    base_name: str,
    suffix: str = "",
    extension: str = "txt"
) -> str:
    """
    Generate output filename with timestamp
    
    Args:
        base_name: Base filename
        suffix: Optional suffix
        extension: File extension
        
    Returns:
        Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix_part = f"_{suffix}" if suffix else ""
    return f"{base_name}_{timestamp}{suffix_part}.{extension}"

def save_text_file(content: str, output_path: Path, encoding: str = "utf-8"):
    """
    Save text content to file
    
    Args:
        content: Text content
        output_path: Output file path
        encoding: File encoding
    """
    ensure_dir(output_path.parent)
    output_path.write_text(content, encoding=encoding)

def load_text_file(file_path: Path, encoding: str = "utf-8") -> str:
    """
    Load text content from file
    
    Args:
        file_path: Input file path
        encoding: File encoding
        
    Returns:
        File content
    """
    return file_path.read_text(encoding=encoding)

def is_valid_audio_file(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Check if file is a valid audio file
    
    Args:
        file_path: File path
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_extensions = {'.m4a', '.mp4', '.mp3', '.wav', '.flac', '.ogg'}
    
    if not file_path.exists():
        return False, "File không tồn tại"
    
    if file_path.suffix.lower() not in valid_extensions:
        return False, f"Định dạng không được hỗ trợ. Hỗ trợ: {', '.join(valid_extensions)}"
    
    file_size = get_file_size(file_path)
    if file_size == 0:
        return False, "File rỗng"
    
    # Check file size (max 2GB)
    if file_size > 2 * 1024 * 1024 * 1024:
        return False, "File quá lớn (tối đa 2GB)"
    
    return True, None

