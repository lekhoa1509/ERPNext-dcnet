---
title: Chi ngân hàng
order: 2
summary: Báo cáo tổng hợp chi qua ngân hàng — gồm trả nhà cung cấp, nộp thuế, lương, trả nợ vay.
---

## Mục đích

Báo cáo **Chi ngân hàng** tổng hợp tất cả giao dịch CHI qua tài khoản ngân hàng (TK 112%) trong kỳ — gồm phiếu kế toán loại Bank Entry (TK 112 ở vế Có) VÀ phiếu thanh toán phương thức Chuyển khoản loại Chi.

## Khi nào dùng

- Xem lịch sử CHI ngân hàng theo ngày và tài khoản ngân hàng.
- Bấm vào từng dòng để mở chứng từ gốc.
- Đối chiếu công nợ TK 331 / TK 334 với Sổ Tài khoản ngân hàng.
- In báo cáo CHI định kỳ cho ban giám đốc.

## Cách thực hiện

1. Bấm **Chi ngân hàng** trên menu Ngân hàng → báo cáo Chi ngân hàng mở.
2. Nhập điều kiện lọc:
   - **Công ty** (bắt buộc, mặc định công ty đang làm việc).
   - **Tài khoản ngân hàng** (tùy chọn — lọc theo TK 112%. Để trống để xem tất cả).
   - **Từ ngày / Đến ngày** (bắt buộc, mặc định 1 tháng gần nhất).
3. Bấm vào dòng để mở chứng từ gốc; menu vẫn được giữ ở VN Accounting.

### Tạo phiếu chi ngân hàng mới

Báo cáo có 2 nút tạo nhanh ở góc trên:
- **Chi thanh toán**: mở trực tiếp biểu mẫu Phiếu thanh toán loại Chi với phương thức Chuyển khoản.
- **Bút toán ngân hàng**: mở trực tiếp biểu mẫu Phiếu kế toán loại Bank Entry.

Ngoài ra có thể tạo từ đường tự nhiên:
- **Trả nhà cung cấp từ hóa đơn mua hàng:** mở hóa đơn mua hàng → "Tạo > Phiếu thanh toán", chọn phương thức Chuyển khoản → biểu mẫu phiếu thanh toán đã điền sẵn.
- **Bút toán tổng quát (nộp thuế, BHXH, lương, trả nợ vay):** mở danh sách phiếu kế toán → "+ Thêm" với loại Bank Entry.

## Định khoản tự động

| Trường hợp | TK Nợ (đối ứng) | TK Có | Ghi chú |
|---|---|---|---|
| Trả nhà cung cấp | 331 (NCC) | 1121 | Cần đối tượng = Nhà cung cấp |
| Nộp thuế GTGT | 3331 | 1121 | Nộp thẳng kho bạc qua ngân hàng |
| Nộp thuế TNDN | 3334 | 1121 | Quý hoặc năm |
| Đóng BHXH/BHYT/BHTN | 338 | 1121 | Đóng theo tháng |
| Trả lương chuyển khoản | 334 (NV) | 1121 | Cần đối tượng = Nhân viên |
| Trả nợ vay gốc | 341 | 1121 | Trả gốc vay ngân hàng |
| Trả lãi vay | 635 | 1121 | Lãi vay ngân hàng |
| Chuyển tiền sang TK khác | 1121-B / 1111-B | 1121-A | Điều chuyển nội bộ |
| Rút tiền mặt từ ngân hàng về quỹ | 1111 | 1121 | Rút tiền mặt |

## Tình huống đặc biệt & cảnh báo

- **Tài khoản không đủ số dư:** Hệ thống không chặn — kiểm tra số dư trước khi ghi sổ. Nếu số dư âm, thường là quên ghi phiếu thu trước hoặc sai ngày.
- **Trả nhà cung cấp nhiều hóa đơn cùng lúc:** Tạo 1 phiếu thanh toán loại Chi với nhiều tham chiếu (hệ thống tự phân bổ), HOẶC 1 Bank Entry với nhiều dòng Nợ TK 331 + 1 dòng Có TK 1121.
- **Trả nợ vay (gốc + lãi) trong 1 lần chuyển:** Tách thành 2 dòng Nợ: TK 341 (gốc) và TK 635 (lãi).
- **Phí ngân hàng:** Ghi nhận riêng dòng Nợ TK 642x / Có TK 1121; có thể tách riêng hoặc gộp cùng 1 Bank Entry với khoản chi chính.
- **Nộp thuế nhiều loại trong 1 lần chuyển:** Tách thành nhiều dòng Nợ (3331, 3334, 3335) trong cùng 1 Bank Entry.

## Báo cáo liên quan

- **Thu ngân hàng**: cặp đối ứng.
- **Sổ Tài khoản ngân hàng**: sổ chi tiết TK 112.
- **Bảng tổng hợp công nợ NCC**: công nợ phải trả theo từng nhà cung cấp.
- **Tổng hợp khoản vay ngân hàng**: theo dõi trả nợ vay.

## FAQ

**Q: Có thể tạo Bank Entry để chi lương hàng loạt không?**
**A:** Có. Tạo 1 Bank Entry với nhiều dòng Nợ TK 334 (mỗi dòng 1 nhân viên) + 1 dòng Có TK 1121.

**Q: Khi nào dùng phiếu thanh toán Chuyển khoản so với Bank Entry?**
**A:** Phiếu thanh toán Chuyển khoản khi trả nhà cung cấp từ hóa đơn mua hàng. Bank Entry cho bút toán tổng quát không gắn với hóa đơn mua hàng (nộp thuế, BHXH, lương, trả nợ vay).

**Q: Tại sao báo cáo sắp xếp cũ nhất trước?**
**A:** Báo cáo hiển thị theo thứ tự thời gian phát sinh để dễ đối chiếu với Sổ Tài khoản ngân hàng và sao kê ngân hàng.
