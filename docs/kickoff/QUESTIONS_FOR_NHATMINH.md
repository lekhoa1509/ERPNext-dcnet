# CÂU HỎI CẦN NHẬT MINH XÁC NHẬN

> **Dự án:** DCNET Flow - CRM cho Nhật Minh Sport
>
> **Ngày tạo:** 2025-12-11
>
> **Mục đích:** Tổng hợp tất cả câu hỏi cần làm rõ trước khi triển khai

---

## MỤC LỤC

1. [Đại lý / Chi nhánh](#1-đại-lý--chi-nhánh)
2. [Đơn hàng - Phân loại & Flow](#2-đơn-hàng---phân-loại--flow)
3. [Doanh số & Báo cáo](#3-doanh-số--báo-cáo)
4. [Lead Management](#4-lead-management)
5. [Quản lý Khách hàng](#5-quản-lý-khách-hàng)
6. [Quản lý Nhân viên](#6-quản-lý-nhân-viên)
7. [Quản lý Sản phẩm](#7-quản-lý-sản-phẩm)
8. [Thanh toán](#8-thanh-toán)
9. [Tích hợp Sàn TMĐT](#9-tích-hợp-sàn-tmđt)
10. [Module Fitting Golf](#10-module-fitting-golf)
11. [Module Coaching Golf](#11-module-coaching-golf)
12. [Tích hợp Vận chuyển](#12-tích-hợp-vận-chuyển)
13. [Tích hợp Bravo ERP](#13-tích-hợp-bravo-erp)
14. [Chăm sóc Khách hàng & Loyalty](#14-chăm-sóc-khách-hàng--loyalty)
15. [Dữ liệu cần từ Nhật Minh](#15-dữ-liệu-cần-từ-nhật-minh)
16. [Đầu mối liên hệ](#16-đầu-mối-liên-hệ)
17. [Vận hành dự án](#17-vận-hành-dự-án)

---

## Độ ưu tiên

| Mức | Ký hiệu | Ý nghĩa |
|-----|---------|---------|
| 🔴 | CRITICAL | Block development nếu không có |
| 🟠 | HIGH | Ảnh hưởng thiết kế, cần sớm |
| 🟡 | MEDIUM | Có thể làm rõ trong quá trình dev |

---

# PHẦN A: NGHIỆP VỤ CORE

---

## 1. Đại lý / Chi nhánh 🔴

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1.1 | **Định nghĩa "Chi nhánh"**: Là cửa hàng của NM hay đại lý bên ngoài? | |
| 1.2 | Hiện có bao nhiêu chi nhánh/đại lý? | |
| 1.3 | Chi nhánh có **kho riêng** không? Hay dùng chung kho? | |
| 1.4 | Chi nhánh có **bảng giá riêng** không? | |
| 1.5 | Cần **phân quyền theo chi nhánh** không? (NV chỉ xem data chi nhánh mình) | |
| 1.6 | **Chi nhánh của KH** có phải để xác định đơn hàng phát sinh từ đâu? | |

---

## 2. Đơn hàng - Phân loại & Flow

### 2.1. Đơn Sỉ vs Lẻ 🔴

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 2.1.1 | Khác biệt chính giữa đơn Sỉ và Lẻ? (Giá? Số lượng tối thiểu? Thanh toán?) | |
| 2.1.2 | Đơn Sỉ có **bảng giá riêng**? Theo số lượng hay theo KH? | |
| 2.1.3 | Đơn Sỉ có **công nợ**? Cho nợ bao nhiêu ngày? | |
| 2.1.4 | **Flow xử lý** đơn Sỉ khác Lẻ như thế nào? (Duyệt? Xuất kho?) | |

### 2.2. Thu cũ Đổi mới 🟠

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 2.2.1 | **Hàng thu về** xử lý như thế nào? (Nhập kho / Thanh lý / Khác) | |
| 2.2.2 | Hàng thu về nhập vào **kho nào**? (Kho chính? Kho riêng?) | |
| 2.2.3 | Hàng cũ có **mã SKU riêng** không? Hay dùng chung mã SP? | |
| 2.2.4 | Có **định giá hàng cũ** không? Ai định giá? Công thức? | |
| 2.2.5 | Quy trình **định giá hàng cũ**? Ai duyệt giá? | |
| 2.2.6 | Hàng cũ có **bán lại** không? Ở đâu? Kênh nào? | |
| 2.2.7 | Cần **tracking nguồn gốc** hàng cũ? (Từ KH nào, ngày nào) | |

### 2.3. Tạo đơn - Trường hợp đặc biệt 🟠

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 2.3.1 | Nếu tạo đơn mà **không đủ tồn kho**, flow như thế nào? (Block / Cho tạo backorder / Cảnh báo) | |
| 2.3.2 | Có cho phép **đặt hàng trước** (pre-order)? | |

---

## 3. Doanh số & Báo cáo 🟠

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 3.1 | **Doanh số Sỉ/Lẻ** cần tách riêng tab để đếm? | |
| 3.2 | **Doanh số theo nguồn KH** - nguồn KH định nghĩa thế nào? (Facebook, Zalo, Walk-in?) | |
| 3.3 | **Doanh số theo nguồn đơn hàng** - các nguồn cần track? (TikTok, Lazada, Shopee, B2B, Cửa hàng) | |
| 3.4 | Có cần báo cáo **so sánh giữa các nguồn** không? | |

---

## 4. Lead Management 🟠

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 4.1 | **Tổng số tương tác** của Lead dựa vào gì? (Số cuộc gọi / Số tin nhắn / Số lần gặp / Tất cả) | |
| 4.2 | **Bảng giá cho Lead** kiểu nào? (Chung / Theo nguồn / Theo loại SP) | |
| 4.3 | **Nguồn Lead** có gắn tag không? (VD: #facebook #zalo #event) | |
| 4.4 | Danh sách **nguồn Lead** cần tracking? (Liệt kê cụ thể) | |
| 4.5 | Vào chi tiết Lead có cần xem **log bình luận/ghi chú** không? | |
| 4.6 | Ai được quyền thêm bình luận? (NV phụ trách / Tất cả) | |

---

## 5. Quản lý Khách hàng 🔴

### 5.1. Thiết lập chung

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 5.1.1 | **Bảng giá KH**: Chung hay riêng theo từng loại KH? (VIP, Thường, Đại lý) | |
| 5.1.2 | **Lịch chăm sóc định kỳ**: Cụ thể là gì? (Nhắc sinh nhật / Nhắc sau X ngày mua / Khác) | |
| 5.1.3 | Có bao nhiêu **loại lịch chăm sóc**? | |

### 5.2. Danh sách Khách hàng - Các trường dữ liệu

| # | Trường | Câu hỏi | Trả lời |
|---|--------|---------|---------|
| 5.2.1 | **Liên hệ lần cuối** | Tự động cập nhật hay nhập text thủ công? | |
| 5.2.2 | **Nguồn Lead** | Từ Lead chuyển qua tự động hay tự thêm tay? | |
| 5.2.3 | **Chi nhánh** | Định nghĩa: NV phụ trách? Nơi mua? Nơi đăng ký? | |
| 5.2.4 | **Số điểm hiện tại** | Xin **công thức tính điểm**? | |
| 5.2.5 | **Doanh số phát sinh** | = Tổng tiền tất cả đơn hàng của KH? | |
| 5.2.6 | **Công nợ** | Định nghĩa: Tiền KH đang nợ NM? Hay ngược lại? | |

---

## 6. Quản lý Nhân viên 🟠

| # | Trường | Câu hỏi | Trả lời |
|---|--------|---------|---------|
| 6.1 | **Hiệu suất** | Công thức tính? (VD: Số đơn/tháng? Tỷ lệ chốt?) | |
| 6.2 | **Doanh thu** | = Tổng đơn hàng NV quản lý? Hay chỉ NV tạo đơn? | |
| 6.3 | **Thưởng** | Nhập tay hay Tính theo công thức? | |
| 6.4 | Nếu có công thức thưởng, xin chi tiết? | % doanh số? Theo KPI? | |

---

## 7. Quản lý Sản phẩm 🔴

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 7.1 | **Nguồn sản phẩm**: Không thêm từ CRM, vậy kéo từ đâu? (Website bán hàng / Bravo / Cả hai) | |
| 7.2 | Nếu từ Bravo, có cần **đồng bộ 2 chiều** không? (CRM → Bravo?) | |

---

## 8. Thanh toán 🟠

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 8.1 | **Chuyển khoản**: Check thủ công hay tự động? (Tự động cần tích hợp ngân hàng ~200-500đ/GD) | |
| 8.2 | Nếu tự động, **ngân hàng nào**? | |
| 8.3 | Có cần **QR Code VietQR** để khách quét CK? | |
| 8.4 | **COD**: NM có đội giao hàng riêng không? (Có / Không - qua ĐVVC) | |
| 8.5 | Nếu qua ĐVVC, đơn vị nào? (Viettel Post / GHTK / GHN) | |

---

## 9. Tích hợp Sàn TMĐT 🟡

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 9.1 | Hiện NM đang bán trên những sàn nào? (Shopee / TikTok / Lazada / Khác) | |
| 9.2 | Đã có tài khoản **Seller Center** chưa? | |
| 9.3 | Muốn **sync những gì** từ sàn? (Đơn hàng / Sản phẩm / Tồn kho / Tất cả) | |

---

# PHẦN B: MODULE FITTING GOLF

---

## 10. Module Fitting Golf 🟠

### 10.1. Thông tin kỹ thuật

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 10.1.1 | **Size tay** có những loại nào? (VD: S/M/L/XL hay đo theo số cm?) | |
| 10.1.2 | **Đường bóng** có những giá trị nào? (VD: Fade / Draw / Straight / Hook / Slice?) | |
| 10.1.3 | **Đường cao bóng** có những giá trị nào? (VD: Low / Mid / High?) | |
| 10.1.4 | **Cấp độ người chơi** ngoài "Người mới / Đã chơi" có level nào khác? | |
| 10.1.5 | **Đơn vị đo** sử dụng là gì? (Khoảng cách: yard hay mét? Tốc độ: mph hay km/h?) | |
| 10.1.6 | **Hình swing** lưu dạng gì? (Text mô tả? Ảnh chụp? Video?) | |

### 10.2. Quy trình & Nghiệp vụ

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 10.2.1 | **Ai thực hiện fitting?** NV bán hàng hay có NV chuyên fitting? Có cần phân quyền riêng? | |
| 10.2.2 | **Giá dịch vụ fitting** tính thế nào? Có bảng giá riêng? Miễn phí hay tính tiền? | |
| 10.2.3 | **Workflow đơn Fitting** như thế nào? (VD: Đặt lịch → Xác nhận → Fitting → Hoàn thành → Tạo đơn SP?) | |
| 10.2.4 | **Linh kiện fitting** (grip, shaft) quản lý tồn kho chung hay riêng? | |
| 10.2.5 | **Đơn Fitting có đồng bộ sang Bravo không?** Hay chỉ quản lý trên CRM? | |

### 10.3. Form đặt lịch Website

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 10.3.1 | **Xài lại form đặt lịch** trên website hiện tại không? (Có / Không - build form mới) | |
| 10.3.2 | Nếu **xài lại** → Cần sync từ web sang CRM như thế nào? (API realtime / Webhook / Cron job) | |
| 10.3.3 | Nếu **build mới** → Form nằm ở đâu? (Tích hợp vào web / Subdomain riêng / Trên CRM public) | |
| 10.3.4 | Form cần thêm field nào ngoài Ngày + Giờ? (Họ tên / SĐT / Email / Ghi chú / Chi nhánh) | |

### 10.4. Dịch vụ phát sinh

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 10.4.1 | Danh sách **dịch vụ phát sinh** cụ thể? (Ngoài: Mua grip, Lắp shaft, Đặt gậy đặc biệt, Combo fitting+gậy còn gì?) | |
| 10.4.2 | **Giá dịch vụ phát sinh** có sẵn bảng giá không? Hay nhập tay từng đơn? | |

### 10.5. Fitting → Sản phẩm

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 10.5.1 | Sau khi Fitting, có **tư vấn chọn sản phẩm** không? (Gợi ý SP phù hợp với thông số) | |
| 10.5.2 | Nếu có, cần **map Fitting với Product ID** không? (Để tracking KH fitting → mua SP) | |
| 10.5.3 | Có template gợi ý SP theo thông số không? (VD: swing speed 85mph → shaft X) | |

---

# PHẦN C: MODULE COACHING GOLF

---

## 11. Module Coaching Golf 🟠

### 11.1. Bài test đầu vào

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.1.1 | **Bài test đầu vào** gồm những nội dung gì? Các tiêu chí đánh giá? Thang điểm? | |
| 11.1.2 | **Ai thực hiện test?** HLV hay NV khác? | |
| 11.1.3 | **Kết quả test** lưu dạng gì? (Điểm số? Text nhận xét? File đính kèm?) | |
| 11.1.4 | **Test có bắt buộc** với tất cả học viên không? Hay chỉ một số gói? | |

### 11.2. Gói huấn luyện & HLV

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.2.1 | **Danh sách gói huấn luyện** hiện có? (VD: 8 buổi cơ bản, 12 buổi nâng cao...) Có mẫu không? | |
| 11.2.2 | **Giá từng gói** như thế nào? Có bảng giá chuẩn? | |
| 11.2.3 | **HLV** có thông tin đặc biệt gì cần lưu? (VD: Chứng chỉ, Kinh nghiệm, Rating, Chuyên môn?) | |
| 11.2.4 | **Một HLV dạy tối đa bao nhiêu học viên** cùng lúc? Có giới hạn? | |
| 11.2.5 | **Các gói huấn luyện** có tạo sẵn trong CRM không? Hay nhập tay mỗi đơn? | |
| 11.2.6 | Một gói có thể chia nhiều HLV không? | |

### 11.3. Sân tập & Địa điểm

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.3.1 | **Danh sách sân tập** hiện có? (Tên, địa chỉ, số lane?) | |
| 11.3.2 | **Sân tập** thuộc Nhật Minh hay đối tác? Có cần quản lý booking sân? | |

### 11.4. Lịch học & Điểm danh

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.4.1 | **Lịch học** cố định hay linh hoạt? (VD: Thứ 2-4-6 hàng tuần hay đặt từng buổi?) | |
| 11.4.2 | **Điểm danh** có cần tracking không? Học viên vắng thì xử lý thế nào? (Học bù? Mất buổi?) | |
| 11.4.3 | **Thời lượng 1 buổi học** là bao lâu? (60 phút? 90 phút?) | |

### 11.5. Thanh toán Coaching

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.5.1 | **Thanh toán** theo buổi hay trọn gói? | |
| 11.5.2 | **Có đặt cọc** trước không? Bao nhiêu %? | |
| 11.5.3 | **Hoàn tiền** nếu học viên nghỉ giữa chừng? Có chính sách không? | |

### 11.6. Trình độ học viên

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.6.1 | **Trình độ học viên** có những level nào? (VD: Chưa biết chơi / Cơ bản / Trung bình / Nâng cao?) | |
| 11.6.2 | **Loại khóa học** có những loại nào? (VD: Cá nhân / Nhóm / Thi đấu?) | |
| 11.6.3 | **Mục tiêu học** có danh sách mẫu không? Hay học viên tự nhập? | |

### 11.7. Báo cáo & Tracking Coaching

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.7.1 | **"Doanh thu phát sinh sau coaching"** tính thế nào? (Là đơn hàng SP của học viên sau khi kết thúc khóa? Trong bao lâu?) | |
| 11.7.2 | **Đơn Coaching có đồng bộ sang Bravo không?** Hay chỉ quản lý trên CRM? | |

### 11.8. Câu hỏi chung Fitting & Coaching

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 11.8.1 | **Fitting và Coaching** có liên kết với nhau không? (VD: Học viên Coaching có được Fitting miễn phí?) | |
| 11.8.2 | **Khách Fitting/Coaching** có tự động thành **Lead** hay **Customer**? Quy trình chuyển đổi? | |
| 11.8.3 | **Báo cáo** cần xuất file (Excel/PDF) không? Hay chỉ xem trên hệ thống? | |
| 11.8.4 | **Thông báo nhắc lịch** có cần không? Gửi qua kênh nào? (SMS/Zalo/Email) | |
| 11.8.5 | **Lịch sử kỹ thuật** của khách có cần lưu theo thời gian? (Để theo dõi tiến bộ?) | |
| 11.8.6 | **Thông số kỹ thuật** giữa Fitting và Coaching có share không? (Nếu KH đã Fitting → auto fill cho Coaching?) | |

---

# PHẦN D: TÍCH HỢP VẬN CHUYỂN

---

## 12. Tích hợp Vận chuyển 🟠

### 12.1. Scope tích hợp

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.1.1 | Đơn vị vận chuyển cần tích hợp MVP? (Chỉ Viettel Post / + GHTK / + GHN) | |
| 12.1.2 | Nếu nhiều đơn vị, ưu tiên đơn vị nào? (1. ___ 2. ___ 3. ___) | |

### 12.2. Flow nghiệp vụ

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.2.1 | Thời điểm tạo đơn giao vận? (Tự động sau xác nhận / NV tạo thủ công / Tự động sau xuất kho) | |
| 12.2.2 | Ai có quyền tạo đơn giao vận? (NV bán hàng / NV kho / Cả hai) | |
| 12.2.3 | Có cho phép chọn loại dịch vụ? (Mặc định 1 loại / Cho chọn nhiều loại) | |
| 12.2.4 | Có cho phép chọn đơn vị VC? (Cố định 1 đơn vị / Cho chọn tại thời điểm tạo) | |

### 12.3. COD - Thu hộ

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.3.1 | Có sử dụng COD (thu hộ)? (Có / Không) | |
| 12.3.2 | Tỷ lệ đơn COD ước tính? (___%) | |
| 12.3.3 | Flow đối soát COD như thế nào? (Manual / Tự động sync từ nhà VC) | |
| 12.3.4 | COD tích hợp với công nợ? (Có - tự động cập nhật / Không - track riêng) | |

### 12.4. Phí vận chuyển

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.4.1 | Ai trả phí vận chuyển? (Khách hàng / Shop / Tùy đơn hàng) | |
| 12.4.2 | Có cần ước tính phí trước? (Có - call API tính phí / Không) | |
| 12.4.3 | Phí VC có hiển thị trên đơn hàng? (Có / Không) | |
| 12.4.4 | Có chính sách miễn phí VC? (Có - đơn từ ___ VNĐ / Không) | |

### 12.5. Địa điểm gửi hàng

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.5.1 | Gửi hàng từ bao nhiêu địa điểm? (1 kho / Nhiều chi nhánh: ___ điểm) | |
| 12.5.2 | Cách chọn địa điểm gửi? (Tự động theo kho xuất / NV chọn thủ công) | |
| 12.5.3 | Đã có địa chỉ đăng ký với Viettel Post? (Có / Chưa) | |

### 12.6. In phiếu giao hàng

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.6.1 | Có cần in phiếu từ CRM? (Có / Không - lên portal nhà VC in) | |
| 12.6.2 | Nếu in từ CRM, template nào? (Mẫu chuẩn Viettel Post / Mẫu custom) | |
| 12.6.3 | Có in kèm hóa đơn bán hàng? (Có / Không) | |

### 12.7. Thông báo cho khách hàng

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.7.1 | Gửi thông báo khi tạo vận đơn? (Có / Không) | |
| 12.7.2 | Gửi thông báo khi cập nhật trạng thái? (Có / Không) | |
| 12.7.3 | Kênh gửi thông báo? (Zalo OA / SMS / Email) | |
| 12.7.4 | Có template tin nhắn sẵn? (Có / DCNET đề xuất) | |

### 12.8. Đơn hàng đặc biệt

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.8.1 | Đơn Fitting có cần giao hàng? (Có - phụ kiện phát sinh / Không) | |
| 12.8.2 | Đơn Coaching có cần giao hàng? (Có - tài liệu, dụng cụ / Không) | |
| 12.8.3 | Đơn thu cũ đổi mới - lấy hàng cũ? (Có - cần giao vận ngược / Không - khách tự mang) | |
| 12.8.4 | Đơn bảo hành - giao trả hàng? (Có / Không - khách tự lấy) | |

### 12.9. Xử lý hoàn/trả

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.9.1 | Khi đơn hoàn, xử lý như thế nào? (Tự động cập nhật tồn kho / Manual - NV xác nhận) | |
| 12.9.2 | Có tạo phiếu nhập kho tự động? (Có / Không) | |
| 12.9.3 | Có ghi nhận lý do hoàn? (Có / Không) | |

### 12.10. API & Tài khoản

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.10.1 | Đã có tài khoản Viettel Post? (Có / Chưa - cần đăng ký) | |
| 12.10.2 | Loại tài khoản VP? (Cá nhân / Doanh nghiệp) | |
| 12.10.3 | Nếu có GHTK - đã có TK? (Có / Chưa / N/A) | |
| 12.10.4 | Nếu có GHN - đã có TK? (Có / Chưa / N/A) | |

### 12.11. Báo cáo vận chuyển

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 12.11.1 | Cần báo cáo gì về vận chuyển? (Số đơn giao thành công / Số đơn hoàn trả / Tổng phí VC / Thời gian giao TB / Tỷ lệ giao thành công) | |
| 12.11.2 | Báo cáo theo chiều nào? (Theo thời gian / Theo nhà VC / Theo chi nhánh) | |

---

# PHẦN E: TÍCH HỢP BRAVO ERP

---

## 13. Tích hợp Bravo ERP 🔴

### 13.1. Chức năng đang sử dụng trên Bravo

| # | Module Bravo | Đang dùng? |
|---|--------------|------------|
| 13.1.1 | Quản lý Sản phẩm | ☐ Có ☐ Không |
| 13.1.2 | Quản lý Kho / Tồn kho | ☐ Có ☐ Không |
| 13.1.3 | Quản lý Đơn hàng / Bán hàng | ☐ Có ☐ Không |
| 13.1.4 | Quản lý Khách hàng | ☐ Có ☐ Không |
| 13.1.5 | Kế toán / Công nợ | ☐ Có ☐ Không |
| 13.1.6 | Quản lý Nhân sự | ☐ Có ☐ Không |
| 13.1.7 | Báo cáo | ☐ Có ☐ Không |
| 13.1.8 | Khác | |

### 13.2. Workflow hiện tại

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 13.2.1 | **Nhập sản phẩm mới** ở đâu? (Bravo / Website / Khác) | |
| 13.2.2 | **Quản lý tồn kho** ở đâu? (Bravo / Website / Khác) | |
| 13.2.3 | **Bán hàng offline** (cửa hàng) dùng gì? (Bravo / POS riêng / Khác) | |
| 13.2.4 | **Bán hàng online** (web) đơn về đâu? (Bravo / WooCommerce / Cả hai) | |
| 13.2.5 | **Quản lý khách hàng** ở đâu? (Bravo / Excel / Khác) | |
| 13.2.6 | **Kế toán / Công nợ** ở đâu? (Bravo / Excel / Khác) | |

### 13.3. Dữ liệu Master

| # | Loại dữ liệu | Master ở đâu? |
|---|--------------|---------------|
| 13.3.1 | Sản phẩm | ☐ Bravo ☐ CRM mới |
| 13.3.2 | Tồn kho | ☐ Bravo ☐ CRM mới |
| 13.3.3 | Khách hàng | ☐ Bravo ☐ CRM mới |
| 13.3.4 | Đơn hàng | ☐ Bravo ☐ CRM mới |
| 13.3.5 | Chi nhánh | ☐ Bravo ☐ CRM mới |
| 13.3.6 | Nhân viên | ☐ Bravo ☐ CRM mới |

### 13.4. Khả năng kỹ thuật - API

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 13.4.1 | Bravo đã có API sẵn chưa? (Có / Không / Không biết) | |
| 13.4.2 | Nếu có, là API đọc hay ghi? (Chỉ đọc / Chỉ ghi / Cả hai) | |
| 13.4.3 | Có tài liệu API không? (Có / Không) | |
| 13.4.4 | Cần request Bravo cung cấp API không? (Có / Không) | |
| 13.4.5 | Nếu cần request, có mất phí không? (Có / Không / Không biết) | |

### 13.5. Khả năng kỹ thuật - Database Access

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 13.5.1 | Bravo cho phép kết nối DB từ bên ngoài không? (Có / Không) | |
| 13.5.2 | Loại database của Bravo? (SQL Server / Oracle / Khác) | |
| 13.5.3 | Có tài liệu DB schema không? (Có / Không) | |

### 13.6. Khả năng kỹ thuật - Export/Import

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 13.6.1 | Bravo có chức năng export Excel không? (Có / Không) | |
| 13.6.2 | Có thể schedule export tự động không? (Có / Không) | |
| 13.6.3 | Bravo có chức năng import Excel không? (Có / Không) | |

### 13.7. Đầu mối kỹ thuật Bravo

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 13.7.1 | Ai quản lý Bravo của Nhật Minh? (Tự quản lý / Bravo support) | |
| 13.7.2 | Đầu mối kỹ thuật Bravo? (Tên: ___ SĐT: ___) | |
| 13.7.3 | Có hợp đồng support với Bravo không? (Có / Không) | |
| 13.7.4 | Phiên bản Bravo đang dùng? (Bravo 8 / Bravo 10 / Khác) | |

### 13.8. Câu hỏi quyết định

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 13.8.1 | Bravo có API không? | |
| 13.8.2 | Scope sync những gì? | |
| 13.8.3 | Dữ liệu master ở đâu? | |
| 13.8.4 | Chấp nhận sync qua Excel không? (Nếu không có API) | |

---

# PHẦN F: CHĂM SÓC KHÁCH HÀNG & LOYALTY

---

## 14. Chăm sóc Khách hàng & Loyalty 🟠

### 14.1. Lịch chăm sóc tự động

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 14.1.1 | Các **loại lịch chăm sóc** cần thiết lập? (Sinh nhật / Sau mua / VIP / Lâu chưa mua / Khác) | |
| 14.1.2 | **Thời gian nhắc** mặc định cho từng loại? (VD: 7 ngày sau mua, 30 ngày không mua) | |
| 14.1.3 | **Ai nhận thông báo** khi đến hạn chăm sóc? (NV phụ trách / Quản lý / Cả hai) | |
| 14.1.4 | **Hành động** sau khi nhắc? (Gọi điện / Nhắn tin / Email / Tất cả) | |
| 14.1.5 | Có cần **log lại kết quả** chăm sóc không? (Đã gọi, không nghe máy, đã tư vấn...) | |
| 14.1.6 | **Phân nhóm KH** để chăm sóc khác nhau? (VD: VIP, thường, tiềm năng) | |
| 14.1.7 | **Tần suất chăm sóc** tối đa/tối thiểu? (Để không spam khách) | |
| 14.1.8 | Có cần **báo cáo hiệu quả** chăm sóc? (Tỷ lệ phản hồi, chốt đơn) | |

### 14.2. Gửi khuyến mãi tự động

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 14.2.1 | **Kênh gửi** ưu tiên? (Zalo OA / SMS / Email) | |
| 14.2.2 | Có **mẫu tin nhắn** sẵn không? Hay DCNET đề xuất? | |
| 14.2.3 | **Tiêu chí lọc KH** để gửi KM? (Tags, chi tiêu, tần suất mua, SP đã mua?) | |
| 14.2.4 | **Giới hạn gửi** tin/tháng cho mỗi KH? (Để tránh spam) | |
| 14.2.5 | Có cần **duyệt nội dung** trước khi gửi? (Admin duyệt / Không cần) | |
| 14.2.6 | Có cần **tracking mở tin/click**? (Để đo hiệu quả) | |

### 14.3. Khảo sát mức độ hài lòng

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 14.3.1 | **Thời điểm gửi khảo sát**? (Sau mua / Sau CSKH / Sau bảo hành) | |
| 14.3.2 | **Nội dung khảo sát** gồm những gì? Có template sẵn không? | |
| 14.3.3 | **Kênh gửi** khảo sát? (Link form / Zalo / Email) | |
| 14.3.4 | Có cần **đánh giá NV** không? (1-5 sao?) | |
| 14.3.5 | **Xử lý feedback tiêu cực** thế nào? (Tự động escalate / Thông báo quản lý) | |

### 14.4. Tích điểm / Loyalty 🔴

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 14.4.1 | **Công thức tích điểm**? (X điểm = Y đồng? Theo SP? Theo nguồn?) | |
| 14.4.2 | **Các hạng thành viên**? (VD: Thường, Bạc, Vàng, Kim cương?) | |
| 14.4.3 | **Điều kiện lên hạng**? (Theo điểm? Theo doanh số?) | |
| 14.4.4 | **Quyền lợi từng hạng**? (Chiết khấu? Quà tặng? Ưu tiên?) | |
| 14.4.5 | **Điểm có hết hạn** không? (Sau bao lâu?) | |
| 14.4.6 | **Quy đổi điểm** thành gì? (Voucher / Giảm giá trực tiếp / Quà) | |
| 14.4.7 | **Tỷ lệ quy đổi**? (X điểm = Y đồng voucher?) | |
| 14.4.8 | Điểm có **chuyển nhượng** được không? (Cho người khác?) | |
| 14.4.9 | **Cộng điểm tự động** hay thủ công? (Sau khi hoàn thành đơn?) | |
| 14.4.10 | Có **lịch sử điểm** cho KH xem không? (App / Website / CRM) | |

### 14.5. Tích hợp kênh giao tiếp

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 14.5.1 | **Zalo OA** đã có chưa? (Cần để tích hợp) | |
| 14.5.2 | **Loại Zalo OA**? (OA thường / OA đăng ký doanh nghiệp) | |
| 14.5.3 | **Messenger/Facebook Page** đã có? | |
| 14.5.4 | Cần **chat 2 chiều** trong CRM không? Hay chỉ gửi 1 chiều? | |
| 14.5.5 | **Ai được quyền** chat với KH? (NV phụ trách / Tất cả) | |
| 14.5.6 | Cần **template tin nhắn** chuẩn không? (VD: Chào hỏi, Xác nhận đơn...) | |

---

# PHẦN G: DỮ LIỆU & VẬN HÀNH

---

## 15. Dữ liệu cần từ Nhật Minh 🔴

| # | Dữ liệu cần | Deadline | Trạng thái |
|---|-------------|----------|------------|
| 15.1 | Mẫu file Excel (SP, KH, Đơn hàng) | 10 ngày đầu | ☐ Chưa có |
| 15.2 | Mã sản phẩm từ Bravo | 10 ngày đầu | ☐ Chưa có |
| 15.3 | Mã nhân viên | 10 ngày đầu | ☐ Chưa có |
| 15.4 | Mã chi nhánh | 10 ngày đầu | ☐ Chưa có |
| 15.5 | Mẫu kế hoạch bán hàng | Sprint 2 | ☐ Chưa có |
| 15.6 | Công thức tính thưởng (KPI) | Sprint 2 | ☐ Chưa có |
| 15.7 | Screenshot màn hình Bravo | 10 ngày đầu | ☐ Chưa có |
| 15.8 | Mẫu phiếu Fitting hiện tại (nếu có) | 10 ngày đầu | ☐ Chưa có |
| 15.9 | Danh sách các thông số kỹ thuật Fitting đầy đủ | 10 ngày đầu | ☐ Chưa có |
| 15.10 | Bảng giá dịch vụ Fitting (nếu có) | 10 ngày đầu | ☐ Chưa có |
| 15.11 | Mẫu hồ sơ học viên hiện tại (nếu có) | 10 ngày đầu | ☐ Chưa có |
| 15.12 | Danh sách gói huấn luyện + giá | 10 ngày đầu | ☐ Chưa có |
| 15.13 | Danh sách HLV hiện có | 10 ngày đầu | ☐ Chưa có |
| 15.14 | Danh sách sân tập | 10 ngày đầu | ☐ Chưa có |
| 15.15 | Mẫu bài test đầu vào (confirm với HLV) | 10 ngày đầu | ☐ Chưa có |
| 15.16 | Chính sách thanh toán/hoàn tiền Coaching | 10 ngày đầu | ☐ Chưa có |
| 15.17 | Tài liệu API Bravo (nếu có) | 10 ngày đầu | ☐ Chưa có |

---

## 16. Đầu mối liên hệ 🔴

### DCNET (2 người)

| Vị trí | Tên | Vai trò |
|--------|-----|---------|
| 📍 Hà Nội | Thịnh |  |
| 📍 Hồ Chí Minh | Đức | Tech Lead |

### Nhật Minh Sport (Cần xác nhận)

| # | Vai trò | Mức độ | Tên | Ghi chú |
|---|---------|--------|-----|---------|
| 16.1 | 🔴 Vận hành - Nghiệp vụ | CRITICAL | ? | Quyết định yêu cầu, UAT |
| 16.2 | 🔴 Bravo ERP | CRITICAL | Dung | API, nghiệp vụ Bravo |
| 16.3 | 🟠 Tích hợp bên ngoài | HIGH | ? | Zalo, Sàn TMĐT, Vận chuyển |
| 16.4 | 🟡 Fitting/Coaching | MEDIUM | ? | Nghiệp vụ golf |

> **Lưu ý:** 🔴 = Không có sẽ BLOCK dự án

---

## 17. Vận hành dự án

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 17.1 | Timeline 90 ngày (3 giai đoạn) có phù hợp? (OK / Cần điều chỉnh) | |
| 17.2 | Tần suất demo (2 tuần/lần / Khác: ___) | |
| 17.3 | Kênh liên lạc chính (Zalo group / Slack / Khác) | |
| 17.4 | Môi trường test/staging (DCNET cung cấp / NM tự có server) | |
| 17.5 | Ngày bắt đầu Sprint 1 | |

---

# TÓM TẮT THEO ĐỘ ƯU TIÊN

---

## 🔴 CRITICAL - Cần trả lời ngay (Block development)

| # | Chủ đề | Câu hỏi chính |
|---|--------|---------------|
| 1 | Đại lý/Chi nhánh | Định nghĩa? Có kho riêng? Phân quyền? |
| 2 | Đơn Sỉ vs Lẻ | Flow khác nhau? Bảng giá? Công nợ? |
| 3 | Bảng giá KH | Chung hay riêng theo loại KH? |
| 4 | Nguồn sản phẩm | Từ Bravo hay Website? |
| 5 | Công nợ KH | Định nghĩa? Cách tính? |
| 6 | Bravo API | Có API không? Scope sync? |
| 7 | Đầu mối liên hệ | Ai là đầu mối nghiệp vụ? Bravo? |

## 🟠 HIGH - Cần trả lời sớm (Ảnh hưởng thiết kế)

| # | Chủ đề | Câu hỏi chính |
|---|--------|---------------|
| 8 | Fitting → Product | Có map không? Logic? |
| 9 | Gói Coaching | Tạo sẵn hay tạo mới mỗi đơn? |
| 10 | Thu cũ đổi mới | Hàng thu về xử lý sao? |
| 11 | Công thức điểm | Tích điểm như thế nào? |
| 12 | Công thức thưởng NV | Nhập tay hay tự động? |
| 13 | Tồn kho không đủ | Cho tạo đơn không? |
| 14 | Check CK tự động | Dùng SePay hay thủ công? |
| 15 | COD | Có dùng không? Flow đối soát? |
| 16 | Loyalty | Công thức tích điểm, hạng thành viên? |

## 🟡 MEDIUM - Có thể trả lời sau

| # | Chủ đề | Câu hỏi chính |
|---|--------|---------------|
| 17 | Kênh thông báo | Zalo? SMS? Email? |
| 18 | Chat trong CRM | Hub thông báo hay 2 chiều? |
| 19 | Chính sách chiết khấu | Bao nhiêu loại? |
| 20 | Kế hoạch bán hàng | Cấu trúc? |
| 21 | Sàn TMĐT | Đang bán sàn nào? Sync gì? |

---

**Ghi chú:**

Vui lòng điền câu trả lời vào cột "Trả lời" và gửi lại cho DCNET.

Nếu có câu hỏi nào chưa rõ, vui lòng liên hệ:
- Thịnh (Hà Nội)
- Đức (HCM): Tech Lead

---

*Tạo: 2025-12-11*
*DCNET Flow Project*
