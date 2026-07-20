# Đặc tả Use Cases - Module Quản lý Coaching

**Dự án:** DCNET Flow - Nhật Minh Sports
**Module:** Coaching Management (Huấn luyện Golf)
**Phiên bản:** 1.0
**Nguồn:** FEATURE_SPECIFICATION.md (Section 5.2.3, 5.4, 14.2)
**Ngày:** 10/01/2026

---

## 1. Định nghĩa Coaching

> **Định nghĩa:**
>
> Coaching là dịch vụ huấn luyện golf cho học viên, bao gồm đánh giá trình độ, đăng ký gói học, theo dõi tiến trình từng buổi, và đánh giá kết quả.

**Đặc điểm:**
- Dịch vụ nhiều buổi (khóa học)
- Có bài test đầu vào
- Tracking tiến trình theo từng buổi
- Đánh giá định kỳ (đầu - giữa - cuối)
- Thông báo tự động qua Zalo/Email

---

## 2. Danh sách Actors và Vai trò

### 2.1. Học viên (Customer)

**Mô tả:** Khách hàng đăng ký học golf

**Hành động:**
- Đăng ký coaching qua Website/Điện thoại/Tại cửa hàng
- Làm bài test đầu vào
- Chọn gói học
- Thanh toán
- Tham gia buổi học
- Nhận thông báo lịch học

---

### 2.2. NV Tư vấn (Sale)

**Mô tả:** Nhân viên tư vấn và bán gói coaching

**Quyền hạn:**
- Tạo đơn Coaching
- Tư vấn gói học
- Tạo Order (đơn hàng)
- Xếp lịch học
- Xem danh sách đơn Coaching

**Giới hạn:**
- Không được điểm danh
- Không được nhập tiến trình buổi học

---

### 2.3. HLV (Coach)

**Mô tả:** Huấn luyện viên thực hiện buổi học

**Quyền hạn:**
- Thực hiện bài test đầu vào
- Nhập kết quả test
- Điểm danh buổi học
- Ghi nhận nội dung buổi học
- Ghi nhận tiến trình học viên
- Đánh giá định kỳ

**Giới hạn:**
- Chỉ thao tác với đơn được phân công

---

### 2.4. Manager

**Mô tả:** Quản lý coaching

**Quyền hạn:**
- Tất cả quyền của NV Tư vấn và HLV
- Phân công HLV
- Hủy đơn Coaching
- Xem báo cáo tổng hợp

---

### 2.5. Admin

**Mô tả:** Quản trị viên hệ thống

**Quyền hạn:**
- Toàn quyền
- Quản lý gói huấn luyện
- Quản lý HLV
- Quản lý sân tập
- Cấu hình hệ thống

---

### 2.6. System (Tự động)

**Mô tả:** Hệ thống tự động thực hiện các tác vụ

**Chức năng:**
- Tạo mã đơn Coaching tự động
- Gửi thông báo tự động (Zalo/Email)
- Cập nhật trạng thái khi hoàn thành buổi
- Ghi log hoạt động

---

## 3. Ma trận Phân quyền

| Use Case | NV Tư vấn | HLV | Manager | Admin | System |
|----------|-----------|-----|---------|-------|--------|
| **UC-01: Tạo đơn Coaching** | ✓ | - | ✓ | ✓ | - |
| **UC-02: Xem danh sách đơn Coaching** | ✓ | ✓ (của mình) | ✓ (tất cả) | ✓ | - |
| **UC-03: Thực hiện test đầu vào** | - | ✓ | ✓ | ✓ | - |
| **UC-04: Nhập kết quả test** | - | ✓ | ✓ | ✓ | - |
| **UC-05: Tư vấn gói học** | ✓ | - | ✓ | ✓ | - |
| **UC-06: Đăng ký gói & Tạo Order** | ✓ | - | ✓ | ✓ | - |
| **UC-07: Xếp lịch học** | ✓ | - | ✓ | ✓ | - |
| **UC-08: Điểm danh buổi học** | - | ✓ | ✓ | ✓ | - |
| **UC-09: Ghi nhận tiến trình** | - | ✓ | ✓ | ✓ | - |
| **UC-10: Đánh giá định kỳ** | - | ✓ | ✓ | ✓ | - |
| **UC-11: Tạm dừng khóa học** | ✓ | ✓ | ✓ | ✓ | - |
| **UC-12: Hoàn thành khóa học** | - | - | - | - | ✓ |
| **UC-13: Hủy đơn Coaching** | - | - | ✓ | ✓ | - |
| **UC-14: Gửi thông báo tự động** | - | - | - | - | ✓ |
| **UC-15: Xem báo cáo Coaching** | - | ✓ (của mình) | ✓ | ✓ | - |
| **UC-16: Quản lý gói huấn luyện** | - | - | - | ✓ | - |
| **UC-17: Quản lý HLV** | - | - | ✓ | ✓ | - |
| **UC-18: Quản lý sân tập** | - | - | - | ✓ | - |

**Chú thích:**
- ✓ = Có quyền thực hiện
- ✓ (của mình) = Chỉ thực hiện trên đơn được phân công
- ✓ (tất cả) = Thực hiện trên tất cả đơn
- - = Không có quyền

---

## 4. Chi tiết Use Cases

### UC-01: Tạo đơn Coaching mới

**ID:** UC-01
**Tên:** Tạo đơn Coaching mới
**Actors:** NV Tư vấn, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3

**Mô tả:**
Tạo đơn coaching mới khi học viên đăng ký học golf.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Khách hàng đã tồn tại hoặc sẽ được tạo mới

**Main Flow:**
1. User chọn "Tạo đơn Coaching"
2. Hệ thống hiển thị form nhập thông tin
3. User nhập **Thông tin học viên:**
   - Chọn khách hàng (hoặc tạo mới)
   - Thông tin cá nhân
   - Trình độ hiện tại
   - Mục tiêu học
4. User nhập **Thông tin đơn:**
   - Nguồn đăng ký (Website/Cửa hàng/Điện thoại)
   - Chi nhánh
   - Ghi chú
5. User submit form
6. Hệ thống tạo đơn Coaching với:
   - Mã tự động: COACH-YYYYMMDD-XXX
   - Trạng thái: "Mới"

**Postcondition:**
- Đơn Coaching mới được tạo
- Trạng thái = "Mới"

**Business Rules:**
- Mã đơn tự động sinh theo format COACH-YYYYMMDD-XXX

---

### UC-02: Xem danh sách đơn Coaching

**ID:** UC-02
**Tên:** Xem danh sách đơn Coaching
**Actors:** NV Tư vấn, HLV, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1

**Mô tả:**
Hiển thị danh sách đơn Coaching theo quyền hạn.

**Precondition:**
- User đã đăng nhập vào hệ thống

**Main Flow:**
1. User truy cập "Danh sách đơn Coaching"
2. Hệ thống hiển thị danh sách theo quyền:
   - **HLV:** Chỉ thấy đơn được phân công
   - **NV Tư vấn:** Thấy đơn mình tạo
   - **Manager/Admin:** Thấy tất cả
3. Hệ thống hiển thị các cột:
   - Mã đơn
   - Học viên
   - Gói học
   - HLV
   - Trạng thái
   - Tiến độ (x/y buổi)
   - Ngày bắt đầu
   - Tổng học phí

**Search/Filter:**
- Tìm theo: Mã đơn, Tên học viên
- Lọc theo: Trạng thái, HLV, Chi nhánh, Thời gian

**Postcondition:**
- Danh sách được hiển thị theo quyền hạn

---

### UC-03: Thực hiện test đầu vào

**ID:** UC-03
**Tên:** Thực hiện test đầu vào
**Actors:** HLV, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3 - "bài test đầu vào"

**Mô tả:**
HLV thực hiện bài test đánh giá trình độ học viên.

**Precondition:**
- Đơn Coaching tồn tại với trạng thái "Mới"
- HLV đã được chỉ định

**Main Flow:**
1. HLV mở chi tiết đơn Coaching
2. HLV chọn "Thực hiện test đầu vào"
3. HLV thực hiện các bài test:
   - Đánh giá swing
   - Đánh giá putting
   - Đánh giá short game
   - Đánh giá khác
4. HLV nhập kết quả (UC-04)

**Postcondition:**
- Bài test được thực hiện
- Chuyển sang UC-04 để nhập kết quả

---

### UC-04: Nhập kết quả test

**ID:** UC-04
**Tên:** Nhập kết quả test
**Actors:** HLV, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3

**Mô tả:**
Nhập kết quả bài test đầu vào và thông số kỹ thuật.

**Precondition:**
- Đã thực hiện bài test (UC-03)

**Main Flow:**
1. HLV mở form nhập kết quả test
2. HLV nhập **Kết quả đánh giá:**
   - Trình độ hiện tại (Beginner/Intermediate/Advanced)
   - Điểm mạnh
   - Điểm cần cải thiện
   - Đề xuất gói phù hợp
3. HLV nhập **Thông số kỹ thuật:** (tương tự Fitting)
   - Chiều cao, Cân nặng
   - Size tay
   - Cấp độ
   - Tốc độ đầu gậy, Tốc độ bóng
   - Hình swing
   - Đường bóng, Đường cao bóng
   - Khoảng cách gậy sắt/driver
   - Tình trạng bộ gậy
   - Nhu cầu riêng
4. HLV submit
5. Hệ thống cập nhật trạng thái: "Mới" → "Đã test"

**Postcondition:**
- Kết quả test được lưu
- Thông số kỹ thuật được lưu
- Trạng thái = "Đã test"

---

### UC-05: Tư vấn gói học

**ID:** UC-05
**Tên:** Tư vấn gói học
**Actors:** NV Tư vấn, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3 - "Gói huấn luyện đăng ký"

**Mô tả:**
Tư vấn gói học phù hợp dựa trên kết quả test.

**Precondition:**
- Đơn có trạng thái "Đã test"
- Có kết quả và đề xuất từ HLV

**Main Flow:**
1. NV xem kết quả test và đề xuất
2. NV tư vấn gói học cho khách:
   - Gói cơ bản (VD: 8 buổi)
   - Gói nâng cao (VD: 12 buổi)
   - Gói thi đấu
3. NV giới thiệu:
   - HLV phù hợp
   - Sân tập
   - Lịch học dự kiến
   - Học phí và ưu đãi
4. NV ghi nhận kết quả tư vấn
5. Hệ thống cập nhật trạng thái: "Đã test" → "Đã tư vấn"

**Postcondition:**
- Thông tin tư vấn được lưu
- Trạng thái = "Đã tư vấn"

---

### UC-06: Đăng ký gói & Tạo Order

**ID:** UC-06
**Tên:** Đăng ký gói & Tạo Order
**Actors:** NV Tư vấn, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3

**Mô tả:**
Đăng ký gói học và tạo đơn hàng thanh toán.

**Precondition:**
- Đơn có trạng thái "Đã tư vấn"
- Học viên đồng ý đăng ký

**Main Flow:**
1. NV chọn "Đăng ký gói học"
2. NV nhập thông tin:
   - **Gói huấn luyện:** (8 buổi cơ bản, 12 buổi nâng cao...)
   - **HLV phụ trách**
   - **Sân tập**
   - **Loại khóa học:** (Cá nhân/Nhóm)
   - **Tổng học phí**
   - **Ưu đãi** (nếu có)
   - **Mục tiêu học**
3. NV tạo Order:
   - Chọn phương thức thanh toán
   - Ghi nhận thanh toán (toàn bộ/đặt cọc)
4. Hệ thống:
   - Tạo Order liên kết với đơn Coaching
   - Cập nhật trạng thái: "Đã tư vấn" → "Đã thanh toán"

**Postcondition:**
- Gói học được đăng ký
- Order được tạo
- Trạng thái = "Đã thanh toán"

---

### UC-07: Xếp lịch học

**ID:** UC-07
**Tên:** Xếp lịch học
**Actors:** NV Tư vấn, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3 - "Tạo lịch coaching"

**Mô tả:**
Xếp lịch các buổi học trong khóa.

**Precondition:**
- Đơn có trạng thái "Đã thanh toán"
- Đã có HLV và sân tập

**Main Flow:**
1. NV chọn "Xếp lịch học"
2. Hệ thống hiển thị calendar
3. NV tạo các buổi học (Sessions):
   - Ngày giờ từng buổi
   - HLV (có thể khác mặc định)
   - Sân tập
4. Hệ thống kiểm tra:
   - Conflict lịch HLV
   - Conflict sân tập
5. NV xác nhận lịch
6. Hệ thống:
   - Tạo các Sessions với status "scheduled"
   - Gửi thông báo lịch cho học viên (Zalo/Email)

**Postcondition:**
- Các buổi học được tạo
- Học viên nhận thông báo lịch

---

### UC-08: Điểm danh buổi học

**ID:** UC-08
**Tên:** Điểm danh buổi học
**Actors:** HLV, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.4 - "Lịch học & điểm danh"

**Mô tả:**
Điểm danh học viên cho từng buổi học.

**Precondition:**
- Đơn có trạng thái "Đang học"
- Buổi học theo lịch

**Main Flow:**
1. HLV mở buổi học cần điểm danh
2. HLV chọn trạng thái:
   - **Completed:** Học viên có mặt
   - **Absent:** Vắng không báo
   - **Cancelled:** Vắng có báo trước
3. HLV submit
4. Hệ thống cập nhật:
   - Nếu Completed: `completed_sessions += 1`
   - Ghi log điểm danh

**Alternative Flow:**
- 2a. Nếu là buổi đầu tiên:
  - Hệ thống chuyển trạng thái đơn: "Đã thanh toán" → "Đang học"

**Postcondition:**
- Điểm danh được ghi nhận
- completed_sessions được cập nhật

---

### UC-09: Ghi nhận tiến trình

**ID:** UC-09
**Tên:** Ghi nhận tiến trình buổi học
**Actors:** HLV, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.4 - "Nội dung từng buổi học", "Tiến độ học tập"

**Mô tả:**
Ghi nhận nội dung và tiến trình sau mỗi buổi học.

**Precondition:**
- Buổi học có trạng thái "Completed"

**Main Flow:**
1. HLV mở buổi học đã hoàn thành
2. HLV nhập:
   - **Nội dung buổi học:** Những gì đã dạy
   - **Tiến trình:** Đánh giá kỹ năng (swing, putting...)
   - **Nhận xét:** Nhận xét chuyên môn
   - **Bài tập về nhà:** Bài tập cho học viên
3. HLV submit
4. Hệ thống lưu thông tin

**Postcondition:**
- Tiến trình buổi học được lưu
- Lịch sử được ghi nhận

---

### UC-10: Đánh giá định kỳ

**ID:** UC-10
**Tên:** Đánh giá định kỳ
**Actors:** HLV, Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.4 - "Đánh giá định kỳ: Đầu - giữa - cuối kỳ"

**Mô tả:**
Thực hiện đánh giá định kỳ: Đầu kỳ, Giữa kỳ, Cuối kỳ.

**Precondition:**
- Đơn có trạng thái "Đang học"
- Đến mốc đánh giá

**Main Flow:**
1. HLV chọn "Đánh giá định kỳ"
2. HLV chọn loại đánh giá:
   - Đầu kỳ (sau test)
   - Giữa kỳ (50% khóa)
   - Cuối kỳ (kết thúc)
3. HLV đánh giá từng kỹ năng:
   - Swing
   - Putting
   - Chipping
   - Driving
   - Course Management
4. HLV nhập nhận xét tổng quan
5. HLV submit

**Postcondition:**
- Đánh giá định kỳ được lưu
- Có thể so sánh tiến bộ qua các kỳ

---

### UC-11: Tạm dừng khóa học

**ID:** UC-11
**Tên:** Tạm dừng khóa học
**Actors:** NV Tư vấn, HLV, Manager, Admin

**Mô tả:**
Tạm dừng khóa học khi học viên có lý do.

**Precondition:**
- Đơn có trạng thái "Đang học"

**Main Flow:**
1. User chọn "Tạm dừng khóa học"
2. User nhập:
   - Lý do tạm dừng
   - Ngày dự kiến học lại
3. User submit
4. Hệ thống:
   - Cập nhật trạng thái: "Đang học" → "Tạm dừng"
   - Ghi lại số buổi đã học/còn lại
   - Thông báo cho học viên

**Postcondition:**
- Trạng thái = "Tạm dừng"
- Thông tin tạm dừng được lưu

---

### UC-12: Hoàn thành khóa học

**ID:** UC-12
**Tên:** Hoàn thành khóa học (Tự động)
**Actors:** System

**Mô tả:**
Hệ thống tự động chuyển trạng thái khi học viên hoàn thành tất cả buổi học.

**Precondition:**
- Đơn có trạng thái "Đang học"
- `completed_sessions == total_sessions`

**Main Flow:**
1. System kiểm tra sau mỗi lần điểm danh
2. Nếu `completed_sessions == total_sessions`:
   - Cập nhật trạng thái: "Đang học" → "Hoàn thành"
   - Gửi thông báo cho học viên và HLV
   - Trigger đánh giá cuối kỳ

**Postcondition:**
- Trạng thái = "Hoàn thành"
- Thông báo được gửi

---

### UC-13: Hủy đơn Coaching

**ID:** UC-13
**Tên:** Hủy đơn Coaching
**Actors:** Manager, Admin

**Mô tả:**
Hủy đơn Coaching (chỉ khi chưa bắt đầu học).

**Precondition:**
- Đơn có trạng thái: Mới, Đã test, Đã tư vấn, hoặc Tạm dừng
- Không thể hủy khi đang học

**Main Flow:**
1. Manager chọn "Hủy đơn"
2. Hệ thống kiểm tra trạng thái hợp lệ
3. Manager nhập lý do hủy
4. Hệ thống:
   - Cập nhật trạng thái → "Hủy"
   - Xử lý hoàn tiền nếu cần
   - Ghi log

**Postcondition:**
- Trạng thái = "Hủy"
- Lý do hủy được lưu

---

### UC-14: Gửi thông báo tự động

**ID:** UC-14
**Tên:** Gửi thông báo tự động
**Actors:** System
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.4 - "CRM gửi lịch học, thay đổi giờ học, lịch thi đấu qua Zalo/Email"

**Mô tả:**
Hệ thống tự động gửi thông báo qua Zalo/Email.

**Trigger:**
- 1 ngày trước buổi học → Nhắc lịch
- Thay đổi lịch → Thông báo thay đổi
- Vắng mặt → Nhắc học bù
- Hoàn thành khóa → Đánh giá + đề xuất

**Main Flow:**
1. System phát hiện trigger event
2. System tạo nội dung thông báo
3. System gửi qua kênh đã cấu hình:
   - Zalo OA
   - Email
4. System ghi log gửi thông báo

**Postcondition:**
- Thông báo được gửi
- Log được ghi

---

### UC-15: Xem báo cáo Coaching

**ID:** UC-15
**Tên:** Xem báo cáo Coaching
**Actors:** HLV (của mình), Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 14.2

**Mô tả:**
Xem báo cáo doanh thu và hiệu suất coaching.

**Báo cáo từ spec:**
1. Doanh thu từ coaching (doanh thu đào tạo)
2. Doanh thu phát sinh sau coaching (doanh thu sản phẩm)
3. Số lượng học viên tham gia coaching
4. Số lượng HLV tham gia coaching và doanh số theo từng HLV

**Main Flow:**
1. User truy cập "Báo cáo Coaching"
2. User chọn loại báo cáo
3. User chọn khoảng thời gian
4. Hệ thống hiển thị báo cáo

**Postcondition:**
- Báo cáo được hiển thị

---

### UC-16: Quản lý gói huấn luyện

**ID:** UC-16
**Tên:** Quản lý gói huấn luyện
**Actors:** Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3 - "Gói huấn luyện đăng ký"

**Mô tả:**
CRUD gói huấn luyện (8 buổi cơ bản, 12 buổi nâng cao, Thi đấu...)

**Main Flow:**
1. Admin truy cập "Quản lý gói huấn luyện"
2. Admin có thể:
   - Xem danh sách gói
   - Tạo gói mới (tên, số buổi, giá, mô tả)
   - Cập nhật gói
   - Ẩn/hiện gói

**Postcondition:**
- Gói huấn luyện được quản lý

---

### UC-17: Quản lý HLV

**ID:** UC-17
**Tên:** Quản lý HLV
**Actors:** Manager, Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3 - "HLV phụ trách"

**Mô tả:**
Quản lý danh sách Huấn luyện viên.

**Main Flow:**
1. User truy cập "Quản lý HLV"
2. User có thể:
   - Xem danh sách HLV
   - Thêm HLV mới (link với Employee)
   - Cập nhật thông tin (chứng chỉ, kinh nghiệm, chuyên môn)
   - Xem lịch dạy
   - Xem doanh số

**Postcondition:**
- HLV được quản lý

---

### UC-18: Quản lý sân tập

**ID:** UC-18
**Tên:** Quản lý sân tập
**Actors:** Admin
**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3 - "Địa điểm học: sân tập"

**Mô tả:**
Quản lý danh sách sân tập golf.

**Main Flow:**
1. Admin truy cập "Quản lý sân tập"
2. Admin có thể:
   - Xem danh sách sân tập
   - Thêm sân tập mới (tên, địa chỉ, số lane, liên hệ)
   - Cập nhật thông tin
   - Đánh dấu sân đối tác

**Postcondition:**
- Sân tập được quản lý

---

## 5. Use Case Diagram (Text)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      «System» Coaching Management                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────┐                                         │
│  │ UC-01: Tạo đơn Coaching        │◄──────────────────────┐                 │
│  └────────────────────────────────┘                       │                 │
│                                                            │                 │
│  ┌────────────────────────────────┐                       │                 │
│  │ UC-02: Xem danh sách đơn       │◄──────────────────────┼────────────────┤
│  └────────────────────────────────┘                       │                │
│                                                            │                │
│  ┌────────────────────────────────┐                       │                │
│  │ UC-03: Thực hiện test          │◄───────┐              │                │
│  └────────────────────────────────┘        │              │                │
│              │                              │              │                │
│              │ «include»                    │              │                │
│              ▼                              │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-04: Nhập kết quả test       │◄───────┤              │                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-05: Tư vấn gói học          │◄───────┼──────────────┤                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-06: Đăng ký & Tạo Order     │◄───────┼──────────────┤                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-07: Xếp lịch học            │◄───────┼──────────────┤                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-08: Điểm danh buổi học      │◄───────┤              │                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-09: Ghi nhận tiến trình     │◄───────┤              │                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-10: Đánh giá định kỳ        │◄───────┤              │                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
│  ┌────────────────────────────────┐        │              │                │
│  │ UC-15: Xem báo cáo             │◄───────┤              │                │
│  └────────────────────────────────┘        │              │                │
│                                             │              │                │
└─────────────────────────────────────────────┼──────────────┼────────────────┘
                                              │              │
                                              │              │
            ┌───────────┐                     │              │
            │   HLV     │─────────────────────┘              │
            └───────────┘                                    │
                  │                                          │
            ┌─────────────┐                            ┌─────────────┐
            │ NV Tư vấn   │────────────────────────────┤   Manager   │
            └─────────────┘                            └─────────────┘
                                                             │
                                                       ┌───────────┐
                                                       │   Admin   │
                                                       └───────────┘
```

---

## 6. Tham khảo

**Tài liệu liên quan:**
- [FEATURE_SPECIFICATION.md](../../feature/FEATURE_SPECIFICATION.md) - Đặc tả chức năng gốc (Section 5.2.3, 5.4, 14.2)
- [COACHING_WORKFLOW.md](./COACHING_WORKFLOW.md) - Workflow và ERD
- [COACHING_DIAGRAMS.md](./COACHING_DIAGRAMS.md) - Tổng hợp Diagrams
- [COACHING_STATUS.md](./COACHING_STATUS.md) - Status Workflow

---

## 7. Ghi chú quan trọng

1. **Thông số kỹ thuật:** Tương tự Fitting, cần thu thập 14+ thông số

2. **Đánh giá định kỳ:** 3 mốc - Đầu kỳ, Giữa kỳ, Cuối kỳ

3. **Thông báo tự động:** Qua Zalo/Email cho lịch học, thay đổi, nhắc nhở

4. **Báo cáo:** 4 loại từ spec
   - Doanh thu đào tạo
   - Doanh thu SP phát sinh
   - Số học viên
   - Doanh số theo HLV

5. **Tracking 2 cấp:**
   - **Cấp khóa học:** Trạng thái đơn Coaching (8 trạng thái)
   - **Cấp buổi học:** Trạng thái Session (scheduled/completed/absent/cancelled)

---

**Ngày cập nhật:** 10/01/2026
**Người soạn:** DCNET Development Team
**Nguồn:** FEATURE_SPECIFICATION.md v1.0 (Section 5.2.3, 5.4, 14.2)
