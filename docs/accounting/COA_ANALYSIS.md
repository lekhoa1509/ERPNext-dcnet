# Phân tích Hệ thống Tài khoản Kế toán Việt Nam cho ERPNext

> **Ngày phân tích:** 15/02/2026
> **File gốc:** `ChartOfAccountsImporter.csv` (từ khách hàng / download)
> **File đã sửa:** `ChartOfAccountsImporter_v2.csv` (trong cùng thư mục)
> **Chuẩn kế toán:** Thông tư 200/2014/TT-BTC
> **Áp dụng cho:** Thăng Long TM + Nhật Minh Sport (2 company riêng, cùng COA)

---

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Đánh giá đầy đủ theo TT200](#2-đánh-giá-đầy-đủ-theo-tt200)
3. [Lỗi ERPNext Account Type](#3-lỗi-erpnext-account-type)
4. [Lỗi Hierarchy (Parent-Child)](#4-lỗi-hierarchy-parent-child)
5. [Đối chiếu với Specs khách hàng (20 features)](#5-đối-chiếu-với-specs-khách-hàng-20-features)
6. [Phân tích theo nghiệp vụ đặc thù DCNET](#6-phân-tích-theo-nghiệp-vụ-đặc-thù-dcnet)
7. [Workflow kế toán trong ERPNext](#7-workflow-kế-toán-trong-erpnext)
8. [Danh sách sửa đổi (Changelog v1 → v2)](#8-danh-sách-sửa-đổi-changelog-v1--v2)
9. [Vấn đề cần Clarify với khách hàng](#9-vấn-đề-cần-clarify-với-khách-hàng)
10. [Hướng dẫn Import vào ERPNext](#10-hướng-dẫn-import-vào-erpnext)

---

## 1. Tổng quan

### 1.1. Thông tin file gốc

| Thông số | Giá trị |
|----------|---------|
| Tổng số dòng | 245 (1 header + 244 tài khoản) |
| Số TK cấp 1 (Root) | 9 loại (Loại 1 → Loại 9) |
| Số TK Group | 67 tài khoản (is_group=1) |
| Số TK Ledger | 177 tài khoản (is_group=0) |
| Đồng tiền | VND (chính), USD (3 TK ngoại tệ) |
| Chuẩn kế toán | Thông tư 200/2014/TT-BTC |

### 1.2. Kết quả đánh giá tổng quan

| Hạng mục | Đánh giá | Ghi chú |
|----------|----------|---------|
| Đầy đủ tài khoản TT200 | ✅ Đủ 9 loại, đủ TK chính | Thiếu vài TK chi tiết |
| Cấu trúc Parent-Child | ⚠️ 2 lỗi hierarchy | TK 2118, 3339 |
| ERPNext Account Type | ❌ Thiếu nhiều type quan trọng | 12+ TK cần sửa type |
| Phù hợp DCNET Flow | ⚠️ 65% trực tiếp | Cần bổ sung cho trade-in, tách DT buôn/lẻ |

### 1.3. Điểm số hỗ trợ 20 Features kế toán

| Kết quả | Số lượng | Tỷ lệ |
|---------|----------|--------|
| ✅ Hỗ trợ đầy đủ | 13 features | 65% |
| ⚠️ Hỗ trợ, cần sửa | 6 features | 30% |
| ❌ Thiếu hoàn toàn | 4 items | 5% |

---

## 2. Đánh giá đầy đủ theo TT200

### 2.1. Loại 1 - Tài sản ngắn hạn

| TK | Tên | Có trong COA | Chi tiết |
|----|-----|:------------:|----------|
| 111 | Tiền mặt | ✅ | 1111, 1112, 1113 |
| 112 | Tiền gửi Ngân hàng | ✅ | 1121, 1122, 1123 |
| 113 | Tiền đang chuyển | ✅ | 1131, 1132 |
| 121 | Chứng khoán kinh doanh | ✅ | 1211, 1212, 1218 |
| 128 | Đầu tư nắm giữ đến ngày đáo hạn | ✅ | 1281-1288 |
| 131 | Phải thu của khách hàng | ✅ | Ledger account |
| 133 | Thuế GTGT được khấu trừ | ✅ | 1331, 1332 |
| 136 | Phải thu nội bộ | ✅ | 1361-1368 |
| 138 | Phải thu khác | ✅ | 1381, 1385, 1388 |
| 141 | Tạm ứng | ✅ | Ledger account |
| 151 | Hàng mua đang đi đường | ✅ | Ledger account |
| 152 | Nguyên liệu, vật liệu | ✅ | Ledger account |
| 153 | Công cụ, dụng cụ | ✅ | 1531-1534 |
| 154 | CP SXKD dở dang | ✅ | Ledger account |
| 155 | Thành phẩm | ✅ | 1551, 1557 |
| 156 | Hàng hóa | ✅ | 1561, 1562, 1567 |
| 157 | Hàng gửi đi bán | ✅ | Ledger account |
| 158 | Hàng hóa kho bảo thuế | ✅ | Ledger account |
| 161 | Chi sự nghiệp | ✅ | 1611, 1612 |
| 171 | Giao dịch mua bán lại TPCP | ✅ | Ledger account |

**Đánh giá:** ✅ Đầy đủ

### 2.2. Loại 2 - Tài sản dài hạn

| TK | Tên | Có trong COA | Chi tiết |
|----|-----|:------------:|----------|
| 211 | TSCĐ hữu hình | ✅ | 2111-2115 + 2118 |
| 212 | TSCĐ thuê tài chính | ✅ | 2121, 2122 |
| 213 | TSCĐ vô hình | ✅ | 2131-2138 |
| 214 | Hao mòn TSCĐ | ✅ | 2141-2147 |
| 217 | Bất động sản đầu tư | ✅ | Ledger |
| 221 | Đầu tư vào CTy con | ✅ | Ledger |
| 222 | Đầu tư LK, liên doanh | ✅ | Ledger |
| 228 | Đầu tư khác | ✅ | 2281, 2288 |
| 229 | Dự phòng tổn thất TS | ✅ | 2291-2294 |
| 241 | XDCB dở dang | ✅ | 2411-2413 |
| 242 | Chi phí trả trước | ✅ | Ledger |
| 243 | TS thuế TNHL | ✅ | Ledger |
| 244 | Cầm cố, thế chấp | ✅ | Ledger |

**Đánh giá:** ✅ Đầy đủ

### 2.3. Loại 3 - Nợ phải trả

| TK | Tên | Có trong COA | Chi tiết |
|----|-----|:------------:|----------|
| 331 | Phải trả cho người bán | ✅ | Ledger |
| 333 | Thuế phải nộp NN | ✅ | 3331-3339 + chi tiết 33311, 33312, 33381, 33382 |
| 334 | Phải trả NLĐ | ✅ | 3341, 3348 |
| 335 | Chi phí phải trả | ✅ | Ledger |
| 336 | Phải trả nội bộ | ✅ | 3361-3368 |
| 337 | TT theo tiến độ HĐXD | ✅ | Ledger |
| 338 | Phải trả, phải nộp khác | ✅ | 3381-3388 |
| 341 | Vay và nợ thuê TC | ✅ | 3411, 3412 |
| 343 | Trái phiếu phát hành | ✅ | 3431, 3432 + chi tiết |
| 344 | Nhận ký quỹ, ký cược | ✅ | Ledger |
| 347 | Thuế TNHL phải trả | ✅ | Ledger |
| 352 | Dự phòng phải trả | ✅ | 3521-3524 |
| 353 | Quỹ khen thưởng, PL | ✅ | 3531-3534 |
| 356 | Quỹ PTKHCN | ✅ | 3561, 3562 |
| 357 | Quỹ bình ổn giá | ✅ | Ledger |

**Đánh giá:** ✅ Đầy đủ

### 2.4. Loại 4 - Vốn chủ sở hữu

| TK | Tên | Có trong COA | Chi tiết |
|----|-----|:------------:|----------|
| 411 | Vốn ĐTCSH | ✅ | 4111-4118 + 41111, 41112 |
| 412 | CL đánh giá lại TS | ✅ | Ledger |
| 413 | CL tỷ giá hối đoái | ✅ | 4131, 4132 |
| 414 | Quỹ ĐTPT | ✅ | Ledger |
| 417 | Quỹ hỗ trợ SX DN | ✅ | Ledger |
| 418 | Các quỹ khác | ✅ | Ledger |
| 419 | Cổ phiếu quỹ | ✅ | Ledger |
| 421 | LNST chưa phân phối | ✅ | 4211, 4212 |
| 441 | Nguồn vốn ĐTXDCB | ✅ | Ledger |
| 461 | Nguồn KP sự nghiệp | ✅ | 4611, 4612 |
| 466 | Nguồn KP đã HT TSCĐ | ✅ | Ledger |

**Đánh giá:** ✅ Đầy đủ

### 2.5. Loại 5 - Doanh thu

| TK | Tên | Có trong COA | Chi tiết |
|----|-----|:------------:|----------|
| 511 | DT bán hàng & CCDV | ✅ | 5111-5118 |
| 515 | DT hoạt động tài chính | ✅ | Ledger |
| 521 | Các khoản giảm trừ DT | ✅ | 5211, 5212, 5213 |

**Đánh giá:** ⚠️ Thiếu tách DT bán buôn/lẻ (51111/51112) cho yêu cầu DCNET

### 2.6. Loại 6 - Chi phí SXKD

| TK | Tên | Có trong COA | Chi tiết |
|----|-----|:------------:|----------|
| 611 | Mua hàng | ✅ | 6111, 6112 |
| 621 | CP NVL trực tiếp | ✅ | Ledger |
| 622 | CP nhân công trực tiếp | ✅ | Ledger |
| 623 | CP sử dụng máy TC | ✅ | 6231-6238 |
| 627 | CP sản xuất chung | ✅ | 6271-6278 |
| 631 | Giá thành sản xuất | ✅ | Ledger |
| 632 | Giá vốn hàng bán | ✅ | Ledger |
| 635 | CP tài chính | ⚠️ | **Chỉ có parent, THIẾU children (6351, 6352, 6353)** |
| 641 | CP bán hàng | ✅ | 6411-6418 |
| 642 | CP QLDN | ✅ | 6421-6428 |

**Đánh giá:** ⚠️ TK 635 thiếu chi tiết quan trọng

### 2.7. Loại 7, 8, 9

| TK | Tên | Có trong COA | Chi tiết |
|----|-----|:------------:|----------|
| 711 | Thu nhập khác | ✅ | Ledger |
| 811 | Chi phí khác | ⚠️ | **Chỉ có parent, THIẾU children (8111, 8112)** |
| 821 | CP thuế TNDN | ✅ | 8211, 8212 |
| 911 | Xác định KQKD | ✅ | Ledger |

**Đánh giá:** ⚠️ TK 811 thiếu chi tiết

---

## 3. Lỗi ERPNext Account Type

### 3.1. ERPNext yêu cầu gì?

ERPNext sử dụng `Account Type` để tự động hoá hạch toán. Khi submit Sales Invoice, Payment Entry, Stock Entry... hệ thống tìm TK theo type, không theo số TK. **Thiếu type = ERPNext không hoạt động được.**

| Account Type | Vai trò trong ERPNext | Bắt buộc? |
|-------------|----------------------|:---------:|
| `Cash` | Tài khoản tiền mặt cho Payment Entry | ✅ |
| `Bank` | Tài khoản ngân hàng cho Payment Entry | ✅ |
| `Receivable` | Công nợ phải thu (Party Accounting) | ✅ |
| `Payable` | Công nợ phải trả (Party Accounting) | ✅ |
| `Stock` | Tài khoản tồn kho (Perpetual Inventory) | ✅ |
| `Cost of Goods Sold` | Giá vốn hàng bán | ✅ |
| `Stock Received But Not Billed` | Hàng nhận chưa có hoá đơn | ✅ |
| `Expenses Included In Asset Valuation` | CP cộng vào giá vốn nhập | ✅ |
| `Stock Adjustment` | Điều chỉnh kiểm kê kho | ✅ |
| `Accumulated Depreciation` | Hao mòn luỹ kế | ✅ |
| `Depreciation` | Chi phí khấu hao (expense) | ✅ |
| `Fixed Asset` | Tài khoản tài sản cố định | ✅ |
| `Capital Work in Progress` | XDCB dở dang | ⚠️ |
| `Tax` | Tài khoản thuế | ✅ |
| `Round Off` | Làm tròn chênh lệch | ⚠️ |
| `Temporary` | TK tạm (WIP) | ⚠️ |

### 3.2. Lỗi nghiêm trọng (Blocker)

#### Lỗi 1: Root account Loại 6 gán sai Account Type

```csv
# SAI (file gốc)
"Chi phí sản xuất, kinh doanh",,6,,1,Expenses Included In Asset Valuation,Expense,VND

# ĐÚNG (v2)
"Chi phí sản xuất, kinh doanh",,6,,1,,Expense,VND
```

**Vấn đề:** Root account (is_group=1) KHÔNG nên có Account Type. ERPNext sẽ coi toàn bộ loại 6 là "chi phí cộng vào giá vốn" → tính sai giá trị tồn kho.

#### Lỗi 2: TK 1561 (Giá mua hàng hoá) - Thiếu Stock type

```csv
# SAI (file gốc)
Giá mua hàng hóa,Hàng hóa,1561,156,0,,Asset,VND

# ĐÚNG (v2)
Giá mua hàng hóa,Hàng hóa,1561,156,0,Stock,Asset,VND
```

**Vấn đề:** Đây là TK chính để ERPNext ghi nhận giá trị tồn kho (Perpetual Inventory). Thiếu type → Stock Entry/Delivery Note không tạo được GL Entry.

**Ảnh hưởng features:** ACC-008 (hoá đơn bán), ACC-009 (hoá đơn mua), tất cả nghiệp vụ kho.

#### Lỗi 3: TK 152 (Nguyên vật liệu) - Thiếu Stock type

```csv
# SAI
"Nguyên liệu, vật liệu",Tài sản ngắn hạn,152,1,0,,Asset,VND

# ĐÚNG (v2)
"Nguyên liệu, vật liệu",Tài sản ngắn hạn,152,1,0,Stock,Asset,VND
```

#### Lỗi 4: TK ngoại tệ gán Currency = USD

```csv
# SAI
Ngoại tệ,Tiền mặt,1112,111,0,Cash,Asset,USD
Ngoại tệ,Tiền gửi Ngân hàng,1122,112,0,Bank,Asset,USD
Ngoại tệ,Tiền đang chuyển,1132,113,0,Bank,Asset,USD

# ĐÚNG (v2) - tất cả phải là VND
Ngoại tệ,Tiền mặt,1112,111,0,Cash,Asset,VND
Ngoại tệ,Tiền gửi Ngân hàng,1122,112,0,Bank,Asset,VND
Ngoại tệ,Tiền đang chuyển,1132,113,0,Bank,Asset,VND
```

**Vấn đề:** ERPNext quản lý multi-currency ở cấp **giao dịch** (Payment Entry), không phải cấp Account. Base currency là VND → tất cả Account phải VND.

### 3.3. Lỗi Account Type thiếu / sai

| TK | Tên | Type hiện tại | Type cần sửa | Ảnh hưởng |
|----|-----|:------------:|:------------:|-----------|
| **1561** | Giá mua hàng hoá | (trống) | `Stock` | Perpetual Inventory |
| **152** | Nguyên vật liệu | (trống) | `Stock` | NVL inventory |
| **1562** | CP thu mua hàng hoá | (trống) | `Expenses Included In Asset Valuation` | CP nhập cộng giá vốn |
| **241** | XDCB dở dang | (trống) | `Capital Work in Progress` | Asset CWIP |
| **2111** | Nhà cửa, vật kiến trúc | (trống) | `Fixed Asset` | Asset module |
| **2112** | Máy móc, thiết bị | (trống) | `Fixed Asset` | Asset module |
| **2113** | Phương tiện vận tải | (trống) | `Fixed Asset` | Asset module |
| **2114** | Thiết bị, dụng cụ QL | (trống) | `Fixed Asset` | Asset module |
| **2115** | Cây lâu năm, súc vật | (trống) | `Fixed Asset` | Asset module |
| **2118** | TSCĐ khác | (trống) | `Fixed Asset` | Asset module |
| **6234** | CP khấu hao máy TC | (trống) | `Depreciation` | Asset depreciation |
| **6274** | CP khấu hao TSCĐ (SX) | (trống) | `Depreciation` | Asset depreciation |
| **6414** | CP khấu hao TSCĐ (BH) | (trống) | `Depreciation` | Asset depreciation |

### 3.4. Tài khoản ERPNext cần nhưng chưa có

| TK đề xuất | Tên | Account Type | Root Type | Lý do |
|-----------|-----|-------------|-----------|-------|
| **4119** | Chênh lệch làm tròn | `Round Off` | Equity | ERPNext cần cho rounding difference |
| **6329** | Điều chỉnh hàng tồn kho | `Stock Adjustment` | Expense | Bắt buộc cho Stock Reconciliation |
| **6351** | Lãi vay | (Expense) | Expense | 635 chỉ có parent, không children |
| **6352** | Chiết khấu thanh toán cho NCC | (Expense) | Expense | Chiết khấu thanh toán |
| **6353** | Lỗ chênh lệch tỷ giá | (Expense) | Expense | Hoạt động kinh doanh |
| **8111** | CP thanh lý, nhượng bán TSCĐ | (Expense) | Expense | 811 chỉ có parent |
| **8112** | Phạt vi phạm hợp đồng | (Expense) | Expense | Nghiệp vụ phạt |
| **1565** | Hàng trade-in (hàng cũ thu lại) | `Stock` | Asset | Nghiệp vụ trade-in DCNET |
| **51111** | Doanh thu bán buôn | (Income) | Income | Tách kênh bán theo yêu cầu |
| **51112** | Doanh thu bán lẻ | (Income) | Income | Tách kênh bán theo yêu cầu |

---

## 4. Lỗi Hierarchy (Parent-Child)

### 4.1. TK 2118 - Parent sai

```csv
# SAI - parent là "Tài sản dài hạn" (TK 2)
TSCĐ khác,Tài sản dài hạn,2118,2,0,,Asset,VND

# ĐÚNG - parent phải là "Tài sản cố định hữu hình" (TK 211)
TSCĐ khác,Tài sản cố định hữu hình,2118,211,0,Fixed Asset,Asset,VND
```

**Lý do:** Theo TT200, TK 2118 thuộc nhóm 211 (TSCĐ hữu hình), không phải trực tiếp dưới loại 2.

### 4.2. TK 3339 - Parent sai

```csv
# SAI - parent là "Nợ phải trả" (TK 3)
"Phí, lệ phí và các khoản phải nộp khác",Nợ phải trả,3339,3,0,Tax,Liability,VND

# ĐÚNG - parent phải là "Thuế và các khoản phải nộp NN" (TK 333)
"Phí, lệ phí và các khoản phải nộp khác",Thuế và các khoản phải nộp Nhà nước,3339,333,0,Tax,Liability,VND
```

**Lý do:** Theo TT200, TK 3339 thuộc nhóm 333.

---

## 5. Đối chiếu với Specs khách hàng (20 features)

### Nguồn tham chiếu

- `docs/feature/ERP_SPECIFICATION.md` — Section 5 (Kế toán)
- `docs/contract/DCNET_SRS_TM.md` — Section 3.22-3.32
- `docs/contract/DCNET_SRS_NM.md` — Section 3.22-3.32
- `docs/contract/appendix/tm/A_FEATURE_MATRIX.md` — ERP-ACC-001 → 020

### 5.1. Kế toán Tiền (ACC-001 → 004)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-001** | Phiếu thu (thu tiền KH) | Nợ 1111/1121, Có 131 | 1111 ✅, 1121 ✅, 131 ✅ | ✅ |
| **ACC-002** | Phiếu chi (chi tiền NCC) | Nợ 331, Có 1111/1121 | 331 ✅, 1111/1121 ✅ | ✅ |
| **ACC-003** | Báo có NH | Nợ 1121, Có 131/xxx | 1121 ✅ | ✅ |
| **ACC-004** | Báo nợ NH | Nợ 331/xxx, Có 1121 | 1121 ✅, 331 ✅ | ✅ |

**Yêu cầu bổ sung:** Chênh lệch tỷ giá tự động → TK 413 ✅, 635 ✅ (nhưng 635 thiếu children 6353)

**Kết luận:** ✅ Hỗ trợ tốt, cần thêm 6353 cho tỷ giá

### 5.2. Kế toán Mua hàng (ACC-009)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-009** | Hoá đơn mua | Nợ 1561, Nợ 1331, Có 331 | 1561 ⚠️, 1331 ✅, 331 ✅ | ⚠️ |
| Phân bổ CP vận chuyển | Cộng vào giá vốn | 1562 ⚠️ (thiếu type) | ⚠️ |
| Thuế nhập khẩu | Nợ 1561, Có 3333 | 3333 ✅ | ✅ |
| CP hải quan, bảo hiểm | Phân bổ vào SP | 1562 ⚠️ | ⚠️ |

**Vấn đề:**
- TK 1561 thiếu `Stock` type → ERPNext không post GL từ Purchase Receipt
- TK 1562 thiếu `Expenses Included In Asset Valuation` → chi phí mua không cộng vào giá vốn

**Kết luận:** ⚠️ Cần sửa Account Type

### 5.3. Kế toán Bán hàng (ACC-008)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-008** | Hoá đơn bán buôn | Nợ 131, Có 5111, Có 33311 | 131 ✅, 5111 ✅, 33311 ✅ | ✅ |
| HĐ bán lẻ (POS) | Nợ 111/112, Có 5111 | 1111/1121 ✅ | ✅ |
| Giá vốn hàng bán | Nợ 632, Có 1561 | 632 ✅, 1561 ⚠️ | ⚠️ |
| Chiết khấu TM | Nợ 5211 | 5211 ✅ | ✅ |
| Hàng bán trả lại | Nợ 5212 | 5212 ✅ | ✅ |
| Giảm giá hàng bán | Nợ 5213 | 5213 ✅ | ✅ |
| **Tách DT buôn/lẻ** | BC theo kênh bán | 51111, 51112 | ❌ **THIẾU** | ❌ |

**Kết luận:** ⚠️ Cần thêm 51111/51112 để tách kênh bán

### 5.4. Kế toán Công nợ (ACC-005, 006, 007)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-005** | Công nợ phải thu (AR Aging) | 131 (Receivable) | ✅ | ✅ |
| **ACC-006** | Công nợ phải trả (AP Aging) | 331 (Payable) | ✅ | ✅ |
| **ACC-007** | Đối chiếu công nợ | 131 + 331 | ✅ | ✅ |
| Tạm ứng - Hoàn ứng | 141 | ✅ | ✅ |
| Hạn mức công nợ | Config trong Customer | Không phụ thuộc COA | ✅ |

**Kết luận:** ✅ Hỗ trợ đầy đủ

### 5.5. Kế toán Tồn kho

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| Giá trị tồn kho | Theo kho, batch | 1561 (Stock) | ⚠️ thiếu type | ⚠️ |
| COGS (Bình quân/FIFO) | Tính giá vốn | 632 ✅ | ✅ | ✅ |
| Chênh lệch kiểm kê | Stock Reconciliation | Stock Adjustment | ❌ **THIẾU** | ❌ |
| Hàng mua đi đường | TK trung gian | 151 ✅ | ✅ | ✅ |

**Kết luận:** ⚠️ Cần thêm 6329 (Stock Adjustment) và sửa type 1561

### 5.6. Chi phí & Hỗ trợ (ACC-016, 017)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-016** | CP hỗ trợ hãng (Marketing, Demo) | 641x | 641x ✅ | ⚠️ |
| **ACC-017** | CP sự kiện (theo SP, chiến dịch) | 641x + Cost Center | 641x ✅ | ⚠️ |
| CP sai giá | Price variance | Chưa có TK riêng | ⚠️ | ⚠️ |

**Ghi chú:** ERPNext sẽ dùng **Cost Center** để theo dõi chi phí theo sự kiện/chiến dịch, không cần TK riêng cho từng loại. Tuy nhiên, có thể cần thêm TK con dưới 641 cho chi tiết hơn.

**Kết luận:** ⚠️ Đủ về mặt TK, cần setup Cost Center

### 5.7. Tài sản & CCDC (ACC-013, 014)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-013** | TSCĐ (nguyên giá, vị trí) | 211x (Fixed Asset) | ⚠️ thiếu type | ⚠️ |
| **ACC-014** | Khấu hao đường thẳng | 214x + 6424 (Depreciation) | 214x ✅, 6424 ✅ | ⚠️ |
| Thanh lý TS | Thu/chi thanh lý | 711, 811 | 711 ✅, 811 ⚠️ thiếu chi tiết | ⚠️ |
| CCDC phân bổ | Nhiều kỳ | 153x, 242 | ✅ | ✅ |
| CWIP | XDCB dở dang | 241 (CWIP type) | ⚠️ thiếu type | ⚠️ |

**Kết luận:** ⚠️ Cần sửa Account Type cho 211x, 241, 6274, 6234, 6414

### 5.8. Thuế (ACC-015)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-015** | VAT đầu vào | 1331, 1332 (Tax) | ✅ | ✅ |
| VAT đầu ra | 33311 (Tax) | ✅ | ✅ |
| VAT nhập khẩu | 33312 | ✅ | ✅ |
| Thuế nhập khẩu | 3333 | ✅ | ✅ |
| Thuế TNDN | 3334, 8211/8212 | ✅ | ✅ |
| TNCN | 3335 | ✅ | ✅ |
| Xuất HTKK | Custom development | Không phụ thuộc COA | N/A |
| Hoá đơn điện tử | Tích hợp bên thứ 3 | Không phụ thuộc COA | N/A |

**Kết luận:** ✅ COA đầy đủ cho thuế. HTKK và HĐĐT là custom development.

### 5.9. Tổng hợp & Báo cáo (ACC-010, 011, 012, 018, 019, 020)

| Feature | Mô tả | TK cần | Có trong COA | Đánh giá |
|---------|--------|--------|:------------:|:--------:|
| **ACC-010** | Sổ cái (General Ledger) | Tất cả TK | ✅ | ✅ |
| **ACC-011** | Sổ nhật ký (Journal Entry) | Tất cả TK | ✅ | ✅ |
| **ACC-012** | Bút toán điều chỉnh | 911, 421 | ✅ | ✅ |
| **ACC-018** | BC tài chính (P&L, BS) | 511-911 | ✅ | ✅ |
| **ACC-019** | BC dòng tiền (Cash Flow) | 111, 112, 113 | ✅ | ✅ |
| **ACC-020** | Đề nghị thanh toán | Payment Request | Không phụ thuộc COA | ✅ |
| BC theo chi nhánh | Quản trị | Cost Center | Không phụ thuộc COA | ✅ |
| Khoá sổ theo kỳ | Accounting Period | Không phụ thuộc COA | ✅ |
| **635 chi tiết** | Lãi vay, CL tỷ giá, CK TT | 6351, 6352, 6353 | ❌ **THIẾU** | ❌ |

**Kết luận:** ✅ Hầu hết OK, cần thêm chi tiết TK 635

### 5.10. Bảng tổng hợp 20 Features

| # | Feature ID | Tên | Priority | COA hỗ trợ |
|---|-----------|------|:--------:|:----------:|
| 1 | ACC-001 | Phiếu thu | Critical | ✅ |
| 2 | ACC-002 | Phiếu chi | Critical | ✅ |
| 3 | ACC-003 | Báo có NH | High | ✅ |
| 4 | ACC-004 | Báo nợ NH | High | ✅ |
| 5 | ACC-005 | Công nợ phải thu | Critical | ✅ |
| 6 | ACC-006 | Công nợ phải trả | Critical | ✅ |
| 7 | ACC-007 | Đối chiếu CN | High | ✅ |
| 8 | ACC-008 | Hoá đơn bán | Critical | ⚠️ Thiếu tách buôn/lẻ |
| 9 | ACC-009 | Hoá đơn mua | Critical | ⚠️ TK 1561 thiếu type |
| 10 | ACC-010 | Sổ cái | Critical | ✅ |
| 11 | ACC-011 | Sổ nhật ký | Critical | ✅ |
| 12 | ACC-012 | Bút toán điều chỉnh | High | ✅ |
| 13 | ACC-013 | Kế toán TSCĐ | High | ⚠️ 211x thiếu Fixed Asset type |
| 14 | ACC-014 | Khấu hao TSCĐ | High | ⚠️ 6274, 6414 thiếu Depreciation type |
| 15 | ACC-015 | Kế toán thuế | Critical | ✅ |
| 16 | ACC-016 | CP hỗ trợ hãng | High | ⚠️ Cần Cost Center |
| 17 | ACC-017 | CP sự kiện | High | ⚠️ Cần Cost Center |
| 18 | ACC-018 | BC tài chính | Critical | ✅ |
| 19 | ACC-019 | BC dòng tiền | High | ✅ |
| 20 | ACC-020 | Đề nghị thanh toán | High | ✅ |

---

## 6. Phân tích theo nghiệp vụ đặc thù DCNET

### 6.1. Trade-in (Thu đổi SP cũ)

**Nguồn:** `FEATURE_SPECIFICATION.md` Section 18, SRS Section 3.14

**Nghiệp vụ:** Khách mang SP cũ → Định giá → Trừ vào giá SP mới

**Bút toán:**
```
Nợ 131/111  (Số tiền KH trả = Giá mới - Giá cũ - Voucher)
Nợ 1565     (Giá trị SP cũ thu về)       ← THIẾU trong COA
Có 5111     (Doanh thu giá SP mới)
Có 33311    (VAT đầu ra)
```

**COA cần thêm:**
| TK | Tên | Account Type | Parent |
|----|-----|-------------|--------|
| **1565** | Hàng trade-in (hàng cũ thu lại) | `Stock` | 156 (Hàng hoá) |

### 6.2. Bán buôn vs Bán lẻ

**Nguồn:** `ERP_SPECIFICATION.md` Section 2, SRS Section 3.25

**Yêu cầu:** Tách báo cáo doanh thu theo kênh bán (bán buôn đại lý vs bán lẻ tại quầy)

**COA hiện tại:** Chỉ có TK 5111 (DT bán hàng hoá) chung → Không tách được

**COA cần thêm:**
| TK | Tên | Account Type | Parent |
|----|-----|-------------|--------|
| **51111** | Doanh thu bán buôn | (Income) | 5111 |
| **51112** | Doanh thu bán lẻ | (Income) | 5111 |

**Lưu ý:** Khi thêm 51111/51112, TK 5111 phải đổi thành `is_group=1`.

### 6.3. Chi phí hỗ trợ hãng & Sự kiện

**Nguồn:** `ERP_SPECIFICATION.md` Section 5.6, `MODULE_GAP_ANALYSIS.md`

**Yêu cầu:** Phân bổ chi phí marketing, demo, trưng bày theo sự kiện và sản phẩm

**Giải pháp ERPNext:** Sử dụng **Cost Center** per event/campaign, không cần thêm TK. Các TK 641x (CP bán hàng) hiện tại đủ dùng.

**Tuy nhiên** nếu khách yêu cầu "CP sai giá" (price variance) riêng:
| TK | Tên | Account Type | Parent |
|----|-----|-------------|--------|
| **6419** | Chi phí sai giá | (Expense) | 641 (CP bán hàng) |

### 6.4. Đa chi nhánh

**Nguồn:** SRS Section 3.15

**Yêu cầu:** BC quản trị theo chi nhánh, theo đại lý

**Giải pháp ERPNext:** **Cost Center** hierarchy (Công ty → Chi nhánh → Bộ phận). Không cần TK riêng per chi nhánh. COA hiện tại đủ.

### 6.5. Nhập khẩu (Import Process)

**Nguồn:** `IMPORT_PROCESS_SPECIFICATION.md`

**Bút toán nhập khẩu:**
```
Nợ 1561    (Giá mua CIF)                    ← cần Stock type
Nợ 1331    (VAT nhập khẩu được khấu trừ)    ✅
Có 331     (Phải trả NCC nước ngoài)         ✅
Có 3333    (Thuế nhập khẩu)                  ✅
Có 33312   (VAT nhập khẩu)                   ✅

Phân bổ CP:
Nợ 1561    (CP vận chuyển, bảo hiểm → cộng giá vốn)
Có 1562    (CP thu mua)                      ← cần Expenses Included In Asset Valuation
```

**COA đánh giá:** ⚠️ Cần sửa type 1561, 1562

---

## 7. Workflow kế toán trong ERPNext

### 7.1. Nguyên tắc cốt lõi

> **Mọi giao dịch tài chính → GL Entry (bút toán kép: Nợ = Có)**
> Các báo cáo tài chính đều đọc từ bảng GL Entry.

### 7.2. Các luồng chính

```
┌─────────────────────────────────────────────────────────────┐
│                    LUỒNG BÁN HÀNG                          │
│  Sales Order → Delivery Note → Sales Invoice → Payment     │
│                                      ↓                     │
│                               GL Entry tự động:            │
│                               Nợ 131, Có 5111, Có 33311   │
│                               Nợ 632, Có 1561 (COGS)      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    LUỒNG MUA HÀNG                          │
│  Purchase Order → Purchase Receipt → Purchase Invoice → PE │
│                                            ↓               │
│                                     GL Entry tự động:      │
│                                     Nợ 1561, Nợ 1331      │
│                                     Có 331                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    LUỒNG KHO                               │
│  Stock Entry / Delivery Note / Purchase Receipt            │
│                       ↓                                    │
│              Stock Ledger Entry                            │
│                       ↓                                    │
│              GL Entry (nếu Perpetual Inventory = ON)       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    LUỒNG THANH TOÁN                        │
│  Payment Entry:                                            │
│    Thu tiền KH:  Nợ 1111/1121, Có 131                     │
│    Chi tiền NCC: Nợ 331, Có 1111/1121                     │
│                       ↓                                    │
│              Bank Reconciliation (đối soát sao kê NH)      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    LUỒNG CUỐI KỲ                           │
│  Journal Entry (bút toán điều chỉnh)                      │
│    → Kết chuyển DT/CP vào 911                             │
│    → Kết chuyển lãi/lỗ vào 421                            │
│    → Đánh giá CL tỷ giá → 413                            │
│    → Khấu hao TSCĐ → 214x, 6424                          │
│                       ↓                                    │
│              Khoá sổ (Accounting Period)                    │
│                       ↓                                    │
│              Báo cáo tài chính                             │
│              ├── Balance Sheet (CĐKT)                      │
│              ├── P&L (KQKD)                                │
│              ├── Cash Flow (Dòng tiền)                     │
│              ├── Trial Balance (CĐPS)                      │
│              ├── General Ledger (Sổ cái)                   │
│              ├── AR/AP Aging (Tuổi nợ)                     │
│              └── Tax Reports (Thuế)                        │
└─────────────────────────────────────────────────────────────┘
```

### 7.3. Bảng GL Entry theo nghiệp vụ

| Nghiệp vụ | Document ERPNext | Nợ | Có |
|-----------|-----------------|-----|-----|
| Bán hàng (DT) | Sales Invoice | 131 (Debtors) | 5111 (DT), 33311 (VAT) |
| Bán hàng (COGS) | Sales Invoice | 632 (COGS) | 1561 (Kho) |
| Mua hàng | Purchase Invoice | 1561 (Kho), 1331 (VAT) | 331 (NCC) |
| Thu tiền KH | Payment Entry | 1111/1121 (Cash/Bank) | 131 (Debtors) |
| Chi tiền NCC | Payment Entry | 331 (NCC) | 1111/1121 (Cash/Bank) |
| Nhập kho | Stock Entry (Receipt) | 1561 (Kho) | Temp/Stock Adjustment |
| Xuất kho | Stock Entry (Issue) | Stock Adjustment | 1561 (Kho) |
| Khấu hao | Journal Entry | 6424 (CP KH) | 2141 (Hao mòn) |
| Kết chuyển DT | Journal Entry | 511 (DT) | 911 (XĐKQKD) |
| Kết chuyển CP | Journal Entry | 911 (XĐKQKD) | 632, 641, 642 |
| Kết chuyển lãi | Journal Entry | 911 (XĐKQKD) | 4212 (LNST) |

---

## 8. Danh sách sửa đổi (Changelog v1 → v2)

### 8.1. Tổng hợp thay đổi

| # | Loại | Số lượng |
|---|------|:--------:|
| Sửa Account Type | 14 TK |
| Sửa Currency | 3 TK |
| Sửa Parent | 2 TK |
| Sửa is_group | 1 TK |
| Thêm TK mới | 10 TK |
| **Tổng** | **30 thay đổi** |

### 8.2. Chi tiết từng thay đổi

#### P0 - Blocker (phải sửa trước khi import)

| # | TK | Thay đổi | Trước | Sau |
|---|-----|---------|-------|-----|
| 1 | 6 (root) | Xoá Account Type | `Expenses Included In Asset Valuation` | (trống) |
| 2 | 1561 | Thêm Account Type | (trống) | `Stock` |
| 3 | 152 | Thêm Account Type | (trống) | `Stock` |
| 4 | 1112 | Sửa Currency | USD | VND |
| 5 | 1122 | Sửa Currency | USD | VND |
| 6 | 1132 | Sửa Currency | USD | VND |
| 7 | 2118 | Sửa Parent + Account Type | Parent=2, type=(trống) | Parent=211, type=`Fixed Asset` |
| 8 | 3339 | Sửa Parent | Parent=3 | Parent=333 |
| 9 | NEW | Thêm 6329 | — | Điều chỉnh HTK (`Stock Adjustment`) |
| 10 | NEW | Thêm 4119 | — | CL làm tròn (`Round Off`) |

#### P1 - Quan trọng

| # | TK | Thay đổi | Trước | Sau |
|---|-----|---------|-------|-----|
| 11 | 241 | Thêm Account Type | (trống) | `Capital Work in Progress` |
| 12 | 2111 | Thêm Account Type | (trống) | `Fixed Asset` |
| 13 | 2112 | Thêm Account Type | (trống) | `Fixed Asset` |
| 14 | 2113 | Thêm Account Type | (trống) | `Fixed Asset` |
| 15 | 2114 | Thêm Account Type | (trống) | `Fixed Asset` |
| 16 | 2115 | Thêm Account Type | (trống) | `Fixed Asset` |
| 17 | 6234 | Thêm Account Type | (trống) | `Depreciation` |
| 18 | 6274 | Thêm Account Type | (trống) | `Depreciation` |
| 19 | 6414 | Thêm Account Type | (trống) | `Depreciation` |
| 20 | 1562 | Thêm Account Type | (trống) | `Expenses Included In Asset Valuation` |
| 21 | NEW | Thêm 6351 | — | Lãi vay (Expense) |
| 22 | NEW | Thêm 6352 | — | Chiết khấu thanh toán (Expense) |
| 23 | NEW | Thêm 6353 | — | Lỗ CL tỷ giá (Expense) |
| 24 | NEW | Thêm 8111 | — | CP thanh lý TSCĐ (Expense) |
| 25 | NEW | Thêm 8112 | — | Phạt vi phạm hợp đồng (Expense) |

#### P2 - Đề xuất cho DCNET

| # | TK | Thay đổi | Mô tả |
|---|-----|---------|-------|
| 26 | 5111 | Đổi is_group | 0 → 1 (để chứa 51111, 51112) |
| 27 | NEW | Thêm 51111 | DT bán buôn (Income) |
| 28 | NEW | Thêm 51112 | DT bán lẻ (Income) |
| 29 | NEW | Thêm 1565 | Hàng trade-in (`Stock`) |
| 30 | 635 | Đổi is_group | 0 → 1 (để chứa 6351, 6352, 6353) |

---

## 9. Vấn đề cần Clarify với khách hàng

### 9.1. Thông tư 99 vs Thông tư 200

| Tài liệu | Ghi | Dòng |
|----------|-----|------|
| `ERP_SPECIFICATION.md` | Thông tư **99** | Section 5.0, line 1059 |
| `DCNET_SRS_TM.md` | Thông tư **200**/2014/TT-BTC | Section 2.4.2, line 271 |
| `DCNET_SRS_NM.md` | Thông tư **200**/2014/TT-BTC | Section 2.4.2, line 275 |

> **Conflict:** ERP spec (từ khách) nói TT99, nhưng 2 SRS (hợp đồng) đều nói TT200.
> COA hiện tại theo **TT200** → phù hợp với SRS.
> **Cần xác nhận:** Khách dùng TT200 hay TT99? (TT99 = Thông tư 99/2018/TT-BTC về chế độ báo cáo tài chính NN, KHÔNG phải chế độ kế toán DN)

### 9.2. Phương pháp tính giá vốn

| Tài liệu | Ghi |
|----------|-----|
| `ERP_SPECIFICATION.md` | Trung bình **tháng** (hoặc FIFO) |
| `DCNET_SRS_TM.md` | Bình quân **gia quyền** |
| ERPNext hỗ trợ | FIFO hoặc Moving Average (bình quân **tại thời điểm**) |

> **Vấn đề:** ERPNext KHÔNG có "trung bình tháng" (tính lại cuối tháng). Chỉ có Moving Average (tính tại mỗi giao dịch).
> **Cần xác nhận:** Khách chấp nhận Moving Average thay cho trung bình tháng?

### 9.3. Trade-in: Giá cũ > Giá mới

> **Câu hỏi (từ FEATURE_SPECIFICATION.md Section 18.3 Q5):**
> Trường hợp giá trị SP cũ > giá SP mới → Khách hàng có được nhận tiền chênh lệch không?
> Nếu có → cần bút toán hoàn tiền, ảnh hưởng COA.

### 9.4. Hoá đơn điện tử

> **Cần xác nhận:** Tích hợp nhà cung cấp HĐĐT nào? (VNPT, Viettel, MISA, FPT...)
> Ảnh hưởng đến cách mapping TK thuế.

### 9.5. Phiếu thu/chi theo mẫu VN

> **Cần xác nhận:** Khách cần in phiếu thu/chi theo mẫu TT200 hay dùng format ERPNext?
> Nếu theo TT200 → cần custom Print Format.

### 9.6. Thông tin bổ sung từ SRS

> Nhiều section kế toán trong SRS ghi:
> *"Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng"*
> (SRS_TM: Section 3.24, 3.27, 3.29, 3.30, 3.31)
> → Cần schedule buổi làm việc chi tiết với kế toán trưởng của khách.

---

## 10. Hướng dẫn Import vào ERPNext

### 10.1. Chuẩn bị

1. Sử dụng file `ChartOfAccountsImporter_v2.csv` (đã sửa)
2. Tạo Company trước (VD: "Thăng Long TM", abbreviation: "TM")
3. Chọn base currency: **VND**

### 10.2. Import qua UI

```
Setup → Chart of Accounts → Import Chart of Accounts
→ Upload ChartOfAccountsImporter_v2.csv
→ Select Company
→ Import
```

### 10.3. Import qua CLI (trong container)

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && \
  bench --site flow.local import-chart-of-accounts \
  --company 'Thăng Long TM' \
  --file /path/to/ChartOfAccountsImporter_v2.csv"
```

### 10.4. Kiểm tra sau import

- [ ] Mở Chart of Accounts → kiểm tra cây TK hiển thị đúng
- [ ] Kiểm tra Account Type đã gán đúng cho các TK quan trọng
- [ ] Thử tạo 1 Sales Invoice → kiểm tra GL Entry tự động
- [ ] Thử tạo 1 Payment Entry → kiểm tra TK Cash/Bank
- [ ] Thử tạo 1 Stock Entry → kiểm tra Perpetual Inventory
- [ ] Kiểm tra báo cáo: Trial Balance, P&L, Balance Sheet

### 10.5. Sau import: Setup bổ sung

| Cấu hình | Nơi setup | Ghi chú |
|----------|-----------|---------|
| Default Accounts | Company DocType | Receivable, Payable, Stock, COGS... |
| Tax Templates | Sales/Purchase Taxes | VAT 8%, 10% → mapping TK 33311, 1331 |
| Cost Centers | Cost Center tree | Theo chi nhánh + sự kiện |
| Payment Terms | Payment Terms | Điều khoản thanh toán |
| Fiscal Year | Fiscal Year | 01/01 - 31/12 |
| Accounting Period | Accounting Period | Khoá sổ theo tháng/quý |

---

## Phụ lục

### A. File đính kèm

| File | Mô tả |
|------|-------|
| `ChartOfAccountsImporter_v2.csv` | COA đã sửa, sẵn sàng import |
| `COA_ANALYSIS.md` | Tài liệu này |

### B. Tham chiếu

| Tài liệu | Đường dẫn |
|----------|-----------|
| ERP Specification | `docs/feature/ERP_SPECIFICATION.md` Section 5 |
| Feature Specification | `docs/feature/FEATURE_SPECIFICATION.md` Section 18 (Trade-in) |
| SRS Thăng Long TM | `docs/contract/DCNET_SRS_TM.md` Section 3.22-3.32 |
| SRS Nhật Minh Sport | `docs/contract/DCNET_SRS_NM.md` Section 3.22-3.32 |
| Feature Matrix | `docs/contract/appendix/tm/A_FEATURE_MATRIX.md` (ERP-ACC-*) |
| Module Gap Analysis | `docs/erpnext-flows/MODULE_GAP_ANALYSIS.md` |
| Import Process | `docs/feature/IMPORT_PROCESS_SPECIFICATION.md` |

### C. Người thực hiện

- Phân tích: Claude Code (AI)
- Review: (chờ review)
- Ngày: 15/02/2026
