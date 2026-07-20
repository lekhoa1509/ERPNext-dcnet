# DCNET Theme — Nation-Inspired ERPNext Desk Theming

> A gift to the DCNET team from Larry & Claude. Built in one session, reviewed 4 times, shipped with love.

Transform ERPNext's default Desk UI into something memorable. Pick a nation-inspired preset, upload your client's logo, and the entire ERP feels like a different product — in under 30 seconds.

## Quick Start

```bash
# After pulling this branch, just migrate:
bench --site {site} migrate

# That's it. 7 presets are auto-seeded. Default theme activates automatically.
```

Then visit:

- **Theme Gallery** → `/app/theme-gallery` — browse and activate presets
- **Theme Settings** → `/app/super-theme-settings` — branding, dark mode, custom CSS

## 7 Presets

| Preset      | Primary         | Accent           | Personality               |
| ----------- | --------------- | ---------------- | ------------------------- |
| Vietnam     | `#da251d` red   | `#ffcd00` gold   | Bold, energetic, warm     |
| Italy       | `#009246` green | `#ce2b37` red    | Elegant Mediterranean     |
| Germany     | `#1a1a1a` black | `#dd0000` red    | Engineering-precise       |
| France      | `#002395` blue  | `#ed2939` red    | Royal, authoritative      |
| Brazil      | `#009c3b` green | `#ffdf00` yellow | Vibrant, tropical         |
| South Korea | `#003478` blue  | `#cd2e3a` red    | Modern, tech-forward      |
| Default     | `#374151` gray  | `#3b82f6` blue   | Polished neutral baseline |

Each preset styles ~80 CSS properties: sidebar, navbar, buttons, cards, inputs, lists, modals, page head — not just colors but border-radius, shadows, spacing, fonts, and hover states.

## Features

- **Gallery Page** — visual card grid with flag gradient stripes and color swatches
- **Dark Mode** — each preset includes a dark variant, toggle in Settings
- **Google Fonts** — each preset loads its own font family
- **Custom CSS** — escape hatch for per-preset and per-site overrides
- **Export/Import** — share themes as JSON files between sites
- **Branding** — logo, favicon, login logo, app title — all from Settings
- **CSS Transitions** — smooth 0.3s scoped transitions on theme switch

## How It Works

```
Admin picks preset in Settings or Gallery
    ↓
dcnet_theme_settings.py → on_save()
    ↓
theme_utils.py generates CSS string from:
  1. Quick-edit fields → :root { --st-* } variables
  2. Component JSON → CSS selectors (data-driven mapping)
  3. Frappe variable bridge → --primary, --sidebar-active-color, etc.
  4. Dark mode variant (if enabled)
  5. Google Font @import
  6. Scoped transitions
  7. Custom CSS layers
    ↓
CSS cached in Redis → injected via boot_session → <style> tag in <head>
    ↓
Browser renders themed Desk on every page load (always fresh, never stale)
```

## Architecture

```
dcnet_theme/
├── __init__.py
├── hooks.py                # Module metadata
├── boot.py                 # boot_session hook — injects CSS via bootinfo
├── install.py              # Seed presets on install/migrate
├── presets.py              # 7 preset definitions as Python dicts
├── theme_utils.py          # CSS generation engine (the brain)
├── doctype/
│   ├── dcnet_theme_preset/ # Each preset = 1 document (hybrid storage)
│   └── dcnet_theme_settings/ # Single DocType — active preset + branding
├── page/
│   └── theme_gallery/      # Gallery page with responsive card grid
└── public/
    └── js/
        └── theme_applicator.js  # Client-side: bootinfo CSS → <style> tag
```

### Key Design Decisions

1. **Boot injection, not static CSS file** — `/files/` URLs have no cache-busting in Frappe. We inject CSS via `bootinfo` (fresh on every page load) instead of `app_include_css`.

2. **Hybrid DocType storage** — 18 quick-edit fields (colors, fonts, border-radius) for fast editing + JSON `component_styles` field for full 80-property control. Best of both worlds.

3. **Data-driven selector mapping** — `COMPONENT_SELECTORS` dict in `theme_utils.py` maps component properties to CSS selectors. Adding a new component = adding a dict entry, not writing CSS.

4. **Frappe variable bridge** — Our CSS overrides Frappe's built-in CSS variables (`--primary`, `--sidebar-active-color`, etc.) so existing `dcnet_theme.css` and Frappe's own styles pick up our colors.

5. **Module isolation** — Zero imports from `dcnet_apps.*` or `erpnext.*`. Only `frappe.*`. Ready to extract as a standalone Frappe app whenever we want.

## Adding a New Preset

1. Add a dict to `presets.py` following the existing pattern
2. Run `bench migrate` — the preset appears in Gallery automatically
3. That's it

## Client Branding Workflow

For a new client deployment:

1. Open `/app/theme-gallery` → pick a preset that matches their brand colors
2. Open `/app/super-theme-settings` → upload their logo, favicon, set app title
3. Optionally tweak colors in the Preset DocType form
4. Optionally add custom CSS for fine-tuning
5. Done — under 5 minutes

## For Future Decoupling

To extract as a standalone Frappe app:

```bash
# 1. Move to its own repo
# 2. Add pyproject.toml + modules.txt
# 3. Remove one-line imports from dcnet_apps root hooks/install/boot
# 4. Install separately:
bench get-app dcnet_theme
bench --site {site} install-app dcnet_theme
```

Zero code changes needed inside the module.

## How This Was Built

This module was designed and built in a single session using Claude Code with gstack skills:

1. **Brainstorming** (`superpowers:brainstorming`) — explored the idea, picked approach, designed presets
2. **CEO Review** (`/plan-ceo-review` x2) — scope expansion: added gallery, preview, export/import, dark mode, Google Fonts, transitions
3. **Design Review** (`/plan-design-review`) — UX specs: interaction states, responsive behavior, accessibility, anti-AI-slop card design
4. **Eng Review** (`/plan-eng-review`) — architecture validation, test plan, error handling, performance
5. **Spec Review** (adversarial subagent x2) — 14 issues found and fixed in the design doc
6. **Implementation** (`superpowers:executing-plans`) — 9 tasks, subagent for preset data, all built in parallel
7. **QA** (`/qa`) — browser testing with gstack browse, found and fixed CSS specificity + cache-busting issues

Total review score: CEO CLEAR, Design 8/10, Eng CLEAR. Zero critical gaps.

---

_Built with care by Larry & Claude — March 2026_
