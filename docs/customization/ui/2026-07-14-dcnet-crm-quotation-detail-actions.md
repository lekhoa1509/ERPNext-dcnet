# DCNET CRM Quotation Detail Actions

## 1. Overview

Bổ sung trang chi tiết Báo giá trong DCNET CRM và các thao tác trực tiếp tại từng tab, giữ người dùng trong luồng CRM đối với Báo giá, Công việc và Đơn hàng.

## 2. Requirements

- Nguồn: yêu cầu trực tiếp và ảnh tham chiếu UI của khách hàng ngày 14/07/2026.
- Tab Ghi chú và Nội dung trao đổi phải cho phép nhập và lưu nội dung.
- Tab Tài liệu đính kèm phải cho phép tải tệp và mở tệp đã đính kèm.
- Tab Đơn hàng phải mở luồng sinh Sales Order trong DCNET CRM.
- Tab Công việc phải cho phép tạo mới và mở công việc trong màn Hoạt động của CRM.
- Các action phải tuân theo quyền của Quotation, File, ToDo và Sales Order.

## 3. Implementation

- Thêm API chi tiết Báo giá gồm hàng hóa, ghi chú, tệp, công việc và đơn hàng liên quan.
- Thêm API tạo ToDo liên kết bằng `reference_type = Quotation`.
- Dùng API `add_note` hiện có cho ghi chú và nội dung trao đổi.
- Upload tệp private qua API chuẩn `upload_file` của Frappe.
- Khi sinh đơn hàng, form Sales Order của CRM được điền khách hàng, cơ hội và hàng hóa từ Báo giá; `prevdoc_docname` giữ liên kết nguồn.
- Danh sách công việc mở bằng route Hoạt động nội bộ của DCNET CRM.

## 4. Technical Notes

- Backend kiểm tra permission trước khi đọc hoặc tạo dữ liệu.
- Nút action chỉ hiển thị khi API trả về quyền tương ứng.
- Không chuyển Báo giá hoặc Đơn hàng sang workspace Kế toán.

## 5. Deployment

```bash
cd /workspace/development/frappe-bench
bench --site flow.local clear-cache
```

Sau deploy, tải lại cứng trình duyệt để nhận bundle mới.

## 6. Future Updates

- Chỉ bổ sung loại trao đổi hoặc workflow phê duyệt mới khi có yêu cầu khách hàng xác nhận.

## 7. Troubleshooting

- Không thấy nút action: kiểm tra quyền Write/Create của DocType tương ứng.
- Tệp không tải lên: kiểm tra CSRF token, giới hạn dung lượng và quyền File.
- Đơn hàng không xuất hiện trong tab: kiểm tra `Sales Order Item.prevdoc_docname` trỏ về Báo giá.

## 8. Verification Checklist

- [x] Ghi chú/trao đổi lưu và tải lại danh sách.
- [x] Tải và mở tài liệu đính kèm.
- [x] Sinh đơn hàng trong DCNET CRM với hàng hóa từ Báo giá.
- [x] Tạo và mở công việc liên quan.
- [x] Frontend check và build thành công.
- [x] Integration tests backend đạt 20/20.
