# CRM Contact Detail — bố cục tham chiếu MISA AMIS

## Nguồn yêu cầu

Phản hồi trực tiếp ngày 14/07/2026 kèm ảnh màn hình chi tiết Liên hệ của
MISA AMIS CRM.

## Phạm vi

Chỉ điều chỉnh cách trình bày màn hình chi tiết Liên hệ. Dữ liệu, quyền và
luồng lưu hiện có được giữ nguyên.

## Thay đổi giao diện

- Header hiển thị avatar, tên liên hệ, tổ chức và thao tác thêm thẻ theo cùng
  một cụm nhận diện.
- Chức danh, phòng ban, điện thoại và email được trình bày thành lưới thông tin
  nhanh hai cột thay cho một hàng ngang dài.
- Thanh tab giữ cố định phía trên vùng nội dung và cho phép cuộn ngang khi
  không đủ chiều rộng.
- Các nhóm trường chi tiết dùng lưới hai cột có chiều rộng đọc tối đa, tránh
  kéo nội dung loãng trên màn hình lớn.
- Panel Hoạt động/Mua hàng được giữ bên phải, bổ sung dải biểu tượng thao tác
  nhanh theo mẫu tham chiếu.
- Ở màn hình hẹp, panel phải được ẩn và lưới trường chuyển về một cột.

## Đồng bộ với chi tiết Tiềm năng

- Ghi chú sử dụng toàn bộ chiều rộng vùng nội dung.
- Tab tài liệu chỉ hiện thao tác khi người dùng có quyền sửa; hỗ trợ thêm liên
  kết, tải tệp và phân biệt icon liên kết, hình ảnh, tài liệu.
- Liên kết không có giao thức được tự động chuẩn hóa thành `https://` ở cả
  frontend và backend.
- Các bảng liên quan dùng cỡ chữ tiêu đề 13px; icon trạng thái rỗng có kích
  thước 40px.
- Các nút thêm Nhiệm vụ, Lịch hẹn và Cuộc gọi mở form nhập liệu thật, lưu vào
  `ToDo` hoặc `Event` với tham chiếu `Contact` và cập nhật lịch sử hoạt động.
- Nút gọi điện, gửi email và thêm thẻ thực hiện hành động thật thay cho thông
  báo chờ cấu hình.
- Sau khi lưu liên hệ, thêm hoạt động hoặc thêm tài liệu, người dùng vẫn ở chi
  tiết Liên hệ và đúng tab đang thao tác.

## Tiêu chí kiểm tra

1. Tổ chức hiển thị dưới tên liên hệ và mở đúng chi tiết Khách hàng khi nhấn.
2. Thông tin nhanh không phát sinh thanh cuộn ngang ở kích thước desktop.
3. Nội dung trường giữ hai cột ở desktop và một cột trên mobile.
4. Các tab dài vẫn cuộn ngang, không đè hoặc cắt nội dung.
5. Nút biểu tượng có `title`, `aria-label` và trạng thái focus bàn phím.
6. Hoạt động mới mang `reference_type/reference_doctype = Contact` và xuất
   hiện trong tab phù hợp ngay sau khi lưu.
7. URL `example.com/profile` được lưu thành `https://example.com/profile`.
