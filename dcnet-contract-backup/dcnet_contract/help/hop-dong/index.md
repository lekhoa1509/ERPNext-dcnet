---
section: Hợp đồng
title: Tổng quan Hợp đồng
summary: Giới thiệu phân hệ Hợp đồng — định danh thoả thuận pháp lý với khách hàng, sinh lịch thu tiền, xuất hoá đơn theo kỳ.
---

## Mục đích

Phân hệ **Hợp đồng** quản lý vòng đời của thoả thuận pháp lý giữa công ty và khách hàng:

- Định danh hợp đồng (số HĐ giấy, ngày ký, loại dịch vụ)
- Lưu thông tin pháp lý Bên A / Bên B (chốt tại thời điểm ký, in trên hợp đồng giấy)
- Sinh **Lịch thu tiền** tự động từ Ngày kích hoạt + Hình thức thanh toán + Thời hạn gói
- Liên kết các bản ghi liên quan: hoá đơn bán hàng, phiếu thanh toán, đơn bán hàng nội bộ

## Khi nào dùng

- Sau khi ký kết với khách: tạo Hợp đồng mới, áp Mẫu hợp đồng, điền Hạng mục
- Nghiệm thu / kích hoạt dịch vụ: cập nhật Ngày kích hoạt → Lịch thu tiền tự sinh
- Hằng tháng: theo dõi Lịch thu tiền (màu nền cho biết trạng thái) và xuất hoá đơn theo kỳ
- Khi cần tạm ngưng / kích hoạt lại / huỷ: dùng nút Actions ở góc phải

## Vòng đời Hợp đồng

| Trạng thái | Ý nghĩa |
|---|---|
| Bản nháp | Đang điền thông tin, chưa duyệt |
| Đang hoạt động | Đã duyệt + đang cung cấp dịch vụ |
| Tạm ngưng | Ngưng cung cấp tạm thời (giữ dữ liệu, không huỷ) |
| Sửa đổi | Đã được sửa đổi sang phiên bản mới |
| Đã huỷ | Huỷ giữa kỳ — Lịch thu kỳ chưa xuất sẽ bị huỷ, kỳ đã xuất sẽ có giấy báo có (Credit Note) |
| Hết hạn | Đã hết thời hạn gói — chuẩn bị gia hạn hoặc đóng |

## Quan hệ với Phương án kinh doanh (PAKD)

Mỗi Hợp đồng có thể có **một PAKD** (cho HĐ định kỳ telecom) hoặc **nhiều PAKD hàng tháng** (cho FTTH hộ gia đình). PAKD là phân tích tài chính nội bộ (biên lợi nhuận, hoa hồng NVKD) — không in trên hợp đồng giấy.
