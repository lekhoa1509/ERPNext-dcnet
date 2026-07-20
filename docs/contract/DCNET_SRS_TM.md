# TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM
# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

## DCNET Flow - Giải pháp Quản lý Doanh nghiệp Toàn diện

---

| Thông tin | Chi tiết |
|-----------|----------|
| **Tên dự án** | DCNET Flow |
| **Phiên bản** | 1.0.0 |
| **Ngày tạo** | 03/02/2026 |
| **Khách hàng** | Công ty TNHH Thăng Long TM |
| **Nhà cung cấp** | DCNET Corporation |
| **Tài liệu số** | PHỤ LỤC SỐ 02 - Hợp đồng DCNET-TLTM |

---

### Lịch sử phiên bản

| Phiên bản | Ngày | Nội dung thay đổi | Người cập nhật |
|-----------|------|-------------------|----------------|
| 1.0.0 | 03/02/2026 | Phiên bản đầu tiên | DCNET |

---

## MỤC LỤC

1. [Giới thiệu](#1-giới-thiệu)
2. [Mô tả tổng quan](#2-mô-tả-tổng-quan)
3. [Yêu cầu chức năng](#3-yêu-cầu-chức-năng)
4. [Yêu cầu phi chức năng](#4-yêu-cầu-phi-chức-năng)
5. [Giao diện hệ thống](#5-giao-diện-hệ-thống)
6. [Phụ lục](#6-phụ-lục)

---

# 1. GIỚI THIỆU

## 1.1. Mục đích tài liệu

Tài liệu Đặc tả Yêu cầu Phần mềm (SRS) này mô tả chi tiết các yêu cầu chức năng và phi chức năng của hệ thống **DCNET Flow** - Giải pháp Quản lý Doanh nghiệp Toàn diện dành cho Thăng Long TM.

Tài liệu này được sử dụng làm:
- Phụ lục hợp đồng giữa DCNET Corporation và Thăng Long TM
- Cơ sở để thiết kế, phát triển và kiểm thử hệ thống
- Tài liệu tham chiếu cho việc nghiệm thu sản phẩm

## 1.2. Phạm vi sản phẩm

**DCNET Flow** là giải pháp quản lý doanh nghiệp toàn diện, bao gồm các phân hệ:

| STT | Phân hệ | Mô tả |
|-----|---------|-------|
| 1 | **CRM** | Quản lý Lead, Khách hàng, Chăm sóc khách hàng |
| 2 | **Bán hàng** | Đơn hàng, Bảng giá, Chiết khấu, Công nợ khách hàng |
| 3 | **Mua hàng** | Đơn mua, Nhập khẩu, Công nợ nhà cung cấp |
| 4 | **Kho vận** | Quản lý kho, Nhập xuất, Barcode, Giao vận |
| 5 | **Kế toán** | Sổ cái, Công nợ, Thuế, Báo cáo tài chính |
| 6 | **Dịch vụ Golf** | Fitting, Coaching, Thu cũ Đổi mới |
| 7 | **Membership** | Quản lý gói/thẻ, QR check-in, nâng/hạ hạng |
| 8 | **Báo cáo** | Dashboard, Analytics, Dự báo doanh thu |

**Quy mô dự án:**

| Chỉ số | Giá trị |
|--------|---------|
| Tổng số modules | 44 |
| Thời gian triển khai | 6 tháng (T3-T8/2026) |

## 1.3. Định nghĩa & Thuật ngữ

| Thuật ngữ | Định nghĩa |
|-----------|------------|
| **Lead** | Cơ hội khách hàng mới có quan tâm mua hàng nhưng chưa phát sinh giao dịch |
| **Khách hàng** | Đối tượng đã phát sinh giao dịch mua hàng |
| **Fitting** | Dịch vụ đo thông số kỹ thuật cá nhân để customize gậy golf |
| **Coaching** | Dịch vụ huấn luyện golf cho học viên |
| **Trade-in** | Chương trình thu sản phẩm cũ để đổi sản phẩm mới |
| **Membership** | Chương trình quản lý gói/thẻ thành viên |
| **PO** | Purchase Order - Đơn đặt hàng mua |
| **SO** | Sales Order - Đơn đặt hàng bán |
| **MOQ** | Minimum Order Quantity - Số lượng đặt hàng tối thiểu |
| **SKU** | Stock Keeping Unit - Mã quản lý hàng hóa |
| **Serial** | Số seri - Mã định danh duy nhất của sản phẩm |
| **Lô (Batch)** | Nhóm sản phẩm cùng đợt sản xuất/nhập khẩu |
| **NCC** | Nhà cung cấp (Supplier) |
| **KH** | Khách hàng (Customer) |
| **NVKD** | Nhân viên kinh doanh |
| **HLV** | Huấn luyện viên |
| **COD** | Cash On Delivery - Thanh toán khi nhận hàng |

## 1.4. Tài liệu tham chiếu

| STT | Tài liệu | Mô tả |
|-----|----------|-------|
| 1 | PHỤ LỤC SỐ 01 - Hợp đồng DCNET-TLTM | Tài liệu yêu cầu gốc từ khách hàng |
| 2 | PHASE_1_FEATURES.xlsx | Bảng tính năng chi tiết Phase 1 (CRM) |
| 3 | PHASE_2_FEATURES.xlsx | Bảng tính năng chi tiết Phase 2 (ERP) |
| 4 | Quy trình nhập hàng | Tài liệu quy trình nghiệp vụ |

---

# 2. MÔ TẢ TỔNG QUAN

## 2.1. Góc nhìn sản phẩm

DCNET Flow là hệ thống quản lý doanh nghiệp được thiết kế riêng cho ngành kinh doanh Golf, đáp ứng các đặc thù:

- **Quản lý sản phẩm đa dạng**: Gậy golf (với biến thể shaft, grip, flex), quần áo, phụ kiện
- **Quy trình nhập khẩu phức tạp**: 7 loại sản phẩm với lịch đặt hàng khác nhau
- **Dịch vụ chuyên biệt**: Fitting, Coaching, Trade-in, Membership
- **Bán hàng đa kênh**: Cửa hàng, Bán buôn, Bán lẻ

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DCNET FLOW - TỔNG QUAN                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────────┐    │   │
│   │  │    CRM    │  │  Bán hàng │  │  Mua hàng │  │   Kho vận     │    │   │
│   │  │           │  │           │  │           │  │               │    │   │
│   │  │ • Lead    │  │ • Đơn hàng│  │ • PO      │  │ • Nhập/Xuất   │    │   │
│   │  │ • Khách   │  │ • Bảng giá│  │ • Import  │  │ • Barcode     │    │   │
│   │  │   hàng    │  │ • Chiết   │  │ • Thanh   │  │ • Serial/Lô   │    │   │
│   │  │ • CSKH    │  │   khấu    │  │   toán    │  │ • Kiểm kê     │    │   │
│   │  │           │  │ • Công nợ │  │ • NCC     │  │ • Vị trí      │    │   │
│   │  └───────────┘  └───────────┘  └───────────┘  └───────────────┘    │   │
│   │                                                                     │   │
│   │  ┌───────────┐  ┌───────────────────────────────────────────────┐  │   │
│   │  │  Kế toán  │  │              DỊCH VỤ GOLF                     │  │   │
│   │  │           │  │                                               │  │   │
│   │  │ • Sổ cái  │  │  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │  │   │
│   │  │ • Công nợ │  │  │ Fitting │  │Coaching │  │ Thu cũ      │   │  │   │
│   │  │ • Thuế    │  │  │         │  │         │  │ Đổi mới     │   │  │   │
│   │  │ • TSCĐ   │  │  └─────────┘  └─────────┘  └─────────────┘   │  │   │
│   │  └───────────┘  └───────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   │  ┌───────────────────────────────────────────────────────────────┐  │   │
│   │  │              MEMBERSHIP & DỰ BÁO                              │  │   │
│   │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐    │  │   │
│   │  │  │ Membership  │  │  Dự báo DT  │  │  Workshop/Event     │    │  │   │
│   │  │  └─────────────┘  └─────────────┘  └─────────────────────┘    │  │   │
│   │  └───────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                     BÁO CÁO & PHÂN TÍCH                             │   │
│   │              (Dashboard, Reports, Dự báo Doanh thu)                 │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.2. Kiến trúc hệ thống

### 2.2.1. Kiến trúc tổng thể

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              NGƯỜI DÙNG                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│   │  Kinh doanh │    │    Kho      │    │   Kế toán   │    │   Quản lý   │  │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
│          │                  │                  │                  │         │
└──────────┼──────────────────┼──────────────────┼──────────────────┼─────────┘
           │                  │                  │                  │
           ▼                  ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GIAO DIỆN WEB                                      │
│                    (Responsive - Desktop & Mobile)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        TẦNG ỨNG DỤNG                                │   │
│   │                                                                     │   │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐   │   │
│   │  │   CRM   │ │ Bán hàng│ │ Mua hàng│ │   Kho   │ │  Kế toán    │   │   │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────────┘   │   │
│   │                                                                     │   │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────────────┐   │   │
│   │  │ Fitting │ │Coaching │ │Trade-in │ │      Báo cáo            │   │   │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────────────────────┘   │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        TẦNG TÍCH HỢP                                │   │
│   │                                                                     │   │
│   │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐   │   │
│   │  │   Viettel Post  │ │      GHTK       │ │     REST API        │   │   │
│   │  └─────────────────┘ └─────────────────┘ └─────────────────────┘   │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        TẦNG DỮ LIỆU                                 │   │
│   │                                                                     │   │
│   │  ┌─────────────────────┐    ┌─────────────────────────────────┐    │   │
│   │  │     Database        │    │         File Storage            │    │   │
│   │  │ (Cơ sở dữ liệu     │    │    (Documents, Images)          │    │   │
│   │  │      quan hệ)       │    │                                 │    │   │
│   │  └─────────────────────┘    └─────────────────────────────────┘    │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2. Môi trường triển khai

| Thành phần | Đặc tả |
|------------|--------|
| **Web Server** | Nginx |
| **Application Server** | Application Server |
| **Database** | Database Server |
| **Cache** | Cache Server |
| **File Storage** | Local/S3-compatible |
| **OS** | Ubuntu 22.04 LTS |

## 2.3. Nhóm người dùng

### 2.3.1. Ma trận người dùng

| Vai trò | Mô tả | Modules sử dụng |
|---------|-------|-----------------|
| **Quản trị hệ thống** | Quản lý user, phân quyền, cấu hình | Tất cả |
| **Ban Lãnh đạo** | Xem báo cáo, phê duyệt | Dashboard, Báo cáo |
| **Giám đốc Kinh doanh** | Quản lý bán hàng, khách hàng | CRM, Bán hàng, Báo cáo |
| **Nhân viên Kinh doanh** | Tạo đơn hàng, chăm sóc KH | CRM, Bán hàng, Fitting, Coaching |
| **Nhân viên Mua hàng** | Quản lý nhập hàng | Mua hàng |
| **Nhân viên Kho** | Nhập xuất kho, kiểm kê | Kho |
| **Kế toán** | Công nợ, hóa đơn, báo cáo TC | Kế toán, Báo cáo |
| **Kế toán trưởng** | Duyệt chứng từ, kiểm soát | Kế toán, Phê duyệt |
| **Nhân viên Fitting** | Thực hiện đo fitting | Fitting |
| **Huấn luyện viên** | Quản lý coaching | Coaching |
| **Nhân viên cửa hàng** | Bán hàng tại quầy | Bán hàng (POS) |

### 2.3.2. Số lượng người dùng dự kiến

| Loại | Số lượng |
|------|----------|
| Người dùng đồng thời | 20-30 |
| Tổng số tài khoản | 50-100 |
| Chi nhánh/Đại lý | 5-10 |

## 2.4. Ràng buộc & Giới hạn

### 2.4.1. Ràng buộc kỹ thuật

| Ràng buộc | Mô tả |
|-----------|-------|
| Trình duyệt | Chrome, Firefox, Safari, Edge (phiên bản mới nhất) |
| Độ phân giải | Tối thiểu 1366x768 |
| Kết nối | Internet ổn định, tối thiểu 10Mbps |
| Ngôn ngữ | Tiếng Việt |

### 2.4.2. Ràng buộc nghiệp vụ

| Ràng buộc | Mô tả |
|-----------|-------|
| Đơn vị tiền tệ | VND (chính), USD (tham khảo) |
| Múi giờ | UTC+7 (Việt Nam) |
| Năm tài chính | 01/01 - 31/12 |
| Chế độ kế toán | Thông tư 200/2014/TT-BTC |

## 2.5. Giả định & Phụ thuộc

### 2.5.1. Giả định

1. Khách hàng cung cấp đầy đủ dữ liệu master (Khách hàng, Nhà cung cấp, Sản phẩm)
2. Khách hàng cung cấp tài khoản API các nền tảng (Viettel Post, GHTK)
3. Khách hàng cung cấp server đúng cấu hình yêu cầu trước ngày triển khai

### 2.5.2. Phụ thuộc bên ngoài

| Dịch vụ | Mục đích | Nhà cung cấp |
|---------|----------|--------------|
| Viettel Post API | Tạo đơn giao vận, tracking | Viettel |
| GHTK API | Tạo đơn giao vận, tracking | GHTK |

---

# 3. YÊU CẦU CHỨC NĂNG

---

## T3: BÀN GIAO 31/03/2026

---

## 3.1. Đăng nhập & Nền tảng

### 3.1.1. Mô tả
Module cung cấp các chức năng nền tảng cho hệ thống bao gồm đăng nhập, đăng xuất, quên mật khẩu và quản lý phiên làm việc. Đây là module cơ sở để người dùng truy cập và sử dụng hệ thống DCNET Flow.

### 3.1.2. Tính năng chính
- Đăng nhập bằng tài khoản (username/email + password)
- Đăng xuất và kết thúc phiên làm việc
- Quên mật khẩu / Đặt lại mật khẩu qua email
- Quản lý phiên đăng nhập (session timeout)
- Giao diện tiếng Việt

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.2. Dashboard

> **Giai đoạn:** Bàn giao T3 (31/03/2026)

### 3.2.1. Dashboard tổng quan

**REQ-RPT-001:** Dashboard tổng quan
- Doanh số theo ngày/tuần/tháng
- Doanh số bán sỉ vs bán lẻ
- Doanh số theo nguồn KH
- Doanh số theo nguồn đơn
- Top 20 sản phẩm bán chạy

---

## 3.3. Quản lý Sản phẩm

> **Giai đoạn:** Bàn giao T3 (31/03/2026)

### 3.3.1. Danh sách Sản phẩm

**REQ-PROD-001:** Hiển thị danh sách sản phẩm

| Trường thông tin | Mô tả |
|------------------|-------|
| Mã sản phẩm | Mã định danh |
| SKU | Mã quản lý kho |
| Tên sản phẩm | Tên hiển thị |
| Nhóm sản phẩm | Danh mục sản phẩm |
| Thương hiệu | TaylorMade / Callaway / ... |
| Giá bán lẻ | Giá niêm yết |
| Tồn kho | Số lượng tồn |
| Trạng thái | Đang kinh doanh / Ngừng kinh doanh |

**REQ-PROD-002:** Lọc sản phẩm
- Theo nhóm sản phẩm
- Theo thương hiệu
- Theo tồn kho (dưới định mức, vượt định mức, còn hàng, hết hàng)
- Theo trạng thái kinh doanh

### 3.3.2. Quản lý Danh mục

**REQ-PROD-003:** Cây danh mục sản phẩm
- Danh mục đa cấp
- Thêm/Sửa/Xóa danh mục
- Gán sản phẩm vào danh mục

### 3.3.3. Tạo Sản phẩm

**REQ-PROD-004:** Thông tin sản phẩm

| Thông tin | Bắt buộc | Mô tả |
|-----------|----------|-------|
| Mã hàng | Có | Mã định danh |
| Mã vạch | Không | Barcode |
| Tên sản phẩm | Có | Tên hiển thị |
| Nhóm sản phẩm | Có | Danh mục |
| Thương hiệu | Có | Hãng sản xuất |
| Đơn vị tính | Có | Cái / Bộ / Đôi / ... |
| Giá bán | Có | Giá niêm yết |
| Trọng lượng | Không | Để tính phí ship |
| Thuộc tính | Không | Màu sắc, Size, Flex, ... |
| Mô tả | Không | Chi tiết sản phẩm |
| Hình ảnh | Không | Ảnh sản phẩm |

**REQ-PROD-005:** Quản lý biến thể
- Sản phẩm có nhiều biến thể (Size, Màu, Flex)
- Mỗi biến thể có SKU riêng
- Quản lý tồn kho theo từng biến thể

### 3.3.4. Import/Export Sản phẩm

**REQ-PROD-006:** Import sản phẩm từ Excel
- Template chuẩn với các cột thông tin
- Import kèm hình ảnh (theo quy tắc đặt tên)
- Báo cáo kết quả import

**REQ-PROD-007:** Export sản phẩm ra Excel
- Export theo điều kiện lọc
- Export tất cả thông tin

---

## 3.4. Danh mục Nhà cung cấp

### 3.4.1. Mô tả
Module quản lý danh sách nhà cung cấp (NCC), bao gồm thông tin liên hệ, điều khoản thanh toán, lịch sử giao dịch và đánh giá NCC. Hỗ trợ phân loại NCC theo nhóm hàng và theo dõi ưu đãi từ NCC.

### 3.4.2. Tính năng chính
- Danh sách NCC với thông tin liên hệ đầy đủ
- Phân loại NCC theo nhóm hàng / thương hiệu
- Quản lý điều khoản thanh toán theo NCC
- Theo dõi lịch sử giao dịch và công nợ NCC
- Import/Export danh sách NCC từ Excel

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.5. Quản lý Mua hàng

> **Giai đoạn:** Bàn giao T3 (31/03/2026)

### 3.5.1. Quy trình Mua hàng

**REQ-PURCH-001:** Workflow mua hàng (10 bước)

```
Kế hoạch → Đơn hàng/HĐ → KH giao hàng → Đề nghị nhập → Phiếu nhập
    ↓                                                        ↓
Xác nhận CN ← Đề nghị TT ← Phiếu chi/Báo nợ ←───────────────┘
    ↓
(Nếu có trả lại) → Lệnh xuất trả → Phiếu xuất trả NCC
```

### 3.5.2. Kế hoạch Mua hàng

**REQ-PURCH-002:** Lập kế hoạch mua hàng
- Theo dõi lịch trình đặt hàng của hãng (7 loại sản phẩm)
- Nhắc nhở deadline đặt hàng
- Tổng hợp nhu cầu từ các đại lý

| Loại sản phẩm | Thời điểm đặt | MOQ |
|---------------|---------------|-----|
| Gậy năm mới | T9-10 | Theo hãng |
| Driver, FW, Rescue, Irons | Launch T1-2 | 10 pcs |
| Softgoods (US) | Hàng tháng | Theo hãng |
| Gậy P Series | 2 năm/lần | 1000+ |
| Putters | Hàng năm | Theo hãng |
| Wedges | Hàng năm | Theo hãng |
| Quần áo & PK (JP) | 2 lần/năm | Theo hãng |

### 3.5.3. Đơn hàng Mua (PO)

**REQ-PURCH-003:** Tạo Purchase Order

| Thông tin | Bắt buộc | Mô tả |
|-----------|----------|-------|
| Số PO | Tự động | PO Number theo hãng |
| Nhà cung cấp | Có | Chọn từ danh sách |
| Ngày đặt | Có | Ngày tạo PO |
| Kho nhận | Có | Kho dự kiến nhận hàng |
| Chi tiết SP | Có | Model, SKU, SL, Giá mua |
| Ship mode | Không | Sea / Air / Express |
| Confirm ship date | Không | Ngày NCC xác nhận giao |

**REQ-PURCH-004:** Trạng thái PO

| Trạng thái | Mô tả |
|------------|-------|
| Nháp | PO mới tạo |
| Đã gửi NCC | Đã gửi cho nhà cung cấp |
| Đang giao | NCC đang giao hàng |
| Nhận một phần | Đã nhận một phần số lượng |
| Hoàn thành | Đã nhận đủ hàng |
| Hủy | PO bị hủy |

### 3.5.4. Nhập hàng

**REQ-PURCH-005:** Phiếu nhập mua/nhập khẩu
- Kế thừa từ PO
- Nhập theo lô, serial
- Ghi nhận số tờ khai (nhập khẩu)
- Kiểm tra giá nhập vs giá PO

**REQ-PURCH-006:** Theo dõi thanh toán NCC
- Ghi nhận thanh toán theo PO
- Trạng thái: Chưa TT / TT một phần / Đã TT đủ
- Đính kèm chứng từ thanh toán

### 3.5.5. Ưu đãi Nhà cung cấp

**REQ-PURCH-007:** Quản lý ưu đãi NCC
- Chiết khấu % theo doanh số
- Chiết khấu tiền
- Quà tặng kèm
- Tính ưu đãi tự động theo điều kiện

---

## 3.6. Báo cáo Phân tích

### 3.6.1. Mô tả
Module cung cấp các báo cáo phân tích tổng hợp cho ban lãnh đạo và quản lý, bao gồm phân tích xu hướng, so sánh kỳ và các chỉ số KPI quan trọng.

### 3.6.2. Tính năng chính
- Báo cáo phân tích xu hướng doanh số
- So sánh doanh số theo kỳ (tháng/quý/năm)
- Phân tích hiệu quả theo kênh bán hàng
- Phân tích biên lợi nhuận theo nhóm sản phẩm
- Export báo cáo ra Excel/PDF

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## T4: BÀN GIAO 30/04/2026

---

## 3.7. Quản lý Kho hàng

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

### 3.7.1. Danh mục Kho

**REQ-WH-001:** Quản lý danh sách kho
- Tên kho, Mã kho
- Địa chỉ
- Nhân viên phụ trách
- Loại kho: Chính / Ký gửi / Transit

### 3.7.2. Nhập xuất Kho

**REQ-WH-002:** Phiếu nhập kho
- Nhập mua (từ NCC)
- Nhập trả lại (từ KH)
- Nhập điều chuyển (từ kho khác)
- Nhập kiểm kê (chênh lệch thừa)

**REQ-WH-003:** Phiếu xuất kho
- Xuất bán (cho KH)
- Xuất trả NCC
- Xuất điều chuyển (sang kho khác)
- Xuất kiểm kê (chênh lệch thiếu)

### 3.7.3. Quản lý Lô và Serial

**REQ-WH-004:** Theo dõi theo Lô (Batch)
- Mỗi đợt nhập hàng là 1 lô
- Tracking xuất nhập theo lô
- Hạn sử dụng theo lô (nếu có)

**REQ-WH-005:** Theo dõi theo Serial
- Mỗi sản phẩm có Serial riêng
- Scan serial khi nhập/xuất
- Truy xuất lịch sử theo serial

### 3.7.4. Mã vạch và In tem

**REQ-WH-006:** Quản lý Barcode
- Gán mã vạch cho sản phẩm
- Hỗ trợ barcode nhà cung cấp
- Tự sinh barcode nội bộ

**REQ-WH-007:** In tem nhãn
- Template tem nhãn tùy chỉnh
- In hàng loạt theo phiếu nhập
- In theo yêu cầu (on-demand)

### 3.7.5. Giữ hàng theo Đơn

**REQ-WH-008:** Reserve stock
- Khi tạo đơn hàng, trừ tồn kho khả dụng
- Tồn kho thực tế vs Tồn kho khả dụng
- Hủy giữ hàng khi hủy đơn

### 3.7.6. Kiểm kê

**REQ-WH-009:** Kiểm kê kho
- Tạo phiếu kiểm kê theo kho
- Nhập số lượng thực tế
- Tính chênh lệch, tạo phiếu điều chỉnh

---

## 3.8. Báo cáo Kho

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

**REQ-RPT-006:** Báo cáo kho
- Tồn kho theo kho
- Giá trị tồn kho
- Sản phẩm dưới định mức
- Sản phẩm không luân chuyển

---

## 3.9. Quản lý Đơn hàng

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

### 3.9.1. Danh sách Đơn hàng

**REQ-ORDER-001:** Hiển thị danh sách đơn hàng

| Trường thông tin | Mô tả |
|------------------|-------|
| Mã đơn hàng | Mã tự động sinh |
| Khách hàng | Tên khách hàng |
| Loại đơn | Lẻ / Sỉ |
| Trạng thái | Chưa xử lý / Đang xuất kho / Đang vận chuyển / Hoàn thành / Hủy |
| Giá trị đơn | Tổng tiền đơn hàng |
| Đã trả | Số tiền đã thanh toán |
| Còn nợ | Số tiền còn nợ |
| Nguồn đơn | Online / Cửa hàng |
| Chi nhánh | Chi nhánh xử lý |
| Ngày tạo | Thời gian tạo đơn |

**REQ-ORDER-002:** Phân loại danh sách đơn
- Đơn vật dụng (bán lẻ, bán buôn)
- Đơn Fitting
- Đơn Coaching
- Đơn Thu cũ Đổi mới

### 3.9.2. Tạo Đơn hàng

**REQ-ORDER-005:** Kiểm tra tồn kho
- Kiểm tra tồn kho trước khi tạo đơn
- Hiển thị tồn kho theo từng kho
- Cảnh báo nếu không đủ hàng

### 3.9.3. Quy trình xử lý đơn hàng

**REQ-ORDER-006:** Workflow đơn hàng bán buôn

```
Tạo đơn → Kiểm tra tồn → Lệnh xuất → Kiểm tra công nợ → Xuất kho → Hóa đơn → Thanh toán
                                          ↓
                              (Vượt hạn mức → Kế toán duyệt)
```

**REQ-ORDER-007:** Workflow đơn hàng bán lẻ

```
Tạo đơn → Kiểm tra tồn → Xuất kho → Hóa đơn → Thanh toán
```

---

## 3.10. Bán buôn

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

### 3.10.1. Tạo đơn hàng bán buôn

**REQ-ORDER-004:** Tạo đơn hàng bán buôn
- Áp dụng bảng giá sỉ
- Áp dụng chính sách chiết khấu theo KH
- Kiểm tra hạn mức công nợ
- Yêu cầu duyệt nếu vượt hạn mức

### 3.10.2. Chính sách Chiết khấu bán buôn

**REQ-SALE-004:** Chính sách chiết khấu bán buôn
- Chiết khấu theo khách hàng
- Chiết khấu theo mặt hàng
- Chiết khấu theo số lượng (bậc thang)
- Chiết khấu theo doanh số tích lũy

### 3.10.3. Hạn mức Công nợ

**REQ-SALE-007:** Quản lý hạn mức
- Thiết lập hạn mức công nợ theo từng khách hàng
- Cảnh báo khi vượt hạn mức
- Yêu cầu Kế toán trưởng duyệt khi vượt

**REQ-SALE-008:** Kiểm tra công nợ quá hạn
- Kiểm tra hóa đơn quá hạn thanh toán
- Chặn xuất hàng nếu có hóa đơn quá hạn (cấu hình được)

### 3.10.4. Tính thưởng Doanh số

**REQ-SALE-009:** Quy tắc tính thưởng
- Thưởng khi KH đạt kế hoạch năm
- Thưởng theo doanh số tích lũy
- Tối đa 3 bước (3 tác nhân) trong thưởng doanh số

---

## 3.11. Bán lẻ

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

### 3.11.1. Tạo đơn hàng bán lẻ

**REQ-ORDER-003:** Tạo đơn hàng bán lẻ

| Thông tin | Bắt buộc | Mô tả |
|-----------|----------|-------|
| Nguồn đơn | Có | Chọn từ danh sách |
| Khách hàng | Có | Chọn hoặc tạo mới |
| Địa chỉ giao | Có | Chi nhánh hoặc địa chỉ KH |
| Kho xuất | Có | Kho xử lý đơn |
| Sản phẩm | Có | Danh sách sản phẩm + số lượng |
| Phương thức TT | Có | Tiền mặt / Chuyển khoản / COD |
| Voucher | Không | Mã giảm giá |
| Giảm giá | Không | Giảm giá thêm (số tiền) |

### 3.11.2. Chính sách Chiết khấu bán lẻ

**REQ-SALE-005:** Chính sách chiết khấu bán lẻ
- Chiết khấu theo nhóm hàng
- Chiết khấu đặc biệt (nhập tay)

---

## 3.12. Quản lý Bán hàng

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

### 3.12.1. Kế hoạch Bán hàng

**REQ-SALE-001:** Kế hoạch doanh số theo năm
- Lập kế hoạch doanh số cho từng khách hàng
- Phân bổ theo tháng/quý
- Theo dõi thực hiện vs kế hoạch

### 3.12.2. Bảng giá

**REQ-SALE-002:** Quản lý bảng giá

| Thông tin | Mô tả |
|-----------|-------|
| Tên bảng giá | Tên định danh |
| Ngày hiệu lực | Từ ngày - Đến ngày |
| Chi nhánh áp dụng | Danh sách chi nhánh |
| Nhóm KH áp dụng | Tags khách hàng |
| Chi tiết giá | Mã hàng, Tên hàng, Giá bán |

**REQ-SALE-003:** Áp dụng bảng giá
- Tự động lấy giá theo bảng giá khi tạo đơn
- Ưu tiên theo thứ tự: KH cụ thể > Nhóm KH > Mặc định

### 3.12.3. Quản lý Voucher

**REQ-SALE-006:** Tạo Voucher
- Mã voucher (tự động hoặc tùy chọn)
- Loại: % giảm / Giảm tiền / Free ship
- Điều kiện: Đơn tối thiểu / Nhóm SP / Nhóm KH
- Thời hạn sử dụng
- Số lượng sử dụng tối đa

---

## 3.13. Danh mục Bán hàng

### 3.13.1. Mô tả
Module quản lý các danh mục dữ liệu nền tảng phục vụ nghiệp vụ bán hàng, bao gồm nhóm khách hàng, kênh bán hàng, phương thức thanh toán, điều khoản thanh toán và các dữ liệu tham chiếu khác.

### 3.13.2. Tính năng chính
- Quản lý nhóm khách hàng (Sỉ / Lẻ / VIP)
- Quản lý kênh bán hàng (Cửa hàng / Online)
- Quản lý phương thức thanh toán
- Quản lý điều khoản thanh toán
- Quản lý nguồn đơn hàng

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.14. Đơn hàng Thu cũ Đổi mới (Trade-in)

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

### 3.14.1. Quản lý đơn Trade-in

**REQ-TI-001:** Danh sách đơn Trade-in

| Trường thông tin | Mô tả |
|------------------|-------|
| Mã đơn | TI-YYYYMMDD-XXX |
| Khách hàng | Tên, SĐT |
| SP cũ | Tên + Thương hiệu |
| SP mới | Tên + Thương hiệu |
| Giá thu SP cũ | Số tiền |
| Giá SP mới | Số tiền |
| Chênh lệch | Số tiền KH cần trả |
| Trạng thái | Workflow |
| NV xử lý | Nhân viên phụ trách |

### 3.14.2. Tạo đơn Trade-in

**REQ-TI-002:** Thông tin SP cũ
- Tên sản phẩm cũ
- Thương hiệu
- Tình trạng: Mới / Tốt / Trung bình / Kém
- Giá thu đề xuất
- Ghi chú tình trạng
- Hình ảnh

**REQ-TI-003:** Thông tin SP mới
- Chọn từ danh sách sản phẩm
- Giá bán

**REQ-TI-004:** Tính toán chênh lệch
```
Số tiền KH thanh toán = Giá SP mới - Giá thu SP cũ - Voucher (nếu có)
```

### 3.14.3. Workflow Trade-in

**REQ-TI-005:** Trạng thái đơn Trade-in

| Trạng thái | Mô tả |
|------------|-------|
| Mới tạo | Đơn vừa được tạo |
| Đang kiểm tra | NV đang kiểm tra SP cũ |
| Đã định giá | SP cũ đã được định giá |
| Khách xác nhận | KH đồng ý với giá |
| Đang xử lý | Đang chuẩn bị SP mới |
| Hoàn thành | Giao dịch hoàn tất |
| Đã hủy | Đơn bị hủy |

### 3.14.4. Tích hợp Kho

**REQ-TI-006:** Xử lý kho
- Nhập SP cũ vào kho "Hàng thu cũ"
- Xuất SP mới cho khách
- Cập nhật tồn kho tự động

### 3.14.5. Báo cáo Trade-in

**REQ-TI-007:** Các báo cáo
- Tổng số đơn trade-in
- Doanh thu từ trade-in (tổng chênh lệch)
- Giá trị SP cũ đã thu
- Báo cáo theo chi nhánh
- Top SP được trade-in nhiều nhất

---

## 3.15. Quản lý Chi nhánh

### 3.15.1. Mô tả
Module quản lý thông tin các chi nhánh, cửa hàng trong hệ thống. Mỗi chi nhánh có kho riêng, nhân viên riêng và theo dõi doanh số riêng.

### 3.15.2. Tính năng chính
- Danh sách chi nhánh với thông tin địa chỉ, liên hệ
- Gán kho cho từng chi nhánh
- Gán nhân viên cho từng chi nhánh
- Theo dõi doanh số theo chi nhánh
- Phân quyền dữ liệu theo chi nhánh

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.16. Quản lý Nhân viên

### 3.16.1. Mô tả
Module quản lý thông tin nhân viên trong hệ thống, bao gồm hồ sơ cá nhân, phân công chi nhánh, vai trò và theo dõi hiệu suất làm việc.

### 3.16.2. Tính năng chính
- Hồ sơ nhân viên (thông tin cá nhân, liên hệ)
- Phân công nhân viên theo chi nhánh
- Gán vai trò và quyền hạn
- Theo dõi KPI nhân viên kinh doanh
- Quản lý lịch làm việc

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.17. Quản lý Khách hàng

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

### 3.17.1. Danh sách Khách hàng

**REQ-CUST-001:** Hiển thị danh sách Khách hàng

| Trường thông tin | Mô tả |
|------------------|-------|
| Mã khách hàng | Mã định danh |
| Tên | Họ tên / Tên công ty |
| Điện thoại | Số điện thoại |
| Email | Địa chỉ email |
| Loại KH | Lẻ / Sỉ |
| Bảng giá áp dụng | Bảng giá đang áp dụng |
| Tổng đơn hàng | Số đơn đã mua |
| Doanh số | Tổng doanh số phát sinh |
| Công nợ | Số tiền còn nợ |
| NV phụ trách | Nhân viên chăm sóc |

### 3.17.2. Khách hàng 360°

**REQ-CUST-002:** Hồ sơ Khách hàng 360°
- Thông tin cơ bản và liên hệ
- Công nợ hiện tại
- Lịch sử giao dịch (tất cả đơn hàng)
- Danh sách sản phẩm đã mua
- Lịch sử fitting, coaching
- Tài liệu đính kèm
- Timeline hoạt động

---

## 3.18. Báo cáo Đơn hàng

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

**REQ-RPT-003:** Báo cáo đơn hàng
- Tổng đơn theo trạng thái
- Đơn thành công vs thất bại
- Báo cáo fitting
- Báo cáo coaching
- Báo cáo đại lý

---

## 3.19. Báo cáo Quản trị

### 3.19.1. Mô tả
Module cung cấp các báo cáo tổng hợp dành cho ban lãnh đạo, hỗ trợ ra quyết định kinh doanh với các chỉ số KPI quan trọng.

### 3.19.2. Tính năng chính
- Báo cáo tổng hợp kinh doanh theo kỳ
- Báo cáo hiệu quả theo chi nhánh
- Báo cáo so sánh kế hoạch vs thực hiện
- Báo cáo chỉ số KPI tổng hợp
- Export báo cáo ra Excel/PDF

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.20. Báo cáo Nhân viên

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

**REQ-RPT-005:** Báo cáo nhân viên
- Tỉ lệ chốt đơn
- Số đơn xử lý
- Doanh thu theo nhân viên
- Hiệu suất làm việc

---

## 3.21. Báo cáo Khách hàng

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

**REQ-RPT-004:** Báo cáo khách hàng
- Số lead theo nguồn
- Top khách hàng doanh thu cao
- Khách mới (sỉ/lẻ)
- Mức độ hài lòng

---

## 3.22. Báo cáo Doanh số

> **Giai đoạn:** Bàn giao T4 (30/04/2026)

**REQ-RPT-002:** Báo cáo doanh số
- Theo thời gian
- Theo chi nhánh
- Theo nhóm khách hàng
- Theo nguồn đơn hàng
- Theo sản phẩm

---

## T5: BÀN GIAO 30/05/2026

---

## 3.23. Kế toán Tiền

> **Giai đoạn:** Bàn giao T5 (30/05/2026)

### 3.23.1. Phiếu thu

**REQ-ACC-005:** Phiếu thu
- Thu tiền từ khách hàng
- Gán vào hóa đơn cụ thể
- Phương thức: Tiền mặt / Chuyển khoản

### 3.23.2. Phiếu chi

**REQ-ACC-006:** Phiếu chi
- Chi tiền cho nhà cung cấp
- Gán vào hóa đơn mua
- Đề nghị thanh toán → Duyệt → Phiếu chi

---

## 3.24. Kế toán Mua hàng

### 3.24.1. Mô tả
Module quản lý các nghiệp vụ kế toán liên quan đến mua hàng, bao gồm hóa đơn mua, ghi nhận chi phí mua hàng, và đối chiếu với đơn mua hàng (PO).

### 3.24.2. Tính năng chính
- Hóa đơn mua hàng (Purchase Invoice) kế thừa từ phiếu nhập
- Ghi nhận chi phí phát sinh (vận chuyển, hải quan, bảo hiểm)
- Phân bổ chi phí nhập khẩu vào giá vốn sản phẩm
- Đối chiếu hóa đơn mua với PO
- Báo cáo chi phí mua hàng theo kỳ

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.25. Kế toán Bán hàng

> **Giai đoạn:** Bàn giao T5 (30/05/2026)

### 3.25.1. Hóa đơn bán buôn

**REQ-ACC-001:** Hóa đơn bán buôn
- Kế thừa từ lệnh xuất hàng
- Thông tin: Khách hàng, Sản phẩm, Số lượng, Đơn giá, Chiết khấu, Thuế
- Hạn thanh toán
- Xuất hóa đơn điện tử

### 3.25.2. Hóa đơn bán lẻ

**REQ-ACC-002:** Hóa đơn bán lẻ (POS)
- Tạo nhanh tại quầy
- Tích hợp thanh toán (Tiền mặt, Thẻ, Chuyển khoản)
- In hóa đơn / Gửi email

---

## 3.26. Kế toán Công nợ

> **Giai đoạn:** Bàn giao T5 (30/05/2026)

### 3.26.1. Công nợ phải thu

**REQ-ACC-003:** Công nợ phải thu (AR)
- Theo dõi công nợ theo khách hàng
- Phân tích tuổi nợ (0-30, 31-60, 61-90, >90 ngày)
- Báo cáo công nợ quá hạn

### 3.26.2. Công nợ phải trả

**REQ-ACC-004:** Công nợ phải trả (AP)
- Theo dõi công nợ theo nhà cung cấp
- Lên lịch thanh toán
- Đối chiếu công nợ

---

## 3.27. Kế toán Hàng tồn kho

### 3.27.1. Mô tả
Module quản lý nghiệp vụ kế toán liên quan đến hàng tồn kho, bao gồm tính giá vốn, ghi nhận biến động tồn kho và đối chiếu kế toán kho.

### 3.27.2. Tính năng chính
- Tính giá vốn hàng bán (phương pháp bình quân gia quyền)
- Ghi nhận giá trị hàng tồn kho
- Đối chiếu kế toán kho với sổ kho
- Xử lý chênh lệch kiểm kê
- Báo cáo giá vốn hàng bán theo kỳ

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.28. Chi phí & Hỗ trợ

> **Giai đoạn:** Bàn giao T5 (30/05/2026)

### 3.28.1. Chi phí theo sự kiện

**REQ-ACC-007:** Theo dõi chi phí theo sự kiện
- Chi phí Marketing (product launch, exhibition)
- Chi phí Demo (customer trials)
- Chi phí Bán hàng (promotion, discount)
- Chi phí sai giá (price variance)

### 3.28.2. Báo cáo chi phí

**REQ-ACC-008:** Báo cáo chi phí
- Chi phí theo event
- Chi phí theo sản phẩm
- Chi phí vs ngân sách

---

## 3.29. Tài sản & CCDC

### 3.29.1. Mô tả
Module quản lý tài sản cố định (TSCĐ) và công cụ dụng cụ (CCDC) của doanh nghiệp, bao gồm theo dõi nguyên giá, khấu hao, phân bổ và thanh lý.

### 3.29.2. Tính năng chính
- Quản lý danh sách TSCĐ (nguyên giá, ngày mua, bộ phận sử dụng)
- Tính khấu hao tự động (theo phương pháp đường thẳng)
- Quản lý CCDC và phân bổ chi phí
- Theo dõi vị trí và tình trạng tài sản
- Thanh lý tài sản

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.30. Kế toán Thuế

### 3.30.1. Mô tả
Module quản lý nghiệp vụ thuế, bao gồm thuế GTGT đầu vào/đầu ra, thuế TNDN và các loại thuế khác theo quy định pháp luật Việt Nam.

### 3.30.2. Tính năng chính
- Quản lý thuế GTGT đầu vào (từ hóa đơn mua)
- Quản lý thuế GTGT đầu ra (từ hóa đơn bán)
- Bảng kê thuế GTGT theo kỳ
- Tờ khai thuế GTGT
- Quản lý hóa đơn điện tử

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.31. Kế toán Tổng hợp

### 3.31.1. Mô tả
Module kế toán tổng hợp quản lý hệ thống sổ cái, bảng cân đối kế toán, báo cáo kết quả kinh doanh và các nghiệp vụ kế toán tổng hợp theo Thông tư 200/2014/TT-BTC.

### 3.31.2. Tính năng chính
- Hệ thống tài khoản kế toán theo TT200
- Sổ cái tổng hợp (General Ledger)
- Bảng cân đối số phát sinh (Trial Balance)
- Báo cáo Kết quả Kinh doanh (P&L)
- Bảng Cân đối Kế toán (Balance Sheet)
- Bút toán điều chỉnh cuối kỳ

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.32. Báo cáo Tổng hợp

> **Giai đoạn:** Bàn giao T5 (30/05/2026)

**REQ-RPT-007:** Báo cáo kế toán
- Công nợ phải thu
- Công nợ phải trả
- Báo cáo tuổi nợ
- Dòng tiền

---

## T6: BÀN GIAO 30/06/2026

---

## 3.33. Quản lý Lead

> **Định nghĩa:** Lead là cơ hội khách hàng mới có quan tâm mua hàng nhưng chưa phát sinh giao dịch thành công.
>
> **Giai đoạn:** Bàn giao T6 (30/06/2026)

### 3.33.1. Danh sách Lead

**REQ-LEAD-001:** Hiển thị danh sách Lead

| Trường thông tin | Mô tả |
|------------------|-------|
| Mã khách hàng | Mã tự động sinh |
| Tên | Họ tên Lead |
| Điện thoại | Số điện thoại liên hệ |
| Email | Địa chỉ email |
| Trạng thái | Chưa nghe máy / Đang tư vấn / Đang giao hàng / Hủy |
| Tags | Nhãn phân loại |
| Nguồn Lead | Website / Facebook / Zalo / Cửa hàng |
| Chi nhánh | Chi nhánh quản lý |
| Nhân viên phụ trách | NVKD được gán |
| Ngày tạo | Thời gian tạo Lead |
| Liên hệ lần cuối | Thời gian tương tác gần nhất |

**REQ-LEAD-002:** Tìm kiếm và lọc Lead

| Tiêu chí | Loại |
|----------|------|
| Tên, Email | Tìm kiếm |
| Trạng thái | Lọc |
| Chi nhánh | Lọc |
| NV phụ trách | Lọc |
| Thời gian tạo | Lọc khoảng |
| Tags | Lọc nhiều giá trị |

### 3.33.2. Tạo Lead

**REQ-LEAD-003:** Tạo Lead mới

| Thông tin | Bắt buộc | Mô tả |
|-----------|----------|-------|
| Mã Lead | Tự động | Format: LEAD-YYYYMMDD-XXX |
| Tên | Có | Họ tên khách hàng |
| Điện thoại | Có | Số điện thoại |
| Email | Không | Địa chỉ email |
| Nguồn | Có | Chọn từ danh sách nguồn |
| Chi nhánh | Có | Chi nhánh quản lý |
| Trạng thái | Có | Mặc định: Mới |

**REQ-LEAD-004:** Kiểm tra trùng lặp
- Hệ thống kiểm tra trùng số điện thoại, email trước khi tạo
- Cảnh báo nếu phát hiện trùng, cho phép tiếp tục hoặc hủy

### 3.33.3. Import/Export Lead

**REQ-LEAD-005:** Import Lead từ Excel
- Template Excel chuẩn với các cột bắt buộc
- Kiểm tra định dạng, trùng lặp khi import
- Báo cáo kết quả: thành công, lỗi, bỏ qua

**REQ-LEAD-006:** Export Lead ra Excel
- Export theo điều kiện lọc
- Xuất tất cả các trường thông tin

### 3.33.4. Tự động tạo Lead

**REQ-LEAD-007:** Tích hợp nguồn bên ngoài
- Nhận Lead từ website qua API
- Nhận Lead từ các kênh đa kênh (nhanh.vn, Zalo, Facebook)
- Tự động gán nguồn Lead tương ứng

**REQ-LEAD-008:** API tạo Lead
- Cung cấp REST API cho phép hệ thống bên ngoài tạo Lead
- Xác thực API Key
- Trả về mã Lead đã tạo

### 3.33.5. Xem chi tiết Lead

**REQ-LEAD-009:** Hiển thị thông tin Lead 360°
- Thông tin cơ bản
- Lịch sử tư vấn (sản phẩm, nhân viên, nội dung, thời gian)
- Lịch sử giao dịch
- Tài liệu đính kèm
- Timeline hoạt động

**REQ-LEAD-010:** Ghi nhận hoạt động
- Gọi điện, SMS, Email, Chat (Facebook, Zalo)
- Ghi chú nội dung tư vấn
- Đính kèm file

### 3.33.6. Chuyển đổi Lead

**REQ-LEAD-011:** Chuyển Lead thành Khách hàng
- Khi Lead phát sinh đơn hàng thành công
- Tự động copy thông tin sang hồ sơ Khách hàng
- Giữ liên kết lịch sử từ Lead

---

## 3.34. Quản lý Fitting

> **Định nghĩa:** Dịch vụ đo thông số kỹ thuật cá nhân để tư vấn và customize gậy golf
>
> **Giai đoạn:** Bàn giao T6 (30/06/2026)

### 3.34.1. Quản lý đơn Fitting

**REQ-FIT-001:** Danh sách đơn Fitting

| Trường thông tin | Mô tả |
|------------------|-------|
| Mã đơn Fitting | FIT-YYYYMMDD-XXX |
| Khách hàng | Tên, SĐT |
| Lịch hẹn | Ngày + Giờ |
| Trạng thái | Mới đăng ký / Đã xác nhận / Đang thực hiện / Hoàn thành / Hủy |
| NV Fitting | Nhân viên thực hiện |
| Chi nhánh | Nơi thực hiện |
| Có đơn SP | Có phát sinh đơn hàng không |

### 3.34.2. Tạo đơn Fitting

**REQ-FIT-002:** Nguồn đăng ký
- Website (tự động tạo đơn)
- Tại cửa hàng
- Điện thoại

**REQ-FIT-003:** Thông tin đơn Fitting
- Khách hàng (chọn hoặc tạo mới)
- Lịch hẹn (ngày + giờ)
- Chi nhánh thực hiện
- NV Fitting phụ trách

### 3.34.3. Thông số kỹ thuật

**REQ-FIT-004:** Nhập thông số Fitting

| Thông số | Mô tả |
|----------|-------|
| Chiều cao | cm |
| Cân nặng | kg |
| Size tay | S/M/L/XL |
| Cấp độ | Người mới / Đã chơi |
| Tốc độ đầu gậy | mph |
| Tốc độ bóng | mph |
| Hình swing | Draw / Fade / Straight |
| Đường bóng | Low / Mid / High |
| Khoảng cách sắt | yards |
| Khoảng cách driver | yards |
| Tình trạng bộ gậy | Mô tả |
| Nhu cầu riêng | Ghi chú |

### 3.34.4. Dịch vụ phát sinh

**REQ-FIT-005:** Ghi nhận dịch vụ phát sinh
- Mua thêm grip
- Lắp shaft
- Đặt gậy theo thông số
- Combo fitting + gậy

**REQ-FIT-006:** Tạo đơn hàng từ Fitting
- Button "Tạo đơn hàng"
- Pre-fill từ dịch vụ phát sinh
- Link đơn hàng với đơn Fitting

### 3.34.5. Báo cáo Fitting

**REQ-FIT-007:** Các báo cáo
- Doanh thu phát sinh từ fitting
- Tổng số buổi fitting trong tháng
- Số lượng khách đến fitting
- Báo cáo linh kiện sử dụng
- Báo cáo NV thực hiện (doanh thu, tỉ lệ tư vấn thành công)

---

## 3.35. Quản lý Coaching ★ TM only

> **Định nghĩa:** Dịch vụ huấn luyện golf cho học viên với các gói học khác nhau
>
> **Giai đoạn:** Bàn giao T6 (30/06/2026)

### 3.35.1. Quản lý đơn Coaching

**REQ-COACH-001:** Danh sách đơn Coaching

| Trường thông tin | Mô tả |
|------------------|-------|
| Mã đơn | COACH-YYYYMMDD-XXX |
| Học viên | Tên, SĐT |
| Gói học | Tên gói huấn luyện |
| HLV | Huấn luyện viên phụ trách |
| Số buổi | Đã học / Tổng |
| Trạng thái | Mới / Đang học / Hoàn thành / Hủy |
| Sân tập | Địa điểm |
| Còn nợ | Số tiền chưa thanh toán |

### 3.35.2. Hồ sơ Học viên

**REQ-COACH-002:** Thông tin học viên
- Thông tin cá nhân
- Trình độ hiện tại
- Mục tiêu học
- Bài test đầu vào
- Kết quả đánh giá

### 3.35.3. Gói Huấn luyện

**REQ-COACH-003:** Quản lý gói học
- Tên gói (VD: 8 buổi cơ bản, 12 buổi nâng cao)
- Loại gói: Cá nhân / Nhóm / Thi đấu
- Số buổi
- Thời lượng/buổi
- Giá
- Mô tả chi tiết

### 3.35.4. Quản lý HLV

**REQ-COACH-004:** Hồ sơ HLV
- Liên kết với Nhân viên
- Chứng chỉ
- Kinh nghiệm
- Chuyên môn
- Đánh giá

### 3.35.5. Lịch học & Điểm danh

**REQ-COACH-005:** Quản lý buổi học
- Buổi thứ mấy
- Thời gian dự kiến
- Thời gian thực tế
- Trạng thái: Đã lên lịch / Hoàn thành / Vắng mặt / Hủy
- Nội dung buổi học
- Ghi chú tiến trình
- Bài tập về nhà

**REQ-COACH-006:** Điểm danh
- Có mặt → Tăng số buổi đã học
- Vắng có báo → Cho phép học bù
- Vắng không báo → Theo chính sách

### 3.35.6. Tiến độ Học tập

**REQ-COACH-007:** Theo dõi tiến độ
- Đánh giá kỹ năng (swing, putting, chipping...)
- Đánh giá định kỳ (đầu - giữa - cuối kỳ)
- Nhận xét chuyên môn từ HLV

### 3.35.7. Thông báo tự động

**REQ-COACH-008:** Gửi thông báo
- Nhắc lịch học qua Zalo/Email
- Thông báo thay đổi giờ học
- Nhắc học bù khi vắng mặt
- Thông báo hoàn thành khóa

### 3.35.8. Báo cáo Coaching

**REQ-COACH-009:** Các báo cáo
- Doanh thu từ coaching
- Doanh thu SP phát sinh sau coaching
- Số lượng học viên
- Doanh số theo từng HLV
- Tỉ lệ hoàn thành khóa học

---

## 3.36. Cài đặt hệ thống

### 3.36.1. Mô tả
Module cho phép quản trị viên cấu hình các thông số hệ thống, bao gồm thông tin công ty, cài đặt mặc định, quản lý template email/SMS và các tùy chỉnh khác.

### 3.36.2. Tính năng chính
- Cấu hình thông tin công ty (tên, logo, địa chỉ, MST)
- Cài đặt mặc định (kho, bảng giá, điều khoản thanh toán)
- Quản lý template email / thông báo
- Cấu hình workflow phê duyệt
- Quản lý danh sách giá trị (dropdown) tùy chỉnh

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.37. Chăm sóc Khách hàng tự động

> **Giai đoạn:** Bàn giao T6 (30/06/2026)

### 3.37.1. Lịch chăm sóc

**REQ-CUST-003:** Lịch chăm sóc tự động
- Giao nhiệm vụ chăm sóc định kỳ cho nhân viên
- Nhắc lịch chăm sóc khách VIP, khách lâu chưa mua
- Gửi thông báo nội bộ khi đến hạn

### 3.37.2. Khuyến mãi tự động

**REQ-CUST-004:** Lịch gửi khuyến mãi tự động
- Lọc nhóm khách theo tags, chi tiêu, tần suất mua
- Thiết lập lịch gửi khuyến mãi tự động
- Gửi qua Zalo/Email

### 3.37.3. Phiếu hỗ trợ

**REQ-CUST-005:** Phiếu hỗ trợ (Ticket)
- Tạo ticket khi khách có yêu cầu hỗ trợ, bảo hành, khiếu nại
- Phân công người xử lý
- Trạng thái: Chưa xử lý → Đang xử lý → Đã xong
- Ghi chú quá trình xử lý

### 3.37.4. Khảo sát

**REQ-CUST-006:** Khảo sát mức độ hài lòng
- Gửi form khảo sát sau mua hàng
- Gửi form khảo sát sau CSKH
- Tổng hợp điểm hài lòng

### 3.37.5. Gợi ý bán hàng

**REQ-CUST-007:** Gợi ý Upsell/Cross-sell
- Phân tích lịch sử mua hàng
- Gợi ý sản phẩm phù hợp
- Hỗ trợ gửi gợi ý qua tin nhắn/email

---

## 3.38. Đơn hàng nâng cao

> **Giai đoạn:** Bàn giao T6 (30/06/2026)

### 3.38.1. Bảo hành

**REQ-ORDER-008:** Phiếu bảo hành
- Tạo phiếu bảo hành cho từng sản phẩm
- Thông tin: Mã đơn, Sản phẩm, Ngày bắt đầu, Ngày hết hạn, Mô tả lỗi
- Đính kèm hình ảnh
- Trạng thái: Mới nhận → Đang xử lý → Chờ linh kiện → Hoàn tất

### 3.38.2. Thông báo bảo hành

**REQ-ORDER-009:** Thông báo bảo hành
- Tự động gửi thông báo tiến độ cho khách

---

## 3.39. Tích hợp Giao vận

> **Giai đoạn:** Bàn giao T6 (30/06/2026)

### 3.39.1. Tạo đơn giao vận

**REQ-SHIP-001:** Liên kết Viettel Post
- Tạo đơn giao vận từ hệ thống sang Viettel Post
- Tự động lấy: Mã vận đơn, Phí ship, Dịch vụ

**REQ-SHIP-002:** Đồng bộ trạng thái
- Tự động cập nhật trạng thái giao hàng
- Các trạng thái: Đã lấy / Đang vận chuyển / Đang giao / Đã giao / Hoàn trả

### 3.39.2. Quản lý đơn giao vận

**REQ-SHIP-003:** Danh sách đơn giao vận
- Mã vận đơn
- Trạng thái giao hàng
- Ngày dự kiến giao
- Phí ship
- Liên kết đơn hàng

**REQ-SHIP-004:** Xử lý hàng hoàn
- Cập nhật lại tồn kho khi có hàng hoàn
- Ghi nhận lý do hoàn

---

## 3.40. Role & Permission

> **Giai đoạn:** Bàn giao T6 (30/06/2026)

### 3.40.1. Quản lý Role

**REQ-AUTH-001:** CRUD Role
- Tạo role mới
- Gán quyền cho role
- Gán user vào role

### 3.40.2. Ma trận phân quyền

**REQ-AUTH-002:** Phân quyền theo module
- Xem / Tạo / Sửa / Xóa theo từng module
- Phân quyền theo chi nhánh
- Phân quyền xem giá (Kho không thấy giá)

### 3.40.3. Audit Log

**REQ-AUTH-003:** Ghi nhận hoạt động
- Log tất cả thao tác quan trọng
- Ai làm gì, lúc nào
- Truy vết thay đổi dữ liệu

---

## 3.41. Kiểm soát

### 3.41.1. Mô tả
Module cung cấp các công cụ kiểm soát nội bộ, giám sát hoạt động hệ thống và đảm bảo tính chính xác của dữ liệu. Hỗ trợ đối chiếu dữ liệu giữa các phân hệ.

### 3.41.2. Tính năng chính
- Đối chiếu dữ liệu kho - kế toán
- Đối chiếu công nợ khách hàng - nhà cung cấp
- Kiểm tra tính nhất quán dữ liệu giữa các phân hệ
- Báo cáo bất thường (anomaly detection)
- Nhật ký kiểm soát (audit trail)

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## T8: THÁNG 8/2026

---

## 3.42. Membership ★ TM only

### 3.42.1. Mô tả
Module quản lý chương trình Membership dành cho khách hàng thân thiết, bao gồm quản lý gói/thẻ thành viên, QR check-in tại cửa hàng và cơ chế nâng/hạ hạng thành viên.

### 3.42.2. Tính năng chính
- Quản lý các gói Membership (hạng thành viên, quyền lợi)
- Phát hành thẻ thành viên (vật lý hoặc số)
- QR check-in khi khách đến cửa hàng
- Cơ chế nâng hạng / hạ hạng tự động theo doanh số
- Theo dõi quyền lợi đã sử dụng
- Báo cáo Membership (số lượng thành viên, tỉ lệ sử dụng)

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.43. Dự báo Doanh thu ★ TM only

### 3.43.1. Mô tả
Module hỗ trợ dự báo doanh thu và cảnh báo sớm khi có nguy cơ hụt doanh số so với kế hoạch. Giúp ban lãnh đạo chủ động điều chỉnh chiến lược kinh doanh.

### 3.43.2. Tính năng chính
- Dự báo doanh thu theo xu hướng lịch sử
- Cảnh báo hụt doanh số so với kế hoạch
- So sánh doanh thu thực tế vs kế hoạch theo thời gian thực
- Dashboard cảnh báo cho ban lãnh đạo
- Phân tích nguyên nhân chênh lệch

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

## 3.44. Workshop/Event ★ TM only

### 3.44.1. Mô tả
Module quản lý các hoạt động Workshop và Event của doanh nghiệp, bao gồm đơn hàng dịch vụ liên quan và theo dõi hiệu quả sự kiện.

### 3.44.2. Tính năng chính
- Tạo và quản lý Workshop/Event (tên, ngày, địa điểm, mô tả)
- Đơn hàng dịch vụ gắn với Workshop/Event
- Tag đơn hàng theo Workshop/Event để theo dõi doanh thu
- Quản lý danh sách khách tham gia
- Báo cáo hiệu quả sự kiện (doanh thu, số khách, chi phí)

> ⚠️ Chi tiết sẽ được bổ sung khi có thêm thông tin từ khách hàng

---

# 4. YÊU CẦU PHI CHỨC NĂNG

## 4.1. Hiệu năng (Performance)

| Chỉ số | Yêu cầu |
|--------|---------|
| Thời gian tải trang | ≤ 3 giây |
| Thời gian xử lý giao dịch | ≤ 5 giây |
| Số người dùng đồng thời | ≥ 30 users |
| Thời gian tạo báo cáo | ≤ 30 giây (báo cáo phức tạp) |

## 4.2. Bảo mật (Security)

| Yêu cầu | Mô tả |
|---------|-------|
| Mã hóa | HTTPS/TLS 1.2+ |
| Xác thực | Username/Password + 2FA (optional) |
| Session | Timeout sau 30 phút không hoạt động |
| Password | Tối thiểu 8 ký tự, có chữ hoa/thường/số |
| Backup | Sao lưu hàng ngày, lưu trữ 30 ngày |

## 4.3. Tính sẵn sàng (Availability)

| Chỉ số | Yêu cầu |
|--------|---------|
| Uptime | ≥ 99.5% |
| Thời gian phục hồi (RTO) | ≤ 4 giờ |
| Điểm phục hồi (RPO) | ≤ 24 giờ |
| Bảo trì định kỳ | Ngoài giờ làm việc |

## 4.4. Khả năng mở rộng (Scalability)

| Yêu cầu | Mô tả |
|---------|-------|
| Dữ liệu | Hỗ trợ 1 triệu records/bảng |
| Users | Mở rộng đến 200 users |
| Chi nhánh | Mở rộng đến 50 chi nhánh |
| Tích hợp | Cho phép thêm API mới |

## 4.5. Tương thích (Compatibility)

| Thành phần | Yêu cầu |
|------------|---------|
| Trình duyệt | Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ |
| Mobile | Responsive design, tương thích iOS/Android |
| Màn hình | 1366x768 trở lên |
| In ấn | Hỗ trợ in A4, A5 |

---

# 5. GIAO DIỆN HỆ THỐNG

## 5.1. Giao diện người dùng (UI)

### 5.1.1. Nguyên tắc thiết kế

- **Responsive**: Tự động điều chỉnh theo kích thước màn hình
- **Tiếng Việt**: Giao diện hoàn toàn tiếng Việt
- **Nhất quán**: Thống nhất màu sắc, font chữ, button style
- **Trực quan**: Dễ sử dụng, ít cần đào tạo

### 5.1.2. Bố cục chung

```
┌─────────────────────────────────────────────────────────────┐
│                        HEADER                                │
│  [Logo]  [Menu]                    [Thông báo] [User Menu]  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐  ┌───────────────────────────────────────────┐ │
│  │         │  │                                           │ │
│  │ SIDEBAR │  │              NỘI DUNG CHÍNH               │ │
│  │         │  │                                           │ │
│  │ • Menu  │  │  [Breadcrumb]                            │ │
│  │ • Items │  │  [Toolbar: Tạo | Filter | Export]        │ │
│  │         │  │  [Danh sách / Form / Dashboard]          │ │
│  │         │  │                                           │ │
│  └─────────┘  └───────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 5.2. Giao diện API (External Integrations)

### 5.2.1. REST API

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/leads` | GET, POST | Quản lý Lead |
| `/api/customers` | GET, POST | Quản lý Khách hàng |
| `/api/orders` | GET, POST | Quản lý Đơn hàng |
| `/api/products` | GET | Danh sách sản phẩm |
| `/api/stock` | GET | Tồn kho |

### 5.2.2. Webhook

| Event | Mô tả |
|-------|-------|
| `order.created` | Khi có đơn hàng mới |
| `order.status_changed` | Khi trạng thái đơn thay đổi |
| `stock.low` | Khi tồn kho dưới định mức |

## 5.3. Giao diện phần cứng

### 5.3.1. Máy in

| Loại | Mục đích |
|------|----------|
| Máy in laser A4 | In hóa đơn, báo cáo |
| Máy in nhiệt (thermal) | In phiếu xuất kho, tem nhãn |
| Máy in tem | In barcode, QR code |

### 5.3.2. Thiết bị scan

| Loại | Mục đích |
|------|----------|
| Máy quét barcode cầm tay | Quét sản phẩm khi bán hàng |
| Máy quét barcode không dây | Quét trong kho |

---

# 6. PHỤ LỤC

## 6.1. Danh sách tính năng chi tiết

Xem file đính kèm: **[Phụ lục A - Feature Matrix](appendix/tm/A_FEATURE_MATRIX.md)**

## 6.2. Sơ đồ ERD

Xem file đính kèm: **[Phụ lục B - ERD Diagrams](appendix/tm/B_ERD_DIAGRAMS.md)**

## 6.3. Sơ đồ Workflow

Xem file đính kèm: **[Phụ lục C - Workflow Diagrams](appendix/tm/C_WORKFLOW_DIAGRAMS.md)**

## 6.4. Ma trận Phân quyền

Xem file đính kèm: **[Phụ lục D - Permission Matrix](appendix/tm/D_PERMISSION_MATRIX.md)**

---

# CHẤP THUẬN

Tài liệu này đã được xem xét và chấp thuận bởi các bên liên quan:

| Vai trò | Họ tên | Chữ ký | Ngày |
|---------|--------|--------|------|
| **Bên A (Khách hàng)** | | | |
| Đại diện Thăng Long TM | _________________ | _________________ | ____/____/2026 |
| **Bên B (Nhà cung cấp)** | | | |
| Đại diện DCNET Corporation | _________________ | _________________ | ____/____/2026 |

---

**© 2026 DCNET Corporation**

**Tài liệu này là phụ lục của Hợp đồng số .../HĐDV/DCNET-TLTM**
