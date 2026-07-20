# CRM Contact — Chức danh và phòng ban của khách hàng

## Nguồn yêu cầu

Phản hồi trực tiếp ngày 14/07/2026: khi tạo Liên hệ, **Chức danh** và
**Phòng ban** thuộc tổ chức của khách hàng, không phải danh mục nhân sự nội bộ.

## Thay đổi

- Hiển thị hai trường dưới dạng ô nhập văn bản ở màn hình tạo mới Liên hệ.
- Áp dụng cùng cách nhập ở màn hình chỉnh sửa Liên hệ.
- Không tải dữ liệu từ hai DocType nội bộ `Designation` và `Department`.
- Lưu trực tiếp giá trị người dùng nhập vào hai trường `Data` chuẩn của Contact.

## Tiêu chí kiểm tra

1. Người dùng có thể nhập chức danh bất kỳ, ví dụ `Trưởng phòng mua hàng`.
2. Người dùng có thể nhập phòng ban bất kỳ, ví dụ `Khối vận hành khách hàng`.
3. Form không còn dropdown chứa chức danh/phòng ban của nhân viên công ty mình.
4. Giá trị đã lưu tiếp tục hiển thị và có thể chỉnh sửa ở chi tiết Liên hệ.
