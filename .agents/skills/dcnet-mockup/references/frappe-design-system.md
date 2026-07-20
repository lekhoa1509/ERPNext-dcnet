# Frappe v16 Design System (Espresso Theme)

Extracted from actual Frappe v16 SCSS source files (`frappe/public/scss/espresso/`).
Complete token inventory for building pixel-accurate mockups.

## Colors

### Grayscale
```
--gray-50:  #f8f8f8   --gray-100: #f3f3f3   --gray-200: #ededed
--gray-300: #e2e2e2   --gray-400: #c7c7c7   --gray-500: #999999
--gray-600: #7c7c7c   --gray-700: #525252   --gray-800: #383838
--gray-900: #171717
```

### Full Color Scales (14 palettes x 9 shades)

**Blue**
```
--blue-50:  #f0f7ff   --blue-100: #d3e8fd   --blue-200: #a8d2fc
--blue-300: #72b5f9   --blue-400: #3b9cf5   --blue-500: #0289f7
--blue-600: #0074d4   --blue-700: #005aaa   --blue-800: #004880
--blue-900: #003360
```

**Green**
```
--green-50:  #edfcf0   --green-100: #cef5d5   --green-200: #9ee8b0
--green-300: #65d682   --green-400: #38c55b   --green-500: #28a745
--green-600: #1d8a38   --green-700: #17702e   --green-800: #115524
--green-900: #0b3a18
```

**Red**
```
--red-50:  #fff2f2   --red-100: #ffd7d7   --red-200: #ffb0b0
--red-300: #ff8585   --red-400: #f06060   --red-500: #e03636
--red-600: #c82424   --red-700: #a31919   --red-800: #7d1515
--red-900: #5c1010
```

**Orange**
```
--orange-50:  #fff6ed   --orange-100: #ffe4cc   --orange-200: #ffc999
--orange-300: #ffaa5e   --orange-400: #f58c2c   --orange-500: #e67512
--orange-600: #c25e0a   --orange-700: #974a0a   --orange-800: #6b3811
--orange-900: #4a2508
```

**Amber**
```
--amber-50:  #fffbeb   --amber-100: #fef3c7   --amber-200: #fde68a
--amber-300: #fcd34d   --amber-400: #fbbf24   --amber-500: #f59e0b
--amber-600: #d97706   --amber-700: #b45309   --amber-800: #92400e
--amber-900: #78350f
```

**Yellow**
```
--yellow-50:  #fffde6   --yellow-100: #fff3bf   --yellow-200: #ffe588
--yellow-300: #ffd84d   --yellow-400: #f5c518   --yellow-500: #e2a714
--yellow-600: #c08a0a   --yellow-700: #9a6e0a   --yellow-800: #733f12
--yellow-900: #5c310e
```

**Cyan**
```
--cyan-50:  #ecfeff   --cyan-100: #daf0f5   --cyan-200: #b0e0eb
--cyan-300: #80cede   --cyan-400: #4ab8cf   --cyan-500: #1a9fbc
--cyan-600: #148ba6   --cyan-700: #106f85   --cyan-800: #0c5466
--cyan-900: #073b49
```

**Teal**
```
--teal-50:  #f0fdfa   --teal-100: #ccfbf1   --teal-200: #99f6e4
--teal-300: #5eead4   --teal-400: #2dd4bf   --teal-500: #14b8a6
--teal-600: #0d9488   --teal-700: #0f766e   --teal-800: #115e59
--teal-900: #134e4a
```

**Violet**
```
--violet-50:  #f5f3ff   --violet-100: #ede9fe   --violet-200: #ddd6fe
--violet-300: #c4b5fd   --violet-400: #a78bfa   --violet-500: #8b5cf6
--violet-600: #7c3aed   --violet-700: #6d28d9   --violet-800: #5b21b6
--violet-900: #4c1d95
```

**Pink**
```
--pink-50:  #fdf2f8   --pink-100: #fce7f3   --pink-200: #fbcfe8
--pink-300: #f9a8d4   --pink-400: #f472b6   --pink-500: #ec4899
--pink-600: #db2777   --pink-700: #be185d   --pink-800: #9d174d
--pink-900: #831843
```

**Purple**
```
--purple-50:  #faf5ff   --purple-100: #ece8fc   --purple-200: #ddd2f9
--purple-300: #c6b0f5   --purple-400: #a98aef   --purple-500: #8b5cf6
--purple-600: #7c3aed   --purple-700: #6624c5   --purple-800: #521d99
--purple-900: #401863
```

**White Overlay (for layering on dark backgrounds)**
```
--white-overlay-50:  rgba(255,255,255,0.04)   --white-overlay-100: rgba(255,255,255,0.06)
--white-overlay-200: rgba(255,255,255,0.10)   --white-overlay-300: rgba(255,255,255,0.16)
--white-overlay-400: rgba(255,255,255,0.28)   --white-overlay-500: rgba(255,255,255,0.44)
--white-overlay-600: rgba(255,255,255,0.56)   --white-overlay-700: rgba(255,255,255,0.72)
--white-overlay-800: rgba(255,255,255,0.86)   --white-overlay-900: rgba(255,255,255,0.93)
```

**Black Overlay (for layering on light backgrounds)**
```
--black-overlay-50:  rgba(0,0,0,0.02)   --black-overlay-100: rgba(0,0,0,0.04)
--black-overlay-200: rgba(0,0,0,0.08)   --black-overlay-300: rgba(0,0,0,0.14)
--black-overlay-400: rgba(0,0,0,0.28)   --black-overlay-500: rgba(0,0,0,0.44)
--black-overlay-600: rgba(0,0,0,0.56)   --black-overlay-700: rgba(0,0,0,0.72)
--black-overlay-800: rgba(0,0,0,0.86)   --black-overlay-900: rgba(0,0,0,0.93)
```

### Semantic Surface Tokens
Surface tokens define backgrounds at different elevation levels.
```css
/* Gray surfaces */
--surface-gray-1: white;             /* Default page background */
--surface-gray-2: var(--gray-50);    /* Slightly elevated, code blocks */
--surface-gray-3: var(--gray-100);   /* Controls, inputs, sidebar bg */
--surface-gray-4: var(--gray-200);   /* Hover on controls */
--surface-gray-5: var(--gray-300);   /* Active/pressed controls */
--surface-gray-6: var(--gray-400);   /* Disabled strong */
--surface-gray-7: var(--gray-500);   /* Heavy muted */

/* Colored surfaces (light tint backgrounds) */
--surface-red-1:   var(--red-50);     --surface-red-2:   var(--red-100);
--surface-green-1: var(--green-50);   --surface-green-2: var(--green-100);
--surface-amber-1: var(--amber-50);   --surface-amber-2: var(--amber-100);
--surface-blue-1:  var(--blue-50);    --surface-blue-2:  var(--blue-100);
```

### Semantic Ink Tokens (Text Colors)
```css
/* Gray ink (text hierarchy) */
--ink-gray-1: var(--gray-900);    /* Headings, primary text */
--ink-gray-2: var(--gray-800);    /* Body text (--text-color) */
--ink-gray-3: var(--gray-700);    /* Muted text (--text-muted) */
--ink-gray-4: var(--gray-600);    /* Light text (--text-light) */
--ink-gray-5: var(--gray-500);    /* Placeholder, disabled text */
--ink-gray-6: var(--gray-400);    /* Very light, decorative */
--ink-gray-7: var(--gray-300);    /* Borders used as text */
--ink-gray-8: var(--gray-200);    /* Faint */
--ink-gray-9: var(--gray-100);    /* Near-invisible on white */

/* Colored ink (status text on colored backgrounds) */
--ink-red-1:   var(--red-600);   --ink-red-2:   var(--red-700);
--ink-red-3:   var(--red-800);   --ink-red-4:   var(--red-900);
--ink-green-1: var(--green-600); --ink-green-2: var(--green-700);
--ink-green-3: var(--green-800); --ink-green-4: var(--green-900);
--ink-amber-1: var(--amber-600); --ink-amber-2: var(--amber-700);
--ink-amber-3: var(--amber-800); --ink-amber-4: var(--amber-900);
--ink-blue-1:  var(--blue-600);  --ink-blue-2:  var(--blue-700);
--ink-blue-3:  var(--blue-800);  --ink-blue-4:  var(--blue-900);
```

### Semantic Outline Tokens (Borders)
```css
/* Gray outlines */
--outline-gray-1: var(--gray-100);   /* Subtle separator */
--outline-gray-2: var(--gray-200);   /* Default border (--border-color) */
--outline-gray-3: var(--gray-300);   /* Stronger border (--dark-border-color) */
--outline-gray-4: var(--gray-400);   /* Emphasis border */
--outline-gray-5: var(--gray-500);   /* Strong emphasis */

/* Colored outlines */
--outline-red:   var(--red-300);
--outline-green: var(--green-300);
--outline-amber: var(--amber-300);
--outline-blue:  var(--blue-300);
```

### Background-Text Pairs (Indicator Pills, Badges)
These are the `--bg-{color}` / `--text-on-{color}` pairs used for indicator pills and badges.
```css
/* Status badges — use these pairs together */
.green   { background: var(--green-100);  color: var(--green-800); }
.blue    { background: var(--blue-100);   color: var(--blue-700); }
.orange  { background: var(--orange-100); color: var(--orange-700); }
.red     { background: var(--red-100);    color: var(--red-700); }
.yellow  { background: var(--yellow-100); color: var(--yellow-700); }
.gray    { background: var(--gray-100);   color: var(--gray-700); }
.purple  { background: var(--purple-100); color: var(--purple-700); }
.cyan    { background: var(--cyan-50);    color: var(--cyan-700); }
.pink    { background: var(--pink-100);   color: var(--pink-700); }
.teal    { background: var(--teal-100);   color: var(--teal-700); }
.violet  { background: var(--violet-100); color: var(--violet-700); }
.amber   { background: var(--amber-100);  color: var(--amber-700); }
```

### Alert Colors
```css
/* Alert backgrounds */
--alert-bg-info:    var(--blue-50);
--alert-bg-success: var(--green-100);
--alert-bg-warning: var(--yellow-50);
--alert-bg-danger:  var(--red-50);

/* Alert text */
--alert-text-info:    var(--blue-700);
--alert-text-success: var(--green-700);
--alert-text-warning: var(--yellow-700);
--alert-text-danger:  var(--red-600);

/* Alert border (optional, Frappe uses subtle left-border) */
--alert-border-info:    var(--blue-300);
--alert-border-success: var(--green-300);
--alert-border-warning: var(--yellow-300);
--alert-border-danger:  var(--red-300);
```

### Functional Colors
```css
--text-color: var(--gray-800);        /* #383838 — body text */
--heading-color: var(--gray-900);     /* #171717 — headings */
--text-muted: var(--gray-700);        /* #525252 — secondary text */
--text-light: var(--gray-600);        /* #7c7c7c — tertiary text */
--bg-color: white;                    /* page background */
--control-bg: var(--gray-100);        /* #f3f3f3 — input backgrounds */
--border-color: var(--gray-200);      /* #ededed — default borders */
--dark-border-color: var(--gray-300); /* #e2e2e2 — emphasis borders */
--primary-color: var(--gray-900);     /* #171717 — primary buttons */
--danger: #e03636;                    /* danger red */
--disabled-text-color: var(--gray-500); /* #999999 */
--disabled-control-bg: var(--gray-50);  /* #f8f8f8 */
--divider-color: var(--gray-200);     /* #ededed — section dividers */
--card-bg: white;                     /* card background */
--modal-bg: white;                    /* modal background */
--invert-neutral: var(--gray-900);    /* inverted neutral for dark elements */
```

## Typography

```css
font-family: "InterVariable", "Inter", -apple-system, BlinkMacSystemFont,
             "Segoe UI", Roboto, sans-serif;
```

### Text Size Tokens
| Token | Size | Usage |
|-------|------|-------|
| --text-tiny | 11px | Badges, small labels |
| --text-2xs / --text-xs | 12px | Captions, footer text |
| --text-sm | 13px | Body text, table cells, controls |
| --text-base | 14px | Default body, section heads |
| --text-lg | 16px | Subheadings, widget group titles |
| --text-xl | 18px | Section titles |
| --text-2xl | 20px | Page titles, number widget values |
| --text-3xl | 24px | Large headings |

### Font Weights
| Weight | Value | CSS Class | Usage |
|--------|-------|-----------|-------|
| --weight-regular | 420 | `.font-weight-regular` | Body text, indicator pills |
| --weight-medium | 500 | `.font-weight-medium` | Buttons, badges, emphasis |
| --weight-semibold | 600 | `.font-weight-semibold` | Headings, labels, number values |
| --weight-bold | 700 | `.font-weight-bold` | Strong headings |

### Line Heights
```css
--leading-tight: 1.25;    /* headings */
--leading-normal: 1.5;    /* body text */
--leading-relaxed: 1.625; /* long text blocks */
```

## Layout

```
--navbar-height: 48px
--sidebar-width: 220px
--sidebar-collapsed-width: 50px
--page-head-height: 45px
--page-max-width: 900px
--input-height: 28px
--btn-height: 28px
--list-row-height: 30px
--page-bottom-margin: 60px
```

### Page Structure
```
+--------------------------------------------------+
| Navbar (48px, bg: white, border-bottom)           |
+----------+---------------------------------------+
| Sidebar  | Content Area                           |
| (220px)  |  Page Head (45px, sticky)              |
| gray-100 |  Page Body (max-width: 900px)         |
|          |  Page Bottom Margin (60px)             |
+----------+---------------------------------------+
```

### Sidebar Tokens
```css
--sidebar-hover-color: #f3f3f3;       /* var(--gray-100) */
--sidebar-active-color: white;         /* white bg + shadow-sm */
--sidebar-border-color: var(--gray-200);
--sidebar-item-height: 30px;
--sidebar-item-radius: 8px;
```

## Spacing

```css
--padding-xs: 5px    --margin-xs: 5px
--padding-sm: 7px    --margin-sm: 10px
--padding-md: 15px   --margin-md: 15px
--padding-lg: 20px   --margin-lg: 20px
--padding-xl: 30px   --margin-xl: 30px
--padding-2xl: 40px  --margin-2xl: 40px
```

### Spacing Scale (for gap/padding in components)
```css
--space-0: 0;
--space-1: 4px;   --space-2: 8px;   --space-3: 12px;
--space-4: 16px;  --space-5: 20px;  --space-6: 24px;
--space-7: 28px;  --space-8: 32px;
```

## Border Radius

```css
--border-radius-tiny: 4px
--border-radius-sm: 8px
--border-radius: 8px          /* default */
--border-radius-md: 10px
--border-radius-lg: 12px
--border-radius-xl: 16px
--border-radius-2xl: 20px
--border-radius-full: 999px   /* pills */
```

## Shadows

```css
--shadow-xs: rgba(0,0,0,0.05) 0px 0.5px 0px, rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.05) 0px 2px 4px;
--shadow-sm: 0px 1px 2px rgba(0,0,0,0.1);
--shadow-md: 0px 0px 1px rgba(0,0,0,0.12), 0px 0.5px 2px rgba(0,0,0,0.15), 0px 2px 3px rgba(0,0,0,0.16);
--shadow-lg: 0px 0px 1px rgba(0,0,0,0.1), 0px 2px 6px rgba(0,0,0,0.12), 0px 10px 20px rgba(0,0,0,0.16);
--shadow-xl: 0px 0px 1px rgba(0,0,0,0.1), 0px 6px 12px rgba(0,0,0,0.12), 0px 20px 36px rgba(0,0,0,0.16);
--card-shadow: var(--shadow-sm);
--btn-shadow: var(--shadow-xs);
--drop-shadow: var(--shadow-md);     /* dropdown menus */
--modal-shadow: var(--shadow-xl);    /* modals */
```

## Focus Rings

```css
--focus-default: 0px 0px 0px 2px #c9c9c9;
--focus-blue:    0px 0px 0px 2px #65b9fc;
--focus-green:   0px 0px 0px 2px #5bb98c;
--focus-yellow:  0px 0px 0px 2px #e2c97e;
--focus-red:     0px 0px 0px 2px #eb9091;
```

## Gradient Tokens

```css
--linear-black: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.6) 100%);
--linear-blue:  linear-gradient(180deg, var(--blue-400) 0%, var(--blue-600) 100%);
--angular-blue: conic-gradient(from 180deg, var(--blue-400), var(--blue-600), var(--blue-400));
```

## Transitions

```css
--transition-base: 150ms ease;
--transition-fast: 100ms ease;
--transition-normal: 200ms ease;
--transition-slow: 300ms ease;
```

## Components

### Button
```css
.btn {
  height: 28px; padding: 0.5rem 1rem;
  border: none; border-radius: 0.375rem;
  font-size: 14px; font-weight: 420;
  box-shadow: var(--shadow-xs);
  cursor: pointer;
}
.btn-primary   { background: var(--gray-900); color: white; }
.btn-primary:hover { background: var(--gray-800); }
.btn-default   { background: var(--gray-100); color: var(--gray-800); }
.btn-default:hover { background: var(--gray-200); }
.btn-danger    { background: #e03636; color: white; }
.btn-danger:hover { background: #c82424; }
.icon-btn      { width: 28px; height: 28px; padding: 0; }
.btn-ghost     { background: transparent; box-shadow: none; }
.btn-ghost:hover { background: var(--gray-100); }
```

### Button Tokens
```css
--btn-primary: var(--gray-900);
--btn-primary-hover: var(--gray-800);
--btn-default-bg: var(--gray-100);
--btn-default-hover-bg: var(--gray-200);
--btn-ghost-hover-bg: var(--gray-100);
```

### Form Control
```css
.form-control {
  height: 28px; padding: 6px 8px;
  background: var(--gray-100); border: none; border-radius: 8px;
  font-size: 13px; color: var(--gray-800);
}
.form-control:focus {
  box-shadow: 0px 0px 0px 2px #65b9fc;
  outline: none;
}
.form-control:disabled {
  background: var(--gray-50);
  color: var(--gray-500);
  cursor: not-allowed;
}
```

### Card
```css
.frappe-card {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 10px;
  padding: 7px;
}
/* NOTE: Frappe cards do NOT use hover elevation (translateY, shadow increase).
   Clickable cards only get cursor: pointer. Keep hover flat/subtle. */
```

### Number Widget (Number Card)
```css
.number-widget-box {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 10px;
  padding: 12px;
  min-height: 84px;
  cursor: pointer;
}
.number-widget-box .widget-head {
  font-size: 11px; font-weight: 500;
  text-transform: uppercase; color: var(--gray-600);
  margin-bottom: 8px;
}
.number-widget-box .number {
  font-size: 20px; font-weight: 600;
  color: var(--gray-900);
}
.number-widget-box .percentage-stat-area {
  font-size: 12px;
  margin-top: 10px;
}
.number-widget-box .percentage-stat-area .indicator-pill-round {
  height: 18px; padding: 2px 6px; border-radius: 999px;
}
.number-widget-box .stat-color.green { color: var(--green-600); }
.number-widget-box .stat-color.red { color: var(--red-600); }
```

### Indicator Pill (Badge)
```css
.indicator-pill {
  display: inline-flex; align-items: center;
  padding: 4.5px 8px;
  border-radius: 999px;
  height: 20px;
  font-size: 13px;
  font-weight: 420;
  gap: 6px;
}
.indicator-pill::before {
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}
/* Colors: use background-text pairs above */
```

### Table
```css
.data-table th {
  font-size: 12px; font-weight: 500; color: var(--gray-600);
  text-transform: uppercase; background: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
  padding: 8px;
}
.data-table td {
  padding: 10px 8px; font-size: 13px; color: var(--gray-800);
  border-bottom: 1px solid var(--gray-100);
}
```

### Sidebar
```css
.sidebar {
  width: 220px; background: var(--gray-100);
  border-right: 1px solid var(--gray-200);
}
.standard-sidebar-item {
  height: 30px; padding: 6px 12px;
  font-size: 13px; color: var(--gray-700);
  border-radius: 8px; margin: 0 4px;
  cursor: pointer;
  display: flex; align-items: center; gap: 8px;
}
.standard-sidebar-item:hover {
  background: #f3f3f3; /* var(--gray-100) slightly diff shade */
  color: var(--gray-900);
}
.standard-sidebar-item.active {
  background: white;
  box-shadow: var(--shadow-sm);
  border-radius: 8px;
  color: var(--gray-900);
  font-weight: 500;
}
/* NOTE: Frappe sidebar does NOT use border-left indicator for active state.
   Active = white background + shadow-sm + border-radius 8px */
```

### Alerts
```css
.alert-info    { background: var(--blue-50);   color: var(--blue-700); }
.alert-success { background: var(--green-100); color: var(--green-700); }
.alert-warning { background: var(--yellow-50); color: var(--yellow-700); }
.alert-danger  { background: var(--red-50);    color: var(--red-600); }
```

### Checkbox
```css
.checkbox {
  width: 14px; height: 14px;
  border: 1.5px solid var(--gray-400);
  border-radius: 4px;
  cursor: pointer;
}
.checkbox:checked {
  background: var(--gray-900);
  border-color: var(--gray-900);
}
.checkbox:focus {
  box-shadow: 0 0 0 2px var(--gray-300);
}
/* Mobile: 18px x 18px for touch targets */
```

### Switch (Toggle)
```css
.switch {
  width: 36px; height: 20px;
  border-radius: 10px;
  background: var(--gray-300);
  cursor: pointer;
}
.switch.on {
  background: var(--gray-900);
}
.switch .switch-handle {
  width: 16px; height: 16px;
  border-radius: 50%;
  background: white;
  box-shadow: var(--shadow-xs);
}
```

### Progress Bar
```css
.progress {
  height: 8px;
  background: var(--gray-200);
  border-radius: 4px;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  border-radius: 4px;
  background: var(--blue-500);
}
```

### Skeleton Loading
```css
.skeleton {
  background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 37%, var(--gray-100) 63%);
  background-size: 400% 100%;
  animation: skeleton-loading 1.4s ease infinite;
  border-radius: 8px;
}
@keyframes skeleton-loading {
  0% { background-position: 100% 50%; }
  100% { background-position: 0 50%; }
}
```

### Rating
```css
.rating {
  display: flex; gap: 2px;
}
.rating .star {
  width: 16px; height: 16px;
  color: var(--yellow-400);
}
.rating .star.empty {
  color: var(--gray-300);
}
```

### Modal
```css
.modal-backdrop {
  background: rgba(0,0,0,0.5); /* 0.5 opacity */
}
.modal-dialog {
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow-xl);
  max-width: 600px;
}
.modal-header {
  padding: var(--padding-sm) var(--padding-lg);
  border-bottom: 1px solid var(--gray-200);
  position: sticky; top: 0;
}
.modal-body {
  padding: var(--padding-lg);
}
.modal-footer {
  padding: var(--padding-sm) var(--padding-lg);
  border-top: 1px solid var(--gray-200);
  position: sticky; bottom: 0;
}
```

### Timeline
```css
.timeline-item {
  padding: 10px 0;
  border-left: 2px solid var(--gray-200);
  margin-left: 10px;
  padding-left: 20px;
  position: relative;
}
.timeline-item::before {
  content: '';
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--gray-300);
  position: absolute;
  left: -6px; top: 14px;
}
.timeline-item.highlight::before {
  background: var(--blue-500);
}
```

## Dark Theme Note

Frappe supports dark theme via `[data-theme="dark"]` selector on `<html>`.
In dark mode, all semantic tokens invert:
- Surface tokens use dark grays instead of whites
- Ink tokens lighten
- Outlines become subtle light borders
- Cards get dark backgrounds with lighter borders

For mockups, always design for **light theme** (default). Dark theme adjustments are handled by Frappe's CSS custom properties automatically.

## Z-Index Scale

```css
--z-navbar: 100;
--z-sidebar: 50;
--z-dropdown: 200;
--z-modal-backdrop: 1040;
--z-modal: 1050;
--z-toast: 1090;
--z-tooltip: 1100;
```
