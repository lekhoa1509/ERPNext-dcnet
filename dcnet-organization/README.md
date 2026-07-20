# DCNET Organization

App Frappe/ERPNext độc lập, override cách lưu **liên kết cơ cấu tổ chức**:

```
Company ── Branch ── Department ── Designation
```

Frappe/ERPNext gốc chỉ có liên kết `Department → Company`. App này bổ sung các liên
kết còn thiếu bằng **Custom Field** (tạo tự động khi install/migrate):

| # | DocType       | Field thêm vào | Kiểu           | Bắt buộc | Ý nghĩa |
|---|---------------|----------------|----------------|----------|---------|
| 1 | `Branch`      | `company`      | Link → Company | ❌ Không | Chi nhánh (tuỳ chọn) thuộc công ty nào |
| 2 | `Department`  | `branch`       | Link → Branch  | ❌ Không | Phòng ban (tuỳ chọn) thuộc chi nhánh |
| 3 | `Designation` | `department`   | Link → Department | ❌ Không | Chức vụ (tuỳ chọn) thuộc phòng ban |

## Tính năng

- **Custom Field tự tạo**: `install.py` gọi `create_custom_fields(..., update=True)` trong
  `after_install` và `after_migrate`. Không dùng fixtures → nguồn sự thật nằm trong
  `organization_customization.py`, dễ review qua git.
- **Cài độc lập**: nếu site chưa có `Branch`/`Department`/`Designation` (chưa cài
  erpnext/hrms), app bỏ qua an toàn, không crash.
- **Link filtering (client)**: form Department chỉ hiện chi nhánh cùng công ty; chọn chi
  nhánh trước sẽ tự điền công ty. Designation chỉ hiện phòng ban còn hoạt động.
- **Validation (server)**: khi lưu, `Department.branch` phải cùng công ty với phòng ban;
  `Designation.department` không được là phòng ban đã vô hiệu hoá.

## Cài đặt

```bash
# trong frappe-bench
bench get-app dcnet_organization /path/to/apps/dcnet-organization
bench --site <site> install-app dcnet_organization
# hoặc nếu đã install, cập nhật field:
bench --site <site> migrate
bench build --app dcnet_organization   # nếu cần publish JS client
```

## Cấu trúc

```
dcnet_organization/
├── hooks.py                      # after_install/migrate, doctype_js, doc_events
├── install.py                    # ensure_organization_custom_fields()
├── organization_customization.py # định nghĩa CUSTOM_FIELDS (nguồn sự thật)
├── overrides.py                  # validate_department / validate_designation
├── modules.txt                   # DCNET Organization
└── public/js/
    ├── branch.js
    ├── department.js
    └── designation.js
```

## License

MIT
