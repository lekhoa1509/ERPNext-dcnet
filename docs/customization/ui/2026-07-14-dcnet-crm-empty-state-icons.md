# CRM — chuẩn hóa icon trạng thái rỗng

## Nguồn yêu cầu

Phản hồi trực tiếp ngày 14/07/2026: icon tại trạng thái “Không có bản ghi” cần
lớn khoảng ba lần kích thước cũ, áp dụng cho Liên hệ và các màn hình CRM khác.

## Thay đổi

- Chuẩn hóa phần hình minh họa trạng thái rỗng về kích thước hiển thị 40px.
- Áp dụng cho Tiềm năng, Liên hệ, Cơ hội, Dashboard và các panel lịch sử có sử
  dụng `CRMIcon`.
- Các icon có nền bao ngoài sử dụng khung 56px, icon bên trong vẫn là 40px.
- Khoảng cách giữa icon và thông báo được chuẩn hóa 8px để hai thành phần nằm
  gần nhau và dễ nhận biết là cùng một trạng thái.

## Tiêu chí kiểm tra

1. Icon “Không có bản ghi” ở Tiềm năng và Liên hệ có kích thước 40 × 40px.
2. Empty state tại Cơ hội, Dashboard và panel lịch sử không còn icon 16–28px.
3. Kích thước icon không làm tràn bảng hoặc tạo thanh cuộn ngang.
4. Màu icon vẫn kế thừa màu trạng thái hiện có.
