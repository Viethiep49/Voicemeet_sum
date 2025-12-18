"""
Text chunking for long transcripts
File: src/summarization/chunker.py
"""
from typing import List
from ..utils.logger import logger
from ..utils.text_processor import chunk_text as _chunk_text_util


class TextChunker:
    """Handle text chunking for long transcripts"""

    def __init__(self, max_chunk_size: int = 15000, overlap: int = 500):
        """
        Initialize text chunker

        Args:
            max_chunk_size: Maximum size of each chunk in characters
            overlap: Number of overlapping characters between chunks
        """
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def should_chunk(self, text: str) -> bool:
        """
        Check if text needs chunking (threshold: 20k chars)

        Args:
            text: Input text to check

        Returns:
            True if text should be chunked, False otherwise
        """
        return len(text) > 20000

    def chunk(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks at sentence boundaries

        Args:
            text: Full transcript text

        Returns:
            List of text chunks
        """
        if not self.should_chunk(text):
            return [text]

        # Use existing chunk_text utility
        chunks = _chunk_text_util(text, self.max_chunk_size, self.overlap)

        logger.info(f"Split transcript into {len(chunks)} chunks")
        return chunks

    def combine_summaries(self, summaries: List[str]) -> str:
        """
        Combine chunk summaries into single text

        Args:
            summaries: List of summarized chunks

        Returns:
            Combined summary text
        """
        if not summaries:
            return ""

        if len(summaries) == 1:
            return summaries[0]

        # Join summaries with double line break for readability
        combined = "\n\n".join(summaries)

        logger.info(f"Combined {len(summaries)} chunk summaries into one text")
        return combined
