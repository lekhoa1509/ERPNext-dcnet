# Đầu mối Dự án - DCNET Flow x Nhật Minh Sport

> **Mục đích:** Xác định đầu mối liên hệ giữa 2 bên để đảm bảo dự án được triển khai suôn sẻ
>
> **Lưu ý:** Các module đánh dấu 🔴 CRITICAL - nếu không có đầu mối sẽ BLOCK dự án

---

## 1. Đầu mối DCNET

| Vị trí | Tên | Vai trò | Nhiệm vụ | Liên hệ |
|--------|-----|---------|----------|---------|
| 📍 **Hà Nội** | Thịnh | Customer Contact | Tiếp nhận yêu cầu, họp với khách, demo sản phẩm, thu thập feedback | |
| 📍 **Hồ Chí Minh** | Đức | Tech Lead | Lead team dev, review kỹ thuật, quyết định giải pháp, quản lý tiến độ | |

---

## 2. Đầu mối Nhật Minh Sport (Cần xác nhận)

### 2.1. Tổng quan

| # | Vai trò | Mức độ | Tên | SĐT/Zalo | Email | Ghi chú |
|---|---------|--------|-----|----------|-------|---------|
| 1 | 🔴 Vận hành - Nghiệp vụ | CRITICAL | | | | Quyết định yêu cầu |
| 2 | 🔴 Bravo ERP | CRITICAL | Dung | | | Đã có thông tin |
| 3 | 🟠 Tích hợp bên ngoài | HIGH | | | | Cần giấy tờ DN |
| 4 | 🟡 Fitting/Coaching | MEDIUM | | | | Nghiệp vụ golf |

### 2.2. Chi tiết từng vai trò

#### 🔴 Vai trò 1: Vận hành - Nghiệp vụ (CRITICAL)

> **Nếu không có:** Không xác nhận được yêu cầu, block toàn bộ dự án

**Trách nhiệm:**
- Xác nhận/quyết định các yêu cầu nghiệp vụ
- Cung cấp thông tin quy trình bán hàng hiện tại
- Tham gia review và UAT testing
- Feedback sau mỗi sprint demo
- Phối hợp training nhân viên

**Phạm vi liên quan:**
- Quy trình bán hàng (lẻ/sỉ)
- Quy trình quản lý khách hàng
- Quy trình xử lý đơn hàng
- Chính sách chiết khấu, thưởng
- Rule chia lead, chăm sóc KH

| Thông tin | Giá trị |
|-----------|---------|
| Họ tên | |
| Chức vụ | |
| SĐT | |
| Zalo | |
| Email | |

---

#### 🔴 Vai trò 2: Bravo ERP (CRITICAL)

> **Nếu không có:** Không sync được Sản phẩm, Tồn kho, Chi nhánh

**Trách nhiệm:**
- Cung cấp thông tin API/DB Bravo (nếu có)
- Hướng dẫn cấu trúc dữ liệu Bravo
- Export file Excel mẫu từ Bravo
- Hỗ trợ test sync dữ liệu
- Liên hệ Bravo vendor nếu cần

**Phạm vi liên quan:**
- Sản phẩm (mã, tên, giá, thuộc tính)
- Tồn kho (số lượng, kho, định mức)
- Chi nhánh/Đại lý
- Khách hàng (import ban đầu)
- Đơn hàng (import ban đầu)

| Thông tin | Giá trị |
|-----------|---------|
| Họ tên | Dung |
| Chức vụ | |
| SĐT | |
| Zalo | |
| Email | |

---

#### 🟠 Vai trò 3: Tích hợp bên ngoài (HIGH)

> **Nếu không có:** Không tích hợp được Zalo, Sàn TMĐT, Vận chuyển

**Trách nhiệm:**
- Cung cấp tài khoản/credentials các nền tảng
- Ký hợp đồng với các đối tác (nếu cần)
- Đăng ký API/Developer account
- Xác thực doanh nghiệp trên các nền tảng

**Phạm vi liên quan:**
- Zalo OA (gửi tin nhắn, CSKH)
- Sàn TMĐT: Shopee, TikTok Shop, Lazada
- Vận chuyển: Viettel Post
- Thanh toán: VNPay, MoMo, ZaloPay (nếu có)
- Facebook/Messenger

| Thông tin | Giá trị |
|-----------|---------|
| Họ tên | |
| Chức vụ | |
| SĐT | |
| Zalo | |
| Email | |

---

#### 🟡 Vai trò 4: Fitting/Coaching (MEDIUM)

> **Nếu không có:** Không build đúng nghiệp vụ đặc thù golf

**Trách nhiệm:**
- Cung cấp quy trình Fitting hiện tại
- Cung cấp quy trình Coaching/đào tạo
- Xác nhận các thông số kỹ thuật golf
- Review module Fitting/Coaching
- Liên hệ HLV nếu cần thông tin

**Phạm vi liên quan:**
- Đơn hàng Fitting (thông số kỹ thuật)
- Đơn hàng Coaching (gói học, lịch học)
- Bài test đầu vào (nếu có)
- Đánh giá tiến độ học viên

| Thông tin | Giá trị |
|-----------|---------|
| Họ tên | |
| Chức vụ | |
| SĐT | |
| Zalo | |
| Email | |

---

## 3. Giấy tờ / Tài khoản cần từ Nhật Minh

### 3.1. Zalo OA / Zalo API

| # | Yêu cầu | Trạng thái | Người cung cấp | Ghi chú |
|---|---------|------------|----------------|---------|
| 1 | Tài khoản Zalo OA (đã xác thực DN) | ☐ Chưa có | | |
| 2 | Giấy phép kinh doanh | ☐ Chưa có | | Để đăng ký API |
| 3 | Quyền admin Zalo OA | ☐ Chưa có | | |
| 4 | Đăng ký Zalo Developer | ☐ Chưa có | | developers.zalo.me |

### 3.2. Sàn TMĐT

| # | Nền tảng | Yêu cầu | Trạng thái | Ghi chú |
|---|----------|---------|------------|---------|
| 1 | Shopee | Seller Center + API key | ☐ Chưa có | |
| 2 | TikTok Shop | Seller account + API | ☐ Chưa có | |
| 3 | Lazada | Seller Center + App key | ☐ Chưa có | |

### 3.3. Vận chuyển

| # | Đơn vị | Yêu cầu | Trạng thái | Ghi chú |
|---|--------|---------|------------|---------|
| 1 | Viettel Post | Hợp đồng + API credentials | ☐ Chưa có | |
| 2 | GHTK | Business account + API | ☐ Chưa có | Nếu cần |
| 3 | GHN | Business account + API | ☐ Chưa có | Nếu cần |

### 3.4. Thanh toán (nếu cần)

| # | Cổng | Yêu cầu | Trạng thái | Ghi chú |
|---|------|---------|------------|---------|
| 1 | VNPay | Merchant account + credentials | ☐ Chưa có | |
| 2 | MoMo | Business account + API | ☐ Chưa có | |
| 3 | ZaloPay | Merchant account | ☐ Chưa có | |

### 3.5. Facebook/Messenger

| # | Yêu cầu | Trạng thái | Ghi chú |
|---|---------|------------|---------|
| 1 | Facebook Page (admin access) | ☐ Chưa có | |
| 2 | Facebook Developer account | ☐ Chưa có | |

---

## 4. Ma trận trách nhiệm (RACI)

| Module | DCNET Thịnh | DCNET Đức | NM Vận hành | NM Bravo | NM Tích hợp | NM Golf |
|--------|-------------|-----------|-------------|----------|-------------|---------|
| Yêu cầu nghiệp vụ | I | C | **A/R** | I | I | C |
| Bravo sync | I | **A** | I | **R** | I | - |
| Zalo OA | I | **A** | C | - | **R** | - |
| Sàn TMĐT | I | **A** | C | - | **R** | - |
| Vận chuyển | I | **A** | C | - | **R** | - |
| Fitting/Coaching | I | **A** | C | - | - | **R** |
| UAT Testing | **R** | C | **A** | I | I | I |
| Training | **R** | C | **A** | I | I | I |

> **R** = Responsible (Thực hiện) | **A** = Accountable (Chịu trách nhiệm) | **C** = Consulted (Tham vấn) | **I** = Informed (Được thông báo)

---

## 5. Kênh liên lạc

| Kênh | Mục đích | Thành viên |
|------|----------|------------|
| **Zalo Group chính** | Trao đổi hàng ngày, thông báo | Tất cả đầu mối |
| **Email** | Tài liệu chính thức, confirm | PM 2 bên |
| **Họp online** | Sprint planning, demo, review | Theo lịch |
| **Họp trực tiếp** | Kickoff, milestone quan trọng | Khi cần |

---

## 6. Lịch họp định kỳ (Đề xuất)

| Loại họp | Tần suất | Thời gian | Thành phần | Mục đích |
|----------|----------|-----------|------------|----------|
| Sprint Planning | 2 tuần/lần | Thứ 2, 9:00 | DCNET + NM Vận hành | Lên kế hoạch sprint |
| Sprint Demo | 2 tuần/lần | Thứ 6, 14:00 | Tất cả | Demo kết quả |
| Sync Bravo | Khi cần | Linh hoạt | DCNET Đức + NM Bravo | Giải quyết vấn đề sync |
| Standup | Hàng ngày (nội bộ) | 9:30 | DCNET team | Cập nhật tiến độ |

---

*Cập nhật: 2025-12-08*
