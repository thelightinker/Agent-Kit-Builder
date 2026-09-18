---
name: ui-ux-pro-max
description: "UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including pages, components, design systems, accessibility, interaction, responsive layout, typography, color, charts, and stack-specific UI implementation. Searchable local data: 79 searchable styles (50 active), 192 product palettes and reasoning profiles, 74 font pairings, 119 UX guidelines, 105 icons, 17 GSAP presets, 25 chart types, and 22 stacks."
when_to_use: "Khi thiết kế, xây dựng, review hoặc nâng cấp giao diện người dùng (UI/UX), tạo design system, sinh DESIGN.md tokens, chọn style/palette/typography, xây dựng visual kits, dashboard, landing page, slides, hoặc audit anti-patterns."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
version: 1.1.0
---

# UI/UX Pro Max - Design Intelligence

Searchable local UI/UX guidance: 79 searchable styles (50 active), 192 product palettes and exact reasoning profiles, 74 font pairings, 119 UX guidelines, 105 curated icons, 17 GSAP presets, 25 chart types, and 22 technology stacks.

## 🛑 MANDATORY GATE: DESIGN.md TOKENS BEFORE ANY UI CODE

Trước khi sinh hoặc sửa bất kỳ mã giao diện nào (HTML, JSX, Vue, Svelte, Tailwind):
1. **Kiểm tra file `DESIGN.md`** tại thư mục gốc của dự án.
2. **Nếu chưa có**: Dùng `ui-ux-pro-max` để tìm palette, typography, style phù hợp và **sinh file `DESIGN.md` chứa YAML Design Tokens** (colors, typography, rounded, spacing, components) theo mẫu `templates/design-spec-template.md`.
3. **Nếu đã có**: Đọc và bám sát 100% các giá trị token đã định nghĩa.
4. **Anti-Cliche Hard Gate**:
   - ❌ **Purple Ban**: Cấm dùng gradient tím AI mặc định trừ khi brand yêu cầu.
   - ❌ **Emoji as Icon Ban**: Tuyệt đối dùng SVG icons (Heroicons/Lucide), không dùng emoji.
   - ❌ **Raw Hex Ban**: Cấm dùng mã màu hex tùy tiện rải rác ngoài token.

---

## When to Apply

Use this Skill when the task involves **UI structure, visual design decisions, interaction patterns, or user experience quality control**: designing new pages, creating/refactoring UI components, choosing color/typography/spacing/layout systems, reviewing UI for UX/accessibility/consistency, implementing navigation/animation/responsive behavior, or improving perceived quality and usability.

Skip it for pure backend logic, API/database design, non-visual performance work, infrastructure/DevOps, or non-visual scripts — unless the task changes how something **looks, feels, moves, or is interacted with**.

## Rule Categories by Priority

*Follow priority 1→10 to decide which category to focus on first; use `--domain <Domain>` to query full details. The full rule text for every category lives in `references/quick-reference.md` — read it on demand rather than loading it every time.*

| Priority | Category | Impact | Domain | Key Checks (Must Have) | Anti-Patterns (Avoid) |
|----------|----------|--------|--------|------------------------|------------------------|
| 1 | Accessibility | CRITICAL | `ux` | Contrast 4.5:1, Alt text, Keyboard nav, Aria-labels | Removing focus rings, Icon-only buttons without labels |
| 2 | Touch & Interaction | CRITICAL | `ux` | Min size 44×44px, 8px+ spacing, Loading feedback | Reliance on hover only, Instant state changes (0ms) |
| 3 | Performance | HIGH | `ux` | WebP/AVIF, Lazy loading, Reserve space (CLS &lt; 0.1) | Layout thrashing, Cumulative Layout Shift |
| 4 | Style Selection | HIGH | `style`, `product` | Match product type, Consistency, SVG icons (no emoji) | Mixing flat & skeuomorphic randomly, Emoji as icons |
| 5 | Layout & Responsive | HIGH | `ux` | Mobile-first breakpoints, Viewport meta, No horizontal scroll | Horizontal scroll, Fixed px container widths, Disable zoom |
| 6 | Typography & Color | MEDIUM | `typography`, `color` | Base 16px, Line-height 1.5, Semantic color tokens | Text &lt; 12px body, Gray-on-gray, Raw hex in components |
| 7 | Animation | MEDIUM | `ux`, `gsap` | Context-aware timing, Motion conveys meaning, Spatial continuity | One duration for every transition, Animating width/height, No reduced-motion |
| 8 | Forms & Feedback | MEDIUM | `ux` | Visible labels, Error near field, Helper text, Progressive disclosure | Placeholder-only label, Errors only at top, Overwhelm upfront |
| 9 | Navigation Patterns | HIGH | `ux` | Predictable back, Bottom nav ≤5, Deep linking | Overloaded nav, Broken back behavior, No deep links |
| 10 | Charts & Data | LOW | `chart` | Legends, Tooltips, Accessible colors | Relying on color alone to convey meaning |

For the full rule list per category (all 119 UX guidelines with rationale), read `references/quick-reference.md`. For app-specific polish rules (icons, touch feedback, dark mode contrast, safe areas) and the canonical pre-delivery checklist, read `references/pro-rules.md`.

---

## Running the search tool

The search script lives inside this skill's `scripts/` directory. Always invoke it via Python:

```bash
python .agents/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain>
```

If `python` is not found, try `python3`, then `py -3`. Requires Python 3.x, no external dependencies.

## Workflow

### Step 1: Analyze User Requirements
Extract product type, target audience, style keywords, and tech stack.

### Step 2: Generate Design System & DESIGN.md
```bash
python .agents/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```
Trích xuất tokens và lưu vào `DESIGN.md` tại thư mục gốc dự án.

### Step 3: Supplement with Detailed Searches
```bash
python .agents/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

### Step 4: Visual Output Delivery
Tạo HTML Visual Kit / UI Component bám sát 100% token từ `DESIGN.md`. Chạy Pre-Delivery Checklist trong `references/pro-rules.md`.
