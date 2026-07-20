# DCNET CRM — Làm mới UI chi tiết Khách hàng theo MISA

**Ngày:** 14/07/2026  
**Nguồn:** Feedback trực tiếp và ảnh tham chiếu MISA AMIS CRM của người dùng.

## Phạm vi

- Màn hình chi tiết `Customer` trong DCNET CRM.
- Không thay đổi quy trình nghiệp vụ hoặc dữ liệu; chỉ thay cấu trúc trình bày và tab mặc định.

## Thay đổi

- Mặc định mở tab **Thông tin chi tiết**, bỏ tab Tổng quan khỏi thanh điều hướng.
- Giữ sidebar trái với tên khách hàng, thêm thẻ, thao tác nhanh và thông tin tóm tắt.
- Tóm tắt sidebar gồm Mã số thuế, Điện thoại, Ngành nghề và Doanh thu như ảnh tham chiếu.
- Nội dung chia hai cột, mật độ gọn và các nhóm: Thông tin chung, Hóa đơn, Giao hàng, Bổ sung, Thống kê mua hàng, Mô tả, Hệ thống và Cổng thông tin.
- Giữ nguyên các tab Liên hệ, Hoạt động, Bán hàng, Hỗ trợ, Marketing, Ghi chú/đính kèm và Trao đổi.
- Giữ chế độ sửa hiện có; trường nhập chỉ hiện viền form khi đang chỉnh sửa.
- Bổ sung responsive: thu gọn sidebar ở màn hình vừa và chuyển một cột trên màn hình nhỏ.
- Sửa checkbox **Đặt làm liên hệ chính** thành control riêng, có trạng thái tick rõ ràng, focus bàn phím và mô tả tác động.
- Làm mới tab **Ghi chú**: vùng nhập full-width, hỗ trợ `Ctrl + Enter`, nút lưu rõ ràng và các ghi chú hiển thị dạng card dễ đọc.
- Nút **Sinh đơn hàng** dùng biến màu chủ đạo của theme (`--st-primary`) thay vì màu xanh lá cố định.
- Đồng bộ thao tác **Thêm liên kết** của Tiềm năng, Liên hệ và Khách hàng: trường URL mặc định `https://`; nếu người dùng chỉ nhập tên miền thì frontend và API tự bổ sung HTTPS.
- Làm mới tab **Trao đổi** theo mô hình luồng bình luận: avatar, metadata người gửi/thời gian, bong bóng nội dung, trạng thái rỗng và composer nhiều dòng có đính kèm, gửi theo màu theme và phím tắt `Ctrl + Enter`.
- Tách đúng nghiệp vụ **Ghi chú** và **Trao đổi**: ghi chú nội bộ lưu/hiển thị bằng `Comment`; nội dung trao đổi lưu/hiển thị bằng `Communication`, không trộn bản ghi giữa hai tab.
- Sửa mapping bị trùng nhãn trong **Thông tin chung**: trường ERPNext `industry` hiển thị là **Lĩnh vực**, trường custom `nganh_nghe` giữ nhãn **Ngành nghề**.
- Các trường phân loại trong chế độ sửa dùng dropdown lấy từ danh mục hệ thống/metadata thay vì nhập text: Nguồn gốc, Nhóm khách hàng, Khu vực, Lĩnh vực, Loại hình, Ngành nghề, Phân khúc, Bảng giá và Người phụ trách. Giá trị cũ ngoài danh mục vẫn được giữ để tránh mất dữ liệu khi lưu.

## Nguyên tắc UI

- Enterprise CRM, nền sáng và đường phân cách nhẹ.
- Tương phản chữ đủ rõ, icon SVG đồng nhất, trạng thái hover/focus không làm dịch chuyển bố cục.
