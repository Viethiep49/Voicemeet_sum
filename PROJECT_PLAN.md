# PROJECT PLAN: Smart Meeting Assistant

## 🎯 Mục tiêu dự án

Xây dựng **Trợ lý họp thông minh** cho doanh nghiệp Việt Nam, tự động chuyển đổi audio cuộc họp thành biên bản chuẩn doanh nghiệp.

**Cuộc thi:** Hội thi "TÌM KIẾM TÀI NĂNG CNTT 2025" - Bảng D: AI & Blockchain  
**Deadline:** Đăng ký 26/12/2025, Bán kết 28-31/12/2025

---

## 📋 Yêu cầu chính

### Ưu tiên cao (MUST HAVE)
- [ ] Transcription chính xác cao cho tiếng Việt
- [ ] Tốc độ xử lý vừa đủ (không quá chậm)
- [ ] Export DOCX theo format biên bản doanh nghiệp VN
- [ ] Metadata placeholders để thư ký điền sau

### Ưu tiên thấp (NICE TO HAVE)
- [ ] Speaker diarization (phân biệt người nói)
- [ ] Chatbot Q&A với nội dung cuộc họp
- [ ] Export PDF
- [ ] Blockchain verification (demo level)

---

## 🏗️ Kiến trúc hệ thống

```
┌──────────────────────────────────────────────────────────────┐
│                      PROCESSING PIPELINE                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [Audio File]                                                │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐                                            │
│  │  FFmpeg     │  Preprocess (normalize, resample 16kHz)    │
│  └─────────────┘                                            │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │  Whisper    │  │  Pyannote   │  [Optional: Diarization]  │
│  │  (medium)   │  │  (speaker)  │                           │
│  └─────────────┘  └─────────────┘                           │
│       │                 │                                    │
│       └────────┬────────┘                                    │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │     Raw Transcript              │                        │
│  └─────────────────────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │     Text Preprocessing          │                        │
│  │     • Clean text                │                        │
│  │     • Chunk if > 20k chars      │                        │
│  └─────────────────────────────────┘                        │
│                │                                             │
│                ▼ (if chunked)                                │
│  ┌─────────────────────────────────┐                        │
│  │     Qwen 2.5 7B                 │                        │
│  │     Summarize each chunk        │                        │
│  │     → Combine summaries         │                        │
│  └─────────────────────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │     Qwen 2.5 7B                 │                        │
│  │     EXTRACT to JSON             │                        │
│  │     (Structured extraction)     │                        │
│  └─────────────────────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │     JSON Validation             │                        │
│  │     • Parse check               │                        │
│  │     • Schema validation         │                        │
│  │     • Retry if failed (max 2)   │                        │
│  └─────────────────────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │     Python Formatter            │                        │
│  │     Apply DOCX template         │                        │
│  └─────────────────────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │     DOCX Export                 │                        │
│  │     • AI-generated content      │                        │
│  │     • Placeholder metadata      │                        │
│  └─────────────────────────────────┘                        │
│                │                                             │
│                ▼                                             │
│         [Final DOCX File]                                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core Processing
| Component | Technology | Purpose |
|-----------|------------|---------|
| Audio Preprocessing | FFmpeg | Normalize, resample to 16kHz mono |
| Speech-to-Text | Faster-Whisper (medium) | Transcription tiếng Việt |
| Speaker Diarization | Pyannote-audio | Phân biệt người nói [Optional] |
| Summarization | Qwen 2.5 7B via Ollama | Extract + Summarize |
| Export | python-docx | Tạo file DOCX |

### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| API Server | FastAPI | HTTP endpoints |
| Task Queue | In-memory dict | Job management (đủ cho demo) |
| File Storage | Local filesystem | Output files |

### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| UI | HTML/CSS/JS (vanilla) | Single page app |
| Styling | Custom CSS | Modern gradient UI |

**Lưu ý:** Không cần database cho demo. In-memory storage đủ dùng.

---

## 📊 JSON Extraction Schema

LLM sẽ extract transcript thành JSON format sau:

```json
{
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
          "speaker": "string hoặc null - Ai nói (nếu biết)",
          "content": "string - Nội dung ý kiến",
          "type": "opinion | proposal | question | answer | decision"
        }
      ],
      "conclusion": "string hoặc null - Kết luận cho topic này"
    }
  ],
  "decisions": [
    {
      "content": "string - Nội dung quyết định",
      "made_by": "string hoặc null - Ai quyết định"
    }
  ],
  "action_items": [
    {
      "task": "string - Công việc cần làm",
      "assignee": "string hoặc null - Người phụ trách",
      "deadline": "string hoặc null - Hạn hoàn thành",
      "priority": "high | medium | low | null"
    }
  ],
  "other_notes": "string hoặc null - Ghi chú khác"
}
```

---

## 📝 DOCX Template - Biên bản họp doanh nghiệp VN

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              CÔNG TY [_______________________]              │
│                     (Placeholder - thư ký điền)             │
│                                                             │
│                     BIÊN BẢN HỌP                           │
│              Số: _____/BB-__________                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Thời gian: Ngày ___/___/______, từ ___:___ đến ___:___   │
│  Địa điểm: [________________________________________________]│
│  Hình thức: ☐ Trực tiếp    ☐ Trực tuyến    ☐ Kết hợp      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  THÀNH PHẦN THAM DỰ:                                       │
│                                                             │
│  Chủ trì:  [______________________] - [______________]     │
│  Thư ký:   [______________________] - [______________]     │
│                                                             │
│  Thành viên:                                               │
│  1. [______________________] - [______________]            │
│  2. [______________________] - [______________]            │
│  3. [______________________] - [______________]            │
│                                                             │
│  Vắng mặt: [______________________________________________]│
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  I. MỤC ĐÍCH CUỘC HỌP                                      │
│     [AI generated: meeting_info.main_purpose]              │
│                                                             │
│  II. NỘI DUNG THẢO LUẬN                                    │
│                                                             │
│     1. [discussions[0].topic]                              │
│        • [speaker]: [content]                              │
│        • [speaker]: [content]                              │
│        → Kết luận: [conclusion]                            │
│                                                             │
│     2. [discussions[1].topic]                              │
│        ...                                                 │
│                                                             │
│  III. CÁC QUYẾT ĐỊNH                                       │
│     1. [decisions[0].content]                              │
│     2. [decisions[1].content]                              │
│                                                             │
│  IV. PHÂN CÔNG CÔNG VIỆC                                   │
│  ┌─────┬──────────────────┬───────────────┬────────────┐   │
│  │ STT │ Nội dung         │ Phụ trách     │ Deadline   │   │
│  ├─────┼──────────────────┼───────────────┼────────────┤   │
│  │  1  │ [task]           │ [assignee]    │ [deadline] │   │
│  │  2  │ [task]           │ [assignee]    │ [deadline] │   │
│  └─────┴──────────────────┴───────────────┴────────────┘   │
│                                                             │
│  V. Ý KIẾN KHÁC                                            │
│     [AI generated: other_notes]                            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Cuộc họp kết thúc vào lúc ___:___, cùng ngày.            │
│                                                             │
│         THƯ KÝ                         CHỦ TRÌ             │
│     (Ký, ghi rõ họ tên)           (Ký, ghi rõ họ tên)      │
│                                                             │
│  ____________________           ____________________        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Nguyên tắc:**
- Sections I, II, III, IV, V: AI generate từ JSON extraction
- Metadata (công ty, thời gian, thành phần...): Placeholder để thư ký điền sau
- Font: Times New Roman 13pt (chuẩn văn bản VN)

---

## 📁 Cấu trúc thư mục đề xuất

```
smart_meeting_assistant/
├── app/
│   ├── __init__.py
│   ├── backend.py              # FastAPI server (giữ nguyên structure)
│   └── static/
│       └── index.html          # Frontend UI
│
├── config/
│   ├── __init__.py
│   ├── settings.py             # App configuration
│   └── prompts.py              # [NEW] Prompt templates cho LLM
│
├── src/
│   ├── __init__.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── meeting_pipeline.py # Main orchestrator
│   │
│   ├── transcription/
│   │   ├── __init__.py
│   │   ├── audio_processor.py  # FFmpeg preprocessing
│   │   ├── whisper_service.py  # Speech-to-text
│   │   └── diarization.py      # [NEW][Optional] Speaker ID
│   │
│   ├── summarization/
│   │   ├── __init__.py
│   │   ├── qwen_service.py     # [REFACTOR] LLM interaction
│   │   ├── extractor.py        # [NEW] JSON extraction logic
│   │   └── chunker.py          # [NEW] Text chunking logic
│   │
│   ├── export/
│   │   ├── __init__.py
│   │   ├── docx_exporter.py    # [NEW] DOCX generation
│   │   └── templates/          # [NEW] DOCX templates
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── file_handler.py
│       ├── system_checker.py
│       └── text_processor.py
│
├── output/                     # Generated files
├── models/                     # Cached models
├── logs/                       # Log files
├── temp/                       # Temporary files
│
├── DEPLOYMENT/
│   ├── setup.bat
│   ├── run_fastapi.bat
│   └── check_system.py
│
├── requirements.txt
├── requirements_fastapi.txt
├── PROJECT_PLAN.md             # This file
└── README.md
```

---

## 🔧 Implementation Tasks

### Phase 1: Refactor Summarization (Priority: HIGH)

#### Task 1.1: Tạo config/prompts.py
```python
# config/prompts.py

CHUNK_SUMMARIZE_PROMPT = """
Tóm tắt ngắn gọn đoạn cuộc họp sau bằng tiếng Việt.
Giữ lại các thông tin quan trọng: ai nói gì, quyết định gì, việc gì cần làm.
Không thêm thông tin không có trong transcript.

TRANSCRIPT:
---
{transcript}
---

TÓM TẮT:
"""

EXTRACTION_PROMPT = """
Bạn là trợ lý phân tích cuộc họp doanh nghiệp Việt Nam.

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

EXTRACTION_SCHEMA = {
    "meeting_info": {
        "main_purpose": "string - Mục đích chính cuộc họp",
        "topics_discussed": ["string"],
        "participants_mentioned": ["string"]
    },
    "discussions": [
        {
            "topic": "string",
            "points": [
                {
                    "speaker": "string or null",
                    "content": "string",
                    "type": "opinion | proposal | question | answer | decision"
                }
            ],
            "conclusion": "string or null"
        }
    ],
    "decisions": [
        {
            "content": "string",
            "made_by": "string or null"
        }
    ],
    "action_items": [
        {
            "task": "string",
            "assignee": "string or null",
            "deadline": "string or null",
            "priority": "high | medium | low | null"
        }
    ],
    "other_notes": "string or null"
}
```

#### Task 1.2: Tạo src/summarization/chunker.py
```python
# src/summarization/chunker.py

from typing import List
from ..utils.logger import logger

class TextChunker:
    """Handle text chunking for long transcripts"""
    
    def __init__(self, max_chunk_size: int = 15000, overlap: int = 500):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def should_chunk(self, text: str) -> bool:
        """Check if text needs chunking (threshold: 20k chars)"""
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
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.max_chunk_size
            
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Find sentence boundary (., !, ?)
            sentence_end = max(
                text.rfind('.', start, end),
                text.rfind('!', start, end),
                text.rfind('?', start, end)
            )
            
            if sentence_end > start + self.max_chunk_size // 2:
                end = sentence_end + 1
            
            chunks.append(text[start:end].strip())
            start = end - self.overlap
        
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
        return "\n\n".join(summaries)
```

#### Task 1.3: Tạo src/summarization/extractor.py
```python
# src/summarization/extractor.py

import json
import re
from typing import Optional, Callable
from ..utils.logger import logger
from config.prompts import EXTRACTION_PROMPT, EXTRACTION_SCHEMA

class MeetingExtractor:
    """Extract structured data from transcript using LLM"""
    
    def __init__(self, qwen_service):
        self.qwen = qwen_service
        self.schema = EXTRACTION_SCHEMA
    
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
            max_retries: Number of retry attempts
            progress_callback: Progress update callback
            
        Returns:
            Validated JSON dict or fallback structure
        """
        for attempt in range(max_retries):
            try:
                if progress_callback:
                    progress_callback(85 + attempt * 3, f"Extracting info (attempt {attempt + 1})...")
                
                # Build prompt
                prompt = EXTRACTION_PROMPT.format(
                    schema=json.dumps(self.schema, indent=2, ensure_ascii=False),
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
        
        # Fallback
        logger.warning("Using fallback extraction")
        return self._fallback_extraction(transcript)
    
    def _validate_json(self, response: str) -> Optional[dict]:
        """
        Parse and validate JSON response
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed dict or None if invalid
        """
        try:
            # Clean response - remove markdown code blocks if present
            cleaned = response.strip()
            cleaned = re.sub(r'^```json\s*', '', cleaned)
            cleaned = re.sub(r'^```\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)
            
            data = json.loads(cleaned)
            
            # Basic schema validation
            required_keys = ['meeting_info', 'discussions', 'decisions', 'action_items']
            if all(key in data for key in required_keys):
                return data
            
            logger.warning(f"Missing required keys in JSON response")
            return None
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {e}")
            return None
    
    def _fallback_extraction(self, transcript: str) -> dict:
        """
        Basic extraction when LLM fails
        
        Args:
            transcript: Original transcript
            
        Returns:
            Minimal valid structure
        """
        return {
            "meeting_info": {
                "main_purpose": "Cuộc họp được ghi nhận từ audio",
                "topics_discussed": [],
                "participants_mentioned": []
            },
            "discussions": [
                {
                    "topic": "Nội dung cuộc họp",
                    "points": [
                        {
                            "speaker": None,
                            "content": transcript[:2000] + "..." if len(transcript) > 2000 else transcript,
                            "type": "opinion"
                        }
                    ],
                    "conclusion": None
                }
            ],
            "decisions": [],
            "action_items": [],
            "other_notes": "Lưu ý: Extraction tự động không thành công. Vui lòng xem transcript đầy đủ."
        }
```

#### Task 1.4: Refactor src/summarization/qwen_service.py
```python
# src/summarization/qwen_service.py

import requests
import json
from typing import Optional, Callable
from ..utils.logger import logger
from config.settings import SUMMARIZATION
from config.prompts import CHUNK_SUMMARIZE_PROMPT

class QwenService:
    """Qwen LLM service via Ollama"""
    
    def __init__(self, config=None):
        self.config = config or SUMMARIZATION
        self.base_url = self.config.base_url
    
    def summarize_chunk(self, chunk: str) -> str:
        """
        Summarize a single chunk of transcript
        
        Args:
            chunk: Text chunk to summarize
            
        Returns:
            Summarized text
        """
        prompt = CHUNK_SUMMARIZE_PROMPT.format(transcript=chunk)
        return self._call_ollama(prompt)
    
    def extract_json(self, prompt: str) -> str:
        """
        Extract structured JSON from text using custom prompt
        
        Args:
            prompt: Full prompt with schema and transcript
            
        Returns:
            Raw LLM response (should be JSON)
        """
        return self._call_ollama(prompt, temperature=0.1)  # Lower temperature for structured output
    
    def _call_ollama(self, prompt: str, temperature: Optional[float] = None) -> str:
        """
        Low-level Ollama API call
        
        Args:
            prompt: Input prompt
            temperature: Override temperature (optional)
            
        Returns:
            Model response text
        """
        url = f"{self.base_url}/api/generate"
        
        temp = temperature if temperature is not None else self.config.temperature
        
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temp,
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
            raise RuntimeError(f"Ollama API error: {e}")
    
    def check_connection(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
```

### Phase 2: DOCX Export (Priority: HIGH)

#### Task 2.1: Tạo src/export/__init__.py
```python
# src/export/__init__.py
"""Export modules"""
```

#### Task 2.2: Tạo src/export/docx_exporter.py
```python
# src/export/docx_exporter.py

from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from ..utils.logger import logger

class MeetingDocxExporter:
    """Export meeting data to DOCX format"""
    
    def __init__(self):
        self.doc = None
    
    def export(self, extracted_data: dict, output_path: str) -> str:
        """
        Generate DOCX from extracted JSON data
        
        Args:
            extracted_data: JSON từ MeetingExtractor
            output_path: Đường dẫn file output
            
        Returns:
            Path to generated file
        """
        self.doc = Document()
        self._setup_styles()
        
        # Build document
        self._add_header()
        self._add_metadata_placeholders()
        self._add_separator()
        self._add_purpose_section(extracted_data)
        self._add_discussion_section(extracted_data)
        self._add_decisions_section(extracted_data)
        self._add_action_items_table(extracted_data)
        self._add_other_notes(extracted_data)
        self._add_separator()
        self._add_signature_section()
        
        # Save
        self.doc.save(output_path)
        logger.info(f"DOCX exported: {output_path}")
        return output_path
    
    def _setup_styles(self):
        """Setup Times New Roman 13pt default"""
        style = self.doc.styles['Normal']
        style.font.name = 'Times New Roman'
        style.font.size = Pt(13)
        
        # Set font for East Asian text
        style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    
    def _add_header(self):
        """Add company name placeholder + title"""
        # Company name
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("CÔNG TY [_______________________]")
        run.bold = True
        run.font.size = Pt(14)
        
        # Title
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("BIÊN BẢN HỌP")
        run.bold = True
        run.font.size = Pt(16)
        
        # Document number
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("Số: _____/BB-__________")
        
        self.doc.add_paragraph()
    
    def _add_metadata_placeholders(self):
        """Add time, location, participants placeholders"""
        # Thời gian
        p = self.doc.add_paragraph()
        run = p.add_run("Thời gian: ")
        run.bold = True
        p.add_run("Ngày ___/___/______, từ ___:___ đến ___:___")
        
        # Địa điểm
        p = self.doc.add_paragraph()
        run = p.add_run("Địa điểm: ")
        run.bold = True
        p.add_run("[__________________________________________________]")
        
        # Hình thức
        p = self.doc.add_paragraph()
        run = p.add_run("Hình thức: ")
        run.bold = True
        p.add_run("☐ Trực tiếp    ☐ Trực tuyến    ☐ Kết hợp")
        
        self.doc.add_paragraph()
        
        # Thành phần tham dự
        p = self.doc.add_paragraph()
        run = p.add_run("THÀNH PHẦN THAM DỰ:")
        run.bold = True
        
        # Chủ trì
        p = self.doc.add_paragraph()
        run = p.add_run("Chủ trì: ")
        run.bold = True
        p.add_run("[______________________] - [_______________]")
        
        # Thư ký
        p = self.doc.add_paragraph()
        run = p.add_run("Thư ký: ")
        run.bold = True
        p.add_run("[______________________] - [_______________]")
        
        # Thành viên
        p = self.doc.add_paragraph()
        run = p.add_run("Thành viên:")
        run.bold = True
        
        for i in range(1, 6):
            p = self.doc.add_paragraph()
            p.add_run(f"   {i}. [______________________] - [_______________]")
        
        # Vắng mặt
        p = self.doc.add_paragraph()
        run = p.add_run("Vắng mặt: ")
        run.bold = True
        p.add_run("[__________________________________________________]")
    
    def _add_separator(self):
        """Add horizontal line separator"""
        p = self.doc.add_paragraph()
        p.add_run("─" * 70)
    
    def _add_purpose_section(self, data: dict):
        """Section I: Mục đích cuộc họp"""
        p = self.doc.add_paragraph()
        run = p.add_run("I. MỤC ĐÍCH CUỘC HỌP")
        run.bold = True
        
        meeting_info = data.get("meeting_info", {})
        purpose = meeting_info.get("main_purpose", "")
        
        p = self.doc.add_paragraph()
        if purpose:
            p.add_run(f"   {purpose}")
        else:
            p.add_run("   [Nội dung được AI tóm tắt từ cuộc họp]")
        
        self.doc.add_paragraph()
    
    def _add_discussion_section(self, data: dict):
        """Section II: Nội dung thảo luận"""
        p = self.doc.add_paragraph()
        run = p.add_run("II. NỘI DUNG THẢO LUẬN")
        run.bold = True
        
        discussions = data.get("discussions", [])
        
        if discussions:
            for i, disc in enumerate(discussions, 1):
                # Topic header
                p = self.doc.add_paragraph()
                run = p.add_run(f"   {i}. {disc.get('topic', 'Chủ đề')}")
                run.bold = True
                
                # Discussion points
                for point in disc.get("points", []):
                    speaker = point.get("speaker", "")
                    content = point.get("content", "")
                    
                    p = self.doc.add_paragraph()
                    if speaker:
                        run = p.add_run(f"      • {speaker}: ")
                        run.italic = True
                        p.add_run(content)
                    else:
                        p.add_run(f"      • {content}")
                
                # Conclusion
                conclusion = disc.get("conclusion")
                if conclusion:
                    p = self.doc.add_paragraph()
                    run = p.add_run("      → Kết luận: ")
                    run.bold = True
                    p.add_run(conclusion)
        else:
            p = self.doc.add_paragraph()
            p.add_run("   [Không có nội dung thảo luận được ghi nhận]")
        
        self.doc.add_paragraph()
    
    def _add_decisions_section(self, data: dict):
        """Section III: Các quyết định"""
        p = self.doc.add_paragraph()
        run = p.add_run("III. CÁC QUYẾT ĐỊNH")
        run.bold = True
        
        decisions = data.get("decisions", [])
        
        if decisions:
            for i, dec in enumerate(decisions, 1):
                p = self.doc.add_paragraph()
                p.add_run(f"   {i}. {dec.get('content', '')}")
        else:
            p = self.doc.add_paragraph()
            p.add_run("   [Không có quyết định được đưa ra]")
        
        self.doc.add_paragraph()
    
    def _add_action_items_table(self, data: dict):
        """Section IV: Bảng phân công công việc"""
        p = self.doc.add_paragraph()
        run = p.add_run("IV. PHÂN CÔNG CÔNG VIỆC")
        run.bold = True
        
        self.doc.add_paragraph()
        
        # Create table
        table = self.doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        
        # Header row
        header_cells = table.rows[0].cells
        headers = ["STT", "Nội dung công việc", "Người phụ trách", "Deadline"]
        for i, header in enumerate(headers):
            header_cells[i].text = header
            for paragraph in header_cells[i].paragraphs:
                for run in paragraph.runs:
                    run.bold = True
        
        # Data rows
        action_items = data.get("action_items", [])
        
        if action_items:
            for i, item in enumerate(action_items, 1):
                row = table.add_row().cells
                row[0].text = str(i)
                row[1].text = item.get("task", "")
                row[2].text = item.get("assignee") or "[___________]"
                row[3].text = item.get("deadline") or "[___/___]"
        else:
            # Empty rows for manual fill
            for i in range(1, 4):
                row = table.add_row().cells
                row[0].text = str(i)
                row[1].text = ""
                row[2].text = "[___________]"
                row[3].text = "[___/___]"
        
        self.doc.add_paragraph()
    
    def _add_other_notes(self, data: dict):
        """Section V: Ý kiến khác"""
        p = self.doc.add_paragraph()
        run = p.add_run("V. Ý KIẾN KHÁC")
        run.bold = True
        
        notes = data.get("other_notes", "")
        
        p = self.doc.add_paragraph()
        if notes:
            p.add_run(f"   {notes}")
        else:
            p.add_run("   [Không có]")
        
        self.doc.add_paragraph()
    
    def _add_signature_section(self):
        """Footer with signature placeholders"""
        p = self.doc.add_paragraph()
        p.add_run("Cuộc họp kết thúc vào lúc ___:___, cùng ngày.")
        
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        
        # Signature table
        table = self.doc.add_table(rows=4, cols=2)
        
        # Row 1: Titles
        table.cell(0, 0).text = "THƯ KÝ"
        table.cell(0, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in table.cell(0, 0).paragraphs[0].runs:
            run.bold = True
        
        table.cell(0, 1).text = "CHỦ TRÌ"
        table.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in table.cell(0, 1).paragraphs[0].runs:
            run.bold = True
        
        # Row 2: Instructions
        table.cell(1, 0).text = "(Ký, ghi rõ họ tên)"
        table.cell(1, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.cell(1, 1).text = "(Ký, ghi rõ họ tên)"
        table.cell(1, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Row 3: Empty space
        table.cell(2, 0).text = ""
        table.cell(2, 1).text = ""
        
        # Row 4: Signature line
        table.cell(3, 0).text = "_______________________"
        table.cell(3, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.cell(3, 1).text = "_______________________"
        table.cell(3, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
```

### Phase 3: Update Pipeline (Priority: HIGH)

#### Task 3.1: Update src/pipeline/meeting_pipeline.py
```python
# Thêm imports và update class MeetingPipeline

# Thêm vào đầu file:
from ..summarization.chunker import TextChunker
from ..summarization.extractor import MeetingExtractor
from ..export.docx_exporter import MeetingDocxExporter

# Update __init__:
def __init__(self):
    self.audio_processor = AudioProcessor()
    self.whisper_service = WhisperService()
    self.qwen_service = QwenService()
    self.chunker = TextChunker()
    self.extractor = MeetingExtractor(self.qwen_service)
    self.docx_exporter = MeetingDocxExporter()

# Update process method để return thêm docx_path
# Thêm logic chunking và extraction
# Gọi docx_exporter.export() ở cuối
```

### Phase 4: Update Backend & Frontend (Priority: MEDIUM)

#### Task 4.1: Update app/backend.py
- Thêm `docx` vào job result
- Update download endpoint để support docx
- Đảm bảo CORS cho file download

#### Task 4.2: Update app/static/index.html
- Thêm button "Tải Biên bản (DOCX)"
- Style cho button mới

---

## 📦 Dependencies cần thêm

```txt
# Thêm vào requirements_fastapi.txt

# DOCX Export
python-docx>=0.8.11
```

Cài đặt:
```bash
pip install python-docx --break-system-packages
```

---

## 🧪 Testing Checklist

### Unit Tests
- [ ] TextChunker.chunk() với text dài
- [ ] TextChunker.should_chunk() threshold
- [ ] MeetingExtractor.extract() với transcript thật
- [ ] MeetingExtractor._validate_json() với invalid JSON
- [ ] MeetingExtractor._fallback_extraction()
- [ ] MeetingDocxExporter.export() output valid DOCX
- [ ] QwenService.summarize_chunk()
- [ ] QwenService.extract_json()

### Integration Tests
- [ ] Full pipeline với file audio 5 phút
- [ ] Full pipeline với file audio 30 phút
- [ ] Full pipeline với file audio 1-2 giờ
- [ ] DOCX mở được trong MS Word
- [ ] DOCX mở được trong Google Docs
- [ ] DOCX có đúng format tiếng Việt

### Demo Checklist
- [ ] Upload file hoạt động
- [ ] Progress bar cập nhật real-time
- [ ] Download transcript TXT
- [ ] Download DOCX biên bản
- [ ] DOCX có đủ 5 sections
- [ ] DOCX có placeholders để điền
- [ ] Font Times New Roman 13pt

---

## ⏱️ Timeline ước tính

| Phase | Tasks | Thời gian |
|-------|-------|-----------|
| Phase 1 | Refactor Summarization | 2-3 giờ |
| Phase 2 | DOCX Export | 2-3 giờ |
| Phase 3 | Update Pipeline | 1-2 giờ |
| Phase 4 | Update Backend/Frontend | 1 giờ |
| Testing | Full testing | 2 giờ |
| **Total** | | **8-11 giờ** |

---

## 🚀 Execution Order cho Claude Code CLI

```bash
# Thứ tự thực hiện:

1. Đọc và hiểu codebase hiện tại
   - Xem src/summarization/qwen_service.py
   - Xem src/pipeline/meeting_pipeline.py
   - Xem app/backend.py

2. Tạo config/prompts.py
   - CHUNK_SUMMARIZE_PROMPT
   - EXTRACTION_PROMPT
   - EXTRACTION_SCHEMA

3. Tạo src/summarization/chunker.py
   - Class TextChunker

4. Tạo src/summarization/extractor.py
   - Class MeetingExtractor

5. Refactor src/summarization/qwen_service.py
   - Thêm summarize_chunk()
   - Thêm extract_json()
   - Giữ backward compatible

6. Tạo src/export/__init__.py

7. Tạo src/export/docx_exporter.py
   - Class MeetingDocxExporter

8. Update src/pipeline/meeting_pipeline.py
   - Import new modules
   - Add chunking logic
   - Add extraction logic
   - Add DOCX export

9. Update app/backend.py
   - Add docx to job result
   - Update download endpoint

10. Update app/static/index.html
    - Add DOCX download button

11. Test end-to-end với file audio thật

12. Fix bugs nếu có

13. DONE - Sẵn sàng demo!
```

---

## 📝 Lưu ý quan trọng cho Claude Code CLI

1. **KHÔNG SỬA** các file đang hoạt động tốt:
   - `src/transcription/whisper_service.py` ✓
   - `src/transcription/audio_processor.py` ✓
   - `src/utils/*` ✓

2. **REFACTOR cẩn thận**:
   - `src/summarization/qwen_service.py` - thêm methods mới, giữ methods cũ
   - `src/pipeline/meeting_pipeline.py` - thêm logic mới

3. **TẠO MỚI**:
   - `config/prompts.py`
   - `src/summarization/chunker.py`
   - `src/summarization/extractor.py`
   - `src/export/__init__.py`
   - `src/export/docx_exporter.py`

4. **Test sau mỗi phase** để đảm bảo không break existing functionality

5. **Output files** lưu vào `output/` folder

6. **Error handling** đầy đủ với logging

7. **Tiếng Việt** - tất cả messages và output phải hỗ trợ Unicode

---

## ✅ Success Criteria

Demo thành công khi:

1. ✅ Upload file M4A/MP4 → Xử lý không lỗi
2. ✅ Progress bar hiển thị đúng tiến trình
3. ✅ Transcript tiếng Việt chính xác >90%
4. ✅ JSON extraction có đủ fields
5. ✅ DOCX có đủ 5 sections theo template
6. ✅ DOCX có placeholders cho metadata
7. ✅ DOCX dùng font Times New Roman 13pt
8. ✅ Tổng thời gian xử lý file 1 giờ < 15 phút
9. ✅ Giám khảo ấn tượng với output quality

---

## 🎯 Điểm khác biệt để nhấn mạnh khi demo

1. **Vietnamese-first AI** - Tối ưu cho tiếng Việt doanh nghiệp
2. **Privacy-first** - Chạy hoàn toàn local, không upload cloud
3. **Enterprise-grade output** - Biên bản chuẩn pháp lý VN
4. **Practical** - Thư ký chỉ cần điền metadata, nội dung AI lo
