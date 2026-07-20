# DCNET CRM — Điều hướng hoạt động nội bộ

**Ngày:** 14/07/2026  
**Nguồn:** Feedback trực tiếp của người dùng tại màn hình chi tiết Tiềm năng/Liên hệ.

## Yêu cầu

- Tên hoạt động trong bảng “Công việc đang thực hiện” và “Công việc đã hoàn thành” phải là liên kết thật.
- Khi bấm, giữ người dùng trong DCNET CRM và chuyển sang trang **Hoạt động**.
- Sidebar phải active tại **Hoạt động**.
- Hỗ trợ cả Nhiệm vụ (`ToDo`), Lịch hẹn và Cuộc gọi (`Event`).

## Thay đổi

- Bổ sung handler điều hướng dùng chung nhận `name` và `doctype` của hoạt động.
- Tách riêng handler mở bản ghi Desk trong menu chi tiết để không ghi đè handler điều hướng nội bộ.
- Trang Hoạt động tải đúng chi tiết `ToDo` hoặc `Event` được chọn.
- Áp dụng liên kết cho bảng hoạt động của Tiềm năng và Liên hệ; timeline hoạt động của Liên hệ cũng dùng cùng luồng.
- Panel danh sách Khách hàng bỏ hàng icon thao tác nhanh để đồng nhất với Liên hệ/Tiềm năng; hoạt động trong panel vẫn mở bằng luồng nội bộ này.
- `Event` được hiển thị read-only trong trang Hoạt động vì form chỉnh sửa hiện tại chỉ lưu cấu trúc `ToDo`.

## Giới hạn

⚠️ Cần clarify với khách hàng nếu muốn chỉnh sửa Lịch hẹn/Cuộc gọi ngay trong trang Hoạt động; hiện tại nút sửa chỉ được bật cho Nhiệm vụ để tránh ghi sai cấu trúc dữ liệu Event.
