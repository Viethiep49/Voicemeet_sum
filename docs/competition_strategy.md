# 🎬 Competition Strategy - IT GOTTALENT 2025

**Tài liệu này chứa:** Demo script, pitch deck outline, visual design, checklist

---

## 📋 CẤU TRÚC PRESENTATION (5-7 phút)

### Timeline Chi Tiết

```
⏱️ Minute 0-1: Hook + Problem
  "Bạn có biết mỗi nhân viên văn phòng mất trung bình 2-3 giờ
   sau mỗi cuộc họp để viết biên bản? Và 60% thông tin bị quên?"

  → Show pain points visual (chart/infographic)

⏱️ Minute 1-2: Solution Overview
  "Voicemeet_sum giúp bạn tiết kiệm 95% thời gian đó!"

  → Architecture diagram (clean, visual)
  → Key technologies showcase

⏱️ Minute 2-5: LIVE DEMO
  🎯 Demo 1: Upload file (30 sec)
    - Kéo thả file audio mẫu
    - Show progress bar, processing status

  🎯 Demo 2: Show results (1 min)
    - Transcript hiển thị
    - Summary highlights key points
    - Compare with manual notes (show savings)

  🎯 Demo 3: Multi-language (1 min)
    - Demo file có Việt + Nhật
    - Show accuracy

  🎯 Demo 4: Special features (1 min)
    - Speaker diarization (nếu có)
    - Action items extraction (nếu có)
    - Export formats

⏱️ Minute 5-6: Impact & Use Cases
  → Show metrics:
    - Time saved: 50 hours/month
    - Cost saved: $0 vs $10/user/month competitors
    - Accuracy: 92-95%

  → Real use cases (3 examples)

⏱️ Minute 6-7: Technical Highlights + Q&A
  → Tech stack showcase
  → GitHub repo, documentation
  → Future roadmap
  → Open for questions
```

---

## 🎤 DEMO SCRIPT (Word-by-Word)

### INTRO - 30 seconds
```
"Xin chào Ban Giám Khảo! Tôi là [Tên], đại diện team [Tên team].

Hôm nay tôi muốn giới thiệu Voicemeet_sum - giải pháp AI giúp
tiết kiệm 95% thời gian viết biên bản cuộc họp.

[Click to problem slide]

Bạn có biết, mỗi nhân viên văn phòng trung bình mất 2-3 giờ
sau MỖI cuộc họp để ghi chép và viết biên bản? Với 20 meetings
mỗi tháng, đó là 50 giờ - hơn 1 tuần làm việc - bị lãng phí!
```

### SOLUTION - 30 seconds
```
[Click to solution slide]

Voicemeet_sum tự động chuyển đổi audio cuộc họp thành văn bản
và tóm tắt thông minh. Chỉ cần 10 phút thay vì 3 giờ!

[Click to architecture]

Hệ thống sử dụng Faster-Whisper cho Speech Recognition và
Qwen 2.5 LLM cho tóm tắt - tất cả chạy OFFLINE trên GPU.
```

### DEMO - 3 minutes
```
[Switch to browser]

Bây giờ tôi sẽ demo trực tiếp. Đây là file recording của
1 cuộc họp 2 tiếng bàn về menu nhà hàng, có cả tiếng Việt
và tiếng Nhật.

[Drag & drop file]

Tôi kéo thả file vào... Và hệ thống bắt đầu xử lý.

[Point to progress bar]

Progress bar hiển thị real-time. Giai đoạn 1 là preprocessing
audio với FFmpeg, giai đoạn 2 là Whisper transcription,
giai đoạn 3 là Qwen summarization.

[Wait/Speed up or show pre-processed]

Và đây là kết quả!

[Show transcript]

Transcript đầy đủ với độ chính xác 95%. Nhìn thấy không,
nó hiểu cả từ "phở", "bún", và cả "ラーメン" (ramen)
tiếng Nhật!

[Scroll to summary]

Và đây là summary - tự động extract:
- Key points discussed
- Decisions made
- Action items
- Timeline

[Show metrics]

Từ 2 giờ audio → 10 phút processing. Time saved: 2 giờ 50 phút!
```

### IMPACT - 1 minute
```
[Click to impact slide]

Impact thực tế:
- 1 công ty 50 người × 20 meetings/tháng = tiết kiệm 1000 giờ
- Equivalent $15,000/tháng labor cost
- 100% data privacy - không data nào lên cloud
- $0 recurring cost vs $500/tháng với competitors
```

### TECHNICAL - 30 seconds
```
[Click to tech slide]

Technical highlights:
✅ Faster-Whisper: 10-13x realtime speed
✅ CUDA GPU acceleration
✅ Multi-language: Việt, Nhật, Anh
✅ FastAPI backend
✅ 100% open-source foundation
```

### CLOSING - 30 seconds
```
[Click to roadmap]

Roadmap tiếp theo:
- Speaker diarization
- Realtime transcription
- Mobile app
- Integration với Teams, Zoom

[Click to thank you slide]

Cảm ơn Ban Giám Khảo đã lắng nghe!
Tôi sẵn sàng trả lời câu hỏi!"
```

---

## 🚀 PITCH DECK OUTLINE

### Slide 1: Title
```
┌─────────────────────────────────────┐
│   🎤 VOICEMEET_SUM                  │
│                                      │
│   AI-Powered Meeting Transcription  │
│   & Summarization                    │
│                                      │
│   Team: [Your Team Name]             │
│   IT GOTTALENT 2025                  │
└─────────────────────────────────────┘
```

### Slide 2: The Problem
```
┌─────────────────────────────────────┐
│   💼 THE PROBLEM                    │
│                                      │
│   [Icon] 2-3 hours wasted           │
│           per meeting on notes       │
│                                      │
│   [Icon] 60% of information lost    │
│                                      │
│   [Icon] Language barriers          │
│           in international teams     │
│                                      │
│   [Icon] No searchable records      │
│                                      │
│   Cost: 50 hours/month/person       │
└─────────────────────────────────────┘
```

### Slide 3: Our Solution
```
┌─────────────────────────────────────┐
│   ✨ THE SOLUTION                   │
│                                      │
│   Voicemeet_sum automatically:      │
│                                      │
│   ✅ Transcribes audio → text       │
│      (95% accuracy, 10x realtime)   │
│                                      │
│   ✅ Summarizes key points          │
│      (AI-powered, multilingual)     │
│                                      │
│   ✅ Extracts action items          │
│      (ready-to-use checklist)       │
│                                      │
│   2 hours → 10 minutes!             │
└─────────────────────────────────────┘
```

### Slide 4-12: [See full outline in original doc]
- Slide 4: Architecture
- Slide 5: Live Demo
- Slide 6: Key Features
- Slide 7: Market Comparison
- Slide 8: Use Cases
- Slide 9: Impact & ROI
- Slide 10: Tech Stack
- Slide 11: Roadmap
- Slide 12: Team & Contact

---

## 🎨 VISUAL DESIGN GUIDELINES

### Color Scheme
```css
Primary:    #2563EB (Blue - trust, technology)
Secondary:  #7C3AED (Purple - innovation, AI)
Accent:     #F59E0B (Orange - energy, action)
Success:    #10B981 (Green - completion)
Error:      #EF4444 (Red - warnings)
Background: #F9FAFB (Light gray)
Text:       #111827 (Near black)
```

### Typography
```
Headings: Inter/Poppins (Bold, modern, clean)
Body:     Inter/Roboto (Readable, professional)
Code:     JetBrains Mono (Monospace)

Sizes:
H1: 48px (Title slide)
H2: 36px (Section headers)
H3: 24px (Subsections)
Body: 18px (Readable from distance)
```

### Layout Principles
- ✅ White space (don't crowd slides)
- ✅ One idea per slide
- ✅ Visual hierarchy
- ✅ High contrast
- ✅ Minimal text (visuals > words)

---

## ✅ COMPETITION CHECKLIST

### 1 Week Before

**Technical Preparation:**
- [ ] Code review (remove debug code)
- [ ] Test on fresh machine
- [ ] Pre-load models (Whisper, Qwen)
- [ ] Prepare 3-4 demo audio files
- [ ] Pre-process demo files (backup)
- [ ] Battery fully charged
- [ ] USB backup (code + data + slides)

**Presentation Preparation:**
- [ ] Finalize slides (proofread)
- [ ] Record backup demo video
- [ ] Practice pitch (time: 5-7 min)
- [ ] Practice Q&A
- [ ] Prepare professional clothes

**Materials:**
- [ ] Business cards
- [ ] GitHub repo public
- [ ] Contact info ready

### Day Before
- [ ] Get 8 hours sleep
- [ ] Charge all devices
- [ ] Pack bag (laptop, charger, USB)
- [ ] Review slides once
- [ ] Quick demo run-through

### Day Of Competition

**Morning:**
- [ ] Eat good breakfast
- [ ] Arrive 30 min early
- [ ] Test equipment
- [ ] Run demo once
- [ ] Deep breaths, relax

**During:**
- [ ] Smile, eye contact
- [ ] Speak clearly
- [ ] Show enthusiasm
- [ ] Handle questions calmly
- [ ] Thank judges

**After:**
- [ ] Network with teams
- [ ] Gather feedback
- [ ] Take notes
- [ ] Celebrate!

---

## 🎖️ COMPETITION SCORING

### Judging Criteria (100 points)

**1. Innovation & Creativity (25 points)**
- Novel SOTA AI application
- Offline-first approach (rare)
- Multi-language for SEA
- End-to-end pipeline
→ Target: 20-22/25

**2. Technical Complexity (25 points)**
- Multi-model AI pipeline
- GPU optimization
- Async architecture
- Production-ready code
→ Target: 22-24/25

**3. Practicality & Impact (25 points)**
- Real pain point solved
- Immediate ROI
- Multiple use cases
- Scalable business
→ Target: 21-23/25

**4. Presentation & Demo (25 points)**
- Live demo (working)
- Clear value proposition
- Professional slides
- Confident delivery
→ Target: 20-22/25

**Total Target: 83-91/100** (Very competitive!)

---

## 💡 TIPS FOR SUCCESS

### Presentation Tips
1. **Hook them early** - Start with relatable problem
2. **Show, don't tell** - Live demo > talking
3. **Use numbers** - Metrics are powerful
4. **Tell stories** - Use case scenarios
5. **Practice timing** - Stay within 5-7 min

### Demo Tips
1. **Have backup** - Pre-recorded video ready
2. **Test everything** - Before you go on stage
3. **Speak while processing** - Explain what's happening
4. **Highlight unique features** - Offline, Vietnamese
5. **Show impact** - Time/cost savings

### Q&A Tips
1. **Listen fully** - Don't interrupt
2. **Pause before answering** - Think first
3. **Be honest** - Admit if you don't know
4. **Bridge to strengths** - Redirect to what you know
5. **Stay calm** - Even with tough questions

---

## 📚 VISUAL ASSETS NEEDED

### Slides/Presentation
- Title slide with logo
- Problem statement infographic
- Architecture diagram (clean, visual)
- Tech stack logos
- Competitive comparison table
- Use case illustrations
- Metrics charts
- Roadmap timeline
- Team photos + contact

### Demo Materials
- 3-4 demo audio files:
  - File 1: Pure Vietnamese (5 min)
  - File 2: Vietnamese + Japanese (5 min)
  - File 3: Business meeting (10 min)
  - File 4: Technical discussion (10 min)

### Screenshots
- Web UI (before & after)
- Sample transcript
- Sample summary
- Metrics dashboard

### Backup
- Screen recording of full workflow (3-4 min)
- Speed up processing parts
- Add annotations

---

## 🎯 KEY MESSAGES TO EMPHASIZE

1. **95% time savings** - From 3 hours to 10 minutes
2. **100% offline** - Privacy-first, data never leaves machine
3. **92-95% Vietnamese accuracy** - Better than competitors
4. **$0 recurring cost** - vs $8-10/user/month
5. **10-13x realtime speed** - Fast processing
6. **Multi-language native** - Việt-Nhật-Anh code-switching

---

**Remember:** Make judges say "I want to use this!"

Focus on VALUE, not just features.
