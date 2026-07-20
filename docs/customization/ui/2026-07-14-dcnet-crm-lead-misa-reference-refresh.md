# DCNET CRM Lead Detail — MISA Reference Refresh

## Overview

Điều chỉnh màn chi tiết Tiềm năng của DCNET CRM theo ảnh tham chiếu MISA do khách hàng cung cấp ngày 14/07/2026.

## Requirements

- Header gọn gồm quay lại, avatar, tên, thẻ và nhóm thao tác.
- Thanh tóm tắt hiển thị 2 cột, 2 hàng.
- Tab nghiệp vụ nằm ngang như ảnh tham chiếu.
- Nội dung chi tiết là form đọc hai cột, khoảng cách và đường kẻ trường gọn.
- Rail Lịch sử giao dịch cố định xuyên suốt chiều cao bên phải.
- Tìm kiếm trường và toggle dữ liệu trống phải hoạt động.

## Implementation

- `frontend/src/features/leads/template.js`: sắp lại header, summary, thứ tự trường, tab và rail.
- `frontend/src/features/leads/composable.js`: thêm tìm kiếm trường, lọc dữ liệu trống, menu thao tác và thêm thẻ thực tế.
- `frontend/src/styles.css`: grid trang hai cột, rail xuyên hàng, form data-dense và responsive.
- Form chi tiết không giới hạn chiều rộng cố định; hai cột tự giãn hết vùng nội dung và cột nhãn được nới rộng để tránh xuống dòng trên màn hình lớn.
- Checkbox `Dùng chung` trong form sửa Tiềm năng được reset style riêng, tránh kế thừa padding và kích thước của input văn bản.
- Giá trị `Loại tiềm năng` hiển thị dạng chữ đậm trên nền trong suốt, không dùng badge/pill.
- Tab Công việc hỗ trợ tạo Nhiệm vụ, Lịch hẹn và Cuộc gọi bằng popup; dữ liệu lưu vào `ToDo`/`Event`, cập nhật bảng hoạt động và rail Lịch sử giao dịch ngay sau khi lưu.
- Nút `Thông tin khác` mở rộng popup theo từng loại hoạt động, bổ sung Tiềm năng, Chiến dịch, người thực hiện/liên quan, ưu tiên, loại nhiệm vụ và thông tin cuộc gọi; có thể thu gọn mà không mất dữ liệu đã nhập.
- Sidebar giữ trạng thái active tại `Tiềm năng` khi mở route chi tiết `lead-detail`, đồng nhất với các màn chi tiết CRM khác.
- Ghi chú sử dụng toàn bộ chiều rộng; header bảng Tài liệu đính kèm/Hàng hóa quan tâm cố định 13px; icon empty-state và SVG hiển thị 40px, được căn gần nội dung.
- Sau khi sửa và lưu Lead, giao diện luôn quay lại đúng trang chi tiết của Lead vừa sửa thay vì trở về danh sách.
- Tab Tài liệu đính kèm hiển thị `Thêm liên kết` và `Thêm tệp` cho người có quyền sửa Lead; liên kết/tệp được lưu bằng File chuẩn và bảng tự làm mới sau khi tải.
- Ô thêm liên kết mặc định `https://`; nếu chỉ nhập tên miền, hệ thống tự bổ sung giao thức HTTPS trước khi lưu.
- Danh sách tài liệu phân biệt bằng icon: liên kết ngoài dùng dây xích, tệp ảnh dùng biểu tượng hình ảnh, các định dạng còn lại dùng biểu tượng tài liệu.
- Bộ lọc hiển thị trực tiếp toàn bộ tiêu chí, không dùng nút `Xem thêm`; quy ước này thống nhất với các danh sách CRM còn lại.

## Technical Notes

- Dữ liệu tiếp tục lấy từ `get_lead_detail`; không thay đổi cấu trúc dữ liệu backend.
- Thêm thẻ gọi API chuẩn `frappe.desk.doctype.tag.tag.add_tag`, không bỏ qua permission.
- Các custom field chưa được cài đặt vẫn hiển thị an toàn dưới dạng rỗng và bị ẩn khi tắt toggle.

## Deployment

1. Chạy `npm run build` trong repository `dcnet-crm`.
2. Chạy `bench --site flow.local clear-cache`.
3. Hard refresh trình duyệt.

## Future Updates

Không bổ sung nghiệp vụ mới ngoài ảnh tham chiếu. Những tab chưa có API riêng tiếp tục dùng empty state hiện có cho đến khi có specification.

## Troubleshooting

- Nếu rail rơi xuống dưới: kiểm tra viewport dưới 900px; đây là responsive behavior.
- Nếu UI cũ còn hiển thị: build lại bundle và clear cache.
- Nếu thêm thẻ thất bại: kiểm tra quyền sửa Lead/Tag của người dùng.

## Verification Checklist

- [x] Header và summary khớp cấu trúc tham chiếu.
- [x] Form hai cột và rail xuyên suốt trang.
- [x] Form tận dụng hết chiều rộng khả dụng, không dồn dữ liệu về bên trái.
- [x] Tìm kiếm trường hoạt động.
- [x] Toggle dữ liệu trống hoạt động.
- [x] Checkbox `Dùng chung` hiển thị đúng và có trạng thái focus rõ ràng.
- [x] Popup tạo ba loại hoạt động lưu dữ liệu thật và liên kết đúng Lead.
- [x] Công việc đang thực hiện/đã hoàn thành và Lịch sử giao dịch cập nhật từ dữ liệu đã lưu.
- [x] Menu `Tiềm năng` vẫn active khi xem chi tiết một Lead.
- [x] Lưu chỉnh sửa Lead giữ người dùng tại trang chi tiết.
- [x] Các tab điều hướng được bằng bàn phím/click.
- [ ] QA trực quan trên dữ liệu khách hàng thật.
