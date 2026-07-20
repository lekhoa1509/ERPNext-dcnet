# HTKK Module — Technical Implementation Guide

> Source: Google Docs (imported 2026-03-13)
> Module: Kê khai thuế tự động trên ERPNext
> Audience: Developer / AI Agent

---

# TECHNICAL IMPLEMENTATION GUIDE — MODULE ERPNEXT HTKK v3.1

Tài liệu kỹ thuật dành cho Coding Agent / Developer

Tài liệu đồng hành với PRD v3.1 — Đọc PRD trước để hiểu nghiệp vụ và UI/UX

| Version | 3.0 |
|---------|-----|
| Ngày | 03/2026 |
| Trạng thái | Draft |
| Mật độ | Internal |

## 1. Cấu trúc thư mục Module

Module nằm trong custom app Frappe tiêu chuẩn tại `custom_app/custom_app/htkk/`. Tuân thủ convention của Frappe với các Doctype riêng và frontend Vue 3 tách biệt.

### 1.1 Cây thư mục tổng quan

```
custom_app/custom_app/htkk/
├── __init__.py
├── hooks.py                    # Frappe hooks cho module
├── api/                         # Whitelist API endpoints
│   ├── __init__.py
│   ├── declaration.py           # API cho Declaration workspace
│   ├── template.py              # API cho Template Manager + Auto-detect
│   ├── mapping_rule.py          # API cho Mapping Rule engine
│   ├── package.py               # API cho Template Package export/import
│   └── xml_generator.py         # XML build + validate
├── doctype/                     # Frappe Doctypes
│   ├── htkk_template_manager/
│   │   ├── htkk_template_manager.py
│   │   ├── htkk_template_manager.json
│   │   └── htkk_template_manager.js
│   ├── htkk_declaration/
│   │   ├── htkk_declaration.py
│   │   ├── htkk_declaration.json
│   │   └── htkk_declaration.js
│   ├── htkk_indicator_value/    # Child Table
│   ├── htkk_appendix_row/       # Doctype riêng cho phụ lục
│   ├── htkk_mapping_rule/       # Mapping Rule engine
│   ├── htkk_audit_log/          # Audit trail
│   └── htkk_template_package/   # Package meta (optional)
├── engine/                      # Core business logic (không phụ thuộc Frappe)
│   ├── __init__.py
│   ├── auto_detect.py           # Regex + heuristic + confidence score
│   ├── data_fetcher.py          # Thực thi Mapping Rules (3 source types)
│   ├── khbs_comparator.py       # So sánh snapshot, tính chênh lệch
│   ├── validate_sync.py         # Incremental Fingerprint
│   ├── xml_builder.py           # lxml XML generation
│   └── xml_validator.py         # xmlschema validation
├── frontend/                    # Vue 3 + Univer frontend
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── pages/
│   │   │   ├── DeclarationWorkspace.vue
│   │   │   ├── AutoDetectReview.vue
│   │   │   ├── MappingRuleManager.vue
│   │   │   └── PackageImport.vue
│   │   ├── components/
│   │   │   ├── DeclarationForm.vue        # HTML/Tailwind từ khai chính
│   │   │   ├── IndicatorSidebar.vue
│   │   │   ├── KHBSModal.vue
│   │   │   ├── DrilldownPopup.vue
│   │   │   ├── ConditionBuilder.vue     # No-code rule editor
│   │   │   ├── SqlEditor.vue            # SQL Builder
│   │   │   └── SaveStatusIndicator.vue
│   │   ├── composables/
│   │   │   ├── useFormState.js            # Form state management
│   │   │   ├── useAutoSave.js           # Dirty-flag + gzip + optimistic lock
│   │   │   └── useRealtimeProgress.js   # WebSocket progress
│   │   └── utils/
│   │       └── frappe-api.js            # frappe.call wrapper
│   ├── package.json
│   └── vite.config.js
├── fixtures/                    # Standard Rules + sample data
│   └── htkk_mapping_rule.json
└── tests/
    ├── test_auto_detect.py
    ├── test_data_fetcher.py
    ├── test_validate_sync.py
    ├── test_xml_builder.py
    └── test_khbs.py
```

### 1.2 Nguyên tắc tổ chức

- `engine/`: Pure Python logic, không import frappe. Dễ unit test.
- `api/`: Frappe whitelist endpoints, gọi engine/ và trả JSON.
- `doctype/`: Frappe ORM + hooks (before_save, on_submit...).
- `frontend/`: Vue 3 SPA, build bằng Vite, mount vào Frappe Page.
- `fixtures/`: Standard Mapping Rules đóng gói sẵn, load bằng bench migrate.

## 2. Doctype Definitions chi tiết

Mỗi Doctype dưới đây cần tạo file .json (schema) và .py (controller). Tham khảo PRD mục 6 cho nghiệp vụ, đây tập trung vào kỹ thuật.

### 2.1 HTKK Template Manager

| Field | Fieldtype | Options/Default | Ghi chú |
|-------|-----------|-----------------|---------|
| template_name | Data | reqd | Tên từ khai |
| target_id | Data | reqd, unique | Mã loại (01/GTGT) |
| circular_version | Data | | TT80/2021 |
| effective_date | Date | reqd | |
| expiry_date | Date | | Null = vô hạn |
| status | Select | Draft/Active/Deprecated | Default: Draft |
| xml_file | Attach | | .xml mẫu |
| xsd_file | Attach | | .xsd schema |
| xlsx_file | Attach | | .xlsx layout |
| xlsx_with_ranges | Attach | | .xlsx đã chốt Named Ranges |
| parsed_nodes | JSON | hidden | Kết quả Parse Schema |
| auto_detect_result | JSON | hidden | Kết quả Auto-detect + confidence |

**Controller hooks quan trọng:**

- `before_save`: Chạy cross-check XSD vs Named Ranges. Block save nếu thiếu.
- `parse_schema()`: Đọc XSD + XML, trả về parsed_nodes JSON.
- `auto_detect_indicators()`: Gọi engine/auto_detect.py, trả về kết quả + confidence.
- `export_package()`: Gom files + rules, tạo .htkktpl.

### 2.2 HTKK Declaration

| Field | Fieldtype | Options/Default | Ghi chú |
|-------|-----------|-----------------|---------|
| company | Link | Company, reqd | |
| template | Link | HTKK Template Manager, reqd | Auto-select theo kỳ |
| tax_period_type | Select | Monthly/Quarterly/Yearly | |
| tax_period_start | Date | reqd | |
| tax_period_end | Date | reqd | |
| declaration_type | Select | Original/Supplement | |
| supplement_number | Int | | 1, 2, 3... (max 5) |
| original_declaration | Link | HTKK Declaration | Chỉ khi Supplement |
| data_fingerprint | JSON | hidden | {invoice_id: signature} |
| state_file | Attach | hidden | Univer state .json.gz |
| state_version | Int | hidden, default 0 | Optimistic locking |
| state_hash | Data | hidden | SHA-256 của state khi Submit |
| workflow_state | Link | Workflow State | Draft/Pending/Submitted/Cancelled |
| indicators | Table | HTKK Indicator Value | Child table chỉ tiêu tổng hợp |

**Controller hooks:**

- `before_submit`: Gọi validate_sync(), kiểm tra KHBS constraints (max 5, 3 năm). Block nếu fail.
- `on_submit`: Lock Univer state, ghi state_hash, sync Child Table + Appendix Row (background).
- `on_cancel`: Kiểm tra đã xuất XML chưa, cảnh báo nếu có.

### 2.3 HTKK Mapping Rule

| Field | Fieldtype | Options/Default | Ghi chú |
|-------|-----------|-----------------|---------|
| declaration_type | Data | reqd | 01/GTGT, 03/TNDN... |
| target_named_range | Data | reqd | CHI_TIEU_29 |
| rule_type | Select | Standard/Custom, reqd | Standard = read-only cho user |
| source_type | Select | condition_builder/sql_builder/python_whitelist | |
| condition_config | JSON | | {doctype, filters[], aggregate} |
| sql_query | Code | SQL | Chỉ SELECT, sanitized |
| whitelist_function | Data | | full.module.path |
| company | Link | Company | Null = global |
| priority | Int | default 10 | Cao hơn = ưu tiên hơn |
| is_active | Check | default 1 | |
| parent_standard | Link | HTKK Mapping Rule | Link đến Standard gốc (nếu Custom) |

### 2.4 HTKK Indicator Value (Child Table)

| Field | Fieldtype | Ghi chú |
|-------|-----------|---------|
| indicator_code | Data | CHI_TIEU_29 |
| indicator_name | Data | Tên chỉ tiêu |
| value | Currency | Giá trị |
| is_manual_edit | Check | 1 nếu đã sửa tay |
| original_value | Currency | Giá trị gốc trước sửa |

### 2.5 HTKK Appendix Row

| Field | Fieldtype | Ghi chú |
|-------|-----------|---------|
| declaration | Link | HTKK Declaration |
| appendix_code | Data | PL01_1_GTGT |
| row_index | Int | |
| data_json | JSON | Toàn bộ cột của dòng |

Insert bằng `frappe.enqueue` + `frappe.publish_realtime` cho progress.

### 2.6 HTKK Audit Log

| Field | Fieldtype | Ghi chú |
|-------|-----------|---------|
| declaration | Link | HTKK Declaration |
| action | Select | fetch_data/save/manual_edit/submit/cancel/export_xml/validate_sync_warning |
| user | Link | User |
| changes_diff | JSON | {cells: [{ref, old, new}]} |
| reason | Small Text | Bắt buộc với manual_edit |
| state_hash | Data | SHA-256 khi save/submit |
| data_fingerprint_snapshot | JSON | Snapshot tại thời điểm action |

## 3. API Contracts

Tất cả API qua `frappe.call` (POST). Response chuẩn: `{message: {status, data, error}}`.

### 3.1 Declaration APIs

| Endpoint | Method | Params | Response |
|----------|--------|--------|----------|
| `htkk.api.declaration.fetch_data` | POST | declaration_name, force_refresh | `{status, indicators: [{code, value, source_rule}], appendix: [{code, rows: [...]}], fingerprint: {inv_id: sig}}` |
| `htkk.api.declaration.save_state` | POST | declaration_name, state_gz (base64), client_version | `{status: saved\|conflict, version, server_state?}` |
| `htkk.api.declaration.validate_sync` | POST | declaration_name | `{status: match\|changed, changed_invoices: [{id, old_modified, new_modified}]}` |
| `htkk.api.declaration.export_xml` | POST | declaration_name | `{status, file_url, xml_hash}` |
| `htkk.api.declaration.validate_xsd` | POST | declaration_name | `{status: valid\|invalid, errors: [{cell, message}]}` |
| `htkk.api.declaration.get_drilldown` | POST | declaration_name, indicator_code | `{invoices: [{name, date, party, amount, tax}]}` |
| `htkk.api.declaration.rollback` | POST | declaration_name, target_version | `{status, restored_version}` |

### 3.2 Template APIs

| Endpoint | Params | Response |
|----------|--------|----------|
| `htkk.api.template.parse_schema` | template_name | `{fixed_nodes: [{code, name, xpath}], repeatable_nodes: [...]}` |
| `htkk.api.template.auto_detect` | template_name | `{indicators: [{code, cell, confidence, anchor_text}], stats: {total, high, medium, low}}` |
| `htkk.api.template.reassign_range` | template_name, code, new_cell | `{status}` |
| `htkk.api.template.save_ranges` | template_name, ranges: [{code, cell}] | `{status, cross_check: {missing: [], extra: []}}` |

### 3.3 Mapping Rule APIs

| Endpoint | Params | Response |
|----------|--------|----------|
| `htkk.api.mapping_rule.test_rule` | rule_name, company, period_start, period_end | `{value, rows_processed, execution_time_ms}` |
| `htkk.api.mapping_rule.resolve_rules` | declaration_type, company | `{rules: [{code, rule_name, rule_type, source_type, value}]}` |
| `htkk.api.mapping_rule.clone_standard` | standard_rule_name, company | `{new_rule_name}` |

### 3.4 Package APIs

| Endpoint | Params | Response |
|----------|--------|----------|
| `htkk.api.package.export` | template_name, include_rules (bool) | `{file_url}` |
| `htkk.api.package.analyze` | file (upload) | `{manifest, compatibility, conflicts: [{rule, status}]}` |
| `htkk.api.package.import_pkg` | file, conflict_resolutions: [{rule, action}] | `{imported, updated, skipped}` |

## 4. Frontend Integration (HTML Form + ag-Grid)

### 4.1 Packages cần cài

```json
// package.json (frontend/)
"dependencies": {
  "ag-grid-community": "^32.x",
  "ag-grid-vue3": "^32.x",
  "tailwindcss": "^3.4.x",
  "@tailwindcss/forms": "^0.5.x",
  "vue": "^3.4.x"
}
```

### 4.2 DeclarationForm.vue — Lifecycle

Component chính quản lý từ khai (HTML form) và phụ lục (ag-Grid):

1. **Mount**: Fetch template config (danh sách chỉ tiêu, layout, formulas) từ Backend.
2. **Render**: Tạo HTML input cho Fixed Nodes, ag-Grid instance cho Repeatable Nodes.
3. **Load state**: Fetch state JSON từ server, fill values vào inputs và ag-Grid rows.
4. **Listen**: `@input` (track changes, toggle CSS class cho color), `@contextmenu` (drill-down).
5. **Computed**: watch inputs, tự động tính các ô formula (`[40] = [29] - [30]`).
6. **Unmount**: Cleanup ag-Grid instances (`gridApi.destroy()`).

### 4.3 Key APIs sử dụng

| Thao tác | API / Cách làm | Dùng khi |
|----------|-----------------|----------|
| Điền giá trị Fixed Node | `document.getElementById(code).value = val` | Fetch data |
| Điền dữ liệu phụ lục | `gridApi.setRowData(rows)` | Fetch data |
| Thêm dòng phụ lục | `gridApi.applyTransaction({add: rows})` | Manual add |
| Tính tổng cột | ag-Grid `pinnedBottomRowData` + `reduce` | Footer row |
| Lock form | `inputs.forEach(i => i.disabled = true)` | Submit lock |
| Color-code ô | `el.classList.toggle('bg-yellow-50')` | Sửa tay |
| Context menu | `@contextmenu.prevent` handler | Drill-down |
| Serialize state | `JSON.stringify({indicators, appendix})` | Auto-save |
| Load state | Parse JSON, fill inputs + `gridApi.setRowData` | Restore |

### 4.4 Mount vào Frappe Page

Tạo Frappe Page (không dùng Frappe Form) để có full control layout:

```javascript
// custom_app/custom_app/htkk/page/declaration_workspace/
// declaration_workspace.json  →  Frappe Page definition
// declaration_workspace.js    →  Mount Vue app

frappe.pages['declaration-workspace'].on_page_load = function(wrapper) {
  const app = createApp(DeclarationWorkspace);
  app.mount(wrapper.querySelector('.layout-main'));
};
```

## 5. Engine Implementation

### 5.1 auto_detect.py

Input: File `.xlsx` path. Output: `List[IndicatorMatch]`.

```python
class IndicatorMatch:
    code: str           # [29]
    cell: str           # D15
    confidence: float   # 0.0 - 1.0
    anchor_text: str    # 'Chỉ tiêu [29]'
    anchor_cell: str    # C15 (backup)

def auto_detect(xlsx_path, xsd_nodes) -> List[IndicatorMatch]:
    wb = openpyxl.load_workbook(xlsx_path)
    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                matches = regex_scan(cell.value)
                if matches:
                    target = find_input_cell(sheet, cell, offset_config)
                    conf = calculate_confidence(cell, target, sheet_structure)
                    results.append(IndicatorMatch(...))
    return cross_check_with_xsd(results, xsd_nodes)
```

### 5.2 data_fetcher.py

Thực thi Mapping Rules theo thứ tự ưu tiên:

```python
def fetch_indicator(declaration_type, named_range, company, period):
    # 1. Tìm Custom Rule (company-specific)
    # 2. Tìm Custom Rule (global)
    # 3. Tìm Standard Rule
    # 4. Không có rule → return None (highlight vàng)
    rule = resolve_rule(declaration_type, named_range, company)
    if not rule: return None

    if rule.source_type == 'condition_builder':
        return execute_condition(rule.condition_config, period)
    elif rule.source_type == 'sql_builder':
        return execute_safe_sql(rule.sql_query, period)  # sanitized
    elif rule.source_type == 'python_whitelist':
        fn = get_whitelisted_function(rule.whitelist_function)
        return fn(company=company, from_date=period[0], to_date=period[1])
```

### 5.3 validate_sync.py

```python
def generate_fingerprint(declaration) -> dict:
    """Tính signature cho từng chứng từ"""
    invoices = get_source_invoices(declaration)
    return {
        inv.name: hashlib.sha256(
            f'{inv.name}:{inv.grand_total}:{inv.modified}'.encode()
        ).hexdigest()[:16]
        for inv in invoices
    }

def compare_fingerprints(old_fp, new_fp) -> list:
    changed = []
    for inv_id, old_sig in old_fp.items():
        new_sig = new_fp.get(inv_id)
        if old_sig != new_sig:
            changed.append({'invoice': inv_id, ...})
    # Cũng kiểm tra inv mới thêm / đã xóa
    return changed
```

### 5.4 xml_builder.py

```python
from lxml import etree

def build_xml(declaration, univer_state) -> bytes:
    template = get_template(declaration)
    root = parse_xml_template(template.xml_file)

    # Fill Fixed Nodes
    for node in template.parsed_nodes['fixed']:
        value = extract_from_univer(univer_state, node['named_range'])
        set_xml_value(root, node['xpath'], value)

    # Fill Repeatable Nodes
    for appendix in template.parsed_nodes['repeatable']:
        rows = extract_appendix_rows(univer_state, appendix['range'])
        insert_repeating_xml(root, appendix['xpath'], rows)

    # Validate against XSD
    schema = xmlschema.XMLSchema(template.xsd_file)
    schema.validate(root)  # Raises on error

    return etree.tostring(root, xml_declaration=True, encoding='utf-8')
```

## 6. Thứ tự Implement (cho Coding Agent)

Coding agent nên thực hiện theo đúng thứ tự này vì có phụ thuộc giữa các module.

### Phase 0: Spike (2 tuần)

1. Tạo Frappe app skeleton: `bench new-app custom_app`.
2. Tạo thư mục `htkk/` với cấu trúc như mục 1.
3. Scaffold `frontend/`: npm init, cài Univer packages.
4. Tạo `UniverSheet.vue`: Mount Univer, load file .xlsx mẫu từ HTKK.
5. Tạo Frappe Page, mount Vue app, verify Univer render đúng.
6. Tạo `engine/auto_detect.py`: Chạy trên 3 file .xlsx thực, đo accuracy.

**Gate:** Univer render OK + Auto-detect > 85% → tiếp. Nếu không → pivot.

### Phase 1: MVP (6 tuần)

**Tuần 1–2: Doctypes + Engine core**

1. Tạo Doctype: HTKK Template Manager, HTKK Declaration, HTKK Indicator Value.
2. Tạo Doctype: HTKK Mapping Rule (Condition Builder only).
3. `engine/data_fetcher.py`: Condition Builder executor.
4. `api/template.py`: parse_schema, auto_detect, save_ranges.

**Tuần 3–4: Frontend core**

1. `DeclarationWorkspace.vue`: Layout 6 vùng (PRD 8.2).
2. `useUniver.js`: Load xlsx, fill data từ API, color-code ô.
3. `useAutoSave.js`: Dirty-flag, gzip, save_state API, optimistic lock.
4. `AutoDetectReview.vue`: Sidebar + confidence + batch review.

**Tuần 5–6: XML + Integration**

1. `engine/xml_builder.py` + `xml_validator.py`.
2. `api/declaration.py`: fetch_data, save_state, validate_xsd, export_xml.
3. End-to-end: Tạo Template → Auto-detect → Tạo Declaration → Fetch → Submit → XML.
4. Unit tests cho `engine/`.

**Gate:** Xuất XML đúng cho 1 mẫu GTGT với dữ liệu thực.

### Phase 2: Hardening (4 tuần)

1. KHBS: `khbs_comparator.py` + `KHBSModal.vue` + constraints (max 5, 3 năm).
2. `validate_sync.py` + Incremental Fingerprint + Warning bar UI.
3. HTKK Audit Log doctype + event logging.
4. HTKK Appendix Row + background insert + realtime progress.
5. Mapping Rule: SQL Builder + Python Whitelist source types.
6. `MappingRuleManager.vue` + `ConditionBuilder.vue` + `SqlEditor.vue`.
7. Workflow (Frappe Workflow): Draft → Pending → Submitted → Cancelled.
8. `DrilldownPopup.vue` + Compare mode.

### Phase 3: Scale (4 tuần)

1. Template Package: export/import `.htkktpl` + `PackageImport.vue` (wizard 4 bước).
2. Base + Override: Standard/Custom rule logic + UI (8.9D).
3. Multi-template: Thêm 2+ mẫu (TNDN, TNCN).
4. Multi-company: Company filter trên Mapping Rule.
5. Fixtures: Đóng gói Standard Rules cho TT200/133.

### Phase 4: Polish (4 tuần)

1. Rollback (snapshot versions) + Data Reconciliation (XML import).
2. Alerting deadline nộp thuế.
3. Performance tuning: Benchmark các mục tiêu PRD 13.1.
4. Parallel Validation: So XML với HTKK gốc.
5. UAT với dữ liệu thực, training.

## 7. Conventions và Lưu ý cho Coding Agent

### 7.1 Python

- **Frappe whitelist**: `@frappe.whitelist()` cho API endpoints.
- **HTKK whitelist**: Tạo decorator `@whitelist_for_htkk` để đánh dấu hàm an toàn cho Mapping Rule.
- **Background job**: `frappe.enqueue('func', queue='long')` cho insert lớn.
- **Realtime**: `frappe.publish_realtime('htkk_progress', {percent, message}, doctype, docname)`.
- **SQL safety**: Dùng `frappe.db.sql` với parameterized queries. SQL Builder phải qua `sanitize_sql()`.
- **File attach**: `frappe.get_doc('File', ...)` để quản lý `.json.gz` state files. Xóa bản cũ khi save mới.

### 7.2 Vue 3 / Frontend

- **Frappe API**: `frappe.call({method, args, callback})` hoặc `fetch('/api/method/...')`.
- **Realtime**: `frappe.realtime.on('htkk_progress', handler)`.
- **Routing**: Dùng Frappe Page routing, không Vue Router (vì embed trong Frappe).
- **State**: Vue reactive (`ref`/`reactive`), không cần Vuex/Pinia cho scope module này.
- **Build**: Vite build output vào `custom_app/public/js/htkk.bundle.js`. Frappe load qua `hooks.py`.

### 7.3 ag-Grid + Tailwind

- **ag-Grid**: Dùng `ag-grid-community` (MIT). Import `AgGridVue` từ `ag-grid-vue3`.
- **Column Defs**: Định nghĩa từ `parsed_nodes` của Template (Repeatable Nodes).
- **Tailwind**: Dùng `@tailwindcss/forms` cho input styling. Prefix `htkk-` cho custom classes.
- **Layout**: Form từ khai dùng `grid-cols-12` Tailwind, mapping từ template config.
- **Color-code**: Toggle CSS classes (`bg-blue-50`, `bg-yellow-50`...) không inline style.

### 7.4 Testing

- **Unit test** `engine/`: pytest, mock `frappe.db` khi cần.
- **Integration test**: `frappe.tests.utils.FrappeTestCase`.
- **Auto-detect accuracy**: Test trên 5+ file .xlsx thực, assert precision > 85%.
- **XML validation**: So output với expected XML (ignore whitespace).

### 7.5 hooks.py

```python
# custom_app/custom_app/htkk/hooks.py

app_include_js = ['/assets/custom_app/js/htkk.bundle.js']
app_include_css = ['/assets/custom_app/css/htkk.css']

fixtures = [
    {"dt": "HTKK Mapping Rule", "filters": {"rule_type": "Standard"}}
]

# Scheduler for deadline alerts
scheduler_events = {
    "daily": ["custom_app.custom_app.htkk.api.declaration.check_deadlines"]
}
```

---

*— Het tai lieu —*
