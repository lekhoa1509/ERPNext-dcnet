# HTKK Module — Design Document

> Created: 2026-03-13
> Branch: `feature/htkk`
> App: `dcnet_htkk`

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Vue 3 SPA                         │
│         ag-Grid · Spreadsheet UI · Dialogs          │
├─────────────────────────────────────────────────────┤
│              Frappe REST API Layer                   │
│         @frappe.whitelist() endpoints               │
├─────────────────────────────────────────────────────┤
│                Engine Layer                          │
│  auto_detect · data_fetcher · xml_generator ·       │
│  fingerprint                                        │
├─────────────────────────────────────────────────────┤
│              DocType / ORM Layer                     │
│  Template Manager · Declaration · Mapping Rule ·    │
│  Indicator Value · Appendix Row · Audit Log         │
├─────────────────────────────────────────────────────┤
│          Frappe Framework + ERPNext                  │
│     Sales Invoice · Purchase Invoice · GL Entry     │
└─────────────────────────────────────────────────────┘
```

## 2. DocType Relationships

```
HTKK Template Manager (1)
  │
  ├──→ has many: HTKK Mapping Rule (N)
  │      └──→ targets: HTKK Indicator Value
  │
  └──→ used by: HTKK Declaration (N)
         ├──→ has many: HTKK Indicator Value (child table)
         ├──→ has many: HTKK Appendix Row (child table)
         └──→ has many: HTKK Audit Log (linked)
```

## 3. HTKK Declaration — State Machine

```
                                ┌──────────────────┐
                                │                  │
┌───────┐   Tạo mới   ┌───────▼┐   fetch_data()  ┌────────────┐
│ Empty │─────────────→│ Draft  │────────────────→│ Data Loaded│
└───────┘              └───┬────┘←────────────────└────────────┘
                           │         re-fetch           │
                           │                            │
                     ┌─────┘                            │ Gửi duyệt
                     │ Từ chối                          │ (validate pass)
                     │                                  │
                ┌────▼─────┐                     ┌──────▼──┐
                │ Rejected │                     │ Pending │
                └──────────┘                     └────┬────┘
                                                      │
                                          Phê duyệt   │ (validate_sync pass)
                                                      │
                   ┌───────────┐              ┌───────▼───┐
                   │ Cancelled │←─────────────│ Submitted │
                   └───────────┘    Hủy       └─────┬─────┘
                                                    │
                                       Khai bổ sung  │ (trong 3 năm, max 5 lần)
                                                    │
                                              ┌─────▼─┐
                                              │ KHBS  │──→ Tạo Declaration mới
                                              └───────┘    (amendment_number + 1)
```

### State Definitions

| State | DocStatus | Editable | Mô tả |
|-------|-----------|----------|-------|
| Empty | 0 | Yes | Vừa tạo, chưa có dữ liệu |
| Draft | 0 | Yes | Đã tạo, sẵn sàng fetch data |
| Data Loaded | 0 | Yes | Đã có dữ liệu, có thể chỉnh sửa |
| Pending | 0 | No | Chờ phê duyệt, read-only |
| Rejected | 0 | Yes | Bị từ chối, quay về chỉnh sửa |
| Submitted | 1 | No | Đã chốt, có thể xuất XML |
| Cancelled | 2 | No | Đã hủy |
| KHBS | 1 | No | Đã khai bổ sung (tạo bản mới) |

### Workflow Transitions

| # | From | To | Action | Role | Điều kiện |
|---|------|----|--------|------|-----------|
| 1 | Empty | Draft | Tạo tờ khai | Accountant | Chọn template + kỳ thuế |
| 2 | Draft | Data Loaded | Lấy dữ liệu | Accountant | `fetch_data()` thành công |
| 3 | Data Loaded | Draft | Lấy lại dữ liệu | Accountant | Reset + re-fetch |
| 4 | Data Loaded | Pending | Gửi duyệt | Accountant | `validate()` pass |
| 5 | Pending | Submitted | Phê duyệt | Manager | `validate_sync()` pass |
| 6 | Pending | Rejected | Từ chối | Manager | Ghi lý do từ chối |
| 7 | Rejected | Data Loaded | Sửa lại | Accountant | Chỉnh sửa + re-validate |
| 8 | Submitted | Cancelled | Hủy tờ khai | Manager | Ghi lý do hủy |
| 9 | Submitted | KHBS | Khai bổ sung | Accountant | Trong 3 năm, max 5 lần/kỳ |

## 4. HTKK Template Manager — Lifecycle

```
Upload files (XML/XSD/XLSX)
        │
        ▼
  ┌─────────────┐
  │ Parse Schema│──→ Extract Fixed Nodes + Repeatable Nodes
  └──────┬──────┘
         │
         ▼
  ┌──────────────────┐
  │ Auto-detect      │──→ Regex + heuristic scan XLSX
  │ Indicators       │    Confidence scoring:
  └──────┬───────────┘    ● ≥90% green (chắc chắn)
         │                ● 70-90% yellow (cần duyệt)
         ▼                ● <70% red (có thể sai)
  ┌──────────────────┐
  │ Review & Confirm │──→ User duyệt từng indicator
  │ Mapping          │    Assign Named Range → Cell
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Active           │──→ Sẵn sàng dùng cho Declaration
  └──────────────────┘
```

## 5. Data Flow — End-to-End

```
1. CREATE
   User chọn Template + Kỳ thuế + Công ty
                    │
                    ▼
2. FETCH DATA
   ┌────────────────────────────────┐
   │ Mapping Rules (per indicator)  │
   │  ├─ Condition Builder          │──→ frappe.db.get_all()
   │  ├─ SQL Builder                │──→ frappe.db.sql() (parameterized)
   │  └─ Python Whitelist           │──→ custom @frappe.whitelist function
   │                                │
   │ Fingerprint each source doc    │──→ SHA-256(docname + modified)
   └────────────────────────────────┘
                    │
                    ▼
3. POPULATE
   ┌────────────────────────────────┐
   │ HTKK Indicator Value (summary) │──→ Child table (42 rows typical)
   │ HTKK Appendix Row (detail)     │──→ Background job if >5000 rows
   │ Form State                     │──→ gzip JSON → File Attachment
   └────────────────────────────────┘
                    │
                    ▼
4. USER REVIEW (Spreadsheet UI)
   ┌────────────────────────────────┐
   │ ag-Grid renders form state     │
   │  ├─ Auto cells (xanh dương)   │──→ Từ mapping rules
   │  ├─ Manual edit (vàng)        │──→ User override
   │  ├─ Formula/readonly (xám)    │──→ Computed fields
   │  └─ Error cells (đỏ)         │──→ Validation failed
   └────────────────────────────────┘
                    │
                    ▼
5. VALIDATE SYNC (Pre-submit)
   ┌────────────────────────────────┐
   │ So sánh fingerprint hiện tại  │
   │ vs fingerprint lúc fetch      │
   │  → Match: cho phép submit     │
   │  → Changed: cảnh báo user     │
   │    ├─ Quay về Draft (safe)    │
   │    └─ Force Submit (ghi nhận) │
   └────────────────────────────────┘
                    │
                    ▼
6. EXPORT XML
   ┌────────────────────────────────┐
   │ lxml build XML tree            │
   │ xmlschema validate vs XSD      │
   │ → File .xml (HTKK-compatible) │
   └────────────────────────────────┘
```

## 6. KHBS Flow (Khai bổ sung)

```
Submitted Declaration (original)
        │
        │ User click "Khai bổ sung"
        ▼
  ┌──────────────────┐
  │ System auto-diff │──→ So sánh values gốc vs hiện tại
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ KHBS Modal       │──→ Hiển thị chênh lệch
  │                  │    User chọn lý do cho mỗi chỉ tiêu
  │                  │    Tính tiền chậm nộp dự kiến
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Tạo Declaration  │──→ amendment_number = original + 1
  │ mới (bản sửa)   │    Copy data + apply changes
  │                  │    Auto-fill PL 01/KHBS
  └──────────────────┘
```

**Constraints:**
- Max 5 lần bổ sung / kỳ thuế
- Trong vòng 3 năm kể từ hạn nộp
- Mỗi lần bổ sung phải có lý do cho từng chỉ tiêu thay đổi

## 7. Mapping Rule — 3 Source Types

| Type | Target User | Mô tả | Security |
|------|-------------|-------|----------|
| **Condition Builder** | Kế toán (no-code) | UI chọn DocType, filters, aggregate | Safe — dùng frappe ORM |
| **SQL Builder** | Admin/Implementer | Viết SQL trực tiếp | Whitelist tables, SELECT only, timeout 10s, max 10k rows |
| **Python Whitelist** | Developer | Gọi hàm `@frappe.whitelist()` | Phải là hàm registered |

**Priority Resolution:** Custom rule > Standard rule (cùng indicator + company)

## 8. Security Model

| Concern | Solution |
|---------|----------|
| SQL Injection | Parameterized queries only, table whitelist |
| Concurrent editing | Optimistic locking (version field) |
| Audit trail | SHA-256 hash chain, immutable log |
| Data integrity | validate_sync() fingerprint check |
| XML injection | lxml + xmlschema validation |
| Role-based access | Accountant (create/edit), Manager (approve), Admin (templates) |

## 9. Wireframe Screens (10 screens)

| # | Screen | Mô tả |
|---|--------|-------|
| 1 | Declaration List | Danh sách tờ khai + deadline alert |
| 2 | Workspace (Draft) | Spreadsheet editable + fetch/refetch |
| 3 | Workspace (Pending) | Read-only + validate_sync warning |
| 4 | Workspace (Submitted) | Read-only + export XML |
| 5 | Auto-detect Review | Confidence scoring sidebar + XLSX preview |
| 6 | KHBS Modal | Diff table + reason select + late fee calc |
| 7 | Drilldown Popup | Source invoices for a specific indicator |
| 8 | Template Manager | Upload files + parse + auto-detect |
| 9 | Mapping Rule | Rule list + 3 source type editors |
| 10 | Package Import | Wizard (upload → check → conflict → import) |

## 10. Project Structure

```
flow_next/
├── docs/feature/htkk/           # Tài liệu gốc
│   ├── README.md
│   ├── HTKK_PRD.md
│   ├── HTKK_TECHNICAL_GUIDE.md
│   ├── HTKK_DESIGN.md           # (this file)
│   └── htkk_wireframes.jsx
│
└── dcnet_htkk/                  # Frappe app
    ├── dcnet_htkk/
    │   ├── __init__.py
    │   ├── hooks.py
    │   ├── modules.txt
    │   └── htkk/
    │       ├── doctype/
    │       │   ├── htkk_template_manager/
    │       │   ├── htkk_declaration/
    │       │   ├── htkk_mapping_rule/
    │       │   ├── htkk_indicator_value/
    │       │   ├── htkk_appendix_row/
    │       │   └── htkk_audit_log/
    │       ├── engine/
    │       │   ├── auto_detect.py
    │       │   ├── data_fetcher.py
    │       │   ├── xml_generator.py
    │       │   └── fingerprint.py
    │       └── api.py
    ├── pyproject.toml
    └── setup.py
```

## 11. Development Tools

- **Plugin:** `frappe-claude` (frappe-fullstack) — 7 agents, 12 commands, 5 skills
- **Key commands:** `/frappe-plan`, `/frappe-doctype-create`, `/frappe-fullstack`, `/frappe-test`
- **Branch:** `feature/htkk` (from `develop`)
- **Workflow:** Plugin agents for parallel development (DocType Architect + Backend + Frontend)
