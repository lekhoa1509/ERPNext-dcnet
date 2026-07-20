# DCNET Permission Manager — UI Redesign Spec

**Date:** 2026-06-09
**Status:** Approved
**Scope:** UI/CSS/HTML only — không thay đổi Python backend, API, DocType

---

## 1. Tổng quan

Thiết kế lại giao diện trang `dcnet_permission_manager` từ CSS/JS hiện tại (809 dòng CSS, 852 dòng JS) sang bộ design system **Clean Card + Teal Brand** — gọn gàng, chuyên nghiệp hơn, nhất quán với brand màu teal hiện có.

**File cần sửa:**
- `dcnet-permission/dcnet_permission/public/css/dcnet_permission_manager.css` — viết lại toàn bộ
- `dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js` — chỉ sửa class names / DOM structure để match CSS mới

**Không thay đổi:**
- `api.py`, `permission_manager.py`, `hooks.py`
- Tất cả DocType JSON
- Logic JS (frappe.call, xử lý data, dialog logic)

---

## 2. Design System

### 2.1 Color Palette

| Token | Hex | Dùng cho |
|-------|-----|---------|
| `--primary` | `#0f766e` | Buttons chính, active state, badge số |
| `--primary-hover` | `#0d6a63` | Button hover |
| `--primary-light` | `#f0fdfa` | Active background, stat icon bg |
| `--primary-mid` | `#14b8a6` | Accent text, border active |
| `--primary-subtle` | `#ccfbf1` | Role tag teal, row highlight |
| `--text-primary` | `#0f172a` | Tiêu đề, tên user |
| `--text-secondary` | `#334155` | Nội dung thường |
| `--text-muted` | `#94a3b8` | Label phụ, placeholder |
| `--border` | `#e2e8f0` | Border card, table |
| `--border-light` | `#f1f5f9` | Divider, row separator |
| `--surface` | `#f8fafc` | Background header, sidebar item hover |
| `--bg` | `#f0f4f8` | Page background |

### 2.2 Typography

- Font: `-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif`
- Page title: `15px / 700`
- Section label: `10px / 700 / uppercase / letter-spacing 0.08em`
- Table header: `10px / 700 / uppercase / letter-spacing 0.06em`
- Body text: `13px / 400`
- Small/meta: `11px / 400`
- Badge/tag: `10px / 600`

### 2.3 Spacing & Radius

- Border radius card: `10px`
- Border radius button: `7px`
- Border radius badge/pill: `20px` (pill) hoặc `5px` (tag)
- Border radius avatar: `50%`
- Page padding: `16–24px`
- Row padding: `11px 16px`

### 2.4 Shadow

- Card nhẹ: `0 1px 4px rgba(0,0,0,0.06)`
- Scope item active: `0 1px 4px rgba(15,118,110,0.12)`

---

## 3. Layout

### 3.1 Cấu trúc tổng thể

```
┌─────────────────────────────────────────────────┐
│  PAGE HEADER  (52px, white, shadow-sm)           │
│  [🛡 icon] Quản lý phân quyền   [Làm mới][+ Tạo]│
├─────────────────────────────────────────────────┤
│  STATS ROW  (4 cards, padding 16px 20px)         │
│  [🏠 5 Phòng ban][👥 24 Tổng][✓ 22 Active][🔒 8]│
├────────────┬────────────────────────────────────┤
│  SIDEBAR   │  MAIN PANEL                        │
│  200px     │  flex-1                            │
│            │  [toolbar: dept label + search + filter]
│  PHÒNG BAN │  ─────────────────────────────────│
│  [search]  │  TABLE                             │
│            │  User | Status | Roles | Actions   │
│  • Kinh... │  ─ row ─ row ─ row ─              │
│  • Kế toán │                                    │
│  ─────     │  ─────────────────────────────────│
│  • Kho     │  FOOTER: count + scope note        │
│  • HR      │                                    │
│  • IT      │                                    │
└────────────┴────────────────────────────────────┘
```

**Chiều cao:** Header (52) + Stats (84) + Body (fill remaining, min 400px)

### 3.2 Page Header

- Background: `white`
- Border-bottom: `1px solid var(--border)`
- Box-shadow: `0 1px 3px rgba(0,0,0,0.06)`
- Height: `52px`
- Left: Icon shield gradient (`#0f766e → #14b8a6`) + Title + Subtitle
- Right: `[Làm mới]` (outline) + `[+ Tạo user mới]` (primary teal)

### 3.3 Stats Row

- 4 cards dạng `display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px`
- Mỗi card: background `#f8fafc`, border `1px solid var(--border)`, radius `10px`, padding `12px 14px`
- Icon 36x36px với background màu pastel theo thứ tự: teal / blue / green / orange
- Value: `20px / 800`, Label: `11px / 500 / muted`

### 3.4 Sidebar

- Width: `200px`, background `white`, border-right `1px solid var(--border)`
- Header: label "PHÒNG BAN" + count badge
- Search input 28px radius 7px
- Scope item (`.scope-item`):
  - Padding: `8px 10px`, radius `8px`
  - Hover: background `#f8fafc`
  - Active: background `#f0fdfa`
  - Top row: tên scope (bold teal khi active) + badge (teal filled khi active, gray khi không)
  - Meta row: "X roles • ..." font 10px muted (teal khi active)
- Divider `1px / #f1f5f9` giữa các nhóm

### 3.5 Main Panel — Toolbar

- Background: `white`, border-bottom `1px solid #f1f5f9`
- Padding: `12px 16px`
- Left: dept name (13px bold) + count pill
- Right: search input (220px min) + filter dropdown

### 3.6 Main Panel — Table

| Cột | Width | Nội dung |
|-----|-------|---------|
| User | 260px | Avatar 32px tròn (chữ tắt màu pastel) + Tên + Email |
| Trạng thái | 110px | Pill: Active (green) / Disabled (gray) |
| Roles | flex | Tags: primary tag teal cho role chính, gray cho phụ, `+N` nếu nhiều |
| Thao tác | 150px right | `[🔒 Phân quyền]` (teal outline) + `[✏️]` + `[⋯]` |

- Table header: `10px uppercase / #f8fafc background / border-bottom`
- Rows: `border-bottom: 1px solid #f1f5f9`, hover `#f8fafc`
- Avatar: `32px`, `border-radius: 50%`, màu background pastel theo hash tên

### 3.7 Table Footer

- `10px 16px padding`, `border-top 1px solid #f1f5f9`
- Left: "Hiển thị X / Y users..."
- Right: note "Chỉ hiển thị user trong scope [Dept]"

---

## 4. Components

### 4.1 Button styles

| Variant | Style |
|---------|-------|
| Primary | `bg #0f766e, color white, hover #0d6a63` |
| Outline | `bg white, border var(--border), color #64748b` |
| Teal outline | `bg #f0fdfa, border #99f6e4, color #0f766e` |
| Icon button | `28x28px, radius 6px, border var(--border), hover bg #f0fdfa` |

### 4.2 Status Pill

```
Active:   bg #f0fdf4, color #15803d, dot #22c55e
Disabled: bg #f9fafb, color #94a3b8, dot #cbd5e1
```

### 4.3 Role Tags

```
Primary (first role): bg #ccfbf1, color #0f766e
Secondary:            bg #f1f5f9, color #475569
Overflow (+N):        transparent, color #94a3b8
```

### 4.4 Avatar

- Size: `32px` (table), `24px` (sidebar nếu dùng)
- Border-radius: `50%`
- Chữ tắt: 2 ký tự đầu họ tên, `font-size 11px / 800`
- Màu background: chọn theo index `charCode(initial[0]) % 5` → map sang 5 màu pastel:
  - 0: teal `#f0fdfa / #0f766e`
  - 1: blue `#eff6ff / #2563eb`
  - 2: purple `#fdf4ff / #9333ea`
  - 3: orange `#fff7ed / #ea580c`
  - 4: rose `#fff1f2 / #e11d48`

---

## 5. Dialogs (giữ nguyên logic, chỉ restyle)

### 5.1 Dialog Tạo/Sửa User

- Max-width: `480px`
- Header: icon + title + close button
- Fields: Full Name, Email, Password, Department (readonly), Roles (checkbox list từ scope)
- Footer: `[Hủy]` + `[Lưu]`

### 5.2 Dialog Phân quyền (Permission Matrix)

- Max-width: `700px`
- Header: user info + mode toggle (Roles / Custom)
- Permission grid: grouped by category, columns: Module | Read | Create | Write | Delete | Submit | Cancel | Report | Export | Print
- Logic giữ nguyên: uncheck Read → clear all; check non-Read → auto check Read

---

## 6. Điều không thay đổi

- Tất cả `frappe.call()` và API endpoints
- Event listeners và business logic trong JS
- Tên class CSS nào đang được JS dùng để query DOM sẽ được giữ hoặc refactor cùng lúc
- Python backend hoàn toàn không đổi

---

## 7. Mockup reference

File mockup đã approve: `.superpowers/brainstorm/43625-1780977630/content/full-mockup.html`
