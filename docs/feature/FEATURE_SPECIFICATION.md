# DCNET Flow - Đặc tả Chức năng CRM

> **Tài liệu chính thức** - Trích xuất từ PHỤ LỤC SỐ 01 Hợp đồng DCNET-NMS
>
> **Phiên bản**: 1.1.0 | **Cập nhật**: 24/01/2026 | **Khách hàng**: Nhật Minh Sport
>
> **Nguồn gốc**:
> - `(DCNET X NMS)_CRM_V12_300525.pdf` - PHỤ LỤC hợp đồng chính thức
> - `PHỤ LỤC _ MÔ TẢ TÍNH NĂNG WEBSITE CRM NHẬT MINH.docx`
> - `PHASE_1_FEATURES.xlsx` - Bảng features chi tiết (14/01/2026)

### 📝 Lịch sử cập nhật

| Ngày | Nội dung | Người cập nhật |
|------|----------|----------------|
| 24/01/2026 | **Đồng bộ với PHASE_1_FEATURES.xlsx**: Cập nhật tổng 23 modules, 135 features. Thêm Import KH, Export SP, Import/Export NV. Chi tiết Dashboard 6 features, CSKH 7 features | DCNET |
| 14/01/2026 | Bổ sung Section 13: Thêm 4 danh sách cài đặt (Chức vụ, Nhóm KH, Trạng thái ĐH, Hành động NV) | DCNET |
| 14/01/2026 | Xóa "Đồng bộ danh mục sản phẩm" (Section 6.2) - không còn Bravo | DCNET |
| 13/01/2026 | Thêm Section 18: Quản lý Thu cũ Đổi mới (Module riêng, chia 2 đợt) | DCNET |
| 13/01/2026 | Xóa tham chiếu Bravo ERP - dự án sẽ build native (Kho, Sản phẩm, Chi nhánh) | DCNET |
| 13/01/2026 | Thêm Section 16: Quản lý Fitting (Module riêng, chia 2 đợt) | DCNET |
| 13/01/2026 | Thêm Section 17: Quản lý Coaching (Module riêng, chia 2 đợt) | DCNET |
| 08/12/2025 | Phiên bản gốc từ PHỤ LỤC hợp đồng | Nhật Minh Sport |

---

## Mục lục

1. [Đăng nhập/Đăng xuất](#1-đăng-nhậpđăng-xuất)
2. [Dashboard](#2-dashboard)
3. [Quản lý Lead](#3-quản-lý-lead)
4. [Quản lý Khách hàng](#4-quản-lý-khách-hàng)
5. [Quản lý Đơn hàng](#5-quản-lý-đơn-hàng)
6. [Quản lý Sản phẩm](#6-quản-lý-sản-phẩm)
7. [Quản lý Bán hàng](#7-quản-lý-bán-hàng)
8. [Quản lý Kho](#8-quản-lý-kho)
9. [Quản lý Giao vận](#9-quản-lý-giao-vận)
10. [Quản lý Chi nhánh](#10-quản-lý-chi-nhánh)
11. [Quản lý Nhân viên](#11-quản-lý-nhân-viên)
12. [Role & Permission](#12-role--permission)
13. [Cài đặt](#13-cài-đặt)
14. [Báo cáo](#14-báo-cáo)
15. [Hệ thống Report Website](#15-hệ-thống-report-website)
16. [Quản lý Fitting](#16-quản-lý-fitting) ⭐ *Module riêng*
17. [Quản lý Coaching](#17-quản-lý-coaching) ⭐ *Module riêng*
18. [Quản lý Thu cũ Đổi mới](#18-quản-lý-thu-cũ-đổi-mới) ⭐ *Module riêng*

---

## Tổng quan Phase 1: CRM

> **Duration**: 90 ngày | **Total**: 23 modules, 135 features
>
> **Source**: PHASE_1_FEATURES.xlsx | **Last Updated**: 24/01/2026

### Tổng kết theo Đợt

| Đợt | Thời gian | Số modules | Số features |
|-----|-----------|------------|-------------|
| **Đợt 1**: Foundation & Core CRM | 50 ngày | 11 | 74 |
| **Đợt 2**: Advanced Features & Operations | 30 ngày | 9 | 48 |
| **Đợt 3**: Reports & Security | 10 ngày | 3 | 13 |
| **TỔNG** | **90 ngày** | **23 modules** | **135 features** |

### Chi tiết Modules theo Đợt

| Giai đoạn | Modules |
|-----------|---------|
| **Đợt 1** | Đăng nhập/Đăng xuất, Quản lý Lead, Quản lý Khách hàng, Quản lý Đơn hàng, Quản lý Sản phẩm, Quản lý Chi nhánh, Quản lý Nhân viên, Cài đặt, **Quản lý Fitting (core)**, **Quản lý Coaching (core)**, **Quản lý Thu cũ Đổi mới (core)** |
| **Đợt 2** | Dashboard, Chăm sóc Khách hàng, Quản lý Đơn hàng (Nâng cao), **Quản lý Fitting (Tích hợp)**, **Quản lý Coaching (Tích hợp)**, **Quản lý Thu cũ Đổi mới (Tích hợp)**, Quản lý Bán hàng, Quản lý Kho, Quản lý Giao vận |
| **Đợt 3** | Role & Permission, Báo cáo, Hệ thống Report Website |

---

## 1. Đăng nhập/Đăng xuất

> **Giai đoạn:** Bàn giao đợt 1

### Chức năng:

| Chức năng | Mô tả |
|-----------|-------|
| Đăng nhập | Đăng nhập bằng email/Password |
| Đăng xuất | Đăng xuất chủ động |
| Quên mật khẩu | Lấy lại mật khẩu |

---

## 2. Dashboard

> **Giai đoạn:** Bàn giao đợt 2
>
> **Tổng features:** 6

### 2.1. Doanh số theo ngày, tuần, tháng

- Hiển thị doanh số theo các mốc thời gian
- Filter theo khoảng thời gian tùy chọn

### 2.2. Doanh số bán sỉ

- Đơn hàng từ khách sỉ
- Thống kê theo đại lý

### 2.3. Doanh số bán lẻ tổng

- Tổng doanh số bán lẻ từ tất cả kênh

### 2.4. Doanh số theo từng nguồn khách hàng

- Breakdown doanh số theo nguồn KH (Facebook, Zalo, Website, Cửa hàng...)

### 2.5. Doanh số theo từng nguồn đơn hàng

- Breakdown doanh số theo nguồn đơn (Online, Offline, TMĐT...)

### 2.6. Doanh số theo sản phẩm (Top 20)

- Top 20 sản phẩm bán chạy nhất
- Biểu đồ doanh số theo sản phẩm

---

## 3. Quản lý Lead

> **Định nghĩa:** Data cơ hội khách hàng mới có quan tâm mua hàng nhưng chưa có giao dịch thành công
>
> **Giai đoạn:** Bàn giao đợt 1

### 3.1. Danh sách Lead

**Hiển thị các cột thông tin:**
- Mã khách hàng
- Tên
- ĐT
- Trạng thái (có thể chuyển tại DS)
- Email
- Tags (có thể thêm tại DS)
- Thời gian tạo
- Ngày nhận lead
- Liên hệ lần cuối
- Tổng số tương tác
- Người tạo
- Nguồn lead
- Chi nhánh
- Địa chỉ
- Giới tính

**Tính năng:**
- Ẩn/hiện thông tin cột
- Cập nhật tags

**Search/Filter:**
- Tìm kiếm theo: tên, email
- Filter theo:
  - Trạng thái
  - Trạng thái phụ trách (có/chưa NV phụ trách)
  - Thời gian tạo
  - Chi nhánh
  - NV phụ trách
  - Người tạo
  - Độ tuổi
  - Tags

### 3.2. Tạo Lead

**Thông tin cơ bản:**
- Mã (auto)
- Ngày nhận
- Tên
- Giới tính
- ĐT
- Email
- Ngày sinh
- Nhân viên phụ trách

**Thông tin nâng cao:**
- Trạng thái (VD: chưa nghe máy, đang tư vấn, đang giao hàng, thuê bao, hủy)
- Tags
- Nguồn
- Chi nhánh
- Địa chỉ: Tỉnh thành phố, Quận huyện, Phường xã
- Bảng giá áp dụng
- Sale chăm sóc

**Tính năng bổ sung:**
- Check trùng thông tin

### 3.3. Import danh sách Lead

| Chức năng | Mô tả |
|-----------|-------|
| Import Lead | File excel |

### 3.4. Xem chi tiết Lead

**Xem thông tin lead:**
- Xem các thông tin cơ bản
- Lịch sử giao dịch
- Hàng hóa đã mua
- Tài liệu đi kèm

**Lịch sử tư vấn:**
- Sản phẩm đã tư vấn
- Nhân viên tư vấn
- Ngày tháng tư vấn
- Nội dung tư vấn

**Bình luận/thay đổi bình luận:**
- Bình luận gắn với hoạt động (gọi, sms, email, FB, Zalo)

**Action:**
- Tạo đơn hàng (Router đến Tạo đơn hàng)
- Xem tài liệu

### 3.5. Cập nhật Lead

- Cập nhật thông tin cơ bản
- Cập nhật tài liệu (Thêm, xóa tài liệu)
- Cập nhật người phụ trách

### 3.6. Xóa Lead

- Xóa lead khỏi hệ thống

### 3.7. Tự động tạo Lead từ nguồn bên ngoài

| Chức năng | Mô tả |
|-----------|-------|
| Tự động tạo lead mới từ nhanh_vn | Về với các nguồn đa kênh |

### 3.8. Export danh sách Lead

| Chức năng | Mô tả |
|-----------|-------|
| Export Lead | File excel |

### 3.9. Expose API tạo khách hàng

| Chức năng | Mô tả |
|-----------|-------|
| Expose API | Xây dựng cổng API cho phép tạo khách hàng mới với nguồn từ hệ thống khác nhằm xác nhận rõ nguồn khách hàng nhận được |

---

## 4. Quản lý Khách hàng

> **Định nghĩa:** Khách hàng đã phát sinh giao dịch

### 4.1. Danh sách Khách hàng

> **Giai đoạn:** Bàn giao đợt 1

**Hiển thị các cột thông tin:**
- Mã khách hàng
- Tên
- ĐT
- Email
- Facebook
- Zalo
- Tags (có thể thêm tại DS)
- Loại khách hàng (Lẻ/Sỉ)
- Bảng giá áp dụng
- Thời gian tạo
- Ngày tạo
- Ngày nhận lead
- Liên hệ lần cuối
- Tổng số đơn hàng phát sinh
- Tổng số tương tác
- Người tạo
- Người phụ trách
- Nguồn lead
- Chi nhánh
- Địa chỉ
- Giới tính
- Số điểm hiện tại
- Doanh số phát sinh
- Công nợ
- Lịch chăm sóc định kỳ (ngày)
- Tài liệu liên quan

**Lưu ý:**
- Với khách hàng có nguồn từ Facebook thì cần có link khách hàng
- Mặc định trường thông tin trong Zalo là SĐT mua hàng

**Tính năng:**
- Ẩn/hiện thông tin cột
- Cập nhật tags

**Search/Filter:**
- Tìm kiếm theo: tên, email
- Filter theo:
  - Chi nhánh
  - Thời gian tạo
  - Ngày sinh nhật
  - Ngày giao dịch cuối
  - NV phụ trách
  - Người tạo
  - Độ tuổi
  - Tags
  - Loại khách hàng (Lẻ/Sỉ)
  - Doanh số (trong khoảng)
  - Công nợ (trong khoảng)

### 4.2. Xem chi tiết Khách hàng

> **Giai đoạn:** Bàn giao đợt 1

**Xem thông tin khách hàng:**
- Xem các thông tin cơ bản
- Công nợ
- Lịch sử giao dịch
- Điểm hiện tại
- Lịch sử tích điểm
- Hàng hóa đã mua
- Tài liệu đi kèm
- Bảng giá đang áp dụng

**Bình luận/thay đổi bình luận:**
- Bình luận gắn với hoạt động (gọi, sms, email, FB, Zalo)

**Action:**
- Tạo đơn hàng (Router đến Tạo đơn hàng)
- Xem tài liệu

### 4.3. Chăm sóc Khách hàng

> **Giai đoạn:** Bàn giao đợt 2
>
> **Tổng features:** 7

#### 4.3.1. Lịch chăm sóc tự động (CRUD)

- Giao nhiệm vụ chăm sóc định kỳ cho nhân viên: gọi lại sau mua hàng, nhắn tin hỏi cảm nhận...
- Nhắc lịch chăm sóc khách VIP, khách lâu chưa mua
- Tự động gửi thông báo nội bộ khi đến hạn chăm sóc

#### 4.3.2. Lịch gửi khuyến mãi tự động (CRUD)

- Chọn lọc nhóm khách cụ thể để gửi khuyến mãi phù hợp
- VD: Khách hay mua mũ → giảm giá mũ
- VD: Khách từ Elite Club → ưu đãi riêng, không trùng với khách lẻ
- CRM cho phép lọc theo tag, chi tiêu, tần suất mua hàng…
- Auto send promotions

#### 4.3.3. Phiếu hỗ trợ - Ticket (CRUD)

- Khi khách có yêu cầu hỗ trợ, bảo hành, khiếu nại → tạo ticket để theo dõi
- Phân công người xử lý (Assignment), ghi chú quá trình xử lý
- Trạng thái: **Chưa xử lý** / **Đang xử lý** / **Đã xong**

#### 4.3.4. Phân quyền CSKH theo nhóm

- Mỗi nhân viên chăm 1 nhóm khách cụ thể (VD: bạn A chuyên chăm khách đại lý, bạn B chăm khách từ Elite Club...)
- CRM giúp phân công rõ ràng, dễ theo dõi hiệu suất
- Assign care groups to staff

#### 4.3.5. Khảo sát mức độ hài lòng

- Gửi form khảo sát sau mua hàng
- Gửi form khảo sát sau CSKH
- Gửi form khảo sát sau khi xử lý khiếu nại

#### 4.3.6. Tích hợp Zalo/Messenger

- Tích hợp Zalo OA vào hệ thống
- Tích hợp Messenger vào hệ thống
- Giao tiếp đa kênh trong CRM

#### 4.3.7. Upsell/Cross-sell

- Gợi ý sản phẩm phù hợp dựa trên lịch sử mua hàng
- Tự động gửi gợi ý qua tin nhắn/email (VD: khách mua găng → gợi ý mũ cùng màu)

### 4.4. Cập nhật Khách hàng

> **Giai đoạn:** Bàn giao đợt 1

- Cập nhật thông tin cơ bản
- Cập nhật chiết khấu theo danh mục sản phẩm
- Thiết lập lịch chăm sóc
- Cập nhật tài liệu (Thêm, xóa tài liệu)
- Cập nhật người phụ trách

### 4.5. Quản lý Nguồn Khách hàng

> **Giai đoạn:** Bàn giao đợt 1

- Danh sách nguồn khách hàng
- Thêm nguồn khách hàng
- Cập nhật/xóa nguồn khách hàng

### 4.6. Quản lý Tích điểm

> **Giai đoạn:** Bàn giao đợt 1

- Quy tắc tính điểm
- Quy tắc lên hạng

### 4.7. Xóa Khách hàng

> **Giai đoạn:** Bàn giao đợt 1

### 4.8. Import danh sách Khách hàng

> **Giai đoạn:** Bàn giao đợt 1
>
> ⭐ *Mới thêm từ PHASE_1_FEATURES.xlsx*

| Chức năng | Mô tả |
|-----------|-------|
| Import Khách hàng | File excel |

### 4.9. Export danh sách Khách hàng

> **Giai đoạn:** Bàn giao đợt 1

| Chức năng | Mô tả |
|-----------|-------|
| Export Khách hàng | File excel |

---

## 5. Quản lý Đơn hàng

### 5.1. Danh sách Đơn hàng

> **Giai đoạn:** Bàn giao đợt 1

**Hiển thị các cột thông tin:**
- Mã đơn hàng
- Khách hàng
- Loại đơn (Lẻ/Sỉ)
- Trạng thái đơn hàng (chưa xử lý, đang xuất kho, đã xuất kho, đang vận chuyển, hoàn thành, hoàn trả, hủy)
- Giá trị đơn hàng
- Nguồn đơn hàng
- Thời gian tạo đơn
- Thời gian duyệt
- Đã trả
- Còn nợ
- Chi nhánh bán
- Kho xử lý
- Ghi chú
- Ghi chú nội bộ

**Loại danh sách:**
- Danh sách đơn vật dụng (bán lẻ, bán buôn) - Tách riêng để tránh nhầm lẫn
- Đơn fitting
- Đơn coaching
- Đơn thu cũ đổi mới

> Mỗi đơn hàng sẽ render ra một mã đơn hàng tự động

**Tính năng:**
- Ẩn/hiện thông tin cột
- Cập nhật tags

**Search/Filter:**
- Tìm kiếm theo: tên, email
- Filter theo:
  - Chi nhánh
  - Thời gian
  - Trạng thái đơn
  - Tags khách hàng
  - Nguồn đơn hàng
  - Loại đơn (Lẻ/Sỉ)

### 5.2. Tạo Đơn hàng

> **Giai đoạn:** Bàn giao đợt 1

#### 5.2.1. Tạo đơn hàng cho các loại vật dụng (Áo, Gậy,...)

**Thông tin:**
- Nguồn đơn
- Khách hàng (nếu chưa có thì mở ra popup tạo mới)
- Số điện thoại
- Địa chỉ nhận hàng (chọn chi nhánh hoặc nhập địa chỉ của khách)
- Thời gian tạo đơn hàng
- Người tạo đơn hàng
- Kho xuất hàng
- Voucher
- Tích điểm
- Phương thức thanh toán (tiền mặt/chuyển khoản/COD)
- Giảm giá (nhập số)
- Thực nhận
- Chọn sản phẩm

**Loại đơn:**
- **Đơn bán lẻ:** Tạo tại cửa hàng vật lý hoặc đơn online cho người dùng
- **Đơn bán buôn:** Tạo cho các đại lý trên hệ thống

#### 5.2.2. Tạo đơn hàng Fitting

> ⭐ **Lưu ý:** Fitting là **module quản lý riêng biệt** với workflow và entity riêng.
> Xem chi tiết tại **[Section 16: Quản lý Fitting](#16-quản-lý-fitting)**
>
> Đơn hàng Fitting trong Section 5 này là **Sales Order phát sinh từ buổi Fitting** (grip, shaft, gậy custom...)

**Quy trình:**
- Đăng ký fitting qua website → đẩy thông tin vào CRM
- Tạo lịch fitting
- Ghi lại thông tin sau khi fitting:
  - Đề xuất nâng cấp
  - Nhân viên phụ trách
  - Phụ kiện phát sinh từ buổi fitting

**Thông tin kỹ thuật:**
- Thời gian
- Tên tuổi
- Chiều cao
- Cân nặng
- Kích thước size tay
- Cấp độ (người mới, người đã chơi)
- Tốc độ đầu gậy
- Tốc độ bóng
- Hình swing
- Đường bóng
- Đường cao bóng
- Khoảng cách của bóng gậy sắt
- Khoảng cách của bóng gậy driver
- Tình trạng bộ gậy của khách
- Nhu cầu riêng của KH (Note)

#### 5.2.3. Tạo đơn hàng Coaching

> ⭐ **Lưu ý:** Coaching là **module quản lý riêng biệt** với workflow và entity riêng.
> Xem chi tiết tại **[Section 17: Quản lý Coaching](#17-quản-lý-coaching)**
>
> Đơn hàng Coaching trong Section 5 này là **Sales Order phát sinh từ khóa học** (gói học, phụ kiện...)

**Thông tin:**
- Hồ sơ học viên: thông tin cá nhân, trình độ, mục tiêu, bài test đầu vào
- Gói huấn luyện đăng ký (VD: 8 buổi cơ bản, Thi đấu nâng cao 12 buổi)
- HLV phụ trách
- Tạo lịch coaching
- Tổng học phí
- Ưu đãi nếu có
- Địa điểm học: sân tập
- Loại khóa học
- Sân tập
- Mục tiêu học

**Thông tin kỹ thuật:** (tương tự Fitting)

#### 5.2.4. Tạo đơn hàng Thu cũ Đổi mới

**Thông tin:**
- Thông tin sản phẩm khách trả lại (gậy cũ)
- Thông tin sản phẩm mới nhận
- Giá trị bù trừ (khách cần trả thêm hoặc nhận lại nếu có)

**Tính năng:**
- Gắn 2 dòng sản phẩm trong cùng một giao dịch
- Cho phép tính giá trị chênh lệch:
  - Giá gậy mới - Giá thu gậy cũ - Voucher (nếu có) = Số tiền khách thanh toán

#### 5.2.5. Tạo đơn bảo hành/bảo trì

#### 5.2.6. Kiểm tra tồn kho

- Kiểm tra tồn kho sản phẩm trước khi tạo đơn
- Hiển thị số lượng tồn theo kho

### 5.3. Import Đơn hàng

> **Giai đoạn:** Bàn giao đợt 1

| Chức năng | Mô tả |
|-----------|-------|
| Import Đơn hàng | File excel |

### 5.4. Xem chi tiết Đơn hàng

> **Giai đoạn:** Bàn giao đợt 1

**Xem chi tiết đơn hàng Áo, Gậy,...**

**Xem chi tiết đơn Fitting:**
- Theo dõi lịch sử fitting khách hàng
- Khách fitting → phát sinh các dịch vụ khác:
  - Mua thêm grip
  - Lắp shaft
  - Đặt gậy theo thông số đặc biệt
  - Mua combo fitting + gậy
- CRM sẽ gắn dịch vụ + sản phẩm đó vào hồ sơ khách hàng để theo dõi toàn diện

**Xem chi tiết đơn Coaching:**
- Lịch học & điểm danh: Lịch từng buổi, tình trạng học
- Nội dung từng buổi học
- Tiến độ học tập: Tổng quan kỹ năng, vd: kỹ năng (swing, putting,...)
- Thông báo & Nhắc lịch tự động: CRM gửi lịch học, thay đổi giờ học, lịch thi đấu qua Zalo/Email
- Phân tích kỹ thuật: nhận xét chuyên môn, lưu trữ theo thời gian
- Đánh giá định kỳ: Đầu - giữa - cuối kỳ
- Lịch sử tương tác & hỗ trợ học viên: Ghi chú các buổi tư vấn, hẹn thêm giờ, phản hồi từ học viên

**Xem chi tiết đơn thu cũ đổi mới**

**Trạng thái bảo hành/bảo trì**

**Công nợ theo đơn hàng**

### 5.5. Cập nhật Đơn hàng

> **Giai đoạn:** Bàn giao đợt 1

- Cập nhật đơn hàng Áo, Gậy,.. (Chuyển sang bộ phận kho xử lý)
- Cập nhật đơn Fitting (dịch vụ phát sinh)
- Cập nhật đơn Coaching
- Cập nhật đơn thu cũ đổi mới

### 5.6. Bảo hành

> **Giai đoạn:** Bàn giao đợt 2

**Cập nhật bảo hành:**
- Tạo phiếu bảo hành cho từng sản phẩm (gậy, túi, máy đo khoảng cách…)
- Ghi rõ thông tin:
  - Mã đơn hàng
  - Tên khách
  - Sản phẩm
  - Ngày bắt đầu bảo hành
  - Ngày hết hạn bảo hành
  - Mô tả lỗi/hỏng
  - Ảnh kèm theo (nếu có)
- Gắn trạng thái: Mới nhận → Đang xử lý → Đang chờ linh kiện → Hoàn tất
- Tự động gửi thông báo cho khách về tiến độ xử lý

### 5.7. Xóa Đơn hàng

> **Giai đoạn:** Bàn giao đợt 2

### 5.8. In Đơn hàng

> **Giai đoạn:** Bàn giao đợt 2

### 5.9. Resell

> **Giai đoạn:** Bàn giao đợt 2

- Cập nhật trạng thái đơn hàng đến khách qua email/Zalo/SMS
- Gửi feedback sau khi giao hàng
- Đề xuất mua lại / bán chéo sau khi hoàn tất đơn hàng

### 5.10. Export Đơn hàng

> **Giai đoạn:** Bàn giao đợt 2

| Chức năng | Mô tả |
|-----------|-------|
| Export Đơn hàng | File excel |

### 5.11. Expose API tạo Đơn hàng

> **Giai đoạn:** Bàn giao đợt 2

### 5.12. Kết nối Đơn hàng (Đồng bộ sàn TMĐT)

> **Giai đoạn:** Bàn giao đợt 2

| Nền tảng | Mô tả |
|----------|-------|
| Shopee | Khi có phát sinh đơn hàng ở trên các nền tảng, cần liên kết để đồng bộ đơn hàng này về hệ thống CRM |
| TikTok | |
| Lazada | |
| Website | |

---

## 6. Quản lý Sản phẩm

> **Giai đoạn:** Bàn giao đợt 1

### 6.1. Danh sách Sản phẩm

**Hiển thị các cột thông tin:**
- Mã sản phẩm
- SKU
- Tên sản phẩm
- Trạng thái đang/ngừng kinh doanh
- Đơn vị tính
- Nhóm sản phẩm
- Thương hiệu
- Giá bán lẻ

**Tính năng:**
- Ẩn/hiện thông tin cột

**Search/Filter:**
- Theo mã sản phẩm, SKU, tên sản phẩm
- Lọc theo:
  - Nhóm sản phẩm
  - Tồn kho (dưới định mức tồn, vượt định mức tồn, còn hàng, hết hàng)
  - Thương hiệu
  - Đang/ngừng kinh doanh

### 6.2. Quản lý Danh mục Sản phẩm

- Danh sách danh mục sản phẩm
- Chi tiết danh mục sản phẩm
- Tạo/Cập nhật/Xóa danh mục sản phẩm

### 6.3. Tạo Sản phẩm

- Tạo một sản phẩm

### 6.4. Import Sản phẩm

**Thông tin import:**
- Mã hàng
- Mã vạch
- Tên sản phẩm
- Nhóm sản phẩm (chọn hoặc tạo mới)
- Thương hiệu (chọn hoặc tạo mới)
- Giá bán
- Trọng lượng
- Tích điểm
- Thêm thuộc tính
- Đơn vị tính
- Thuộc tính thêm (chiều cao, chiều dài, chiều rộng, chất liệu)
- Mô tả

**Phương thức:** File excel

### 6.5. Export Sản phẩm

> **Giai đoạn:** Bàn giao đợt 1
>
> ⭐ *Mới thêm từ PHASE_1_FEATURES.xlsx*

| Chức năng | Mô tả |
|-----------|-------|
| Export Sản phẩm | File excel |

### 6.6. Xem chi tiết Sản phẩm

**Bảo hành bảo trì:**
- Thông tin bảo hành
- Thời gian bảo hành 1 năm với tất cả sản phẩm (gậy golf, shaft)

---

## 7. Quản lý Bán hàng

> **Giai đoạn:** Bàn giao đợt 2

### 7.1. Quản lý Kế hoạch Bán hàng

- Danh sách kế hoạch bán hàng
- Chi tiết kế hoạch
- Tạo kế hoạch
- Cập nhật kế hoạch
- Xóa kế hoạch

### 7.2. Quản lý Chính sách Chiết khấu

- Danh sách chính sách
- Chi tiết chính sách
- Tạo chính sách
- Cập nhật chính sách
- Xóa chính sách

### 7.3. Quản lý Bán lẻ

- Quản lý hóa đơn
- Quản lý đổi trả
- Quản lý hàng hóa/tồn kho
- Quản lý nhập hàng
- Quản lý điều chuyển

### 7.4. Quản lý Hàng trả lại

- Danh sách hàng trả lại
- Chi tiết hàng trả lại
- Tạo yêu cầu trả lại
- Cập nhật thông tin trả lại
- Xóa yêu cầu trả lại (Danh sách Return)

### 7.5. Tính thưởng Doanh số

- Danh sách thưởng
- Chi tiết thưởng:
  - Tính thưởng doanh số theo rule
  - Gồm tối đa 3 bước (3 tác nhân) tham gia trong thưởng doanh số
- Tạo thưởng
- Cập nhật thưởng
- Xóa thưởng

### 7.6. Quản lý Voucher

- Danh sách voucher
- Chi tiết voucher
- Tạo voucher
- Xóa voucher

### 7.7. Danh sách Bảng giá

**Hiển thị các cột thông tin:**
- Tên bảng giá
- Trạng thái (còn/hết thời gian áp dụng)
- Chi nhánh áp dụng (thêm ngoài màn)
- Tags KH áp dụng (thêm ngoài màn)

**Tính năng:**
- Ẩn/hiện thông tin cột
- Cập nhật tags (Tạo thưởng, tính toán doanh số)
- Cập nhật chi nhánh (Cập nhật trạng thái hoặc số liệu)
- Search/Filter (Xóa/hủy thưởng)

### 7.8. Thêm mới Bảng giá

- Thêm 1 bảng giá
- Thêm nhiều bảng giá

### 7.9. Xem chi tiết Bảng giá

### 7.10. Cập nhật Bảng giá

- Thời gian áp dụng
- Chi nhánh áp dụng
- Tags KH áp dụng
- Chọn làm bảng giá mặc định

### 7.11. Xóa Bảng giá

- Thời gian áp dụng
- Chi nhánh áp dụng
- Tags KH áp dụng
- Chọn làm bảng giá mặc định

---

## 8. Quản lý Kho

> **Giai đoạn:** Bàn giao đợt 2

### 8.1. Danh sách Kho

**Hiển thị các cột thông tin**

**Search/Filter:**
- Tìm kiếm theo tên

### 8.2. Tạo Kho

**Thông tin:**
- Tên kho
- Mã kho
- Địa chỉ
- NV phụ trách (có thể chọn nhiều)

### 8.3. Xem chi tiết Kho

**Tồn kho bao gồm các cột:**
- Mã SP
- SKU
- Tên SP
- Tồn kho
- Định mức tồn MIN
- Định mức tồn MAX

---

## 9. Quản lý Giao vận

> **Giai đoạn:** Bàn giao đợt 2

### 9.1. Danh sách Đơn giao vận

**Hiển thị các cột thông tin**

**Filter:**
- Lọc theo: Trạng thái đơn giao vận

### 9.2. Liên kết với đơn vị Viettel Post

**Tính năng:**
- Cho phép tạo đơn giao vận từ hệ thống CRM sang Viettel Post
- Đồng bộ mã giao vận, dịch vụ giao vận, giá vận chuyển, trạng thái giao vận với Viettel Post

**Lưu ý:**
- Đơn ở trạng thái đổi/trả thì cập nhật lại tồn kho

---

## 10. Quản lý Chi nhánh

> **Giai đoạn:** Bàn giao đợt 1

### 10.1. Danh sách Chi nhánh

- Hiển thị các cột thông tin
- Search/Filter

### 10.2. Tạo Chi nhánh

- Tạo mới chi nhánh/đại lý
- Thông tin: Tên, địa chỉ, số điện thoại, email
- Gán kho hàng cho chi nhánh

### 10.3. Xem chi tiết Chi nhánh

- Hiển thị thông tin cơ bản: Tên, địa chỉ, số điện thoại, email
- Thông tin kho hàng liên kết
- Danh sách nhân viên thuộc chi nhánh

### 10.4. Cập nhật Chi nhánh

### 10.5. Xóa Chi nhánh

---

## 11. Quản lý Nhân viên

> **Giai đoạn:** Bàn giao đợt 1

### 11.1. Danh sách Nhân viên

- Hiển thị các cột thông tin
- Search/Filter

### 11.2. Tạo Nhân viên

- Tạo một nhân viên
- Tạo nhiều nhân viên

### 11.3. Xem chi tiết Nhân viên

### 11.4. Cập nhật Nhân viên

### 11.5. Xóa Nhân viên

### 11.6. Import Nhân viên

> **Giai đoạn:** Bàn giao đợt 1
>
> ⭐ *Mới thêm từ PHASE_1_FEATURES.xlsx*

| Chức năng | Mô tả |
|-----------|-------|
| Import Nhân viên | File excel |

### 11.7. Export Nhân viên

> **Giai đoạn:** Bàn giao đợt 1
>
> ⭐ *Mới thêm từ PHASE_1_FEATURES.xlsx*

| Chức năng | Mô tả |
|-----------|-------|
| Export Nhân viên | File excel |

---

## 12. Role & Permission

> **Giai đoạn:** Bàn giao đợt 3

### 12.1. Danh sách Role

### 12.2. Tạo Role

### 12.3. Cập nhật Role

### 12.4. Xóa Role

---

## 13. Cài đặt

> **Giai đoạn:** Bàn giao đợt 1

### 13.1. Cài đặt Khách hàng

| Chức năng | Mô tả |
|-----------|-------|
| Phân công Lead | Phân công Lead thủ công cho NV theo chi nhánh |
| Quản lý tags khách hàng | |
| Quản lý trạng thái cơ hội | |

### 13.2. Danh sách Chức vụ

**Tính năng:**
- Danh sách các chức vụ có trong công ty
- Phân quyền cho từng chức vụ

**CRUD:**
- Thêm chức vụ mới
- Sửa chức vụ
- Xóa chức vụ

### 13.3. Danh sách Nhóm Khách hàng

**Tính năng:**
- Nhóm KH theo loại, vùng miền, đặc điểm chung

**CRUD:**
- Thêm nhóm khách hàng mới
- Sửa nhóm khách hàng
- Xóa nhóm khách hàng

### 13.4. Danh sách Trạng thái Đơn hàng

**Trạng thái cài sẵn:**
- Xác nhận đơn
- Đang xử lý
- Hoàn thành
- Hủy

> ⚠️ **Cần clarify:** Có cho phép tùy chỉnh trạng thái không?

### 13.5. Danh sách Hành động của Nhân viên

**Hành động cài sẵn:**
- Gọi điện
- Nhắn tin
- Gửi email
- Chat Facebook
- Chat Zalo

> ⚠️ **Cần clarify:** Có cho phép tùy chỉnh hành động không?

---

## 14. Báo cáo

> **Giai đoạn:** Bàn giao đợt 3

### 14.1. Báo cáo Doanh số

- Theo thời gian
- Theo chi nhánh
- Theo tags khách hàng
- Theo nguồn khách hàng
- Theo đơn sỉ/lẻ
- Theo nguồn khách hàng
- Theo sản phẩm (top 10 bán chạy)

### 14.2. Báo cáo Đơn hàng

**Tổng đơn:**
- Tổng đơn hàng theo thời gian, theo tags khách hàng, theo nguồn khách hàng, theo nguồn đơn hàng

**Fitting:**
- Doanh thu phát sinh từ fitting
- Tổng số buổi fitting trong tháng
- Số lượng khách đến thực hiện fitting
- Báo cáo linh kiện sử dụng trong fitting
- Báo cáo nhân viên thực hiện (doanh thu, tỉ lệ tư vấn thành công)

**Coaching:**
- Doanh thu từ coaching (doanh thu đào tạo)
- Doanh thu phát sinh sau coaching (Doanh thu sản phẩm)
- Số lượng học viên tham gia coaching
- Số lượng HLV tham gia coaching và doanh số theo từng HLV

**Cửa hàng vật lý/Đại lý:**
- Doanh thu tại cửa hàng vật lý/đại lý
- Doanh thu tại cửa hàng vật lý/đại lý theo sản phẩm
- Doanh thu tại cửa hàng vật lý/đại lý theo dòng sản phẩm
- Doanh thu tại cửa hàng vật lý/đại lý theo tuần/tháng/năm

**Trạng thái:**
- Đơn hàng thành công
- Đơn hàng không thành công (Đơn có trạng thái giao vận là trả, hoàn)

### 14.3. Báo cáo Khách hàng

- Báo cáo về số lead theo thời gian, theo nguồn khách hàng
- Top khách hàng doanh thu cao
- Báo cáo khách sỉ mới, khách lẻ mới
- Báo cáo mức độ hài lòng (từ khảo sát)

### 14.4. Báo cáo Nhân viên

- Nhân viên có tỉ lệ chốt đơn cao
- Số đơn xử lý
- Doanh thu theo nhân viên
- Tỷ lệ hiệu suất

### 14.5. Báo cáo Kho

- Báo cáo tồn kho theo kho
- Báo cáo giá trị tồn kho của từng kho
- Thống kê các sản phẩm đang dưới và gần định mức tồn kho cùng mức tồn kho hiện tại
  - Định nghĩa: sản phẩm đang gần định mức tồn kho là xếp theo sản phẩm có mức tồn kho gần với mức MIN trong định mức tồn kho nhất

---

## 15. Hệ thống Report Website

> **Giai đoạn:** Bàn giao đợt 3

### 15.1. Ghi nhận lại lượt truy cập vào web

- Số lượng lượt truy cập website theo tháng/tuần/ngày/giờ
- Số lượng đơn hàng mới từ nguồn website
- Số lượng khách hàng mới từ nguồn website
- Tỉ lệ chuyển đổi ghi nhận theo thời gian
- Thời gian trung bình người dùng ở lại với website

### 15.2. Bản đồ nhiệt (Heatmap)

- Thống kê theo bản đồ nhiệt người dùng cuối vào website tương tác/click vào đâu cho đến khi rời khỏi website
- Lọc phiên theo sự kiện:
  - Giỏ hàng bị từ bỏ
  - Thanh toán bị từ bỏ
  - Đơn hàng thành công

### 15.3. Phân tích Data

- PageView
- Scroll Depth
- Session Start
- User Engagement
- Purchase
- Add to Cart
- Begin Checkout
- Complete Purchase
- Subscribe
- Page Load Time
- Broken Link Click

### 15.4. Tối ưu

- Ghi lại các phiên mà không ảnh hưởng đến tốc độ load web, điểm của web

---

## 16. Quản lý Fitting

> **Định nghĩa:** Dịch vụ đo thông số kỹ thuật cá nhân để tư vấn và customize gậy golf phù hợp với từng khách hàng
>
> ⭐ **Lưu ý:** Fitting là **module quản lý riêng biệt** với lifecycle khác đơn hàng thông thường.
> Fitting Order có thể phát sinh Sales Order (grip, shaft, gậy custom...) hoặc không.

### 16.1. Đợt 1: Core Fitting Management

> **Giai đoạn:** Bàn giao đợt 1

#### 16.1.1. Danh sách đơn Fitting

**Hiển thị các cột thông tin:**
- Mã đơn Fitting (tự động: FIT-YYYYMMDD-XXX)
- Khách hàng
- SĐT
- Lịch hẹn
- Trạng thái
- NV Fitting
- Chi nhánh
- Nguồn (Website/Cửa hàng/Điện thoại)
- Có đơn SP (Yes/No)

**Tính năng:**
- Ẩn/hiện thông tin cột
- Calendar view lịch hẹn

**Search/Filter:**
- Tìm kiếm theo: tên, SĐT
- Filter theo:
  - Trạng thái
  - Chi nhánh
  - NV Fitting
  - Khoảng thời gian
  - Có đơn SP (Yes/No)

#### 16.1.2. Tạo đơn Fitting

**Nguồn đăng ký:**
- Website (tự động đẩy vào CRM)
- Tại cửa hàng
- Điện thoại

**Thông tin đơn Fitting:**
- Khách hàng (chọn hoặc tạo mới)
- Lịch hẹn (ngày + giờ)
- Chi nhánh thực hiện
- NV Fitting phụ trách
- Ghi chú

#### 16.1.3. Trạng thái đơn Fitting

| Trạng thái | Mô tả |
|------------|-------|
| Mới đăng ký | Khách đăng ký, chưa xác nhận lịch |
| Đã xác nhận | Sale đã xác nhận lịch hẹn với khách |
| Đang thực hiện | NV Fitting đang thực hiện đo |
| Hoàn thành | Đã hoàn thành fitting |
| Hủy | Khách hủy hoặc không đến |

#### 16.1.4. Nhập thông số kỹ thuật

**Thông tin kỹ thuật (từ Section 5.2.2):**
- Chiều cao, Cân nặng
- Kích thước size tay
- Cấp độ (người mới, người đã chơi)
- Tốc độ đầu gậy, Tốc độ bóng
- Hình swing, Đường bóng, Đường cao bóng
- Khoảng cách gậy sắt, Khoảng cách driver
- Tình trạng bộ gậy của khách
- Nhu cầu riêng của KH

**Đề xuất nâng cấp:**
- Ghi chú tư vấn từ NV Fitting

#### 16.1.5. Dịch vụ phát sinh

**Loại dịch vụ (ghi nhận, chưa tạo đơn):**
- Mua thêm grip
- Lắp shaft
- Đặt gậy theo thông số đặc biệt
- Mua combo fitting + gậy

#### 16.1.6. Phân công NV Fitting

- Phân công NV thực hiện Fitting
- Đổi NV phụ trách

---

### 16.2. Đợt 2: Tích hợp Order + Báo cáo

> **Giai đoạn:** Bàn giao đợt 2

#### 16.2.1. Tạo Sales Order từ Fitting

**Tính năng:**
- Button "Tạo đơn hàng" từ chi tiết đơn Fitting
- Pre-fill thông tin từ dịch vụ phát sinh
- Link đơn hàng với đơn Fitting
- Gắn vào hồ sơ khách hàng

#### 16.2.2. Tích hợp Website

**Tính năng:**
- API nhận đăng ký Fitting từ website
- Tự động tạo đơn Fitting mới
- Gửi thông báo cho Sale xác nhận

#### 16.2.3. Báo cáo Fitting

**Các loại báo cáo (từ Section 14.2):**
- Doanh thu phát sinh từ fitting
- Tổng số buổi fitting trong tháng
- Số lượng khách đến thực hiện fitting
- Báo cáo linh kiện sử dụng trong fitting
- Báo cáo nhân viên thực hiện (doanh thu, tỉ lệ tư vấn thành công)

#### 16.2.4. Dashboard Widgets

- Số buổi fitting tháng này
- Doanh thu từ fitting
- Tỉ lệ chuyển đổi (fitting → đơn hàng)
- Top NV Fitting

---

## 17. Quản lý Coaching

> **Định nghĩa:** Dịch vụ huấn luyện golf cho học viên với các gói học khác nhau
>
> ⭐ **Lưu ý:** Coaching là **module quản lý riêng biệt** với lifecycle khác đơn hàng thông thường.
> Coaching có thể phát sinh Sales Order (gói học, phụ kiện...) hoặc không.

### 17.1. Đợt 1: Core Coaching Management

> **Giai đoạn:** Bàn giao đợt 1

#### 17.1.1. Danh sách đơn Coaching

**Hiển thị các cột thông tin:**
- Mã đơn Coaching (tự động: COACH-YYYYMMDD-XXX)
- Học viên
- SĐT
- Gói học
- HLV phụ trách
- Trạng thái
- Số buổi đã học / Tổng buổi
- Sân tập
- Ngày bắt đầu
- Còn nợ

**Tính năng:**
- Ẩn/hiện thông tin cột
- Calendar view lịch học

**Search/Filter:**
- Tìm kiếm theo: tên, SĐT
- Filter theo:
  - Trạng thái
  - HLV
  - Gói học
  - Sân tập
  - Khoảng thời gian

#### 17.1.2. Tạo đơn Coaching

**Hồ sơ học viên:**
- Thông tin cá nhân
- Trình độ hiện tại
- Mục tiêu học
- Bài test đầu vào

**Thông tin khóa học:**
- Gói huấn luyện đăng ký (VD: 8 buổi cơ bản, Thi đấu nâng cao 12 buổi)
- HLV phụ trách
- Sân tập
- Lịch học
- Tổng học phí
- Ưu đãi nếu có

**Thông tin kỹ thuật:** (tương tự Fitting - từ Section 5.2.2)

#### 17.1.3. Trạng thái đơn Coaching

| Trạng thái | Code | Mô tả |
|------------|------|-------|
| Mới | `new` | Đơn coaching mới đăng ký, chưa test đầu vào |
| Đã test | `tested` | Đã làm bài test đánh giá trình độ |
| Đã tư vấn | `consulted` | Đã tư vấn gói học phù hợp |
| Đã thanh toán | `paid` | Đã đăng ký gói và thanh toán |
| Đang học | `in_progress` | Đang trong quá trình học |
| Tạm dừng | `paused` | Học viên xin nghỉ tạm thời |
| Hoàn thành | `completed` | Đã hoàn thành khóa học |
| Hủy | `cancelled` | Đơn bị hủy |

#### 17.1.4. Quản lý Gói huấn luyện (COACHING_PACKAGE)

**Thông tin gói:**
- Tên gói (VD: 8 buổi cơ bản, Thi đấu nâng cao 12 buổi)
- Loại gói (Cá nhân/Nhóm/Thi đấu)
- Số buổi
- Thời lượng/buổi (phút)
- Giá
- Mô tả

#### 17.1.5. Quản lý HLV (COACH)

**Thông tin HLV:**
- Liên kết với Employee
- Chứng chỉ
- Kinh nghiệm (năm)
- Chuyên môn
- Đánh giá (rating)

#### 17.1.6. Quản lý Sân tập (GOLF_COURSE)

**Thông tin sân:**
- Tên sân tập
- Địa chỉ
- Số lane
- SĐT liên hệ
- Đối tác hay của NM

#### 17.1.7. Bài test đầu vào (COACHING_TEST)

**Thông tin test:**
- Ngày test
- HLV thực hiện test
- Kết quả đánh giá trình độ
- Chi tiết bài test
- Đề xuất gói phù hợp

#### 17.1.8. Lịch học & Điểm danh (COACHING_SESSION)

**Thông tin buổi học:**
- Buổi thứ mấy
- Thời gian dự kiến
- Thời gian thực tế (bắt đầu/kết thúc)
- Trạng thái buổi: scheduled/completed/absent/cancelled
- Nội dung buổi học
- Ghi chú tiến trình
- Bài tập về nhà

**Tính năng điểm danh:**
- Có mặt → `completed_sessions += 1`
- Vắng có báo trước → Có thể học bù
- Vắng không báo → Theo chính sách

#### 17.1.9. Tiến độ học tập

**Thông tin:**
- Tổng quan kỹ năng (swing, putting, chipping...)
- Đánh giá định kỳ (đầu - giữa - cuối kỳ)
- Phân tích kỹ thuật
- Nhận xét chuyên môn

---

### 17.2. Đợt 2: Tích hợp Order + Báo cáo

> **Giai đoạn:** Bàn giao đợt 2

#### 17.2.1. Tạo Sales Order từ Coaching

**Tính năng:**
- Tạo đơn thanh toán học phí
- Tạo đơn mua phụ kiện phát sinh
- Link đơn hàng với đơn Coaching
- Gắn vào hồ sơ học viên
- Theo dõi công nợ

**Hình thức thanh toán:**
- Trọn gói (100%)
- Đặt cọc (X%)
- Theo buổi

#### 17.2.2. Thông báo & Nhắc lịch tự động

**Tính năng:**
- CRM gửi lịch học qua Zalo/Email
- Thông báo thay đổi giờ học
- Nhắc lịch thi đấu
- Nhắc học bù khi vắng mặt
- Thông báo hoàn thành khóa

#### 17.2.3. Báo cáo Coaching

**Các loại báo cáo (từ Section 14.2):**
- Doanh thu từ coaching (doanh thu đào tạo)
- Doanh thu phát sinh sau coaching (Doanh thu sản phẩm)
- Số lượng học viên tham gia coaching
- Số lượng HLV tham gia coaching và doanh số theo từng HLV

**KPI mở rộng:**
- Tỉ lệ hoàn thành khóa học
- Tỉ lệ đăng ký tiếp
- Điểm danh trung bình

#### 17.2.4. Dashboard Widgets

- Số học viên đang học
- Doanh thu coaching tháng này
- Doanh thu SP phát sinh
- Top HLV theo doanh số
- Tỉ lệ hoàn thành khóa học

---

## 18. Quản lý Thu cũ Đổi mới

> **Định nghĩa:** Chương trình cho phép khách hàng mang sản phẩm cũ (gậy golf) để đổi lấy sản phẩm mới, với việc tính toán giá trị chênh lệch
>
> ⭐ **Lưu ý:** Thu cũ Đổi mới là **module quản lý riêng biệt** với workflow khác đơn hàng thông thường.
> Trade-in Order có thể phát sinh thanh toán chênh lệch hoặc hoàn tiền cho khách.

### 18.1. Đợt 1: Core Trade-in Management

> **Giai đoạn:** Bàn giao đợt 1

#### 18.1.1. Danh sách đơn Thu cũ Đổi mới

**Hiển thị các cột thông tin:**
- Mã đơn Trade-in (tự động: TI-YYYYMMDD-XXX)
- Khách hàng
- SĐT
- SP cũ (tên + thương hiệu)
- SP mới (tên + thương hiệu)
- Giá thu SP cũ
- Giá SP mới
- Chênh lệch
- Trạng thái
- NV xử lý
- Chi nhánh
- Ngày tạo

**Tính năng:**
- Ẩn/hiện thông tin cột
- Cập nhật tags

**Search/Filter:**
- Tìm kiếm theo: tên KH, SĐT
- Filter theo:
  - Trạng thái
  - Chi nhánh
  - NV xử lý
  - Khoảng thời gian

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1 (Line 393)

#### 18.1.2. Tạo đơn Thu cũ Đổi mới

**Thông tin sản phẩm cũ (khách trả):**
- Chọn hoặc nhập tên SP cũ
- Thương hiệu
- Tình trạng (Mới/Tốt/Trung bình/Kém)
- Giá thu SP cũ
- Ghi chú tình trạng
- Hình ảnh (nếu có)

**Thông tin sản phẩm mới (khách nhận):**
- Chọn từ danh sách sản phẩm
- Giá bán

**Tính năng:**
- Gắn 2 dòng sản phẩm (cũ + mới) trong cùng một giao dịch
- Áp dụng Voucher (nếu có)
- Tính giá trị chênh lệch theo công thức:
  - **Số tiền KH thanh toán = Giá SP mới - Giá thu SP cũ - Voucher (nếu có)**

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.4 (Line 489-500)

#### 18.1.3. Trạng thái đơn Trade-in

| Trạng thái | Mô tả |
|------------|-------|
| Mới tạo | Đơn vừa được tạo, chờ kiểm tra SP cũ |
| Đang kiểm tra | NV đang kiểm tra/định giá SP cũ |
| Đã định giá | SP cũ đã được định giá, chờ KH xác nhận |
| Khách xác nhận | KH đồng ý với giá trị chênh lệch |
| Đang xử lý | Đang chuẩn bị SP mới cho KH |
| Hoàn thành | Giao dịch hoàn tất |
| Đã hủy | Đơn bị hủy |

> ⚠️ **Lưu ý:** Trạng thái được đề xuất dựa trên quy trình nghiệp vụ. Cần xác nhận với khách hàng.

#### 18.1.4. Xem chi tiết đơn Trade-in

- Thông tin khách hàng
- Thông tin SP cũ (tên, thương hiệu, tình trạng, giá thu, ảnh)
- Thông tin SP mới (tên, SKU, giá bán)
- Chi tiết thanh toán (giá mới - giá cũ - voucher = chênh lệch)
- Lịch sử trạng thái

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.4 (Line 540)

#### 18.1.5. Cập nhật đơn Trade-in

- Cập nhật thông tin SP cũ
- Cập nhật giá thu (cần Manager duyệt)
- Cập nhật SP mới
- Cập nhật Voucher

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.5 (Line 553)

---

### 18.2. Đợt 2: Tích hợp Kho + Báo cáo

> **Giai đoạn:** Bàn giao đợt 2

#### 18.2.1. Quy trình kiểm tra & định giá SP cũ

**Tính năng:**
- Checklist kiểm tra tình trạng SP cũ
- Ghi nhận kết quả kiểm tra với ảnh
- Đề xuất giá thu
- Manager duyệt giá thu

> ⚠️ **Cần clarify:** Tiêu chí định giá SP cũ cụ thể?

#### 18.2.2. Tích hợp Kho

**Tính năng:**
- Khi hoàn thành giao dịch:
  - Nhập SP cũ vào kho "Hàng thu cũ"
  - Xuất SP mới từ kho cho khách
- Cập nhật tồn kho tự động

#### 18.2.3. Báo cáo Trade-in

**Các loại báo cáo:**
- Tổng số đơn trade-in theo thời gian
- Doanh thu từ trade-in (tổng chênh lệch thu được)
- Giá trị SP cũ đã thu
- Báo cáo theo chi nhánh
- Báo cáo theo NV xử lý

#### 18.2.4. Dashboard Widgets

- Số đơn trade-in tháng này
- Tổng giá trị chênh lệch thu được
- Số SP cũ đã thu
- Top SP được trade-in nhiều nhất

---

### 18.3. Các điểm cần Clarify với khách hàng

| # | Câu hỏi | Lý do |
|---|---------|-------|
| 1 | Tiêu chí kiểm tra SP cũ (checklist)? | Spec không chi tiết |
| 2 | Quy tắc định giá SP cũ? | Cần biết cách xác định giá thu |
| 3 | Ai có quyền duyệt giá thu? | Không có trong spec |
| 4 | SP cũ sau khi thu nhập kho nào? | Cần xác định kho riêng |
| 5 | Trường hợp giá cũ > giá mới? | KH có được nhận tiền chênh lệch? |
| 6 | Có giới hạn thời gian SP cũ? | VD: chỉ thu SP mua trong 2 năm |
| 7 | Có yêu cầu hóa đơn mua SP cũ? | Xác minh nguồn gốc |

---

**© 2025 DCNET Corporation - Powered by DCNET Cloud**

**Nguồn tài liệu:** PHỤ LỤC SỐ 01 - Hợp đồng số .01/HĐDV/DCNET-NMS
