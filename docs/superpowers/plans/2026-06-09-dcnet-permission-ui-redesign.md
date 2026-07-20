# DCNET Permission Manager — UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite CSS and update JS HTML structure for dcnet-permission-manager to the Clean Card + Teal Brand design system.

**Architecture:** CSS full-rewrite (keeping all class names referenced in JS); JS updated in `renderShell`, `renderStats`, `renderScopes`, `renderUsers`, `renderUserRows`, `renderUserRoleChips` and new helper `avatarColorIndex`. No Python/API/DocType changes.

**Tech Stack:** Vanilla JS (IIFE), CSS3, Frappe page/dialog APIs.

---

## Files

| Action | File |
|--------|------|
| **Rewrite** | `dcnet-permission/dcnet_permission/public/css/dcnet_permission_manager.css` |
| **Modify** | `dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js` |

---

## Task 1: Rewrite CSS

**Files:**
- Rewrite: `dcnet-permission/dcnet_permission/public/css/dcnet_permission_manager.css`

- [ ] **Step 1: Replace the entire CSS file**

```css
/* ── Reset / Page ───────────────────────────────────────── */
.dcnet-permission-page {
	background: #f0f4f8;
	min-height: calc(100vh - 120px);
	padding: 16px;
}

.dpm-root {
	color: #0f172a;
	font-size: 13px;
}

/* ── Stats Row ──────────────────────────────────────────── */
.dpm-stats {
	display: grid;
	gap: 12px;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	margin-bottom: 14px;
}

.dpm-stat-card {
	align-items: center;
	background: #ffffff;
	border: 1px solid #e2e8f0;
	border-radius: 10px;
	display: flex;
	gap: 12px;
	padding: 12px 14px;
}

.dpm-stat-icon {
	align-items: center;
	border-radius: 9px;
	display: flex;
	flex-shrink: 0;
	height: 36px;
	justify-content: center;
	width: 36px;
}

.dpm-stat-icon svg {
	height: 18px;
	width: 18px;
}

.dpm-stat-body {
	display: flex;
	flex-direction: column;
	gap: 2px;
}

.dpm-stat-value {
	color: #0f172a;
	font-size: 20px;
	font-weight: 800;
	line-height: 1;
}

.dpm-stat-label {
	color: #94a3b8;
	font-size: 11px;
	font-weight: 500;
}

/* loading shimmer */
.dpm-root.dpm-loading .dpm-stats,
.dpm-root.dpm-loading .dpm-layout {
	opacity: 0.5;
	pointer-events: none;
}

.dpm-root.dpm-loading .dpm-stat-value {
	animation: dpm-shimmer 1.2s ease infinite;
	background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
	background-size: 200% 100%;
	border-radius: 4px;
	color: transparent;
}

@keyframes dpm-shimmer {
	0% { background-position: 200% 0; }
	100% { background-position: -200% 0; }
}

/* ── Layout ─────────────────────────────────────────────── */
.dpm-layout {
	display: flex;
	min-height: 480px;
	border: 1px solid #e2e8f0;
	border-radius: 10px;
	overflow: hidden;
	background: #ffffff;
}

/* ── Sidebar ────────────────────────────────────────────── */
.dpm-sidebar {
	background: #ffffff;
	border-right: 1px solid #e2e8f0;
	display: flex;
	flex-direction: column;
	flex-shrink: 0;
	min-width: 0;
	width: 200px;
}

.dpm-sidebar-head {
	align-items: center;
	display: flex;
	justify-content: space-between;
	padding: 12px 16px 6px;
}

.dpm-sidebar-title {
	color: #94a3b8;
	font-size: 10px;
	font-weight: 700;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.dpm-sidebar-count {
	background: #f1f5f9;
	border-radius: 10px;
	color: #64748b;
	font-size: 10px;
	font-weight: 600;
	padding: 2px 7px;
}

.dpm-sidebar-search {
	margin: 0 10px 6px;
}

.dpm-sidebar-search-input {
	background: #f8fafc;
	border: 1px solid #e2e8f0;
	border-radius: 7px;
	color: #334155;
	font-size: 12px;
	height: 28px;
	padding: 0 10px;
	width: 100%;
}

.dpm-sidebar-search-input:focus {
	border-color: #14b8a6;
	box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.1);
	outline: none;
}

.dpm-sidebar-search-input::placeholder {
	color: #cbd5e1;
}

.dpm-scopes {
	display: flex;
	flex: 1;
	flex-direction: column;
	gap: 2px;
	overflow-y: auto;
	padding: 2px 8px 8px;
}

.dpm-scope {
	background: transparent;
	border: none;
	border-radius: 8px;
	color: inherit;
	cursor: pointer;
	display: flex;
	flex-direction: column;
	gap: 3px;
	padding: 8px 10px;
	text-align: left;
	transition: background 150ms ease;
	width: 100%;
}

.dpm-scope:hover {
	background: #f8fafc;
}

.dpm-scope.is-active {
	background: #f0fdfa;
}

.dpm-scope-header {
	align-items: center;
	display: flex;
	justify-content: space-between;
}

.dpm-scope-name {
	color: #334155;
	font-size: 12px;
	font-weight: 600;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.dpm-scope.is-active .dpm-scope-name {
	color: #0f766e;
}

.dpm-scope-badge {
	background: #e2e8f0;
	border-radius: 10px;
	color: #64748b;
	flex-shrink: 0;
	font-size: 10px;
	font-weight: 700;
	padding: 1px 6px;
}

.dpm-scope.is-active .dpm-scope-badge {
	background: #0f766e;
	color: #ffffff;
}

.dpm-scope-meta {
	color: #94a3b8;
	font-size: 10px;
}

.dpm-scope.is-active .dpm-scope-meta {
	color: #14b8a6;
}

.dpm-sidebar-divider {
	background: #f1f5f9;
	height: 1px;
	margin: 4px 10px;
}

/* ── Main Panel ──────────────────────────────────────────── */
.dpm-main {
	display: flex;
	flex: 1;
	flex-direction: column;
	min-width: 0;
	overflow: hidden;
}

.dpm-main-body {
	display: flex;
	flex: 1;
	flex-direction: column;
	min-width: 0;
	overflow: hidden;
}

/* ── Toolbar ─────────────────────────────────────────────── */
.dpm-toolbar {
	align-items: center;
	background: #ffffff;
	border-bottom: 1px solid #f1f5f9;
	display: flex;
	gap: 8px;
	padding: 10px 16px;
}

.dpm-dept-label {
	color: #0f172a;
	font-size: 13px;
	font-weight: 700;
	flex-shrink: 0;
}

.dpm-dept-count {
	background: #f1f5f9;
	border-radius: 10px;
	color: #94a3b8;
	font-size: 11px;
	font-weight: 600;
	padding: 2px 8px;
}

.dpm-toolbar-gap {
	flex: 1;
}

.dpm-search-wrap {
	min-width: 200px;
}

.dpm-search {
	border: 1px solid #e2e8f0 !important;
	border-radius: 7px !important;
	font-size: 12px !important;
	height: 32px !important;
	padding: 0 12px !important;
}

.dpm-search:focus {
	border-color: #14b8a6 !important;
	box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.1) !important;
}

.dpm-status {
	border: 1px solid #e2e8f0 !important;
	border-radius: 7px !important;
	color: #334155 !important;
	font-size: 12px !important;
	height: 32px !important;
	padding: 0 10px !important;
	width: auto !important;
}

/* ── Table ───────────────────────────────────────────────── */
.dpm-table-wrap {
	flex: 1;
	overflow-x: auto;
	overflow-y: auto;
}

.dpm-table {
	margin-bottom: 0;
	min-width: 560px;
}

.dpm-table thead th {
	background: #f8fafc;
	border-bottom: 1px solid #e2e8f0;
	border-top: none;
	color: #94a3b8;
	font-size: 10px;
	font-weight: 700;
	letter-spacing: 0.06em;
	padding: 10px 16px;
	text-transform: uppercase;
	white-space: nowrap;
}

.dpm-table thead th:last-child {
	text-align: right;
}

.dpm-table tbody td {
	border-bottom: 1px solid #f1f5f9;
	padding: 11px 16px;
	vertical-align: middle;
}

.dpm-table tbody tr:last-child td {
	border-bottom: none;
}

.dpm-table tbody tr:hover td {
	background: #f8fafc;
}

/* ── User Cell ───────────────────────────────────────────── */
.dpm-user {
	align-items: center;
	display: flex;
	gap: 10px;
	min-width: 200px;
}

/* Avatar: base style */
.dpm-avatar {
	align-items: center;
	border-radius: 50%;
	display: inline-flex;
	flex: 0 0 32px;
	font-size: 11px;
	font-weight: 800;
	height: 32px;
	justify-content: center;
	width: 32px;
}

/* Avatar color variants (charCode % 5) */
.dpm-avatar--0 { background: #f0fdfa; color: #0f766e; }
.dpm-avatar--1 { background: #eff6ff; color: #2563eb; }
.dpm-avatar--2 { background: #fdf4ff; color: #9333ea; }
.dpm-avatar--3 { background: #fff7ed; color: #ea580c; }
.dpm-avatar--4 { background: #fff1f2; color: #e11d48; }

.dpm-user-name {
	color: #0f172a;
	font-size: 13px;
	font-weight: 600;
	line-height: 1.3;
}

.dpm-user-email,
.dpm-muted {
	color: #94a3b8;
	font-size: 11px;
}

/* ── Status Pill ─────────────────────────────────────────── */
.dpm-status-dot {
	border-radius: 50%;
	display: inline-block;
	flex-shrink: 0;
	height: 6px;
	margin-right: 5px;
	width: 6px;
}

.dpm-status-pill {
	align-items: center;
	border-radius: 20px;
	display: inline-flex;
	font-size: 11px;
	font-weight: 600;
	padding: 3px 9px;
	white-space: nowrap;
}

.dpm-status-pill.is-enabled {
	background: #f0fdf4;
	color: #15803d;
}

.dpm-status-pill.is-enabled .dpm-status-dot {
	background: #22c55e;
}

.dpm-status-pill.is-disabled {
	background: #f9fafb;
	color: #94a3b8;
}

.dpm-status-pill.is-disabled .dpm-status-dot {
	background: #cbd5e1;
}

.dpm-status-pill.is-warning {
	background: #fef3c7;
	color: #92400e;
}

.dpm-status-pill.is-neutral {
	background: #e5e7eb;
	color: #374151;
}

/* ── Role Tags ───────────────────────────────────────────── */
.dpm-role-list {
	align-items: center;
	display: flex;
	flex-wrap: wrap;
	gap: 4px;
}

.dpm-role-tag {
	background: #f1f5f9;
	border-radius: 5px;
	color: #475569;
	font-size: 10px;
	font-weight: 600;
	padding: 3px 8px;
	white-space: nowrap;
}

.dpm-role-tag--primary {
	background: #ccfbf1;
	color: #0f766e;
}

.dpm-role-tag--more {
	background: transparent;
	color: #94a3b8;
}

/* Legacy chip (used in dialogs) */
.dpm-role-chip {
	background: #edf2ff;
	border: 1px solid #c7d2fe;
	border-radius: 999px;
	color: #263b78;
	display: inline-flex;
	font-size: 12px;
	font-weight: 600;
	padding: 4px 8px;
}

.dpm-role-chip.is-personal {
	background: #ecfdf5;
	border-color: #86efac;
	color: #166534;
}

/* ── Action Buttons ──────────────────────────────────────── */
.dpm-actions {
	text-align: right;
	white-space: nowrap;
}

.dpm-action-primary-btn {
	align-items: center;
	background: #f0fdfa;
	border: 1px solid #99f6e4;
	border-radius: 6px;
	color: #0f766e;
	cursor: pointer;
	display: inline-flex;
	font-size: 11px;
	font-weight: 600;
	gap: 4px;
	height: 28px;
	padding: 0 10px;
	transition: background 150ms ease, border-color 150ms ease;
	vertical-align: middle;
	white-space: nowrap;
}

.dpm-action-primary-btn:hover {
	background: #ccfbf1;
	border-color: #14b8a6;
}

.dpm-action-icon-btn {
	align-items: center;
	background: #ffffff;
	border: 1px solid #e2e8f0;
	border-radius: 6px;
	color: #64748b;
	cursor: pointer;
	display: inline-flex;
	height: 28px;
	justify-content: center;
	margin-left: 4px;
	transition: background 150ms ease, border-color 150ms ease, color 150ms ease;
	vertical-align: middle;
	width: 28px;
}

.dpm-action-icon-btn:hover {
	background: #f0fdfa;
	border-color: #14b8a6;
	color: #0f766e;
}

.dpm-row-menu {
	display: inline-block;
	vertical-align: middle;
}

.dpm-row-menu .dropdown-menu {
	min-width: 140px;
}

.dpm-row-menu .dropdown-menu li > a {
	cursor: pointer;
	font-size: 13px;
	padding: 6px 14px;
}

.dpm-row-menu .dropdown-menu .text-danger {
	color: #dc2626 !important;
}

/* ── Table Footer ────────────────────────────────────────── */
.dpm-table-footer {
	align-items: center;
	background: #ffffff;
	border-top: 1px solid #f1f5f9;
	display: flex;
	justify-content: space-between;
	padding: 8px 16px;
}

.dpm-footer-count,
.dpm-footer-note {
	color: #94a3b8;
	font-size: 11px;
}

/* ── Empty States ────────────────────────────────────────── */
.dpm-empty {
	background: #f8fafc;
	border: 1px dashed #cbd5e1;
	border-radius: 8px;
	color: #64748b;
	display: grid;
	gap: 4px;
	padding: 14px;
}

.dpm-empty strong {
	color: #1f2937;
}

.dpm-empty-large {
	margin: 20px;
	min-height: 160px;
	place-content: center;
	text-align: center;
}

.dpm-empty-icon {
	color: #cbd5e1;
	margin-bottom: 10px;
}

.dpm-empty-icon svg {
	height: 40px;
	width: 40px;
}

/* ── Permission Dialog ───────────────────────────────────── */
.dpm-permission-dialog .modal-dialog {
	max-width: min(1240px, calc(100vw - 48px));
	width: min(1240px, calc(100vw - 48px));
}

.dpm-permission-dialog .modal-body {
	max-height: 70vh;
	overflow-y: auto;
	position: relative;
}

.dpm-user-permission-summary {
	align-items: center;
	background: #f8fafc;
	border: 1px solid #e2e8f0;
	border-radius: 8px;
	display: flex;
	justify-content: space-between;
	margin-bottom: 12px;
	padding: 12px 14px;
}

.dpm-panel-title {
	color: #1f2937;
	font-size: 14px;
	font-weight: 700;
}

.dpm-permission-grid {
	display: grid;
	gap: 14px;
	padding: 14px;
}

.dpm-permission-group {
	border: 1px solid #dfe5ee;
	border-radius: 8px;
	overflow: hidden;
}

.dpm-permission-group-title {
	background: #f8fafc;
	border-bottom: 1px solid #e2e8f0;
	color: #172033;
	font-size: 13px;
	font-weight: 800;
	padding: 10px 12px;
}

.dpm-permission-table {
	min-width: 980px;
}

.dpm-permission-table thead th {
	background: #f8fafc;
	box-shadow: 0 1px 0 #e5e7eb;
	position: sticky;
	top: 0;
	z-index: 2;
}

.dpm-permission-table th:not(:first-child),
.dpm-permission-table td:not(:first-child) {
	text-align: center;
	width: 74px;
}

.dpm-permission-table tbody tr:hover td {
	background: #fbfefd;
}

.dpm-permission-item {
	display: grid;
	gap: 2px;
	min-width: 220px;
}

.dpm-permission-item strong {
	color: #111827;
	font-size: 13px;
}

.dpm-permission-item span {
	color: #64748b;
	font-size: 12px;
}

/* ── Permission Checkboxes ───────────────────────────────── */
.dpm-perm-cell {
	align-items: center;
	cursor: pointer;
	display: inline-flex;
	height: 36px;
	justify-content: center;
	margin: 0;
	position: relative;
	width: 38px;
}

.dpm-perm-cell input[type="checkbox"] {
	inset: 0;
	opacity: 0;
	position: absolute;
	z-index: 2;
}

.dpm-perm-box {
	align-items: center;
	background: #ffffff;
	border: 1.5px solid #cbd5e1;
	border-radius: 6px;
	box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
	display: inline-flex;
	height: 20px;
	justify-content: center;
	position: relative;
	transition: background 140ms ease, border-color 140ms ease, box-shadow 140ms ease;
	width: 20px;
}

.dpm-perm-box::after {
	border: 2px solid #ffffff;
	border-left: 0;
	border-top: 0;
	content: "";
	height: 10px;
	opacity: 0;
	position: absolute;
	top: 3px;
	transform: rotate(45deg) scale(0.7);
	transition: opacity 120ms ease, transform 120ms ease;
	width: 6px;
}

.dpm-perm-cell:hover:not(.is-disabled) .dpm-perm-box {
	border-color: #0f766e;
	box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.1);
}

.dpm-perm-cell input[type="checkbox"]:focus-visible + .dpm-perm-box {
	border-color: #0f766e;
	box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.18);
}

.dpm-perm-cell input[type="checkbox"]:checked + .dpm-perm-box {
	background: #0f766e;
	border-color: #0f766e;
	box-shadow: 0 5px 14px rgba(15, 118, 110, 0.18);
}

.dpm-perm-cell input[type="checkbox"]:checked + .dpm-perm-box::after {
	opacity: 1;
	transform: rotate(45deg) scale(1);
}

.dpm-perm-cell input[type="checkbox"]:disabled + .dpm-perm-box {
	background: #f8fafc;
	border-color: #e5e7eb;
	box-shadow: none;
	cursor: not-allowed;
}

.dpm-perm-cell.is-disabled {
	cursor: not-allowed;
	opacity: 0.58;
}

/* ── Saving Overlay ──────────────────────────────────────── */
.dpm-permission-dialog.dpm-is-saving .dpm-user-permission-summary,
.dpm-permission-dialog.dpm-is-saving .dpm-permission-grid {
	opacity: 0.42;
	user-select: none;
}

.dpm-dialog-saving {
	align-items: center;
	background: rgba(248, 250, 252, 0.78);
	display: flex;
	inset: 0;
	justify-content: center;
	pointer-events: auto;
	position: absolute;
	z-index: 5;
}

.dpm-dialog-saving[hidden] {
	display: none !important;
}

.dpm-saving-card {
	align-items: center;
	background: #ffffff;
	border: 1px solid #dbe4ee;
	border-radius: 8px;
	box-shadow: 0 14px 34px rgba(15, 23, 42, 0.12);
	color: #172033;
	display: inline-flex;
	font-size: 14px;
	font-weight: 600;
	gap: 10px;
	min-height: 44px;
	padding: 10px 14px;
}

.dpm-spinner,
.dpm-btn-spinner {
	animation: dpm-spin 800ms linear infinite;
	border: 2px solid rgba(15, 118, 110, 0.22);
	border-radius: 999px;
	border-top-color: #0f766e;
	display: inline-block;
	flex: 0 0 auto;
	height: 18px;
	width: 18px;
}

.dpm-btn-spinner {
	border-color: rgba(255, 255, 255, 0.38);
	border-top-color: #ffffff;
	height: 14px;
	margin-right: 7px;
	vertical-align: -2px;
	width: 14px;
}

.dpm-btn-loading {
	align-items: center;
	display: inline-flex;
	justify-content: center;
}

@keyframes dpm-spin {
	to { transform: rotate(360deg); }
}

/* ── Dialog Form Components ──────────────────────────────── */
.dpm-role-checks {
	display: grid;
	gap: 8px;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	margin-top: 4px;
}

.dpm-role-check {
	align-items: center;
	background: #f8fafc;
	border: 1px solid #e2e8f0;
	border-radius: 8px;
	cursor: pointer;
	display: flex;
	gap: 8px;
	margin: 0;
	min-height: 42px;
	padding: 9px 10px;
}

.dpm-role-check span {
	font-weight: 600;
}

.dpm-dialog-empty {
	background: #fff7ed;
	border: 1px solid #fed7aa;
	border-radius: 8px;
	color: #9a3412;
	padding: 10px 12px;
}

.dpm-password-note {
	background: #ecfeff;
	border: 1px solid #a5f3fc;
	border-radius: 8px;
	color: #155e75;
	font-size: 13px;
	line-height: 1.45;
	padding: 10px 12px;
}

.dpm-employee-note {
	background: #f8fafc;
	border: 1px solid #e2e8f0;
	border-radius: 8px;
	color: #334155;
	display: grid;
	font-size: 13px;
	gap: 3px;
	line-height: 1.4;
	padding: 10px 12px;
}

.dpm-employee-note span {
	color: #64748b;
	overflow-wrap: anywhere;
}

.dpm-employee-note.is-muted {
	border-style: dashed;
}

.dpm-employee {
	display: grid;
	gap: 2px;
}

.dpm-employee strong {
	color: #111827;
	font-size: 13px;
	line-height: 1.25;
}

.dpm-employee span {
	color: #6b7280;
	font-size: 12px;
}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 900px) {
	.dcnet-permission-page {
		padding: 10px;
	}

	.dpm-stats {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.dpm-layout {
		flex-direction: column;
	}

	.dpm-sidebar {
		border-bottom: 1px solid #e2e8f0;
		border-right: none;
		width: 100%;
	}

	.dpm-scopes {
		flex-direction: row;
		flex-wrap: wrap;
		max-height: 120px;
	}

	.dpm-toolbar {
		flex-wrap: wrap;
	}

	.dpm-toolbar-gap {
		flex: 0 0 100%;
		order: 3;
	}
}

@media (max-width: 560px) {
	.dpm-stats {
		grid-template-columns: 1fr;
	}

	.dpm-role-checks {
		grid-template-columns: 1fr;
	}
}
```

- [ ] **Step 2: Commit CSS rewrite**

```bash
cd /Users/khoa/Desktop/flow_next
git add dcnet-permission/dcnet_permission/public/css/dcnet_permission_manager.css
git commit -m "feat(dcnet-permission): rewrite CSS — Clean Card + Teal Brand design system"
```

---

## Task 2: Update renderShell and renderStats in JS

**Files:**
- Modify: `dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js`

**Changes:** `renderShell()` adds sidebar-title, sidebar-count, sidebar-search-input. `renderStats()` adds stat-icon + stat-body wrapper with SVG icons.

- [ ] **Step 1: Replace renderShell()**

Find:
```js
		renderShell() {
			this.page.main.html(`
				<div class="dpm-root">
					<section class="dpm-stats" aria-live="polite"></section>

					<div class="dpm-layout">
						<aside class="dpm-sidebar">
							<div class="dpm-sidebar-head">
								<span class="dpm-panel-title">${__("Managed Scope")}</span>
							</div>
							<div class="dpm-scopes"></div>
						</aside>

						<main class="dpm-main">
							<div class="dpm-main-body"></div>
						</main>
					</div>
				</div>
			`);
		}
```

Replace with:
```js
		renderShell() {
			this.page.main.html(`
				<div class="dpm-root">
					<section class="dpm-stats" aria-live="polite"></section>

					<div class="dpm-layout">
						<aside class="dpm-sidebar">
							<div class="dpm-sidebar-head">
								<span class="dpm-sidebar-title">${__("Departments")}</span>
								<span class="dpm-sidebar-count">0</span>
							</div>
							<div class="dpm-sidebar-search">
								<input class="dpm-sidebar-search-input" type="search" placeholder="${__("Search...")}" />
							</div>
							<div class="dpm-scopes"></div>
						</aside>

						<main class="dpm-main">
							<div class="dpm-main-body"></div>
						</main>
					</div>
				</div>
			`);
		}
```

- [ ] **Step 2: Replace renderStats()**

Find the entire `renderStats()` method:
```js
		renderStats() {
			const stats = this.state.dashboard?.stats || {};
			const cards = [
				{ label: __("Departments"), value: stats.departments || 0 },
				{ label: __("Managed Users"), value: stats.users || 0 },
				{ label: __("Active"), value: stats.enabled_users || 0 },
				{ label: __("Permission Items"), value: stats.permission_items || 0 },
			];

			this.page.main.find(".dpm-stats").html(
				cards
					.map(
						(card) => `
							<div class="dpm-stat-card">
								<div class="dpm-stat-value">${frappe.utils.escape_html(String(card.value))}</div>
								<div class="dpm-stat-label">${card.label}</div>
							</div>
						`
					)
					.join("")
			);
		}
```

Replace with:
```js
		renderStats() {
			const stats = this.state.dashboard?.stats || {};
			const cards = [
				{
					label: __("Departments"),
					value: stats.departments || 0,
					iconBg: "#f0fdfa",
					iconColor: "#0f766e",
					icon: '<path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>',
				},
				{
					label: __("Managed Users"),
					value: stats.users || 0,
					iconBg: "#eff6ff",
					iconColor: "#2563eb",
					icon: '<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>',
				},
				{
					label: __("Active"),
					value: stats.enabled_users || 0,
					iconBg: "#f0fdf4",
					iconColor: "#16a34a",
					icon: '<path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
				},
				{
					label: __("Permission Items"),
					value: stats.permission_items || 0,
					iconBg: "#fff7ed",
					iconColor: "#ea580c",
					icon: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>',
				},
			];

			this.page.main.find(".dpm-stats").html(
				cards
					.map(
						(card) => `
							<div class="dpm-stat-card">
								<div class="dpm-stat-icon" style="background:${card.iconBg}">
									<svg viewBox="0 0 24 24" fill="none" stroke="${card.iconColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${card.icon}</svg>
								</div>
								<div class="dpm-stat-body">
									<div class="dpm-stat-value">${frappe.utils.escape_html(String(card.value))}</div>
									<div class="dpm-stat-label">${card.label}</div>
								</div>
							</div>
						`
					)
					.join("")
			);
		}
```

- [ ] **Step 3: Commit**

```bash
git add dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js
git commit -m "feat(dcnet-permission): update shell and stat cards with icons"
```

---

## Task 3: Update renderScopes and add avatarColorIndex

**Files:**
- Modify: `dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js`

- [ ] **Step 1: Add `avatarColorIndex()` helper method**

Add this method inside the `DCNETPermissionManager` class, just before the closing `}` of the class (after `initials()`):

```js
		avatarColorIndex(user) {
			const source = user.full_name || user.email || "";
			const initial = source.trim()[0] || "A";
			return initial.toUpperCase().charCodeAt(0) % 5;
		}
```

- [ ] **Step 2: Update renderScopes() to set sidebar count + wire sidebar search**

At the end of `renderScopes()`, after the event binding block `this.page.main.find(".dpm-scope").on("click", ...)`, add:

```js
			this.page.main.find(".dpm-sidebar-count").text(departments.length);

			this.page.main.find(".dpm-sidebar-search-input").on("input", (event) => {
				const query = (event.target.value || "").trim().toLowerCase();
				this.page.main.find(".dpm-scope").each((_i, el) => {
					const name = (el.dataset.department || "").toLowerCase();
					el.style.display = !query || name.includes(query) ? "" : "none";
				});
			});
```

- [ ] **Step 3: Commit**

```bash
git add dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js
git commit -m "feat(dcnet-permission): add sidebar count, search filter, avatarColorIndex helper"
```

---

## Task 4: Update renderUsers — new toolbar

**Files:**
- Modify: `dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js`

**Change:** Replace toolbar HTML in `renderUsers()` to include dept label + count on left, search + filter on right.

- [ ] **Step 1: Replace renderUsers()**

Find the entire `renderUsers()` method:
```js
		renderUsers() {
			const body = this.page.main.find(".dpm-main-body");
			body.html(`
				<div class="dpm-toolbar">
					<div class="dpm-search-wrap">
						<input class="dpm-search form-control" type="search" placeholder="${__("Search user, email, role")}" value="${frappe.utils.escape_html(this.state.query)}" />
					</div>
					<select class="dpm-status form-control">
						<option value="enabled">${__("Active")}</option>
						<option value="disabled">${__("Disabled")}</option>
						<option value="all">${__("All")}</option>
					</select>
				</div>
				<div class="dpm-users"></div>
			`);
			body.find(".dpm-status").val(this.state.status);
			body.find(".dpm-search").on("input", (event) => {
				this.state.query = event.target.value || "";
				this.renderUserRows();
			});
			body.find(".dpm-status").on("change", (event) => {
				this.state.status = event.target.value || "enabled";
				this.renderUserRows();
			});
			this.renderUserRows();
		}
```

Replace with:
```js
		renderUsers() {
			const body = this.page.main.find(".dpm-main-body");
			const dept = this.state.department;
			const userCount = (this.state.dashboard?.users || []).filter((u) => u.department === dept).length;
			const countBadge = dept ? `<span class="dpm-dept-count">${userCount} ${__("users")}</span>` : "";

			body.html(`
				<div class="dpm-toolbar">
					<span class="dpm-dept-label">${frappe.utils.escape_html(dept || __("Select a department"))}</span>
					${countBadge}
					<div class="dpm-toolbar-gap"></div>
					<div class="dpm-search-wrap">
						<input class="dpm-search form-control" type="search" placeholder="${__("Search user, email, role")}" value="${frappe.utils.escape_html(this.state.query)}" />
					</div>
					<select class="dpm-status form-control">
						<option value="enabled">${__("Active")}</option>
						<option value="disabled">${__("Disabled")}</option>
						<option value="all">${__("All")}</option>
					</select>
				</div>
				<div class="dpm-users"></div>
			`);
			body.find(".dpm-status").val(this.state.status);
			body.find(".dpm-search").on("input", (event) => {
				this.state.query = event.target.value || "";
				this.renderUserRows();
			});
			body.find(".dpm-status").on("change", (event) => {
				this.state.status = event.target.value || "enabled";
				this.renderUserRows();
			});
			this.renderUserRows();
		}
```

- [ ] **Step 2: Commit**

```bash
git add dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js
git commit -m "feat(dcnet-permission): new toolbar with dept label and count badge"
```

---

## Task 5: Update renderUserRows — new table structure

**Files:**
- Modify: `dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js`

**Change:** Remove `dpm-users-head`, remove Employee column, use circular avatar with color class, new action buttons, add table footer.

- [ ] **Step 1: Replace renderUserRows()**

Find the entire `renderUserRows()` method and replace with:

```js
		renderUserRows() {
			const users = this.filteredUsers();
			const currentDepartment = this.state.department;
			const usersWrapper = this.page.main.find(".dpm-users");

			if (!currentDepartment) {
				usersWrapper.html(`
					<div class="dpm-empty dpm-empty-large">
						<div class="dpm-empty-icon">${frappe.utils.icon("shield", "xl")}</div>
						<strong>${__("No Data")}</strong>
						<span>${__("No department scope is assigned to you.")}</span>
					</div>
				`);
				return;
			}

			if (!users.length) {
				usersWrapper.html(`
					<div class="dpm-empty dpm-empty-large">
						<div class="dpm-empty-icon">${frappe.utils.icon("users", "xl")}</div>
						<strong>${__("No Matching Users")}</strong>
						<span>${__("Create a new user or change filters.")}</span>
					</div>
				`);
				return;
			}

			const rows = users
				.map((user) => {
					const statusClass = user.enabled ? "is-enabled" : "is-disabled";
					const statusLabel = user.enabled ? __("Active") : __("Disabled");
					const colorIdx = this.avatarColorIndex(user);
					const rolesHtml = this.renderUserRoleChips(user);

					return `
						<tr>
							<td>
								<div class="dpm-user">
									<div class="dpm-avatar dpm-avatar--${colorIdx}">${this.initials(user)}</div>
									<div>
										<div class="dpm-user-name">${frappe.utils.escape_html(user.full_name || user.email)}</div>
										<div class="dpm-user-email">${frappe.utils.escape_html(user.email || user.name)}</div>
									</div>
								</div>
							</td>
							<td>
								<span class="dpm-status-pill ${statusClass}">
									<span class="dpm-status-dot"></span>${statusLabel}
								</span>
							</td>
							<td><div class="dpm-role-list">${rolesHtml}</div></td>
							<td class="dpm-actions">
								<button class="dpm-action-primary-btn dpm-edit-permissions" data-user="${frappe.utils.escape_html(user.name)}">
									${frappe.utils.icon("lock", "xs")} ${__("Permissions")}
								</button>
								<button class="dpm-action-icon-btn dpm-edit" data-user="${frappe.utils.escape_html(user.name)}" title="${__("Edit User")}">
									${frappe.utils.icon("edit", "xs")}
								</button>
								<div class="dropdown dpm-row-menu">
									<button class="dpm-action-icon-btn dropdown-toggle" data-toggle="dropdown" title="${__("More")}">
										${frappe.utils.icon("dot-horizontal", "xs")}
									</button>
									<ul class="dropdown-menu dropdown-menu-right">
										<li><a class="dpm-disable text-danger" data-user="${frappe.utils.escape_html(user.name)}" ${user.enabled ? "" : 'style="opacity:0.4;pointer-events:none"'}>${__("Disable")}</a></li>
									</ul>
								</div>
							</td>
						</tr>
					`;
				})
				.join("");

			const allInDept = (this.state.dashboard?.users || []).filter((u) => u.department === currentDepartment);

			usersWrapper.html(`
				<div class="dpm-table-wrap">
					<table class="table dpm-table">
						<thead>
							<tr>
								<th>${__("User")}</th>
								<th>${__("Status")}</th>
								<th>${__("Roles")}</th>
								<th></th>
							</tr>
						</thead>
						<tbody>${rows}</tbody>
					</table>
				</div>
				<div class="dpm-table-footer">
					<span class="dpm-footer-count">${__("{0} / {1} users", [users.length, allInDept.length])}</span>
					<span class="dpm-footer-note">${frappe.utils.escape_html(currentDepartment)}</span>
				</div>
			`);

			usersWrapper.find(".dpm-edit-permissions").on("click", (event) => {
				this.openUserPermissions(event.currentTarget.dataset.user);
			});
			usersWrapper.find(".dpm-edit").on("click", (event) => {
				event.preventDefault();
				const user = this.findUser(event.currentTarget.dataset.user);
				this.openForm(user);
			});
			usersWrapper.find(".dpm-disable").on("click", (event) => {
				event.preventDefault();
				this.disableUser(event.currentTarget.dataset.user);
			});
		}
```

- [ ] **Step 2: Commit**

```bash
git add dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js
git commit -m "feat(dcnet-permission): new table — circular avatar, role tags, action buttons, footer"
```

---

## Task 6: Update renderUserRoleChips

**Files:**
- Modify: `dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js`

**Change:** Use new `.dpm-role-tag` classes instead of `.dpm-role-chip`. Show max 2 roles with `+N` overflow badge.

- [ ] **Step 1: Replace renderUserRoleChips()**

Find:
```js
		renderUserRoleChips(user) {
			const roleChips = (user.roles || [])
				.map((role) => `<span class="dpm-role-chip">${frappe.utils.escape_html(role)}</span>`)
				.join("");
			const personalChip =
				user.permission_mode === "user"
					? `<span class="dpm-role-chip is-personal">${__("Custom Permissions")}</span>`
					: "";
			return roleChips || personalChip || `<span class="dpm-muted">${__("No scoped roles")}</span>`;
		}
```

Replace with:
```js
		renderUserRoleChips(user) {
			if (user.permission_mode === "user") {
				return `<span class="dpm-role-tag dpm-role-tag--primary">${__("Custom Permissions")}</span>`;
			}

			const roles = user.roles || [];
			if (!roles.length) {
				return `<span class="dpm-muted">${__("No scoped roles")}</span>`;
			}

			const maxVisible = 2;
			const visible = roles.slice(0, maxVisible);
			const overflow = roles.length - maxVisible;

			const chips = visible
				.map((role, i) => `<span class="dpm-role-tag ${i === 0 ? "dpm-role-tag--primary" : ""}">${frappe.utils.escape_html(role)}</span>`)
				.join("");
			const overflowChip = overflow > 0 ? `<span class="dpm-role-tag dpm-role-tag--more">+${overflow}</span>` : "";

			return chips + overflowChip;
		}
```

- [ ] **Step 2: Commit**

```bash
git add dcnet-permission/dcnet_permission/public/js/dcnet_permission_manager.js
git commit -m "feat(dcnet-permission): role tags — teal primary, gray secondary, +N overflow"
```

---

## Task 7: Clear cache and smoke test

- [ ] **Step 1: Clear Frappe cache**

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

Expected output: `Cache cleared`

- [ ] **Step 2: Open the page in browser**

Navigate to `http://flow.local/dcnet-permission-manager` (or the site URL).

Verify visually:
1. Stats row: 4 cards with SVG icons (teal/blue/green/orange), value 20px bold, label muted
2. Sidebar: "DEPARTMENTS" label + count badge + search input + compact scope list with teal active state
3. Toolbar: dept name + count pill on left, search + filter on right
4. Table: circular avatar with color, Status pill (green/gray + dot), role tags (teal primary + gray secondary + +N), "Permissions" teal button + icon buttons
5. Table footer: user count + scope name
6. Loading shimmer on stats while fetching

- [ ] **Step 3: Test interactions**

- Click a different department → sidebar active state updates, toolbar dept label updates, table reloads
- Type in search → table filters instantly
- Change status filter → table filters
- Click "Permissions" → dialog opens (existing behavior unchanged)
- Click edit icon → user form dialog opens
- Click ⋯ → dropdown shows Disable option
- Type in sidebar search → scopes filter by name

- [ ] **Step 4: Final commit if any tweaks needed**

```bash
git add dcnet-permission/dcnet_permission/public/
git commit -m "fix(dcnet-permission): visual tweaks after smoke test"
```
