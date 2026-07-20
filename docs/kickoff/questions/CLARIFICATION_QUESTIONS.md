# Câu hỏi cần làm rõ với Nhật Minh

> **Nguồn:** Notes từ team DCNET sau khi review PHỤ LỤC
>
> **Mục đích:** Tổng hợp các điểm chưa rõ, cần xác nhận trước khi triển khai

---

## Tổng quan

### Tổng hợp tất cả câu hỏi

| Module | Số câu hỏi | File | Ghi chú |
|--------|------------|------|---------|
| **Chung (GĐ 1)** | 50+ câu | File này | Nghiệp vụ core |
| **Chung (GĐ 2)** | 10+ câu | File này | Advanced features |
| **Fitting** | 17 câu | [Chi tiết →](./FITTING_QUESTIONS.md) | Module Fitting Golf |
| **Coaching** | 27 câu | [Chi tiết →](./COACHING_QUESTIONS.md) | Module Coaching Golf |
| **Vận chuyển** | 35 câu | [Chi tiết →](./SHIPPING_QUESTIONS.md) | Viettel Post, COD |
| **Bravo Integration** | 30 câu | [Chi tiết →](./BRAVO_QUESTIONS.md) | Sync ERP |

### Độ ưu tiên

| Mức | Ký hiệu | Ý nghĩa |
|-----|---------|---------|
| 🔴 | CRITICAL | Block development nếu không có |
| 🟠 | HIGH | Ảnh hưởng thiết kế, cần sớm |
| 🟡 | MEDIUM | Có thể làm rõ trong quá trình dev |

---

## PHẦN A: GĐ 1 - CORE FEATURES

---

### 1. Đại lý / Chi nhánh 🔴

> **Lưu ý:** Đây là khái niệm nền tảng, ảnh hưởng nhiều module khác

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 1.1 | **Định nghĩa "Chi nhánh"**: Là cửa hàng của NM hay đại lý bên ngoài? | | |
| 1.2 | Hiện có bao nhiêu chi nhánh/đại lý? | | |
| 1.3 | Chi nhánh có **kho riêng** không? | Hay dùng chung kho? | |
| 1.4 | Chi nhánh có **bảng giá riêng** không? | | |
| 1.5 | Cần **phân quyền theo chi nhánh** không? | NV chỉ xem data chi nhánh mình | |
| 1.6 | **Chi nhánh của KH** có phải để xác định đơn hàng phát sinh từ đâu? | Hay chỉ để phân loại? | |

---

### 2. Đơn hàng - Phân loại & Flow

#### 2.1. Đơn Sỉ vs Lẻ 🔴

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 2.1.1 | Khác biệt chính giữa đơn Sỉ và Lẻ? | Giá? Số lượng tối thiểu? Thanh toán? | |
| 2.1.2 | Đơn Sỉ có **bảng giá riêng**? | Theo số lượng hay theo KH? | |
| 2.1.3 | Đơn Sỉ có **công nợ**? | Cho nợ bao nhiêu ngày? | |
| 2.1.4 | **Flow xử lý** đơn Sỉ khác Lẻ như thế nào? | Duyệt? Xuất kho? | |

#### 2.2. Đơn Fitting 🟠

> **Chi tiết đầy đủ:** [FITTING_QUESTIONS.md](./FITTING_QUESTIONS.md)

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 2.2.1 | Sau khi Fitting, có **tư vấn chọn sản phẩm** không? | Gợi ý SP phù hợp với thông số | |
| 2.2.2 | Nếu có, cần **map Fitting với Product ID** không? | Để tracking KH fitting → mua SP | |
| 2.2.3 | Có template gợi ý SP theo thông số không? | VD: swing speed 85mph → shaft X | |

#### 2.3. Đơn Coaching 🟠

> **Chi tiết đầy đủ:** [COACHING_QUESTIONS.md](./COACHING_QUESTIONS.md)

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 2.3.1 | **Các gói huấn luyện** có tạo sẵn trong CRM không? | Hay nhập tay mỗi đơn? | |
| 2.3.2 | Nếu có, cần những thông tin gì cho gói? | Số buổi, giá, thời hạn, HLV? | |
| 2.3.3 | Một gói có thể chia nhiều HLV không? | | |

#### 2.4. Thu cũ Đổi mới 🟠

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 2.4.1 | **Hàng thu về** xử lý như thế nào? | ☐ Nhập kho ☐ Thanh lý ☐ Khác | |
| 2.4.2 | Hàng thu về nhập vào **kho nào**? | Kho chính? Kho riêng? | |
| 2.4.3 | Hàng cũ có **mã SKU riêng** không? | Hay dùng chung mã SP? | |
| 2.4.4 | Có **định giá hàng cũ** không? | Ai định giá? Công thức? | |
| 2.4.5 | Quy trình **định giá hàng cũ**? | Ai duyệt giá? | |
| 2.4.6 | Hàng cũ có **bán lại** không? | Ở đâu? Kênh nào? | |
| 2.4.7 | Cần **tracking nguồn gốc** hàng cũ? | Từ KH nào, ngày nào | |

#### 2.5. Tạo đơn - Trường hợp đặc biệt 🟠

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 2.5.1 | Nếu tạo đơn mà **không đủ tồn kho**, flow như thế nào? | ☐ Block ☐ Cho tạo (backorder) ☐ Cảnh báo | |
| 2.5.2 | Có cho phép **đặt hàng trước** (pre-order)? | | |

---

### 3. Doanh số & Báo cáo 🟠

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 3.1 | **Doanh số Sỉ/Lẻ** cần tách riêng tab để đếm? | ☐ Có ☐ Không | |
| 3.2 | **Doanh số theo nguồn KH** - nguồn KH định nghĩa thế nào? | Facebook, Zalo, Walk-in...? | |
| 3.3 | **Doanh số theo nguồn đơn hàng** - các nguồn cần track? | ☐ TikTok ☐ Lazada ☐ Shopee ☐ B2B ☐ Cửa hàng | |
| 3.4 | Có cần báo cáo **so sánh giữa các nguồn** không? | | |

---

### 4. Lead Management 🟠

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 4.1 | **Tổng số tương tác** của Lead dựa vào gì? | ☐ Số cuộc gọi ☐ Số tin nhắn ☐ Số lần gặp ☐ Tất cả | |
| 4.2 | **Bảng giá cho Lead** kiểu nào? | ☐ Chung ☐ Theo nguồn ☐ Theo loại SP | |
| 4.3 | **Nguồn Lead** có gắn tag không? | VD: #facebook #zalo #event | |
| 4.4 | Danh sách **nguồn Lead** cần tracking? | Liệt kê cụ thể | |

#### Chi tiết Lead

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 4.5 | Vào chi tiết Lead có cần xem **log bình luận/ghi chú** không? | Timeline hoạt động | |
| 4.6 | Ai được quyền thêm bình luận? | ☐ NV phụ trách ☐ Tất cả | |

---

### 5. Quản lý Khách hàng 🔴

#### 5.1. Thiết lập chung

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 5.1.1 | **Bảng giá KH**: Chung hay riêng theo từng loại KH? | VIP, Thường, Đại lý? | |
| 5.1.2 | **Lịch chăm sóc định kỳ**: Cụ thể là gì? | ☐ Nhắc sinh nhật ☐ Nhắc sau X ngày mua ☐ Khác | |
| 5.1.3 | Có bao nhiêu **loại lịch chăm sóc**? | | |

#### 5.2. Danh sách Khách hàng - Các trường dữ liệu

| # | Trường | Câu hỏi | Trả lời |
|---|--------|---------|---------|
| 5.2.1 | **Liên hệ lần cuối** | Tự động cập nhật hay nhập text thủ công? | |
| 5.2.2 | **Nguồn Lead** | Từ Lead chuyển qua tự động hay tự thêm tay? | |
| 5.2.3 | **Chi nhánh** | Định nghĩa: NV phụ trách? Nơi mua? Nơi đăng ký? | |
| 5.2.4 | **Số điểm hiện tại** | Xin **công thức tính điểm**? | |
| 5.2.5 | **Doanh số phát sinh** | = Tổng tiền tất cả đơn hàng của KH? | |
| 5.2.6 | **Công nợ** | Định nghĩa: Tiền KH đang nợ NM? Hay ngược lại? | |

---

### 6. Quản lý Nhân viên 🟠

| # | Trường | Câu hỏi | Trả lời |
|---|--------|---------|---------|
| 6.1 | **Hiệu suất** | Công thức tính? VD: Số đơn/tháng? Tỷ lệ chốt? | |
| 6.2 | **Doanh thu** | = Tổng đơn hàng NV quản lý? Hay chỉ NV tạo đơn? | |
| 6.3 | **Thưởng** | ☐ Nhập tay ☐ Tính theo công thức | |
| 6.4 | Nếu có công thức thưởng, xin chi tiết? | % doanh số? Theo KPI? | |

---

### 7. Quản lý Sản phẩm 🔴

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 7.1 | **Nguồn sản phẩm**: Không thêm từ CRM, vậy kéo từ đâu? | ☐ Website bán hàng ☐ Bravo ☐ Cả hai | |
| 7.2 | Nếu từ Bravo, có cần **đồng bộ 2 chiều** không? | CRM → Bravo? | |

> **Chi tiết Bravo Integration:** [BRAVO_QUESTIONS.md](./BRAVO_QUESTIONS.md)

---

### 8. Thanh toán 🟠

> **Yêu cầu từ NM:** Tiền mặt / Chuyển khoản / COD (KHÔNG cần MoMo, ZaloPay, VNPay)

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 8.1 | **Chuyển khoản**: Check thủ công hay tự động? | Tự động cần tích hợp ngân hàng (SePay ~200-500đ/GD) | |
| 8.2 | Nếu tự động, **ngân hàng nào**? | | |
| 8.3 | Có cần **QR Code VietQR** để khách quét CK? | | |

#### COD & Giao hàng

> **Chi tiết đầy đủ:** [SHIPPING_QUESTIONS.md](./SHIPPING_QUESTIONS.md)

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 8.4 | **COD**: NM có đội giao hàng riêng không? | ☐ Có ☐ Không (qua ĐVVC) | |
| 8.5 | Nếu qua ĐVVC, đơn vị nào? | ☐ Viettel Post ☐ GHTK ☐ GHN | |

---

### 9. Tích hợp Sàn TMĐT 🟡

| # | Câu hỏi | Lựa chọn/Ghi chú | Trả lời |
|---|---------|------------------|---------|
| 9.1 | Hiện NM đang bán trên những sàn nào? | ☐ Shopee ☐ TikTok ☐ Lazada ☐ Khác | |
| 9.2 | Đã có tài khoản **Seller Center** chưa? | ☐ Có ☐ Chưa | |
| 9.3 | Muốn **sync những gì** từ sàn? | ☐ Đơn hàng ☐ Sản phẩm ☐ Tồn kho ☐ Tất cả | |

---

## PHẦN B: GĐ 2 - ADVANCED FEATURES

---

### 10. Kế hoạch & Chính sách 🟡

| # | Module | Câu hỏi | Trả lời |
|---|--------|---------|---------|
| 10.1 | **Kế hoạch bán hàng** | Cấu trúc kế hoạch? Theo tháng/quý? Theo NV/team? | |
| 10.2 | **Chính sách chiết khấu** | Bao nhiêu loại? Theo KH? Theo SP? Theo số lượng? | |
| 10.3 | **Chính sách thưởng** | Cho ai? NV? Đại lý? Công thức? | |
| 10.4 | **Hàng trả lại** | Flow xử lý? Nhập lại kho? Hoàn tiền? | |

---

### 11. Kênh giao tiếp & Chăm sóc KH 🟡

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 11.1 | **Lịch chăm sóc KH** thông báo qua bao nhiêu kênh? | ☐ SMS ☐ Zalo ☐ Email ☐ App notification | |
| 11.2 | Kênh nào là **chính**? | | |

#### 11.3. Tích hợp kênh giao tiếp - 2 hướng tiếp cận:

| Hướng | Mô tả | Ưu điểm | Nhược điểm |
|-------|-------|---------|------------|
| **A. Hub thông báo** | CRM gửi tin nhắn 1 chiều ra Zalo/SMS | Đơn giản, nhanh, rẻ | Không nhận được phản hồi |
| **B. Chat trong CRM** | 2 chiều: KH nhắn → CRM → NV trả lời | Quản lý tập trung, xem lịch sử | Phức tạp, cần Zalo OA API |

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.4 | NM muốn hướng nào? | ☐ A. Hub thông báo ☐ B. Chat trong CRM ☐ Cả hai |
| 11.5 | Nếu chọn B, đã có **Zalo OA** chưa? | ☐ Có ☐ Chưa |

---

## PHẦN C: TÓM TẮT THEO ĐỘ ƯU TIÊN

### 🔴 CRITICAL - Cần trả lời ngay (Block development)

| # | Chủ đề | Câu hỏi chính | Mục |
|---|--------|---------------|-----|
| 1 | Đại lý/Chi nhánh | Định nghĩa? Có kho riêng? Phân quyền? | 1.x |
| 2 | Đơn Sỉ vs Lẻ | Flow khác nhau? Bảng giá? Công nợ? | 2.1.x |
| 3 | Bảng giá KH | Chung hay riêng theo loại KH? | 5.1.1 |
| 4 | Nguồn sản phẩm | Từ Bravo hay Website? | 7.1 |
| 5 | Công nợ KH | Định nghĩa? Cách tính? | 5.2.6 |

### 🟠 HIGH - Cần trả lời sớm (Ảnh hưởng thiết kế)

| # | Chủ đề | Câu hỏi chính | Mục |
|---|--------|---------------|-----|
| 6 | Fitting → Product | Có map không? Logic? | 2.2.x |
| 7 | Gói Coaching | Tạo sẵn hay tạo mới mỗi đơn? | 2.3.x |
| 8 | Thu cũ đổi mới | Hàng thu về xử lý sao? | 2.4.x |
| 9 | Công thức điểm | Tích điểm như thế nào? | 5.2.4 |
| 10 | Công thức thưởng NV | Nhập tay hay tự động? | 6.3, 6.4 |
| 11 | Tồn kho không đủ | Cho tạo đơn không? | 2.5.1 |
| 12 | Check CK tự động | Dùng SePay hay thủ công? | 8.1 |

### 🟡 MEDIUM - Có thể trả lời sau (GĐ 2)

| # | Chủ đề | Câu hỏi chính | Mục |
|---|--------|---------------|-----|
| 13 | Kênh thông báo | Zalo? SMS? Email? | 11.1 |
| 14 | Chat trong CRM | Hub thông báo hay 2 chiều? | 11.3-11.5 |
| 15 | Chính sách chiết khấu | Bao nhiêu loại? | 10.2 |
| 16 | Kế hoạch bán hàng | Cấu trúc? | 10.1 |

---

## PHẦN D: FILES CHI TIẾT (MODULES ĐẶC THÙ)

Các module sau có quá nhiều câu hỏi đặc thù, được tách riêng:

| File | Module | Số câu hỏi | Nội dung chính |
|------|--------|------------|----------------|
| [FITTING_QUESTIONS.md](./FITTING_QUESTIONS.md) | ⛳ Fitting Golf | 17 câu | Thông số kỹ thuật, form đặt lịch, dịch vụ phát sinh |
| [COACHING_QUESTIONS.md](./COACHING_QUESTIONS.md) | 🏌️ Coaching Golf | 27 câu | Gói học, HLV, sân tập, bài test, lịch học |
| [SHIPPING_QUESTIONS.md](./SHIPPING_QUESTIONS.md) | 🚚 Vận chuyển | 35 câu | Viettel Post, COD, phí ship, đơn hoàn |
| [BRAVO_QUESTIONS.md](./BRAVO_QUESTIONS.md) | 🔄 Bravo ERP | 30 câu | API, sync SP/Kho, master data |

---

## Action Items

| # | Action | Owner | Deadline |
|---|--------|-------|----------|
| 1 | Gửi file này cho NM review trước buổi họp | DCNET | |
| 2 | NM chuẩn bị câu trả lời (ưu tiên 🔴 CRITICAL) | NM | |
| 3 | Họp clarify các câu hỏi | Cả 2 | |
| 4 | Update file này sau buổi họp | DCNET | |

---

*Tạo: 2025-12-10*
*Cập nhật: 2025-12-10*
