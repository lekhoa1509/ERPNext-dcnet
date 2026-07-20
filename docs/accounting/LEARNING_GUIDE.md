# Hướng Dẫn Học Kế Toán Căn Bản — Qua Demo Data DCNET Flow

> **Tài liệu này dùng bộ dữ liệu mô phỏng 3 năm (2023–2026) của DCNET Flow** để dạy kế toán doanh nghiệp Việt Nam theo Thông tư 200/2014/TT-BTC (TT200), kết hợp với ERPNext.
>
> **Đối tượng:** Developer, PM, hoặc bất kỳ ai muốn hiểu kế toán qua thực hành.
>
> **Cách đọc:** Đọc tuần tự từ Phần 1 → Phần 7. Mỗi phần có ví dụ thực tế từ code generator.

---

## Mục lục

1. [Phương trình kế toán & Ghi sổ kép](#1-phương-trình-kế-toán--ghi-sổ-kép)
2. [Hệ thống tài khoản TT200](#2-hệ-thống-tài-khoản-tt200)
3. [Dòng chảy dữ liệu demo 3 năm](#3-dòng-chảy-dữ-liệu-demo-3-năm)
4. [Các luồng nghiệp vụ kế toán](#4-các-luồng-nghiệp-vụ-kế-toán)
5. [Báo cáo tài chính](#5-báo-cáo-tài-chính)
6. [ERPNext & Kế toán tự động](#6-erpnext--kế-toán-tự-động)
7. [Bài tập tự kiểm tra](#7-bài-tập-tự-kiểm-tra)

---

## 1. Phương trình kế toán & Ghi sổ kép

### 1.1. Phương trình kế toán cơ bản

Đây là nền tảng của MỌI hệ thống kế toán trên thế giới:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   TÀI SẢN  =  NỢ PHẢI TRẢ  +  VỐN CHỦ SỞ HỮU         ║
║   (Assets)    (Liabilities)     (Equity)                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

**Mọi giao dịch trong doanh nghiệp đều giữ phương trình này cân bằng.**

Ví dụ từ demo — **Góp vốn 10 tỷ VND** (`vietnamese_accounting.py:152-187`):

```
Trước:  Tài sản (0) = Nợ (0) + Vốn (0)

Giao dịch: Chủ sở hữu góp 10 tỷ (2 tỷ tiền mặt + 8 tỷ ngân hàng)

Sau:    Tài sản (10 tỷ) = Nợ (0) + Vốn (10 tỷ)
        ├── Tiền mặt: +2 tỷ
        └── Ngân hàng: +8 tỷ         Vốn CSH: +10 tỷ

Kiểm tra: 10 tỷ = 0 + 10 tỷ ✓
```

### 1.2. Mở rộng phương trình

Khi doanh nghiệp hoạt động, phương trình mở rộng thêm Doanh thu và Chi phí:

```
TÀI SẢN = NỢ PHẢI TRẢ + VỐN + (DOANH THU - CHI PHÍ)
                                  └──── Lãi/Lỗ ─────┘
```

- **Doanh thu > Chi phí** → Lãi → Vốn tăng
- **Chi phí > Doanh thu** → Lỗ → Vốn giảm

### 1.3. Nguyên tắc GHI SỔ KÉP (Double-entry Bookkeeping)

> **Quy tắc vàng: Mỗi giao dịch PHẢI ghi ít nhất 2 dòng — NỢ (Debit) và CÓ (Credit) — tổng Nợ = tổng Có.**

Trong ERPNext, mỗi giao dịch tạo ra các dòng **GL Entry** (General Ledger Entry) tuân theo nguyên tắc này.

#### Bảng quy tắc Nợ/Có

```
┌─────────────────────────┬──────────────┬──────────────┐
│ Loại tài khoản          │ NỢ (Debit)   │ CÓ (Credit)  │
│                         │ = Tăng (+)   │ = Tăng (+)   │
├─────────────────────────┼──────────────┼──────────────┤
│ Tài sản (1xx, 2xx)     │      ✓       │              │
│ Chi phí (6xx, 8xx)     │      ✓       │              │
├─────────────────────────┼──────────────┼──────────────┤
│ Nợ phải trả (3xx)      │              │      ✓       │
│ Doanh thu (5xx, 7xx)   │              │      ✓       │
│ Vốn CSH (4xx)          │              │      ✓       │
└─────────────────────────┴──────────────┴──────────────┘
```

**Mẹo nhớ đơn giản:**

- **Nợ (Debit)** = bên trái = tiền đi đâu / chi phí phát sinh
- **Có (Credit)** = bên phải = tiền từ đâu đến / nguồn vốn tăng

#### Ví dụ minh họa từ demo

**Mua xe tải 650 triệu + VAT 10%** (`vietnamese_accounting.py:218-244`):

```
                    NỢ (Dr)           CÓ (Cr)
                    ─────────         ─────────
TK 2111 TSCĐ       650,000,000                    ← Tài sản tăng
TK 1331 VAT vào     65,000,000                    ← Tài sản (thuế) tăng
TK 1121 Ngân hàng                    715,000,000  ← Tài sản (tiền) giảm
                    ─────────         ─────────
TỔNG:               715,000,000       715,000,000  ✓ Cân bằng!
```

Giải thích: Công ty bỏ ra 715tr (ngân hàng giảm) để nhận về xe trị giá 650tr + quyền khấu trừ thuế 65tr.

---

## 2. Hệ thống tài khoản TT200

### 2.1. Thông tư 200 là gì?

**Thông tư 200/2014/TT-BTC** là chuẩn kế toán Việt Nam cho doanh nghiệp vừa và lớn, ban hành bởi Bộ Tài chính. Nó quy định:
- Hệ thống tài khoản (mã số + tên)
- Cách ghi sổ từng loại nghiệp vụ
- Mẫu báo cáo tài chính

### 2.2. Cấu trúc mã tài khoản

```
Chữ số đầu tiên = NHÓM tài khoản:

  1xx = Tài sản ngắn hạn (tiền, kho, phải thu)
  2xx = Tài sản dài hạn (TSCĐ, đầu tư)
  3xx = Nợ phải trả (NCC, lương, thuế)
  4xx = Vốn chủ sở hữu
  5xx = Doanh thu
  6xx = Chi phí sản xuất kinh doanh
  7xx = Thu nhập khác
  8xx = Chi phí khác
  9xx = Xác định kết quả kinh doanh
```

### 2.3. Các tài khoản dùng trong demo DCNET

Demo sử dụng 26 tài khoản TT200 (xem `vietnamese_accounting.py:19-57`), chia thành 5 nhóm:

#### NHÓM 1: TÀI SẢN — "Công ty CÓ gì?"

```
┌─────────────────────────────────────────────────────────────────────┐
│ TÀI SẢN NGẮN HẠN (luân chuyển nhanh, < 1 năm)                    │
├────────┬────────────────────────────────┬──────────────────────────┤
│ Mã TK  │ Tên tài khoản                 │ Vai trò trong demo       │
├────────┼────────────────────────────────┼──────────────────────────┤
│ 1111   │ Tiền mặt                       │ Quỹ tiền mặt công ty    │
│ 1121   │ TG Ngân hàng (Techcombank)     │ TK ngân hàng chính      │
│ 1122   │ TG Ngân hàng (Vietcombank)     │ TK ngân hàng phụ        │
│ 131    │ Phải thu khách hàng            │ Tiền KH còn nợ mình     │
│ 1331   │ Thuế GTGT được khấu trừ        │ VAT mua hàng (đòi lại)  │
│ 153    │ Công cụ, dụng cụ              │ Máy tính, bàn ghế...    │
│ 156    │ Hàng hóa                       │ Tồn kho sản phẩm golf   │
├────────┴────────────────────────────────┴──────────────────────────┤
│ TÀI SẢN DÀI HẠN (sử dụng > 1 năm)                               │
├────────┬────────────────────────────────┬──────────────────────────┤
│ 2111   │ TSCĐ hữu hình                 │ Xe tải (650tr)           │
│ 2141   │ Hao mòn lũy kế TSCĐ           │ Phần đã khấu hao        │
│ 242    │ Chi phí trả trước             │ Laptop (120tr / 24 tháng)│
└────────┴────────────────────────────────┴──────────────────────────┘
```

**Cách hiểu:** Tài sản = mọi thứ có giá trị mà công ty sở hữu. `Hao mòn lũy kế (2141)` là số ÂM, trừ dần giá trị tài sản theo thời gian.

#### NHÓM 3: NỢ PHẢI TRẢ — "Công ty NỢ ai?"

```
┌────────┬────────────────────────────────┬──────────────────────────┐
│ Mã TK  │ Tên tài khoản                 │ Vai trò trong demo       │
├────────┼────────────────────────────────┼──────────────────────────┤
│ 331    │ Phải trả người bán            │ Nợ NCC chưa trả         │
│ 3331   │ Thuế GTGT phải nộp            │ VAT bán hàng (nộp NN)   │
│ 334    │ Phải trả người lao động       │ Lương chưa trả          │
│ 3383   │ Bảo hiểm xã hội              │ BHXH phần DN đóng       │
│ 3384   │ Bảo hiểm y tế                │ BHYT phần DN đóng       │
└────────┴────────────────────────────────┴──────────────────────────┘
```

**Cách hiểu:** Nợ = nghĩa vụ tài chính mà công ty phải thanh toán. Khi bán hàng thu VAT, công ty giữ hộ nhà nước → phải nộp lại.

#### NHÓM 4: VỐN CHỦ SỞ HỮU — "Chủ sở hữu bỏ bao nhiêu + lãi bao nhiêu?"

```
┌────────┬────────────────────────────────┬──────────────────────────┐
│ Mã TK  │ Tên tài khoản                 │ Vai trò trong demo       │
├────────┼────────────────────────────────┼──────────────────────────┤
│ 4111   │ Vốn góp của chủ sở hữu       │ 10 tỷ ban đầu           │
│ 4212   │ Lợi nhuận chưa phân phối      │ Lãi tích lũy qua năm   │
└────────┴────────────────────────────────┴──────────────────────────┘
```

#### NHÓM 5 & 7: DOANH THU — "Kiếm tiền từ đâu?"

```
┌────────┬────────────────────────────────┬──────────────────────────┐
│ Mã TK  │ Tên tài khoản                 │ Vai trò trong demo       │
├────────┼────────────────────────────────┼──────────────────────────┤
│ 5111   │ Doanh thu bán hàng hóa        │ Bán đồ golf              │
│ 515    │ Doanh thu hoạt động tài chính  │ Lãi tiền gửi ngân hàng  │
│ 711    │ Thu nhập khác                  │ Bán tài sản cũ (50tr)   │
└────────┴────────────────────────────────┴──────────────────────────┘
```

#### NHÓM 6 & 8: CHI PHÍ — "Tốn tiền vào đâu?"

```
┌────────┬────────────────────────────────┬──────────────────────────┐
│ Mã TK  │ Tên tài khoản                 │ Vai trò trong demo       │
├────────┼────────────────────────────────┼──────────────────────────┤
│ 632    │ Giá vốn hàng bán (COGS)       │ Giá nhập của hàng đã bán│
│ 6411   │ CP nhân viên bán hàng         │ Marketing, hoa hồng     │
│ 6421   │ CP nhân viên quản lý          │ Lương văn phòng         │
│ 6422   │ CP vật liệu quản lý          │ Văn phòng phẩm          │
│ 6423   │ CP đồ dùng văn phòng         │ Nước, đồ dùng           │
│ 6424   │ CP khấu hao TSCĐ             │ Trích khấu hao hàng tháng│
│ 6427   │ CP dịch vụ mua ngoài         │ Thuê MB, điện, internet  │
│ 811    │ Chi phí khác                  │ Lỗ thanh lý TS (40tr)   │
└────────┴────────────────────────────────┴──────────────────────────┘
```

**Phân biệt 632 (COGS) và 6xx (Chi phí hoạt động):**
- **632** = giá mua hàng ĐÃ BÁN cho khách → liên quan trực tiếp tới từng đơn hàng
- **641x/642x** = chi phí vận hành hàng ngày → không liên quan cụ thể đơn hàng nào

---

## 3. Dòng chảy dữ liệu demo 3 năm

### 3.1. Thứ tự thực thi

```
Pha │ Generator                     │ Tạo ra                           │ Số lượng ước tính
────┼───────────────────────────────┼──────────────────────────────────┼──────────────────
 1  │ foundation.py                 │ FY, Cost Center, Warehouse, Tax  │ ~25 records
 2  │ vietnamese_accounting.py      │ COA, Vốn 10 tỷ, TSCĐ, Khấu hao │ ~37 Journal Entries
 3  │ (master data - có sẵn)        │ Items, Customers, Suppliers      │ ~100+ records
 4  │ stock_management.py           │ Tồn kho đầu, Restock, Transfer  │ ~65 Stock Entries
 5  │ procurement.py                │ PO → PR → PI → Payment          │ ~500+ POs
 6  │ sales_cycle.py                │ SO → DN → SI → Payment          │ ~250+ SOs
 7  │ business_expenses.py          │ Lương, Thuê, Marketing, KH      │ ~420 Journal Entries
```

### 3.2. Sơ đồ quan hệ dữ liệu

```
                    ┌─────────────┐
                    │  GÓP VỐN    │
                    │  10 tỷ VND  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐  ┌────────┐  ┌──────────┐
         │Tiền mặt│  │Ngân hàng│  │Mua TSCĐ  │
         │ 2 tỷ   │  │  8 tỷ  │  │ 770tr    │
         │ (1111) │  │ (1121) │  │(2111+VAT)│
         └────┬───┘  └───┬────┘  └────┬─────┘
              │          │             │
              │    ┌─────┴──────┐      ▼
              │    │            │  ┌──────────┐
              │    ▼            ▼  │ Khấu hao │
         ┌────┴────────┐  ┌──────┐│ hàng     │
         │  MUA HÀNG   │  │ BÁN  ││ tháng    │
         │  (Procure)  │  │ HÀNG ││ 15.8tr   │
         │             │  │(Sales)│└──────────┘
         │ PO→PR→PI→$  │  │SO→DN │
         │ ~500 đơn    │  │→SI→$ │
         │             │  │~250  │
         └──────┬──────┘  └──┬───┘
                │            │
                ▼            ▼
         ┌─────────────────────────┐
         │     KHO HÀNG (156)      │
         │                         │
         │  Nhập ← Mua hàng       │
         │  Xuất → Bán hàng       │
         │  Chuyển giữa các kho   │
         │                         │
         │  HCM ──→ Hà Nội        │
         │  HCM ──→ Fitting       │
         └─────────────────────────┘
                     │
                     ▼
         ┌─────────────────────────┐
         │   CHI PHÍ HÀNG THÁNG   │
         │                         │
         │  Lương:    150-320tr    │
         │  Thuê MB:   30-60tr    │
         │  Marketing: 15-50tr    │
         │  Điện/nước:  6-10tr    │
         │  Internet:   2-3.5tr   │
         │  Phí NH:     1-3tr     │
         │  BHXH:      21.5%      │
         │  Bảo hiểm:  8-14tr/quý│
         └─────────────────────────┘
```

### 3.3. Mô hình tăng trưởng

Demo mô phỏng công ty bán đồ golf tăng trưởng 50%/năm (`foundation.py:29-34`):

```
Năm  │ Hệ số │ Đơn mua/quý │ Đơn bán/quý │ GT trung bình │ Biên lãi gộp
─────┼────────┼─────────────┼─────────────┼───────────────┼─────────────
2023 │ 1.0x   │     20      │     30      │   15 triệu    │    25%
2024 │ 1.5x   │     30      │     45      │   18 triệu    │    28%
2025 │ 2.25x  │     45      │     68      │   22 triệu    │    30%
2026 │ 3.375x │     55      │     85      │   25 triệu    │    32%
```

**Tính mùa vụ** (`foundation.py:37-42`):

```
Q1 (Jan-Mar): 1.2x  ← Sau Tết, mùa golf bắt đầu
Q2 (Apr-Jun): 0.8x  ← Mùa thấp điểm
Q3 (Jul-Sep): 0.85x ← Thấp-trung bình
Q4 (Oct-Dec): 1.3x  ← Quà Tết, đơn cuối năm
```

---

## 4. Các luồng nghiệp vụ kế toán

### 4.1. LUỒNG MUA HÀNG (Procurement Cycle)

Đây là luồng **nhập hàng hóa vào kho** và **trả tiền cho nhà cung cấp (NCC)**.

#### Chuỗi chứng từ

```
Purchase Order ──→ Purchase Receipt ──→ Purchase Invoice ──→ Payment Entry
(Đặt hàng)        (Nhận hàng)          (Hóa đơn NCC)       (Trả tiền)
   │                    │                    │                    │
   │               Kho TĂNG             Ghi nhận            Tiền GIẢM
   │               (156 Dr)            nợ NCC              Nợ NCC HẾT
   │                                   (331 Cr)            (331 Dr)
   │                                   + VAT               (1121 Cr)
   │                                   (1331 Dr)
   │
   └──── Chưa có bút toán kế toán (chỉ là cam kết mua)
```

#### Ví dụ chi tiết: Mua 20 bộ gậy golf, đơn giá 3 triệu, VAT 10%

**Bước 1: Purchase Order** — Cam kết mua, CHƯA ghi sổ kế toán

```
Chỉ tạo đơn hàng, chưa ảnh hưởng tài khoản nào.
→ Giống việc bạn order trên Shopee nhưng chưa nhận hàng.
```

**Bước 2: Purchase Receipt** — Nhận hàng vào kho (`procurement.py:139-156`)

```
GL Entry:
  Nợ 156  Hàng hóa           60,000,000   ← Kho tăng (nhận hàng)
  Có 331  Phải trả NCC       60,000,000   ← Nợ NCC tăng (chưa trả tiền)
```

> **Nguyên tắc phát sinh (Accrual):** Ghi nhận khi NHẬN HÀNG, không phải khi trả tiền. Đây là điểm khác biệt lớn nhất giữa kế toán doanh nghiệp và ghi chép gia đình.

**Bước 3: Purchase Invoice** — Nhận hóa đơn VAT (`procurement.py:159-177`)

```
GL Entry (bổ sung VAT):
  Nợ 1331 VAT đầu vào         6,000,000   ← Quyền khấu trừ thuế
  Có 331  Phải trả NCC        6,000,000   ← Nợ NCC thêm phần VAT

Tổng nợ NCC hiện tại: 60tr + 6tr = 66 triệu
```

**Bước 4: Payment Entry** — Trả tiền cho NCC (`procurement.py:180-211`)

```
GL Entry:
  Nợ 331  Phải trả NCC       66,000,000   ← Hết nợ NCC
  Có 1121 Ngân hàng          66,000,000   ← Tiền ngân hàng giảm

⚠️ Quy định TT200: Đơn hàng ≥ 20 triệu → BẮT BUỘC chuyển khoản (không tiền mặt)
   Dưới 20 triệu → 40% tiền mặt, 60% chuyển khoản
```

#### Tỷ lệ trong demo

```
95% PO → có Purchase Receipt (5% hủy/chờ)
  ├── 80% nhận đủ hàng
  └── 15% nhận thiếu (partial)
90% PI → có Payment Entry (10% chưa trả)
```

---

### 4.2. LUỒNG BÁN HÀNG (Sales Cycle)

Đây là luồng **xuất hàng cho khách** và **thu tiền về**.

#### Chuỗi chứng từ

```
Sales Order ──→ Delivery Note ──→ Sales Invoice ──→ Payment Entry
(Đơn hàng)      (Giao hàng)       (Xuất hóa đơn)   (Thu tiền)
   │                 │                  │                 │
   │            Kho GIẢM          Ghi nhận DT        Tiền TĂNG
   │            (156 Cr)          (5111 Cr)          (1121 Dr)
   │            COGS tăng         Phải thu KH        Phải thu HẾT
   │            (632 Dr)          (131 Dr)           (131 Cr)
   │                              + VAT đầu ra
   │                              (3331 Cr)
   │
   └──── Kiểm tra tồn kho trước khi tạo!
```

#### Ví dụ chi tiết: Bán 5 bộ gậy golf, giá bán 5 triệu, giá vốn 3 triệu, VAT 10%

**Bước 1: Sales Order** — Đơn hàng, CHƯA ghi sổ

```
Kiểm tra tồn kho → build_so_items_with_stock_check() (sales_cycle.py:121-161)
Nếu kho không đủ → bỏ qua đơn hàng (skipped_no_stock++)
```

**Bước 2: Delivery Note** — Xuất kho giao hàng (`sales_cycle.py:197-219`)

```
GL Entry (Perpetual Inventory — ERPNext tự tạo):
  Nợ 632  Giá vốn hàng bán   15,000,000   ← Chi phí hàng đã bán
  Có 156  Hàng hóa            15,000,000   ← Kho giảm (giá VỐN, không phải giá bán)
```

> **COGS (Cost of Goods Sold)** = giá MUA TRUNG BÌNH của hàng đã bán, KHÔNG phải giá bán. Đây là chi phí TRỰC TIẾP nhất của việc bán hàng.

**Bước 3: Sales Invoice** — Xuất hóa đơn cho khách (`sales_cycle.py:222-249`)

```
GL Entry:
  Nợ 131  Phải thu KH        27,500,000   ← Khách nợ mình (giá bán + VAT)
  Có 5111 Doanh thu           25,000,000   ← Ghi nhận doanh thu
  Có 3331 VAT đầu ra           2,500,000   ← Thu hộ nhà nước
```

> **Due Date (hạn thanh toán):**
> - B2B (công ty): 15-45 ngày
> - B2C (cá nhân): ngay lập tức

**Bước 4: Payment Entry** — Thu tiền từ khách (`sales_cycle.py:252-284`)

```
GL Entry:
  Nợ 1121 Ngân hàng          27,500,000   ← Tiền ngân hàng tăng
  Có 131  Phải thu KH        27,500,000   ← Khách hết nợ

⚠️ TT200: ≥ 10 triệu → thu qua ngân hàng
   < 10 triệu → 60% tiền mặt, 40% ngân hàng
```

#### Lãi gộp từ giao dịch này

```
Doanh thu:     25,000,000  (5 × 5tr)
Giá vốn:      15,000,000  (5 × 3tr)
───────────────────────────────────
LÃI GỘP:      10,000,000  (margin 40%)
```

#### Tỷ lệ trong demo

```
95% SO → có Delivery Note (5% hủy)
  ├── 85% giao đủ hàng
  └── 10% giao thiếu (partial)
70-85% SI → có Payment Entry
  ├── B2B: 70% (trả chậm 7-45 ngày)
  └── B2C: 85% (trả ngay 0-7 ngày)
```

---

### 4.3. LUỒNG KHO HÀNG (Stock Management)

#### Tồn kho ban đầu (`stock_management.py:69-175`)

```
01/01/2023 — Material Receipt (Nhập kho ban đầu):

┌───────────────────────────┬──────────────┬────────────────────┐
│ Kho                       │ Số lượng/SP  │ Giá nhập           │
├───────────────────────────┼──────────────┼────────────────────┤
│ Kho Chính HCM             │ 200-500 cái  │ 60% giá bán        │
│ Kho Showroom Hà Nội       │ 30-80 cái    │ 60% giá bán        │
│ Kho Fitting               │ 5-20 cái     │ 60% giá bán        │
└───────────────────────────┴──────────────┴────────────────────┘

GL Entry (Perpetual Inventory):
  Nợ 156  Hàng hóa           xxx          ← Kho tăng
  Có      Stock Adjustment    xxx          ← Điều chỉnh số dư đầu kỳ
```

#### Luân chuyển hàng quý

```
┌──────────────────────────────────────────────────────────┐
│                    KHO CHÍNH HCM                         │
│                                                          │
│  ← Nhập từ NCC (Purchase Receipt)                        │
│  ← Restock hàng quý (50-150 cái/SP)                     │
│                                                          │
│  → Xuất bán cho KH (Delivery Note)                       │
│  → Chuyển đến Hà Nội (5-40 cái, tăng từ 2025)           │
│  → Chuyển đến Kho Fitting (2-8 cái)                      │
└──────────────────────────────────────────────────────────┘
```

#### Moving Average — Giá vốn bình quân

ERPNext tự tính giá vốn theo **Moving Average** (bình quân gia quyền liên hoàn):

```
Lần nhập 1: 100 cái × 2,000,000 = 200,000,000
  → Giá TB = 2,000,000

Lần nhập 2: 50 cái × 2,400,000 = 120,000,000
  → Giá TB = (200,000,000 + 120,000,000) / (100 + 50) = 2,133,333

Bán 30 cái:
  → COGS = 30 × 2,133,333 = 64,000,000

Tồn kho: 120 cái × 2,133,333 = 256,000,000

✅ ERPNext tự tính, kế toán không cần làm thủ công!
```

---

### 4.4. LUỒNG LƯƠNG & BẢO HIỂM (Payroll)

Mỗi tháng tạo **2 bút toán** (`business_expenses.py:209-243`):

#### Bút toán 1: TRÍCH LƯƠNG (ngày 28-30 hàng tháng)

```
Ví dụ năm 2024: Lương 200 triệu, BHXH phần DN đóng 21.5%

  Nợ 6421 CP nhân viên QL    243,000,000   ← Chi phí: lương + BHXH
  Có 334  Phải trả NLĐ      200,000,000   ← Nợ lương nhân viên
  Có 3383 BHXH                32,000,000   ← Nợ BHXH (16% lương)
  Có 3384 BHYT                11,000,000   ← Nợ BHYT (5.5% lương)
```

> **Tại sao 21.5%?** Theo luật VN, DN đóng cho nhân viên:
> - BHXH: 17% (hưu trí, ốm đau, thai sản, tai nạn)
> - BHYT: 3%
> - BHTN: 1%
> - Tổng: 21% (demo làm tròn 21.5%)

#### Bút toán 2: THANH TOÁN LƯƠNG (5 ngày sau)

```
  Nợ 334  Phải trả NLĐ      200,000,000   ← Hết nợ lương
  Có 1121 Ngân hàng          200,000,000   ← Chuyển khoản trả lương
```

#### Tăng trưởng lương qua các năm

```
Năm  │ Lương/tháng │ BHXH DN (21.5%) │ Tổng CP/tháng │ Ước tính nhân sự
─────┼─────────────┼─────────────────┼───────────────┼─────────────────
2023 │   150 tr    │     32.25 tr    │   182.25 tr   │ ~10 người
2024 │   200 tr    │     43.00 tr    │   243.00 tr   │ ~13 người
2025 │   280 tr    │     60.20 tr    │   340.20 tr   │ ~18 người
2026 │   320 tr    │     68.80 tr    │   388.80 tr   │ ~20 người
```

---

### 4.5. LUỒNG TÀI SẢN CỐ ĐỊNH (Fixed Assets)

#### Vòng đời tài sản: Mua → Khấu hao → Thanh lý

```
02/2023                    03/2023 → 03/2026                  06/2025
MUA XE TẢI                 KHẤU HAO HÀNG THÁNG               THANH LÝ TB CŨ
650tr + VAT 65tr           10.83tr/tháng × 33 tháng           Bán 50tr, lỗ 40tr
                           (650tr ÷ 60 tháng = 5 năm)
```

#### Mua tài sản (`vietnamese_accounting.py:218-244`)

```
Mua xe tải Hyundai — 15/02/2023:

  Nợ 2111 TSCĐ hữu hình     650,000,000   ← Ghi nhận tài sản
  Nợ 1331 VAT đầu vào        65,000,000   ← Khấu trừ thuế
  Có 1121 Ngân hàng          715,000,000   ← Trả tiền

Mua 5 laptop Dell — 10/01/2023:

  Nợ 242  Chi phí trả trước  120,000,000   ← Phân bổ dần 24 tháng
  Nợ 1331 VAT đầu vào         12,000,000
  Có 1121 Ngân hàng          132,000,000
```

> **Tại sao xe vào 2111 mà laptop vào 242?**
> - Xe tải > 30 triệu + sử dụng > 1 năm → **Tài sản cố định** (2111), khấu hao
> - Laptop 120tr/5 chiếc = 24tr/chiếc < 30 triệu → **Công cụ dụng cụ**, phân bổ

#### Khấu hao hàng tháng (`vietnamese_accounting.py:246-282`)

```
Hàng tháng (từ 03/2023 đến 03/2026 = 33 tháng):

  Nợ 6424 CP khấu hao TSCĐ   15,800,000
  Có 2141 Hao mòn lũy kế     10,800,000   ← Xe tải: 650tr ÷ 60 tháng
  Có 242  Chi phí trả trước    5,000,000   ← Laptop: 120tr ÷ 24 tháng
```

**Khấu hao đường thẳng (Straight-line):**

```
Khấu hao/tháng = Nguyên giá ÷ Số tháng sử dụng

Xe tải:  650,000,000 ÷ 60 tháng = 10,833,333/tháng
Laptop:  120,000,000 ÷ 24 tháng =  5,000,000/tháng

Giá trị còn lại xe tải sau 33 tháng:
  = 650tr - (10.83tr × 33) = 292.5 triệu
```

#### Thanh lý tài sản (`vietnamese_accounting.py:284-317`)

```
Tháng 06/2025: Bán thiết bị cũ — nguyên giá 100tr, đã khấu hao 60tr

Giá trị còn lại = 100tr - 60tr = 40 triệu
Bán được 50 triệu → LÃI 10 triệu? KHÔNG!

Cách ghi sổ:
  Nợ 1121 Ngân hàng           50,000,000   ← Thu tiền bán
  Nợ 2141 Hao mòn lũy kế      60,000,000   ← Xóa phần đã khấu hao
  Nợ 811  Chi phí khác         40,000,000   ← Ghi nhận giá trị còn lại
  Có 711  Thu nhập khác        50,000,000   ← Ghi nhận tiền bán
  Có 2111 TSCĐ                100,000,000   ← Xóa tài sản khỏi sổ

Kết quả: Thu nhập khác 50tr - Chi phí khác 40tr = Lãi 10 triệu ✓
```

---

### 4.6. LUỒNG CHI PHÍ VẬN HÀNH (Business Expenses)

Hàng tháng phát sinh (`business_expenses.py:29-66`):

```
┌────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Khoản mục          │ 2023     │ 2024     │ 2025     │ 2026     │
├────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Thuê mặt bằng      │  30 tr   │  35 tr   │  55 tr*  │  60 tr   │
│ Điện nước          │   6 tr   │   7 tr   │   9 tr   │  10 tr   │
│ Internet           │   2 tr   │ 2.5 tr   │   3 tr   │ 3.5 tr   │
│ Marketing          │  15 tr   │  25 tr   │  40 tr   │  50 tr   │
│ Lương (đã tính ở trên)│ 150 tr │ 200 tr   │ 280 tr   │ 320 tr   │
│ Phí ngân hàng      │   1 tr   │ 1.5 tr   │ 2.5 tr   │   3 tr   │
├────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ TỔNG/tháng (ước)   │ ~204 tr  │ ~271 tr  │ ~389 tr  │ ~447 tr  │
├────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Bảo hiểm (quý)     │   8 tr   │  10 tr   │  12 tr   │  14 tr   │
│ Khấu hao/tháng     │   5 tr   │   5 tr   │   8 tr   │   8 tr   │
└────────────────────┴──────────┴──────────┴──────────┴──────────┘

* 2025 thuê tăng vọt vì mở Showroom Hà Nội
```

#### Mapping tài khoản chi phí

```
Thuê mặt bằng  → 6427 (CP dịch vụ mua ngoài)  ← Cost Center: Kế toán
Điện nước      → 6427                          ← Cost Center: Kho vận
Marketing      → 6411 (CP NV bán hàng)          ← Cost Center: Marketing
Lương          → 6421 (CP NV quản lý)           ← Cost Center: Kế toán
Phí NH         → 6427                          ← Cost Center: Kế toán
Bảo hiểm       → 6421                          ← Quý (tháng 3, 6, 9, 12)
Khấu hao       → 6424 → Có 2141                ← Cost Center: Kế toán
```

---

### 4.7. LUỒNG THUẾ VAT (Value Added Tax)

VAT là thuế **giá trị gia tăng** — đánh thuế trên phần TĂNG THÊM giá trị ở mỗi khâu.

```
NCC bán cho DCNET        DCNET bán cho khách
giá 3tr + VAT 10%       giá 5tr + VAT 10%
= 3.3tr                  = 5.5tr

                  DCNET
                  ┌──────────────────────┐
      Trả 300K   │  VAT đầu vào: 300K   │   Thu 500K
    (VAT mua) ←──┤  VAT đầu ra:  500K   ├──→ (VAT bán)
                  │  ─────────────────── │
                  │  Nộp nhà nước: 200K  │
                  │  = 500K - 300K       │
                  └──────────────────────┘
```

**Trong sổ sách:**

```
TK 1331 (VAT đầu vào) — Tài sản: số tiền VAT đã trả cho NCC
  → Quyền được khấu trừ (giảm thuế phải nộp)
  → Số dư Nợ (bình thường)

TK 3331 (VAT đầu ra) — Nợ phải trả: số tiền VAT thu từ KH
  → Nghĩa vụ nộp nhà nước
  → Số dư Có (bình thường)

Cuối tháng: Thuế phải nộp = Số dư 3331 - Số dư 1331
  Nếu 3331 > 1331 → Nộp thuế
  Nếu 1331 > 3331 → Được hoàn thuế (carry forward)
```

---

## 5. Báo cáo tài chính

Tất cả bút toán trên cuối cùng đổ vào **3 báo cáo tài chính chính**:

### 5.1. Bảng cân đối kế toán (Balance Sheet)

> **Trả lời câu hỏi: "Tại thời điểm X, công ty CÓ GÌ và NỢ GÌ?"**

```
┌──────────────────────────────────┬───────────────────────────────────┐
│        TÀI SẢN                   │         NGUỒN VỐN                 │
├──────────────────────────────────┼───────────────────────────────────┤
│ A. TÀI SẢN NGẮN HẠN            │ C. NỢ PHẢI TRẢ                   │
│                                  │                                   │
│ Tiền mặt (1111)           xxx   │ Phải trả NCC (331)          xxx  │
│ Ngân hàng (1121+1122)     xxx   │ Thuế phải nộp (3331)        xxx  │
│ Phải thu KH (131)         xxx   │ Lương chưa trả (334)        xxx  │
│ VAT đầu vào (1331)        xxx   │ BHXH/BHYT (3383+3384)       xxx  │
│ Hàng tồn kho (156)        xxx   │                                   │
│                                  │                                   │
│ B. TÀI SẢN DÀI HẠN             │ D. VỐN CHỦ SỞ HỮU               │
│                                  │                                   │
│ TSCĐ (2111)               xxx   │ Vốn góp (4111)              xxx  │
│ - Hao mòn (2141)         (xxx)  │ Lãi chưa PP (4212)          xxx  │
│ Chi phí trả trước (242)   xxx   │                                   │
│                                  │                                   │
├──────────────────────────────────┼───────────────────────────────────┤
│ TỔNG TÀI SẢN              XXX   │ TỔNG NGUỒN VỐN              XXX  │
│                                  │                                   │
│          ★ LUÔN LUÔN BẰNG NHAU (A+B = C+D) ★                       │
└──────────────────────────────────┴───────────────────────────────────┘
```

### 5.2. Báo cáo kết quả kinh doanh (Profit & Loss / P&L)

> **Trả lời câu hỏi: "Trong kỳ, công ty LÃI hay LỖ bao nhiêu?"**

```
  Doanh thu bán hàng (5111)                          +xxx
- Giá vốn hàng bán (632)                              -xxx
  ──────────────────────────────────────────────────────────
= LÃI GỘP (Gross Profit)                              xxx
  (Biên lãi gộp = Lãi gộp / Doanh thu)

- Chi phí bán hàng (6411: Marketing, NV bán hàng)     -xxx
- Chi phí quản lý (6421: Lương, 6427: Thuê, Điện...)  -xxx
- Chi phí khấu hao (6424)                             -xxx
  ──────────────────────────────────────────────────────────
= LÃI THUẦN TỪ HOẠT ĐỘNG KINH DOANH                  xxx

+ Thu nhập khác (711: Bán TS cũ)                       +xxx
- Chi phí khác (811: Lỗ thanh lý)                      -xxx
  ──────────────────────────────────────────────────────────
= LÃI TRƯỚC THUẾ (Profit Before Tax)                  xxx

- Thuế TNDN (20%)                                     -xxx
  ──────────────────────────────────────────────────────────
= LÃI SAU THUẾ (Net Profit)                           xxx
  → Chuyển vào TK 4212 (Lợi nhuận chưa phân phối)
```

### 5.3. Báo cáo lưu chuyển tiền tệ (Cash Flow Statement)

> **Trả lời câu hỏi: "Tiền THỰC SỰ đi đâu, đến từ đâu?"**

```
I. Tiền từ hoạt động kinh doanh:
   + Thu tiền từ khách hàng (Payment Entry - Sales)
   - Trả tiền cho NCC (Payment Entry - Purchase)
   - Trả lương nhân viên
   - Nộp thuế
   - Trả tiền thuê, điện, internet...
   ──────────────────────────────────
   = Dòng tiền kinh doanh                  xxx

II. Tiền từ hoạt động đầu tư:
   - Mua TSCĐ (xe tải: -715tr, laptop: -132tr)
   + Bán TSCĐ cũ (+50tr)
   ──────────────────────────────────
   = Dòng tiền đầu tư                     (xxx)

III. Tiền từ hoạt động tài chính:
   + Góp vốn CSH (+10 tỷ)
   - Chia cổ tức (0 trong demo)
   ──────────────────────────────────
   = Dòng tiền tài chính                   xxx

──────────────────────────────────────────
Tăng/giảm tiền trong kỳ = I + II + III    xxx
Tiền đầu kỳ                               xxx
Tiền cuối kỳ (= 1111 + 1121 + 1122)       XXX
```

> **Lãi ≠ Có tiền!** Công ty có thể LÃI trên P&L nhưng HẾT TIỀN trên Cash Flow (vì KH nợ nhiều, hàng tồn kho lớn, đầu tư TSCĐ). Đây là lý do nhiều DN lãi mà vẫn phá sản.

---

## 6. ERPNext & Kế toán tự động

### 6.1. Perpetual Inventory — Kế toán tồn kho liên tục

ERPNext dùng hệ thống **Perpetual Inventory**, nghĩa là:

```
Mỗi khi stock di chuyển → ERPNext TỰ ĐỘNG tạo GL Entry

Purchase Receipt (nhận hàng):
  → Stock Ledger: +qty vào warehouse
  → GL Entry: Nợ 156 / Có 331 (tự động)

Delivery Note (giao hàng):
  → Stock Ledger: -qty từ warehouse
  → GL Entry: Nợ 632 / Có 156 (tự động, theo Moving Average)

Kế toán KHÔNG CẦN ghi bút toán kho thủ công!
```

### 6.2. ERPNext tự động tạo bao nhiêu GL Entry?

```
1 Purchase Invoice submit = tối thiểu 3 GL Entries:
  Nợ 156 (Hàng hóa)
  Nợ 1331 (VAT đầu vào)
  Có 331 (Phải trả NCC)

1 Sales Invoice submit = tối thiểu 3 GL Entries:
  Nợ 131 (Phải thu KH)
  Có 5111 (Doanh thu)
  Có 3331 (VAT đầu ra)

1 Payment Entry submit = 2 GL Entries:
  Nợ/Có tài khoản tiền
  Có/Nợ tài khoản công nợ
```

### 6.3. Chuỗi chứng từ liên kết trong ERPNext

```
ERPNext sử dụng "against" links để liên kết chứng từ:

Purchase Order ─── purchase_order field ──→ Purchase Receipt
Purchase Receipt ─ purchase_receipt field ──→ Purchase Invoice
Purchase Invoice ─ references table ──────→ Payment Entry

Tương tự:
Sales Order ─── sales_order field ──→ Delivery Note
Delivery Note ─ delivery_note field ──→ Sales Invoice
Sales Invoice ─ references table ───→ Payment Entry

→ Có thể trace ngược từ Payment → Invoice → Receipt → Order
```

### 6.4. Cost Center — Phân tích chi phí theo bộ phận

Demo tạo 8 Cost Centers (`foundation.py:97-107`) cho phép phân tích:

```
              Công ty (Root)
              ├── Ban Giám đốc
              ├── Kinh doanh (Group)
              │   ├── Bán lẻ
              │   └── Bán sỉ
              ├── Kho vận
              ├── Kế toán
              ├── Fitting & Dịch vụ
              └── Marketing

→ Báo cáo theo Cost Center cho biết bộ phận nào tốn bao nhiêu:
  Marketing: 15-50tr/tháng (6411)
  Kho vận: 6-10tr/tháng điện nước (6427)
  Kế toán: 30-60tr/tháng thuê + 1-3tr phí NH (6427)
```

---

## 7. Bài tập tự kiểm tra

### Bài 1: Phương trình kế toán

Sau các giao dịch sau, hãy tính số dư từng tài khoản:

```
1. Góp vốn 10 tỷ (2 tỷ tiền mặt + 8 tỷ ngân hàng)
2. Mua xe tải 650tr + VAT 10% = 715tr (trả qua ngân hàng)
3. Nhập kho hàng hóa 500tr (chưa trả NCC)
4. Bán hàng giá vốn 200tr, giá bán 350tr + VAT 10% (KH chưa trả)
5. KH trả tiền 385tr vào ngân hàng
```

<details>
<summary>Đáp án</summary>

```
1111 Tiền mặt:      +2,000,000,000
1121 Ngân hàng:      +8,000,000,000 - 715,000,000 + 385,000,000 = 7,670,000,000
131  Phải thu KH:    +385,000,000 - 385,000,000 = 0
1331 VAT vào:        +65,000,000
156  Hàng hóa:       +500,000,000 - 200,000,000 = 300,000,000
2111 TSCĐ:           +650,000,000
331  Phải trả NCC:   +500,000,000
3331 VAT ra:         +35,000,000
4111 Vốn CSH:        +10,000,000,000
5111 Doanh thu:      +350,000,000
632  Giá vốn:        +200,000,000

Kiểm tra phương trình:
Tài sản: 2,000 + 7,670 + 0 + 65 + 300 + 650 = 10,685 triệu
Nợ + Vốn: 500 + 35 + 10,000 + (350 - 200) = 10,685 triệu ✓
```

</details>

### Bài 2: Ghi sổ kép

Ghi bút toán cho các giao dịch sau:

```
a) Trả tiền thuê văn phòng 30 triệu bằng chuyển khoản
b) Thu tiền mặt từ KH 5 triệu (KH đã mua hàng trước đó)
c) Trích lương tháng 200 triệu + BHXH 21.5%
d) Nhập kho 100 sản phẩm golf, đơn giá 2 triệu, VAT 10%, chưa trả tiền
```

<details>
<summary>Đáp án</summary>

```
a) Thuê văn phòng:
   Nợ 6427 CP dịch vụ mua ngoài    30,000,000
   Có 1121 Ngân hàng               30,000,000

b) Thu tiền KH:
   Nợ 1111 Tiền mặt                 5,000,000
   Có 131  Phải thu KH              5,000,000

c) Trích lương:
   Nợ 6421 CP NV quản lý          243,000,000  (200tr + 43tr BHXH)
   Có 334  Phải trả NLĐ          200,000,000
   Có 3383 BHXH                    32,000,000  (200tr × 16%)
   Có 3384 BHYT                    11,000,000  (200tr × 5.5%)

d) Nhập kho hàng golf:
   Nợ 156  Hàng hóa              200,000,000  (100 × 2tr)
   Nợ 1331 VAT đầu vào            20,000,000  (200tr × 10%)
   Có 331  Phải trả NCC          220,000,000
```

</details>

### Bài 3: Tính lãi gộp

```
Quý 1/2024 DCNET bán được:
- 45 đơn hàng, giá trị trung bình 18 triệu (chưa VAT)
- Hệ số mùa vụ Q1: 1.2x → thực tế: 54 đơn
- Biên lãi gộp: 28%

Hỏi:
a) Doanh thu Q1/2024?
b) Giá vốn Q1/2024?
c) Lãi gộp Q1/2024?
d) Nếu chi phí vận hành 271 triệu/tháng × 3 = 813 triệu, lãi ròng Q1?
```

<details>
<summary>Đáp án</summary>

```
a) Doanh thu = 54 đơn × 18 triệu = 972 triệu

b) Giá vốn = 972 × (1 - 0.28) = 972 × 0.72 = 699.84 triệu

c) Lãi gộp = 972 - 699.84 = 272.16 triệu
   (Kiểm tra: 272.16 / 972 = 28% ✓)

d) Lãi ròng = 272.16 - 813 = -540.84 triệu (LỖ!)

→ Q1/2024 vẫn LỖ vì chi phí cố định cao hơn lãi gộp.
   Đây là giai đoạn đầu, doanh nghiệp cần scale để cover chi phí cố định.
   Từ 2025-2026 khi DT tăng mạnh, lãi gộp sẽ vượt chi phí → có lãi.
```

</details>

### Bài 4: Hiểu dòng tiền

```
Tháng 3/2024, DCNET có:
- Bán hàng 500 triệu (nhưng KH B2B trả chậm 30 ngày, chưa thu)
- Mua hàng 300 triệu (đã trả ngay qua ngân hàng)
- Trả lương 200 triệu
- Thuê mặt bằng 35 triệu

Hỏi:
a) P&L tháng 3 lãi hay lỗ?
b) Dòng tiền thực tháng 3?
c) Giải thích nghịch lý nếu có.
```

<details>
<summary>Đáp án</summary>

```
a) P&L tháng 3:
   Doanh thu:    +500 triệu
   Giá vốn:     -300 triệu (ước tính = giá mua)
   Lương:       -200 triệu
   Thuê:         -35 triệu
   ────────────────────────
   LỖ:           -35 triệu

b) Dòng tiền thực:
   Thu từ KH:       0 triệu (chưa thu do trả chậm 30 ngày!)
   Trả NCC:      -300 triệu
   Trả lương:    -200 triệu
   Thuê:          -35 triệu
   ────────────────────────
   Dòng tiền:    -535 triệu (tiền giảm 535 triệu)

c) Nghịch lý:
   P&L lỗ 35 triệu nhưng tiền giảm tới 535 triệu!
   Lý do: KH B2B chưa trả 500 triệu (nằm ở TK 131 - Phải thu).
   → "Có lãi" nhưng "hết tiền" là chuyện THƯỜNG XẢY RA.
   → Quản lý dòng tiền (Cash Flow) quan trọng ngang quản lý lợi nhuận.
```

</details>

### Bài 5: VAT cân đối

```
Quý 2/2024:
- Mua hàng: 1 tỷ (chưa VAT), VAT 10%
- Bán hàng: 800 triệu (chưa VAT), VAT 10%

Hỏi:
a) VAT đầu vào (1331)?
b) VAT đầu ra (3331)?
c) Thuế phải nộp nhà nước?
d) Nếu VAT vào > VAT ra, chuyện gì xảy ra?
```

<details>
<summary>Đáp án</summary>

```
a) VAT đầu vào = 1 tỷ × 10% = 100 triệu (TK 1331)
b) VAT đầu ra = 800 triệu × 10% = 80 triệu (TK 3331)
c) Thuế phải nộp = 80 triệu - 100 triệu = -20 triệu
   → Âm! Nghĩa là nhà nước NỢ DCNET 20 triệu
d) VAT vào > VAT ra → Được khấu trừ (carry forward) sang quý sau.
   Hoặc nếu quá lớn + kéo dài → xin hoàn thuế VAT.

   Tại sao xảy ra? Vì quý này nhập hàng nhiều (tích kho),
   nhưng bán chưa hết → VAT mua > VAT bán.
```

</details>

---

## Phụ lục: Thuật ngữ

| Tiếng Việt | Tiếng Anh | Viết tắt | Giải thích |
|-----------|-----------|----------|------------|
| Bút toán | Journal Entry | JE | Một giao dịch kế toán ghi sổ |
| Sổ cái | General Ledger | GL | Sổ ghi toàn bộ giao dịch theo tài khoản |
| Bảng CĐKT | Balance Sheet | BS | Ảnh chụp tài chính tại 1 thời điểm |
| BCKQKD | Profit & Loss | P&L | Lãi/lỗ trong 1 kỳ |
| BCLCTT | Cash Flow Statement | CF | Dòng tiền thực trong 1 kỳ |
| Giá vốn | Cost of Goods Sold | COGS | Giá mua của hàng đã bán |
| Tài sản cố định | Fixed Asset | FA/TSCĐ | Tài sản > 30tr, dùng > 1 năm |
| Khấu hao | Depreciation | Dep | Trích chi phí TSCĐ theo thời gian |
| Phải thu | Accounts Receivable | AR | Tiền KH nợ mình |
| Phải trả | Accounts Payable | AP | Tiền mình nợ NCC |
| VAT đầu vào | Input VAT | - | VAT trả cho NCC (khấu trừ) |
| VAT đầu ra | Output VAT | - | VAT thu từ KH (nộp NN) |
| Biên lãi gộp | Gross Margin | GM | (DT - COGS) / DT × 100% |
| Đòn bẩy hoạt động | Operating Leverage | - | CP cố định cao → lãi tăng nhanh khi DT tăng |
| Bình quân gia quyền | Moving Average | MA | Cách tính giá vốn TB sau mỗi lần nhập |

---

> **File liên quan:**
> - `docs/accounting/COA_ANALYSIS.md` — Phân tích chi tiết COA
> - `docs/accounting/ChartOfAccountsImporter_v2.csv` — File COA dùng để import
> - `dcnet_apps/dcnet_fixtures/dcnet_fixtures/generators/` — Source code 6 generators
>
> **Cập nhật:** 07/03/2026
