# dcnet-crm — Design Spec

**Date:** 2026-06-12
**Status:** Approved
**Source:** Analysis of 10 MISA AMIS CRM tutorial videos → `docs/competitor-analysis/misa-amis/crm/ANALYSIS.md`

---

## Goal

Build a CRM module (`dcnet-crm`) that clones MISA AMIS CRM's UI style and core features on top of Frappe + ERPNext. Display name: **CRM**. Reuse ERPNext's existing CRM DocTypes (Lead, Opportunity, Contact, Customer, Quotation, Sales Order) — only create new DocTypes where ERPNext has nothing.

---

## Approach

**Separate Frappe app** (`dcnet-crm`) following the `dcnet-permission` pattern — same repo level, installed alongside dcnet_apps. Full custom Vue SPA as the UI layer, Python API endpoints calling ERPNext DocTypes directly.

---

## App Structure

```
dcnet-crm/
├── setup.py
└── dcnet_crm/
    ├── __init__.py
    ├── hooks.py                  ← register page, custom fields, fixtures
    ├── modules.txt               ← "CRM"
    ├── crm/
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── dashboard.py      ← KPI data, funnel, growth charts
    │   │   ├── leads.py          ← list, detail, convert, activities
    │   │   ├── opportunities.py  ← list, pipeline/kanban data
    │   │   ├── customers.py      ← list, detail, transaction history
    │   │   ├── contacts.py       ← list, detail
    │   │   ├── quotations.py     ← list, detail, generate SO
    │   │   ├── orders.py         ← list, detail, ghi doanh số actions
    │   │   ├── import_wizard.py  ← parse Excel, field mapping, batch insert
    │   │   ├── reports.py        ← 20+ report queries
    │   │   └── scoring.py        ← compute lead score from rules
    │   ├── doctype/
    │   │   └── crm_lead_score_rule/
    │   │       ├── crm_lead_score_rule.json
    │   │       └── crm_lead_score_rule.py
    │   └── page/
    │       └── crm/
    │           ├── crm.html      ← <div id="crm-app">
    │           ├── crm.py        ← has_permission check
    │           └── crm.js        ← load built Vue bundle
    └── public/
        └── dist/                 ← Vite build output (JS + CSS)
```

---

## Vue App Structure

```
dcnet_crm/crm/page/crm/src/
├── main.js
├── App.vue                        ← CRMLayout shell
├── router/index.js
├── stores/
│   ├── auth.js                    ← current user, permissions
│   └── crm.js                     ← shared state (filters, active record)
├── components/
│   ├── layout/
│   │   ├── CRMTopNav.vue          ← 10 nav items + settings icon
│   │   └── CRMSettingsSidebar.vue ← slide-in ⚙ panel
│   ├── list/
│   │   ├── TriPaneListView.vue    ← reusable wrapper (config via props)
│   │   ├── FilterPanel.vue        ← saved filters + filter fields
│   │   ├── ListTable.vue          ← sortable, selectable rows + row actions
│   │   ├── BulkActionBar.vue      ← contextual toolbar when rows selected
│   │   └── ActivityFeedPanel.vue  ← right panel, loads per selected row
│   ├── dashboard/
│   │   ├── KPICard.vue            ← value + % change + icon
│   │   ├── FunnelChart.vue        ← opportunity stages funnel
│   │   └── GrowthChart.vue        ← line chart (orders/customers/revenue)
│   ├── form/
│   │   ├── CRMForm.vue            ← generic field renderer
│   │   └── ActivityLogger.vue     ← log call / task / note
│   └── shared/
│       ├── ImportWizard.vue       ← 4-step Excel import modal
│       ├── AvatarInitials.vue     ← circular avatar with color hash
│       └── StatusBadge.vue        ← pill badge per stage/status
└── views/
    ├── CRMDashboard.vue
    ├── leads/
    │   ├── LeadList.vue           ← TriPaneListView config for Lead
    │   └── LeadDetail.vue
    ├── opportunities/
    │   ├── OpportunityList.vue    ← list view + kanban toggle
    │   └── OpportunityDetail.vue
    ├── customers/
    │   ├── CustomerList.vue
    │   └── CustomerDetail.vue
    ├── contacts/
    │   └── ContactList.vue
    ├── quotations/
    │   ├── QuotationList.vue
    │   └── QuotationDetail.vue
    ├── orders/
    │   ├── OrderList.vue
    │   └── OrderDetail.vue        ← includes Ghi doanh số actions
    └── reports/
        └── ReportsView.vue
```

---

## Routes

| Path | View | MISA Equivalent |
|------|------|----------------|
| `/crm` | CRMDashboard | Báo cáo ban quản trị |
| `/crm/leads` | LeadList | Tiềm năng |
| `/crm/leads/:name` | LeadDetail | Chi tiết Tiềm năng |
| `/crm/opportunities` | OpportunityList | Cơ hội |
| `/crm/opportunities/:name` | OpportunityDetail | Chi tiết Cơ hội |
| `/crm/customers` | CustomerList | Khách hàng |
| `/crm/customers/:name` | CustomerDetail | Chi tiết Khách hàng |
| `/crm/contacts` | ContactList | Liên hệ |
| `/crm/quotations` | QuotationList | Báo giá |
| `/crm/quotations/:name` | QuotationDetail | Chi tiết Báo giá |
| `/crm/orders` | OrderList | Đơn hàng |
| `/crm/orders/:name` | OrderDetail | Chi tiết Đơn hàng |
| `/crm/reports` | ReportsView | Báo cáo |
| `/crm/settings` | SettingsView | Thiết lập |

---

## TriPaneListView — Core UI Pattern

```
┌──────────────┬──────────────────────────────┬───────────────────┐
│ FILTER PANEL │        LIST TABLE            │  ACTIVITY FEED    │
│  (240px)     │      (flex grow)             │    (320px)        │
│              │                              │                   │
│ Bộ lọc đã   │ ☐  Tên  ĐT  Email  Nguồn   │ (hiện khi click   │
│ lưu:         │ ☐  Nguyễn A  0901..  @..   │  1 row)           │
│  • Tháng này │ ☐  Trần B    0912..  @..   │                   │
│  • Tuần này  │                              │ Lịch sử GD:       │
│              │ ── khi select rows ──        │ 📞 Gọi 10p  2/6  │
│ LỌC THEO:   │ [Gắn thẻ][Cập nhật]         │ ✉ Email      1/6  │
│ Tên...       │ [Chuyển đổi][Xóa]...        │ 📋 Task done 30/5 │
│ Nguồn...     │                              │                   │
│ Trạng thái.. │                              │ [Gọi][Email][+]   │
└──────────────┴──────────────────────────────┴───────────────────┘
```

`TriPaneListView` nhận config prop:
```js
{
  doctype: 'Lead',
  columns: [...],
  filters: [...],
  bulkActions: [...],
  rowActions: ['call', 'email', 'task']
}
```

---

## New DocTypes

### `CRM Lead Score Rule`

| Field | Type | Description |
|-------|------|-------------|
| rule_name | Data | Tên rule |
| field_name | Select | Field của Lead (nguon_goc, tinh_trang...) |
| operator | Select | `=`, `!=`, `>`, `<`, `contains` |
| value | Data | Giá trị so sánh |
| score | Int | Điểm cộng nếu match |
| is_active | Check | Bật/tắt rule |

---

## Custom Fields (trên ERPNext DocTypes)

| DocType | Field Name | Type | Label |
|---------|-----------|------|-------|
| Lead | `lead_score` | Int | Điểm tiềm năng |
| Lead | `lead_score_detail` | Text | Chi tiết điểm (JSON) |
| Sales Order | `revenue_recognition_status` | Select | Tình trạng ghi doanh số |
| Sales Order | `revenue_recognition_date` | Date | Ngày ghi doanh số |
| Sales Order | `revenue_recognition_by` | Link → User | Người ghi doanh số |

`revenue_recognition_status` options: `Bản nhập`, `Đề nghị ghi`, `Đã ghi doanh số`

---

## ERPNext Workflow — Ghi doanh số

Applied to: **Sales Order**
Field: `revenue_recognition_status`

```
Bản nhập
  → [Đề nghị ghi DS]  (role: Nhân viên KD)
Đề nghị ghi
  → [Duyệt & Ghi]     (role: Trưởng phòng / Kế toán)
  → [Thu hồi]         (role: Nhân viên KD)
Đã ghi doanh số
  → [Đề nghị xuất HĐ] (role: Nhân viên KD)
```

---

## Import Excel Wizard — 4 Steps

```
Step 1 — Upload
  Drag & drop .xlsx/.csv
  Preview 5 rows
  Limit: 5,000 rows (.xlsx), unlimited (.csv)

Step 2 — Map fields
  Source column vs target field
  Màu xanh = matched tự động
  Màu cam = chưa map (cần chọn)
  Inline search khi type tên field

Step 3 — Assign owner
  Option A: Chọn user từ list
  Option B: Assignment rule
  Option C: Lấy từ cột trong file

Step 4 — Execute
  Progress bar
  Kết quả: X thành công / Y lỗi
  Download error log (.xlsx)
```

**API:** `import_wizard.py` dùng `openpyxl` parse → validate → `frappe.get_doc().insert()` batch

---

## MISA Color Scheme

```css
--crm-primary:     #1a73e8;
--crm-teal:        #00897b;
--crm-success:     #34a853;
--crm-warning:     #fbbc04;
--crm-danger:      #ea4335;
--crm-sidebar-bg:  #f8f9fa;
--crm-border:      #e0e0e0;
--crm-text:        #202124;
--crm-text-muted:  #5f6368;
--crm-nav-height:  48px;
--crm-filter-w:    240px;
--crm-feed-w:      320px;
```

---

## Data Flow

```
Vue Component
  → frappe.call('dcnet_crm.crm.api.leads.get_leads', { filters, page, page_length })
    → Python: frappe.db.get_list('Lead', filters=..., fields=...) 
      → return { data: [...], total: N }
        → Vue reactive state update → render
```

All API methods decorated with `@frappe.whitelist()`. Permission checked via `frappe.has_permission()` before any query.

---

## Build Summary

| Item | Count |
|------|-------|
| Frappe app | 1 (`dcnet-crm`) |
| Vue views | 14 |
| Vue components | 12 |
| New DocTypes | 1 (`CRM Lead Score Rule`) |
| Custom Fields | 5 |
| Python API modules | 9 |
| ERPNext Workflow | 1 (Ghi doanh số) |
| Reports | 10+ (Phase 1) |

---

## Out of Scope (Phase 2)

- Di tuyến / Field Sales Routing + GPS tracking
- Email Marketing integration
- SMS Brandname
- Mạng xã hội (Facebook/Zalo lead capture)
- Mobile app
