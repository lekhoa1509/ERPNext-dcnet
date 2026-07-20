# Kickoff Questions - Tổng hợp

> **Buổi họp:** Kickoff Meeting - Nhật Minh Sport
>
> **Mục đích:** Danh sách các vấn đề cần làm rõ trước khi bắt đầu triển khai

---

## Trạng thái tổng quan

| Module | Số câu hỏi | Trạng thái | Link |
|--------|------------|------------|------|
| **📋 TỔNG HỢP CHÍNH** | 60+ câu | 🔴 Chưa xác nhận | [CLARIFICATION_QUESTIONS.md](./questions/CLARIFICATION_QUESTIONS.md) |
| **⛳ Fitting** | 17 câu | 🔴 Chưa xác nhận | [Chi tiết →](./questions/FITTING_QUESTIONS.md) |
| **🏌️ Coaching** | 27 câu | 🔴 Chưa xác nhận | [Chi tiết →](./questions/COACHING_QUESTIONS.md) |
| **🚚 Vận chuyển** | 35 câu | Chưa xác nhận | [Chi tiết →](./questions/SHIPPING_QUESTIONS.md) |
| **🔄 Bravo Integration** | 30 câu | Chưa xác nhận | [Chi tiết →](./questions/BRAVO_QUESTIONS.md) |
| **💚 Chăm sóc KH & Loyalty** | 35 câu | 🔴 Chưa xác nhận | [Mục 8](#8-chăm-sóc-khách-hàng--loyalty) |
| Dữ liệu từ Nhật Minh | 7 | Chưa xác nhận | [Mục 3](#3-dữ-liệu-cần-từ-nhật-minh) |
| Quy trình nghiệp vụ | 4 | Chưa xác nhận | [Mục 4](#4-quy-trình-nghiệp-vụ) |
| **Cần làm rõ từ PHỤ LỤC** | 3 | ⚠️ Chưa rõ | [Mục 4.1](#41-cần-làm-rõ-từ-phụ-lục) |
| Đầu mối liên hệ | 4 vai trò | Chưa xác nhận | [Chi tiết](./CONTACT_POINTS.md) |
| Vận hành dự án | 5 | Chưa xác nhận | [Mục 6](#6-vận-hành-dự-án) |
| Bàn giao & Bảo hành | 4 | Chưa xác nhận | [Mục 7](#7-bàn-giao-mã-nguồn--bảo-hành) |

---

## Câu hỏi theo Module (Chi tiết)

### Modules cần tích hợp bên ngoài

| # | Module | Plugin | Ưu tiên | Chi tiết |
|---|--------|--------|---------|----------|
| 1 | **Tích hợp Vận chuyển** | `dcnet/shipping` | Cao | [SHIPPING_QUESTIONS.md](./questions/SHIPPING_QUESTIONS.md) |
| 2 | Tích hợp Thanh toán | - | Thấp | [PAYMENT_QUESTIONS.md](./questions/PAYMENT_QUESTIONS.md) |
| 3 | Tích hợp TMĐT | `dcnet/ecommerce` | TB | *(Tạo sau)* |
| 4 | **Tích hợp Bravo** | `dcnet/bravo` | Cao | [BRAVO_QUESTIONS.md](./questions/BRAVO_QUESTIONS.md) |

### Modules nghiệp vụ đặc thù

| # | Module | Plugin | Ưu tiên | Chi tiết |
|---|--------|--------|---------|----------|
| 5 | Lead Management | `dcnet/leads` | Cao | *(Tạo sau)* |
| 6 | **Fitting** | `dcnet/fitting` | 🔴 Cao | [FITTING_COACHING_QUESTIONS.md](./questions/FITTING_COACHING_QUESTIONS.md#a-module-fitting-đơn-fitting-golf) |
| 7 | **Coaching** | `dcnet/coaching` | 🔴 Cao | [FITTING_COACHING_QUESTIONS.md](./questions/FITTING_COACHING_QUESTIONS.md#b-module-coaching-đơn-coaching) |

---

## Câu hỏi chung (Không theo module)

### 2. Tích hợp Thanh toán Online

| # | Câu hỏi | Lựa chọn | Trả lời |
|---|---------|----------|---------|
| 1 | Có cần tích hợp thanh toán online? | ☐ Không (chỉ tiền mặt/CK/COD) | |
| | | ☐ Có (VNPay/MoMo/ZaloPay) | |
| 2 | Nếu có, ưu tiên cổng nào? | ☐ VNPay ☐ MoMo ☐ ZaloPay | |

---

### 3. Dữ liệu cần từ Nhật Minh

| # | Dữ liệu cần | Deadline | Người phụ trách | Trạng thái |
|---|-------------|----------|-----------------|------------|
| 1 | Mẫu file Excel (SP, KH, Đơn hàng) | 10 ngày đầu | | ☐ Chưa có |
| 2 | Mã sản phẩm từ Bravo | 10 ngày đầu | | ☐ Chưa có |
| 3 | Mã nhân viên | 10 ngày đầu | | ☐ Chưa có |
| 4 | Mã chi nhánh | 10 ngày đầu | | ☐ Chưa có |
| 5 | Mẫu kế hoạch bán hàng | Sprint 2 | | ☐ Chưa có |
| 6 | Công thức tính thưởng (KPI) | Sprint 2 | | ☐ Chưa có |
| 7 | Screenshot màn hình Bravo | 10 ngày đầu | | ☐ Chưa có |

---

### 4. Quy trình nghiệp vụ

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 1 | **Rule chia Lead:** Admin tự phân công hay cần auto chia? | Mặc định: Admin tự phân công | |
| 2 | **Bài test đầu vào Coaching:** Có template sẵn không? | Liên quan HLV | |
| 3 | **Chính sách chiết khấu:** Có bao nhiêu tệp KH với mức CK khác nhau? | Để tạo bảng giá | |
| 4 | **Website B2B riêng:** Đã có chưa hay cần build mới? | Cho đại lý đặt hàng | |

---

### 4.1. Cần làm rõ từ PHỤ LỤC

> **Lưu ý:** Các chức năng sau có nhắc trong PHỤ LỤC nhưng chưa mô tả chi tiết

| # | Chức năng | Câu hỏi cần làm rõ | PHỤ LỤC STT | Trả lời |
|---|-----------|-------------------|-------------|---------|
| 1 | **Loại KH Lẻ/Sỉ** | Khác biệt giữa Lẻ và Sỉ? Có chính sách giá riêng? Có flow xử lý đơn riêng? | STT 16-17 | |
| 2 | **Công nợ khách hàng** | Quy trình theo dõi công nợ? Có nhắc nợ tự động? Có liên kết với Bravo? | STT 17 (DS KH) | |
| 3 | **Bảo hành sản phẩm** | Thông tin bảo hành lấy từ đâu? Chỉ hiển thị hay cần quản lý? Chỉ gậy golf + shaft? | STT 36 | |

---

### 5. Đầu mối liên hệ

> **Chi tiết đầy đủ:** [CONTACT_POINTS.md](./CONTACT_POINTS.md)

#### DCNET (2 người)

| Vị trí | Tên | Vai trò |
|--------|-----|---------|
| 📍 Hà Nội | Thịnh | Customer Contact - Tiếp nhận yêu cầu, họp với khách |
| 📍 Hồ Chí Minh | Đức | Tech Lead - Lead team dev, quyết định kỹ thuật |

#### Nhật Minh Sport (Cần xác nhận)

| # | Vai trò | Mức độ | Tên | Ghi chú |
|---|---------|--------|-----|---------|
| 1 | 🔴 Vận hành - Nghiệp vụ | CRITICAL | ? | Quyết định yêu cầu, UAT |
| 2 | 🔴 Bravo ERP | CRITICAL | Dung | API, nghiệp vụ Bravo |
| 3 | 🟠 Tích hợp bên ngoài | HIGH | ? | Zalo, Sàn TMĐT, Vận chuyển |
| 4 | 🟡 Fitting/Coaching | MEDIUM | ? | Nghiệp vụ golf |

> **Lưu ý:** 🔴 = Không có sẽ BLOCK dự án

---

### 6. Vận hành dự án

| # | Câu hỏi | Lựa chọn | Trả lời |
|---|---------|----------|---------|
| 1 | Timeline 90 ngày (3 giai đoạn) có phù hợp? | ☐ OK ☐ Cần điều chỉnh | |
| 2 | Tần suất demo | ☐ 2 tuần/lần ☐ Khác: ___ | |
| 3 | Kênh liên lạc chính | ☐ Zalo group ☐ Slack ☐ Khác | |
| 4 | Môi trường test/staging | ☐ DCNET cung cấp ☐ NM tự có server | |
| 5 | Ngày bắt đầu Sprint 1 | | |

---

### 7. Bàn giao mã nguồn & Bảo hành

#### 7.1. Bàn giao Source Code

| # | Câu hỏi | Lựa chọn | Trả lời |
|---|---------|----------|---------|
| 1 | Có yêu cầu bàn giao source code sau khi hoàn thành? | ☐ Có ☐ Không | |
| 2 | Nếu có, thời điểm bàn giao? | ☐ Sau nghiệm thu ☐ Sau bảo hành ☐ Khác | |

#### 7.2. Rủi ro khi bàn giao Source Code

> **Lưu ý nội bộ DCNET:** Cần cân nhắc các rủi ro sau nếu bàn giao source

| Rủi ro | Mô tả | Cơ chế kiểm soát đề xuất |
|--------|-------|--------------------------|
| **Đối tác khác can thiệp** | Khách đưa source cho bên thứ 3 chỉnh sửa, gây lỗi hệ thống | Điều khoản: DCNET không chịu trách nhiệm nếu có bên thứ 3 can thiệp |
| **Ảnh hưởng bảo hành** | Bên thứ 3 sửa code → lỗi → khách yêu cầu DCNET bảo hành | Điều khoản: Bảo hành chỉ áp dụng khi không có can thiệp từ bên ngoài |
| **Mất kiểm soát chất lượng** | Code bị sửa đổi không đúng chuẩn | Yêu cầu thông báo trước khi cho bên khác can thiệp |

#### 7.3. Chính sách Bảo hành

| # | Hạng mục | Thông tin | Ghi chú |
|---|----------|-----------|---------|
| 1 | Thời gian bảo hành | 6 tháng | Yêu cầu từ Nhật Minh |
| 2 | Phạm vi bảo hành | ☐ Lỗi phần mềm do DCNET ☐ Hỗ trợ vận hành | Cần làm rõ |
| 3 | Điều kiện bảo hành | Không có can thiệp từ bên thứ 3 | Đề xuất |
| 4 | Hỗ trợ sau bảo hành | ☐ Có (tính phí) ☐ Không | |

#### 7.4. Đề xuất điều khoản hợp đồng

```
Nếu bàn giao source code:

1. Bảo hành 6 tháng chỉ áp dụng khi:
   - Hệ thống vận hành trên môi trường DCNET triển khai
   - Không có sự can thiệp/chỉnh sửa từ bên thứ 3

2. Nếu khách cho bên thứ 3 can thiệp vào source code:
   - Phải thông báo bằng văn bản cho DCNET
   - DCNET được miễn trừ trách nhiệm với các lỗi phát sinh sau đó
   - Chính sách bảo hành sẽ chấm dứt từ thời điểm can thiệp

3. Quyền sở hữu:
   - Nhật Minh sở hữu dữ liệu nghiệp vụ
   - DCNET giữ quyền sở hữu trí tuệ với framework/plugin core
```

---

### 8. Chăm sóc Khách hàng & Loyalty

> **Lưu ý:** Đây là phần quan trọng để duy trì và phát triển khách hàng

#### 8.1. Lịch chăm sóc tự động 🟠

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 1 | Các **loại lịch chăm sóc** cần thiết lập? | ☐ Sinh nhật ☐ Sau mua ☐ VIP ☐ Lâu chưa mua ☐ Khác | |
| 2 | **Thời gian nhắc** mặc định cho từng loại? | VD: 7 ngày sau mua, 30 ngày không mua | |
| 3 | **Ai nhận thông báo** khi đến hạn chăm sóc? | ☐ NV phụ trách ☐ Quản lý ☐ Cả hai | |
| 4 | **Hành động** sau khi nhắc? | ☐ Gọi điện ☐ Nhắn tin ☐ Email ☐ Tất cả | |
| 5 | Có cần **log lại kết quả** chăm sóc không? | Đã gọi, không nghe máy, đã tư vấn... | |
| 6 | **Phân nhóm KH** để chăm sóc khác nhau? | VD: VIP, thường, tiềm năng | |
| 7 | **Tần suất chăm sóc** tối đa/tối thiểu? | Để không spam khách | |
| 8 | Có cần **báo cáo hiệu quả** chăm sóc? | Tỷ lệ phản hồi, chốt đơn | |

---

#### 8.2. Gửi khuyến mãi tự động 🟠

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 1 | **Kênh gửi** ưu tiên? | ☐ Zalo OA ☐ SMS ☐ Email | |
| 2 | Có **mẫu tin nhắn** sẵn không? | Hay DCNET đề xuất? | |
| 3 | **Tiêu chí lọc KH** để gửi KM? | Tags, chi tiêu, tần suất mua, SP đã mua? | |
| 4 | **Giới hạn gửi** tin/tháng cho mỗi KH? | Để tránh spam | |
| 5 | Có cần **duyệt nội dung** trước khi gửi? | ☐ Admin duyệt ☐ Không cần | |
| 6 | Có cần **tracking mở tin/click**? | Để đo hiệu quả | |

---

#### 8.3. Khảo sát mức độ hài lòng 🟡

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 1 | **Thời điểm gửi khảo sát**? | ☐ Sau mua ☐ Sau CSKH ☐ Sau bảo hành | |
| 2 | **Nội dung khảo sát** gồm những gì? | Có template sẵn không? | |
| 3 | **Kênh gửi** khảo sát? | ☐ Link form ☐ Zalo ☐ Email | |
| 4 | Có cần **đánh giá NV** không? | 1-5 sao? | |
| 5 | **Xử lý feedback tiêu cực** thế nào? | ☐ Tự động escalate ☐ Thông báo quản lý | |

---

#### 8.4. Tích điểm / Loyalty 🔴

> **Quan trọng:** Cần làm rõ để thiết kế cơ chế tích điểm từ đầu

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 1 | **Công thức tích điểm**? | X điểm = Y đồng? Theo SP? Theo nguồn? | |
| 2 | **Các hạng thành viên**? | VD: Thường, Bạc, Vàng, Kim cương? | |
| 3 | **Điều kiện lên hạng**? | Theo điểm? Theo doanh số? | |
| 4 | **Quyền lợi từng hạng**? | Chiết khấu? Quà tặng? Ưu tiên? | |
| 5 | **Điểm có hết hạn** không? | Sau bao lâu? | |
| 6 | **Quy đổi điểm** thành gì? | ☐ Voucher ☐ Giảm giá trực tiếp ☐ Quà | |
| 7 | **Tỷ lệ quy đổi**? | X điểm = Y đồng voucher? | |
| 8 | Điểm có **chuyển nhượng** được không? | Cho người khác? | |
| 9 | **Cộng điểm tự động** hay thủ công? | Sau khi hoàn thành đơn? | |
| 10 | Có **lịch sử điểm** cho KH xem không? | ☐ App ☐ Website ☐ CRM | |

---

#### 8.5. Tích hợp kênh giao tiếp 🟠

| # | Câu hỏi | Ghi chú | Trả lời |
|---|---------|---------|---------|
| 1 | **Zalo OA** đã có chưa? | Cần để tích hợp | |
| 2 | **Loại Zalo OA**? | ☐ OA thường ☐ OA đăng ký doanh nghiệp | |
| 3 | **Messenger/Facebook Page** đã có? | | |
| 4 | Cần **chat 2 chiều** trong CRM không? | Hay chỉ gửi 1 chiều? | |
| 5 | **Ai được quyền** chat với KH? | ☐ NV phụ trách ☐ Tất cả | |
| 6 | Cần **template tin nhắn** chuẩn không? | VD: Chào hỏi, Xác nhận đơn... | |

---

## Ghi chú từ buổi họp

<!-- Ghi chú thêm các thông tin quan trọng từ buổi kickoff -->

---

## Cấu trúc thư mục

```
docs/kickoff/
├── KICKOFF_QUESTIONS.md      # File này - Tổng hợp
├── KICKOFF_SLIDE_DECK.md     # Slide deck
├── ONE_PAGER.md              # One pager
├── TALKING_POINTS.md         # Talking points
├── CONTACT_POINTS.md         # Đầu mối liên hệ
└── questions/                # Chi tiết câu hỏi theo module
    ├── CLARIFICATION_QUESTIONS.md  # 📋 FILE CHÍNH - Tổng hợp 60+ câu hỏi
    ├── FITTING_QUESTIONS.md        # ⛳ Fitting Golf (17 câu)
    ├── COACHING_QUESTIONS.md       # 🏌️ Coaching Golf (27 câu)
    ├── SHIPPING_QUESTIONS.md       # 🚚 Vận chuyển (35 câu)
    └── BRAVO_QUESTIONS.md          # 🔄 Bravo integration (30 câu)
```

---

*Cập nhật: 2025-12-10*
