# DCNET CRM Contact MISA Tabs

**Ngày:** 06/07/2026  
**App:** `dcnet_crm`  
**Route:** `/desk/dcnet-crm?view=contact-detail`

## Overview

Sửa màn hình chi tiết Liên hệ theo bộ tab tham chiếu MISA AMIS CRM.

## Requirements

- Tab ngang của Liên hệ phải có đủ các mục như MISA.
- Các tab có dữ liệu ERPNext phải hiển thị bảng liên quan thay vì empty state chung.
- Tab Hóa đơn phải show các hóa đơn liên quan đến liên hệ nếu user có quyền đọc.
- Các tab chưa có backend/spec phải vẫn bấm được và có phản hồi rõ ràng.

## Implementation

- Chuyển tab bar Contact sang cấu hình `CONTACT_DETAIL_TABS` trong `frontend/src/features/contacts/composable-create.js`.
- Bổ sung badge số lượng cho ghi chú, tài liệu, hàng hóa đã mua, cơ hội, đơn hàng, báo giá, hóa đơn và công việc.
- Dựng panel MISA-style cho:
  - `Hàng hóa đã mua`
  - `Cơ hội`
  - `Đơn hàng`
  - `Báo giá`
  - `Hóa đơn`
  - `Chiến dịch`
  - `Công việc đang thực hiện`
  - `Công việc đã hoàn thành`
  - `Thẻ tư vấn`
  - `Email`
  - `SMS`
  - `Lộ trình di tuyến`
  - `Nội dung trao đổi`
  - `Khác`
- Bổ sung backend helper trong `dcnet_crm/api.py` để lấy chứng từ liên quan theo `contact_person` hoặc Customer liên kết.
- Right rail danh sách Liên hệ chỉ có hai tab `Hoạt động/Mua hàng` theo mẫu MISA.
- Khi chọn một Liên hệ, danh sách gọi `get_contact_detail` thay cho API chi tiết chung để nhận đúng dữ liệu nghiệp vụ.
- `Hoạt động` hợp nhất ghi chú `Comment`, nhiệm vụ, lịch hẹn và cuộc gọi theo thời gian; ghi chú vừa tạo được tải lại và xuất hiện ngay trong panel.
- Panel danh sách chỉ hiển thị dữ liệu; thao tác tạo ghi chú được giữ tại màn hình chi tiết Liên hệ.
- `Mua hàng` tổng hợp Báo giá, Cơ hội, Đơn hàng và Hóa đơn liên quan; mỗi thẻ mở đúng chứng từ đích.

## Technical Notes

- Backend chỉ trả dữ liệu khi user có quyền đọc DocType tương ứng.
- Sales documents được lấy theo `contact_person = Contact.name`; nếu Contact có Customer link thì fallback thêm theo Customer.
- `Hàng hóa đã mua` tổng hợp từ Sales Invoice Item của các Sales Invoice hợp lệ.
- Các tab chưa có luồng backend chính thức sẽ hiện thông báo chờ cấu hình khi bấm action.

## Deployment

Build frontend bundle của `dcnet_crm`, build assets app và clear cache site.

## Future Updates

- Nối API thật cho Chiến dịch, Thẻ tư vấn, Email, SMS và Lộ trình khi specs chốt.
- Nếu cần persist/chi tiết hóa "Nội dung trao đổi", map sang Communication thay vì chỉ dùng ghi chú.

## Troubleshooting

- Nếu tab mới chưa hiện, hard reload browser và clear cache.
- Nếu tab Hóa đơn trống, kiểm tra quyền đọc Sales Invoice và dữ liệu có `contact_person` hoặc Customer link.
- Nếu bảng bị thiếu cột, kiểm tra field tồn tại trên DocType tương ứng; backend đã tự bỏ qua field không tồn tại.

## Verification Checklist

- [x] Tab Contact có đủ bộ tab theo MISA.
- [x] Tab bấm được và active state đổi đúng.
- [x] Hàng hóa đã mua, Đơn hàng, Báo giá, Hóa đơn đọc dữ liệu backend khi có quyền.
- [x] Hóa đơn dùng bộ lọc Contact/Customer liên kết.
- [x] Các tab chưa có dữ liệu hiển thị empty state/action rõ ràng.
- [x] Frontend build pass.
- [x] API `get_contact_detail` execute pass.
- [x] Danh sách Liên hệ hiển thị ghi chú mới trong `Hoạt động` và chứng từ liên quan trong `Mua hàng`.
- [x] Backend integration tests đạt `39/39` ngày 15/07/2026.
