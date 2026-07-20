---
title: Bút toán chung
order: 9
summary: Phiếu kế toán điều chỉnh, kết chuyển và bù trừ công nợ mua hàng không qua hóa đơn.
---

## Mục đích

**Bút toán chung** (phiếu kế toán) cho phép định khoản thủ công những nghiệp vụ mua hàng/công nợ không đi qua hóa đơn mua hàng chuẩn: điều chỉnh công nợ NCC, kết chuyển, bù trừ phải thu — phải trả cùng một đối tượng, ghi nhận giảm giá/chiết khấu sau mua, hạch toán chi phí phân bổ. Kế toán tự chọn TK Nợ/Có theo bản chất nghiệp vụ.

## Khi nào dùng

- Điều chỉnh số dư công nợ NCC sau đối chiếu.
- Bù trừ phải thu ↔ phải trả với một đối tượng vừa là khách vừa là NCC.
- Ghi nhận chiết khấu/giảm giá sau mua không lập Credit Note.
- Kết chuyển, phân bổ chi phí mua hàng cuối kỳ.
- Ghi nhận công nợ mua không có hóa đơn chuẩn (theo biên bản, hợp đồng).

## Cách thực hiện

1. Bấm **Bút toán chung** trên menu Mua hàng → danh sách phiếu kế toán.
2. Bấm **+ Thêm** → chọn **Ngày ghi sổ**, loại phiếu kế toán phù hợp.
3. Thêm các dòng định khoản: mỗi dòng chọn **Tài khoản**, nhập **Nợ** hoặc **Có**, gắn **Đối tượng** (NCC) ở dòng TK 331 để theo dõi công nợ.
4. Đảm bảo **tổng Nợ = tổng Có** thì mới ghi sổ được.
5. **Lưu** → **Ghi sổ/Duyệt**.

## Định khoản tự động

Phiếu kế toán **không tự định khoản** — kế toán nhập tay. Một số bút toán mua hàng phổ biến:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Bù trừ phải thu/phải trả cùng đối tượng | 331 (NCC) | 131 (KH) | Đối tượng vừa là khách vừa là NCC |
| Chiết khấu/giảm giá sau mua | 331 (NCC) | 156/152/632/711 | Tùy hàng còn tồn hay đã bán |
| Điều chỉnh tăng công nợ NCC | TK chi phí/hàng | 331 (NCC) | Theo biên bản đối chiếu |
| Kết chuyển chi phí mua | TK đích | TK nguồn | Phân bổ cuối kỳ |

Khi định khoản TK 331, BẮT BUỘC gắn đối tượng NCC để báo cáo công nợ đúng.

## Tình huống đặc biệt & cảnh báo

- **Phải gắn đối tượng cho dòng TK 331:** nếu ghi 331 mà không gắn NCC, [Công nợ phải trả](cong-no-phai-tra.md) sẽ không gom được vào đúng NCC.
- **Cân Nợ = Có:** hệ thống chặn ghi sổ nếu lệch.
- **Phiếu nhiều dòng (>100):** phiếu kế toán rất nhiều dòng có thể được hệ thống xử lý ghi sổ nền — chờ hoàn tất trước khi thao tác tiếp.
- **Đã ghi sổ phát hiện sai:** hủy phiếu và lập lại, không sửa trực tiếp phiếu đã ghi sổ.
- **Đối chiếu cuối kỳ:** mọi điều chỉnh công nợ qua bút toán chung phải có chứng từ kèm (biên bản đối chiếu, phụ lục hợp đồng) để giải trình thanh tra.

## Báo cáo liên quan

- [Công nợ phải trả](cong-no-phai-tra.md) — kiểm tra số dư NCC sau điều chỉnh.
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — chứng từ mua chuẩn (ưu tiên dùng thay vì bút toán tay khi có hóa đơn).
- Sổ Cái / Sổ nhật ký chung (phân hệ Tổng hợp) — xem dòng phát sinh.

## FAQ

**Q: Khi nào dùng bút toán chung thay vì hóa đơn mua hàng?**
**A:** Khi nghiệp vụ không có hóa đơn mua chuẩn: điều chỉnh công nợ, bù trừ, chiết khấu sau mua, kết chuyển. Có hóa đơn mua thì luôn ưu tiên lập hóa đơn mua hàng để tách thuế và theo dõi đầy đủ.

**Q: Ghi giảm công nợ NCC nhưng quên gắn đối tượng thì sao?**
**A:** Báo cáo công nợ sẽ không trừ đúng vào NCC đó. Hủy phiếu, lập lại và gắn đối tượng NCC ở dòng TK 331.

**Q: Bù trừ phải thu và phải trả cùng một đối tượng làm thế nào?**
**A:** Lập phiếu kế toán: Nợ 331 / Có 131 (cùng đối tượng) số tiền bù trừ; gắn đối tượng ở cả hai dòng để cập nhật đồng thời công nợ phải trả và phải thu.
