# Import Auto (AI) — Smart Plan + Smart Fix Handoff

> **Dùng cho tab AI mới:** mở file này trước, rồi đọc tiếp các file code được liệt kê ở mục **7. Files đã sửa trong session này**. Nếu cần kiểm chứng nhanh, chạy các command ở mục **8. Cách chạy lại local**.
>
> **Prompt gợi ý cho tab mới:** "Đọc `docs/modules/import-auto/AI_SMART_FIX_HANDOFF.md` rồi tiếp tục phát triển/test module Import Auto AI theo phần Roadmap."
>
> **Mục đích:** Tài liệu này tổng hợp toàn bộ context cần thiết để tiếp tục phát triển/bảo trì module **Import tự động (AI)** trong `dcnet_migrate`, đặc biệt là 2 workflow:
> 1. **Smart Plan** — AI sinh kế hoạch insert đa bước cho file Excel (đặc biệt: Chart of Accounts).
> 2. **Smart Fix** — AI tự sửa lỗi import, kể cả **tự đề xuất tạo dữ liệu phụ thuộc còn thiếu** (Department, Designation, ...) trước khi insert lại.
>
> Tài liệu được sinh sau session phát triển ngày 21/05/2026. Mọi file path đều là **đường dẫn tuyệt đối từ repo root** `flow_next/`.

---

## 0. TL;DR — workflow user-facing

```
[Đường dẫn import = 1 file .xlsx HOẶC 1 thư mục HOẶC nhiều dòng]
    ↓ Quét tệp Excel (scan_files)
[Bảng files: 1 row / file]
    ↓ Phân tích (analyze_files) — AI nhận diện target_doctype
[Hàng có safety_status = Safe/Warning]
    ↓ Bấm nút ☀️ Smart Import (smart_plan_file)
[Dialog: plan_summary tiếng Việt + N steps với preview table/tree]
    ↓ User bấm "Đồng ý import vào ERPNext" (smart_execute_file → savepoint)
    ✓ Inserted records          ✗ Failed → dialog lỗi với nút "🪄 Sửa lỗi bằng AI"
                                    ↓ smart_fix_file (AI sinh patches + new_dependency_steps)
                                [Dialog diff: ô tick các Department/Designation thiếu]
                                    ↓ User confirm (confirm_smart_fix_dependencies)
                                [Plan đã merge → execute_smart_plan lần 2]
```

---

## 1. Repo layout

```
flow_next/                                 # repo root, cwd
├── dcnet-migrate/dcnet_migrate/           # Frappe app handle data migration
│   ├── import_auto/
│   │   ├── doctype/
│   │   │   ├── import_auto/                ← parent doc; auto-name IMPORT-AUTO-YYYY-#####
│   │   │   │   ├── import_auto.json        ← field schema (folder_path, recursive, file_pattern, files-table, ...)
│   │   │   │   ├── import_auto.py          ← controller + whitelisted endpoints
│   │   │   │   └── import_auto.js          ← UI dialogs, progress, smart-fix renderer  (3500+ lines)
│   │   │   ├── import_auto_file/           ← child table row per Excel file
│   │   │   └── import_auto_settings/       ← AI config (api_key, model, base_url, timeout)
│   │   ├── services/
│   │   │   ├── utils.py                    ← scan_excel_files (file | folder | multi-line), file_sha256, normalize_key
│   │   │   ├── excel.py                    ← summarize_workbook, extract_records, header detection
│   │   │   ├── ai_client.py                ← OpenAI-compatible chat completion wrapper
│   │   │   ├── doctype_metadata.py         ← IMPORT_FILE_HINTS, get_doctype_schema, infer_import_file
│   │   │   ├── analysis.py                 ← per-file AI analysis → mappings/defaults
│   │   │   ├── duplicate_checker.py        ← match check against existing DB
│   │   │   ├── processor.py                ← background runners (scan, analyze, reanalyze) + realtime
│   │   │   ├── smart_planner.py            ⭐ AI plan builder + COA post-process + smart-fix
│   │   │   ├── smart_executor.py           ⭐ executes plan steps in a savepoint
│   │   │   ├── smart_runner.py             ← background queue for smart_plan / smart_fix + realtime
│   │   │   └── importer.py                 ← legacy Data Import-based path (still used for safe files)
│   │   └── workspace/import_auto_home/
│   └── ...
```

**Stack:** Frappe v16 + ERPNext v16 + custom app `dcnet_migrate`. Container `devcontainer-frappe-1`, site `flow.local`, company test: `CÔNG TY CỔ PHẦN VIỄN THÔNG DCNET` (abbr `DCNET`).

---

## 2. Doctype `Import Auto` — fields cốt lõi

```
folder_path (Small Text, required)
    Label: "Đường dẫn import"
    Accepts:
      (a) /abs/path/to/file.xlsx
      (b) /abs/path/to/folder/
      (c) Nhiều dòng (\n hoặc ;) — mỗi dòng 1 file hoặc folder
recursive (Check, default 1)   — chỉ áp dụng khi đường dẫn là folder
file_pattern (Data, default "*.xlsx,*.xls") — chỉ áp dụng khi folder
company (Link Company)
status (Select hidden) — Draft/Scanning/Scanned/Analyzing/Analyzed/Importing/Completed/Partial/Failed
files (Table → Import Auto File)
summary_json (Code JSON, read-only)
AI section (hidden) — api_base_url, api_key (Password), model, timeout_seconds
```

**Naming:** `IMPORT-AUTO-{YYYY}-{#####}` (Expression).
**Permissions:** System Manager (full), Accounts Manager (no delete).

---

## 3. Smart Plan — AI sinh kế hoạch insert

### 3.1 Entry points

| Method (whitelisted) | Caller | Action |
|---|---|---|
| `Import Auto.smart_plan_file(file_row_name)` | JS `run_smart_plan` | Enqueue background job sinh plan |
| `dcnet_migrate.import_auto.services.smart_runner.run_smart_plan_job` | RQ worker | Gọi `build_smart_plan` rồi publish realtime `import_auto_smart_plan` |
| `Import Auto.smart_execute_file(file_row_name, plan_json)` | JS `execute_smart_plan` | Gọi `smart_executor.execute_plan(dry_run=False)` |

### 3.2 `smart_planner.build_smart_plan(doc, file_row, user_feedback)`

1. `summarize_workbook(file_row.file_path)` → sheets + sample 30 rows.
2. Đọc `file_row.analysis_json` (target_doctype, sheet_name, header_row_number).
3. `extract_records(file_path, sheet_name, header_row)` → toàn bộ raw rows.
4. Detect COA: `_is_coa_file(file_row, analysis, headers)` (filename contains `he_thong_tai_khoan`/`chart_of_accounts`, hoặc headers có cả `account_number` + `parent_account`, hoặc analysis đã ra `Account`).
5. Nếu COA: lấy `_company_coa_context(company)` (abbr, existing root accounts, 5 expected VN roots).
6. Build system prompt: base + `COA_SYSTEM_PROMPT_ADDON` (11 quy tắc ERPNext-specific).
7. User payload: company, headers, sheet_name, total_records, records_sample, `is_chart_of_accounts`, `coa_context`, `required_json_schema`.
8. Chat completion với `Import Auto Settings.api_base_url + model + api_key` (timeout floor 5 min cho smart plan).
9. `_parse_json_response(raw)` → plan dict.
10. `_normalise_plan(plan, raw_records, doc)`:
    - Validate every step's target_doctype tồn tại.
    - Materialise `row_template.field_map` nếu plan dùng row_template thay vì liệt kê records.
    - Dedupe theo `deduplicate_by`.
    - Cap `MAX_PLAN_RECORDS_PER_STEP = 5000`.
    - Apply `fixed_values`.
    - Default `company` field cho mọi DocType có `company` field.
    - Set `preview_format = "tree"` nếu doctype ∈ `HIERARCHICAL_DOCTYPES`.
    - **Topological sort** records nếu có `parent_field` (cha trước con).
11. Nếu plan không error → `_post_process_coa_plan(plan, doc)`:
    - Ghép `" - {abbr}"` vào mọi `parent_account` (idempotent).
    - Set `parent_account = None` cho root (KHÔNG để `""` — ERPNext sẽ raise MandatoryError).
    - Map `balance_must_be`: `"Dư Nợ"→Debit`, `"Dư Có"→Credit`, các giá trị khác → `""`.
    - Map `disabled`: `"Ngừng sử dụng"→1`, mặc định `0`.
    - Whitelist `account_type` về danh sách ERPNext (Bank, Cash, Receivable, Payable, Tax, Stock, Fixed Asset, Expense Account, Income Account, ...).
    - Tạo đúng 5 root VN còn thiếu (Tài sản/Nợ phải trả/Vốn chủ sở hữu/Thu nhập/Chi phí) thành step đầu tiên; bỏ root step nếu DB đã có hết.
    - Topo-sort lại bằng key đã có suffix.
    - Renumber `step` field + recompute totals.

### 3.3 `smart_executor.execute_plan(doc, file_row, plan, dry_run)`

- Tạo savepoint `smart_import_savepoint`.
- Loop từng step → từng record → `frappe.get_doc(record).insert()`.
- **Đặc biệt với `Account`**: tự set `flags.ignore_mandatory = True` (vì `parent_account` được mark mandatory ngay cả cho root).
- Nếu step nào fail: lưu `failed_step_index`, `failed_row_index`, `failed_record`, `error_type` (classified: MandatoryError / LinkValidationError / ValidationError / DuplicateEntryError / PermissionError) → raise → rollback savepoint.
- Trả về dict: `{ok, results, total_inserted, total_failed, total_skipped, failed_*}`.

---

## 4. Smart Fix — AI sửa lỗi + đề xuất tạo dữ liệu phụ thuộc

### 4.1 Entry points

| Method | Caller |
|---|---|
| `Import Auto.smart_fix_file(file_row, plan_json, error_json)` | JS `run_smart_fix` |
| `smart_runner.run_smart_fix_job` | RQ worker → publish realtime `import_auto_smart_fix` |
| `Import Auto.confirm_smart_fix_dependencies(file_row, plan_json, proposals_json, accepted_ids_json)` ⭐NEW | JS sau khi user tick chọn |

### 4.2 `smart_planner.fix_plan_errors`

**Input:** plan dict + error_info dict.

**Stages (publish realtime `import_auto_smart_fix`):**

| stage | percent | message |
|---|---|---|
| reading | 10 | Đang đọc lại tệp Excel để có context... |
| preparing | 25 | Đang chuẩn bị bối cảnh cho AI... |
| **scanning** ⭐ | 40 | Đang phát hiện dữ liệu phụ thuộc còn thiếu... |
| thinking | 55 | AI đang phân tích lỗi và đề xuất sửa... |
| applying | 85 | Đang áp dụng các thay đổi vào plan... |
| complete | 100 | Đã sửa xong, đang tải bản xem so sánh... |

**Pre-AI: `_detect_missing_dependencies(plan, error_info, doc)`** — quét mọi Link field trong plan, check `frappe.db.exists()` trong DB (kể cả company-scoped). Trả về dict:

```json
{
  "Department": {
    "missing_values": ["PHÒNG KỸ THUẬT HẠ TẦNG", "PHÒNG KINH DOANH"],
    "via_fields": ["department"],
    "total_missing": 2
  },
  "Designation": {...}
}
```

Chỉ scan các doctype nằm trong `SMART_FIX_DEPENDENCY_ALLOWED_DOCTYPES`.

### 4.3 AI prompt 3-option output

AI có thể chọn 1 trong 3 cách sửa:

| Option | Field | Mô tả |
|---|---|---|
| **A. Patches** | `patches` | Sửa field-level trong records đã có. CHỈ field trong `SMART_FIX_ALLOWED_FIELDS`. Field trong `SMART_FIX_PROTECTED_FIELDS` (account_number, account_name, opening_balance, debit, credit, ...) bị reject. |
| **B. New dependency steps** ⭐ | `new_dependency_steps` | Tạo TRƯỚC bản ghi master data còn thiếu (Department, Designation, UOM, ...). Phải nằm trong `SMART_FIX_DEPENDENCY_ALLOWED_DOCTYPES`. |
| **C. Unresolved** | `unresolved` | Không xử lý được, để user fix tay. |

Output JSON strict: `{"patches":[...], "new_dependency_steps":[...], "unresolved":[...]}`.

### 4.4 `SMART_FIX_DEPENDENCY_ALLOWED_DOCTYPES` (whitelist 24 master)

```
HR:           Department, Designation, Employee Grade, Branch, Employment Type,
              Holiday List, Shift Type, Leave Type
Selling/Buy:  Customer Group, Supplier Group, Territory, Sales Person
Items:        Item Group, Brand, UOM, Item Attribute
Stock:        Warehouse
Accounting:   Cost Center, Account, Mode of Payment, Currency
Projects:     Project, Project Type
Generic:      Country
```

**KHÔNG** có transactional doctype (Sales Invoice, Stock Entry, Journal Entry, Payment Entry, ...). Bảo mật — AI không bao giờ tự tạo voucher.

`SMART_FIX_MAX_DEPENDENCY_RECORDS = 200` — vượt = reject.

### 4.5 `_normalise_dependency_proposals(raw_steps, plan)`

Server-side validation cho mỗi proposal AI trả về:
- `target_doctype` phải trong whitelist + tồn tại trên site.
- `records` non-empty + ≤ 200.
- Strip empty fields, dedupe theo `unique_key`.
- Check `frappe.db.exists()` từng record → tách `records_to_create` vs `records_existing` (số đã có).
- Auto-detect `label_field` qua `_guess_label_field`.
- Trả về list proposals đã sạch + list rejected (kèm reason tiếng Việt).

**Quan trọng:** function này KHÔNG insert vào plan. Nó chỉ chuẩn bị các đề xuất để UI hiển thị. Việc insert xảy ra sau khi user tick + bấm confirm.

### 4.6 `merge_dependency_steps_into_plan(plan, accepted_ids, all_proposals)` ⭐

Gọi từ `confirm_smart_fix_dependencies` sau khi user confirm:
1. Deep copy plan.
2. Mỗi proposal được tick → tạo 1 step mới:
   ```python
   {
     "step": <renumbered>,
     "title": "[AI gợi ý] Tạo {target_doctype} còn thiếu",
     "description": proposal.reason,
     "target_doctype": ...,
     "_origin": "smart_fix_dependency",
     "_proposal_id": proposal.proposal_id,
     ...
   }
   ```
3. Chèn vào plan trước `insert_before_step` (sort descending để index không lệch).
4. Renumber `step`, recompute totals.
5. Gọi `_rewrite_link_refs_post_merge(plan)` ⭐:

### 4.7 `_rewrite_link_refs_post_merge(plan)` ⭐ (critical)

Một số DocType ERPNext autoname với suffix `" - {abbr}"`:
- **Đổi tên:** Department, Account, Cost Center, Warehouse (`Department: PHÒNG KỸ THUẬT → PHÒNG KỸ THUẬT - DCNET`).
- **Không đổi:** Designation, UOM, Brand, Item Group (autoname từ chính field label).

Function này:
1. Quét các step có `_origin = "smart_fix_dependency"` → predict tên ERPNext final qua `_predict_record_name(doctype, rec)` (đọc `meta.autoname`).
2. Build name_map: `(doctype, raw_label) → predicted_name`.
3. Quét tất cả step gốc → mọi Link field → nếu value match raw_label → rewrite thành predicted_name.

**Ví dụ:**

```python
# Before merge:
Employee.department = "PHÒNG KỸ THUẬT HẠ TẦNG"

# After merge + rewrite:
Employee.department = "PHÒNG KỸ THUẬT HẠ TẦNG - DCNET"
```

Không có function này thì step Employee sẽ fail vì link không khớp.

---

## 5. Frontend — `import_auto.js`

### 5.1 Smart plan dialog (existing, ~ line 1004)

- `show_smart_plan_dialog(frm, row_name, payload)`
- Render từng step:
  - `preview_format = "tree"` → render hierarchical tree (indented by depth) cho Account/Item Group/Cost Center.
  - `preview_format = "table"` → render flat table với header columns lấy từ records.
- Primary action: `execute_smart_plan(frm, row_name, plan, dialog)`.

### 5.2 Smart fix dialog ⭐ MODIFIED

#### Progress dialog (`render_smart_fix_progress`)
8 stages mới (vs 6 cũ): `queued → reading → preparing → scanning → thinking → applying → merging → complete`. Có percent + spinner + timeline chấm tròn.

#### Diff dialog (`show_smart_fix_diff_dialog`)
Renders 4 sections (giảm nhiễu khi không có):

1. **Summary** — 4 tile: Đã sửa | Dữ liệu phụ thuộc đề xuất tạo | Từ chối (bảo vệ data) | Chưa xử lý được.
2. **Dependency proposals** ⭐ NEW — `render_smart_fix_proposals(proposals)`:
   - Card per target_doctype (gradient tím-xanh).
   - Icon + title `Department  [2 bản ghi mới]  (1 đã có trong DB, bỏ qua)`.
   - Reason tiếng Việt của AI.
   - Meta: "Sẽ chèn trước bước **N**" + "Khử trùng theo `<unique_key>`".
   - Nút "Chọn tất cả/Bỏ chọn tất cả" per card.
   - Bảng records preview với checkbox per row, các cột thông minh chọn từ `pick_proposal_columns()` (ưu tiên label_field, sau là department_name/designation_name/uom_name/..., max 6 cột).
3. **Fixes table** — bảng diff before/after từng patch.
4. **Rejected / Unresolved** — `<details>` collapsible.

Primary action label tự động đổi theo case:
- Cả patches + proposals: "✓ Tạo dữ liệu thiếu & import lại"
- Chỉ proposals: "✓ Tạo dữ liệu thiếu & import lại (N mục)"
- Chỉ patches: "✓ Xác nhận import lại (N thay đổi)"
- Không có gì: "Import lại (không có sửa đổi)"

#### Confirm flow
Khi user bấm primary action:
1. Collect các `proposal_id` của checkbox đang `:checked` (nhóm theo proposal).
2. Nếu không có proposal → call `execute_smart_plan` trực tiếp với `new_plan`.
3. Nếu có proposal:
   - Mở progress dialog ("Đang ghép N bước dữ liệu phụ thuộc vào kế hoạch...").
   - Call `confirm_smart_fix_dependencies(plan_json, proposals_json, accepted_ids_json)` → response.message.plan = merged plan.
   - Hiển thị alert success.
   - Call `execute_smart_plan(frm, row_name, merged, parent_dialog)`.

### 5.3 CSS classes mới
```
.import-auto-dep-proposals               container (gradient bg)
.import-auto-dep-proposal                card
.import-auto-dep-proposal__head          header
.import-auto-dep-proposal__icon          gradient avatar
.import-auto-dep-proposal__title         doctype title + badges
.import-auto-dep-proposal__count         pill badge
.import-auto-dep-proposal__reason        AI reason text
.import-auto-dep-proposal__meta          chip meta info
.import-auto-dep-proposal__select-all    button
.import-auto-dep-proposal__table-wrap    sticky-header table 260px
.import-auto-dep-proposal__check         checkbox
.import-auto-fix-summary__item.is-proposal   tile color indigo
```

---

## 6. Đã test thành công

### Test A — Chart of Accounts (file `he_thong_tai_khoan_DCNET.xlsx`, 259 rows)

```
[1] Scan: 1 file → 1 row in files-table
[2] Analyze: target_doctype=Account, safety_status=Safe
[3] Smart Plan: AI sinh 2 steps:
    • Step 1: 5 root VN (Tài sản, Nợ phải trả, Vốn chủ sở hữu, Thu nhập, Chi phí)
    • Step 2: 259 accounts với parent_account đã ghép " - DCNET", topo-sorted
[4] Execute: 264 inserted, 0 failed, 0 skipped
[5] DB verify: 52 groups + 212 leaves + 5 disabled ✅
```

File test command:
```bash
docker exec devcontainer-frappe-1 bash -lc \
  "cd /workspace/development/frappe-bench/sites && \
   /workspace/development/frappe-bench/env/bin/python /tmp/test_full.py"
```

### Test B — Smart Fix với dependency Department/Designation

Synthetic plan: 2 Employee references missing Department + Designation.

```
[1] _detect_missing_dependencies → 2 Department + 2 Designation missing
[2] fix_plan_errors → AI returns 2 proposals (Department, Designation), 0 patches
[3] User accepts all → merge_dependency_steps_into_plan:
    step 1 [smart_fix_dependency] Designation (2 recs)
    step 2 [smart_fix_dependency] Department (2 recs)
    step 3 [original] Employee (2 recs với department="...- DCNET")
[4] Execute merged plan: 6 inserted, 0 failed ✅
[5] DB verify: tất cả 6 records tồn tại với đúng autoname
```

---

## 7. Files đã sửa trong session này

| File | Lý do | Function chính ảnh hưởng |
|---|---|---|
| `dcnet-migrate/dcnet_migrate/import_auto/services/utils.py:1` | Cho phép `folder_path` nhận file/folder/multi-line | `scan_excel_files`, mới: `resolve_input_path`, `_split_input_entries`, `_is_valid_excel` |
| `dcnet-migrate/dcnet_migrate/import_auto/services/doctype_metadata.py:34` | Mở rule COA `is_supported=False → True`, thêm keyword `he_thong_tai_khoan` | `IMPORT_FILE_HINTS` |
| `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.json` | Đổi label "Đường dẫn import", `folder_path` thành Small Text, thêm description 3 chế độ | field schema |
| `dcnet-migrate/dcnet_migrate/import_auto/services/smart_planner.py` | COA prompt + post-process + dependency proposals + link rewriter | `build_smart_plan`, `_is_coa_file`, `_company_coa_context`, `_post_process_coa_plan`, `fix_plan_errors`, `_detect_missing_dependencies`, `_normalise_dependency_proposals`, `merge_dependency_steps_into_plan`, `_rewrite_link_refs_post_merge`, `_predict_record_name`, `_topological_sort_records` |
| `dcnet-migrate/dcnet_migrate/import_auto/services/smart_executor.py:108` | Set `flags.ignore_mandatory=True` cho Account | `_run_step` |
| `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.py` | Endpoint mới `confirm_smart_fix_dependencies` | thêm 1 method trên class + 1 top-level whitelist |
| `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.js` | Dialog diff: section proposals + checkbox + confirm flow + CSS + thêm 2 stage `scanning`/`merging` | `show_smart_fix_diff_dialog`, `render_smart_fix_diff`, mới: `render_smart_fix_proposals`, `pick_proposal_columns`, `format_proposal_value`, `guess_label_field`; CSS class mới `import-auto-dep-proposal*` |

---

## 8. Cách chạy lại local (cheat-sheet)

### Container
- Container: `devcontainer-frappe-1`
- Bench root: `/workspace/development/frappe-bench`
- Python venv: `/workspace/development/frappe-bench/env/bin/python`
- Site: `flow.local`

### Common bench commands
```bash
# Migrate (sau khi sửa .json doctype)
docker exec devcontainer-frappe-1 bash -lc \
  "cd /workspace/development/frappe-bench && bench --site flow.local migrate"

# Clear cache (sau khi sửa code Python/JS)
docker exec devcontainer-frappe-1 bash -lc \
  "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"

# Console (Frappe IPython shell)
docker exec -it devcontainer-frappe-1 bash -lc \
  "cd /workspace/development/frappe-bench && bench --site flow.local console"

# Run script with frappe context (preferred for tests — produces clean stdout)
docker exec devcontainer-frappe-1 bash -lc \
  "cd /workspace/development/frappe-bench/sites && \
   /workspace/development/frappe-bench/env/bin/python /tmp/my_script.py"
```

### Cleanup test data
```python
# bench --site flow.local console
import frappe
COMPANY = "CÔNG TY CỔ PHẦN VIỄN THÔNG DCNET"
# Accounts (must delete by rgt asc to avoid parent-not-empty errors)
for a in frappe.get_all("Account", filters={"company": COMPANY},
                         fields=["name"], order_by="rgt asc"):
    try: frappe.delete_doc("Account", a.name, ignore_permissions=True, force=True)
    except Exception: pass
# Import Auto docs
for ia in frappe.get_all("Import Auto", pluck="name"):
    try: frappe.delete_doc("Import Auto", ia, ignore_permissions=True, force=True, delete_permanently=True)
    except Exception: pass
frappe.db.commit()
```

### Test files dùng được
```
/workspace/data import/kế toán/15.05.2026/he_thong_tai_khoan_DCNET.xlsx   ← COA 259 accounts
/workspace/data import/kế toán/15.05.2026/Danh_sach_nhan_vien.xlsx        ← Employee (trigger smart fix)
/workspace/data import/kế toán/15.05.2026/Danh_sach_khach_hang.xlsx       ← Customer
/workspace/data import/kế toán/15.05.2026/Danh_sach_nha_cung_cap.xlsx     ← Supplier
... và nhiều file khác trong folder
```

---

## 9. Vấn đề/quirks đã biết

1. **AI thỉnh thoảng đề xuất Designation dù plan đã có step Designation gốc** — không sai về logic vì executor có `ignore_duplicates=True`, chỉ hơi thừa. Có thể tinh chỉnh prompt sau nếu muốn AI biết "đừng đề xuất nếu đã có step tạo cái đó".
2. **Employee yêu cầu mandatory fields** (gender, date_of_birth, date_of_joining) — không phải lỗi của module, mà là yêu cầu của ERPNext. AI hiện không tự fill từ Excel nếu cột không có. Tương lai: mở rộng `SMART_FIX_ALLOWED_FIELDS` cho phép AI patch các default sentinel value (vd: `gender = "Prefer not to say"` nếu Excel không có).
3. **`is_supported` đã True nhưng heuristic analysis vẫn cần `direct mappings`** — file `he_thong_tai_khoan_DCNET.xlsx` được AI route đúng vì headers match `account_number`, `account_name`, `parent_account`. Nếu file Excel khác có headers tiếng Việt khác, AI vẫn xử lý được vì smart_plan dùng full payload không phụ thuộc heuristic mapping.
4. **`bench migrate` chạy plugin install hooks rất chậm** (~30s) — không liên quan module này, chỉ là noise.
5. **HierarchicalDoctype không tự autoname suffix:** chỉ Department/Account/Cost Center/Warehouse có suffix `" - {abbr}"`. Item Group thì autoname theo `field:item_group_name` (no suffix). `_predict_record_name` đã handle, nhưng nếu thêm doctype mới vào whitelist cần update `_predict_record_name` + `_candidate_raw_keys`.

---

## 10. Roadmap tiếp theo (open work)

- [ ] **Apply smart fix cho transactional plans:** Hiện smart fix mạnh nhất cho master data. Cần test với plans như Sales Order/Purchase Order (Link fields: Customer, Supplier, Item) — đảm bảo link rewrite đúng cho các autoname phức tạp hơn (`SO-{####}` vs `field:customer_name`).
- [ ] **AI dependency proposal cho Item:** Item có hệ phụ thuộc phức tạp (UOM + Item Group + Brand). Test xem AI có chain đúng không khi import Item file.
- [ ] **Cho phép user edit values trong dialog proposal:** hiện chỉ tick/bỏ tick. Có thể thêm inline-edit cho cột label nếu cần (vd: AI gõ sai `PHÒNG KỸ THUẬT HẠ TẦNG` thì user sửa thành `PHÒNG KỸ THUẬT HẠ TẦNG (HN)`).
- [ ] **Per-step retry instead of full plan rollback:** Hiện 1 step fail → rollback toàn bộ savepoint. Có thể thêm option "Bỏ qua step lỗi, tiếp tục" với savepoint riêng cho từng step.
- [ ] **Lưu plan history:** Hiện plan trả về realtime, mất sau khi đóng dialog. Có thể lưu `last_smart_plan_json` vào `Import Auto File` để user xem lại sau.
- [ ] **Audit log cho dependency creation:** Khi AI tạo Department/Designation, log lại "AI auto-created via Import Auto IMPORT-AUTO-...#####" để user truy vết.
- [ ] **Test các file đông như `Danh_sach_hang_hoa_dich_vu.xlsx`** (Item list, thường > 500 rows) — kiểm tra `row_template` materialise hoạt động đúng.

---

## 11. Câu hỏi cần clarify với khách (nếu phát sinh task mới)

- ⚠️ **Item Group hierarchy:** Khách muốn phân nhóm cha-con như thế nào? (Item Group có `parent_item_group` field — tương tự Account)
- ⚠️ **Default values cho Employee:** Field nào được set mặc định khi Excel không có? (gender, date_of_birth, date_of_joining)
- ⚠️ **Mapping cho file `Doi_tuong_tap_hop_chi_phi.xlsx`:** Đối tượng tập hợp chi phí ERPNext không có doctype tương đương — cần custom DocType?

---

**Hết. Đọc xong file này là tab AI mới có thể tiếp tục bất kỳ task nào liên quan Import Auto.**
