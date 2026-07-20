---
title: Hoá đơn mua hàng
order: 2
summary: Ghi nhận hóa đơn mua — phát sinh công nợ phải trả (TK 331) và thuế GTGT đầu vào (TK 1331).
---

## Mục đích

**Hóa đơn mua hàng** là chứng từ ghi nhận nghĩa vụ phải trả nhà cung cấp khi mua hàng hóa/dịch vụ. Khi ghi sổ, hóa đơn mua hàng sinh bút toán ghi tăng giá trị hàng/chi phí, ghi nhận thuế GTGT đầu vào được khấu trừ (TK 1331) và công nợ phải trả người bán (TK 331). Đây là chứng từ trung tâm để theo dõi công nợ phải trả và kê khai thuế GTGT đầu vào.

## Khi nào dùng

- Khi nhận được hóa đơn từ NCC (mua hàng tồn kho, vật tư, tài sản, dịch vụ, chi phí mua ngoài).
- Khi cần ghi nhận công nợ phải trả và thuế GTGT đầu vào để kê khai khấu trừ.
- Khi ghi nhận chi phí mua ngoài không qua kho (điện, nước, thuê ngoài, vận chuyển...).

## Cách thực hiện

1. **Từ đơn mua hàng / phiếu nhập kho** (khuyến nghị): mở chứng từ gốc → bấm **Tạo > Hóa đơn mua hàng** để kế thừa dòng hàng. Hoặc:
2. **Tạo trực tiếp**: mở mục **Hoá đơn mua hàng** → **+ Thêm** → chọn **Nhà cung cấp**, nhập **Ngày ghi sổ**, thêm dòng hàng.
3. Nhập **Số hóa đơn NCC** (`bill_no`) và **Ngày hóa đơn NCC** (`bill_date`) để đối chiếu và kê khai.
4. Gắn **Mẫu thuế mua hàng** (Tax Template VAT 10% / 8% / 5% / 0%) ở phần Thuế để tách thuế GTGT đầu vào.
5. Nếu là hàng tồn kho mua thẳng không qua phiếu nhập kho riêng: tích **Cập nhật tồn kho** để hóa đơn vừa ghi công nợ vừa ghi tăng kho.
6. **Lưu** → **Ghi sổ/Duyệt**. Thanh toán sau bằng "Tạo > Phiếu thanh toán".

## Định khoản tự động

Hóa đơn mua hàng tự sinh bút toán khi ghi sổ. Tùy bản chất:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Mua hàng tồn kho, khớp phiếu nhập kho | 151 (tất toán) + 1331 | 331 | Khớp với "hàng đang đi đường" |
| Mua hàng tồn kho, có tích "Cập nhật tồn kho" | 152/153/156 + 1331 | 331 | Hóa đơn vừa ghi kho vừa ghi công nợ |
| Mua tài sản cố định | 211 + 1331 | 331 | Sau đó ghi tăng TSCĐ |
| Mua công cụ dụng cụ phân bổ | 242 (hoặc 153) + 1331 | 331 | Phân bổ dần vào chi phí |
| Chi phí mua ngoài (dịch vụ) | 627/641/642 + 1331 | 331 | Theo bộ phận sử dụng |
| Hóa đơn không có thuế GTGT khấu trừ | TK chi phí/hàng (gồm thuế) | 331 | Xem [Mua không VAT](mua-khong-vat.md) |

TT99/2025: TK 1331 = thuế GTGT đầu vào được khấu trừ; TK 331 = phải trả người bán.

## Tình huống đặc biệt & cảnh báo

- **Số hóa đơn NCC dùng để chống trùng:** không dùng tổng tiền (`grand_total`) để kiểm tra trùng hóa đơn — tổng có thể đổi khi đổi mẫu thuế. Dùng `bill_no` + nhà cung cấp + ngày ghi sổ.
- **Hàng về trước hóa đơn:** lập phiếu nhập kho trước, hóa đơn mua hàng sau, khớp với phiếu nhập kho để không ghi tăng kho hai lần.
- **Thuế GTGT đầu vào không được khấu trừ:** với hàng/chi phí không đủ điều kiện khấu trừ (không có hóa đơn hợp lệ, mục đích không phục vụ SXKD), ghi cả thuế vào giá trị hàng/chi phí — không tách 1331.
- **Mua hàng nhập khẩu / chi phí thu mua:** chi phí vận chuyển, bốc xếp tính vào giá vốn hàng qua phiếu chi phí nhập hàng riêng (Landed Cost), không cộng tay vào dòng hàng.
- **Hóa đơn trả lại / giảm giá:** dùng Credit Note (hóa đơn mua hàng âm) hoặc phiếu kế toán điều chỉnh, không sửa trực tiếp hóa đơn đã ghi sổ.

## Báo cáo liên quan

- [Công nợ phải trả](cong-no-phai-tra.md) — theo dõi tuổi nợ TK 331 theo hóa đơn.
- [Mua không VAT](mua-khong-vat.md) — rà các hóa đơn chưa nhận hóa đơn VAT điện tử từ NCC.
- [Nhập kho mua hàng](nhap-kho-mua-hang.md) — chứng từ ghi tăng kho khớp với hóa đơn.
- [BC mua hàng](bc-mua-hang.md) / [BC theo mặt hàng](bc-theo-mat-hang.md) — phân tích chi tiêu.

## FAQ

**Q: Khi nào tích "Cập nhật tồn kho" trên hóa đơn mua hàng?**
**A:** Khi mua hàng tồn kho và KHÔNG lập phiếu nhập kho riêng — hóa đơn sẽ vừa ghi tăng kho vừa ghi công nợ. Nếu đã có phiếu nhập kho, KHÔNG tích (tránh tăng kho hai lần).

**Q: Thuế GTGT đầu vào ghi vào tài khoản nào?**
**A:** TK 1331 (thuế GTGT đầu vào được khấu trừ), tách qua Mẫu thuế mua hàng. Nếu không đủ điều kiện khấu trừ thì ghi luôn vào giá trị hàng/chi phí.

**Q: Hóa đơn mua hàng đã ghi sổ phát hiện sai số tiền thì làm gì?**
**A:** Hủy hóa đơn và lập lại, hoặc dùng Credit Note/phiếu kế toán điều chỉnh. Tuyệt đối không sửa trực tiếp hóa đơn đã ghi sổ.
