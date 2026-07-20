---
title: Bút toán chung
order: 11
summary: Phiếu kế toán điều chỉnh/ghi nhận thủ công các nghiệp vụ bán hàng không qua hóa đơn.
---

## Mục đích

**Bút toán chung** (phiếu kế toán) cho phép ghi nhận thủ công các nghiệp vụ bán hàng mà không có chứng từ chuyên dụng: chiết khấu/giảm giá phát sinh sau, hàng bán bị trả lại, điều chỉnh công nợ, ghi nhận doanh thu đặc thù, hoặc bút toán kết chuyển. Kế toán tự nhập các dòng Nợ/Có và TK đối ứng. Khi ghi sổ, bút toán phản ánh trực tiếp vào Sổ Cái.

## Khi nào dùng

- Giảm giá hàng bán / chiết khấu thương mại phát sinh sau khi đã lập hóa đơn.
- Hàng bán bị trả lại (nếu không lập hóa đơn điều chỉnh riêng).
- Điều chỉnh công nợ phải thu (xóa nợ, bù trừ công nợ, chuyển nợ giữa khách).
- Ghi nhận doanh thu/khoản phải thu đặc thù không qua hóa đơn bán hàng.
- Bút toán kết chuyển liên quan đến doanh thu.

## Cách thực hiện

1. Mở **Bút toán chung** → "+ Thêm".
2. Chọn **ngày ghi sổ** và nhập **diễn giải** rõ ràng (mục đích bút toán).
3. Thêm các dòng tài khoản: mỗi dòng chọn TK + số tiền Nợ hoặc Có; gắn **đối tượng** (khách hàng) cho dòng TK 131 nếu cần theo dõi công nợ.
4. Đảm bảo **tổng Nợ = tổng Có**.
5. (Tùy chọn) Gắn tham chiếu tới hóa đơn bán hàng liên quan.
6. Lưu và ghi sổ → phản ánh vào Sổ Cái.

## Định khoản tự động

Bút toán chung **không tự định khoản** — kế toán nhập thủ công các dòng Nợ/Có. Một số bút toán bán hàng thường gặp:

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Chiết khấu thương mại sau hóa đơn | 5211 | 131 | Giảm doanh thu, giảm nợ phải thu |
| Giảm giá hàng bán | 5213 | 131 | |
| Hàng bán bị trả lại | 5212 + 3331 | 131 | Kèm hoàn thuế GTGT đầu ra |
| Xóa nợ phải thu khó đòi | 642 / 229 | 131 | Theo quyết định / dự phòng đã lập |
| Bù trừ công nợ (vừa mua vừa bán 1 đối tác) | 331 | 131 | Khi đối tác vừa là KH vừa là NCC |

## Tình huống đặc biệt & cảnh báo

- **Cân Nợ = Có:** bút toán không cân sẽ không ghi sổ được.
- **Gắn đối tượng cho TK công nợ:** dòng TK 131 phải gắn khách hàng để báo cáo công nợ cập nhật đúng.
- **Tham chiếu hóa đơn:** khi điều chỉnh liên quan một hóa đơn cụ thể, gắn tham chiếu để dễ đối chiếu và để số nợ trên hóa đơn cập nhật đúng.
- **Ưu tiên chứng từ chuyên dụng:** với hàng trả lại/giảm giá lớn, nên dùng hóa đơn điều chỉnh để giữ liên kết hóa đơn điện tử; bút toán chung dùng cho điều chỉnh nội bộ.
- **Bút toán nhiều dòng:** bút toán có hơn 100 dòng tài khoản sẽ được xử lý nền — chờ hệ thống ghi sổ xong.

## Báo cáo liên quan

- [Hóa đơn bán hàng](hoa-don-ban-hang.md): chứng từ doanh thu chính.
- [Công nợ phải thu](cong-no-phai-thu.md): xem tác động của bút toán điều chỉnh lên công nợ.
- **Sổ Cái / Sổ nhật ký chung** (phân hệ Tổng hợp): nơi bút toán phản ánh.

## FAQ

**Q: Khi nào dùng bút toán chung thay vì hóa đơn bán hàng?**
**A:** Dùng bút toán chung cho điều chỉnh/ghi nhận không phát sinh hóa đơn mới (xóa nợ, bù trừ, chiết khấu sau...). Doanh thu bán hàng thông thường luôn đi qua hóa đơn bán hàng để có hóa đơn điện tử và theo dõi thuế.

**Q: Hàng bán bị trả lại nên xử lý thế nào?**
**A:** Tốt nhất lập hóa đơn điều chỉnh (giữ liên kết hóa đơn điện tử). Nếu xử lý nội bộ bằng bút toán chung: Nợ 5212 + Nợ 3331 / Có 131, đồng thời nhập lại kho (Nợ 156 / Có 632).

**Q: Bút toán điều chỉnh có ảnh hưởng tuổi nợ không?**
**A:** Có, nếu gắn đối tượng khách hàng cho dòng TK 131 — số dư và tuổi nợ của khách sẽ cập nhật theo.
