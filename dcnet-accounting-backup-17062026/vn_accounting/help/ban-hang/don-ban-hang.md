---
title: Đơn bán hàng
order: 2
summary: Đơn bán hàng đã xác nhận với khách — gồm cả danh sách lọc "cần xuất hóa đơn"; chưa phát sinh bút toán.
---

## Mục đích

**Đơn bán hàng** ghi nhận cam kết mua bán đã được khách hàng xác nhận: mặt hàng, số lượng, đơn giá, ngày giao và **điều khoản thanh toán**. Đây là chứng từ điều phối giao hàng và lập hóa đơn — **chưa phát sinh bút toán** cho tới khi xuất kho/lập hóa đơn.

Mục **Đơn bán hàng cần xuất hóa đơn** là cùng danh sách này nhưng **lọc sẵn** các đơn đã giao hàng nhưng chưa lập đủ hóa đơn — giúp kế toán không bỏ sót việc xuất hóa đơn.

## Khi nào dùng

- Khách đã chốt mua: tạo đơn bán hàng (thủ công hoặc từ báo giá đã chấp nhận).
- Cần chia kỳ thanh toán (đặt cọc, trả góp): gắn **điều khoản thanh toán**.
- Theo dõi tiến độ: đơn nào đã giao, đã lập hóa đơn, còn nợ hàng/nợ hóa đơn.
- Cuối kỳ: dùng mục **"Đơn bán hàng cần xuất hóa đơn"** để rà soát các đơn đã giao mà chưa lập hóa đơn.

## Cách thực hiện

1. Mở **Đơn bán hàng** → "+ Thêm" (hoặc từ báo giá: "Tạo > Đơn bán hàng").
2. Chọn **Khách hàng**, nhập **ngày giao hàng** dự kiến.
3. Thêm các dòng mặt hàng + số lượng + đơn giá.
4. (Tùy chọn) Chọn **mẫu điều khoản thanh toán** để chia kỳ — xem [Điều khoản thanh toán](dieu-khoan-thanh-toan.md).
5. Lưu và ghi sổ.
6. Bước tiếp theo từ đơn đã ghi sổ:
   - **"Tạo > Phiếu xuất kho"** để giao hàng hóa (ghi giảm tồn kho).
   - **"Tạo > Hóa đơn bán hàng"** để phát hành hóa đơn (ghi nhận doanh thu).

### Dùng mục "Đơn bán hàng cần xuất hóa đơn"

Mở mục này để xem danh sách đơn đã giao hàng nhưng tỷ lệ lập hóa đơn chưa đủ 100%. Bấm vào từng đơn → "Tạo > Hóa đơn bán hàng" để hoàn tất.

## Định khoản tự động

**Không tự định khoản.** Đơn bán hàng là cam kết, chưa phát sinh kế toán. Bút toán chỉ phát sinh ở **phiếu xuất kho** (Nợ 632 / Có 156) và **hóa đơn bán hàng** (Nợ 131 / Có 511 + Có 3331).

## Tình huống đặc biệt & cảnh báo

- **Không cho trùng mặt hàng:** trên một đơn bán hàng, mặc định không cho nhập cùng một mã hàng trên nhiều dòng (khác với báo giá). Nếu cần nhiều quy cách, hãy gộp số lượng hoặc tách thành mặt hàng riêng.
- **Đặt cọc trước khi giao:** khách đặt cọc → thu vào TK 131 (ứng trước) qua phiếu thanh toán; số dư này tự khấu trừ khi lập hóa đơn.
- **Đơn còn nợ hàng/nợ hóa đơn:** đơn vẫn ở trạng thái mở (chưa hoàn tất) cho tới khi giao đủ và lập đủ hóa đơn. Do làm tròn qua nhiều dòng, đôi khi tỷ lệ giao/lập hóa đơn đạt ~99,99% nhưng đơn chưa tự chuyển "Hoàn tất" — đây là sai số làm tròn rất nhỏ, không ảnh hưởng số tiền.
- **Sửa đơn đã ghi sổ:** đơn đã ghi sổ không sửa trực tiếp các dòng đã giao/đã lập hóa đơn; cần hủy hoặc tạo bản sửa đổi.

## Báo cáo liên quan

- [Phiếu xuất kho](phieu-xuat-kho.md): giao hàng từ đơn bán hàng.
- [Hóa đơn bán hàng](hoa-don-ban-hang.md): phát hành hóa đơn từ đơn bán hàng.
- [Điều khoản thanh toán](dieu-khoan-thanh-toan.md): cấu hình chia kỳ thanh toán.
- [BC bán hàng](bc-ban-hang.md): phân tích đơn theo khách/mặt hàng.

## FAQ

**Q: "Đơn bán hàng" và "Đơn bán hàng cần xuất hóa đơn" có phải hai loại chứng từ khác nhau?**
**A:** Không. Đó là cùng một danh sách đơn bán hàng; "cần xuất hóa đơn" chỉ lọc sẵn các đơn đã giao nhưng chưa lập đủ hóa đơn để kế toán rà soát.

**Q: Có thể bỏ qua đơn bán hàng, lập thẳng hóa đơn không?**
**A:** Có. Với bán lẻ giao ngay, có thể tạo thẳng hóa đơn bán hàng. Đơn bán hàng hữu ích khi cần theo dõi cam kết, chia kỳ thanh toán hoặc giao hàng nhiều lần.

**Q: Khách hủy đơn sau khi đã đặt cọc?**
**A:** Hủy đơn bán hàng; khoản đặt cọc trên TK 131 xử lý riêng (hoàn lại hoặc chuyển sang đơn khác) bằng phiếu thanh toán/bút toán điều chỉnh.
