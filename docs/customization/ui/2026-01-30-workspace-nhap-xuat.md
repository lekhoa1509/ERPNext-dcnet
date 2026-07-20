# Workspace Customization: Quy trình Nhập Xuất hàng

> **Ngày tạo**: 30/01/2026
> **Người thực hiện**: Claude Code
> **Module**: Import Management

---

## 1. Tổng quan

Tạo 2 workspace mới để quản lý quy trình nhập xuất hàng của DCNET Flow:

| Workspace | Mục đích | Icon |
|-----------|----------|------|
| **Nhập hàng từ Hãng** | Quy trình TLTM nhập hàng từ Hãng (TaylorMade, Callaway, etc.) | buying |
| **Bán hàng Đại lý** | Quy trình TLTM bán hàng cho Đại lý cấp 1 | selling |

---

## 2. Files đã tạo

### 2.1. Module Import Management

```
dcnet_apps/dcnet_apps/import_management/
├── __init__.py
├── doctype/
│   ├── __init__.py
│   └── import_schedule/
│       ├── __init__.py
│       ├── import_schedule.json    # DocType definition
│       └── import_schedule.py      # Controller
├── fixtures/
│   ├── __init__.py
│   └── import_schedule.json        # Sample data (7 loại SP)
└── workspace/
    ├── nhap_hang_tu_hang/
    │   └── nhap_hang_tu_hang.json  # Workspace definition
    └── ban_hang_dai_ly/
        └── ban_hang_dai_ly.json    # Workspace definition
```

### 2.2. Files đã update

| File | Thay đổi |
|------|----------|
| `modules.txt` | Thêm "Import Management" |
| `hooks.py` | Thêm fixtures cho Import Schedule và Workspace |

---

## 3. Workspace: Nhập hàng từ Hãng

### 3.1. Menu Structure

| Card | Links |
|------|-------|
| **Quản lý Nhà cung cấp** | Supplier, Supplier Group, Contact, Address |
| **Giao dịch Mua hàng** | Purchase Order, Request for Quotation, Supplier Quotation |
| **Nhập kho** | Purchase Receipt, Warehouse, Item |
| **Thanh toán** | Purchase Invoice, Payment Entry, Accounts Payable |
| **Báo cáo** | Purchase Analytics, Purchase Order Analysis, Supplier-Wise Report, Purchase Order Trends |
| **Lịch đặt hàng** | Import Schedule (NEW), Item Group |

### 3.2. Shortcuts

- Đơn đặt hàng (Purchase Order) - Green
- Phiếu nhập kho (Purchase Receipt) - Blue
- Phiếu thanh toán (Payment Entry) - Orange

---

## 4. Workspace: Bán hàng Đại lý

### 4.1. Menu Structure

| Card | Links |
|------|-------|
| **Quản lý Đại lý** | Customer, Customer Group, Contact, Address |
| **Giao dịch Bán hàng** | Quotation, Sales Order, Item |
| **Giao hàng** | Delivery Note, Warehouse, Packing Slip |
| **Thanh toán** | Sales Invoice, Payment Entry, Accounts Receivable |
| **Giá & Chính sách** | Price List, Item Price, Pricing Rule, Promotional Scheme |
| **Báo cáo** | Sales Analytics, Sales Order Analysis, Customer-wise Report, Sales Order Trends |

### 4.2. Shortcuts

- Đơn bán hàng (Sales Order) - Green
- Phiếu xuất kho (Delivery Note) - Blue
- Hóa đơn bán (Sales Invoice) - Orange

---

## 5. DocType: Import Schedule

### 5.1. Mục đích

Quản lý lịch trình đặt hàng từ Hãng theo từng loại sản phẩm.

### 5.2. Fields

| Field | Type | Description |
|-------|------|-------------|
| category_name | Data (unique) | Tên loại sản phẩm |
| product_category | Link → Item Group | Nhóm sản phẩm |
| supplier | Link → Supplier | Nhà cung cấp |
| is_active | Check | Đang hoạt động |
| order_period | Select | Chu kỳ: Hàng tháng/quý/năm/2 năm |
| order_months | Data | Tháng đặt hàng (T1,T2...) |
| deadline_day | Int | Hạn gửi đơn (ngày trong tháng) |
| lead_time_days | Int | Thời gian giao hàng (ngày) |
| moq | Int | Số lượng tối thiểu |
| moq_unit | Select | Đơn vị: Chiếc/Bộ/Đôi/Thùng |
| notes | Small Text | Ghi chú |

### 5.3. Sample Data (7 loại SP)

| # | Loại SP | Chu kỳ | Tháng | MOQ | Lead time |
|---|---------|--------|-------|-----|-----------|
| 1 | Gậy năm tiếp theo | Hàng năm | T9,T10 | 10 Bộ | 90 ngày |
| 2 | Driver, FW, Rescue, Irons | Hàng năm | T1,T2 | 10 Chiếc | 30 ngày |
| 3 | Softgoods (US Specs) | Hàng tháng | - | - | 30 ngày |
| 4 | Gậy P Series | 2 năm/lần | T3 | - | 90 ngày |
| 5 | Putters | Hàng năm | T4 | - | 90 ngày |
| 6 | Wedges | Hàng năm | T4 | - | 90 ngày |
| 7 | Quần áo & PK (JP) | Hàng quý | T6,T7,T11,T12 | - | 60 ngày |

---

## 6. Deployment

### 6.1. Áp dụng cho team

```bash
# Pull code mới
git pull origin main

# Migrate để tạo DocType và Workspace
bench --site flow.local migrate

# Verify workspace
# Browser: http://flow.local:8000/app/nhap-hang-tu-hang
# Browser: http://flow.local:8000/app/ban-hang-dai-ly
```

### 6.2. Import fixtures (nếu cần)

```bash
# Import Import Schedule data
bench --site flow.local import-doc dcnet_apps/dcnet_apps/import_management/fixtures/import_schedule.json
```

---

## 7. Troubleshooting

### 7.1. Workspace không hiển thị

```bash
# Clear cache
bench --site flow.local clear-cache

# Rebuild assets
bench build --app dcnet_apps
```

### 7.2. DocType không tìm thấy

```bash
# Check module registration
cat dcnet_apps/dcnet_apps/modules.txt
# Phải có: Import Management

# Re-migrate
bench --site flow.local migrate
```

---

## 8. Rollback

Nếu cần rollback:

```bash
# Xóa Workspace
bench --site flow.local console
>>> frappe.delete_doc("Workspace", "Nhập hàng từ Hãng")
>>> frappe.delete_doc("Workspace", "Bán hàng Đại lý")
>>> frappe.db.commit()

# Xóa DocType (xóa data trước)
>>> frappe.db.sql("DELETE FROM `tabImport Schedule`")
>>> frappe.delete_doc("DocType", "Import Schedule")
>>> frappe.db.commit()
```

---

## 9. References

- **Nguồn yêu cầu**: IMPORT_PROCESS_SPECIFICATION.md
- **Flowchart**: ERP_SPECIFICATION.md Section 3.2.0 (Quy trình Mua hàng)
- **Tracking file**: docs/implementation/workspace_nhap_xuat/IMPLEMENTATION_TRACKING.md
