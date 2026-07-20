# Import tự động — Xử lý thông minh (AI Multi-Step Plan)

## Overview

Một số file Excel của khách (ví dụ `Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx`) cần map sang **nhiều DocType ERPNext** trong một lần import (Bank → Bank Account → Opening Journal Entry…). Việc bắt user tách file là không khả thi vì dữ liệu lớn và khách không nắm rõ cấu trúc ERPNext.

Tính năng mới:

- Nút **Xử lý thông minh (AI)** trên mỗi row + trong popup *Review tệp Excel*.
- AI đọc lại file, tự động lập **kế hoạch nhiều bước** (mỗi bước là 1 DocType + danh sách bản ghi) và tự chuẩn hoá số kiểu Việt Nam (`1.234.567,89`), loại bỏ dòng `Tổng/Cộng/Total`.
- Trước khi insert, hệ thống mở popup preview:
  - DocType **dạng cây** (Account, Item Group, Cost Center, Department, Warehouse…) → tree view, hỗ trợ parent/child.
  - DocType phẳng → table view (tối đa 8 cột, 20 dòng đầu).
- User có thể **góp ý cho AI** ngay trong popup → bấm *Phân tích lại* để AI tạo plan khác.
- Khi confirm, server gọi `frappe.get_doc(...).insert()` cho từng bản ghi, **toàn bộ chạy trong 1 SAVEPOINT** — fail là rollback hết, không insert nửa vời.

## Implementation

- `dcnet_migrate/import_auto/services/smart_planner.py` (mới): build prompt + parse, normalise plan, gắn `company`, fill default field, đoán `unique_key` / `label_field` / `parent_field` cho DocType cây.
- `dcnet_migrate/import_auto/services/smart_executor.py` (mới): `execute_plan(doc, row, plan, dry_run)` — mở SAVEPOINT, lặp từng step → record, skip duplicate theo `unique_key`, fail là rollback toàn bộ và return `{ok: False, error}`.
- `dcnet_migrate/import_auto/doctype/import_auto/import_auto.py`:
  - Doc-method + module-level whitelisted `smart_plan_file` và `smart_execute_file`.
  - `_execute_smart_plan` cập nhật trạng thái row Excel sau khi insert (`Imported` / `Partial` + `imported_records` / `failed_records`).
- `dcnet_migrate/import_auto/doctype/import_auto/import_auto.js`:
  - Nút biểu tượng **mặt trời nhỏ** (`smart_btn`) trên mỗi row.
  - Nút phụ trong popup *Review tệp Excel* (`set_secondary_action`).
  - `run_smart_plan` → `show_smart_plan_dialog` → `execute_smart_plan` (`frappe.confirm` xác nhận trước khi insert).
  - `render_smart_step` chọn tree/table dựa vào `preview_format`. Tree dùng `parent_field` + `unique_key` để gom node.

### Plan JSON Schema (AI output)

```json
{
  "plan_summary": "Vietnamese summary",
  "steps": [
    {
      "step": 1,
      "title": "Tạo Bank",
      "description": "...",
      "target_doctype": "Bank",
      "preview_format": "table",
      "unique_key": "bank_name",
      "label_field": "bank_name",
      "ignore_duplicates": true,
      "fixed_values": { "...": "..." },
      "records": [{ "bank_name": "..." }]
    }
  ]
}
```

## Hạn chế / lưu ý

- Plan chỉ insert document mới (mode `insert`); chưa hỗ trợ update/upsert. Trùng theo `unique_key` được skip an toàn.
- Mỗi bước giới hạn `MAX_PLAN_RECORDS_PER_STEP = 5000` để tránh AI trả plan quá lớn.
- Sample preview giới hạn 20 dòng; plan thực thi đầy đủ records trong JSON.
- Nếu AI không trả JSON đúng schema → popup hiển thị error đỏ, không cho confirm.
- Vẫn giữ flow Data Import cũ (CSV) cho file đơn giản — user tự chọn nút Import truyền thống hoặc Smart.

## Verification

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

- [ ] Bấm nút mặt trời nhỏ trên row → popup hiển thị các bước.
- [ ] Account / Item Group hiển thị cây chính xác theo `parent_*`.
- [ ] Confirm → bản ghi được tạo trong ERPNext (kiểm tra DocType list).
- [ ] Inject lỗi (ví dụ thêm `account_number` trùng) → toàn bộ rollback, ERPNext không có bản ghi mới nào.
- [ ] Trong popup *Review tệp Excel*: bấm secondary action *Xử lý thông minh* mở plan dialog tương đương.
