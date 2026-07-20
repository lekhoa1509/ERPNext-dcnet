# DCNET CRM Sales Order Word Print

## 1. Overview

Kết nối màn hình chi tiết Đơn hàng CRM với danh sách mẫu Word của ứng dụng `dcnet-contract`, đồng thời cho phép mở chi tiết Khách hàng từ thẻ khách hàng trên đơn.

## 2. Requirements

- Nguồn: yêu cầu trực tiếp và ảnh phản hồi khách hàng ngày 15/07/2026.
- Nút `In` phải mở hộp chọn mẫu tương tự chức năng In hợp đồng của `dcnet-contract`.
- Bỏ biểu tượng tải xuống riêng trên tiêu đề đơn hàng.
- Mỗi mẫu hỗ trợ Xem trước, Tải Word (khi có file DOCX) và In.
- Thẻ khách hàng trên đơn phải mở chi tiết khách hàng trong DCNET CRM.
- Người dùng phải có quyền đọc Sales Order trước khi tạo tài liệu.

## 3. Implementation

- Thêm API xác thực để lấy danh sách mẫu, xem trước và trộn dữ liệu Sales Order vào mẫu được chọn.
- Điền thông tin khách hàng, liên hệ, địa chỉ, công ty, mặt hàng và giá trị đơn.
- Lưu file sinh ra ở chế độ riêng tư và đính kèm vào Sales Order.
- Nút `In` mở modal danh sách mẫu; không tự tải tài liệu.
- Bản xem trước dùng HTML của mẫu và có action in qua trình duyệt.
- Action `Tải` trên từng mẫu tạo file `.docx` riêng tư và đính kèm vào Sales Order.
- Chuyển thẻ khách hàng thành button có hover và focus-visible, điều hướng tới `customer-detail`.

## 4. Technical Notes

- `dcnet-contract` được nạp tại runtime để `dcnet_crm` vẫn giữ phụ thuộc tùy chọn.
- Nguồn mẫu: toàn bộ bản ghi `DCNet Contract Template`; người dùng chọn mẫu tại thời điểm in.
- API là `POST` vì thao tác tạo thêm một bản ghi File.
- File đầu ra là private File và gắn với đúng Sales Order.

## 5. Deployment

Build frontend, clear cache và hard refresh trình duyệt. Site cần cài `dcnet-contract` và seed mẫu Word mặc định.

## 6. Future Updates

Có thể bổ sung bản PDF khi môi trường triển khai có LibreOffice hoặc dịch vụ chuyển đổi tài liệu được phê duyệt.

## 7. Troubleshooting

- Không tạo được file: kiểm tra ứng dụng `dcnet-contract`, DocType template và file đính kèm của mẫu.
- Không thấy UI mới: build bundle, clear cache và hard refresh.
- Không mở được khách hàng: kiểm tra quyền đọc Customer của người dùng.

## 8. Verification Checklist

- [x] API chặn người không có quyền đọc Sales Order.
- [x] Tạo được DOCX từ đơn `SAL-ORD-2026-00009`.
- [x] File chứa mã đơn, khách hàng, mặt hàng và giá trị đơn.
- [x] Không còn placeholder `{{...}}` trong file kết quả.
- [x] Nút In mở danh sách mẫu từ dcnet-contract.
- [x] Đã bỏ icon tải riêng trên tiêu đề đơn hàng.
- [x] Xem trước điền đúng dữ liệu đơn và không còn placeholder `{{...}}`.
- [x] Tải Word và In hoạt động theo đúng mẫu người dùng chọn.
- [x] Thẻ khách hàng mở chi tiết Customer trong CRM.
- [x] Frontend build thành công.
- [x] 39 integration tests vượt qua.
