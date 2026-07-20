---
name: dcnet-mockup
description: |
  Create UI mockup HTML prototypes for DCNET Flow modules.
  Output: docs/modules/{STT}-{slug}/mockup/

  Use when:
  - User asks "/dcnet-mockup {STT}" (e.g., "/dcnet-mockup 02")
  - User wants to create UI prototype for a module
  - User says "tao mockup", "tao UI", "lam giao dien mau"
  - After /dcnet-module step when UI Mockup is pending

  Triggers: "mockup", "UI prototype", "giao dien mau", "tao mockup"
---

# /dcnet-mockup — UI Mockup Builder for DCNET Flow

Create standalone HTML mockup files following Frappe v16 UI, output to module docs folder.

## Usage

```bash
/dcnet-mockup 02               # Auto-resolve: STT 02 → 02-dashboard
/dcnet-mockup 07               # Auto-resolve: STT 07 → 07-kho-hang
```

## Output

```
docs/modules/{STT}-{slug}/mockup/
├── {screen-name}.mockup.html
├── index.html                   # Landing page (if 2+ screens)
└── SUMMARY.md
```

## Process

### Step 1: Resolve Module

1. Parse argument → get STT number
2. Look up STT in source mapping at `../dcnet-module/references/source-mapping.md` → get slug, module name
3. Also accept `{STT}-{slug}` format for backward compatibility
4. Module folder path: `docs/modules/{STT}-{slug}/`
5. Read module docs: `README.md`, `analysis/gap.md`, `technical-spec/`
6. Read source spec if available (`docs/feature/`)
7. If no module docs: warn, suggest `/dcnet-module {STT}` first

### Step 2: Identify Screens

Ask user with AskUserQuestion — which screens to mock up:

- **List View** — DocType list + filters + search + status badges
- **Form View** — DocType form + tabs + fields + workflow buttons
- **Dashboard** — Number cards + charts + KPI widgets
- **Workspace** — Shortcuts + charts + report links
- **Custom Page** — Wizard, calendar, kanban, etc.

### Step 3: Build Mockups

Create `.mockup.html` per screen. Rules:

- **Standalone HTML + inline CSS** — no external dependencies, open in any browser
- **Follow Frappe v16 UI exactly** — use design tokens from [frappe-design-system.md](references/frappe-design-system.md)
- **Realistic Vietnamese sample data** — not lorem ipsum
- **Interactive where useful** — tab switching, hover states via JS
- **File naming:** `{screen-name}.mockup.html` (kebab-case)

#### Screen Templates

**List View:** Navbar (48px) + Sidebar (220px) + search bar + filter toolbar + data table + status indicator-pills + pagination

**Form View:** Navbar + form header (title + status indicator + workflow buttons) + tabs + field layout (Section Break / Column Break) + timeline section

**Dashboard:** Number Card grid (value + trend %) + Dashboard Chart areas + date filter bar + responsive grid

**Workspace:** Header with icon + shortcut cards row + Number Cards + Charts + report links list

### Step 4: Create SUMMARY.md

Document what was created, screens, design decisions.

### Step 5: Update Module README

Check UI Mockup in the module's `README.md` checklist.

## Design System

**Tokens:** [frappe-design-system.md](references/frappe-design-system.md) — colors (14 palettes x 9 shades), semantic tokens, typography, spacing, shadows, focus rings, component tokens

**Patterns:** [frappe-ui-patterns.md](references/frappe-ui-patterns.md) — page layout, navbar, sidebar, form, list view, buttons, indicator pills, modals, filter/toolbar, widgets (number/chart/shortcut/links), POS layout, stock dashboard, interactive states

Quick ref:
```
Colors:   --gray-900 #171717 (primary)  --blue-500 #0289f7  --danger #e03636
Font:     InterVariable / Inter / -apple-system, 13px body, weight 420/500/600/700
Layout:   navbar 48px, sidebar 220px (50px collapsed), input 28px, btn 28px
Radius:   8px default, 10px card, 999px pill
Shadows:  --shadow-xs (buttons), --shadow-sm (cards), --shadow-md (dropdowns)
Number:   20px size, 600 weight (NOT 28px/700), min-height 84px
Sidebar:  active = white bg + shadow-sm + 8px radius (NO border-left indicator)
Cards:    NO hover elevation (no translateY, no shadow increase) — just cursor:pointer
```

## UX Checklist

Apply these rules to ALL mockups:

- [ ] **No emojis as icons** — use inline SVG icons (Lucide or Frappe-style stroke icons, 16x16, stroke-width 2)
- [ ] **cursor: pointer** on all clickable elements (buttons, cards, links, rows)
- [ ] **:focus-visible** with `box-shadow: var(--focus-default)` ring (NOT `:focus`)
- [ ] **prefers-reduced-motion** media query — disable transitions/transforms
- [ ] **ARIA labels** on interactive elements (`aria-label`, `role`, `aria-current`)
- [ ] **`<label for="">`** on all form inputs
- [ ] **Touch targets min 28px** (Frappe standard, NOT 44px — this is desktop-first ERP)
- [ ] **No translateY/shadow elevation on card hover** — Frappe cards stay flat
- [ ] **Number widget values: 20px/600** — NOT 28px/700

> **Important:** Frappe Desk = desktop-first ERP UI, NOT generic web design.
> Follow Frappe conventions, not trendy styles. No glassmorphism, no elevation hover,
> no gradient backgrounds. Keep it flat, functional, and professional.

## Principles

- **Bam sat Frappe UI** — Dung dung CSS variables va component patterns cua Frappe v16
- **Standalone** — Mo truc tiep trong browser, khong can server
- **Realistic** — Data mau bang tieng Viet, so lieu thuc te
- **Focused** — Chi mock screens giup ra quyet dinh thiet ke, bo qua man hinh hien nhien
