"""
Qwen summarization service via Ollama
"""
import requests
from typing import Optional, Callable
import json
import time

from ..utils.logger import logger
from ..utils.text_processor import chunk_text
from config.settings import SUMMARIZATION


class QwenService:
    """Handle summarization using Qwen via Ollama"""
    
    def __init__(self, config=None):
        """
        Initialize Qwen service
        
        Args:
            config: SummarizationConfig instance
        """
        self.config = config or SUMMARIZATION
        self.base_url = self.config.base_url
    
    def summarize(
        self,
        transcript: str,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> str:
        """
        Generate summary from transcript
        
        Args:
            transcript: Full transcript text
            progress_callback: Callback function(progress: float, status: str)
            
        Returns:
            Formatted summary
        """
        logger.info("Starting summarization")
        start_time = time.time()
        
        # Check if Ollama is available
        if not self._check_ollama():
            logger.error("Ollama is not running")
            raise RuntimeError("Ollama chưa được khởi động. Vui lòng chạy: ollama serve")
        
        # Check if model is available
        self._ensure_model_exists()
        
        # Chunk transcript if too long
        max_length = 20000  # Approximate token limit
        if len(transcript) > max_length:
            logger.info("Transcript too long, chunking...")
            chunks = chunk_text(transcript, max_length - 1000, overlap=200)
            
            # Summarize chunks first
            chunk_summaries = []
            for i, chunk in enumerate(chunks):
                if progress_callback:
                    progress = 80 + (i / len(chunks)) * 15
                    progress_callback(progress, f"Đang tóm tắt... ({i+1}/{len(chunks)})")
                
                chunk_summary = self._summarize_chunk(chunk)
                chunk_summaries.append(chunk_summary)
            
            # Combine and summarize again
            combined = "\n".join(chunk_summaries)
            if progress_callback:
                progress_callback(95, "Đang hoàn thiện tóm tắt...")
            
            final_summary = self._summarize_final(combined)
        else:
            if progress_callback:
                progress_callback(85, "Đang tóm tắt...")
            final_summary = self._summarize_complete(transcript)
        
        summarize_time = time.time() - start_time
        logger.info(f"Summarization completed in {summarize_time:.2f}s")
        
        if progress_callback:
            progress_callback(100, "Hoàn thành!")
        
        return final_summary
    
    def _summarize_complete(self, text: str) -> str:
        """
        Summarize complete transcript
        
        Args:
            text: Full transcript
            
        Returns:
            Summary
        """
        prompt = self._build_summary_prompt(text, style="complete")
        response = self._call_ollama(prompt)
        return response
    
    def _summarize_chunk(self, chunk: str) -> str:
        """
        Summarize a chunk of transcript
        
        Args:
            chunk: Chunk of text
            
        Returns:
            Chunk summary
        """
        prompt = self._build_summary_prompt(chunk, style="chunk")
        response = self._call_ollama(prompt)
        return response
    
    def _summarize_final(self, combined_summaries: str) -> str:
        """
        Create final summary from combined chunk summaries
        
        Args:
            combined_summaries: Combined summaries
            
        Returns:
            Final formatted summary
        """
        prompt = self._build_summary_prompt(combined_summaries, style="final")
        response = self._call_ollama(prompt)
        return response
    
    def _build_summary_prompt(self, text: str, style: str = "complete") -> str:
        """
        Build prompt for summarization
        
        Args:
            text: Input text
            style: Prompt style (complete, chunk, final)
            
        Returns:
            Formatted prompt
        """
        base_instruction = """
Bạn là trợ lý chuyên nghiệp tóm tắt cuộc họp. Hãy tóm tắt cuộc họp bằng tiếng Việt theo cấu trúc sau:

# TÓM TẮT CUỘC HỌP

## NỘI DUNG CHÍNH
[Tóm tắt ngắn gọn 3-5 điểm chính của cuộc họp]

## CÁC QUYẾT ĐỊNH
[Liệt kê các quyết định quan trọng được đưa ra, nếu có]

## HÀNH ĐỘNG CẦN LÀM
[Liệt kê các công việc cần làm tiếp theo với deadline hoặc người chịu trách nhiệm, nếu có]

Chỉ trả về nội dung tóm tắt, không thêm lời giải thích khác.
"""
        
        if style == "complete":
            prompt = f"{base_instruction}\n\nNội dung cuộc họp:\n{text}"
        elif style == "chunk":
            prompt = f"Tóm tắt ngắn gọn đoạn họp sau:\n\n{text}"
        else:  # final
            prompt = f"{base_instruction}\n\nCác tóm tắt phụ:\n{text}"
        
        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API
        
        Args:
            prompt: Input prompt
            
        Returns:
            Model response
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            raise RuntimeError(f"Lỗi khi gọi Ollama: {e}")
    
    def _check_ollama(self) -> bool:
        """
        Check if Ollama is running
        
        Returns:
            True if running
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _ensure_model_exists(self):
        """
        Check and pull model if not exists
        """
        try:
            # Check available models
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if self.config.model not in model_names:
                logger.info(f"Model {self.config.model} not found, pulling...")
                self._pull_model()
        except Exception as e:
            logger.warning(f"Could not check model: {e}")
    
    def _pull_model(self):
        """
        Pull model from Ollama
        """
        url = f"{self.base_url}/api/pull"
        payload = {"name": self.config.model}
        
        try:
            response = requests.post(url, json=payload, stream=True, timeout=3600)
            response.raise_for_status()
            
            logger.info("Downloading model...")
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    logger.debug(f"Model pull: {data.get('status', '')}")
            
            logger.info("Model downloaded successfully")
        except Exception as e:
            logger.error(f"Failed to pull model: {e}")
            raise RuntimeError(f"Không thể tải model: {e}")

