# DCNET CRM Lead MISA Detail UI

**Ngày:** 06/07/2026  
**App:** `dcnet_crm`  
**Route:** `/desk/dcnet-crm?view=lead-detail`

## Overview

Sửa màn hình chi tiết Tiềm năng theo bố cục tham chiếu MISA AMIS CRM.

## Requirements

- Header rộng với avatar, tên Tiềm năng, trạng thái và action.
- Có dòng thông tin nhanh phía trên.
- Có tab ngang giống MISA.
- Nội dung chi tiết hiển thị trong khung lớn, field dạng label/value có line dưới.
- Có panel bên phải cho action nhanh và lịch sử giao dịch.

## Implementation

- Rebuild template chi tiết Lead trong `frontend/src/features/leads/template.js`.
- Override CSS Lead detail trong `frontend/src/styles.css` với namespace `.misa-lead-page`.
- Nối tab ngang vào state `leadDetailTab`; tab đang chọn có active state và đổi nội dung.
- Sửa grid layout của trang thành 4 hàng rõ ràng: header, summary, tabs, content để tab không bị kéo xuống cuối màn hình.
- Dựng panel kiểu MISA cho các tab liên quan: Ghi chú, Tài liệu đính kèm, Hàng hóa quan tâm, Chiến dịch, Email, Công việc, SMS, Lộ trình, Nội dung trao đổi, aiMarketing.
- Bổ sung modal `Chọn hàng hóa` lấy dữ liệu từ `Item`, có tìm kiếm, chọn nhiều, chọn cả trang và phân trang.
- Giữ nút `Gửi phê duyệt`; không chuyển Lead sang Contact trực tiếp.
- Normalize `Lead.notes` trong `dcnet_crm/api.py` để child table note hiển thị thành text thay vì object/JSON.
- Bổ sung `utm_source` vào dữ liệu chi tiết Lead.
- Trả thêm `attachments` trong `get_lead_detail` để tab Tài liệu đính kèm hiển thị file thật nếu Lead có File.
- Trả thêm `items` trong `get_lead_form_options` để phục vụ picker Hàng hóa quan tâm.

## Technical Notes

- Tab Tài liệu đính kèm đọc File thật của Lead.
- Tab Hàng hóa quan tâm chọn được hàng hóa trong UI/session; chưa lưu DB vì hiện chưa có field/API chính thức trong spec để persist danh sách này.
- Các action chưa có luồng backend như Thêm chiến dịch, Thêm lịch hẹn, aiMarketing sẽ hiện thông báo chờ cấu hình thay vì im lặng.
- Right rail hiển thị timeline hiện có từ `_get_timeline("Lead", name)`.

## Deployment

Build frontend bundle của `dcnet_crm`, build assets app và clear cache site.

## Future Updates

Khi có API cho từng tab, nối tab ngang vào state active tab và render dữ liệu thực tế theo từng tab.

## Troubleshooting

- Nếu layout cũ vẫn xuất hiện, hard reload browser và clear cache.
- Nếu mô tả hiện object, kiểm tra `get_lead_detail` đã trả `document.notes` dạng chuỗi.

## Verification Checklist

- [x] Header Lead giống hướng MISA hơn: avatar, title, action.
- [x] Có summary row và tab ngang.
- [x] Tab ngang bấm được, đổi active state và nội dung theo từng tab MISA.
- [x] Modal chọn hàng hóa mở được và lấy danh sách `Item` từ backend.
- [x] Tab Tài liệu đính kèm đọc danh sách File gắn với Lead.
- [x] Tab và content nằm ngay dưới summary, không còn khoảng trắng lớn.
- [x] Field detail hiển thị dạng 2 cột, line dưới.
- [x] Right rail có action icons và lịch sử giao dịch.
- [x] Notes child table không còn hiển thị JSON/object.
