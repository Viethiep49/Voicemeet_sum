"""
Meeting information extraction from transcript
File: src/summarization/extractor.py
"""
import json
import re
from typing import Optional, Callable
from ..utils.logger import logger
from config.prompts import EXTRACTION_PROMPT, get_extraction_schema_json


class MeetingExtractor:
    """Extract structured data from transcript using LLM"""

    def __init__(self, qwen_service):
        """
        Initialize meeting extractor

        Args:
            qwen_service: QwenService instance for LLM calls
        """
        self.qwen = qwen_service

    def extract(
        self,
        transcript: str,
        max_retries: int = 2,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Extract meeting info to structured JSON

        Args:
            transcript: Meeting transcript text
            max_retries: Number of retry attempts if extraction fails
            progress_callback: Progress update callback function

        Returns:
            Validated JSON dict or fallback structure
        """
        for attempt in range(max_retries):
            try:
                if progress_callback:
                    progress = 85 + attempt * 3
                    progress_callback(progress, f"Extracting info (attempt {attempt + 1})...")

                logger.info(f"Extraction attempt {attempt + 1}/{max_retries}")

                # Build prompt
                prompt = EXTRACTION_PROMPT.format(
                    schema=get_extraction_schema_json(),
                    transcript=transcript
                )

                # Call LLM
                response = self.qwen.extract_json(prompt)

                # Validate JSON
                data = self._validate_json(response)
                if data:
                    logger.info("JSON extraction successful")
                    return data

            except Exception as e:
                logger.warning(f"Extraction attempt {attempt + 1} failed: {e}")

        # Fallback if all attempts fail
        logger.warning("All extraction attempts failed, using fallback")
        return self._fallback_extraction(transcript)

    def _validate_json(self, response: str) -> Optional[dict]:
        """
        Parse and validate JSON response from LLM

        Args:
            response: Raw LLM response text

        Returns:
            Parsed dict if valid, None if invalid
        """
        try:
            # Clean response - remove markdown code blocks if present
            cleaned = response.strip()

            # Remove ```json and ``` markers if present
            cleaned = re.sub(r'^```json\s*', '', cleaned)
            cleaned = re.sub(r'^```\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)

            # Parse JSON
            data = json.loads(cleaned)

            # Basic schema validation - check required top-level keys
            required_keys = ['meeting_info', 'discussions', 'decisions', 'action_items']
            if all(key in data for key in required_keys):
                logger.info("JSON validation passed")
                return data

            logger.warning(f"Missing required keys in JSON response. Found: {list(data.keys())}")
            return None

        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {e}")
            logger.debug(f"Raw response: {response[:500]}...")  # Log first 500 chars
            return None

    def _fallback_extraction(self, transcript: str) -> dict:
        """
        Basic extraction when LLM fails - returns minimal valid structure

        Args:
            transcript: Original transcript text

        Returns:
            Minimal valid JSON structure
        """
        logger.info("Creating fallback extraction structure")

        # Truncate transcript if too long for fallback
        max_fallback_length = 2000
        truncated_transcript = transcript[:max_fallback_length]
        if len(transcript) > max_fallback_length:
            truncated_transcript += "..."

        return {
            "meeting_info": {
                "main_purpose": "Cuộc họp được ghi nhận từ audio",
                "topics_discussed": ["(Extraction tự động không thành công, xem transcript đầy đủ)"],
                "participants_mentioned": []
            },
            "discussions": [
                {
                    "topic": "Nội dung cuộc họp",
                    "points": [
                        {
                            "speaker": None,
                            "content": truncated_transcript,
                            "type": "opinion"
                        }
                    ],
                    "conclusion": None
                }
            ],
            "decisions": [],
            "action_items": [],
            "other_notes": "Lưu ý: Extraction tự động không thành công. Vui lòng xem transcript đầy đủ để biết chi tiết cuộc họp."
        }
