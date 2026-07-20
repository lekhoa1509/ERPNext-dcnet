# CRM Opportunity List — Related Data Panel

## Nguồn yêu cầu

- Feedback trực tiếp của người dùng ngày 15/07/2026.
- UI tham chiếu: danh sách Cơ hội của MISA AMIS CRM do người dùng cung cấp.
- Phạm vi chỉ tổ chức và hiển thị dữ liệu liên quan đã có; không bổ sung nghiệp vụ ngoài đặc tả.

## Hành vi

Khi chọn một dòng trong danh sách **Cơ hội**, panel bên phải có hai phạm vi dữ liệu độc lập:

1. **Cơ hội**
   - Hoạt động: nhật ký và hoạt động gắn trực tiếp với cơ hội.
   - Mua hàng: báo giá, đơn hàng và hóa đơn phát sinh từ đúng cơ hội đang chọn.
   - Liên hệ: liên hệ trực tiếp và các liên hệ thuộc khách hàng của cơ hội.
   - Hàng hóa: danh sách hàng hóa của cơ hội.
2. **Khách hàng**
   - Chỉ khả dụng khi cơ hội được gắn với một Customer.
   - Hoạt động, Mua hàng và Liên hệ lấy từ workspace của Customer được gắn vào cơ hội.
   - Không hiển thị form thêm ghi chú tại panel danh sách; panel chỉ đọc dữ liệu.

## Quy tắc dữ liệu

- Dữ liệu phạm vi **Cơ hội** không được lẫn toàn bộ chứng từ của khách hàng.
- Sales Order chỉ được đưa vào phạm vi Cơ hội khi `custom_opportunity` trùng cơ hội đang chọn.
- Sales Invoice của phạm vi Cơ hội được truy theo Sales Order đã liên kết với cơ hội.
- Khi đổi nhanh dòng đang chọn, phản hồi Customer cũ không được ghi đè dữ liệu của Customer mới.
- Tất cả API tiếp tục kiểm tra quyền đọc của DocType và document tương ứng.

## Tệp triển khai

- `dcnet-crm/dcnet_crm/api.py`
- `dcnet-crm/frontend/src/app.js`
- `dcnet-crm/frontend/src/features/opportunities/composable.js`
- `dcnet-crm/frontend/src/features/opportunities/template.js`
- `dcnet-crm/frontend/src/styles.css`

