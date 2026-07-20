# Hướng Dẫn Sử Dụng Module Dashboard

> **Hệ thống:** DCNET Flow
> **Phiên bản:** 1.0 | **Ngày:** 16/02/2026
> **Đối tượng:** Quản lý cửa hàng, Kế toán, Nhân viên bán hàng

---

## Mục Lục

1. [Giới Thiệu](#1-giới-thiệu)
2. [Truy Cập Dashboard](#2-truy-cập-dashboard)
3. [Tổng Quan Giao Diện](#3-tổng-quan-giao-diện)
4. [Number Card — Chỉ Số Doanh Số](#4-number-card--chỉ-số-doanh-số)
5. [Biểu Đồ Doanh Số Theo Nguồn Khách Hàng](#5-biểu-đồ-doanh-số-theo-nguồn-khách-hàng)
6. [Biểu Đồ Doanh Số Theo Nguồn Đơn Hàng](#6-biểu-đồ-doanh-số-theo-nguồn-đơn-hàng)
7. [Biểu Đồ Top 20 Sản Phẩm Bán Chạy](#7-biểu-đồ-top-20-sản-phẩm-bán-chạy)
8. [Sử Dụng Bộ Lọc](#8-sử-dụng-bộ-lọc)
9. [Xem Báo Cáo Chi Tiết](#9-xem-báo-cáo-chi-tiết)
10. [Widget Mở Rộng (T4-T8)](#10-widget-mở-rộng-t4-t8)
11. [Câu Hỏi Thường Gặp (FAQ)](#11-câu-hỏi-thường-gặp-faq)
12. [Phụ Lục](#12-phụ-lục)

---

## 1. Giới Thiệu

Dashboard là trang tổng quan doanh số của DCNET Flow. Tại đây, bạn có thể theo dõi nhanh tình hình kinh doanh thông qua các chỉ số và biểu đồ trực quan.

### Dashboard cung cấp gì?

| STT | Thông tin | Hình thức | Mô tả |
|-----|-----------|-----------|-------|
| 1 | Doanh số tổng | Number Card | Tổng doanh số tháng hiện tại, có so sánh % với tháng trước |
| 2 | Doanh số bán sỉ | Number Card | Doanh số từ khách sỉ (đại lý), có so sánh % |
| 3 | Doanh số bán lẻ | Number Card | Doanh số từ khách lẻ (tất cả kênh), có so sánh % |
| 4 | Doanh số theo nguồn KH | Biểu đồ cột | Phân bổ doanh số theo nguồn khách hàng (Cửa hàng, Facebook, Zalo...) |
| 5 | Doanh số theo nguồn đơn | Biểu đồ cột | Phân bổ doanh số theo kênh bán (Online, Offline, TMĐT...) |
| 6 | Top 20 SP bán chạy | Biểu đồ cột | 20 sản phẩm có doanh số cao nhất |

### Nguồn dữ liệu

Dashboard lấy dữ liệu từ **Hóa đơn bán hàng** (Sales Invoice) đã được xác nhận (submitted). Chỉ những hóa đơn đã duyệt mới được tính vào doanh số.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     LUỒNG DỮ LIỆU DASHBOARD                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────┐    ┌────────────────┐    ┌──────────────────────┐   │
│  │  Đơn hàng  │───▶│  Hóa đơn bán   │───▶│     DASHBOARD        │   │
│  │(Sales Order)│   │(Sales Invoice) │    │  Number Card + Chart │   │
│  └────────────┘    └────────────────┘    └──────────────────────┘   │
│                          │                                          │
│                    Phải Submit                                      │
│                    (xác nhận)                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Truy Cập Dashboard

### Cách 1: Từ trang Home (Desktop)

1. Mở trình duyệt, truy cập DCNET Flow
2. Tại trang Home, click vào icon **Dashboard** (icon biểu đồ, vị trí đầu tiên)

### Cách 2: Từ Sidebar

1. Tại bất kỳ trang nào, nhìn sang **sidebar bên trái**
2. Click vào **Dashboard** trong nhóm "Modules"

### Cách 3: Tìm kiếm nhanh

1. Nhấn phím `/` hoặc click vào ô tìm kiếm trên thanh điều hướng
2. Gõ "Dashboard"
3. Chọn **Dashboard** từ kết quả

```
┌─────────────────────────────────────────────────────────────────────┐
│ DCNET Flow    [Tìm kiếm hoặc nhập lệnh...]              🔔  ⚙  ĐN │
├──────────┬──────────────────────────────────────────────────────────┤
│ Modules  │                                                         │
│ ■ Dashboard ◄── Bạn đang ở đây                                    │
│   Sản phẩm│                                                        │
│   NCC     │                                                         │
│   Mua hàng│                                                         │
│──────────│                                                         │
│ Bán hàng │                                                         │
│   Đơn hàng│                                                        │
│   Bán lẻ  │                                                        │
│   Bán sỉ  │                                                        │
│──────────│                                                         │
│Kho & Kế toán│                                                      │
│   Kho hàng│                                                        │
│   Kế toán │                                                        │
│──────────│                                                         │
│ CRM      │                                                         │
│   Khách hàng│                                                      │
│   Lead    │                                                        │
│   Fitting │                                                        │
└──────────┴──────────────────────────────────────────────────────────┘
```

---

## 3. Tổng Quan Giao Diện

Giao diện Dashboard gồm 5 khu vực chính, sắp xếp từ trên xuống:

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Dashboard                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  (A) BỘ LỌC                                                        │
│  [Ngày] [Tháng] [Quý] [Năm]  Từ [__/__/____] Đến [__/__/____]    │
│                                            Chi nhánh [Tất cả ▼]    │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  (B) TỔNG QUAN DOANH SỐ ──────────────────────────── [T3]          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ DOANH SỐ TỔNG│  │  BÁN SỈ      │  │  BÁN LẺ      │             │
│  │2.847.500.000đ│  │1.923.000.000đ│  │  924.500.000đ│              │
│  │  ▲ 12.5%     │  │  ▲ 8.3%      │  │  ▲ 18.7%     │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  (C) PHÂN TÍCH DOANH SỐ ──────────────────────────── [T3]          │
│  ┌─────────────────────┐  ┌─────────────────────┐                   │
│  │DS theo nguồn KH     │  │DS theo nguồn đơn    │                   │
│  │ ████████░ Cửa hàng  │  │ █████░░░ Offline    │                   │
│  │ ██████░░░ Facebook   │  │ ███░░░░░ Online     │                   │
│  │ ███░░░░░░ Zalo       │  │ █░░░░░░░ TMĐT      │                   │
│  │ ██░░░░░░░ Website    │  │ ░░░░░░░░ Khác      │                   │
│  │ █░░░░░░░░ Giới thiệu │  │                     │                   │
│  └─────────────────────┘  └─────────────────────┘                   │
│                                                                     │
│  ┌──────────────────────────────────────────────┐                   │
│  │ Top 20 sản phẩm bán chạy                    │                   │
│  │ █████████████████░ Gậy Driver TM Qi35   425tr│                   │
│  │ ██████████████░░░░ Set Sắt Mizuno       348tr│                   │
│  │ ███████████░░░░░░░ Bóng golf Titleist   276tr│                   │
│  │ ██████████░░░░░░░░ Áo Polo Malbon       234tr│                   │
│  │ ...                                          │                   │
│  │        Hiển thị 10/20 — Xem đầy đủ →        │                   │
│  └──────────────────────────────────────────────┘                   │
│                                                                     │
├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
│                                                                     │
│  (D) WIDGET MỞ RỘNG (viền nét đứt, nền xám)                       │
│  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐           │
│  │ Fitting [T6]                                         │           │
│  │ [  —  ] [  —  ] [  —  ] [  —  ]                     │           │
│  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘           │
│  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐           │
│  │ Trade-in [T4]                                        │           │
│  │ [  —  ] [  —  ] [  —  ] [  —  ]                     │           │
│  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘           │
│  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐           │
│  │ Coaching [T6 — chỉ Thăng Long TM]                   │           │
│  │ [  —  ] [  —  ] [  —  ] [  —  ]                     │           │
│  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

(A) Bộ lọc thời gian + chi nhánh
(B) 3 Number Card — chỉ số doanh số chính
(C) 3 biểu đồ cột — phân tích theo nguồn + top sản phẩm
(D) Widget tương lai — viền nét đứt, giá trị "—", tự hiện khi module deploy
```

---

## 4. Number Card — Chỉ Số Doanh Số

Dashboard hiển thị 3 Number Card ở hàng đầu:

### 4.1. Doanh số tổng

| Thông tin | Mô tả |
|-----------|-------|
| **Giá trị** | Tổng doanh số (grand_total) từ tất cả Hóa đơn bán hàng đã submit trong tháng |
| **Trend** | % tăng/giảm so với cùng kỳ tháng trước |
| **Màu** | Xanh dương |

### 4.2. Doanh số bán sỉ

| Thông tin | Mô tả |
|-----------|-------|
| **Giá trị** | Doanh số từ khách hàng thuộc nhóm **"Khách sỉ"** |
| **Trend** | % tăng/giảm so với tháng trước |
| **Màu** | Xanh lá |

### 4.3. Doanh số bán lẻ

| Thông tin | Mô tả |
|-----------|-------|
| **Giá trị** | Doanh số từ khách hàng thuộc nhóm **"Khách lẻ"** |
| **Trend** | % tăng/giảm so với tháng trước |
| **Màu** | Cam |

### Cách đọc Number Card

```
┌──────────────────────────┐
│ DOANH SỐ TỔNG       💰  │  ← Tiêu đề + icon
│                          │
│ 2.847.500.000đ           │  ← Giá trị (định dạng VND, hậu tố đ)
│                          │
│ ▲ 12.5%  so với tháng   │  ← Trend: xanh = tăng, đỏ = giảm
│          trước           │
└──────────────────────────┘
```

- **Mũi tên xanh (▲)**: Doanh số tăng so với tháng trước → tốt
- **Mũi tên đỏ (▼)**: Doanh số giảm so với tháng trước → cần chú ý
- Giá trị hiển thị **số đầy đủ** (2.847.500.000đ), không viết tắt (2,85 B)

---

## 5. Biểu Đồ Doanh Số Theo Nguồn Khách Hàng

Biểu đồ này trả lời câu hỏi: **"Khách hàng đến từ đâu?"**

### Các nguồn khách hàng

| Nguồn | Mô tả |
|-------|-------|
| **Cửa hàng** | Khách đến trực tiếp cửa hàng mua |
| **Facebook** | Khách tìm hiểu và đặt hàng qua Facebook |
| **Zalo** | Khách liên hệ qua Zalo |
| **Website** | Khách đặt hàng qua website |
| **Giới thiệu** | Khách được người quen giới thiệu |
| **Không rõ** | Chưa xác định nguồn (chưa có thông tin Lead) |

### Dữ liệu mẫu (theo mockup)

```
Cửa hàng    ████████████████░░  1.215tr
Facebook    ████████████░░░░░░  885tr
Zalo        █████░░░░░░░░░░░░░  398tr
Website     ███░░░░░░░░░░░░░░░  250tr
Giới thiệu  █░░░░░░░░░░░░░░░░░  99.5tr
```

- Thanh càng dài = doanh số càng cao
- Số tiền hiển thị bên phải mỗi thanh
- Dữ liệu lấy từ: Hóa đơn bán hàng → Khách hàng → Lead → Nguồn UTM

### Nút hành động trên biểu đồ

Mỗi biểu đồ có 2 nút ở góc phải trên:

| Nút | Chức năng |
|-----|-----------|
| **Làm mới** (icon xoay) | Tải lại dữ liệu biểu đồ |
| **Phóng to** (icon mở rộng) | Mở biểu đồ toàn màn hình để xem chi tiết |

> **Lưu ý:** Nguồn khách hàng chỉ hiển thị chính xác khi khách hàng có thông tin Lead (module Lead, T6). Trước đó, phần lớn sẽ hiển thị "Không rõ".

### Xem báo cáo chi tiết

Click vào tiêu đề biểu đồ hoặc vào Sidebar > **DS theo nguồn KH** để mở báo cáo đầy đủ với bộ lọc.

---

## 6. Biểu Đồ Doanh Số Theo Nguồn Đơn Hàng

Biểu đồ này trả lời câu hỏi: **"Đơn hàng đến từ kênh nào?"**

### Các nguồn đơn hàng

| Nguồn | Mô tả |
|-------|-------|
| **Offline** | Đơn hàng tại cửa hàng (bán trực tiếp) |
| **Online** | Đơn hàng qua website, app |
| **TMĐT** | Đơn hàng từ sàn thương mại điện tử (Shopee, Lazada...) |
| **Facebook** | Đơn hàng qua Facebook Shop/Messenger |
| **Zalo** | Đơn hàng qua Zalo Shop |
| **Website** | Đơn hàng từ website riêng |
| **Khác** | Kênh khác |
| **Không rõ** | Chưa chọn nguồn đơn |

### Dữ liệu mẫu (theo mockup)

```
Offline     ██████████░░░░░░░░  1.566tr
Online      █████░░░░░░░░░░░░░  854tr
TMĐT        ██░░░░░░░░░░░░░░░░  285tr
Khác        █░░░░░░░░░░░░░░░░░  142.5tr
```

- Dữ liệu lấy từ trường **Nguồn đơn hàng** (`custom_order_source`) trên Hóa đơn bán hàng

> **Lưu ý:** Trường "Nguồn đơn hàng" cần được chọn khi tạo Đơn hàng (Sales Order). Nếu không chọn, đơn sẽ hiển thị "Không rõ" trên biểu đồ.

---

## 7. Biểu Đồ Top 20 Sản Phẩm Bán Chạy

Biểu đồ này trả lời câu hỏi: **"Sản phẩm nào bán chạy nhất?"**

### Thông tin hiển thị

| Cột | Mô tả |
|-----|-------|
| **Tên sản phẩm** | Tên đầy đủ của sản phẩm |
| **Thanh biểu đồ** | Chiều dài tương ứng với doanh số |
| **Giá trị** | Doanh số (VND) và số lượng bán |

### Dữ liệu mẫu (theo mockup)

```
Gậy Driver TM Qi35         █████████████████████  425tr (85 cái)
Set Sắt Mizuno JPX925       ████████████████░░░░░  348tr (29 bộ)
Bóng golf Titleist V1       █████████████░░░░░░░░  276tr (230 hộp)
Áo Polo Malbon SS26         ███████████░░░░░░░░░░  234tr (156 cái)
Giày golf Ecco Biom         ██████████░░░░░░░░░░░  204tr (68 đôi)
Túi gậy Vessel Player       █████████░░░░░░░░░░░░  178tr (36 cái)
Găng tay FootJoy Pure       ██████░░░░░░░░░░░░░░░  128tr (320 đôi)
Gậy Putter Scotty Cam       █████░░░░░░░░░░░░░░░░  115tr (15 cái)
Mũ Titleist Tour Elite      ████░░░░░░░░░░░░░░░░░  76.5tr (153 cái)
Ô golf Callaway 68"         ██░░░░░░░░░░░░░░░░░░░  51tr (102 cái)
```

- Sản phẩm xếp từ trên xuống theo doanh số giảm dần
- Mặc định hiển thị **Top 20** (có thể thay đổi trong báo cáo chi tiết)
- Trên Dashboard chỉ hiển thị 10 sản phẩm đầu. Click **"Xem đầy đủ →"** để mở báo cáo

---

## 8. Sử Dụng Bộ Lọc

### Bộ lọc thời gian nhanh

```
[Ngày] [Tháng] [Quý] [Năm]
```

| Nút | Khoảng thời gian |
|-----|-----------------|
| **Ngày** | Chỉ ngày hôm nay |
| **Tháng** | Từ đầu tháng đến hôm nay (mặc định) |
| **Quý** | Từ đầu quý đến cuối quý |
| **Năm** | Cả năm |

Click vào nút tương ứng để thay đổi — Number Card và biểu đồ sẽ tự động cập nhật.

### Bộ lọc ngày tùy chọn

| Trường | Mô tả |
|--------|-------|
| **Từ** | Ngày bắt đầu |
| **Đến** | Ngày kết thúc |

Nhập ngày trực tiếp hoặc click vào ô để mở lịch chọn ngày.

### Bộ lọc chi nhánh

```
Chi nhánh: [Tất cả ▼]
```

Các tùy chọn: Tất cả, HN - Cầu Giấy, HN - Hai Bà Trưng, HCM - Q1, HCM - Q7

Chọn chi nhánh cụ thể để xem doanh số của riêng chi nhánh đó. Chọn "Tất cả" để xem tổng.

> **Lưu ý:** Bộ lọc chi nhánh tương ứng với trường **Company** trong ERPNext. Mỗi chi nhánh là một Company riêng.

---

## 9. Xem Báo Cáo Chi Tiết

Từ Dashboard, bạn có thể truy cập 3 báo cáo chi tiết:

### Cách truy cập

**Cách 1:** Click vào tiêu đề biểu đồ trên Dashboard

**Cách 2:** Vào Sidebar > mục **Báo cáo**:
- DS theo nguồn KH
- DS theo nguồn đơn
- Top 20 SP bán chạy

### Báo cáo có bộ lọc riêng

Mỗi báo cáo đều có bộ lọc chi tiết hơn Dashboard:

| Bộ lọc | Mô tả | Mặc định |
|--------|-------|----------|
| **Company** | Công ty/Chi nhánh | Công ty mặc định của bạn |
| **Từ ngày** | Ngày bắt đầu | 12 tháng trước |
| **Đến ngày** | Ngày kết thúc | Hôm nay |
| **Top N** | Số sản phẩm (chỉ Top SP) | 20 |

### Xuất báo cáo

Tại trang báo cáo, bạn có thể:
1. **In**: Click **Menu > Print** hoặc `Ctrl + P`
2. **Xuất Excel**: Click **Menu > Download** chọn định dạng Excel/CSV
3. **Gửi email**: Click **Menu > Email** để gửi báo cáo qua email

```
┌─────────────────────────────────────────────────────────────────────┐
│ Doanh số theo nguồn KH                              [Menu ▼]       │
├─────────────────────────────────────────────────────────────────────┤
│ Company*: [DCNET Flow ▼]  Từ*: [01/01/2026]  Đến*: [16/02/2026]   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ │ Nguồn KH       │ Doanh số          │                              │
│ ├────────────────┼───────────────────┤                              │
│ │ Cửa hàng       │ 1.215.000.000đ    │                              │
│ │ Facebook       │   885.000.000đ    │                              │
│ │ Zalo           │   398.000.000đ    │                              │
│ │ Website        │   250.000.000đ    │                              │
│ │ Giới thiệu     │    99.500.000đ    │                              │
│ ├────────────────┼───────────────────┤                              │
│ │ **Tổng**       │ **2.847.500.000đ**│                              │
│                                                                     │
│ [═══ BIỂU ĐỒ CỘT ══════════════════]                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 10. Widget Mở Rộng (T4-T8)

Dashboard sẽ tự động bổ sung các widget mới khi các module tương ứng được triển khai. Các widget này hiển thị với **viền nét đứt, nền xám** và giá trị **"—"** cho đến khi module được kích hoạt.

### T6 (30/06/2026) — Fitting

| Widget | Mô tả |
|--------|-------|
| Số buổi fitting | Tổng số buổi fitting trong tháng |
| Doanh thu fitting | Doanh thu từ dịch vụ fitting |
| Tỉ lệ chuyển đổi | % khách fitting chuyển sang mua hàng |
| Top NV Fitting | Nhân viên fitting có hiệu suất cao nhất |

### T4 (30/04/2026) — Trade-in

| Widget | Mô tả |
|--------|-------|
| Số đơn trade-in | Tổng số đơn thu cũ đổi mới trong tháng |
| Giá trị chênh lệch | Tổng chênh lệch (giá mới - giá cũ) |
| SP cũ đã thu | Số lượng sản phẩm cũ đã thu về |
| Top SP trade-in | Sản phẩm được trade-in nhiều nhất |

### T6 (30/06/2026) — Coaching (chỉ Thăng Long TM)

| Widget | Mô tả |
|--------|-------|
| Số học viên | Số học viên đang theo học |
| DT coaching | Doanh thu từ khóa học |
| DT SP phát sinh | Doanh thu sản phẩm bán thêm qua coaching |
| Top HLV | Huấn luyện viên có doanh số cao nhất |

> Các widget này sẽ **tự động xuất hiện** trên Dashboard khi module được kích hoạt. Bạn không cần cấu hình gì thêm.

---

## 11. Câu Hỏi Thường Gặp (FAQ)

### Q1: Tại sao Number Card hiển thị 0?

**A:** Number Card lấy dữ liệu từ Hóa đơn bán hàng (Sales Invoice) đã **submit**. Nếu chưa có hóa đơn nào được submit trong tháng, giá trị sẽ là 0. Kiểm tra:
- Đã tạo Hóa đơn bán hàng chưa?
- Hóa đơn đã được **Submit** (xác nhận) chưa? Hóa đơn Draft không được tính.

### Q2: Tại sao trend hiển thị 0%?

**A:** Trend so sánh doanh số tháng này với tháng trước. Nếu tháng trước không có doanh số (0), hệ thống không thể tính % thay đổi.

### Q3: Tại sao biểu đồ nguồn KH hiển thị "Không rõ"?

**A:** Nguồn khách hàng lấy từ thông tin **Lead** (utm_source). Nếu khách hàng không có Lead liên kết, hoặc Lead chưa được gán nguồn UTM, sẽ hiện "Không rõ". Module Lead (T6) sẽ cung cấp dữ liệu đầy đủ hơn.

### Q4: Tại sao biểu đồ nguồn đơn hiển thị "Không rõ"?

**A:** Trường **"Nguồn đơn hàng"** trên Đơn hàng (Sales Order) chưa được chọn. Hãy đảm bảo nhân viên chọn nguồn đơn khi tạo đơn hàng.

### Q5: Làm sao để xem doanh số của 1 chi nhánh cụ thể?

**A:** Sử dụng bộ lọc **Chi nhánh** (Company) trên thanh bộ lọc. Chọn chi nhánh cần xem.

### Q6: Dashboard có tự động cập nhật không?

**A:** Dashboard cập nhật mỗi khi bạn **tải lại trang** (F5) hoặc khi bạn chuyển sang trang khác rồi quay lại. Dữ liệu không tự động refresh theo thời gian thực.

### Q7: Tôi có thể tùy chỉnh Dashboard không?

**A:** Hiện tại Dashboard được cấu hình chuẩn cho tất cả người dùng. Nếu cần biểu đồ hoặc chỉ số khác, liên hệ quản trị viên hệ thống.

### Q8: Doanh số có bao gồm thuế (VAT) không?

**A:** Có. Number Card dùng trường **grand_total** (tổng tiền sau thuế). Nếu cần xem doanh số trước thuế, vui lòng xem Báo Cáo Bán Hàng chi tiết.

### Q9: Tại sao doanh số bán sỉ + bán lẻ không bằng doanh số tổng?

**A:** Có thể có khách hàng chưa được phân nhóm (không thuộc "Khách sỉ" hay "Khách lẻ"). Kiểm tra Customer Group của khách hàng trong danh sách Khách hàng.

### Q10: Làm sao để in Dashboard?

**A:** Dashboard không có chức năng in trực tiếp. Để in báo cáo, vào từng báo cáo chi tiết (Sidebar > Báo cáo) và sử dụng **Menu > Print** hoặc **Menu > Download** để xuất Excel.

### Q11: Top 20 SP có tính sản phẩm trả lại không?

**A:** Không. Báo cáo chỉ tính Hóa đơn bán hàng đã submit (docstatus = 1). Sản phẩm trả lại (Credit Note/Return) là hóa đơn riêng và không được trừ.

### Q12: Bộ lọc Quý tính như thế nào?

**A:** Quý tính theo năm dương lịch:
- Q1: 01/01 - 31/03
- Q2: 01/04 - 30/06
- Q3: 01/07 - 30/09
- Q4: 01/10 - 31/12

---

## 12. Phụ Lục

### 12.1. Phím Tắt

| Phím tắt | Chức năng |
|----------|-----------|
| `/` | Mở tìm kiếm nhanh |
| `Ctrl + P` | In trang hiện tại |
| `F5` | Tải lại trang (cập nhật dữ liệu) |
| `Esc` | Đóng dialog/popup |

### 12.2. Thuật Ngữ

| Thuật ngữ | Giải thích |
|-----------|------------|
| **Number Card** | Thẻ số — hiển thị 1 con số tổng hợp (tổng, trung bình, đếm) |
| **Dashboard Chart** | Biểu đồ trên trang Dashboard |
| **Script Report** | Báo cáo tùy chỉnh, dùng code để truy vấn dữ liệu |
| **Workspace** | Trang làm việc trong ERPNext, chứa các widget (card, biểu đồ, link) |
| **Submit** | Xác nhận chứng từ (hóa đơn, đơn hàng). Sau khi submit, chứng từ không sửa được trực tiếp |
| **Sales Invoice** | Hóa đơn bán hàng — chứng từ ghi nhận doanh thu |
| **Sales Order** | Đơn hàng — chứng từ ghi nhận đơn đặt hàng của khách |
| **Customer Group** | Nhóm khách hàng (VD: "Khách sỉ", "Khách lẻ") |
| **UTM Source** | Nguồn tiếp thị — theo dõi khách hàng đến từ đâu (Facebook, Zalo...) |
| **Grand Total** | Tổng tiền sau thuế và chiết khấu |
| **Trend** | Xu hướng tăng/giảm so với kỳ trước (%) |
| **Company** | Công ty / Chi nhánh trong hệ thống ERPNext |
| **Trade-in** | Thu cũ đổi mới — khách mang sản phẩm cũ đổi sản phẩm mới |
| **Fitting** | Dịch vụ đo và thử đồ dùng golf |
| **Coaching** | Dịch vụ dạy/huấn luyện golf |

---

**Document Version:** 1.0
**Created:** 16/02/2026
**Last Updated:** 16/02/2026
**Author:** DCNET Team

---

*© 2026 DCNET Telecom. All rights reserved.*
