# 04 - Danh mục NCC: Spec -> ERPNext Mapping

> **Nguồn:** ERP_SPECIFICATION.md Section 3.0 + SRS Section 3.4
> **ERPNext:** v16 — Buying Module (Supplier, Supplier Group, Price List)
> **Cập nhật:** 17/02/2026

## Quy ước Tags

| Tag | Nghĩa | Action |
|-----|--------|--------|
| `USE` | ERPNext có sẵn, dùng ngay | Config + test |
| `CFG` | ERPNext có, cần config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext có, cần mở rộng | Custom field, client/server script |
| `NEW` | ERPNext không có, cần build | Custom DocType, module mới |
| `REF` | Thuộc module khác | Tham chiếu |

---

## 3.0. Danh mục NCC (2 features)

### 3.0.1. Danh mục nhà cung cấp

- **Tag:** `CFG`
- **Spec yêu cầu:** Quản lý thông tin NCC (Mã, Tên, Nhóm, Điều khoản thanh toán)
- **ERPNext:** Supplier DocType + Supplier Group + Contact + Address
- **ERPNext đã có:**
  - **Supplier DocType**: Tên NCC, Supplier Group, Payment Terms, Tax ID, website, disabled flag
  - **Supplier Group**: Phân loại NCC theo nhóm (tree structure, hỗ trợ nhóm con)
  - **Contact**: Liên hệ NCC (tên, email, phone, designation) — link tới Supplier
  - **Address**: Địa chỉ NCC (billing, shipping) — link tới Supplier
  - **Supplier Dashboard**: Tự động hiển thị Purchase Orders, Purchase Invoices, Purchase Receipts liên kết
  - **Supplier Scorecard**: Đánh giá NCC theo tiêu chí (giao hàng đúng hạn, chất lượng, giá cả)
  - **Data Import**: Import/Export Supplier từ Excel (built-in)
  - **CRUD**: Tạo/Sửa/Xóa đầy đủ với permission control
- **Gap:** Không có gap lớn. Cần config:
  - Setup Supplier Group phù hợp (nội địa, quốc tế, theo hãng/thương hiệu)
  - Setup Payment Terms Template cho các loại NCC
  - Config Supplier Scorecard criteria (nếu dùng)
  - Tạo Data Import template chuẩn để import từ BRAVO
- **Action:**
  1. Tạo Supplier Group theo cấu trúc khách hàng yêu cầu
  2. Tạo Payment Terms Template (VD: 30 ngày, 60 ngày, COD)
  3. Config Naming Series cho Supplier (nếu cần mã riêng)
  4. Tạo Data Import template để import NCC từ BRAVO
  5. Config Supplier Scorecard criteria (nếu khách hàng cần)
  6. Test CRUD + import/export
- **Effort:** 1-1.5 ngày
- **Dependency:** Không có

**Chi tiết tính năng (từ SRS):**

| Tính năng | ERPNext | Status |
|-----------|---------|--------|
| Danh sách NCC (tên, mã, liên hệ, nhóm) | Supplier DocType + Contact | Có sẵn |
| Tạo/Sửa/Xóa thông tin NCC | Supplier CRUD | Có sẵn |
| Phân loại NCC theo nhóm (nội địa, quốc tế, hãng) | Supplier Group (tree) | Cần setup data |
| Điều khoản thanh toán theo NCC | Payment Terms Template | Cần setup data |
| Lịch sử giao dịch và công nợ NCC | Supplier Dashboard + Accounts Payable | Có sẵn |
| Đánh giá NCC (SRS TM) | Supplier Scorecard | Cần config criteria |
| Import/Export NCC từ Excel | Data Import/Export | Có sẵn |

---

### 3.0.2. Bảng giá nhà cung cấp

- **Tag:** `CFG`
- **Spec yêu cầu:** Giá theo model/SKU + Hiệu lực giá + Làm cơ sở tính KM đầu vào
- **ERPNext:** Price List (Buying) + Item Price + Pricing Rule
- **ERPNext đã có:**
  - **Price List**: Tạo nhiều bảng giá (VD: bảng giá từng NCC/hãng)
  - **Item Price**: Giá theo Item + Price List, có `valid_from` và `valid_upto` (hiệu lực giá)
  - **Pricing Rule**: Tự động áp dụng chiết khấu/giá đặc biệt theo điều kiện (NCC, SL, thời gian)
  - **Supplier Quotation**: Báo giá từ NCC, so sánh giá giữa các NCC
  - **Buying Settings**: Default Buying Price List
- **Gap:**
  - "Cơ sở tính KM đầu vào": Cần clarify KM cụ thể là gì (chiết khấu % theo doanh số? quà tặng? volume discount?)
  - ERPNext Pricing Rule có thể handle phần lớn nhưng cần hiểu rõ yêu cầu để config đúng
- **Action:**
  1. Tạo Buying Price List cho từng NCC hoặc nhóm NCC
  2. Setup Item Price với valid_from / valid_upto
  3. Config Pricing Rule cho các loại ưu đãi NCC (sau khi clarify)
  4. Test luồng: Item Price → Purchase Order tự động lấy giá đúng
- **Effort:** 1-1.5 ngày
- **Dependency:** 03 - Sản phẩm (cần có Item trước)
- **Clarify:** Xem CLARIFY.md #1.1 — "Cơ sở tính KM đầu vào" cụ thể là gì?

---

## Liên kết với features module khác (REF)

| Feature | Module | Ghi chú |
|---------|--------|---------|
| Ưu đãi NCC (CK%, CK tiền, quà tặng) | 05 - Mua hàng (3.1.1) | Config Pricing Rule ở module 05 |
| Công nợ NCC | 26 - KT Công nợ | Accounts Payable built-in |
| Lịch sử mua hàng theo NCC | 05 - Mua hàng (3.1.17) | Report ở module 05 |
| BC NCC tốt nhất | 06 - BC Phân tích (3.1.18) | Report ở module 06 |

---

## Tổng hợp

| Tag | Số feature | Effort |
|-----|-----------|--------|
| `CFG` | 2 | 2-3 ngày |
| **Tổng** | **2** | **2-3 ngày** |

### Phân bổ effort chi tiết

| Hạng mục | Effort |
|----------|--------|
| Setup Supplier Group + Payment Terms | 0.5 ngày |
| Setup Price List + Item Price | 0.5 ngày |
| Config Supplier Scorecard (nếu cần) | 0.5 ngày |
| Tạo Data Import template (BRAVO migration) | 0.5 ngày |
| Testing + Fix | 0.5 ngày |
| **Tổng** | **2.5 ngày** |
