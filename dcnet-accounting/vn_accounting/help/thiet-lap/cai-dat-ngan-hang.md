---
section: Thiết lập
title: Cài đặt ngân hàng
summary: Thiết lập cấu hình import sao kê, đối soát và xử lý giao dịch ngân hàng.
---

## Mục đích

**Cài đặt ngân hàng** quản các tham số dùng cho import sao kê và đối soát giao dịch ngân hàng. Đây là cấu hình nền để kế toán ngân hàng xử lý sao kê, khớp giao dịch và theo dõi các khoản chưa đối soát.

## Khi nào dùng

- Khi triển khai lần đầu phân hệ ngân hàng.
- Khi thay đổi cách import sao kê hoặc logic đối soát.
- Khi cần kiểm tra vì sao giao dịch ngân hàng không tự khớp với chứng từ kế toán.

## Cách thực hiện

1. Mở **Thiết lập → Cài đặt ngân hàng**.
2. Kiểm tra các thiết lập import sao kê và đối soát.
3. Lưu cấu hình trước khi import sao kê mới.
4. Chạy lại đối soát nếu thay đổi cấu hình ảnh hưởng tới giao dịch đang chờ khớp.

## Lưu ý kế toán

- Cài đặt này không tự sinh bút toán.
- Cấu hình sai có thể làm giao dịch sao kê không tự khớp với phiếu thu/chi hoặc payment entry.
- Sau khi đổi cấu hình, nên thử với một file sao kê nhỏ trước khi import hàng loạt.
