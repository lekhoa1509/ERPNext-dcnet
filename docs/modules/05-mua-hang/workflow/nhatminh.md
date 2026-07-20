# Luồng Mua hàng - Nhật Minh Sport

> **Nguồn:** ERP_SPECIFICATION.md Section 3 | DCNET_SRS_NM.md Section 3.5
> **Bàn giao:** T3 (31/03/2026) — Core | T4+ — Nâng cao
> **Phạm vi:** Chỉ bao gồm tính năng trong specs khách hàng
> **Satellites:** 04 (NCC), 06 (BC Phân tích), 24 (KT Mua hàng — chưa có SPEC_MAPPING)

---

## Mục lục

1. [So sánh ERPNext vs Nhật Minh](#1-so-sánh-erpnext-vs-nhật-minh)
2. [Quy trình mua hàng (10 bước)](#2-quy-trình-mua-hàng-10-bước)
3. [Sơ đồ luồng dữ liệu](#3-sơ-đồ-luồng-dữ-liệu)
4. [Chi tiết từng bước](#4-chi-tiết-từng-bước)
5. [Danh mục NCC (Module 04)](#5-danh-mục-ncc-module-04)
6. [Tính năng mua hàng (18 features)](#6-tính-năng-mua-hàng-18-features)
7. [Trạng thái đơn hàng mua (PO)](#7-trạng-thái-đơn-hàng-mua-po)
8. [Nhập hàng: Lô, Serial, Mã vạch](#8-nhập-hàng-lô-serial-mã-vạch)
9. [Trả hàng NCC](#9-trả-hàng-ncc)
10. [Thanh toán NCC](#10-thanh-toán-ncc)
11. [Báo cáo mua hàng (Module 06)](#11-báo-cáo-mua-hàng-module-06)
12. [KT Mua hàng (Module 24)](#12-kt-mua-hàng-module-24)
13. [Vấn đề cần xác nhận với khách](#13-vấn-đề-cần-xác-nhận-với-khách)

---

## 1. So sánh ERPNext vs Nhật Minh

> Bảng dưới liệt kê **toàn bộ** chức năng mua hàng của ERPNext.
> ✅ = Nhật Minh sử dụng | ❌ = Không dùng / Không có trong specs | 🔧 = Cần custom

### 1.1 DocType & Luồng chính

| # | ERPNext DocType / Luồng | NM | Ghi chú |
|---|------------------------|:--:|---------|
| 1 | Material Request (Yêu cầu mua hàng) | ❌ | Specs không đề cập. Thay bằng **Purchase Plan** (Custom) — Bước 1, REQ-PURCH-002 |
| 2 | Supplier Quotation (Báo giá NCC) | ❌ | Specs không đề cập. NM mua từ hãng phân phối cố định |
| 3 | Supplier Quotation Comparison | ❌ | Không cần khi không dùng SQ |
| 4 | **Purchase Order (Đơn hàng mua)** | ✅ | Bước 2, REQ-PURCH-003. + custom fields: ship_mode, vendor_po_number, confirm_ship_date |
| 5 | **Purchase Receipt (Phiếu nhập kho)** | ✅ | Bước 5, REQ-PURCH-005. + workflow duyệt 3 bước + customs fields |
| 6 | **Purchase Invoice (Hóa đơn mua)** | ✅ | Bước 5 (kế toán). Ghi nhận công nợ NCC |
| 7 | **Payment Entry (Thanh toán)** | ✅ | Bước 10, REQ-PURCH-006. + workflow đề nghị TT |
| 8 | **Landed Cost Voucher (Chi phí mua)** | ✅ | Bước 6. Vận chuyển, bốc dỡ |
| 9 | **Debit Note / Purchase Return** | ✅ | Bước 7-8. Workflow 2 bước (Lệnh xuất → Phiếu xuất trả) |
| 10 | Subcontracting (Gia công) | ❌ | Specs không đề cập |
| 11 | Request for Quotation (RFQ) | ❌ | Specs không đề cập |
| 12 | Blanket Order (HĐ khung) | ❌ | Specs không đề cập |

### 1.2 Tính năng trên DocType

| # | ERPNext Feature | NM | Ghi chú |
|---|----------------|:--:|---------|
| 1 | **Supplier Master** | ✅ | Feature 3.0.1: Mã, Tên, Nhóm, Điều khoản TT — Module 04 |
| 2 | **Supplier Price List** | ✅ | Feature 3.0.2: Giá theo model/SKU + hiệu lực — Module 04 |
| 3 | **Pricing Rule - Discount** | ✅ | Feature 3.1.1, REQ-PURCH-007: CK %, CK tiền |
| 4 | **Pricing Rule - Free Item** | ✅ | Feature 3.1.1: Quà tặng kèm |
| 5 | **Batch Tracking** | ✅ | Feature 3.1.8: Mã lô + ngày nhập + link PO |
| 6 | **Serial No Tracking** | ✅ | Feature 3.1.9: Serial duy nhất + scan |
| 7 | **Barcode Scanning** | ✅ | Feature 3.1.10: Gán barcode + quét nhập kho |
| 8 | **File Attachment** | ✅ | Feature 3.1.15: HĐ NCC, phiếu giao, HĐ |
| 9 | **Payment Terms** | ✅ | Feature 3.1.13: Tiền mặt, CK, Công nợ |
| 10 | **PO Status Tracking** | ✅ | Feature 3.1.5, 3.1.7, REQ-PURCH-004: Trạng thái + % nhận |
| 11 | **Payment Status Tracking** | ✅ | Feature 3.1.14: Đã TT / 1 phần / Còn nợ |
| 12 | Multi-currency | ✅ | Bước 5: NK có tiền tệ USD/JPY |
| 13 | Quality Inspection | ❌ | Specs không đề cập QC riêng, chỉ kiểm đếm |
| 14 | BOM-based Purchase | ❌ | Không sản xuất |
| 15 | Auto Reorder | ❌ | KH mua hàng thủ công theo mùa |
| 16 | Inter-company Purchase | ❌ | 2 site riêng, không mua chéo trên hệ thống |
| 17 | Purchase Taxes Template | ✅ | Bước 5: thuế NK (nhập khẩu) |

### 1.3 Báo cáo

| # | ERPNext Report | NM | Ghi chú |
|---|---------------|:--:|---------|
| 1 | Purchase Analytics | ✅ | Feature 3.1.17 (lịch sử mua hàng) |
| 2 | Purchase Order Analysis | ✅ | Feature 3.1.7 (theo dõi thực hiện) |
| 3 | Purchase Order Items To Receive | ✅ | Theo dõi hàng chưa nhận |
| 4 | Accounts Payable / AP Summary | ✅ | Bước 9 (xác nhận công nợ) |
| 5 | Supplier Ledger Summary | ✅ | Bước 9 (đối chiếu NCC) |
| 6 | Purchase Register | ✅ | Lịch sử mua hàng |
| 7 | Stock Balance | ✅ | Module 06: Feature 14.5.1 |
| 8 | Stock Ageing | ✅ | Module 06: Feature 6.3.1 (hàng tồn chậm) |
| 9 | Supplier-Wise Sales Analytics | ❌ | Không cần |
| 10 | Items To Be Requested | ❌ | Không dùng Material Request |
| 11 | Requested Items To Order | ❌ | Không dùng Material Request |
| 12 | **Giá mua bình quân** | 🔧 | Feature 3.1.18: Custom Script Report |
| 13 | **NCC tốt nhất** | 🔧 | Feature 3.1.18: Custom Script Report |
| 14 | **So sánh KH mua vs Đơn hàng** | 🔧 | BC quản trị: Custom Script Report |
| 15 | **Hàng sắp hết vòng đời** | 🔧 | Module 06: Feature 6.3.2: Custom Report |
| 16 | **Hàng thanh lý / sale** | 🔧 | Module 06: Feature 6.3.4: Custom Report |

### 1.4 Custom DocType (Không có trong ERPNext)

| # | DocType mới | Mapping specs | Ghi chú |
|---|------------|:------------:|---------|
| 1 | **Purchase Plan** | Bước 1, REQ-PURCH-002 | KH 12 tháng, fields: Family, Year, Category, Shaft |
| 2 | **Delivery Schedule** | Bước 3 | ~22 fields vendor, ship mode, EAN/UPC, import từ Excel hãng |

### 1.5 Tổng kết nhanh

```
ERPNext Buying Module          Nhật Minh Sport
──────────────────────         ──────────────────────
Material Request         ❌    → thay bằng Purchase Plan (Custom)
Supplier Quotation       ❌    → không dùng (NCC cố định)
RFQ / SQ Comparison      ❌    → không dùng
Purchase Order           ✅    + custom fields (ship_mode, vendor_po#...)
Purchase Receipt         ✅    + workflow duyệt 3 bước + customs fields
Purchase Invoice         ✅    dùng nguyên
Payment Entry            ✅    + workflow đề nghị TT 4 bước
Landed Cost Voucher      ✅    dùng nguyên
Debit Note (Return)      ✅    + workflow 2 bước
Subcontracting           ❌    → không sản xuất
Blanket Order            ❌    → không dùng
Auto Reorder             ❌    → KH mua hàng thủ công
Quality Inspection       ❌    → chỉ kiểm đếm
                               + Purchase Plan (NEW)
                               + Delivery Schedule (NEW)
```

---

## 2. Quy trình mua hàng (10 bước)

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 | REQ-PURCH-001

| Bước | Tên | Bộ phận | Mô tả |
|:----:|-----|---------|-------|
| 1 | Kế hoạch mua hàng | Mua hàng | Lập KH mua theo kỳ/năm, gửi NCC |
| 2 | Đơn hàng mua / HĐ mua | Mua hàng | Tạo PO, điều khoản TT & giao hàng |
| 3 | Kế hoạch giao hàng | Mua hàng | Cập nhật lịch giao khi nhận từ NCC |
| 4 | Đề nghị nhập hàng | Mua hàng | Thông báo kho chuẩn bị nhận hàng |
| 5 | Phiếu nhập mua / NK | Kế toán, Kho | Ghi nhận hàng nhập kho, công nợ |
| 6 | Chi phí mua hàng | Mua hàng | CP vận chuyển, bốc dỡ |
| 7 | Lệnh xuất trả lại NCC | Mua hàng | Lệnh trả hàng lỗi / không đạt |
| 8 | Phiếu xuất trả NCC | Kế toán, Kho | Xuất kho trả NCC |
| 9 | Xác nhận công nợ | Mua hàng | Đối chiếu công nợ với NCC |
| 10 | Đề nghị thanh toán | Mua hàng → KT | Lập đề nghị TT → KT chi |

---

## 3. Sơ đồ luồng dữ liệu

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2.0

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           QUY TRÌNH MUA HÀNG                                │
├─────────────────────────────────────┬───────────────────────────────────────┤
│           BP MUA HÀNG               │          BP KẾ TOÁN / KHO             │
├─────────────────────────────────────┼───────────────────────────────────────┤
│                                     │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 1. Kế hoạch mua hàng          │  │                                       │
│  └───────────────┬───────────────┘  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 2. Đơn hàng mua / HĐ mua     │  │                                       │
│  └───────────────┬───────────────┘  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 3. Kế hoạch giao hàng         │  │                                       │
│  └───────────────┬───────────────┘  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 4. Đề nghị nhập hàng          │──┼──▶ ┌─────────────────────────────┐   │
│  └───────────────────────────────┘  │    │ 5. Phiếu nhập mua / NK      │   │
│                                     │    └──────────────┬──────────────┘   │
│  ┌───────────────────────────────┐  │                   │                  │
│  │ 6. Chi phí mua hàng           │  │                   │                  │
│  └───────────────────────────────┘  │                   │                  │
│                                     │                   │                  │
│  ┌───────────────────────────────┐  │                   │                  │
│  │ 7. Lệnh xuất trả lại NCC     │──┼──▶ ┌─────────────────────────────┐   │
│  └───────────────────────────────┘  │    │ 8. Phiếu xuất trả NCC       │   │
│                                     │    └──────────────┬──────────────┘   │
│  ┌───────────────────────────────┐  │                   │                  │
│  │ 9. Xác nhận công nợ           │◀─┼───────────────────┘                  │
│  └───────────────┬───────────────┘  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │    ┌─────────────────────────────┐   │
│  │ 10. Đề nghị thanh toán        │──┼──▶ │ Phiếu chi / Báo nợ          │   │
│  └───────────────────────────────┘  │    └──────────────┬──────────────┘   │
│                                     │                   ▼                  │
│                                     │    ┌─────────────────────────────┐   │
│                                     │    │    Hệ thống báo cáo          │   │
│                                     │    └─────────────────────────────┘   │
└─────────────────────────────────────┴───────────────────────────────────────┘
```

---

## 4. Chi tiết từng bước

### Bước 1: Kế hoạch mua hàng

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 1 | REQ-PURCH-002

**Mục đích:** Bộ phận mua hàng cập nhật kế hoạch mua hàng gửi NCC.

**Thông tin cần có:**

| Nhóm | Trường |
|------|--------|
| Chung | Ngày, Số KH, NCC, Nội dung |
| Chi tiết | Mã VT, Tên VT, ĐVT, Loại mua (Demo/Purchase), Đơn giá, Family, Year, Category, Sub category, Shaft, Price, SL tháng 1-12 |

**Lịch đặt hàng:**

| Loại sản phẩm | Thời điểm đặt | MOQ |
|---------------|---------------|-----|
| Gậy năm mới | T9-10 | Theo hãng |
| Driver, FW, Rescue, Irons | Launch T1-2 | 10 pcs |
| Softgoods (US) | Hàng tháng | Theo hãng |
| Gậy P Series | 2 năm/lần | 1000+ |
| Putters / Wedges | Hàng năm | Theo hãng |
| Quần áo & PK (JP) | 2 lần/năm | Theo hãng |

### Bước 2: Đơn hàng mua / HĐ mua

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 2 | REQ-PURCH-003

**Thông tin cần có:**

| Trường | Bắt buộc | Mô tả |
|--------|:--------:|-------|
| Số PO | Tự động | PO Number theo hãng |
| NCC | Có | Chọn từ danh mục |
| Ngày đặt | Có | Ngày tạo PO |
| Kho nhận | Có | Kho dự kiến |
| Chi tiết SP | Có | Model, SKU, SL, Giá mua |
| Ship mode | | Sea / Air / Express |
| Confirm ship date | | Ngày NCC xác nhận giao |
| Điều khoản TT | | Điều kiện thanh toán |
| Điều khoản GH | | Điều kiện giao hàng |

**Tính năng:** Kế thừa từ kế hoạch mua hàng (mã hàng, đơn giá, thuộc tính).

### Bước 3: Kế hoạch giao hàng

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 3

**Thông tin chi tiết:** Mã VT, Tên VT chính thức, Tên VT theo danh mục NCC, Vendor name, PO Number, PO Create Date, Buyer name, Type, Product Group, Category, Location, Model, Stastic factor, Total Unit, Ship to, Month, Confirm ship date, Ship mode, EAN, UPC, PO comment, Remark, Số KH mua hàng, Số đơn đặt hàng

**Tính năng:**
- Kế thừa từ đơn đặt hàng
- **Cảnh báo** nếu tên VT chính thức khác với tên trên danh mục NCC

### Bước 4: Đề nghị nhập hàng

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 4

**Thông tin:** Ngày, Số lệnh, NCC, Kho, Tình trạng thông quan, Ngày dự kiến/thực tế thông quan. Chi tiết: Mã VT, SL, KH, liên kết B1-B3. Chi tiết lô: Số lot, Serial number, SL.

**Tính năng:** Kế thừa từ kế hoạch giao hàng.

### Bước 5: Phiếu nhập mua / NK

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 5 | REQ-PURCH-005

**Thông tin:** Ngày, Số phiếu, NCC, Tiền tệ, Kho, Số tờ khai. Chi tiết: Mã VT, SL, Đơn giá nhập, Thành tiền, Số lô, Seri, liên kết B1-B4, Đơn giá KH, Đơn giá ĐH.

**Tính năng:**
- Kế thừa từ lệnh nhập hàng
- **Cảnh báo nếu giá nhập khác giá đơn hàng**

**Trạng thái:** (Feature 3.1.16)
```
Nháp → Chờ duyệt → Đã nhập kho
```

### Bước 6: Chi phí mua hàng

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 6

Cập nhật chi phí vận chuyển, bốc dỡ.

### Bước 7-8: Trả hàng NCC

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 7-8

**Bước 7:** BP Mua hàng thống kê SP lỗi → Lập **lệnh xuất trả** → Chờ duyệt
**Bước 8:** Kế toán/Kho thực hiện **phiếu xuất trả** → Giảm kho + Giảm CN

### Bước 9: Xác nhận công nợ

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 9

Đối chiếu công nợ dựa trên phiếu nhập, phiếu trả, các khoản đã thanh toán.

### Bước 10: Đề nghị thanh toán

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2 Bước 10 | REQ-PURCH-006

**Thông tin:** Ngày đề nghị, Số đề nghị, Nội dung, NCC, Đơn hàng mua/HĐ mua, Giá trị đơn hàng, Đã tạm ứng, Giá trị thanh toán, Người lập, Hình thức TT.

**Theo dõi:** Chưa TT → TT một phần → Đã TT đủ

---

## 5. Danh mục NCC (Module 04)

> **Nguồn:** ERP_SPECIFICATION.md Section 3.0 | SPEC_MAPPING 04

### Feature 3.0.1: Danh mục NCC

- Mã NCC, Tên NCC, Nhóm NCC, Điều khoản TT
- Tạo/Sửa/Xóa, Phân loại theo nhóm
- Lịch sử giao dịch + công nợ

### Feature 3.0.2: Bảng giá NCC

- Giá theo model/SKU + Hiệu lực giá
- Làm cơ sở tính KM đầu vào

---

## 6. Tính năng mua hàng (18 features)

> **Nguồn:** ERP_SPECIFICATION.md Section 3.1

| # | Feature | Mô tả |
|---|---------|-------|
| 3.1.1 | Ưu đãi NCC | CK % + CK tiền + Quà tặng |
| 3.1.2 | Import hình ảnh SP | Import ảnh theo model + Quy tắc đặt tên |
| 3.1.3 | Tạo PO | PO Number (auto) + NCC + Kho nhận + Ngày đặt |
| 3.1.4 | Chi tiết PO | Model + SKU + SL + Giá mua |
| 3.1.5 | Theo dõi PO | Nháp → Đã gửi NCC → Đang giao → Hoàn thành |
| 3.1.6 | Lệnh nhập hàng | Sinh từ PO + Nhập 1 phần / nhiều lần |
| 3.1.7 | Theo dõi thực hiện | Đã đặt + Đã nhận 1 phần (%) + Đã nhận đủ |
| 3.1.8 | Nhập theo lô | Mã lô + Ngày nhập + Gắn PO |
| 3.1.9 | Nhập theo serial | Serial duy nhất + Scan |
| 3.1.10 | Nhập theo mã vạch | Gán barcode + Quét nhập kho |
| 3.1.11 | Vòng đời SP | 6 tháng / 1 năm / 2 năm |
| 3.1.12 | Nguồn tiền | Quỹ TM / TK ngân hàng |
| 3.1.13 | Phương thức TT | TM + CK + Công nợ |
| 3.1.14 | Theo dõi TT PO | Đã TT + 1 phần + Còn nợ |
| 3.1.15 | Đính kèm chứng từ | HĐ NCC + Phiếu giao + HĐ |
| 3.1.16 | Trạng thái phiếu nhập | Nháp + Chờ duyệt + Đã nhập kho |
| 3.1.17 | Lịch sử mua hàng | Theo NCC + PO + SP |
| 3.1.18 | BC mua hàng | Giá BQ + NCC tốt nhất + CP mua |

---

## 7. Trạng thái đơn hàng mua (PO)

> **Nguồn:** Feature 3.1.5 | REQ-PURCH-004

```
Nháp → Đã gửi NCC → Đang giao → Nhận một phần → Hoàn thành
                                                    Hủy
```

---

## 8. Nhập hàng: Lô, Serial, Mã vạch

> **Nguồn:** Features 3.1.8, 3.1.9, 3.1.10

| Loại | Thông tin |
|------|----------|
| Lô (3.1.8) | Mã lô, Ngày nhập, Gắn với PO |
| Serial (3.1.9) | Serial duy nhất, Scan serial khi nhập |
| Mã vạch (3.1.10) | Gán barcode cho SP/serial, Nhập kho bằng quét |

---

## 9. Trả hàng NCC

> **Nguồn:** Section 3.2 Bước 7-8

```
B7: Lệnh xuất trả (BP Mua hàng) → Chờ duyệt → Approved
B8: Phiếu xuất trả (KT/Kho) → Giảm kho + Giảm CN
```

---

## 10. Thanh toán NCC

> **Nguồn:** Features 3.1.12, 3.1.13, 3.1.14, Bước 9-10

| Phương thức | Mô tả |
|------------|-------|
| Tiền mặt | Chi TM từ quỹ |
| Chuyển khoản | CK ngân hàng |
| Công nợ | Ghi nhận, TT sau |

**Theo dõi:** Chưa TT → TT 1 phần → Đã TT đủ

---

## 11. Báo cáo mua hàng (Module 06)

> **Nguồn:** Features 3.1.17, 3.1.18 + Module 06 SPEC_MAPPING

### Lịch sử mua hàng (3.1.17)

| Góc nhìn | Mô tả |
|----------|-------|
| Theo NCC | Tất cả đơn hàng 1 NCC |
| Theo PO | Chi tiết 1 đơn hàng |
| Theo SP | Lịch sử mua 1 SP qua các NCC |

### BC phân tích (3.1.18)

| Báo cáo | Mô tả |
|---------|-------|
| Giá mua bình quân | Giá TB theo item, theo kỳ |
| NCC tốt nhất | Xếp hạng NCC |
| Chi phí mua hàng | Tổng hợp CP mua theo kỳ |

### BC quản trị

| Báo cáo | Mô tả |
|---------|-------|
| So sánh KH mua vs Đơn hàng | Kế hoạch vs PO thực tế, % hoàn thành |

### BC từ Module 06

| Báo cáo | Feature | Mô tả |
|---------|---------|-------|
| Hàng tồn chậm | 6.3.1 | Bán chậm + Đề xuất sale/điều chuyển |
| Hàng sắp hết vòng đời | 6.3.2 | Còn 60 ngày / 45 ngày |
| Hàng điều chuyển | 6.3.3 | Giữa kho + cho đại lý |
| Hàng thanh lý / sale | 6.3.4 | Campaign + Thanh lý |

---

## 12. KT Mua hàng (Module 24)

> **Nguồn:** DCNET_SRS_NM.md Section 3.24
> **Lưu ý:** Module 24 chưa có SPEC_MAPPING chi tiết. Thông tin dưới đây từ SRS.

**Tính năng chính:**
- Hạch toán hóa đơn mua hàng trong nước
- Hạch toán hóa đơn nhập khẩu (CP vận chuyển, thuế NK)
- Đối chiếu hóa đơn mua với phiếu nhập kho
- Ghi nhận chiết khấu mua hàng

> Chi tiết sẽ bổ sung khi có SPEC_MAPPING cho module 24.
> Tham khảo kỹ thuật GL Entry → xem `erpnext.md` cùng folder.

---

## 13. Vấn đề cần xác nhận với khách

> **Nguồn:** docs/modules/05-mua-hang/CLARIFY.md

| # | Vấn đề | Mức độ |
|---|--------|:------:|
| 1 | Quy tắc đặt tên ảnh: `{item_code}.jpg` hay `{model}_{sku}.jpg`? | Cao |
| 2 | Scan barcode: quét mã item hay quét từng serial? | Cao |
| 3 | Vòng đời SP: shelf life hay product end-of-life? | TB |
| 4 | Trạng thái PO: Workflow hay field Select? | TB |
| 5 | **Duyệt phiếu nhập: Ai duyệt? Tất cả hay theo ngưỡng?** | **Cao** |
| 6 | **KH mua hàng: DocType riêng hay extend MR?** | **Cao** |
| 7 | **KH giao hàng: DocType riêng hay extend PO?** | **Cao** |
| 8 | **Đề nghị nhập hàng: chứng từ riêng hay dùng PR?** | **Cao** |
| 9 | Trả hàng: 2 bước hay 1 bước? | TB |
| 10 | Đề nghị TT: DocType riêng hay Workflow trên PE? | TB |
| 11 | KH giao hàng: Import tự động từ Excel NCC? | TB |
| 12 | So sánh tên VT: Exact match hay fuzzy? | Thấp |
| 13 | Pre-order đại lý + tracking vận chuyển: T3 hay sau? | **Cao** |

---

> **Last Updated:** 17/03/2026
> **Nguồn specs:** ERP_SPECIFICATION.md Section 3 | DCNET_SRS_NM.md Section 3.5
> **BA Analysis:** `analysis/BA_ANALYSIS.md`
> **ERPNext reference:** `workflow/erpnext.md`
