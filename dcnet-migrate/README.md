# dcnet_migrate

Data migration tooling for DCNET Flow / ERPNext v16. Hiện tại bao gồm:

- **Import tự động (AI)** — quét & phân tích Excel xuất từ các hệ thống nguồn, dùng AI map cột → DocType ERPNext, rồi nạp dữ liệu qua Frappe Data Import.

## Quickstart

```bash
# bên trong devcontainer
bench --site <site> install-app dcnet_migrate
```

Sau khi cài:

- Mở workspace **Import tự động (AI)**
- Vào **Setting Import AI** để cấu hình endpoint AI + thư mục Excel
- Tạo bản ghi **Import tự động (AI)** → quét → phân tích → nạp Data Import

## Cấu trúc

```
dcnet-migrate/
├── dcnet_migrate/
│   ├── hooks.py
│   ├── install.py
│   ├── modules.txt
│   └── import_auto/      # module chính
│       ├── doctype/
│       ├── services/
│       └── workspace/
└── pyproject.toml
```

## Tách từ dcnet_apps

App này được tách khỏi `dcnet_apps` để tách rõ phần *runtime business logic* và phần *migration tooling*. Code nội bộ dùng namespace `dcnet_migrate.import_auto.*`.
