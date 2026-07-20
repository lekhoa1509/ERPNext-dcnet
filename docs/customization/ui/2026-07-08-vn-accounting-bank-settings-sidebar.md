# VN Accounting Bank Settings Sidebar

## Overview

Thêm mục **Cài đặt ngân hàng** vào sidebar **VN Accounting > Thiết lập** để kế toán mở nhanh cấu hình import/đối soát sao kê ngân hàng.

## Requirements

- Mục nằm trong nhóm **Thiết lập**.
- Link tới Single DocType `Bank Statement Settings` của app `vn_banking`.
- Không thay đổi các mục nghiệp vụ ngân hàng hiện có trong nhóm **Ngân hàng**.

## Implementation

- Cập nhật `dcnet-accounting/vn_accounting/workspace_sidebar/vn_accounting.json`.
- Cập nhật help tổng quan `dcnet-accounting/vn_accounting/help/thiet-lap/index.md`.
- Sync DB bằng `vn_accounting.install._sync_workspace_sidebar`.

## Technical Notes

`Bank Statement Settings` quản lý tolerance đối soát, tài khoản phí/chênh lệch ngân hàng, regex nhận diện hóa đơn và rule match khi import sao kê.

## Deployment

Chạy migrate hoặc gọi sync sidebar:

```bash
bench --site flow.local execute vn_accounting.install._sync_workspace_sidebar
bench --site flow.local clear-cache
```

## Verification Checklist

- [x] JSON sidebar hợp lệ.
- [x] DB có item `Cài đặt ngân hàng -> Bank Statement Settings`.
- [x] Item nằm sau `Cài đặt kho` và trước `Cài đặt kế toán`.
