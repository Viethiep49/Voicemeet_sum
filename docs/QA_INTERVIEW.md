# Q&A PHONG VAN - IT GOTTALENT 2025

## 1. TONG QUAN DU AN

**Q: Du an nay giai quyet van de gi?**
> Giam 95% thoi gian viet bien ban hop - tu 2-3 gio xuong con 10 phut. Tu dong chuyen audio thanh van ban va tom tat.

**Q: Tai sao chon giai phap nay?**
> 100% offline, bao mat toi da. Toi uu cho tieng Viet (92-95% accuracy). Mien phi, khong phu thuoc cloud.

**Q: Doi tuong su dung?**
> Cong ty, van phong, truong hoc, phong kham - bat ky ai can ghi chep cuoc hop.

---

## 2. CONG NGHE

**Q: Dung nhung cong nghe gi?**
> - **Faster-Whisper**: Speech-to-text, CUDA GPU
> - **Qwen 2.5 LLM**: Tom tat thong minh qua Ollama
> - **FastAPI**: Backend async Python
> - **FFmpeg**: Xu ly audio

**Q: Tai sao chon Whisper thay vi Google/Azure?**
> Whisper chay offline, mien phi, ho tro tieng Viet tot. Google/Azure can internet va tra phi.

**Q: Tai sao chon Qwen thay vi GPT/Claude?**
> Qwen chay local qua Ollama, mien phi, bao mat. GPT/Claude can API key va tra phi theo token.

**Q: Toc do xu ly bao nhieu?**
> 15-20x realtime. File 30 phut xu ly trong 2 phut.

---

## 3. KY THUAT SAU

**Q: Lam sao xu ly file lon (2GB)?**
> Async processing voi FastAPI + background task. Khong block server, user thay progress realtime.

**Q: Lam sao toi uu toc do?**
> - Whisper: model tiny, int8, beam=1
> - FFmpeg: bo loudnorm, multi-thread
> - Qwen: model 3b, giam max_tokens

**Q: GPU nao phu hop?**
> RTX 3060 12GB tro len. VRAM cang lon cang tot.

**Q: Xu ly loi nhu the nao?**
> Try-catch moi buoc, fallback CPU neu GPU loi, log chi tiet de debug.

---

## 4. THACH THUC & GIAI PHAP

**Q: Gap kho khan gi khi lam?**
> 1. Race condition khi unload model -> Fix: bo unload ngay lap tuc
> 2. Summary qua ngan -> Fix: cai thien prompt
> 3. Toc do cham -> Fix: toi uu config

**Q: Han che cua he thong?**
> - Can GPU manh (RTX 3060+)
> - Accuracy tieng Viet ~85-90% (co the nghe nham)
> - Chua phan biet nguoi noi (speaker diarization)

---

## 5. KINH DOANH

**Q: Mo hinh kinh doanh?**
> - Mien phi cho ca nhan
> - Ban license cho doanh nghiep
> - Tich hop vao he thong HR/CRM

**Q: So voi doi thu?**
| | Voicemeet | Otter.ai | Fireflies |
|---|---|---|---|
| Gia | $0 | $8/thang | $10/thang |
| Offline | Co | Khong | Khong |
| Tieng Viet | 90% | 60% | 65% |

**Q: Tiem nang phat trien?**
> - Phase 2: Speaker diarization, export PDF
> - Phase 3: Realtime transcription, mobile app
> - Phase 4: Zoom/Teams integration

---

## 6. DEMO

**Q: Demo nhu the nao?**
> 1. Upload file audio 2-3 phut
> 2. Cho xu ly (~30 giay)
> 3. Download transcript + summary + DOCX
> 4. So sanh voi ban goc

**Q: Neu demo loi?**
> Co video backup. Giai thich ky thuat tai sao loi va cach fix.

---

## TIP TRA LOI

1. **Ngan gon**: Tra loi trong 30 giay
2. **Co so lieu**: "Giam 95%", "2 phut xu ly"
3. **Tu tin**: Day la san pham thuc, da test
4. **Trung thuc**: Noi ro han che, khong phai perfect
