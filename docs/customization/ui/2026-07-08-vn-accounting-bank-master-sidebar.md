# VN Accounting Bank Master Sidebar

## Overview

Thêm danh mục **Ngân hàng** vào sidebar **VN Accounting > Danh mục** để kế toán truy cập nhanh DocType chuẩn `Bank`.

## Requirements

- Mục nằm trong nhóm **Danh mục**.
- Link tới DocType `Bank`.
- Không thay thế nhóm nghiệp vụ **Ngân hàng** và không thay thế `Bank Account`.

## Implementation

- Cập nhật `dcnet-accounting/vn_accounting/workspace_sidebar/vn_accounting.json`.
- Cập nhật help tổng quan `dcnet-accounting/vn_accounting/help/danh-muc/index.md`.
- Sync DB bằng `vn_accounting.install._sync_workspace_sidebar`.

## Technical Notes

`Bank` là danh mục ngân hàng; `Bank Account` là tài khoản ngân hàng cụ thể của công ty. Hai mục cần tách riêng để tránh nhầm giữa master data và tài khoản kế toán/ngân hàng dùng trong giao dịch.

## Deployment

```bash
bench --site flow.local execute vn_accounting.install._sync_workspace_sidebar
bench --site flow.local clear-cache
```

## Verification Checklist

- [x] JSON sidebar hợp lệ.
- [x] DB có item `Ngân hàng -> Bank` trong `VN Accounting`.
- [x] Route `/desk/bank` không còn lỗi page/module.
