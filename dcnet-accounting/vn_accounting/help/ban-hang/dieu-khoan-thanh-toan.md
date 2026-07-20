---
title: Điều khoản thanh toán
order: 6
summary: Mẫu chia kỳ thanh toán (đặt cọc, trả góp, gối đầu) gắn vào đơn bán hàng và hóa đơn.
---

## Mục đích

**Mẫu điều khoản thanh toán** định nghĩa cách chia một khoản phải thu thành **nhiều kỳ** với tỷ lệ và hạn thanh toán riêng (ví dụ: đặt cọc 30% ngay, 40% khi giao hàng, 30% sau 30 ngày). Gắn mẫu này vào **đơn bán hàng** hoặc **hóa đơn bán hàng** để hệ thống tự tạo lịch thanh toán và theo dõi tuổi nợ chính xác từng kỳ.

## Khi nào dùng

- Hợp đồng chia kỳ: đặt cọc → tạm ứng → quyết toán.
- Bán trả góp, trả chậm theo nhiều mốc.
- Khách quen cho công nợ N ngày (net 30, net 45...).
- Cần tính tuổi nợ theo **hạn thanh toán** của từng kỳ thay vì một hạn duy nhất.

## Cách thực hiện

1. Mở **Điều khoản thanh toán** → "+ Thêm".
2. Đặt tên mẫu (ví dụ "Đặt cọc 30 - 40 - 30").
3. Thêm các dòng kỳ thanh toán, mỗi kỳ gồm:
   - **Tỷ lệ %** (hoặc số tiền cố định) của tổng phải thu.
   - **Hạn thanh toán**: số ngày kể từ ngày hóa đơn, hoặc ngày cố định trong tháng.
4. Đảm bảo tổng tỷ lệ các kỳ = 100%.
5. Lưu → mẫu sẵn sàng để chọn trên đơn bán hàng / hóa đơn.
6. Trên **đơn bán hàng** hoặc **hóa đơn bán hàng**: chọn mẫu này → hệ thống tự sinh lịch các kỳ với hạn riêng.

## Định khoản tự động

**Không tự định khoản.** Điều khoản thanh toán chỉ tạo **lịch thanh toán** (chia kỳ + hạn), không phát sinh bút toán. Bút toán doanh thu vẫn theo hóa đơn bán hàng; bút toán thu tiền theo phiếu thanh toán.

## Tình huống đặc biệt & cảnh báo

- **Tổng các kỳ phải đủ 100%:** nếu chia theo %, tổng các kỳ phải bằng 100% (hoặc tổng số tiền cố định bằng tổng phải thu).
- **Tuổi nợ theo từng kỳ:** khi gắn điều khoản nhiều kỳ, báo cáo công nợ tính tuổi nợ theo hạn của **từng kỳ** — một hóa đơn có thể có kỳ trong hạn và kỳ quá hạn cùng lúc.
- **Đặt cọc:** kỳ đặt cọc thường thu trước khi giao hàng → ghi vào TK 131 (ứng trước), tự khấu trừ khi lập hóa đơn.
- **Thay đổi điều khoản giữa chừng:** nên tạo mẫu mới thay vì sửa mẫu đang dùng cho các chứng từ cũ, tránh ảnh hưởng lịch đã phát sinh.

## Báo cáo liên quan

- [Đơn bán hàng](don-ban-hang.md): nơi gắn mẫu điều khoản thanh toán.
- [Hóa đơn bán hàng](hoa-don-ban-hang.md): kế thừa lịch thanh toán từ đơn.
- [Công nợ phải thu](cong-no-phai-thu.md): tuổi nợ tính theo hạn từng kỳ.

## FAQ

**Q: Khác gì giữa "hạn theo số ngày" và "ngày cố định trong tháng"?**
**A:** "Số ngày" = hạn = ngày hóa đơn + N ngày (net 30). "Ngày cố định" = mọi hóa đơn đều đến hạn vào một ngày nhất định trong tháng (ví dụ ngày 25 hàng tháng).

**Q: Một hóa đơn có nhiều hạn thì tuổi nợ tính thế nào?**
**A:** Theo từng kỳ riêng. Kỳ nào quá hạn sẽ vào nhóm tuổi nợ tương ứng (30/60/90/120 ngày); kỳ còn trong hạn vẫn ở nhóm chưa đến hạn.

**Q: Có bắt buộc dùng điều khoản thanh toán không?**
**A:** Không. Nếu khách trả một lần, để trống — hóa đơn dùng một hạn thanh toán duy nhất.
