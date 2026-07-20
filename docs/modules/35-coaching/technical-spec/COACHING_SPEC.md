# Module Coaching - Đặc tả theo Nhật Minh

> **Nguồn:** `docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.3, 5.4, 14.2
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Bàn giao đợt 1
> **Lưu ý:** File này chỉ ghi lại ĐÚNG những gì có trong spec gốc

---

## Định nghĩa

> Đơn Coaching là dịch vụ huấn luyện golf cho học viên, bao gồm quản lý gói học, HLV, lịch học, và theo dõi tiến trình.

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1 - Loại đơn hàng

---

## Tạo đơn hàng Coaching

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.3 (Line 452-466)

### Thông tin đơn Coaching:

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

### Thông tin kỹ thuật (tương tự Fitting):

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.2 (Line 435-450)

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

---

## Xem chi tiết đơn Coaching

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.4 (Line 509-516)

- **Lịch học & điểm danh:** Lịch từng buổi, tình trạng học
- **Nội dung từng buổi học**
- **Tiến độ học tập:** Tổng quan kỹ năng, vd: kỹ năng (swing, putting,...)
- **Thông báo & Nhắc lịch tự động:** CRM gửi lịch học, thay đổi giờ học, lịch thi đấu qua Zalo/Email
- **Phân tích kỹ thuật:** nhận xét chuyên môn, lưu trữ theo thời gian
- **Đánh giá định kỳ:** Đầu - giữa - cuối kỳ
- **Lịch sử tương tác & hỗ trợ học viên:** Ghi chú các buổi tư vấn, hẹn thêm giờ, phản hồi từ học viên

---

## Cập nhật đơn Coaching

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.5 (Line 530)

- Cập nhật đơn Coaching

---

## Báo cáo Coaching

**Nguồn:** FEATURE_SPECIFICATION.md Section 14.2 (Line 899-903)

| # | Báo cáo | Mô tả |
|---|---------|-------|
| 1 | Doanh thu từ coaching | Doanh thu đào tạo |
| 2 | Doanh thu phát sinh sau coaching | Doanh thu sản phẩm |
| 3 | Số lượng học viên tham gia coaching | Đếm học viên |
| 4 | Số lượng HLV tham gia coaching | Doanh số theo từng HLV |

---

## Tổng hợp chức năng Module Coaching

| STT | Chức năng | Mô tả | Nguồn |
|-----|-----------|-------|-------|
| 1 | Tạo đơn Coaching | Hồ sơ học viên, gói, HLV, lịch, học phí | 5.2.3 |
| 2 | Nhập thông số kỹ thuật | Tương tự Fitting (14+ thông số) | 5.2.3 |
| 3 | Xem chi tiết đơn Coaching | Lịch học, điểm danh, tiến độ | 5.4 |
| 4 | Lịch học & điểm danh | Lịch từng buổi, tình trạng học | 5.4 |
| 5 | Tiến độ học tập | Tổng quan kỹ năng (swing, putting...) | 5.4 |
| 6 | Thông báo & Nhắc lịch | Tự động qua Zalo/Email | 5.4 |
| 7 | Phân tích kỹ thuật | Nhận xét chuyên môn, lưu trữ | 5.4 |
| 8 | Đánh giá định kỳ | Đầu - giữa - cuối kỳ | 5.4 |
| 9 | Lịch sử tương tác | Ghi chú tư vấn, phản hồi học viên | 5.4 |
| 10 | Cập nhật đơn Coaching | Cập nhật thông tin đơn | 5.5 |
| 11 | Báo cáo doanh thu | Doanh thu đào tạo + SP phát sinh | 14.2 |
| 12 | Báo cáo HLV | Số lượng HLV, doanh số theo HLV | 14.2 |

---

## So sánh với Fitting

| Tiêu chí | Fitting | Coaching |
|----------|---------|----------|
| **Thời gian** | 1 buổi | Nhiều buổi (khóa học) |
| **Người thực hiện** | NV Fitting | HLV |
| **Output** | Thông số kỹ thuật | Kỹ năng chơi golf |
| **Thông số KT** | ✅ Có | ✅ Có (tương tự Fitting) |
| **Tracking** | 1 lần | Nhiều buổi + tiến trình |
| **Đánh giá** | Không | Định kỳ (đầu-giữa-cuối) |

---

**Nguồn:** `docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.3, 5.4, 14.2
**Lưu ý:** Đây là spec GỐC từ Nhật Minh (PHỤ LỤC hợp đồng)
**Ngày cập nhật:** 10/01/2026
