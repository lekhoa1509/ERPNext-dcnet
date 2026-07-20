---
title: Bút toán ngân hàng
order: 6
summary: Danh sách phiếu kế toán loại Bank Entry — xem và tạo bút toán ngân hàng không gắn với hóa đơn.
---

## Mục đích

**Bút toán ngân hàng** là danh sách các phiếu kế toán có loại **Bank Entry** — dùng cho các nghiệp vụ ngân hàng không phát sinh từ hóa đơn bán hàng hoặc hóa đơn mua hàng. Các nghiệp vụ thường gặp: nộp thuế, đóng BHXH, trả lương chuyển khoản, trả nợ vay, ghi nhận lãi vay, mua ngoại tệ.

## Khi nào dùng

- Tạo bút toán nộp thuế qua ngân hàng (TK 3331, 3334, 3335).
- Tạo bút toán đóng BHXH/BHYT/BHTN qua ngân hàng (TK 338).
- Tạo bút toán trả lương chuyển khoản hàng loạt (TK 334).
- Tạo bút toán trả nợ vay gốc (TK 341) và lãi vay (TK 635).
- Tạo bút toán điều chuyển tiền giữa các tài khoản ngân hàng (Contra Entry).
- Ghi nhận các khoản thu/chi ngân hàng không có hóa đơn (lãi ngân hàng, phí ngân hàng).

## Cách thực hiện

1. Bấm **Bút toán ngân hàng** trên menu Ngân hàng → danh sách phiếu kế toán Bank Entry mở (đã lọc sẵn loại Bank Entry).
2. Bấm **+ Thêm** để tạo phiếu mới → biểu mẫu phiếu kế toán mở với loại Bank Entry.
3. Điền thông tin:
   - **Ngày ghi sổ**: ngày phát sinh giao dịch.
   - **Số hiệu chứng từ**: tự động (có thể sửa).
   - **Dòng kế toán**: ít nhất 2 dòng (1 Nợ, 1 Có), tổng Nợ = tổng Có.
4. Lưu và **Ghi sổ** (Submit).

### Các loại bút toán tương tự

| Loại bút toán | Dùng cho | Mục menu |
|---|---|---|
| Bank Entry | Giao dịch ngân hàng không gắn hóa đơn | Bút toán ngân hàng |
| Cash Entry | Giao dịch tiền mặt không gắn hóa đơn | Mục Tổng hợp → Phiếu kế toán |
| Contra Entry | Điều chuyển giữa các tài khoản cùng công ty | Điều chuyển nội bộ |
| Journal Entry | Bút toán tổng hợp khác | Mục Tổng hợp → Phiếu kế toán |

## Định khoản tự động

Bút toán ngân hàng không tự định khoản — kế toán viên chọn TK phù hợp. Các mẫu phổ biến:

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Nộp thuế GTGT | 3331 | 1121 | Nộp qua ngân hàng |
| Nộp thuế TNDN | 3334 | 1121 | Quý hoặc năm |
| Đóng BHXH/BHYT/BHTN | 338 | 1121 | Đóng hàng tháng |
| Trả lương chuyển khoản | 334 (NV) | 1121 | Cần đối tượng = Nhân viên |
| Trả nợ vay gốc | 341 | 1121 | Gốc vay ngân hàng |
| Trả lãi vay | 635 | 1121 | Lãi vay định kỳ |
| Phí ngân hàng | 642x | 1121 | Phí duy trì TK, phí chuyển tiền |
| Lãi ngân hàng nhập gốc | 1121 | 515 | Lãi tiền gửi thanh toán |
| Chuyển tiền nội bộ NH | 1121-B | 1121-A | Dùng Contra Entry tiện hơn |

## Tình huống đặc biệt & cảnh báo

- **Nộp thuế nhiều loại cùng lần:** Tạo 1 Bank Entry với nhiều dòng Nợ (3331, 3334, 3335) + 1 dòng Có TK 1121.
- **Trả lương hàng loạt:** Tạo 1 Bank Entry với nhiều dòng Nợ TK 334 (mỗi dòng 1 nhân viên) + 1 dòng Có TK 1121.
- **Trả nợ vay (gốc + lãi):** Tách thành 2 dòng Nợ: TK 341 (gốc) và TK 635 (lãi); Có TK 1121.
- **Đối tượng:** Với TK 334 (lương) và TK 141 (tạm ứng), nên chỉ định đối tượng (Nhân viên) để phục vụ báo cáo công nợ.
- **Ghi sổ lùi ngày:** Chứng từ ghi sổ ngược thời gian (ngày ghi sổ trong quá khứ) cần kiểm tra lại trước khi lưu, vì hệ thống có thể tự đổi về hôm nay.

## Báo cáo liên quan

- **Thu ngân hàng / Chi ngân hàng**: tổng hợp giao dịch ngân hàng (gồm cả Bank Entry và phiếu thanh toán).
- **Sổ Tài khoản ngân hàng**: sổ chi tiết TK 112.
- **Sổ cái kế toán**: chi tiết tất cả tài khoản.

## FAQ

**Q: Bank Entry khác phiếu thanh toán Chuyển khoản thế nào?**
**A:** Phiếu thanh toán Chuyển khoản gắn với hóa đơn bán/mua, tự động phân bổ công nợ. Bank Entry là bút toán tổng quát, kế toán viên tự định khoản, không gắn với hóa đơn.

**Q: Có cần tạo riêng 1 Bank Entry cho mỗi khoản phí ngân hàng không?**
**A:** Có thể gộp nhiều khoản phí cùng loại vào 1 Bank Entry (nhiều dòng Nợ 642x + 1 dòng Có 1121). Nên ghi rõ diễn giải từng dòng để dễ đối chiếu sau này.

**Q: Lỡ ghi sổ Bank Entry sai — sửa thế nào?**
**A:** Hủy chứng từ (Cancel) → tạo bút toán mới. KHÔNG sửa trực tiếp chứng từ đã ghi sổ.
