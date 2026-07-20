# Import tự động (AI) Duplicate Check Warning + Popup

## Overview

Sau khi AI/heuristic phân tích xong tệp Excel, hệ thống đối chiếu dữ liệu trong tệp với các bản ghi đã có trong cơ sở dữ liệu. Nếu phát hiện trùng (chính xác hoặc gần đúng), trạng thái an toàn của tệp được hạ từ **Safe** xuống **Warning** (thay vì giữ Safe hoặc đẩy thành Error). Người dùng có thêm nút **Kiểm tra trùng** trên mỗi dòng để mở popup hiển thị các bản ghi đã có trong DB cùng với loại khớp và link tới bản ghi gốc.

## Requirements

- Sau Analyze hoặc Reanalyze: tự động chạy duplicate check cho các dòng `Safe` và đặt lại `safety_status = Warning` khi có trùng.
- Mỗi dòng có nút check riêng để chạy lại đối chiếu bất kỳ lúc nào (ví dụ sau khi DB thay đổi).
- Popup phải hiển thị: DocType đối chiếu, tổng dòng tệp, số trùng chính xác, số có thể trùng, danh sách mẫu (cột tệp ↔ bản ghi đã có).
- Vẫn cho phép import file `Warning` nhưng phải bật xác nhận thêm trước khi mở Data Import.
- Người dùng `Error` vẫn bị chặn import như cũ.

## Implementation

- DocType `Import Auto File` thêm 3 field: `duplicate_check_status` (Pending/Clean/Warning/Error), `duplicate_match_count`, `duplicate_report_json`. `safety_status` thêm option `Warning`.
- Service `dcnet_migrate.import_auto.services.duplicate_checker`:
  - Per-DocType `MATCH_RULES` định nghĩa exact key (ví dụ `tax_id`, `item_code`) và fuzzy key (ví dụ `customer_name`).
  - `check_duplicates_for_row(doc, row)` đọc records từ Excel theo `analysis.sheet_name` + `header_row_number`, build index từ `frappe.get_all(target_doctype)` và so trùng bằng `normalize_key`. Trả về `{total_matches, exact_match_count, fuzzy_match_count, samples[]}`.
  - `determine_safety_status` chỉ hạ `Safe → Warning`, không chuyển `Error → Warning`.
- `processor.analyze_files` và `reanalyze_file` chạy duplicate check ngay sau analysis cho mọi dòng `Safe`.
- API mới `check_duplicates_file(file_row_name, docname)` (cả module-level + doc-method) cho phép re-run từ UI.
- `importer._validate_row_for_import` cho phép `Warning` import (`Safe` hoặc `Warning`); `Error` vẫn chặn.
- `import_auto.js`:
  - Stat card mới **Cảnh báo** (amber).
  - Row state `warning` + status pill mới + style amber.
  - Action group thêm nút **kính lúp** với badge số dòng trùng. Nút import row Warning hiện label `Import (cảnh báo)` + class `btn-warning`.
  - `frappe.confirm` mở trước khi prepare Data Import nếu `safety_status === "Warning"`, thông báo số dòng trùng + ghi chú.
  - Popup duplicate hiển thị summary + bảng mẫu (link sang `/app/{doctype}/{name}` cho mỗi bản ghi đã có).
- Patch `dcnet_migrate.patches.v0_0_2.run_duplicate_check_for_existing_rows` chạy ngay sau migrate để backfill cho rows đã có trong DB.

## Technical Notes

- Files thay đổi:
  - `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto_file/import_auto_file.json`
  - `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.py`
  - `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.js`
  - `dcnet-migrate/dcnet_migrate/import_auto/services/duplicate_checker.py` (mới)
  - `dcnet-migrate/dcnet_migrate/import_auto/services/processor.py`
  - `dcnet-migrate/dcnet_migrate/import_auto/services/importer.py`
  - `dcnet-migrate/dcnet_migrate/patches/v0_0_2/run_duplicate_check_for_existing_rows.py` (mới)
  - `dcnet-migrate/dcnet_migrate/patches.txt`
- Index limit `EXISTING_INDEX_LIMIT = 5000` để không bị nặng khi DocType đích lớn. Sample popup giới hạn `SAMPLE_LIMIT = 25` dòng đầu tiên.
- Fuzzy match dùng substring trên chuỗi đã chuẩn hoá (`normalize_key`) để bắt các tên có khoảng trắng/dấu khác nhau giữa BRAVO và ERPNext.
- Reuse `MATCH_RULES` cho 11 DocType chính (UOM, Item Group, Bank, Warehouse, Customer, Supplier, Item, Bank Account, Department, Project, Account). DocType ngoài danh sách trả về note `Chưa hỗ trợ đối chiếu trùng cho ...` và không hạ trạng thái.

## Deployment

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

`migrate` sẽ tự sync 3 field mới vào bảng `tabImport Auto File` và chạy patch backfill. Nếu chỉ muốn chạy lại backfill mà không migrate đầy đủ:

```bash
bench --site flow.local execute dcnet_migrate.patches.v0_0_2.run_duplicate_check_for_existing_rows.execute
```

## Verification Checklist

- [ ] Sau Analyze: row có dữ liệu trùng đã chuyển sang `Warning` (cột "An toàn" hiển thị Cảnh báo amber).
- [ ] Bấm nút kính lúp mở popup liệt kê đúng các bản ghi đã có trong DB.
- [ ] Bấm Import trên row Warning xuất hiện confirm trước khi mở Data Import.
- [ ] Backfill patch chạy không lỗi và cập nhật `duplicate_match_count`.
- [ ] Row `Error` vẫn bị chặn import như cũ.

## Future Updates

- Có thể mở rộng `MATCH_RULES` cho thêm DocType (Address, Contact, Employee...) khi mở rộng scope migration.
- Có thể thêm filter "Chỉ hiện file Warning" trong toolbar nếu danh sách dài.
- Cân nhắc cache `existing_index` theo (target_doctype, hash) để chạy lại nhanh hơn khi click nhiều file cùng DocType.
