"""
Prompt templates for LLM (Qwen) interactions
File: config/prompts.py
"""
import json

# ============================================
# CHUNK SUMMARIZATION PROMPT
# ============================================
CHUNK_SUMMARIZE_PROMPT = """Tóm tắt ngắn gọn đoạn cuộc họp sau bằng tiếng Việt.
Giữ lại các thông tin quan trọng: ai nói gì, quyết định gì, việc gì cần làm.
Không thêm thông tin không có trong transcript.

TRANSCRIPT:
---
{transcript}
---

TÓM TẮT:
"""

# ============================================
# JSON EXTRACTION PROMPT
# ============================================
EXTRACTION_PROMPT = """Bạn là trợ lý phân tích cuộc họp doanh nghiệp Việt Nam.

NHIỆM VỤ: Phân tích transcript và trích xuất thông tin theo JSON schema.

QUY TẮC BẮT BUỘC:
1. CHỈ trả về JSON, không có text nào khác
2. KHÔNG bịa thông tin không có trong transcript
3. Nếu không chắc chắn, để null
4. Giữ nguyên tên riêng tiếng Việt
5. Tóm tắt ngắn gọn, súc tích

JSON SCHEMA:
```json
{schema}
```

TRANSCRIPT:
---
{transcript}
---

JSON OUTPUT:
"""

# ============================================
# JSON EXTRACTION SCHEMA
# ============================================
EXTRACTION_SCHEMA = {
    "meeting_info": {
        "main_purpose": "string - Mục đích chính cuộc họp",
        "topics_discussed": ["string - Các chủ đề được bàn"],
        "participants_mentioned": ["string - Tên người được nhắc đến trong audio"]
    },
    "discussions": [
        {
            "topic": "string - Chủ đề",
            "points": [
                {
                    "speaker": "string or null - Ai nói (nếu biết)",
                    "content": "string - Nội dung ý kiến",
                    "type": "opinion | proposal | question | answer | decision"
                }
            ],
            "conclusion": "string or null - Kết luận cho topic này"
        }
    ],
    "decisions": [
        {
            "content": "string - Nội dung quyết định",
            "made_by": "string or null - Ai quyết định"
        }
    ],
    "action_items": [
        {
            "task": "string - Công việc cần làm",
            "assignee": "string or null - Người phụ trách",
            "deadline": "string or null - Hạn hoàn thành",
            "priority": "high | medium | low | null"
        }
    ],
    "other_notes": "string or null - Ghi chú khác"
}

# ============================================
# Helper function to get schema as formatted JSON string
# ============================================
def get_extraction_schema_json() -> str:
    """
    Get JSON schema as formatted string for prompt injection

    Returns:
        Formatted JSON schema string
    """
    return json.dumps(EXTRACTION_SCHEMA, indent=2, ensure_ascii=False)
