# VN Accounting — Vietnamese Accounting for ERPNext v16

Bản địa hoá kế toán Việt Nam cho ERPNext v16 theo Thông tư 99/2025/TT-BTC.

## Features

### Chart of Accounts (Hệ thống tài khoản)

- **2 COA templates** theo TT99/2025: Doanh nghiệp lớn (`vn_large_enterprise`) và Doanh nghiệp nhỏ (`vn_small_enterprise`)
- Tự động đăng ký khi chọn Country = Vietnam trong Company creation flow
- Tự động thiết lập tài khoản mặc định (Cash, Bank, AR, AP, Income, Expense, Depreciation...) sau khi tạo Company

### Reports (Báo cáo)

| Report | Tên tiếng Việt | Mô tả |
|--------|---------------|-------|
| Bang Can Doi So Phat Sinh | Bảng cân đối số phát sinh | Số dư đầu kỳ, phát sinh, cuối kỳ theo tài khoản |
| So Chi Tiet Tai Khoan | Sổ chi tiết tài khoản | Sổ cái theo từng tài khoản, có số dư chạy |
| So Quy Tien Mat | Sổ quỹ tiền mặt | Thu/chi tiền mặt (TK 111) |
| So Tien Gui Ngan Hang | Sổ tiền gửi ngân hàng | Thu/chi ngân hàng (TK 112) |

### Workspace & Dashboard

- **5 Number Cards**: Tồn quỹ, Tổng doanh thu, Tổng chi phí, Công nợ phải thu, Công nợ phải trả
- **4 Dashboard Charts**: Doanh thu vs Chi phí, Biến động tiền, AR timeline, AP timeline
- **Workspace sidebar** với 40+ navigation items, sticky across DocTypes (3-tier selection: localStorage → boot defaults → Frappe)

### Sidebar Fixes (Frappe v16)

- Fix `route_options` trên DocType links trong Workspace Sidebar (Frappe v16 bug)
- Auto-accordion sections với localStorage persistence
- Workspace sidebar persistence khi navigate giữa các DocType

## Requirements

- Frappe v16.x
- ERPNext v16.x

## Installation

```bash
bench get-app https://github.com/<org>/vn_accounting
bench --site <site> install-app vn_accounting
```

After install, create a new Company with Country = Vietnam to see VN COA templates.

## Account Number Reference (TT99/2025)

| TK | Tên | ERPNext mapping |
|----|-----|-----------------|
| 111 | Tiền mặt | default_cash_account |
| 112 | Tiền gửi ngân hàng | default_bank_account |
| 131 | Phải thu khách hàng | default_receivable_account |
| 1561 | Giá mua hàng hoá (con của 156) | default_inventory_account |
| 1562 | Chi phí thu mua hàng hoá (con của 156) | TK đích cho phụ phí LCV (mặc định) |
| 214 | Hao mòn TSCĐ | accumulated_depreciation_account |
| 331 | Phải trả người bán | default_payable_account |
| 511 | Doanh thu | default_income_account |
| 632 | Giá vốn hàng bán | default_expense_account |
| 711 | Thu nhập khác | round_off_account |

## License

MIT
