# VN Accounting UX Redesign + Sample Data Fix

**Date:** 2026-04-02
**Status:** Approved
**Scope:** 2 parallel workstreams across 2 apps

---

## Context

vn_accounting v1.0 is feature-complete (COA TT99/2025, workspace, sidebar, Number Cards, route_options). But the UX needs improvement for pro accountants migrating from Misa, and dashboard shows no data because dcnet_sample uses standard CoA instead of VN COA.

**Target users:** Kế toán trưởng (overview) + Kế toán viên (daily data entry), migrating from Misa.

---

## Workstream 1: Workspace Redesign (vn_accounting)

**App:** `/home/long/long/frappe-bench-dcnet/apps/vn_accounting/`

### 1.1 Workspace JSON Restructure

Reorganize `ke_toan_vn.json` layout:

**Row 1 — KPI Strip:** 5 Number Cards (keep as-is)

**Row 2 — Quick Create:** URL shortcuts with `link_type: "URL"` for 1-click new document creation:
- `+ Phiếu thu tiền mặt` → `/app/payment-entry/new?payment_type=Receive&mode_of_payment=Cash`
- `+ Phiếu chi tiền mặt` → `/app/payment-entry/new?payment_type=Pay&mode_of_payment=Cash`
- `+ Thu tiền ngân hàng` → `/app/payment-entry/new?payment_type=Receive&mode_of_payment=Bank`
- `+ Chi tiền ngân hàng` → `/app/payment-entry/new?payment_type=Pay&mode_of_payment=Bank`
- `+ Hóa đơn bán hàng` → `/app/sales-invoice/new`
- `+ Hóa đơn mua hàng` → `/app/purchase-invoice/new`
- `+ Bút toán` → `/app/journal-entry/new`

**Row 3 — Shortcuts by Section:** Group existing shortcuts under section headers matching Misa categories:
- **Tiền mặt & Ngân hàng** — Payment Entry list, Bank Account, Bank Reconciliation
- **Mua hàng** — Purchase Invoice, Purchase Order, Supplier list
- **Bán hàng** — Sales Invoice, Sales Order, Customer list  
- **Kho** — Stock Entry, Stock Ledger, Stock Balance
- **Tổng hợp & Báo cáo** — Journal Entry, GL, Trial Balance, P&L, Balance Sheet, Cash Flow

**Row 4 — Charts:** 4 Dashboard Charts (keep as-is)

### 1.2 Sidebar Accordion JS

Extend existing `sidebar_route_options.bundle.js`:

- **Auto-accordion:** Click section header → open that section, close all others
- **localStorage memory:** Save open section key in `localStorage('vn_sidebar_open')`
- **Restore on page load:** Read localStorage, auto-open saved section
- **Default:** First section ("Quỹ tiền mặt") open on first visit

### 1.3 Sidebar CSS Styling

New CSS bundle `vn_accounting.bundle.css` via `app_include_css` in hooks.py:

- Compact spacing (reduce padding between items)
- Section header styling (slightly bolder, subtle background)
- Active item highlight
- Smooth collapse/expand transition
- Professional, clean look matching Misa's sidebar density

### 1.4 Sidebar Cleanup

Review and optimize `ke_toan_vn.json` sidebar:
- Remove duplicate links (GL appears twice currently)
- Merge related sections where logical
- Ensure consistent naming convention (Vietnamese with diacritics)
- Add missing dividers between major sections

---

## Workstream 2: Sample Data COA Fix (dcnet_sample)

**App:** `/home/long/long/frappe-bench-dcnet/apps/dcnet_sample/`

### 2.1 Root Cause

dcnet_sample creates Company "DCNET" with standard ERPNext CoA (English account names). vn_accounting Number Cards query VN account codes (TK 511, 131, 331, etc.). COA mismatch → all KPIs show 0.

### 2.2 Fix: Switch to VN COA

**company.py changes:**
- Set `chart_of_accounts` to `"Vietnam - Hệ thống TK theo TT99/2025 (DN lớn)"`
- This requires vn_accounting to be installed (add as dependency or check at runtime)
- Company country must be "Vietnam"

**transactions.py account mapping:**
Replace English account name lookups with VN account code lookups:

| Current (English) | New (VN Code) | Purpose |
|---|---|---|
| Sales/Revenue | 511 - Doanh thu | Income |
| Debtors | 131 - Phải thu | Receivables |
| Creditors | 331 - Phải trả | Payables |
| COGS | 632 - Chi phí | Cost of goods |
| Salary Expense | 642 - Chi phí quản lý | Admin expense |
| Cash | 111 - Tiền mặt | Cash account |
| Bank | 112 - Tiền gửi NH | Bank account |
| Fixed Assets | 211 - TSCĐ | Capital assets |
| Rent | 642 - Chi phí quản lý | Rent expense |
| Utility | 642 - Chi phí quản lý | Utility expense |

### 2.3 Add VAT to Transactions

- Sales Invoices: add VAT 10% output tax (TK 33311)
- Purchase Invoices: add VAT 10% input tax (TK 1331)
- Tax templates should reference VN tax accounts

### 2.4 Invocation

Add bench command or expose via `after_install` hook for easy setup:
```bash
bench --site dcnet.localhost execute dcnet_sample.setup.setup_all
```

### 2.5 Teardown

Ensure `teardown_all()` properly cleans up all VN COA-linked data.

---

## Technical Constraints

- Frappe v16.12.2 / ERPNext v16.12.0
- Workspace JSON is a fixture — changes via JSON edit + `bench migrate`
- Sidebar JSON is a separate fixture (`workspace_sidebar/`)
- JS/CSS bundles need `.bundle.js`/`.bundle.css` naming + `bench build`
- `app_include_js`/`app_include_css` in hooks.py (no path prefix)
- After hooks.py edit → `bench clear-cache`
- dcnet_sample depends on vn_accounting being installed for COA template

## Out of Scope

- Period selector on workspace (fights framework)
- Recent docs in sidebar (redundant with awesomebar)
- Custom `frappe.new_doc()` JS (URL params sufficient)
- Fixed Asset management in sample data
- Multi-currency transactions
- Inventory/stock items
