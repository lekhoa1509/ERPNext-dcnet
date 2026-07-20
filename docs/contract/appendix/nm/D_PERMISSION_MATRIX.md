# PHỤ LỤC D - MA TRẬN PHÂN QUYỀN
# PERMISSION MATRIX

> **Tài liệu:** SRS - DCNET Flow
> **Phiên bản:** 1.0.0
> **Ngày tạo:** 03/02/2026

---

## 1. DANH SÁCH VAI TRÒ (ROLES)

| # | Role | Mô tả | Cấp độ |
|---|------|-------|--------|
| 1 | **System Administrator** | Quản trị hệ thống, cấu hình | Cao nhất |
| 2 | **General Manager** | Ban Lãnh đạo, xem tất cả | Cao |
| 3 | **Sales Manager** | Giám đốc Kinh doanh | Cao |
| 4 | **Accounting Manager** | Kế toán trưởng | Cao |
| 5 | **Warehouse Manager** | Quản lý Kho | Trung bình |
| 6 | **Sales User** | Nhân viên Kinh doanh | Thấp |
| 7 | **Fitter** | Nhân viên Fitting | Thấp |
| 8 | **Coach** | Huấn luyện viên | Thấp |
| 9 | **Accountant** | Nhân viên Kế toán | Thấp |
| 10 | **Warehouse User** | Nhân viên Kho | Thấp |
| 11 | **Purchase User** | Nhân viên Mua hàng | Thấp |
| 12 | **Store Cashier** | Nhân viên Thu ngân | Thấp |

---

## 2. MA TRẬN PHÂN QUYỀN THEO MODULE

### Chú thích

| Ký hiệu | Ý nghĩa |
|---------|---------|
| **C** | Create (Tạo mới) |
| **R** | Read (Xem) |
| **U** | Update (Sửa) |
| **D** | Delete (Xóa) |
| **A** | Approve (Duyệt) |
| **P** | Print (In) |
| **E** | Export (Xuất file) |
| ✅ | Có quyền |
| ❌ | Không có quyền |
| 🔒 | Quyền hạn chế (chỉ dữ liệu của mình) |

---

### 2.1. Module CRM - Lead

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | Accountant |
|-----------|-----------|-----|-----------|------------|------------|
| Xem danh sách Lead | ✅ | ✅ | ✅ | 🔒 | ❌ |
| Tạo Lead | ✅ | ✅ | ✅ | ✅ | ❌ |
| Sửa Lead | ✅ | ✅ | ✅ | 🔒 | ❌ |
| Xóa Lead | ✅ | ✅ | ✅ | ❌ | ❌ |
| Import Lead | ✅ | ✅ | ✅ | ❌ | ❌ |
| Export Lead | ✅ | ✅ | ✅ | 🔒 | ❌ |
| Phân công Lead | ✅ | ✅ | ✅ | ❌ | ❌ |
| Chuyển Lead thành KH | ✅ | ✅ | ✅ | ✅ | ❌ |

### 2.2. Module CRM - Khách hàng

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | Accountant | WH User |
|-----------|-----------|-----|-----------|------------|------------|---------|
| Xem danh sách KH | ✅ | ✅ | ✅ | 🔒 | ✅ | ❌ |
| Xem chi tiết KH 360° | ✅ | ✅ | ✅ | 🔒 | ✅ | ❌ |
| Tạo KH | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Sửa KH | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ |
| Xóa KH | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Xem công nợ KH | ✅ | ✅ | ✅ | 🔒 | ✅ | ❌ |
| Thiết lập hạn mức CN | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Import KH | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Export KH | ✅ | ✅ | ✅ | 🔒 | ✅ | ❌ |

### 2.3. Module Bán hàng - Đơn hàng

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | Accountant | WH Mgr | WH User | Cashier |
|-----------|-----------|-----|-----------|------------|------------|--------|---------|---------|
| Xem DS đơn hàng | ✅ | ✅ | ✅ | 🔒 | ✅ | ✅ | 🔒 | 🔒 |
| Tạo đơn bán lẻ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Tạo đơn bán buôn | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sửa đơn hàng | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | ❌ | ❌ |
| Hủy đơn hàng | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Duyệt đơn vượt hạn mức | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| In đơn hàng | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Export đơn hàng | ✅ | ✅ | ✅ | 🔒 | ✅ | ❌ | ❌ | ❌ |

### 2.4. Module Bán hàng - Bảng giá & Chiết khấu

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | Accountant |
|-----------|-----------|-----|-----------|------------|------------|
| Xem bảng giá | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tạo bảng giá | ✅ | ✅ | ✅ | ❌ | ❌ |
| Sửa bảng giá | ✅ | ✅ | ✅ | ❌ | ❌ |
| Xóa bảng giá | ✅ | ✅ | ❌ | ❌ | ❌ |
| Xem chính sách CK | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tạo chính sách CK | ✅ | ✅ | ✅ | ❌ | ❌ |
| Sửa chính sách CK | ✅ | ✅ | ✅ | ❌ | ❌ |
| Xem Voucher | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tạo Voucher | ✅ | ✅ | ✅ | ❌ | ❌ |

### 2.5. Module Sản phẩm

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | WH Mgr | WH User | Purchase |
|-----------|-----------|-----|-----------|------------|--------|---------|----------|
| Xem DS sản phẩm | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Xem chi tiết SP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tạo sản phẩm | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Sửa sản phẩm | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Xóa sản phẩm | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Import SP | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Export SP | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Quản lý danh mục | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |

### 2.6. Module Mua hàng

| Chức năng | Sys Admin | GM | Purchase | Acc Mgr | Accountant | WH Mgr | WH User |
|-----------|-----------|-----|----------|---------|------------|--------|---------|
| Xem DS PO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Tạo PO | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sửa PO | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Duyệt PO | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Tạo phiếu nhập | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| Xem công nợ NCC | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Tạo đề nghị TT | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Duyệt thanh toán | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |

### 2.7. Module Kho

| Chức năng | Sys Admin | GM | WH Mgr | WH User | Sales User | Accountant |
|-----------|-----------|-----|--------|---------|------------|------------|
| Xem DS kho | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tạo kho | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Xem tồn kho | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tạo phiếu nhập | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Tạo phiếu xuất | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Điều chuyển kho | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Kiểm kê | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Duyệt điều chỉnh | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| In tem nhãn | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Xem giá trị tồn** | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Xem đơn giá** | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |

> **Lưu ý:** Nhân viên Kho (WH User) không được phép xem đơn giá, thành tiền trên các chứng từ kho.

### 2.8. Module Kế toán

| Chức năng | Sys Admin | GM | Acc Mgr | Accountant | Sales Mgr | WH Mgr |
|-----------|-----------|-----|---------|------------|-----------|--------|
| Xem sổ cái | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Tạo bút toán | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Duyệt bút toán | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Xem công nợ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Tạo phiếu thu | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Tạo phiếu chi | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Duyệt phiếu chi | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Xuất hóa đơn | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Xem báo cáo TC | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Khóa sổ kỳ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |

### 2.9. Module Dịch vụ Fitting

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | Fitter | Accountant |
|-----------|-----------|-----|-----------|------------|--------|------------|
| Xem DS Fitting | ✅ | ✅ | ✅ | 🔒 | ✅ | ✅ |
| Tạo đơn Fitting | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Nhập thông số KT | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Tư vấn đề xuất | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Tạo SO từ Fitting | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Xem báo cáo Fitting | ✅ | ✅ | ✅ | ❌ | 🔒 | ✅ |

### 2.10. Module Dịch vụ Coaching

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | Coach | Accountant |
|-----------|-----------|-----|-----------|------------|-------|------------|
| Xem DS Coaching | ✅ | ✅ | ✅ | 🔒 | 🔒 | ✅ |
| Tạo đơn Coaching | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Quản lý gói học | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Lên lịch học | ✅ | ✅ | ✅ | ❌ | 🔒 | ❌ |
| Điểm danh | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Đánh giá học viên | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Xem báo cáo | ✅ | ✅ | ✅ | ❌ | 🔒 | ✅ |

### 2.11. Module Trade-in

| Chức năng | Sys Admin | GM | Sales Mgr | Sales User | WH Mgr | Accountant |
|-----------|-----------|-----|-----------|------------|--------|------------|
| Xem DS Trade-in | ✅ | ✅ | ✅ | 🔒 | ✅ | ✅ |
| Tạo đơn Trade-in | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Kiểm tra SP cũ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Đề xuất giá thu | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Duyệt giá thu | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Xử lý kho | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Xem báo cáo | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |

### 2.12. Module Báo cáo

| Chức năng | Sys Admin | GM | Sales Mgr | Acc Mgr | WH Mgr | Sales | Acc |
|-----------|-----------|-----|-----------|---------|--------|-------|-----|
| BC Doanh số | ✅ | ✅ | ✅ | ✅ | ❌ | 🔒 | ✅ |
| BC Đơn hàng | ✅ | ✅ | ✅ | ✅ | ✅ | 🔒 | ✅ |
| BC Khách hàng | ✅ | ✅ | ✅ | ✅ | ❌ | 🔒 | ❌ |
| BC Nhân viên | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| BC Kho | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| BC Mua hàng | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| BC Tài chính | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| BC Công nợ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | 🔒 | 🔒 |

### 2.13. Module Hệ thống

| Chức năng | Sys Admin | GM | Managers | Users |
|-----------|-----------|-----|----------|-------|
| Quản lý User | ✅ | ❌ | ❌ | ❌ |
| Quản lý Role | ✅ | ❌ | ❌ | ❌ |
| Phân quyền | ✅ | ❌ | ❌ | ❌ |
| Cấu hình hệ thống | ✅ | ❌ | ❌ | ❌ |
| Quản lý Chi nhánh | ✅ | ✅ | ❌ | ❌ |
| Quản lý Nhân viên | ✅ | ✅ | 🔒 | ❌ |
| Xem Audit Log | ✅ | ✅ | ❌ | ❌ |
| Backup/Restore | ✅ | ❌ | ❌ | ❌ |

---

## 3. PHÂN QUYỀN THEO CHI NHÁNH

### 3.1. Nguyên tắc

1. **Mỗi User thuộc một Chi nhánh chính**
2. **User chỉ xem/tạo dữ liệu của chi nhánh mình** (trừ Manager)
3. **Manager có thể xem tất cả chi nhánh**
4. **System Admin không giới hạn**

### 3.2. Ma trận phân quyền theo Chi nhánh

| Role | Xem data Chi nhánh mình | Xem data Chi nhánh khác | Tạo data Chi nhánh khác |
|------|-------------------------|-------------------------|-------------------------|
| System Administrator | ✅ | ✅ | ✅ |
| General Manager | ✅ | ✅ | ✅ |
| Sales Manager | ✅ | ✅ | ❌ |
| Accounting Manager | ✅ | ✅ | ❌ |
| Warehouse Manager | ✅ | ✅ | ❌ |
| Sales User | ✅ | ❌ | ❌ |
| Fitter | ✅ | ❌ | ❌ |
| Coach | ✅ | ❌ | ❌ |
| Accountant | ✅ | ❌ | ❌ |
| Warehouse User | ✅ | ❌ | ❌ |
| Purchase User | ✅ | ✅* | ✅* |
| Store Cashier | ✅ | ❌ | ❌ |

> *Purchase User có thể xem/tạo PO cho tất cả chi nhánh do tính chất công việc mua hàng tập trung.

---

## 4. QUY TRÌNH PHÊ DUYỆT

### 4.1. Các loại phê duyệt

| Loại | Điều kiện | Người duyệt |
|------|-----------|-------------|
| Đơn hàng vượt hạn mức | Công nợ > Credit Limit | Accounting Manager |
| Đơn hàng KH quá hạn | Có HĐ quá hạn TT | Accounting Manager |
| Giá bán ngoài bảng giá | Giá # bảng giá | Sales Manager |
| Giá thu Trade-in | Tất cả | Sales Manager |
| Điều chỉnh kho | Chênh lệch kiểm kê | Warehouse Manager |
| Phiếu chi > 10 triệu | Giá trị > 10,000,000 | Accounting Manager |
| Phiếu chi > 50 triệu | Giá trị > 50,000,000 | General Manager |
| PO > 500 triệu | Giá trị > 500,000,000 | General Manager |

### 4.2. Workflow phê duyệt

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Người tạo    │────►│  Chờ duyệt    │────►│  Đã duyệt     │
│  (Draft)      │     │  (Pending)    │     │  (Approved)   │
└───────────────┘     └───────┬───────┘     └───────────────┘
                              │
                              │ Từ chối
                              ▼
                      ┌───────────────┐
                      │  Bị từ chối   │
                      │  (Rejected)   │
                      └───────────────┘
```

---

## 5. RÀNG BUỘC BẢO MẬT

### 5.1. Các quy tắc bảo mật

| Quy tắc | Mô tả |
|---------|-------|
| Password | Tối thiểu 8 ký tự, chữ hoa + thường + số |
| Session Timeout | 30 phút không hoạt động |
| Login Attempts | Khóa sau 5 lần sai |
| IP Whitelist | Giới hạn IP truy cập (optional) |
| 2FA | Two-Factor Authentication (optional) |
| Audit Log | Ghi nhận mọi thao tác |

### 5.2. Dữ liệu nhạy cảm

| Dữ liệu | Ai được xem | Ghi chú |
|---------|-------------|---------|
| Giá vốn | Sys Admin, GM, Acc Mgr, Accountant | Kho không thấy |
| Lợi nhuận | Sys Admin, GM, Acc Mgr | |
| Lương NV | Sys Admin, GM | |
| Credit Limit KH | Sys Admin, GM, Sales Mgr, Acc Mgr | |
| Số dư ngân hàng | Sys Admin, GM, Acc Mgr | |

---

## 6. TỔNG HỢP SỐ LƯỢNG QUYỀN

### 6.1. Thống kê theo Role

| Role | Số module | Số quyền C | Số quyền R | Số quyền U | Số quyền D | Số quyền A |
|------|-----------|------------|------------|------------|------------|------------|
| System Administrator | Tất cả | Tất cả | Tất cả | Tất cả | Tất cả | Tất cả |
| General Manager | Tất cả | Hạn chế | Tất cả | Hạn chế | Hạn chế | Nhiều |
| Sales Manager | CRM, Bán hàng | Nhiều | Nhiều | Nhiều | Một số | Một số |
| Accounting Manager | Kế toán, BC | Nhiều | Nhiều | Nhiều | Hạn chế | Nhiều |
| Sales User | CRM, Bán hàng | Nhiều | Hạn chế | Hạn chế | Không | Không |
| Warehouse User | Kho | Một số | Một số | Một số | Không | Không |

### 6.2. Thống kê theo Module

| Module | Số vai trò có quyền | Vai trò chính |
|--------|---------------------|---------------|
| Lead | 4 | Sales User, Sales Manager |
| Khách hàng | 5 | Sales User, Sales Manager |
| Đơn hàng | 7 | Sales User, Cashier |
| Sản phẩm | 5 | Purchase User |
| Mua hàng | 5 | Purchase User |
| Kho | 4 | Warehouse User |
| Kế toán | 3 | Accountant |
| Fitting | 4 | Fitter, Sales User |
| Coaching | 4 | Coach, Sales User |
| Trade-in | 5 | Sales User |
| Báo cáo | 7 | Managers |
| Hệ thống | 1-2 | Sys Admin |

---

**© 2026 DCNET Corporation**
