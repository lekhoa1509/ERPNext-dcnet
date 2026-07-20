# PHÂN TÍCH QUY TRÌNH ERP - THĂNG LONG TM & NHẬT MINH
## So sánh với ERPNext v15 chuẩn

**Dự án:** Triển khai ERPNext cho Thăng Long TM & Nhật Minh
**Đơn vị thực hiện:** DCNET
**Ngày phân tích:** 16/03/2026

---

## MỤC LỤC

1. [Tổng quan hệ thống](#1-tổng-quan)
2. [Module Mua Hàng](#2-module-mua-hàng)
3. [Module Bán Hàng](#3-module-bán-hàng)
4. [Module Kế Toán](#4-module-kế-toán)
5. [Module Kho](#5-module-kho)
6. [Ma trận Gap Analysis](#6-gap-analysis)
7. [Khuyến nghị tùy chỉnh](#7-khuyến-nghị)

---

## 1. TỔNG QUAN

### 1.1 Mô hình kinh doanh
| Thực thể | Vai trò | Ghi chú |
|----------|---------|---------|
| Thăng Long TM | Nhà phân phối độc quyền TaylorMade tại VN | Công ty mẹ |
| Nhật Minh | Đại lý cấp 1 của TM | Công ty con / liên kết |
| Đại lý khác | Đại lý cấp 1 và cấp 2 | Khách hàng B2B |

### 1.2 Nhóm sản phẩm chính
- **Gậy golf:** Driver/FW/Rescue/Iron/Putter/Wedge/P Series
- **Quần áo & phụ kiện:** Dòng US (monthly) + Dòng JP (2 lần/năm)
- **Dịch vụ:** Fitting, Coaching, Trade-in

### 1.3 Kiến trúc ERPNext đề xuất
- **2 Company riêng biệt:** Thăng Long TM + Nhật Minh (multi-company)
- **Intercompany Transaction:** TM → Nhật Minh
- **Shared Masters:** Item, Supplier (một số)
- **Separate:** Chart of Accounts, Warehouse, Reports

---

## 2. MODULE MUA HÀNG

### 2.1 Quy trình chuẩn ERPNext v15

```
Material Request → Request for Quotation → Supplier Quotation
→ Purchase Order → Purchase Receipt → Purchase Invoice → Payment Entry
```

**Các điểm quan trọng ERPNext v15:**
- PO có thể tạo nhiều PR (nhận hàng nhiều đợt từ 1 PO)
- PR ảnh hưởng kho (Stock Ledger)
- PI ảnh hưởng công nợ + thuế (Accounts Payable + VAT 1331)
- PI có thể tích hợp PR ("Update Stock" flag = vừa nhận hàng vừa tạo hóa đơn)
- Landed Cost Voucher: phân bổ phí vận chuyển, thuế nhập khẩu vào giá vốn

### 2.2 Quy trình thực tế của Thăng Long TM (từ tài liệu)

#### Quy trình nhập hàng TM (Import từ TaylorMade)

```
[1] Nhận catalog mùa mới
       ↓
[2] Họp đánh giá sản phẩm (GĐ Kinh Doanh + Marketing + Kỹ Thuật + Thời Trang)
       ↓
[3] Nhận Order Form từ nhà cung cấp
       ↓
[4] Tổng hợp danh sách hàng pre-order (theo từng dòng sản phẩm)
       ↓
[5] GĐ Kinh Doanh duyệt → trình Ban Lãnh Đạo
       ↓
[6] Gửi Order cho nhà cung cấp
       ↓
[7] Nhà cung cấp xác nhận / từ chối đơn hàng
       ↓
[8] Nhà cung cấp gửi lịch giao hàng (trước 1 tháng)
       ↓
[9] BP Nhập hàng tạo PO theo từng lô hàng
       ↓
[10] Phối hợp Forwarder/Logistics (vận chuyển, hải quan)
       ↓
[11] BP Kế Toán khai báo thuế (thuế nhập khẩu, VAT)
       ↓
[12] Marketing hoàn thiện catalog + bảng giá
       ↓
[13] Nhận hàng: Kho + Kế Toán + BP Nhập cùng kiểm tra số lượng
       ↓
[14] Xử lý sai lệch (thiếu/hỏng/sai hàng) trong vòng 1 ngày
       ↓
[15] Lưu hồ sơ: biên bản, email, công văn
```

#### Quy trình đặt hàng từ Đại lý (Nhật Minh → TM)

```
[1] Họp đề xuất nhập hàng với TM (dựa trên báo cáo bán hàng + xu hướng thị trường)
       ↓
[2] Trải nghiệm sản phẩm mẫu (đại diện TM thăm)
       ↓
[3] Nhận Order Form + catalog từ TM
       ↓
[4] Đặt hàng theo lịch (xem bảng bên dưới)
       ↓
[5] Ký hợp đồng vận chuyển với TM
       ↓
[6] Nhận hàng từng lô (theo tồn kho thực tế TM)
       ↓
[7] Kiểm tra hàng trong vòng 1 ngày
       ↓
[8] Thanh toán theo điều khoản hợp đồng
```

#### Lịch đặt hàng cố định

| Dòng sản phẩm | Tần suất | Thời điểm đặt | MOQ | Ghi chú |
|---------------|----------|---------------|-----|---------|
| Gậy (năm sau) | Hàng năm | Tháng 9-10 | 10 cái | Đặt trước 3 tháng |
| Driver/FW/Rescue/Iron | Hàng năm | Tháng 1-2 | 10 cái | - |
| Softgoods (US) | Hàng tháng | Theo tháng | Pool MOQ | - |
| Gậy P Series | 2 năm/lần | 3 tháng trước | - | Có thể chuyển sang hàng năm |
| Putter | Hàng năm | 3 tháng trước launch | - | - |
| Wedge | Hàng năm | 3 tháng trước launch | - | - |
| Quần áo/Phụ kiện (JP) | 2 lần/năm | Tháng 6-7 (SS), Tháng 11-12 (FW) | - | Spring/Summer, Fall/Winter |
| Đơn hàng đặc biệt | Theo yêu cầu | - | 1.000-3.000 cái | Lead time 3-6 tháng |

### 2.3 So sánh & Gap Analysis - Mua Hàng

| Tính năng | ERPNext v15 Chuẩn | Yêu cầu TM/NM | Trạng thái | Hành động |
|-----------|-------------------|----------------|------------|-----------|
| Material Request | Có | Cần (đánh giá sản phẩm, pre-order) | Dùng được | Tùy chỉnh workflow approval |
| Request for Quotation | Có | Ít dùng (supplier cố định) | Tùy chọn | Bỏ qua nếu không cần |
| Supplier Quotation | Có | Không rõ yêu cầu | Tùy chọn | - |
| Purchase Order | Có | **Có - Core** | Dùng được | Thêm trường "Lô hàng", "Mùa vụ" |
| PO nhiều đợt nhận hàng | Có (1 PO → nhiều PR) | **Bắt buộc** | Dùng được | Cấu hình đúng |
| Purchase Receipt | Có | **Có - Core** | Dùng được | Thêm kiểm tra chất lượng |
| Purchase Invoice | Có | **Có - Core** | Dùng được | Tách hóa đơn CIF/FOB |
| Landed Cost Voucher | Có | **Bắt buộc** (thuế NK, phí vận) | Dùng được | Mapping đúng tài khoản VAS |
| Payment Entry | Có | **Có - Core** | Dùng được | Thêm theo dõi công nợ nhà CC |
| Lịch đặt hàng cố định | Không có sẵn | **Cần** | Thiếu | Tùy chỉnh / reminder tự động |
| Phê duyệt đa cấp | Có (Workflow) | **Cần** (GĐ → BLĐ) | Dùng được | Cấu hình Workflow |
| Tracking đơn hàng theo lô | Không có sẵn | **Cần** (nhiều lô từ 1 PO) | Thiếu | Dùng Batch tracking hoặc Custom Field |
| Biên bản giao nhận | Không có sẵn | **Cần** | Thiếu | Tạo Print Format tùy chỉnh |
| Xử lý hàng lỗi/sai | Có (Purchase Return) | **Cần** | Dùng được | Cấu hình thêm |

---

## 3. MODULE BÁN HÀNG

### 3.1 Quy trình chuẩn ERPNext v15

```
Lead → Opportunity → Quotation → Sales Order
→ Delivery Note → Sales Invoice → Payment Entry
```

**Các điểm quan trọng ERPNext v15:**
- Pricing Rules: Giá theo nhóm khách hàng, mùa vụ, số lượng
- Commission: Tính hoa hồng theo Sales Person
- Credit Limit: Kiểm tra hạn mức tín dụng khách hàng
- Delivery Note tách từ SO (giao nhiều đợt)
- Return/Credit Note cho hàng trả lại

### 3.2 Quy trình thực tế TM/NM

#### Kênh bán hàng

```
Bán buôn (B2B):
TM → Đại lý cấp 1 (Nhật Minh + đại lý khác)
TM/NM → Đại lý cấp 2

Bán lẻ (B2C):
TM/NM → Khách hàng cá nhân
NM → Khách hàng qua Shopee/TikTok/Lazada

Dịch vụ:
NM → Fitting service
NM → Coaching service
TM/NM → Trade-in
```

#### Quy trình bán lẻ/đại lý chuẩn

```
[1] Tạo đơn hàng (Sales Order)
       ↓
[2] Kiểm tra tồn kho
       ↓
[3] Kiểm tra hạn mức tín dụng
       ↓
[4] Kiểm tra công nợ quá hạn
       ↓    ↓ (không đạt điều kiện)
[5] Hủy đơn ← ←
       ↓ (đạt điều kiện)
[6] Tạo lệnh xuất kho (Delivery Note)
       ↓
[7] Xuất hóa đơn bán hàng (Sales Invoice)
       ↓
[8] Thu tiền (Payment Entry)
```

#### Quy trình Fitting (từ tài liệu CRM)

```
[1] Tạo Fitting Order (từ website / trung tâm / điện thoại)
    - Mã: FIT-YYYY-MM-DD-XX
    - Trạng thái: Mới → Đã xác nhận → Đang Fitting → Hoàn thành → Follow-up / Hủy
       ↓
[2] Xác nhận lịch hẹn
       ↓
[3] Khách đến
       ↓
[4] Kiểm tra tình trạng gậy, tư vấn khách
       ↓
[5] Khách hủy? → Lead follow-up (tự động chuyển sang Lead)
       ↓
[6] Khách đồng ý → Tạo Sales Order
       ↓
[7] Kiểm tra tồn kho
       ↓
[8] Xuất kho
       ↓
[9] Kiểm tra hạn mức tín dụng
       ↓
[10] Kiểm tra công nợ quá hạn
        ↓
[11] Hủy đơn nếu không đạt ← ←
        ↓
[12] Xuất hóa đơn bán hàng
        ↓
[13] Tính hoa hồng nhân viên
```

**Thông tin Fitting Order cần lưu:**
- Thông số kỹ thuật: tốc độ bóng, khoảng cách, đường bay bóng, swing path, smash factor
- Loại gậy cần fitting/sửa chữa
- Nhân viên phụ trách fitting
- Nguồn lead (walk-in, website, referral...)

#### Quy trình Coaching (từ tài liệu CRM)

```
[1] Đăng ký khóa học
    - Mã: COA-YYYY-MM-DD-XX
    - Trạng thái: Mới → Đã kiểm tra → Đã tư vấn → Đã thanh toán → Đang học → Tạm dừng → Hoàn thành → Hủy
       ↓
[2] Kiểm tra trình độ đầu vào
       ↓
[3] Đánh giá & tư vấn
       ↓
[4] Khách hủy? → Lead follow-up
       ↓
[5] Khách đồng ý → Tạo Sales Order
       ↓
[6] Thanh toán & ký hợp đồng
       ↓
[7] Xếp lịch học
       ↓
[8] Giảng dạy & điểm danh
       ↓
[9] Kết thúc khóa học
       ↓
[10] Chăm sóc sau khóa học
        ↓
[11] Xuất hóa đơn
        ↓
[12] Tính hoa hồng & chiết khấu
```

**Thông tin Coaching Order cần lưu:**
- Học viên, Gói tập, HLV phụ trách
- Lịch học, Học phí, Chiết khấu, Địa điểm
- Loại khóa: Mới tập / Trung cấp / Nâng cao

### 3.3 So sánh & Gap Analysis - Bán Hàng

| Tính năng | ERPNext v15 Chuẩn | Yêu cầu TM/NM | Trạng thái | Hành động |
|-----------|-------------------|----------------|------------|-----------|
| Sales Order | Có | **Có - Core** | Dùng được | Thêm trường "Loại đơn hàng" |
| Quotation | Có | Cần cho B2B | Dùng được | - |
| Pricing Rules | Có | **Bắt buộc** (đại lý, mùa, SL) | Dùng được | Cấu hình theo tier đại lý |
| Credit Limit Check | Có | **Bắt buộc** | Dùng được | Cấu hình theo từng khách |
| Delivery Note | Có | **Có - Core** | Dùng được | - |
| Sales Invoice | Có | **Có - Core** | Dùng được | Thêm thông tin thuế VAT |
| Payment Entry | Có | **Có - Core** | Dùng được | - |
| Commission | Có (Sales Person) | **Cần** | Dùng được | Cấu hình Sales Team + Commission |
| Return/Credit Note | Có | **Cần** | Dùng được | - |
| Fitting Order (CRM) | Không có sẵn | **Bắt buộc** | Thiếu | **Tạo Custom DocType "Fitting Order"** |
| Coaching Order (CRM) | Không có sẵn | **Bắt buộc** | Thiếu | **Tạo Custom DocType "Coaching Order"** |
| Membership Module | Không có sẵn | **Cần** | Thiếu | **Tạo Module Membership** |
| Trade-in | Không có sẵn | **Cần** | Thiếu | Dùng Stock Entry + Credit Note |
| Lead → Fitting auto | Không có sẵn | **Cần** | Thiếu | Custom Workflow + Script |
| Tích hợp Shopee/TikTok/Lazada | Không có sẵn | **Cần (Phase 2)** | Thiếu | API Integration (Phase 2) |
| Giao nhiều đợt từ 1 SO | Có | **Cần** | Dùng được | - |
| Kiểm tra công nợ quá hạn | Partial (có cảnh báo) | **Bắt buộc** | Cần cải thiện | Custom validation script |
| Tự động tạo mã đơn | Có (naming series) | **Bắt buộc** (FIT-/COA-) | Dùng được | Cấu hình Naming Series |

---

## 4. MODULE KẾ TOÁN

### 4.1 Quy trình chuẩn ERPNext v15

**Hệ thống tài khoản:**
- Chart of Accounts (CoA) theo chuẩn VAS (Việt Nam Accounting Standard)
- Cost Center để phân bổ chi phí
- Fiscal Year: 01/01 - 31/12

**Luồng ghi sổ chính:**

| Giao dịch | Nợ | Có |
|-----------|-----|-----|
| Purchase Receipt | 1561 (Hàng tồn kho) | 331 (Phải trả NCC) |
| Purchase Invoice (có thuế) | 1561 + 1331 (VAT vào) | 331 |
| Payment to Supplier | 331 | 1111/1121 (Tiền mặt/NH) |
| Sales Invoice | 131 (Phải thu KH) | 511 + 3331 (Doanh thu + VAT ra) |
| Payment from Customer | 1111/1121 | 131 |
| Landed Cost | 1561 | 3333/627/... (tài khoản phí) |

### 4.2 Yêu cầu kế toán TM/NM

#### Yêu cầu từ tài liệu

1. **Kế toán tách biệt** TM và Nhật Minh (2 pháp nhân riêng)
2. **Báo cáo chi tiết** theo:
   - Sản phẩm, nhóm sản phẩm
   - Đại lý
   - Thời gian (tháng, quý, năm)
   - Tình trạng thanh toán (đã TT, chưa TT, quá hạn)
3. **Theo dõi dòng tiền** chi tiết
4. **Thuế nhập khẩu** và VAT nhập khẩu
5. **Công nợ phải thu** theo đại lý với aging report
6. **Hoa hồng nhân viên** (Fitting, Coaching, Sales)

#### Các tài khoản quan trọng cần mapping (VAS)

| Tài khoản | Tên | Sử dụng trong |
|-----------|-----|----------------|
| 111 | Tiền mặt | Payment Entry |
| 112 | Tiền gửi ngân hàng | Payment Entry |
| 131 | Phải thu khách hàng | Sales Invoice |
| 133 (1331, 1332) | Thuế GTGT đầu vào | Purchase Invoice |
| 156 (1561, 1562) | Hàng hóa tồn kho | Stock |
| 331 | Phải trả người bán | Purchase Invoice |
| 333 (3331, 3333) | Thuế GTGT đầu ra, thuế NK | Sales Invoice, Landed Cost |
| 511 | Doanh thu bán hàng | Sales Invoice |
| 632 | Giá vốn hàng bán | Sales Invoice (COGS) |
| 641, 642 | Chi phí BH, QLDN | Journal Entry |

### 4.3 So sánh & Gap Analysis - Kế Toán

| Tính năng | ERPNext v15 Chuẩn | Yêu cầu TM/NM | Trạng thái | Hành động |
|-----------|-------------------|----------------|------------|-----------|
| Multi-company accounting | Có | **Bắt buộc** (TM + NM) | Dùng được | Cấu hình 2 Company |
| Intercompany transaction | Có | **Cần** (TM → NM) | Dùng được | Cấu hình Intercompany |
| Chart of Accounts VAS | Partial (cần import) | **Bắt buộc** | Cần thiết lập | Import CoA chuẩn VAS |
| Cost Center | Có | **Cần** (phân theo bộ phận) | Dùng được | Cấu hình theo phòng ban |
| VAT (thuế GTGT) | Có | **Bắt buộc** | Dùng được | Cấu hình Tax Template |
| Import Duty (thuế NK) | Có qua Landed Cost | **Bắt buộc** | Dùng được | Cấu hình Landed Cost |
| Accounts Payable Aging | Có | **Cần** | Dùng được | - |
| Accounts Receivable Aging | Có | **Bắt buộc** | Dùng được | - |
| Cash Flow Statement | Có | **Bắt buộc** | Dùng được | Mapping đúng |
| Balance Sheet | Có | **Cần** | Dùng được | - |
| P&L Statement | Có | **Cần** | Dùng được | - |
| Payment Terms | Có | **Bắt buộc** | Dùng được | Cấu hình theo từng đại lý |
| Journal Entry | Có | **Cần** | Dùng được | - |
| Báo cáo dòng tiền tracking | Partial | **Bắt buộc** | Cần cải thiện | Custom Report |
| Báo cáo tình trạng TT | Partial | **Bắt buộc** | Cần cải thiện | Custom Report |
| Hoa hồng nhân viên | Có (Commission) | **Cần** | Dùng được | Liên kết với Sales Person |
| E-invoice (Hóa đơn điện tử) | Plugin available | **Bắt buộc** (VN pháp lý) | Cần plugin | Tích hợp VNPT/MISA |

---

## 5. MODULE KHO

### 5.1 Quy trình chuẩn ERPNext v15

**Các loại giao dịch kho:**
- **Stock Entry:** Material Issue, Material Receipt, Material Transfer, Manufacture
- **Purchase Receipt → Stock Ledger** (nhập kho từ mua hàng)
- **Delivery Note → Stock Ledger** (xuất kho từ bán hàng)
- **Stock Reconciliation:** Kiểm kê định kỳ
- **Batch Tracking:** Theo dõi theo lô (hạn sử dụng, số lô)
- **Serial Number:** Theo dõi từng item riêng lẻ (thiết bị, gậy golf từng chiếc)
- **Reorder Level:** Cảnh báo tồn kho thấp

**Phương pháp định giá:**
- FIFO (First In First Out) - Phù hợp ngành golf
- Moving Average - Dễ quản lý
- Standard (không khuyến nghị với golf)

### 5.2 Yêu cầu kho TM/NM

#### Đặc điểm hàng hóa golf

1. **Thuộc tính phức tạp:**
   - Gậy: loại gậy, thương hiệu, model, shaft material (graphite/steel), flex, loft, lie angle, màu sắc
   - Quần áo: size, màu sắc, chất liệu, tay áo, mùa vụ (SS/FW)
   - Phụ kiện: loại, màu sắc

2. **Quản lý theo mùa vụ (Season):**
   - Hàng mùa xuân/hè khác mùa thu/đông
   - Cần phân biệt trong kho và báo cáo

3. **Đặc điểm nhập kho:**
   - Hàng về nhiều đợt từ 1 PO
   - Cần kiểm tra từng lô với biên bản giao nhận

4. **Kho TM và Kho NM tách biệt**

5. **Báo cáo kho yêu cầu (từ danh sách báo cáo):**
   - Nhập-Xuất-Tồn chi tiết (3 dạng: số lượng / giá trị / cả hai)
   - Tóm tắt tồn kho theo năm / nhóm hàng
   - Phân bổ hàng trước khi nhập (pre-allocation)
   - Theo dõi hàng chậm/nhanh luân chuyển

#### Luồng kho trong quy trình TM

```
Nhập kho từ nước ngoài:
Purchase Order → Purchase Receipt (nhập kho TM) → [kiểm tra] → Stock OK

Xuất kho sang Nhật Minh:
Stock Transfer (TM Warehouse → NM Warehouse)  [Intercompany]
HOẶC: TM Sales Invoice → NM Purchase Receipt

Xuất kho bán lẻ:
Sales Order → Delivery Note → Kho giảm → Sales Invoice

Xuất kho Fitting:
Fitting Order → Sales Order → Delivery Note (xuất gậy fitting)

Điều chỉnh kho:
Stock Reconciliation (kiểm kê định kỳ)
Stock Entry - Material Receipt (nhập bổ sung)
Stock Entry - Material Issue (xuất sử dụng nội bộ)
```

### 5.3 So sánh & Gap Analysis - Kho

| Tính năng | ERPNext v15 Chuẩn | Yêu cầu TM/NM | Trạng thái | Hành động |
|-----------|-------------------|----------------|------------|-----------|
| Multi-warehouse | Có | **Bắt buộc** (TM + NM tách biệt) | Dùng được | Cấu hình Warehouse tree |
| Item Variants (thuộc tính) | Có | **Bắt buộc** (size, màu, flex...) | Dùng được | Cấu hình Item Attributes |
| Item Variant - Gậy golf | Có | **Cần nhiều attributes** | Dùng được | Cấu hình attributes: loại gậy, shaft, flex, loft... |
| Item Variant - Quần áo | Có | **Cần**: size, màu, chất liệu, mùa | Dùng được | Cấu hình attributes |
| Batch Tracking | Có | **Cần** (theo lô nhập) | Dùng được | Enable Batch No |
| Serial Number | Có | **Cần cho gậy cao cấp** | Dùng được | Enable Serial No cho gậy đơn lẻ |
| Stock Entry | Có | **Có - Core** | Dùng được | - |
| Stock Reconciliation | Có | **Cần** (kiểm kê định kỳ) | Dùng được | - |
| Reorder Level | Có | **Cần** | Dùng được | Cấu hình theo từng item |
| Stock Ledger Report | Có | **Bắt buộc** | Dùng được | - |
| Stock Balance Report | Có | **Bắt buộc** | Dùng được | - |
| Intercompany Stock Transfer | Có | **Bắt buộc** (TM → NM) | Dùng được | Cấu hình Intercompany |
| Phân bổ hàng trước nhập | Không có sẵn | **Cần** | Thiếu | Custom Report / Reserved Qty |
| Nhập-Xuất-Tồn (VN format) | Partial | **Bắt buộc** | Cần tùy chỉnh | Custom Stock Ledger Report |
| Biên bản kiểm nhận | Không có sẵn | **Cần** | Thiếu | Custom Print Format |
| Mùa vụ (Season) tracking | Không có sẵn | **Cần** | Thiếu | Custom Field trên Item/Batch |
| Hàng chậm/nhanh luân chuyển | Partial | **Cần** | Cần cải thiện | Custom Report |
| Định giá FIFO | Có | **Khuyến nghị** | Dùng được | Cấu hình Valuation Method |

---

## 6. MA TRẬN GAP ANALYSIS TỔNG HỢP

### 6.1 Phân loại theo độ ưu tiên

#### Ưu tiên 1 - Cấu hình chuẩn ERPNext (Không cần code)
| # | Hạng mục | Module | Thời gian ước tính |
|---|----------|--------|---------------------|
| 1 | Thiết lập 2 Company (TM + NM) | Chung | 0.5 ngày |
| 2 | Import Chart of Accounts VAS | Kế toán | 1 ngày |
| 3 | Cấu hình Warehouse tree | Kho | 0.5 ngày |
| 4 | Cấu hình Item Attributes (gậy, quần áo) | Kho | 2 ngày |
| 5 | Cấu hình Item Variants | Kho | 2 ngày |
| 6 | Cấu hình Tax Templates (VAT in/out) | Kế toán | 1 ngày |
| 7 | Cấu hình Payment Terms per Dealer | Kế toán | 0.5 ngày |
| 8 | Cấu hình Pricing Rules | Bán hàng | 1 ngày |
| 9 | Cấu hình Credit Limit per Customer | Bán hàng | 0.5 ngày |
| 10 | Cấu hình Naming Series (FIT-, COA-, v.v.) | Chung | 0.5 ngày |
| 11 | Cấu hình Workflow phê duyệt PO/SO | Mua/Bán | 2 ngày |
| 12 | Cấu hình Landed Cost Voucher | Mua hàng | 1 ngày |
| 13 | Cấu hình Intercompany transactions | Chung | 2 ngày |
| 14 | Cấu hình Sales Person + Commission | Bán hàng | 1 ngày |
| 15 | Cấu hình Batch/Serial Number tracking | Kho | 1 ngày |
| **Tổng** | | | **~16 ngày** |

#### Ưu tiên 2 - Tùy chỉnh Print Format & Report
| # | Hạng mục | Module | Thời gian ước tính |
|---|----------|--------|---------------------|
| 1 | Báo cáo Nhập-Xuất-Tồn format VN | Kho | 3 ngày |
| 2 | Báo cáo Công nợ phải thu theo đại lý | Kế toán | 2 ngày |
| 3 | Báo cáo Dòng tiền chi tiết | Kế toán | 3 ngày |
| 4 | Báo cáo Tổng hợp tồn kho | Kho | 2 ngày |
| 5 | Báo cáo Theo dõi đơn hàng Gậy/Quần áo | Mua hàng | 2 ngày |
| 6 | Báo cáo Bán hàng theo đại lý | Bán hàng | 2 ngày |
| 7 | Báo cáo Nhập khẩu - Kế hoạch vs Thực tế | Mua hàng | 2 ngày |
| 8 | Báo cáo Dự báo nhập-bán | Mua hàng | 3 ngày |
| 9 | Biên bản kiểm nhận hàng (Print Format) | Kho | 1 ngày |
| 10 | Print Format hóa đơn chuẩn VN | Kế toán | 2 ngày |
| **Tổng** | | | **~22 ngày** |

#### Ưu tiên 3 - Tùy chỉnh Custom DocType (Cần code)
| # | Hạng mục | Module | Thời gian ước tính |
|---|----------|--------|---------------------|
| 1 | Custom DocType: Fitting Order | CRM/Bán hàng | 5 ngày |
| 2 | Custom DocType: Coaching Order | CRM/Bán hàng | 5 ngày |
| 3 | Custom DocType: Membership Package | CRM | 3 ngày |
| 4 | Custom Workflow: Lead → Fitting auto | CRM | 2 ngày |
| 5 | Custom Script: Kiểm tra công nợ quá hạn | Bán hàng | 2 ngày |
| 6 | Custom Field: Season, Lô hàng, Mùa vụ | Chung | 2 ngày |
| 7 | Custom: Lịch đặt hàng cố định / Reminder | Mua hàng | 3 ngày |
| 8 | Custom: Phân bổ hàng trước nhập | Kho | 3 ngày |
| **Tổng** | | | **~25 ngày** |

#### Ưu tiên 4 - Tích hợp bên ngoài (Phase 2)
| # | Hạng mục | Thời gian ước tính |
|---|----------|---------------------|
| 1 | Tích hợp Shopee API | 10 ngày |
| 2 | Tích hợp TikTok Shop API | 10 ngày |
| 3 | Tích hợp Lazada API | 8 ngày |
| 4 | Tích hợp E-invoice (VNPT/MISA) | 5 ngày |
| **Tổng** | | **~33 ngày** |

---

## 7. KHUYẾN NGHỊ VÀ KẾ HOẠCH TRIỂN KHAI

### 7.1 Kiến trúc đề xuất

```
ERPNext v15
├── Company: Thăng Long TM
│   ├── Warehouse: TM - Main
│   ├── Warehouse: TM - Showroom
│   └── Chart of Accounts: VAS (riêng TM)
│
└── Company: Nhật Minh
    ├── Warehouse: NM - Main
    ├── Warehouse: NM - Showroom
    └── Chart of Accounts: VAS (riêng NM)

Intercompany:
  TM → NM: Purchase/Sales Invoice tự động
```

### 7.2 Lộ trình triển khai (theo biên bản họp 30/01/2026)

#### Tháng 3-4: Module Mua-Bán-Kho (Ưu tiên 1)
- [x] Setup Company, CoA, Warehouse
- [x] Item Master + Variants (gậy, quần áo)
- [x] Quy trình mua hàng đầy đủ (MR → PO → PR → PI → PE)
- [x] Quy trình bán hàng đầy đủ (SO → DN → SI → PE)
- [x] Quy trình kho (Stock Entry, Reconciliation)
- [x] Báo cáo cơ bản (NXT, tồn kho)

#### Tháng 5: Module Kế Toán
- [ ] Chart of Accounts VAS hoàn chỉnh
- [ ] Tax configuration (VAT 8/10%, Thuế NK)
- [ ] Landed Cost Voucher
- [ ] Intercompany transactions TM ↔ NM
- [ ] Báo cáo tài chính cơ bản
- [ ] Theo dõi công nợ + dòng tiền

#### Tháng 6-7: Module CRM + Tích hợp
- [ ] Fitting Order module
- [ ] Coaching Order module
- [ ] Membership module
- [ ] Báo cáo nâng cao (15 báo cáo thống nhất)
- [ ] Kiểm thử tổng thể
- [ ] Training người dùng
- [ ] Go-live

#### Tháng 8+: Phase 2
- [ ] Tích hợp Shopee/TikTok/Lazada
- [ ] E-invoice
- [ ] Phân tích nâng cao / BI

### 7.3 Các điểm rủi ro cần lưu ý

1. **Item Variants phức tạp:** Gậy golf có rất nhiều combination thuộc tính. Cần thiết kế Item Template cẩn thận để tránh tạo quá nhiều variants.

2. **Intercompany:** Giao dịch TM → NM cần cấu hình cẩn thận để tránh double-counting doanh thu/chi phí.

3. **Hàng nhập nhiều đợt từ 1 PO:** ERPNext hỗ trợ tốt nhưng cần training để người dùng không tạo PO mới cho từng lô.

4. **Dữ liệu từ hệ thống cũ (Bravo):** Cần kế hoạch migration dữ liệu riêng.

5. **Phân quyền người dùng:** TM và NM có dữ liệu tách biệt, cần cấu hình Permission đúng để không xem được dữ liệu của nhau.

6. **Báo cáo 15 loại:** Một số báo cáo phức tạp (dự báo nhập-bán) cần thêm thời gian custom.

### 7.4 Cấu trúc Item Attributes gợi ý

**Gậy golf:**
```
Item Template: TaylorMade [Model] [Type]
Attributes:
  - Club Type: Driver / FW / Rescue / Iron / Wedge / Putter
  - Shaft Material: Graphite / Steel
  - Shaft Flex: Regular / Stiff / X-Stiff / Senior / Ladies
  - Loft: (text field)
  - Hand: Right / Left
  - Color: (list)
```

**Quần áo:**
```
Item Template: TM [Season] [Model]
Attributes:
  - Size: XS / S / M / L / XL / XXL
  - Color: (list)
  - Gender: Men / Women / Unisex
  - Season: SS2025 / FW2025 / SS2026 / FW2026
  - Fabric: (text field)
```

---

## PHỤ LỤC: MAPPING TÀI KHOẢN KẾ TOÁN VAS → ERPNext

| ERPNext Account Type | Tài khoản VAS | Tên tài khoản |
|---------------------|---------------|----------------|
| Cash | 1111 | Tiền mặt VNĐ |
| Bank | 1121 | Tiền gửi VNĐ |
| Receivable | 131 | Phải thu khách hàng |
| Tax Asset | 1331 | Thuế GTGT đầu vào được khấu trừ |
| Stock | 1561 | Giá mua hàng hóa |
| Stock | 1562 | Chi phí thu mua hàng hóa |
| Payable | 331 | Phải trả người bán |
| Tax Liability | 3331 | Thuế GTGT phải nộp |
| Tax Liability | 3333 | Thuế xuất nhập khẩu |
| Income | 511 | Doanh thu bán hàng và cung cấp DV |
| Cost of Goods Sold | 632 | Giá vốn hàng bán |
| Expense | 641 | Chi phí bán hàng |
| Expense | 642 | Chi phí quản lý doanh nghiệp |

---

*Tài liệu được tổng hợp từ: Biên bản họp 30/12/2025, 30/01/2026; Quy trình nhập hàng TM và Đại lý; Tính năng CRM Fitting-Coaching; Danh sách báo cáo thống nhất; Tính năng nội bộ DEV.*
