---
section: Hợp đồng
title: Mẫu hợp đồng
summary: Mẫu hợp đồng tự điền nhanh — Apply, Outdated, khi nào re-apply, edit tay có an toàn không.
---

## Mục đích

**Mẫu hợp đồng** (Contract Template) giúp tạo Hợp đồng nhanh bằng cách tự điền:

- Loại HĐ (Recurring / One-off)
- Hình thức thanh toán
- Thời hạn gói (tháng)
- Hạng mục (item_label, đơn giá, đơn vị, số lượng)
- Nội dung văn bản (Contract HTML)

## Cách dùng

### Cách 1 — Áp dụng khi tạo

1. Tạo Hợp đồng mới (chưa lưu)
2. Mở section **Tham chiếu & bản mẫu**, chọn **Mẫu hợp đồng** trong dropdown
3. Bấm **Apply Template** — các trường tự điền

### Cách 2 — Chuyển sang mẫu khác (HĐ Draft)

1. Mở HĐ ở trạng thái Draft
2. Chọn template khác, bấm **Apply Template**
3. Hệ thống cảnh báo nếu đã có Hạng mục — xác nhận để ghi đè

## Template Outdated (cảnh báo phiên bản cũ)

Khi mẫu hợp đồng nguồn được cập nhật (đổi version), các HĐ Draft đang dùng mẫu cũ sẽ hiển thị thông báo **"Template has been updated. Click 'Re-apply Template' to use the latest version."**

- Nếu nội dung Hạng mục chưa được sửa tay: bấm Re-apply để cập nhật
- Nếu đã sửa Hạng mục: Re-apply sẽ ghi đè — cân nhắc trước khi bấm

## Sửa tay Contract HTML

- Mở section **Văn bản hợp đồng**, chỉnh sửa nội dung trực tiếp
- Hệ thống đánh dấu `contract_html_edited = 1` để theo dõi
- Re-apply Template sau khi sửa sẽ ghi đè — sẽ có cảnh báo

## Khi nào TẠO mẫu mới thay vì sửa mẫu cũ

- Mẫu cũ có nhiều HĐ Active đang dùng → tạo mẫu version mới (giữ Number cũ, bump version)
- Đổi điều khoản pháp lý quan trọng → ALWAYS tạo mẫu mới (giữ vết)
- Chỉ đổi mức giá → sửa version tại chỗ (các HĐ Active không bị ảnh hưởng vì giá đã lock vào HĐ)
