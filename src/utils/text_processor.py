"""
Text processing utilities
"""
from typing import List

def chunk_text(text: str, chunk_size: int, overlap: int = 200) -> List[str]:
    """
    Split text into chunks with overlap
    
    Args:
        text: Input text
        chunk_size: Maximum chunk size in characters
        overlap: Overlap between chunks in characters
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Try to break at sentence end
        sentence_end = text.rfind('.', start, end)
        if sentence_end > start + chunk_size // 2:
            end = sentence_end + 1
        else:
            # Try to break at word boundary
            word_end = text.rfind(' ', start, end)
            if word_end > start + chunk_size // 2:
                end = word_end
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

def clean_text(text: str) -> str:
    """
    Clean text: remove extra whitespaces, normalize line breaks
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove excessive blank lines
    lines = text.split('\n')
    cleaned_lines = []
    prev_blank = False
    
    for line in lines:
        is_blank = not line.strip()
        
        if not (is_blank and prev_blank):
            cleaned_lines.append(line)
        
        prev_blank = is_blank
    
    return '\n'.join(cleaned_lines).strip()

def format_summary(
    content: str,
    decisions: str = "",
    actions: str = ""
) -> str:
    """
    Format summary with sections
    
    Args:
        content: Main content
        decisions: Decisions made
        actions: Action items
        
    Returns:
        Formatted summary
    """
    sections = ["# TÓM TẮT CUỘC HỌP\n\n## NỘI DUNG CHÍNH"]
    
    if content:
        sections.append(content)
    
    if decisions:
        sections.append("\n## CÁC QUYẾT ĐỊNH")
        sections.append(decisions)
    
    if actions:
        sections.append("\n## HÀNH ĐỘNG CẦN LÀM")
        sections.append(actions)
    
    return "\n".join(sections)

def estimate_word_count(text: str) -> int:
    """
    Estimate word count (Vietnamese-friendly)
    
    Args:
        text: Input text
        
    Returns:
        Estimated word count
    """
    # Simple estimation: split by spaces
    words = text.split()
    return len(words)

def estimate_reading_time(word_count: int, words_per_minute: int = 200) -> str:
    """
    Estimate reading time
    
    Args:
        word_count: Number of words
        words_per_minute: Average reading speed
        
    Returns:
        Formatted reading time
    """
    minutes = word_count / words_per_minute
    
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds} giây"
    
    if minutes < 60:
        return f"{int(minutes)} phút"
    
    hours = minutes / 60
    remaining_minutes = int(minutes % 60)
    
    if remaining_minutes == 0:
        return f"{int(hours)} giờ"
    
    return f"{int(hours)} giờ {remaining_minutes} phút"

