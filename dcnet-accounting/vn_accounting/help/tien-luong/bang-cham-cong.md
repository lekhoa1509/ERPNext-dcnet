---
title: Bảng chấm công
order: 1
summary: Ghi nhận ngày công, ca làm và tình trạng đi làm của nhân viên — đầu vào để tính lương.
---

## Mục đích

**Bảng chấm công** ghi nhận tình trạng đi làm của từng nhân viên theo từng ngày: Có mặt, Vắng, Nửa ngày, Nghỉ phép, hoặc Làm việc từ xa. Số ngày công này là đầu vào để Bảng lương tính ra số tiền lương theo số ngày làm thực tế. Đây là dữ liệu nhân sự — **không** tạo bút toán kế toán.

## Khi nào dùng

- Hằng ngày hoặc cuối tháng: ghi nhận công cho nhân viên trước khi chạy lương.
- Khi nhân viên nghỉ phép, nghỉ không lương, đi muộn/về sớm — đánh dấu để trừ công.
- Khi cần đối chiếu số ngày công thực tế trước khi duyệt Bảng lương.

## Cách thực hiện

1. Bấm **Bảng chấm công** trên menu Tiền lương → danh sách bản ghi chấm công mở ra.
2. Bấm **+ Thêm** để tạo bản ghi cho một nhân viên/một ngày: chọn **Nhân viên**, **Ngày**, **Trạng thái** (Có mặt / Vắng / Nửa ngày / Làm từ xa), gắn **Ca làm** nếu có.
3. Để chấm công hàng loạt nhiều nhân viên/nhiều ngày, dùng công cụ chấm công nhanh (Đánh dấu công) nếu có, hoặc nhập từng dòng.
4. Bấm **Lưu** rồi **Duyệt** để chốt bản ghi.

## Định khoản tự động

Bảng chấm công **không tự định khoản** — chỉ ghi nhận dữ liệu công. Số ngày công ảnh hưởng gián tiếp tới số tiền lương khi Bảng lương tính theo "số ngày làm việc / tổng số ngày công chuẩn".

## Tình huống đặc biệt & cảnh báo

- **Nghỉ không lương (LWP)** làm giảm số ngày được trả lương → số tiền lương trên Phiếu lương giảm tương ứng nếu thành phần lương có thiết lập "phụ thuộc số ngày công".
- **Chấm công trùng:** mỗi nhân viên chỉ có 1 bản ghi cho 1 ngày — hệ thống chặn trùng ngày.
- **Ngày lễ/cuối tuần** được xác định theo Lịch nghỉ lễ gán cho nhân viên — kiểm tra Lịch nghỉ lễ đã đúng trước khi tính lương.
- **Chấm công sau khi đã chạy lương:** nếu sửa chấm công sau khi Bảng lương đã tạo phiếu lương, phải tính lại Bảng lương để số liệu phản ánh đúng.

## Báo cáo liên quan

- [Bảng lương](bang-luong.md): dùng số ngày công để tính tiền lương.
- [Phiếu lương](phieu-luong.md): hiển thị số ngày được trả lương của từng người.

## FAQ

**Q: Chấm công có sinh bút toán không?**
**A:** Không. Đây là dữ liệu nhân sự. Bút toán chi phí lương chỉ phát sinh khi duyệt Bảng lương.

**Q: Nhân viên nghỉ phép có lương thì chấm thế nào?**
**A:** Đánh dấu Trạng thái "Nghỉ phép" (On Leave) với loại phép có lương — ngày đó vẫn được tính lương; nếu là nghỉ không lương thì bị trừ.

**Q: Quên chấm công một ngày, phát hiện sau khi chạy lương?**
**A:** Thêm bản ghi chấm công còn thiếu, sau đó tính lại Bảng lương của kỳ đó để cập nhật số ngày công.
