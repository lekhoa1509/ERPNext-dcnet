---
section: Thuế
title: Quy tắc thuế
summary: Tự động áp mẫu thuế bán hàng hoặc mua hàng theo điều kiện giao dịch.
---

## Mục đích

**Quy tắc thuế** giúp hệ thống tự động chọn **Mẫu thuế bán hàng** hoặc **Mẫu thuế mua hàng** khi lập chứng từ. Quy tắc có thể dựa trên danh mục thuế, khách hàng, nhà cung cấp, nhóm khách hàng, nhóm nhà cung cấp, mặt hàng hoặc nhóm hàng.

## Khi nào dùng

- Khi cần tự động áp VAT 5%, 8%, 10%, 0% theo nhóm hàng hoặc đối tượng.
- Khi một số khách hàng/nhà cung cấp có quy tắc thuế riêng.
- Khi muốn giảm rủi ro kế toán chọn nhầm mẫu thuế trên Sales Invoice hoặc Purchase Invoice.

## Cách thực hiện

1. Mở **Thuế → Quy tắc thuế**.
2. Chọn **Tax Type** là `Sales` hoặc `Purchase`.
3. Khai báo điều kiện áp dụng như danh mục thuế, khách hàng/nhà cung cấp, nhóm hàng hoặc mặt hàng.
4. Chọn mẫu thuế tương ứng:
   - **Sales Tax Template** cho bán hàng.
   - **Purchase Tax Template** cho mua hàng.
5. Lưu và thử tạo hóa đơn để kiểm tra mẫu thuế được tự động áp đúng.

## Lưu ý kế toán

- Tránh tạo nhiều quy tắc trùng điều kiện vì có thể gây xung đột khi hệ thống chọn mẫu thuế.
- Mẫu thuế bán hàng phải trỏ đúng tài khoản thuế đầu ra **33311**.
- Mẫu thuế mua hàng phải trỏ đúng tài khoản thuế đầu vào **1331** nếu được khấu trừ.
