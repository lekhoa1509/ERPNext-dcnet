# HTKK — Kê khai thuế tự động trên ERPNext

> **Status:** Pre-development (Structure & Docs setup)
> **Branch:** `feature/htkk`
> **App:** `dcnet_htkk` (Frappe app riêng)
> **Plugin:** `frappe-claude` (frappe-fullstack)

## Tài liệu

| File | Mô tả |
|------|-------|
| `HTKK_PRD.md` | Product Requirements Document v3.1 |
| `HTKK_TECHNICAL_GUIDE.md` | Technical Implementation Guide cho Developer/Agent |
| `htkk_wireframes.jsx` | React wireframe (10 screens) |
| `HTKK_DESIGN.md` | Design document (architecture, workflow, state machine) |

## Tổng quan

Module tự động hóa kê khai thuế VN trên ERPNext — loại bỏ nhập liệu thủ công giữa ERPNext và phần mềm HTKK của Tổng cục Thuế.

### 6 DocTypes

1. **HTKK Template Manager** — Quản lý mẫu tờ khai (XSD/XML/XLSX)
2. **HTKK Declaration** — Workspace làm việc chính (spreadsheet-like)
3. **HTKK Mapping Rule** — Quy tắc ánh xạ dữ liệu (Condition Builder / SQL / Python)
4. **HTKK Indicator Value** — Child table cho chỉ tiêu tổng hợp
5. **HTKK Appendix Row** — Dữ liệu phụ lục chi tiết
6. **HTKK Audit Log** — Theo dõi thay đổi SHA-256

### Tech Stack

- **Frontend:** Vue 3 SPA + ag-Grid Community
- **Backend:** Frappe Framework (Python), lxml, openpyxl
- **Storage:** gzip JSON File Attachment + Child Tables

### Roadmap

| Phase | Scope | Duration |
|-------|-------|----------|
| 0 | Spike — validate feasibility | 2 weeks |
| 1 | MVP — DocTypes + Core engine | 6 weeks |
| 2 | Hardening — KHBS, validation | 4 weeks |
| 3 | Scale — multi-template | 4 weeks |
| 4 | Polish — rollback, performance | 4 weeks |

---

## Checklist Tracking

### Phase 0: Setup & Preparation
- [x] Tạo branch `feature/htkk`
- [x] Tạo folder `docs/feature/htkk/` + lưu tài liệu gốc (PRD, Tech Guide, Wireframes)
- [x] Tạo Design doc (architecture, workflow, state machine)
- [x] Tạo `dcnet_htkk/` app skeleton (hooks.py, modules.txt, pyproject.toml, setup.py)
- [x] Tạo 6 doctype folders + engine folder
- [x] Push lên `origin/feature/htkk`
- [ ] Install plugin `frappe-claude` (frappe-fullstack)
- [ ] Tạo implementation plan chi tiết (Phase 0 Spike)

### Phase 0: Spike — Validate Feasibility (2 weeks)
- [ ] **DocType: HTKK Template Manager** — schema + fields + controller
- [ ] **DocType: HTKK Declaration** — schema + fields + workflow setup
- [ ] **DocType: HTKK Mapping Rule** — schema + fields + 3 source types
- [ ] **DocType: HTKK Indicator Value** — child table schema
- [ ] **DocType: HTKK Appendix Row** — child table schema
- [ ] **DocType: HTKK Audit Log** — schema + SHA-256 hashing
- [ ] **Engine: auto_detect.py** — regex + heuristic scan XLSX
- [ ] **Engine: data_fetcher.py** — fetch data từ Mapping Rules
- [ ] **Engine: xml_generator.py** — lxml build + xmlschema validate
- [ ] **Engine: fingerprint.py** — SHA-256 fingerprint cho source docs
- [ ] **API: api.py** — @frappe.whitelist endpoints
- [ ] **Test:** 1 mẫu GTGT 01/GTGT end-to-end (fetch → review → export XML)

### Phase 1: MVP — Core Engine (6 weeks)
- [ ] Spreadsheet UI (Vue 3 + ag-Grid)
- [ ] Condition Builder UI (no-code mapping)
- [ ] SQL Builder UI (low-code mapping)
- [ ] Python Whitelist integration
- [ ] Declaration workflow (Draft → Pending → Submitted)
- [ ] validate_sync() — fingerprint comparison
- [ ] XML export + XSD validation
- [ ] Drilldown popup (source invoices)
- [ ] Unit tests + integration tests

### Phase 2: Hardening — KHBS & Validation (4 weeks)
- [ ] KHBS flow (khai bổ sung, max 5 lần/kỳ)
- [ ] KHBS Modal UI (diff + reason + late fee)
- [ ] Optimistic locking (concurrent edit)
- [ ] Audit Log chain validation
- [ ] Error handling + edge cases
- [ ] Performance optimization (background jobs >5000 rows)

### Phase 3: Scale — Multi-template (4 weeks)
- [ ] Template Package Import wizard (.htkktpl)
- [ ] Conflict resolution (Standard vs Custom rules)
- [ ] Multiple tax form types (TNDN, TNCN, etc.)
- [ ] Template versioning
- [ ] Auto-detect confidence tuning

### Phase 4: Polish — Rollback & Performance (4 weeks)
- [ ] Rollback to previous version
- [ ] Render time < 3s optimization
- [ ] Manual correction rate < 5% validation
- [ ] User guide (Vietnamese)
- [ ] Final QA + security audit
