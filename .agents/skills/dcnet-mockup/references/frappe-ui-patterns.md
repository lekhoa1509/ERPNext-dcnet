# Frappe Desk + ERPNext UI Patterns

Component patterns with HTML structure and CSS for building pixel-accurate mockups.
Use together with [frappe-design-system.md](frappe-design-system.md) for tokens.

> **Key Principle:** Frappe Desk is a **desktop-first ERP UI**. It is NOT generic web design.
> Follow Frappe's flat, functional aesthetic — no trendy gradients, no elevation on hover,
> no glassmorphism. Cards are flat with 1px borders. Hover is subtle (bg change only).

---

## A. Frappe Desk Core Patterns

### A1. Page Layout

The fundamental page structure for all Frappe screens.

```html
<div class="page-container">
  <div class="page-head" style="height: 45px; position: sticky; top: 48px; z-index: 2;">
    <!-- Title + primary actions -->
    <div class="page-head-content">
      <div class="title-area">
        <h3 class="title-text">Page Title</h3>
      </div>
      <div class="page-actions">
        <button class="btn btn-default btn-sm">Secondary</button>
        <button class="btn btn-primary btn-sm">Primary Action</button>
      </div>
    </div>
  </div>
  <div class="page-body">
    <div class="layout-main">
      <div class="layout-main-section">
        <!-- Main content here -->
      </div>
      <div class="layout-side-section" style="width: 240px;">
        <!-- Optional sidebar (form view) -->
      </div>
    </div>
  </div>
</div>
```

```css
.page-container { background: white; }
.page-head {
  height: 45px;
  display: flex; align-items: center;
  padding: 0 15px;
  border-bottom: 1px solid var(--gray-200);
  background: white;
  position: sticky; top: 48px; /* below navbar */
  z-index: 2;
}
.page-head-content {
  display: flex; align-items: center;
  justify-content: space-between;
  width: 100%;
}
.title-text {
  font-size: 14px; font-weight: 600;
  color: var(--gray-900);
}
.page-body { padding: 15px; }
.layout-main {
  display: flex; flex-direction: row;
  gap: 15px;
}
.layout-main-section { flex: 1; min-width: 0; }
.layout-side-section { width: 240px; flex-shrink: 0; }
```

### A2. Navbar

```html
<header class="navbar" style="height: 48px;">
  <div class="navbar-home">
    <img src="logo.png" width="32" height="32" alt="Logo">
  </div>
  <div class="search-bar">
    <input type="text" placeholder="Search or type a command (Ctrl + /)"
           style="max-width: 300px; height: 28px;">
  </div>
  <nav class="navbar-nav">
    <button class="navbar-icon" aria-label="Notifications">
      <!-- bell icon -->
    </button>
    <div class="avatar-frame" style="width: 28px; height: 28px;">
      <!-- user avatar -->
    </div>
  </nav>
</header>
```

```css
.navbar {
  height: 48px;
  background: white;
  border-bottom: 1px solid var(--gray-200);
  display: flex; align-items: center;
  padding: 0 16px;
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 100;
}
.navbar-home { margin-right: 16px; }
.navbar-home img { width: 32px; height: 32px; }
.search-bar input {
  max-width: 300px; height: 28px;
  background: var(--gray-100); border: none; border-radius: 8px;
  padding: 0 12px; font-size: 13px; color: var(--gray-600);
}
.navbar-nav {
  margin-left: auto;
  display: flex; align-items: center; gap: 8px;
}
.navbar-icon {
  width: 28px; height: 28px;
  border: none; background: none;
  border-radius: 6px;
  color: var(--gray-600); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.navbar-icon:hover {
  background: var(--gray-100);
  color: var(--gray-900);
}
```

### A3. Sidebar

Frappe sidebar has two states: collapsed (50px, icons only) and expanded (220px).

```html
<aside class="sidebar" style="width: 220px;">
  <div class="sidebar-menu">
    <div class="sidebar-section">
      <div class="sidebar-label">MODULE</div>
      <a class="standard-sidebar-item active" href="#">
        <span class="sidebar-icon"><!-- icon --></span>
        <span class="sidebar-text">Dashboard</span>
      </a>
      <a class="standard-sidebar-item" href="#">
        <span class="sidebar-icon"><!-- icon --></span>
        <span class="sidebar-text">Sales Order</span>
      </a>
    </div>
  </div>
</aside>
```

```css
.sidebar {
  width: 220px; /* or 50px collapsed */
  background: var(--gray-100);
  border-right: 1px solid var(--gray-200);
  position: fixed; top: 48px; bottom: 0;
  overflow-y: auto;
  padding: 8px 0;
}
.sidebar-label {
  padding: 8px 16px 4px;
  font-size: 11px; font-weight: 600;
  text-transform: uppercase;
  color: var(--gray-500);
  letter-spacing: 0.5px;
}
.standard-sidebar-item {
  height: 30px;
  padding: 0 12px;
  margin: 0 4px;
  border-radius: 8px;
  font-size: 13px;
  color: var(--gray-700);
  cursor: pointer;
  display: flex; align-items: center; gap: 8px;
  text-decoration: none;
}
.standard-sidebar-item:hover {
  background: #f3f3f3;
  color: var(--gray-900);
}
.standard-sidebar-item.active {
  background: white;
  box-shadow: 0px 1px 2px rgba(0,0,0,0.1); /* --shadow-sm */
  color: var(--gray-900);
  font-weight: 500;
}
/* IMPORTANT: NO border-left indicator. Active = white bg + shadow-sm */
.sidebar-icon {
  width: 16px; height: 16px;
  flex-shrink: 0;
  color: var(--gray-600);
}
.standard-sidebar-item.active .sidebar-icon,
.standard-sidebar-item:hover .sidebar-icon {
  color: var(--gray-900);
}
```

### A4. Form View

```html
<div class="form-page">
  <!-- Form Header -->
  <div class="form-header">
    <div class="title-area">
      <span class="indicator-pill green">Submitted</span>
      <h2 class="form-title">SO-2026-00042</h2>
    </div>
    <div class="form-actions">
      <button class="btn btn-default">Amend</button>
      <button class="btn btn-primary">Submit</button>
    </div>
  </div>

  <!-- Form Tabs -->
  <div class="form-tabs-list" style="position: sticky; top: 93px;">
    <ul class="nav">
      <li><a class="nav-link active" href="#">Details</a></li>
      <li><a class="nav-link" href="#">Accounting</a></li>
      <li><a class="nav-link" href="#">Connections</a></li>
    </ul>
  </div>

  <!-- Form Section -->
  <div class="form-section">
    <div class="section-head">Customer Details</div>
    <div class="section-body">
      <div class="form-column" style="flex: 1;">
        <div class="frappe-control">
          <label class="control-label">Customer</label>
          <div class="control-input">
            <input type="text" class="form-control" value="Thang Long TM">
          </div>
        </div>
      </div>
      <div class="form-column" style="flex: 1;">
        <div class="frappe-control">
          <label class="control-label">Order Date</label>
          <div class="control-input">
            <input type="date" class="form-control" value="2026-02-15">
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

```css
.form-header {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  border-bottom: 1px solid var(--gray-200);
}
.form-title {
  font-size: 16px; font-weight: 600;
  color: var(--gray-900);
  margin-left: 8px;
}
.form-tabs-list {
  border-bottom: 1px solid var(--gray-200);
  padding: 0 15px;
  background: white;
  position: sticky; top: 93px; /* navbar 48 + page-head 45 */
  z-index: 1;
}
.form-tabs-list .nav {
  display: flex; gap: 0; list-style: none;
  margin: 0; padding: 0;
}
.nav-link {
  padding: 8px 12px;
  font-size: 13px; font-weight: 500;
  color: var(--gray-600);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  cursor: pointer;
}
.nav-link:hover { color: var(--gray-900); }
.nav-link.active {
  color: var(--gray-900);
  border-bottom-color: var(--gray-900);
}
.form-section { padding: 15px; }
.section-head {
  font-size: 14px; font-weight: 500;
  color: var(--gray-900);
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--gray-200);
}
.section-body {
  display: flex; flex-wrap: wrap;
  gap: 15px;
}
.frappe-control { margin-bottom: 10px; }
.control-label {
  font-size: 11px; font-weight: 500;
  color: var(--gray-600);
  text-transform: uppercase;
  margin-bottom: 4px;
  display: block;
}
.control-input .form-control {
  width: 100%; height: 28px;
  padding: 6px 8px;
  background: var(--gray-100); border: none; border-radius: 8px;
  font-size: 13px; color: var(--gray-800);
}
.control-input .form-control:focus {
  box-shadow: 0px 0px 0px 2px #65b9fc;
  outline: none;
}
```

### A5. List View

```html
<div class="frappe-list">
  <!-- List Header -->
  <div class="list-row list-row-head" style="height: 30px; background: var(--gray-50);">
    <div class="list-row-col ellipsis" style="flex: 0 0 30px;">
      <input type="checkbox" class="list-check-all">
    </div>
    <div class="list-row-col ellipsis" style="flex: 2;">Name</div>
    <div class="list-row-col ellipsis" style="flex: 1;">Status</div>
    <div class="list-row-col ellipsis" style="flex: 1;">Customer</div>
    <div class="list-row-col ellipsis" style="flex: 1; text-align: right;">Amount</div>
  </div>

  <!-- List Rows -->
  <div class="list-row-container">
    <div class="list-row" style="cursor: pointer;">
      <div class="list-row-col" style="flex: 0 0 30px;">
        <input type="checkbox">
      </div>
      <div class="list-row-col" style="flex: 2;">
        <a class="ellipsis" href="#">SO-2026-00042</a>
      </div>
      <div class="list-row-col" style="flex: 1;">
        <span class="indicator-pill green">Submitted</span>
      </div>
      <div class="list-row-col" style="flex: 1;">Thang Long TM</div>
      <div class="list-row-col" style="flex: 1; text-align: right; font-weight: 500;">
        45.500.000
      </div>
    </div>
  </div>
</div>
```

```css
.frappe-list { background: white; }
.list-row {
  display: flex; align-items: center;
  padding: 8px 15px;
  border-bottom: 1px solid var(--gray-100);
  font-size: 13px; /* --text-sm */
  color: var(--gray-800);
  cursor: pointer;
}
.list-row:hover {
  background: var(--gray-50);
}
.list-row-head {
  height: 30px;
  background: var(--gray-50);
  font-size: 12px; font-weight: 500;
  color: var(--gray-600);
  text-transform: uppercase;
  cursor: default;
}
.list-row-head:hover { background: var(--gray-50); /* no change */ }
.list-row-col {
  padding: 0 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.list-row-col a {
  color: var(--gray-900);
  font-weight: 500;
  text-decoration: none;
}
.list-row-col a:hover { text-decoration: underline; }
```

### A6. Buttons

Full button reference with all variants.

```css
/* Base button */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  height: 28px;
  padding: 0 10px;
  border: none; border-radius: 6px;
  font-size: 14px; font-weight: 420;
  cursor: pointer;
  box-shadow: var(--shadow-xs);
  gap: 6px; /* for icon + text */
}
.btn-sm { height: 24px; font-size: 12px; padding: 0 8px; }

/* Primary — dark (Frappe uses gray-900, NOT blue) */
.btn-primary {
  background: var(--gray-900); color: white;
}
.btn-primary:hover { background: var(--gray-800); }

/* Default — light gray */
.btn-default {
  background: var(--gray-100); color: var(--gray-800);
}
.btn-default:hover { background: var(--gray-200); }

/* Danger */
.btn-danger {
  background: #e03636; color: white;
}
.btn-danger:hover { background: #c82424; }

/* Icon button (square) */
.icon-btn {
  width: 28px; height: 28px;
  padding: 0; border: none;
  background: none; border-radius: 6px;
  color: var(--gray-600); cursor: pointer;
}
.icon-btn:hover {
  background: var(--gray-100);
  color: var(--gray-900);
}

/* Ghost button (no shadow, transparent) */
.btn-ghost {
  background: transparent;
  box-shadow: none;
  color: var(--gray-700);
}
.btn-ghost:hover { background: var(--gray-100); }
```

### A7. Indicator Pills (Status Badges)

```html
<!-- With dot indicator -->
<span class="indicator-pill green">Submitted</span>
<span class="indicator-pill blue">Draft</span>
<span class="indicator-pill red">Cancelled</span>
<span class="indicator-pill orange">Pending</span>
<span class="indicator-pill yellow">On Hold</span>
<span class="indicator-pill gray">Not Started</span>

<!-- Without dot (plain badge) -->
<span class="badge-pill green">Active</span>
```

```css
.indicator-pill {
  display: inline-flex; align-items: center;
  padding: 2px 8px 2px 6px;
  border-radius: 999px;
  height: 20px;
  font-size: 12px; font-weight: 420;
  gap: 6px;
  white-space: nowrap;
}
.indicator-pill::before {
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

/* Color pairs */
.indicator-pill.green  { background: var(--green-100);  color: var(--green-800); }
.indicator-pill.blue   { background: var(--blue-100);   color: var(--blue-700); }
.indicator-pill.red    { background: var(--red-100);    color: var(--red-700); }
.indicator-pill.orange { background: var(--orange-100); color: var(--orange-700); }
.indicator-pill.yellow { background: var(--yellow-100); color: var(--yellow-700); }
.indicator-pill.gray   { background: var(--gray-200);   color: var(--gray-700); }
.indicator-pill.purple { background: var(--purple-100); color: var(--purple-700); }
.indicator-pill.cyan   { background: var(--cyan-100);   color: var(--cyan-700); }
.indicator-pill.pink   { background: var(--pink-100);   color: var(--pink-700); }

/* Common ERPNext status mappings */
/* Draft = blue, Submitted = green/blue, Cancelled = red,
   Pending = orange, On Hold = yellow, Completed = green,
   Overdue = red, Not Started = gray, Partially = orange */
```

### A8. Modals / Dialogs

```html
<div class="modal-backdrop" style="opacity: 0.5;"></div>
<div class="modal-dialog">
  <div class="modal-header">
    <h4 class="modal-title">Confirm Action</h4>
    <button class="btn-close icon-btn">&times;</button>
  </div>
  <div class="modal-body">
    <p>Are you sure you want to submit this document?</p>
  </div>
  <div class="modal-footer">
    <button class="btn btn-default">Cancel</button>
    <button class="btn btn-primary">Yes, Submit</button>
  </div>
</div>
```

```css
.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1040;
}
.modal-dialog {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow-xl);
  max-width: 600px; width: 90%;
  z-index: 1050;
  max-height: 80vh;
  display: flex; flex-direction: column;
}
.modal-header {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 7px 20px; /* --padding-sm --padding-lg */
  border-bottom: 1px solid var(--gray-200);
  position: sticky; top: 0;
  background: white;
  border-radius: 12px 12px 0 0;
}
.modal-title {
  font-size: 14px; font-weight: 600;
  color: var(--gray-900);
}
.modal-body {
  padding: 20px;
  overflow-y: auto; flex: 1;
}
.modal-footer {
  display: flex; justify-content: flex-end;
  gap: 8px;
  padding: 7px 20px;
  border-top: 1px solid var(--gray-200);
  position: sticky; bottom: 0;
  background: white;
  border-radius: 0 0 12px 12px;
}
```

### A9. Filter / Toolbar

```html
<div class="page-form">
  <div class="filter-area">
    <button class="filter-button btn btn-default">
      <span class="filter-icon"><!-- filter icon --></span>
      Filter
    </button>
    <div class="active-filters">
      <span class="filter-tag">
        Status = Submitted
        <button class="remove-filter">&times;</button>
      </span>
    </div>
  </div>
  <div class="sort-area">
    <button class="btn btn-ghost btn-sm">Sort</button>
  </div>
</div>
```

```css
.page-form {
  display: flex; align-items: center;
  flex-wrap: wrap; gap: 8px;
  padding: 8px 15px;
  background: white; /* or var(--card-bg) */
  border-bottom: 1px solid var(--gray-200);
}
.filter-button {
  font-weight: 600; /* semibold */
}
.filter-area {
  display: flex; align-items: center; gap: 8px;
  flex: 1;
}
.filter-tag {
  display: inline-flex; align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: var(--gray-100);
  border-radius: 6px;
  font-size: 12px;
  color: var(--gray-700);
}
.filter-tag .remove-filter {
  border: none; background: none;
  color: var(--gray-500);
  cursor: pointer; font-size: 14px;
  padding: 0 2px;
}
/* Filter popover: min-width 500px, shadow-md */
.filter-popover {
  min-width: 500px;
  background: white;
  border-radius: 10px;
  box-shadow: var(--shadow-md);
  padding: 12px;
}
```

### A10. Dropdown Menu

```html
<div class="dropdown-menu" style="display: block;">
  <a class="dropdown-item" href="#">Edit</a>
  <a class="dropdown-item" href="#">Duplicate</a>
  <div class="dropdown-divider"></div>
  <a class="dropdown-item text-danger" href="#">Delete</a>
</div>
```

```css
.dropdown-menu {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  box-shadow: var(--shadow-md);
  padding: 4px;
  min-width: 180px;
  z-index: 200;
}
.dropdown-item {
  display: block;
  padding: 6px 12px;
  font-size: 13px;
  color: var(--gray-800);
  text-decoration: none;
  border-radius: 6px;
  cursor: pointer;
}
.dropdown-item:hover {
  background: var(--gray-100);
  color: var(--gray-900);
}
.dropdown-item.text-danger { color: var(--red-500); }
.dropdown-item.text-danger:hover { background: var(--red-50); }
.dropdown-divider {
  height: 1px;
  background: var(--gray-200);
  margin: 4px 0;
}
```

---

## B. ERPNext Dashboard / Workspace Patterns

### B1. Widget Group

Container for dashboard widgets. Uses auto-fill grid with 300px minimum.

```html
<div class="widget-group">
  <div class="widget-group-head">
    <span class="widget-group-title">Key Metrics</span>
  </div>
  <div class="widget-group-body grid-col-3">
    <!-- Number widgets go here -->
  </div>
</div>
```

```css
.widget-group {
  margin-bottom: 20px;
}
.widget-group-title {
  font-size: 16px; font-weight: 600;
  color: var(--gray-900);
  margin-bottom: 12px;
  display: block;
}
.widget-group-body.grid-col-3 {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}
```

### B2. Number Widget

The standard number card used in dashboards and workspaces.

```html
<div class="number-widget-box" onclick="..." style="cursor: pointer;">
  <div class="widget-head">
    <span class="widget-label">Total Revenue</span>
  </div>
  <div class="widget-body">
    <div class="number">2.847.500.000</div>
    <div class="percentage-stat-area">
      <span class="indicator-pill-round green">
        <svg width="10" height="10"><!-- arrow up --></svg>
        12.5%
      </span>
      <span class="stat-period">vs last month</span>
    </div>
  </div>
</div>
```

```css
.number-widget-box {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 10px;
  padding: 12px;
  min-height: 84px;
  cursor: pointer;
}
/* NO hover elevation. No translateY. No shadow increase on hover.
   Just cursor: pointer. This is Frappe's actual behavior. */
.number-widget-box .widget-head {
  margin-bottom: 8px;
}
.number-widget-box .widget-label {
  font-size: 11px; font-weight: 500;
  text-transform: uppercase;
  color: var(--gray-600);
}
.number-widget-box .number {
  font-size: 20px;  /* NOT 28px */
  font-weight: 600; /* NOT 700 */
  color: var(--gray-900);
}
.percentage-stat-area {
  display: flex; align-items: center; gap: 6px;
  margin-top: 10px;
  font-size: 12px;
}
.indicator-pill-round {
  display: inline-flex; align-items: center; gap: 3px;
  padding: 2px 6px;
  border-radius: 999px;
  height: 18px;
  font-size: 11px; font-weight: 500;
}
.indicator-pill-round.green {
  background: var(--green-100);
  color: var(--green-700);
}
.indicator-pill-round.red {
  background: var(--red-100);
  color: var(--red-700);
}
.stat-period {
  font-size: 11px;
  color: var(--gray-500);
}
```

### B3. Chart Widget

```html
<div class="dashboard-widget-box" style="min-height: 240px;">
  <div class="chart-widget-head">
    <span class="chart-widget-title">Revenue Trend</span>
    <div class="chart-widget-actions">
      <button class="icon-btn" aria-label="Refresh"><!-- refresh --></button>
      <button class="icon-btn" aria-label="Expand"><!-- expand --></button>
    </div>
  </div>
  <div class="chart-container">
    <!-- Frappe Charts or CSS chart here -->
  </div>
</div>
```

```css
.dashboard-widget-box {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 10px;
  padding: 12px;
  min-height: 240px;
}
.chart-widget-head {
  display: flex; align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.chart-widget-title {
  font-size: 13px; font-weight: 600;
  color: var(--gray-900);
}
.chart-widget-actions {
  display: flex; gap: 4px;
}
.chart-container {
  height: calc(100% - 40px);
}
```

### B4. Shortcut Widget

```html
<div class="shortcut-widget-box" onclick="..." style="cursor: pointer;">
  <div class="shortcut-content">
    <span class="shortcut-icon"><!-- icon --></span>
    <span class="shortcut-label">New Sales Order</span>
  </div>
  <span class="shortcut-count">142</span>
</div>
```

```css
.shortcut-widget-box {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 10px 12px;
  cursor: pointer;
  display: flex; align-items: center;
  justify-content: space-between;
}
.shortcut-widget-box:hover {
  border-color: var(--gray-900); /* --invert-neutral */
}
.shortcut-content {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; color: var(--gray-800);
}
.shortcut-count {
  font-size: 12px; font-weight: 500;
  color: var(--gray-600);
  background: var(--gray-100);
  padding: 2px 8px; border-radius: 999px;
}
```

### B5. Links Widget

```html
<div class="links-widget-box">
  <div class="widget-head">
    <span class="widget-label">Reports</span>
  </div>
  <div class="links-list">
    <a class="link-item" href="#">
      <span class="link-icon"><!-- icon --></span>
      Sales Register
    </a>
    <a class="link-item" href="#">
      <span class="link-icon"><!-- icon --></span>
      Gross Profit
    </a>
  </div>
</div>
```

```css
.links-widget-box {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 10px;
  padding: 12px;
}
.links-list {
  display: flex; flex-direction: column;
}
.link-item {
  display: flex; align-items: center; gap: 8px;
  padding: 4px 8px;
  font-size: 13px;
  color: var(--gray-700);
  text-decoration: none;
  border-radius: 6px;
}
.link-item:hover {
  background: var(--gray-50);
  color: var(--gray-900);
}
```

### B6. Report Summary

Summary bar shown at top of reports with key aggregates.

```html
<div class="report-summary">
  <div class="summary-item">
    <span class="summary-label">Total Sales</span>
    <span class="summary-value">2.847.500.000</span>
  </div>
  <div class="summary-item">
    <span class="summary-label">Total Orders</span>
    <span class="summary-value">342</span>
  </div>
  <div class="summary-item">
    <span class="summary-label">Average Order</span>
    <span class="summary-value">8.325.000</span>
  </div>
</div>
```

```css
.report-summary {
  display: flex; flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  margin-bottom: 16px;
}
.summary-item {
  min-width: 160px;
}
.summary-label {
  display: block;
  font-size: 11px; font-weight: 500;
  text-transform: uppercase;
  color: var(--gray-600);
  margin-bottom: 4px;
}
.summary-value {
  font-size: 20px; font-weight: 600;
  color: var(--gray-900);
}
```

---

## C. ERPNext Custom Page Patterns

### C1. POS Layout

Point of Sale uses a 10-column grid.

```html
<div class="pos-container">
  <div class="items-selector" style="grid-column: span 6;">
    <div class="search-bar">
      <input type="text" placeholder="Search items...">
    </div>
    <div class="items-grid">
      <div class="item-card">
        <div class="item-image"><!-- image --></div>
        <div class="item-name">Gay Driver TM Qi35</div>
        <div class="item-price">5.000.000</div>
      </div>
      <!-- more items -->
    </div>
  </div>
  <div class="customer-cart" style="grid-column: span 4;">
    <div class="cart-header">
      <input type="text" placeholder="Search customer...">
    </div>
    <div class="cart-items">
      <!-- cart item rows -->
    </div>
    <div class="cart-totals">
      <div class="total-row">
        <span>Total</span>
        <span class="total-amount">15.500.000</span>
      </div>
    </div>
    <div class="numpad-container">
      <!-- 3x4 numpad grid -->
    </div>
    <button class="btn btn-primary btn-lg" style="width: 100%;">
      Complete Order
    </button>
  </div>
</div>
```

```css
.pos-container {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 16px;
  height: calc(100vh - 48px);
  padding: 16px;
  background: var(--gray-50);
}
.items-selector {
  grid-column: span 6;
  background: white;
  border-radius: 10px;
  border: 1px solid var(--gray-200);
  overflow: hidden;
}
.customer-cart {
  grid-column: span 4;
  background: white;
  border-radius: 10px;
  border: 1px solid var(--gray-200);
  display: flex; flex-direction: column;
}
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
  padding: 12px;
  overflow-y: auto;
}
.item-card {
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  text-align: center;
}
.item-card:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-sm);
}
.item-name {
  font-size: 12px; font-weight: 500;
  color: var(--gray-800);
  margin-top: 6px;
}
.item-price {
  font-size: 13px; font-weight: 600;
  color: var(--gray-900);
  margin-top: 2px;
}
.numpad-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding: 12px;
}
/* NOTE: POS item cards ARE an exception — they do use scale(1.02) on hover.
   This is unique to POS; other Frappe cards do NOT hover-scale. */
```

### C2. Stock Dashboard

```html
<div class="stock-dashboard">
  <div class="dashboard-list-item">
    <div class="item-info">
      <span class="item-name">Gay Driver TM Qi35</span>
      <span class="warehouse-tag">Kho HN - Cau Giay</span>
    </div>
    <div class="stock-indicator">
      <div class="progress" style="width: 200px;">
        <div class="progress-bar" style="width: 72%; background: var(--green-500);"></div>
      </div>
      <span class="stock-qty">72 / 100</span>
    </div>
  </div>
</div>
```

```css
.stock-dashboard {
  background: white;
}
.dashboard-list-item {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  border-bottom: 1px solid var(--gray-100);
  font-size: 13px;
}
.dashboard-list-item:hover {
  background: var(--gray-50);
}
.item-info {
  display: flex; align-items: center; gap: 12px;
}
.warehouse-tag {
  font-size: 11px;
  color: var(--gray-500);
  background: var(--gray-100);
  padding: 2px 6px; border-radius: 4px;
}
.stock-indicator {
  display: flex; align-items: center; gap: 8px;
}
.stock-qty {
  font-size: 12px; font-weight: 500;
  color: var(--gray-700);
  min-width: 80px; text-align: right;
}
/* Progress bar colors based on stock level:
   > 60% = green-500, 30-60% = orange-500, < 30% = red-500 */
```

### C3. Item Grid Template

Used in Stock Balance and warehouse views.

```html
<div class="item-grid">
  <div class="item-grid-card">
    <div class="item-grid-image">
      <!-- product image -->
    </div>
    <div class="item-grid-info">
      <span class="item-grid-name">Gay Driver TM Qi35</span>
      <span class="item-grid-stock green">In Stock: 72</span>
    </div>
    <div class="item-grid-meta">
      <span class="warehouse-color" style="background: var(--blue-500);"></span>
      <span>Kho HN</span>
    </div>
  </div>
</div>
```

```css
.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}
.item-grid-card {
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}
.item-grid-card:hover {
  border-color: var(--gray-300);
}
.item-grid-image {
  height: 140px;
  background: var(--gray-50);
  display: flex; align-items: center; justify-content: center;
}
.item-grid-info {
  padding: 8px 10px;
}
.item-grid-name {
  font-size: 13px; font-weight: 500;
  color: var(--gray-800);
  display: block;
}
.item-grid-stock {
  font-size: 11px; font-weight: 500;
  margin-top: 2px; display: block;
}
.item-grid-stock.green { color: var(--green-600); }
.item-grid-stock.orange { color: var(--orange-600); }
.item-grid-stock.red { color: var(--red-600); }
.item-grid-meta {
  padding: 6px 10px;
  border-top: 1px solid var(--gray-100);
  display: flex; align-items: center; gap: 6px;
  font-size: 11px; color: var(--gray-500);
}
.warehouse-color {
  width: 8px; height: 8px;
  border-radius: 50%;
}
/* Discount label overlay */
.discount-label {
  position: absolute; top: 8px; right: 8px;
  background: var(--red-500); color: white;
  padding: 2px 6px; border-radius: 4px;
  font-size: 10px; font-weight: 600;
}
```

### C4. Sales Funnel / Chart Pattern

```html
<div class="sales-funnel">
  <div class="funnel-stage">
    <div class="funnel-bar" style="width: 100%; background: var(--blue-500);">
      <span class="funnel-label">Leads</span>
      <span class="funnel-count">450</span>
    </div>
  </div>
  <div class="funnel-stage">
    <div class="funnel-bar" style="width: 65%; background: var(--blue-400);">
      <span class="funnel-label">Opportunities</span>
      <span class="funnel-count">292</span>
    </div>
  </div>
  <div class="funnel-stage">
    <div class="funnel-bar" style="width: 35%; background: var(--blue-300);">
      <span class="funnel-label">Quotations</span>
      <span class="funnel-count">158</span>
    </div>
  </div>
  <div class="funnel-stage">
    <div class="funnel-bar" style="width: 20%; background: var(--green-500);">
      <span class="funnel-label">Sales Orders</span>
      <span class="funnel-count">90</span>
    </div>
  </div>
</div>
```

```css
.sales-funnel {
  display: flex; flex-direction: column;
  gap: 8px;
  padding: 12px;
}
.funnel-stage {
  display: flex;
}
.funnel-bar {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 6px;
  color: white;
  min-height: 36px;
}
.funnel-label {
  font-size: 13px; font-weight: 500;
}
.funnel-count {
  font-size: 14px; font-weight: 600;
}
```

---

## D. Interactive States Reference

### D1. Hover States

| Element | Hover Behavior | CSS |
|---------|---------------|-----|
| List rows | Light gray background | `background: var(--gray-50)` |
| Sidebar items | Slightly darker gray | `background: #f3f3f3` |
| Buttons (default) | Darker gray | `background: var(--gray-200)` |
| Cards | **NO hover elevation** | `cursor: pointer` only |
| Icon buttons | Gray background | `background: var(--gray-100)` |
| Shortcut widget | Border darkens | `border-color: var(--gray-900)` |
| Links | Text underline | `text-decoration: underline` |
| POS item cards | **EXCEPTION**: slight scale | `transform: scale(1.02)` |
| Dropdown items | Gray background | `background: var(--gray-100)` |

**Key insight:** Frappe does NOT use `translateY` hover on cards, does NOT use shadow
elevation on hover. Keep everything flat and subtle. The only exception is POS item cards.

### D2. Active States

| Element | Active Behavior | CSS |
|---------|----------------|-----|
| Sidebar items | White bg + subtle shadow | `background: white; box-shadow: var(--shadow-sm)` |
| Tab links | Bottom border | `border-bottom: 1px solid var(--gray-900)` |
| Filter buttons | Primary color | `background: var(--gray-900); color: white` |
| Buttons | Focus shadow | `box-shadow: var(--focus-default)` |
| Checkbox | Dark fill | `background: var(--gray-900)` |

### D3. Focus States

| Element | Focus Behavior | CSS |
|---------|---------------|-----|
| Inputs | Blue ring | `box-shadow: 0 0 0 2px #65b9fc` |
| Buttons | Gray ring | `box-shadow: var(--focus-default)` |
| Checkbox | Gray ring | `box-shadow: 0 0 0 2px var(--gray-300)` |
| Links | Blue outline | `outline: 2px solid var(--blue-500)` |

Use `:focus-visible` (not `:focus`) to show rings only for keyboard navigation.

### D4. Disabled States

```css
.disabled, [disabled], :disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}
/* Or more specifically: */
.form-control:disabled {
  background: var(--gray-50);
  color: var(--gray-500);
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### D5. Loading States

```css
/* Skeleton loading for number widgets */
.number-widget-box.loading .number {
  width: 120px; height: 24px;
  background: var(--gray-200);
  border-radius: 6px;
  animation: skeleton-loading 1.4s ease infinite;
}

/* Button loading spinner */
.btn.loading {
  color: transparent;
  position: relative;
}
.btn.loading::after {
  content: '';
  width: 14px; height: 14px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  position: absolute;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## E. Common Layout Combinations

### E1. Dashboard Page

```
Navbar (48px)
+-- Sidebar (220px) --+-- Main Content -------------------+
|                      |  Page Head (45px): "Dashboard"    |
|  Dashboard           |  Filter Bar: Day/Month/Year       |
|  * active            |                                    |
|  Sales Order         |  Widget Group: "Key Metrics"       |
|  Purchase Order      |  [Number] [Number] [Number]        |
|  ...                 |                                    |
|                      |  Widget Group: "Charts"            |
|                      |  [Chart Card] [Chart Card]         |
|                      |                                    |
+----------------------+------------------------------------+
```

### E2. List Page

```
Navbar (48px)
+-- Sidebar (220px) --+-- Main Content -------------------+
|                      |  Page Head: "Sales Order" [+Add]  |
|                      |  Filter Toolbar                    |
|                      |  [Checkbox] Name | Status | Amount |
|                      |  --------------------------------- |
|                      |  [ ] SO-001 | Submitted | 45.5M   |
|                      |  [ ] SO-002 | Draft     | 12.3M   |
|                      |  ...                               |
|                      |  Page Footer: Showing 1-20 of 342 |
+----------------------+------------------------------------+
```

### E3. Form Page

```
Navbar (48px)
+-- Sidebar (220px) --+-- Main Content ---+-- Side Section --+
|                      |  Form Header:      |  Activity       |
|                      |  [Status] SO-001   |  Timeline       |
|                      |  [Amend] [Submit]  |  Comments       |
|                      |  [Details|Acct|...]|                  |
|                      |  ---Section Head---|                  |
|                      |  Customer | Date   |  Connections    |
|                      |  ---Items Table----|  - Delivery Note |
|                      |  Item | Qty | Rate |  - Sales Invoice |
+----------------------+-------------------+------------------+
```

---

## F. Responsive Breakpoints

Frappe is desktop-first. Mobile adaptations are minimal:

```css
/* Frappe breakpoints (approximate) */
@media (max-width: 1200px) {
  /* Sidebar collapses to 50px icon-only */
}
@media (max-width: 768px) {
  /* Sidebar hidden (hamburger menu) */
  /* Layout stacks vertically */
  /* Form columns become full-width */
}
```

For mockups, always design for **desktop (1280px+)** first.
Mobile is secondary for ERP applications.
