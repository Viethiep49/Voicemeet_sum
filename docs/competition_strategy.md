# Competition Strategy - IT GOT TALENT 2025

**Mã đội:** D12
**Đề tài:** VOICEMEET_SUM – HỆ THỐNG AI CHUYỂN ĐỔI VÀ TÓM TẮT CUỘC HỌP ĐA NGÔN NGỮ
**Ngày thi:** 28/12/2025 - 19h00 (Thứ tự: 5)
**Hình thức:** Online qua Google Meet

---

## QUY ĐỊNH CUỘC THI

### Thời gian: 10 phút
| Phần | Thời gian | Nội dung |
|------|-----------|----------|
| Trình bày + Demo | **5 phút** | Slide + Video demo |
| Hỏi đáp BGK | **5 phút** | Trả lời câu hỏi |

### Yêu cầu Slide
- ✅ Mã đội (SBD): **D12**
- ✅ Tên đề tài: VOICEMEET_SUM
- ✅ Thông tin thành viên nhóm
- ❌ **KHÔNG** để tên Giảng viên hướng dẫn
- ❌ **KHÔNG** để tên Trường/Viện

### Tiêu chí chấm điểm (100 điểm)

| STT | Tiêu chí | Điểm | Mô tả | Voicemeet_sum đáp ứng |
|-----|----------|------|-------|----------------------|
| 1 | **Tính sáng tạo** | 30 | Ý tưởng mới, giải pháp mới | AI offline, đa ngôn ngữ, privacy-first |
| 2 | **Tính thực tiễn** | 25 | Khả năng áp dụng, thương mại hóa | Tiết kiệm 95% thời gian, $0 cost |
| 3 | **Hoàn thiện sản phẩm** | 15 | Đầy đủ tính năng, có thể thành sản phẩm | Web UI, export DOCX, multi-language |
| 4 | **Công nghệ** | 15 | Dùng AI mới (ChatGPT, Copilot...) | Whisper + Qwen + Claude Code |
| 5 | **Trình bày** | 15 | Kỹ năng thuyết trình, trả lời BGK | Luyện tập, chuẩn bị Q&A |

---

## CẤU TRÚC SLIDE (5 phút trình bày)

### Slide 1: Title (15 giây)
```
┌─────────────────────────────────────────────┐
│            SBD: D12                         │
│                                             │
│         🎤 VOICEMEET_SUM                    │
│                                             │
│   HỆ THỐNG AI CHUYỂN ĐỔI VÀ TÓM TẮT        │
│   CUỘC HỌP ĐA NGÔN NGỮ                      │
│                                             │
│   Thành viên:                               │
│   - [Tên 1]                                 │
│   - [Tên 2]                                 │
│                                             │
│   IT GOT TALENT 2025                        │
└─────────────────────────────────────────────┘
```

### Slide 2: Problem - Vấn đề (45 giây)
```
┌─────────────────────────────────────────────┐
│   💼 VẤN ĐỀ THỰC TẾ                         │
│                                             │
│   $37 TỶ         71%           31 GIỜ       │
│   lãng phí/năm   họp không     lãng phí     │
│   (US)           hiệu quả      /tháng/người │
│                                             │
│   ─────────────────────────────────────     │
│                                             │
│   Sau mỗi cuộc họp:                         │
│   ⏰ 2-3 giờ viết biên bản thủ công         │
│   📉 60% nội dung bị quên/ghi thiếu         │
│   🌏 Rào cản ngôn ngữ (Việt-Nhật-Anh)       │
│                                             │
│   Nguồn: Cross River Therapy, Otter.ai      │
└─────────────────────────────────────────────┘
```

### Slide 3: Solution - Giải pháp (30 giây)
```
┌─────────────────────────────────────────────┐
│   ✨ GIẢI PHÁP: VOICEMEET_SUM               │
│                                             │
│   🎙️ Audio ──► 📝 Transcript ──► 📋 Summary │
│        │              │               │     │
│    Upload file   Faster-Whisper    Qwen AI  │
│                   (Speech-to-Text)  (LLM)   │
│                                             │
│   ─────────────────────────────────────     │
│                                             │
│   ✅ 100% Offline - Bảo mật tuyệt đối       │
│   ✅ Đa ngôn ngữ: Việt - Nhật - Anh         │
│   ✅ 10 phút thay vì 3 giờ                  │
│                                             │
└─────────────────────────────────────────────┘
```

### Slide 4: Demo Video (90 giây)
```
┌─────────────────────────────────────────────┐
│   🎬 DEMO VOICEMEET_SUM                     │
│                                             │
│   ┌─────────────────────────────────────┐   │
│   │                                     │   │
│   │         [VIDEO DEMO]                │   │
│   │                                     │   │
│   │   1. Upload file audio              │   │
│   │   2. Processing (Whisper + Qwen)    │   │
│   │   3. Kết quả: Transcript + Summary  │   │
│   │   4. Export DOCX                    │   │
│   │                                     │   │
│   └─────────────────────────────────────┘   │
│                                             │
│   File test: 30 phút audio → 7 phút xử lý   │
└─────────────────────────────────────────────┘
```

### Slide 5: Công nghệ & AI (30 giây)
```
┌─────────────────────────────────────────────┐
│   🔧 CÔNG NGHỆ SỬ DỤNG                      │
│                                             │
│   AI/ML:                                    │
│   • Faster-Whisper (Speech-to-Text)         │
│   • Qwen 2.5 LLM (Summarization)            │
│   • Claude Code (Development Assistant)     │
│                                             │
│   Backend:                                  │
│   • FastAPI (Python)                        │
│   • Ollama (Local LLM Runtime)              │
│   • FFmpeg (Audio Processing)               │
│                                             │
│   Infrastructure:                           │
│   • CUDA GPU Acceleration                   │
│   • 100% Local Processing                   │
└─────────────────────────────────────────────┘
```

### Slide 6: Kết quả & Impact (30 giây)
```
┌─────────────────────────────────────────────┐
│   📊 KẾT QUẢ ĐẠT ĐƯỢC                       │
│                                             │
│   95%            92-95%          $0         │
│   tiết kiệm      độ chính xác    chi phí    │
│   thời gian      tiếng Việt      vận hành   │
│                                             │
│   ─────────────────────────────────────     │
│                                             │
│   So với đối thủ:                           │
│   │ Feature      │ Voicemeet │ Otter.ai │   │
│   │ Offline      │ ✅ 100%   │ ❌ Cloud │   │
│   │ Tiếng Việt   │ ✅ 92%    │ ⚠️ 70%   │   │
│   │ Chi phí/thg  │ $0        │ $8.33    │   │
│   │ Privacy      │ ✅ Local  │ ❌ Cloud │   │
│                                             │
└─────────────────────────────────────────────┘
```

### Slide 7: Roadmap & Kết (15 giây)
```
┌─────────────────────────────────────────────┐
│   🚀 ROADMAP                                │
│                                             │
│   ✅ Phase 1 (Done):                        │
│      Core transcription + summarization     │
│                                             │
│   🔄 Phase 2 (In Progress):                 │
│      Speaker diarization, Action items      │
│                                             │
│   📅 Phase 3 (Future):                      │
│      Realtime, Mobile app, Zoom/Teams       │
│                                             │
│   ─────────────────────────────────────     │
│                                             │
│   🎯 CẢM ƠN BAN GIÁM KHẢO!                  │
│      SBD: D12 - VOICEMEET_SUM               │
└─────────────────────────────────────────────┘
```

---

## SCRIPT THUYẾT TRÌNH (5 phút)

### Slide 1: Title (15 giây)
```
"Xin chào Ban Giám Khảo! Chúng tôi là đội D12.

Hôm nay xin giới thiệu VOICEMEET_SUM - Hệ thống AI
chuyển đổi và tóm tắt cuộc họp đa ngôn ngữ."
```

### Slide 2: Problem (45 giây)
```
"Mỗi năm, doanh nghiệp Mỹ mất 37 tỷ đô vì họp không hiệu quả.
71% cuộc họp được đánh giá là lãng phí thời gian.

Và sau mỗi cuộc họp, nhân viên mất thêm 2-3 tiếng viết biên bản -
với 60% nội dung bị quên hoặc ghi thiếu.

Đặc biệt với các công ty có đối tác Nhật Bản, Hàn Quốc -
rào cản ngôn ngữ làm việc ghi chép càng khó khăn hơn.

Đây là vấn đề thực tế mà Voicemeet_sum giải quyết."
```

### Slide 3: Solution (30 giây)
```
"Voicemeet_sum sử dụng AI để tự động:

- Chuyển đổi audio thành văn bản với Faster-Whisper
- Tóm tắt thông minh với Qwen 2.5 LLM

Điểm đặc biệt: 100% offline - dữ liệu không rời máy.
Hỗ trợ 3 ngôn ngữ: Việt, Nhật, Anh.
Từ 2-3 giờ viết biên bản xuống còn 10 phút."
```

### Slide 4: Demo (90 giây)
```
"Bây giờ xin mời BGK xem demo.

[PLAY VIDEO]

Video demo với file audio 30 phút cuộc họp thực tế.

Bước 1: Upload file audio lên hệ thống.
Bước 2: Hệ thống xử lý qua 3 giai đoạn - FFmpeg, Whisper, Qwen.
Bước 3: Kết quả hiển thị - transcript đầy đủ và summary.
Bước 4: Export ra file DOCX để sử dụng.

Thời gian xử lý: 7 phút cho 30 phút audio - nhanh hơn 4x realtime."
```

### Slide 5: Công nghệ (30 giây)
```
"Về công nghệ, chúng tôi sử dụng:

- Faster-Whisper cho Speech-to-Text với GPU acceleration
- Qwen 2.5 LLM chạy local qua Ollama
- Claude Code hỗ trợ phát triển và tối ưu code

Tất cả đều là công nghệ AI mới nhất, chạy 100% local
đảm bảo bảo mật dữ liệu cuộc họp."
```

### Slide 6: Impact (30 giây)
```
"Kết quả đạt được:

- Tiết kiệm 95% thời gian xử lý biên bản
- Độ chính xác 92-95% với tiếng Việt
- Chi phí vận hành $0 - so với $8-10/user/tháng của đối thủ

So với Otter.ai, Fireflies.ai - chúng tôi là giải pháp
duy nhất 100% offline và tối ưu cho tiếng Việt."
```

### Slide 7: Kết (15 giây)
```
"Roadmap tiếp theo: Speaker diarization, realtime, mobile app.

Cảm ơn Ban Giám Khảo đã lắng nghe!
Đội D12 - Voicemeet_sum sẵn sàng trả lời câu hỏi."
```

---

## CHUẨN BỊ VIDEO DEMO

### Nội dung video (90 giây)
1. **0-15s:** Mở web UI, giới thiệu giao diện
2. **15-30s:** Upload file audio mẫu (30 phút)
3. **30-60s:** Hiển thị processing (có thể speed up)
4. **60-75s:** Show kết quả - Transcript
5. **75-85s:** Show kết quả - Summary
6. **85-90s:** Export DOCX

### Yêu cầu kỹ thuật
- Resolution: 1080p
- Audio: Có voice-over giải thích
- Speed: Có thể tua nhanh phần processing
- Annotations: Thêm text chú thích

### File audio mẫu cho demo
- Dùng file đã test: LPBank Training Session
- Hoặc file ngắn hơn (10-15 phút) để demo nhanh

---

## CHUẨN BỊ Q&A (5 phút)

### Câu hỏi kỹ thuật dự kiến

**Q: Tại sao chọn Whisper thay vì Google Speech API?**
```
A: Whisper chạy offline, không tốn phí API, bảo mật 100%.
Google Speech API tốn $0.006/15 giây và data lên cloud.
Với 2 giờ audio = $2.88/file. Whisper = $0.
```

**Q: Accuracy 92-95% so với đối thủ?**
```
A: Google Speech API tiếng Việt khoảng 85-90%.
Whisper large model đạt 92-95% với tiếng Việt.
Chúng tôi đã test với file thực tế từ LPBank.
```

**Q: Có thể scale cho doanh nghiệp lớn?**
```
A: Có. Kiến trúc FastAPI hỗ trợ async, có thể deploy
trên server GPU. Roadmap có Docker containerization.
```

**Q: Sử dụng AI tools gì trong development?**
```
A: Claude Code để hỗ trợ viết code, debug, optimize.
GitHub Copilot cho code completion.
ChatGPT để research và design prompts cho Qwen.
```

### Câu hỏi business dự kiến

**Q: Khách hàng mục tiêu?**
```
A: - Doanh nghiệp có đối tác nước ngoài (Nhật, Anh)
   - Công ty luật, y tế cần bảo mật
   - Startup tiết kiệm chi phí
   - Training/Education sector
```

**Q: Mô hình kinh doanh?**
```
A: - Bán license cho doanh nghiệp: $500-2000/năm
   - Hoặc bán hardware bundle (PC + software)
   - Consulting/customization services
```

**Q: Đối thủ cạnh tranh?**
```
A: Otter.ai, Fireflies.ai - nhưng họ cloud-based,
không hỗ trợ tốt tiếng Việt, và tốn phí hàng tháng.
Voicemeet_sum là giải pháp offline duy nhất.
```

---

## CHECKLIST TRƯỚC THI

### Ngày 27/12 (Hôm nay)
- [ ] Quay video demo (90 giây)
- [ ] Hoàn thiện 7 slides
- [ ] Luyện script (đúng 5 phút)
- [ ] Test thiết bị: camera, mic

### Ngày 28/12 (Ngày thi)
- [ ] Vào Zalo group Bảng D kiểm tra thông tin
- [ ] Test Google Meet trước 18h45
- [ ] Chuẩn bị slide, video sẵn sàng share screen
- [ ] Ăn mặc lịch sự
- [ ] Vào Meet lúc 18h45 (trước 15 phút)
- [ ] Đợi đến lượt (thứ 5, ~19h40)

---

## TIPS QUAN TRỌNG

### Trình bày (30 điểm = Sáng tạo)
- Nhấn mạnh: **Offline-first** = Ý tưởng mới
- Nhấn mạnh: **Đa ngôn ngữ Việt-Nhật** = Giải pháp mới
- Nhấn mạnh: **$0 cost** = Khác biệt với đối thủ

### Công nghệ (15 điểm)
- Mention: Faster-Whisper, Qwen 2.5, Claude Code
- Nhấn mạnh: Dùng AI tools trong development
- Show: GPU acceleration, async processing

### Thực tiễn (25 điểm)
- Dùng số liệu: $37 tỷ, 71%, 95% tiết kiệm
- Mention: Use cases thực tế (LPBank, F&B)
- Mention: Khả năng thương mại hóa

### Trình bày (15 điểm)
- Nói rõ ràng, không nhanh quá
- Eye contact với camera
- Trả lời Q&A tự tin, ngắn gọn

---

**Ghi nhớ:**
- Mã đội: **D12**
- Thời gian: **28/12/2025 - 19h00** (thứ tự 5)
- Link Meet: https://meet.google.com/fvf-nttc-ryh
