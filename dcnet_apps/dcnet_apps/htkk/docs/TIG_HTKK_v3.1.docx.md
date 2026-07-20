

**TECHNICAL IMPLEMENTATION GUIDE**

**MODULE ERPNEXT HTKK v3.1**

*Tài liệu kỹ thuật dành cho Coding Agent / Developer*

Tài liệu đồng hành với PRD v3.1 — Đọc PRD trước để hiểu nghiệp vụ và UI/UX

| Version | 3.0 |
| :---- | :---- |
| **Ngày** | 03/2026 |
| **Trạng thái** | Draft |
| **Mật độ** | Internal |

# **1\. Cấu trúc thư mục Module**

Module nằm trong custom app Frappe tiêu chuẩn tại custom\_app/custom\_app/htkk/. Tuân thủ convention của Frappe với các Doctype riêng và frontend Vue 3 tách biệt.

### **1.1 Cây thư mục tổng quan**

custom\_app/custom\_app/htkk/├── \_\_init\_\_.py├── hooks.py                    \# Frappe hooks cho module├── api/                         \# Whitelist API endpoints│   ├── \_\_init\_\_.py│   ├── declaration.py           \# API cho Declaration workspace│   ├── template.py              \# API cho Template Manager \+ Auto-detect│   ├── mapping\_rule.py          \# API cho Mapping Rule engine│   ├── package.py               \# API cho Template Package export/import│   └── xml\_generator.py         \# XML build \+ validate├── doctype/                     \# Frappe Doctypes│   ├── htkk\_template\_manager/│   │   ├── htkk\_template\_manager.py│   │   ├── htkk\_template\_manager.json│   │   └── htkk\_template\_manager.js│   ├── htkk\_declaration/│   │   ├── htkk\_declaration.py│   │   ├── htkk\_declaration.json│   │   └── htkk\_declaration.js│   ├── htkk\_indicator\_value/    \# Child Table│   ├── htkk\_appendix\_row/       \# Doctype riêng cho phụ lục│   ├── htkk\_mapping\_rule/       \# Mapping Rule engine│   ├── htkk\_audit\_log/          \# Audit trail│   └── htkk\_template\_package/   \# Package meta (optional)├── engine/                      \# Core business logic (không phụ thuộc Frappe)│   ├── \_\_init\_\_.py│   ├── auto\_detect.py           \# Regex \+ heuristic \+ confidence score│   ├── data\_fetcher.py          \# Thực thi Mapping Rules (3 source types)│   ├── khbs\_comparator.py       \# So sánh snapshot, tính chênh lệch│   ├── validate\_sync.py         \# Incremental Fingerprint│   ├── xml\_builder.py           \# lxml XML generation│   └── xml\_validator.py         \# xmlschema validation├── frontend/                    \# Vue 3 \+ Univer frontend│   ├── src/│   │   ├── main.js│   │   ├── App.vue│   │   ├── pages/│   │   │   ├── DeclarationWorkspace.vue│   │   │   ├── AutoDetectReview.vue│   │   │   ├── MappingRuleManager.vue│   │   │   └── PackageImport.vue│   │   ├── components/│   │   │   ├── DeclarationForm.vue        \# HTML/Tailwind từ khai chính│   │   │   ├── IndicatorSidebar.vue│   │   │   ├── KHBSModal.vue│   │   │   ├── DrilldownPopup.vue│   │   │   ├── ConditionBuilder.vue     \# No-code rule editor│   │   │   ├── SqlEditor.vue            \# SQL Builder│   │   │   └── SaveStatusIndicator.vue│   │   ├── composables/│   │   │   ├── useFormState.js            \# Form state management│   │   │   ├── useAutoSave.js           \# Dirty-flag \+ gzip \+ optimistic lock│   │   │   └── useRealtimeProgress.js   \# WebSocket progress│   │   └── utils/│   │       └── frappe-api.js            \# frappe.call wrapper│   ├── package.json│   └── vite.config.js├── fixtures/                    \# Standard Rules \+ sample data│   └── htkk\_mapping\_rule.json└── tests/    ├── test\_auto\_detect.py    ├── test\_data\_fetcher.py    ├── test\_validate\_sync.py    ├── test\_xml\_builder.py    └── test\_khbs.py

### **1.2 Nguyên tắc tổ chức**

* engine/: Pure Python logic, không import frappe. Dễ unit test.

* api/: Frappe whitelist endpoints, gọi engine/ và trả JSON.

* doctype/: Frappe ORM \+ hooks (before\_save, on\_submit...).

* frontend/: Vue 3 SPA, build bằng Vite, mount vào Frappe Page.

* fixtures/: Standard Mapping Rules đóng gói sẵn, load bằng bench migrate.

# **2\. Doctype Definitions chi tiết**

Mỗi Doctype dưới đây cần tạo file .json (schema) và .py (controller). Tham khảo PRD mục 6 cho nghiệp vụ, đây tập trung vào kỹ thuật.

## **2.1 HTKK Template Manager**

| Field | Fieldtype | Options/Default | Ghi chú |
| ----- | ----- | ----- | ----- |
| template\_name | Data | reqd | Tên từ khai |
| target\_id | Data | reqd, unique | Mã loại (01/GTGT) |
| circular\_version | Data |  | TT80/2021 |
| effective\_date | Date | reqd |  |
| expiry\_date | Date |  | Null \= vô hạn |
| status | Select | Draft/Active/Deprecated | Default: Draft |
| xml\_file | Attach |  | .xml mẫu |
| xsd\_file | Attach |  | .xsd schema |
| xlsx\_file | Attach |  | .xlsx layout |
| xlsx\_with\_ranges | Attach |  | .xlsx đã chốt Named Ranges |
| parsed\_nodes | JSON | hidden | Kết quả Parse Schema |
| auto\_detect\_result | JSON | hidden | Kết quả Auto-detect \+ confidence |

Controller hooks quan trọng:

* before\_save: Chạy cross-check XSD vs Named Ranges. Block save nếu thiếu.

* parse\_schema(): Đọc XSD \+ XML, trả về parsed\_nodes JSON.

* auto\_detect\_indicators(): Gọi engine/auto\_detect.py, trả về kết quả \+ confidence.

* export\_package(): Gom files \+ rules, tạo .htkktpl.

## **2.2 HTKK Declaration**

| Field | Fieldtype | Options/Default | Ghi chú |
| ----- | ----- | ----- | ----- |
| company | Link | Company, reqd |  |
| template | Link | HTKK Template Manager, reqd | Auto-select theo kỳ |
| tax\_period\_type | Select | Monthly/Quarterly/Yearly |  |
| tax\_period\_start | Date | reqd |  |
| tax\_period\_end | Date | reqd |  |
| declaration\_type | Select | Original/Supplement |  |
| supplement\_number | Int |  | 1, 2, 3... (max 5\) |
| original\_declaration | Link | HTKK Declaration | Chỉ khi Supplement |
| data\_fingerprint | JSON | hidden | {invoice\_id: signature} |
| state\_file | Attach | hidden | Univer state .json.gz |
| state\_version | Int | hidden, default 0 | Optimistic locking |
| state\_hash | Data | hidden | SHA-256 của state khi Submit |
| workflow\_state | Link | Workflow State | Draft/Pending/Submitted/Cancelled |
| indicators | Table | HTKK Indicator Value | Child table chỉ tiêu tổng hợp |

Controller hooks:

* before\_submit: Gọi validate\_sync(), kiểm tra KHBS constraints (max 5, 3 năm). Block nếu fail.

* on\_submit: Lock Univer state, ghi state\_hash, sync Child Table \+ Appendix Row (background).

* on\_cancel: Kiểm tra đã xuất XML chưa, cảnh báo nếu có.

## **2.3 HTKK Mapping Rule**

| Field | Fieldtype | Options/Default | Ghi chú |
| ----- | ----- | ----- | ----- |
| declaration\_type | Data | reqd | 01/GTGT, 03/TNDN... |
| target\_named\_range | Data | reqd | CHI\_TIEU\_29 |
| rule\_type | Select | Standard/Custom, reqd | Standard \= read-only cho user |
| source\_type | Select | condition\_builder/sql\_builder/python\_whitelist |  |
| condition\_config | JSON |  | {doctype, filters\[\], aggregate} |
| sql\_query | Code | SQL | Chỉ SELECT, sanitized |
| whitelist\_function | Data |  | full.module.path |
| company | Link | Company | Null \= global |
| priority | Int | default 10 | Cao hơn \= ưu tiên hơn |
| is\_active | Check | default 1 |  |
| parent\_standard | Link | HTKK Mapping Rule | Link đến Standard gốc (nếu Custom) |

## **2.4 HTKK Indicator Value (Child Table)**

| Field | Fieldtype | Ghi chú |
| ----- | ----- | ----- |
| indicator\_code | Data | CHI\_TIEU\_29 |
| indicator\_name | Data | Tên chỉ tiêu |
| value | Currency | Giá trị |
| is\_manual\_edit | Check | 1 nếu đã sửa tay |
| original\_value | Currency | Giá trị gốc trước sửa |

## **2.5 HTKK Appendix Row**

| Field | Fieldtype | Ghi chú |
| ----- | ----- | ----- |
| declaration | Link | HTKK Declaration |
| appendix\_code | Data | PL01\_1\_GTGT |
| row\_index | Int |  |
| data\_json | JSON | Toàn bộ cột của dòng |

Insert bằng frappe.enqueue \+ frappe.publish\_realtime cho progress.

## **2.6 HTKK Audit Log**

| Field | Fieldtype | Ghi chú |
| ----- | ----- | ----- |
| declaration | Link | HTKK Declaration |
| action | Select | fetch\_data/save/manual\_edit/submit/cancel/export\_xml/validate\_sync\_warning |
| user | Link | User |
| changes\_diff | JSON | {cells: \[{ref, old, new}\]} |
| reason | Small Text | Bắt buộc với manual\_edit |
| state\_hash | Data | SHA-256 khi save/submit |
| data\_fingerprint\_snapshot | JSON | Snapshot tại thời điểm action |

# **3\. API Contracts**

Tất cả API qua frappe.call (POST). Response chuẩn: {message: {status, data, error}}.

## **3.1 Declaration APIs**

| Endpoint | Method | Params | Response |
| ----- | ----- | ----- | ----- |
| htkk.api.declaration.fetch\_data | POST | declaration\_name, force\_refresh | {status, indicators: \[{code, value, source\_rule}\], appendix: \[{code, rows: \[...\]}\], fingerprint: {inv\_id: sig}} |
| htkk.api.declaration.save\_state | POST | declaration\_name, state\_gz (base64), client\_version | {status: saved|conflict, version, server\_state?} |
| htkk.api.declaration.validate\_sync | POST | declaration\_name | {status: match|changed, changed\_invoices: \[{id, old\_modified, new\_modified}\]} |
| htkk.api.declaration.export\_xml | POST | declaration\_name | {status, file\_url, xml\_hash} |
| htkk.api.declaration.validate\_xsd | POST | declaration\_name | {status: valid|invalid, errors: \[{cell, message}\]} |
| htkk.api.declaration.get\_drilldown | POST | declaration\_name, indicator\_code | {invoices: \[{name, date, party, amount, tax}\]} |
| htkk.api.declaration.rollback | POST | declaration\_name, target\_version | {status, restored\_version} |

## **3.2 Template APIs**

| Endpoint | Params | Response |
| ----- | ----- | ----- |
| htkk.api.template.parse\_schema | template\_name | {fixed\_nodes: \[{code, name, xpath}\], repeatable\_nodes: \[...\]} |
| htkk.api.template.auto\_detect | template\_name | {indicators: \[{code, cell, confidence, anchor\_text}\], stats: {total, high, medium, low}} |
| htkk.api.template.reassign\_range | template\_name, code, new\_cell | {status} |
| htkk.api.template.save\_ranges | template\_name, ranges: \[{code, cell}\] | {status, cross\_check: {missing: \[\], extra: \[\]}} |

## **3.3 Mapping Rule APIs**

| Endpoint | Params | Response |
| ----- | ----- | ----- |
| htkk.api.mapping\_rule.test\_rule | rule\_name, company, period\_start, period\_end | {value, rows\_processed, execution\_time\_ms} |
| htkk.api.mapping\_rule.resolve\_rules | declaration\_type, company | {rules: \[{code, rule\_name, rule\_type, source\_type, value}\]} |
| htkk.api.mapping\_rule.clone\_standard | standard\_rule\_name, company | {new\_rule\_name} |

## **3.4 Package APIs**

| Endpoint | Params | Response |
| ----- | ----- | ----- |
| htkk.api.package.export | template\_name, include\_rules (bool) | {file\_url} |
| htkk.api.package.analyze | file (upload) | {manifest, compatibility, conflicts: \[{rule, status}\]} |
| htkk.api.package.import\_pkg | file, conflict\_resolutions: \[{rule, action}\] | {imported, updated, skipped} |

# **4\. Frontend Integration (HTML Form \+ ag-Grid)**

### **4.1 Packages cần cài**

// package.json (frontend/)"dependencies": {  "ag-grid-community": "^32.x",  "ag-grid-vue3": "^32.x",  "tailwindcss": "^3.4.x",  "@tailwindcss/forms": "^0.5.x",  "vue": "^3.4.x"}

### **4.2 DeclarationForm.vue — Lifecycle**

Component chính quản lý từ khai (HTML form) và phụ lục (ag-Grid):

1. Mount: Fetch template config (danh sách chỉ tiêu, layout, formulas) từ Backend.

2. Render: Tạo HTML input cho Fixed Nodes, ag-Grid instance cho Repeatable Nodes.

3. Load state: Fetch state JSON từ server, fill values vào inputs và ag-Grid rows.

4. Listen: @input (track changes, toggle CSS class cho color), @contextmenu (drill-down).

5. Computed: watch inputs, tự động tính các ô formula (\[40\] \= \[29\] \- \[30\]).

6. Unmount: Cleanup ag-Grid instances (gridApi.destroy()).

### **4.3 Key APIs sử dụng**

| Thao tác | API / Cách làm | Dùng khi |
| ----- | ----- | ----- |
| Điền giá trị Fixed Node | document.getElementById(code).value \= val | Fetch data |
| Điền dữ liệu phụ lục | gridApi.setRowData(rows) | Fetch data |
| Thêm dòng phụ lục | gridApi.applyTransaction({add: rows}) | Manual add |
| Tính tổng cột | ag-Grid pinnedBottomRowData \+ reduce | Footer row |
| Lock form | inputs.forEach(i \=\> i.disabled \= true) | Submit lock |
| Color-code ô | el.classList.toggle('bg-yellow-50') | Sửa tay |
| Context menu | @contextmenu.prevent handler | Drill-down |
| Serialize state | JSON.stringify({indicators, appendix}) | Auto-save |
| Load state | Parse JSON, fill inputs \+ gridApi.setRowData | Restore |

### **4.4 Mount vào Frappe Page**

Tạo Frappe Page (không dùng Frappe Form) để có full control layout:

// custom\_app/custom\_app/htkk/page/declaration\_workspace/// declaration\_workspace.json  →  Frappe Page definition// declaration\_workspace.js    →  Mount Vue appfrappe.pages\['declaration-workspace'\].on\_page\_load \= function(wrapper) {  const app \= createApp(DeclarationWorkspace);  app.mount(wrapper.querySelector('.layout-main'));};

# **5\. Engine Implementation**

## **5.1 auto\_detect.py**

Input: File .xlsx path. Output: List\[IndicatorMatch\].

class IndicatorMatch:    code: str           \# \[29\]    cell: str           \# D15    confidence: float   \# 0.0 \- 1.0    anchor\_text: str    \# 'Chỉ tiêu \[29\]'    anchor\_cell: str    \# C15 (backup)def auto\_detect(xlsx\_path, xsd\_nodes) \-\> List\[IndicatorMatch\]:    wb \= openpyxl.load\_workbook(xlsx\_path)    for sheet in wb.worksheets:        for row in sheet.iter\_rows():            for cell in row:                matches \= regex\_scan(cell.value)                if matches:                    target \= find\_input\_cell(sheet, cell, offset\_config)                    conf \= calculate\_confidence(cell, target, sheet\_structure)                    results.append(IndicatorMatch(...))    return cross\_check\_with\_xsd(results, xsd\_nodes)

## **5.2 data\_fetcher.py**

Thực thi Mapping Rules theo thứ tự ưu tiên:

def fetch\_indicator(declaration\_type, named\_range, company, period):    \# 1\. Tìm Custom Rule (company-specific)    \# 2\. Tìm Custom Rule (global)    \# 3\. Tìm Standard Rule    \# 4\. Không có rule → return None (highlight vàng)    rule \= resolve\_rule(declaration\_type, named\_range, company)    if not rule: return None    if rule.source\_type \== 'condition\_builder':        return execute\_condition(rule.condition\_config, period)    elif rule.source\_type \== 'sql\_builder':        return execute\_safe\_sql(rule.sql\_query, period)  \# sanitized    elif rule.source\_type \== 'python\_whitelist':        fn \= get\_whitelisted\_function(rule.whitelist\_function)        return fn(company=company, from\_date=period\[0\], to\_date=period\[1\])

## **5.3 validate\_sync.py**

def generate\_fingerprint(declaration) \-\> dict:    """Tính signature cho từng chứng từ"""    invoices \= get\_source\_invoices(declaration)    return {        inv.name: hashlib.sha256(            f'{inv.name}:{inv.grand\_total}:{inv.modified}'.encode()        ).hexdigest()\[:16\]        for inv in invoices    }def compare\_fingerprints(old\_fp, new\_fp) \-\> list:    changed \= \[\]    for inv\_id, old\_sig in old\_fp.items():        new\_sig \= new\_fp.get(inv\_id)        if old\_sig \!= new\_sig:            changed.append({'invoice': inv\_id, ...})    \# Cũng kiểm tra inv mới thêm / đã xóa    return changed

## **5.4 xml\_builder.py**

from lxml import etreedef build\_xml(declaration, univer\_state) \-\> bytes:    template \= get\_template(declaration)    root \= parse\_xml\_template(template.xml\_file)        \# Fill Fixed Nodes    for node in template.parsed\_nodes\['fixed'\]:        value \= extract\_from\_univer(univer\_state, node\['named\_range'\])        set\_xml\_value(root, node\['xpath'\], value)        \# Fill Repeatable Nodes    for appendix in template.parsed\_nodes\['repeatable'\]:        rows \= extract\_appendix\_rows(univer\_state, appendix\['range'\])        insert\_repeating\_xml(root, appendix\['xpath'\], rows)        \# Validate against XSD    schema \= xmlschema.XMLSchema(template.xsd\_file)    schema.validate(root)  \# Raises on error        return etree.tostring(root, xml\_declaration=True, encoding='utf-8')

# **6\. Thứ tự Implement (cho Coding Agent)**

Coding agent nên thực hiện theo đúng thứ tự này vì có phụ thuộc giữa các module.

## **Phase 0: Spike (2 tuần)**

1. Tạo Frappe app skeleton: bench new-app custom\_app.

2. Tạo thư mục htkk/ với cấu trúc như mục 1\.

3. Scaffold frontend/: npm init, cài Univer packages.

4. Tạo UniverSheet.vue: Mount Univer, load file .xlsx mẫu từ HTKK.

5. Tạo Frappe Page, mount Vue app, verify Univer render đúng.

6. Tạo engine/auto\_detect.py: Chạy trên 3 file .xlsx thực, đo accuracy.

Gate: Univer render OK \+ Auto-detect \> 85% → tiếp. Nếu không → pivot.

## **Phase 1: MVP (6 tuần)**

Tuần 1–2: Doctypes \+ Engine core

1. Tạo Doctype: HTKK Template Manager, HTKK Declaration, HTKK Indicator Value.

2. Tạo Doctype: HTKK Mapping Rule (Condition Builder only).

3. engine/data\_fetcher.py: Condition Builder executor.

4. api/template.py: parse\_schema, auto\_detect, save\_ranges.

Tuần 3–4: Frontend core

1. DeclarationWorkspace.vue: Layout 6 vùng (PRD 8.2).

2. useUniver.js: Load xlsx, fill data từ API, color-code ô.

3. useAutoSave.js: Dirty-flag, gzip, save\_state API, optimistic lock.

4. AutoDetectReview.vue: Sidebar \+ confidence \+ batch review.

Tuần 5–6: XML \+ Integration

1. engine/xml\_builder.py \+ xml\_validator.py.

2. api/declaration.py: fetch\_data, save\_state, validate\_xsd, export\_xml.

3. End-to-end: Tạo Template → Auto-detect → Tạo Declaration → Fetch → Submit → XML.

4. Unit tests cho engine/.

Gate: Xuất XML đúng cho 1 mẫu GTGT với dữ liệu thực.

## **Phase 2: Hardening (4 tuần)**

1. KHBS: khbs\_comparator.py \+ KHBSModal.vue \+ constraints (max 5, 3 năm).

2. validate\_sync.py \+ Incremental Fingerprint \+ Warning bar UI.

3. HTKK Audit Log doctype \+ event logging.

4. HTKK Appendix Row \+ background insert \+ realtime progress.

5. Mapping Rule: SQL Builder \+ Python Whitelist source types.

6. MappingRuleManager.vue \+ ConditionBuilder.vue \+ SqlEditor.vue.

7. Workflow (Frappe Workflow): Draft → Pending → Submitted → Cancelled.

8. DrilldownPopup.vue \+ Compare mode.

## **Phase 3: Scale (4 tuần)**

1. Template Package: export/import .htkktpl \+ PackageImport.vue (wizard 4 bước).

2. Base \+ Override: Standard/Custom rule logic \+ UI (8.9D).

3. Multi-template: Thêm 2+ mẫu (TNDN, TNCN).

4. Multi-company: Company filter trên Mapping Rule.

5. Fixtures: Đóng gói Standard Rules cho TT200/133.

## **Phase 4: Polish (4 tuần)**

1. Rollback (snapshot versions) \+ Data Reconciliation (XML import).

2. Alerting deadline nộp thuế.

3. Performance tuning: Benchmark các mục tiêu PRD 13.1.

4. Parallel Validation: So XML với HTKK gốc.

5. UAT với dữ liệu thực, training.

# **7\. Conventions và Lưu ý cho Coding Agent**

### **7.1 Python**

* Frappe whitelist: @frappe.whitelist() cho API endpoints.

* HTKK whitelist: Tạo decorator @whitelist\_for\_htkk để đánh dấu hàm an toàn cho Mapping Rule.

* Background job: frappe.enqueue('func', queue='long') cho insert lớn.

* Realtime: frappe.publish\_realtime('htkk\_progress', {percent, message}, doctype, docname).

* SQL safety: Dùng frappe.db.sql với parameterized queries. SQL Builder phải qua sanitize\_sql().

* File attach: frappe.get\_doc('File', ...) để quản lý .json.gz state files. Xóa bản cũ khi save mới.

### **7.2 Vue 3 / Frontend**

* Frappe API: frappe.call({method, args, callback}) hoặc fetch('/api/method/...').

* Realtime: frappe.realtime.on('htkk\_progress', handler).

* Routing: Dùng Frappe Page routing, không Vue Router (vì embed trong Frappe).

* State: Vue reactive (ref/reactive), không cần Vuex/Pinia cho scope module này.

* Build: Vite build output vào custom\_app/public/js/htkk.bundle.js. Frappe load qua hooks.py.

### **7.3 ag-Grid \+ Tailwind**

* ag-Grid: Dùng ag-grid-community (MIT). Import AgGridVue từ ag-grid-vue3.

* Column Defs: Định nghĩa từ parsed\_nodes của Template (Repeatable Nodes).

* Tailwind: Dùng @tailwindcss/forms cho input styling. Prefix htkk- cho custom classes.

* Layout: Form từ khai dùng grid-cols-12 Tailwind, mapping từ template config.

* Color-code: Toggle CSS classes (bg-blue-50, bg-yellow-50...) không inline style.

### **7.4 Testing**

* Unit test engine/: pytest, mock frappe.db khi cần.

* Integration test: frappe.tests.utils.FrappeTestCase.

* Auto-detect accuracy: Test trên 5+ file .xlsx thực, assert precision \> 85%.

* XML validation: So output với expected XML (ignore whitespace).

### **7.5 hooks.py**

\# custom\_app/custom\_app/htkk/hooks.pyapp\_include\_js \= \['/assets/custom\_app/js/htkk.bundle.js'\]app\_include\_css \= \['/assets/custom\_app/css/htkk.css'\]fixtures \= \[    {"dt": "HTKK Mapping Rule", "filters": {"rule\_type": "Standard"}}\]\# Scheduler for deadline alertsscheduler\_events \= {    "daily": \["custom\_app.custom\_app.htkk.api.declaration.check\_deadlines"\]}

*— Hết tài liệu —*