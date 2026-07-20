---
title: Thu ngân hàng
order: 1
summary: Báo cáo tổng hợp các giao dịch thu qua ngân hàng — gồm phiếu kế toán và phiếu thanh toán.
---

## Mục đích

Báo cáo **Thu ngân hàng** tổng hợp tất cả giao dịch THU qua tài khoản ngân hàng (TK 112%) trong kỳ — gồm phiếu kế toán loại Bank Entry (TK 112 ở vế Nợ) VÀ phiếu thanh toán phương thức Chuyển khoản loại Thu.

## Khi nào dùng

- Xem lịch sử THU ngân hàng theo ngày và tài khoản ngân hàng.
- Bấm vào từng dòng để mở chứng từ gốc (phiếu kế toán hoặc phiếu thanh toán).
- Đối chiếu với Sổ Tài khoản ngân hàng và sao kê ngân hàng cuối ngày/tháng.
- Lọc theo công ty, tài khoản ngân hàng và khoảng ngày để báo cáo định kỳ.

## Cách thực hiện

1. Bấm **Thu ngân hàng** trên menu Ngân hàng → báo cáo Thu ngân hàng mở.
2. Nhập điều kiện lọc:
   - **Công ty** (bắt buộc, mặc định công ty đang làm việc).
   - **Tài khoản ngân hàng** (tùy chọn — lọc theo TK 112% của công ty. Để trống để xem tất cả).
   - **Từ ngày / Đến ngày** (bắt buộc, mặc định 1 tháng gần nhất).
3. Bấm **Refresh** → bảng hiển thị các dòng thu, sắp xếp theo ngày tăng dần (cũ trước → mới sau).
4. **Xem chứng từ gốc**: bấm vào dòng → mở chứng từ trong tab mới. Menu vẫn được giữ ở "VN Accounting".

### Tạo phiếu thu ngân hàng mới

Báo cáo có 2 nút tạo nhanh ở góc trên:
- **Nhận thanh toán**: mở trực tiếp biểu mẫu Phiếu thanh toán loại Thu với phương thức Chuyển khoản.
- **Bút toán ngân hàng**: mở trực tiếp biểu mẫu Phiếu kế toán loại Bank Entry.

Ngoài ra có thể tạo từ đường tự nhiên:
- Thanh toán hóa đơn bán hàng: mở hóa đơn bán hàng → bấm "Tạo > Phiếu thanh toán", chọn phương thức Chuyển khoản → biểu mẫu phiếu thanh toán đã điền sẵn.
- Bút toán tổng quát (lãi vay, thu nhập khác, nhận vốn góp): mở danh sách phiếu kế toán → "+ Thêm" với loại Bank Entry.

### Các cột hiển thị

| Cột | Mô tả |
|---|---|
| Ngày | Ngày ghi sổ |
| Số chứng từ | Link đến chứng từ gốc (phiếu kế toán hoặc phiếu thanh toán) |
| Loại chứng từ | Bút toán / Phiếu thanh toán |
| Diễn giải | Nội dung giao dịch |
| TK đối ứng | Tài khoản đối ứng (trích từ `against` field của GL Entry) |
| Số tiền | Số tiền thu (debit TK 112) |

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Khách hàng thanh toán hóa đơn | 1121 | 131 (KH) | Phương thức Chuyển khoản |
| Hoàn tạm ứng | 1121 | 141 (NV) | Nhân viên trả lại số tạm ứng dư |
| Doanh thu trực tiếp | 1121 | 511 + 3331 | Bán hàng thu qua chuyển khoản |
| Thu nhập tài chính (lãi vay, lãi TG) | 1121 | 515 | Lãi ngân hàng nhập tài khoản |
| Nhận vốn vay ngân hàng | 1121 | 341 | Vay ngân hàng giải ngân |
| Chuyển tiền từ TK khác | 1121-B | 1121-A / 1111-A | Điều chuyển nội bộ |

## Tình huống đặc biệt & cảnh báo

- **Tỷ giá ngoại tệ:** Nếu thu USD/EUR vào tài khoản ngoại tệ (TK 1122), tỷ giá theo ngày phát sinh; chênh lệch tỷ giá ghi vào TK 515/635.
- **Sai số tiền so với sao kê:** Đối chiếu ngay trong ngày bằng công cụ Đối soát sao kê. Chênh lệch cần điều chỉnh kịp thời.
- **Thu kèm thuế GTGT đầu ra:** Khi bán hàng thu qua chuyển khoản và có hóa đơn GTGT, định khoản 511 + 3331 ở phía Có.
- **Số dư âm:** Hệ thống không chặn tài khoản ngân hàng âm trong báo cáo; nếu Sổ TK ngân hàng báo số dư âm, kiểm tra ngay.

## Báo cáo liên quan

- **Chi ngân hàng**: cặp đối ứng.
- **Sổ Tài khoản ngân hàng**: sổ chi tiết TK 112 với cột số dư lũy kế.
- **Đối soát sao kê**: công cụ đối chiếu tự động.

## FAQ

**Q: Thu ngân hàng có tự động khớp với sao kê không?**
**A:** Không tự động. Dùng công cụ Đối soát sao kê để khớp dữ liệu sổ sách với file sao kê từ ngân hàng.

**Q: Khi nào dùng Bank Entry so với phiếu thanh toán Chuyển khoản?**
**A:** Phiếu thanh toán Chuyển khoản khi có hóa đơn bán hàng cần thanh toán. Bank Entry cho bút toán tổng quát không có hóa đơn (lãi vay, nhận vốn góp, thu khác).

**Q: Tại sao báo cáo sắp xếp cũ nhất trước?**
**A:** Báo cáo hiển thị theo thứ tự thời gian phát sinh (cũ trước → mới sau) để dễ đối chiếu với Sổ Tài khoản ngân hàng và sao kê ngân hàng (cũng sắp xếp theo trình tự thời gian).

**Q: Khi mở chứng từ gốc có giữ menu VN Accounting không?**
**A:** Có. Phiếu kế toán và phiếu thanh toán đều được đăng ký thuộc về phân hệ VN Accounting → bấm vào dòng → mở chứng từ → menu không nhảy.
