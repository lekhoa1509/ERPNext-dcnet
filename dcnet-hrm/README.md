# DCNET HRM

Custom Frappe app bổ sung nghiệp vụ nhân sự – tiền lương theo pháp luật Việt Nam
trên nền [Frappe HR](https://github.com/frappe/hrms) (không viết lại doctype gốc
của Frappe HR — chỉ extend qua Custom Field / hooks, và tạo doctype mới cho phần
pháp luật VN không có tương đương).

Nguồn yêu cầu: `prompt-dcnet-hrm.md` (repo root).

## Cài đặt (dev)

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench get-app dcnet_hrm /workspace/dcnet-hrm && bench --site flow.local install-app dcnet_hrm"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

## Lộ trình

- **Phase 1 — Payroll VN (core):** constants + VN Payroll Settings + Insurance Rate +
  Statutory Wage + Dependent + Custom Fields + `payroll/vn_payroll.py` + unit tests +
  báo cáo bảng lương tháng. ✅ đang triển khai.
- **Phase 2 — Pháp lý:** Labor Contract + Insurance Declaration (D02-LT) + 05/KK-TNCN +
  PIT Annual Settlement.
- **Phase 3 — Chấm công & OT:** ZKTeco connector + Overtime Request + overtime engine.

## Đa ngôn ngữ (EN/VN)

App dùng cơ chế i18n chuẩn của Frappe: label/message viết mặc định bằng English,
bản dịch tiếng Việt nằm trong `dcnet_hrm/translations/vi.csv`. Khi đổi Language của
User hoặc System Settings, giao diện tự đổi theo — không cần switcher riêng.
