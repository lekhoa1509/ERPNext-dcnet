---
title: Gán Cơ cấu lương
order: 7
summary: Gán một cơ cấu lương và mức lương gốc cho từng nhân viên kèm ngày hiệu lực và tài khoản phải trả lương.
---

## Mục đích

**Gán Cơ cấu lương** liên kết một nhân viên với một [Cơ cấu lương](co-cau-luong.md), kèm **mức lương gốc** và **ngày bắt đầu hiệu lực**. Đây là bước bắt buộc để nhân viên xuất hiện trong Bảng lương và được tính lương. Bản gán cũng khai **Tài khoản phải trả lương** (TK 334) dùng khi hạch toán.

## Khi nào dùng

- Khi tuyển nhân viên mới: gán cơ cấu lương + mức lương.
- Khi nhân viên được điều chỉnh lương: tạo bản gán mới với ngày hiệu lực mới.
- Trước khi chạy Bảng lương lần đầu cho một nhân viên.

## Cách thực hiện

1. Bấm **Gán Cơ cấu lương** → bấm **+ Thêm**.
2. Chọn **Nhân viên**, **Cơ cấu lương**, **Công ty**.
3. Nhập **Ngày bắt đầu** (hiệu lực từ), **Mức lương gốc**.
4. Khai **Tài khoản phải trả lương** (TK 334) — nếu để trống sẽ lấy TK phải trả lương mặc định của công ty.
5. Bấm **Lưu** → **Duyệt**.

## Định khoản tự động

Gán Cơ cấu lương **không tự định khoản** — chỉ cấu hình. Tuy nhiên **Tài khoản phải trả lương** khai ở đây được dùng làm vế Có TK 334 khi [Bảng lương](bang-luong.md) hạch toán. Nếu TK này khai sai loại (không phải loại "Phải trả"), Bảng lương sẽ bị chặn duyệt.

## Tình huống đặc biệt & cảnh báo

- **Một bản gán hiệu lực tại một thời điểm.** Tránh nhiều bản gán chồng kỳ cho cùng nhân viên — Bảng lương sẽ khó xác định cơ cấu nào áp dụng.
- **Tăng lương = bản gán mới.** Không sửa bản gán cũ; tạo bản mới với ngày hiệu lực để giữ lịch sử.
- **TK phải trả lương phải là loại "Phải trả".** Đây là điều kiện chặn ở Bảng lương — kiểm tra TK 334 đã đúng loại tài khoản.
- **Nhân viên không vào được Bảng lương:** kiểm tra đã có bản Gán Cơ cấu lương duyệt và hiệu lực trong kỳ tính lương.

## Báo cáo liên quan

- [Cơ cấu lương](co-cau-luong.md): khuôn mẫu được gán.
- [Bảng lương](bang-luong.md): dùng bản gán để tính lương và lấy TK phải trả lương.

## FAQ

**Q: Vì sao nhân viên không hiện trong Bảng lương dù đã chấm công?**
**A:** Vì chưa có Gán Cơ cấu lương duyệt và hiệu lực trong kỳ. Chấm công không thay cho gán cơ cấu.

**Q: Mức lương gốc khai ở đây dùng làm gì?**
**A:** Là cơ sở để các công thức trong cơ cấu tính ra từng thành phần (ví dụ phụ cấp = % lương gốc).

**Q: Tài khoản phải trả lương khác nhau theo nhân viên được không?**
**A:** Được, nhưng thông thường dùng chung TK 334. Nếu để trống, hệ thống lấy TK phải trả lương mặc định của công ty.
