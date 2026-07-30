# Example: Personal Brand Video Factory (Tier 2 — Multi-State Pipeline)

Ví dụ hoàn chỉnh output của Agent Kit Builder.
Domain: Tạo video ngắn từ ý tưởng (Idea → MP4 tự động).
Tier: 2 — Multi-state pipeline (6-stage production flow).

---

## Builder's Internal Analysis (không xuất cho user — chỉ minh hoạ process)

### Complexity Tier: 2 — Multi-state
- Nhiều stage: Brief → Script → Scene Plan → Voice → Compose → Render
- Context động: idea input → scene JSON → HTML/JS/CSS → MP4
- Pipeline tuần tự, mỗi stage có I/O contract riêng

### Lenses áp dụng:
- **A (Token Efficiency)**: AGENTS.md lưu hard-earned rules (CSS/GSAP) để agent không lặp lại lỗi
- **C (Reliable Performance)**: Multi-stage QA + preflight check + `qa_check()` sau render
- **E (Interoperability)**: Tích hợp Piper TTS, HyperFrames, GSAP, FFmpeg — local stack thuần

### Lenses KHÔNG áp dụng:
- **B (Adaptive)**: Input format cố định (idea text), output format cố định (MP4)
- **D (Lean Context)**: Pipeline phức tạp, cần AGENTS.md dài để guide agent
- **F (Safety)**: Chạy local, không có API key, không gọi network

### Dynamic Enhancement Discovery:
1. Outcome quan trọng nhất: **Tạo video hoàn chỉnh từ 1 câu lệnh** — local, free, không API key
2. Điểm thất bại phổ biến nhất: CSS transform bị GSAP ghi đè → layout lệch, phải re-render
3. Đòn bẩy 80/20:
   - **CSS/GSAP Positioning Rules** — nguồn gốc lỗi lớn nhất, hard rule trong AGENTS.md
   - **Scene Type System** — 5 scene type cố định (hero_title, text_card, callout, stat_card, closing) giúp agent tạo script nhanh, chuẩn

---

## OUTPUT THỰC TẾ (đây là thứ user nhận được):

---

# Personal Brand Video Factory

Idea → MP4 trong một câu lệnh. Pipeline tự động hoàn toàn, local/free, không cần API key.

## TÓM TẮT CHO NGƯỜI DÙNG

Công cụ CLI biến một ý tưởng thành video MP4 hoàn chỉnh — tự động viết script, tạo giọng đọc (Piper TTS), dựng hình ảnh động (GSAP/HyperFrames) và render ra video.
Chạy hoàn toàn local, không cần API key, không phí cloud.
Hỗ trợ 5 phong cách (playbook): clean-professional, flat-motion-graphics, minimalist-diagram, anime-ghibli, premium-minimalist.
Phát hiện tiếng Việt tự động, dùng voice model vi_VN-vais1000-medium.

---

## CẤU TRÚC KIT (output/short video builder/)

```
video/
├── video-factory.py          # CLI chính (874 lines)
├── video-factory.bat          # Windows wrapper
├── AGENTS.md                  # AI instructions — chứa rule quan trọng
├── README.md                  # Hướng dẫn người dùng
├── OpenMontage/               # Engine render
│   ├── pipeline_defs/personal-brand-video.yaml
│   └── ...
├── projects/                  # Project configs
└── renders/                   # Output MP4
```

---

## PIPELINE (6 Stage)

| Stage | Function | Input → Output |
|-------|----------|----------------|
| 1. Brief | `generate_brief()` | Idea → Brief dataclass |
| 2. Script | `generate_script()` | Brief → Script (6 scenes) |
| 3. Scene Plan | `generate_scene_plan()` | Script → Scene JSON |
| 4. Voice | `generate_voice()` | Scene text → Piper TTS WAV |
| 5. Compose | `generate_html()` | Scene + Voice → HyperFrames HTML |
| 6. Render | `render_video()` | HTML → `npx hyperframes render` → MP4 |
| QA | `qa_check()` | MP4 → ffprobe validate |

---

## SCENE TYPES (5 loại)

| Type | Visual | Công dụng |
|------|--------|-----------|
| `hero_title` | Large heading + divider | Opening hook |
| `text_card` | Heading + body text | Giải thích |
| `callout` | Badge + text on gradient bg | Key insight |
| `stat_card` | Surface card + list | Kết quả/Tính năng |
| `closing` | Accent heading + subtitle | CTA/Kết thúc |

---

## TECH STACK

| Component | Tool | Type |
|-----------|------|------|
| Voiceover | Piper TTS | Local/free |
| Visual | Clean Professional playbook | OpenMontage style |
| Animation | GSAP (via HyperFrames) | JavaScript |
| Rendering | HyperFrames | Local (HTML→MP4) |
| Composition | FFmpeg | Local |

---

## HARD-EARNED RULES (được đúc rút từ thực tế)

### CSS + GSAP Positioning (nguồn lỗi #1)
1. Không dùng `xPercent`/`yPercent` trong CSS — chỉ dùng trong GSAP `.set()`
2. Element được GSAP animate `x`/`y` thì CSS `transform` sẽ bị mất
3. Dùng wrapper pattern nếu cần vừa center vừa complex motion
4. Canvas flow lines ở portrait: `baseY = h * 0.45`

### Audio cho HyperFrames
- Dùng `src` trên `<audio>`, không dùng `<source>` children
- Cần đủ: `src`, `data-media-id`, `data-start`, `data-duration`, `preload="auto"`

### Render
- Dùng `--resolution portrait`, không dùng `--width`/`--height`
- FFmpeg phải có trên PATH
- HyperFrames lint trước, render sau — 0 errors, 0 warnings

---

## KEY DESIGN DECISIONS

1. **Single file CLI** (874 lines video-factory.py) — dễ deploy, dễ hiểu
2. **Scene type system** — 5 scene types vừa đủ, không over-engineer
3. **Playbook architecture** — style tách riêng, dễ mở rộng
4. **Local-first** — không phụ thuộc API, chạy offline hoàn toàn
5. **Vietnamese auto-detection** — dùng regex range U+00C0–U+01FF
6. **Piper temp file workaround** — Windows UTF-8 pipe bug → dùng `--input_file`

---

## LESSONS LEARNED (cho builder sau)

1. **CSS transform + GSAP = lỗi invisible** — hard rule trong AGENTS.md, không thể phụ thuộc agent tự nhớ
2. **Scene count fixed = 6** — đủ cho short video, không cần dynamic
3. **QA after EVERY render** — duration, size, scene count — phát hiện lỗi sớm
4. **Windows path hell** — hardcode FFmpeg WinGet path, auto-add to session PATH
5. **Audio format khó** — HyperFrames chỉ nhận WAV, không nhận source children

---

*Kết thúc Agent Kit Golden Example.*
