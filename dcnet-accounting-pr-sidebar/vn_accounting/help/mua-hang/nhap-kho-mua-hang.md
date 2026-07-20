---
title: Nhập kho mua hàng
order: 3
summary: Phiếu nhập kho hàng mua về — ghi tăng giá trị hàng tồn kho, đối ứng tài khoản chờ nhận hóa đơn.
---

## Mục đích

**Nhập kho mua hàng** (phiếu nhập kho từ mua hàng) ghi nhận hàng hóa/vật tư mua về nhập kho, làm tăng số lượng và giá trị hàng tồn kho. Dùng khi hàng về kho TRƯỚC khi nhận được hóa đơn từ NCC, hoặc khi muốn tách việc nhận hàng (kho theo dõi) khỏi việc ghi nhận công nợ (kế toán theo dõi). Phiếu nhập kho ghi tăng kho đối ứng tài khoản chờ nhận hóa đơn (TK 151 "Hàng mua đang đi đường" hoặc TK 3388).

## Khi nào dùng

- Khi hàng tồn kho (vật tư, hàng hóa, công cụ) về kho và cần cập nhật số lượng ngay.
- Khi hàng về trước, hóa đơn NCC về sau — cần ghi nhận hàng đã có trong kho.
- Khi muốn kiểm soát số lượng nhập thực tế tách khỏi giá trị trên hóa đơn.

## Cách thực hiện

1. **Từ đơn mua hàng** (khuyến nghị): mở đơn mua hàng → bấm **Tạo > Phiếu nhập kho** để kế thừa dòng hàng + số lượng cần nhận. Hoặc:
2. **Tạo trực tiếp**: mở mục **Nhập kho mua hàng** → **+ Thêm** → chọn **Nhà cung cấp**, **Kho nhận**, thêm dòng hàng và số lượng thực nhận.
3. Kiểm tra **Giá vốn nhập** (đơn giá nhập kho) — đây là cơ sở tính giá tồn kho.
4. **Lưu** → **Ghi sổ/Duyệt** → hệ thống cập nhật số lượng và giá trị kho.
5. Khi nhận hóa đơn NCC: từ phiếu nhập kho hoặc đơn mua hàng bấm **Tạo > Hóa đơn mua hàng** để khớp và ghi công nợ.

## Định khoản tự động

Phiếu nhập kho mua hàng sinh bút toán ghi tăng kho khi ghi sổ:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Nhập kho hàng hóa | 156 | 151 / 3388 | Đối ứng TK chờ nhận hóa đơn |
| Nhập kho vật tư/nguyên liệu | 152 | 151 / 3388 | |
| Nhập kho công cụ dụng cụ | 153 | 151 / 3388 | |

Khi lập **hóa đơn mua hàng** khớp với phiếu nhập kho: tất toán TK chờ (Có 151 hoặc 3388) đối ứng công nợ (Cr 331) và tách thuế GTGT đầu vào (Dr 1331). TK 151 = hàng mua đang đi đường theo TT99/2025.

## Tình huống đặc biệt & cảnh báo

- **Không lập phiếu nhập kho nếu mua dịch vụ / chi phí không qua kho:** chỉ cần hóa đơn mua hàng. Phiếu nhập kho chỉ dành cho hàng tồn kho theo dõi số lượng.
- **Tránh ghi tăng kho hai lần:** nếu đã lập phiếu nhập kho, KHÔNG tích "Cập nhật tồn kho" trên hóa đơn mua hàng tương ứng.
- **Chi phí thu mua (vận chuyển, bốc xếp):** phân bổ vào giá vốn qua phiếu chi phí nhập hàng riêng (Landed Cost), không cộng tay vào đơn giá nhập.
- **Hủy phiếu nhập kho đã có hóa đơn khớp:** phải hủy hóa đơn mua hàng trước rồi mới hủy phiếu nhập kho.
- **Giá nhập kho ≠ giá hóa đơn:** nếu hóa đơn về sau có giá khác giá tạm tính lúc nhập, hệ thống điều chỉnh chênh lệch khi khớp hóa đơn — kiểm tra TK chờ nhận hóa đơn sau khi khớp xong phải về 0.

## Báo cáo liên quan

- [Đơn mua hàng](don-mua-hang.md) — chứng từ gốc tạo phiếu nhập kho.
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — bước ghi công nợ khớp với phiếu nhập kho.
- [BC theo mặt hàng](bc-theo-mat-hang.md) — sổ chi tiết mua theo mặt hàng.
- Sổ chi tiết hàng tồn kho / Báo cáo tồn kho (phân hệ Kho) — kiểm tra số lượng và giá trị tồn.

## FAQ

**Q: Bắt buộc lập phiếu nhập kho khi mua hàng không?**
**A:** Không bắt buộc. Chỉ cần với hàng tồn kho theo dõi số lượng. Với dịch vụ/chi phí mua ngoài, chỉ cần hóa đơn mua hàng. Cũng có thể bỏ phiếu nhập kho và tích "Cập nhật tồn kho" trên hóa đơn nếu hàng và hóa đơn về cùng lúc.

**Q: Nhập kho trước rồi hóa đơn về sau với giá khác thì xử lý thế nào?**
**A:** Lập hóa đơn mua hàng khớp với phiếu nhập kho; hệ thống điều chỉnh chênh lệch giá. Sau khi khớp, số dư TK chờ nhận hóa đơn (151/3388) cho phiếu đó phải về 0.

**Q: Phiếu nhập kho mua hàng có ghi nhận thuế GTGT đầu vào không?**
**A:** Không. Phiếu nhập kho chỉ ghi tăng giá trị hàng. Thuế GTGT đầu vào (TK 1331) chỉ ghi nhận trên hóa đơn mua hàng.
