---
name: "{PROJECT_NAME} Design Tokens"
version: 1.0.0
colors:
  primary: "{COLOR_PRIMARY}"
  secondary: "{COLOR_SECONDARY}"
  accent: "{COLOR_ACCENT}"
  neutral: "{COLOR_NEUTRAL}"
  surface: "{COLOR_SURFACE}"
  on_surface: "{COLOR_ON_SURFACE}"
  error: "{COLOR_ERROR}"
typography:
  fontFamilyDisplay: "{FONT_DISPLAY}"
  fontFamilyBody: "{FONT_BODY}"
  fontFamilyMono: "{FONT_MONO}"
  h1: { fontSize: "36px", fontWeight: "700", lineHeight: "1.2" }
  h2: { fontSize: "28px", fontWeight: "600", lineHeight: "1.3" }
  h3: { fontSize: "22px", fontWeight: "600", lineHeight: "1.4" }
  body: { fontSize: "16px", fontWeight: "400", lineHeight: "1.6" }
  bodySm: { fontSize: "14px", fontWeight: "400", lineHeight: "1.5" }
  caption: { fontSize: "12px", fontWeight: "500", lineHeight: "1.4" }
rounded:
  sm: "4px"
  md: "8px"
  lg: "16px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
components:
  buttonPrimary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "10px 20px"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: "24px"
    border: "1px solid rgba(255, 255, 255, 0.1)"
---

# {PROJECT_NAME} — Design Specification

> **Single Source of Truth (SSOT)** for project visual design, tokens, and UX rationale.  
> **Hard Gate:** Mọi trang, component và mã CSS/Tailwind phải đối chiếu và tuân thủ 100% token ở YAML frontmatter trên.

---

## 1. Overview & Brand Personality
- **Emotional Tone**: {BRAND_TONE_DESCRIPTION} (e.g. Sleek, Modern, High-trust, Minimalist).
- **Target Audience**: {TARGET_AUDIENCE}.
- **Style Archetype**: {STYLE_ARCHETYPE} (e.g. Glassmorphism Dark, Clean SaaS, Neo-brutalism).

---

## 2. Color Palette & Accessibility
- **Primary ({COLOR_PRIMARY})**: Dùng cho CTA chính và điểm nhấn thương hiệu.
- **Secondary ({COLOR_SECONDARY})**: Dùng cho các thành phần bổ trợ.
- **Surface ({COLOR_SURFACE})**: Nền card, container.
- **WCAG AA Compliance**: Đảm bảo tỷ lệ tương phản văn bản $\ge 4.5:1$ đối với văn bản thông thường và $\ge 3:1$ đối với UI components.

---

## 3. Typography Hierarchy
- **Display Font**: `{FONT_DISPLAY}` (Google Fonts) — Dành cho Headline H1/H2.
- **Body Font**: `{FONT_BODY}` (Google Fonts) — Dành cho nội dung văn bản, tính dễ đọc cao.
- **Monospace Font**: `{FONT_MONO}` — Dành cho code snippet, số liệu kỹ thuật.

---

## 4. Spacing & Spatial Layout
- **Spatial Unit**: Bội số 4px / 8px.
- **Touch Targets**: Kích thước tương tác tối thiểu $\ge 44 \times 44\text{px}$.
- **Responsive Breakpoints**: 375px (Mobile), 768px (Tablet), 1024px (Laptop), 1440px (Desktop).

---

## 5. Do's and Don'ts (Anti-Cliche Hard Gates)
- ✅ **Do**: Sử dụng SVG icons (Heroicons/Lucide); chuyển động mượt mà (150–300ms transition).
- ❌ **Don't**: Tuyệt đối KHÔNG dùng emoji làm icon; KHÔNG lạm dụng gradient tím AI mặc định (Purple Ban).
- ❌ **Don't**: Không dùng mã màu hex tùy tiện ngoài danh mục tokens ở YAML header.
