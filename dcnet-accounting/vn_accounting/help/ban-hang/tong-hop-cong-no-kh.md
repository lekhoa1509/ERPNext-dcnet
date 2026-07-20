---
title: Bảng tổng hợp công nợ KH
order: 8
summary: Tổng hợp số dư công nợ phải thu theo từng khách hàng, kèm tuổi nợ.
---

## Mục đích

Báo cáo **Bảng tổng hợp công nợ khách hàng** gộp công nợ phải thu (TK 131) theo **từng khách hàng** — mỗi khách một dòng với tổng số dư còn nợ và phân bổ theo tuổi nợ. Phù hợp để có cái nhìn nhanh ai nợ nhiều nhất, tổng nợ quá hạn, mà không cần xem chi tiết từng hóa đơn.

## Khi nào dùng

- Họp công nợ định kỳ: cần bảng tóm tắt nợ theo khách.
- Xác định nhóm khách nợ lớn/quá hạn để ưu tiên thu hồi.
- Lập báo cáo lãnh đạo về tổng nợ phải thu và cơ cấu tuổi nợ.
- Đối chiếu nhanh tổng số dư TK 131 theo khách.

## Cách thực hiện

1. Mở mục **Bảng tổng hợp công nợ KH**.
2. Đặt bộ lọc:
   - **Công ty** và **Ngày báo cáo** (số dư đến ngày này).
   - **Tính tuổi nợ theo**: Hạn thanh toán (mặc định) hoặc Ngày hóa đơn.
   - **Dải tuổi nợ**: mặc định 30, 60, 90, 120 ngày — có thể chỉnh.
3. Mỗi dòng là một khách hàng: tổng còn nợ + các cột tuổi nợ.
4. Xuất Excel nếu cần gửi báo cáo.

## Định khoản tự động

**Không tự định khoản — chỉ tra cứu.** Báo cáo tổng hợp số dư từ TK 131; không tạo bút toán.

## Tình huống đặc biệt & cảnh báo

- **Chỉ số tổng theo khách:** không hiển thị từng hóa đơn. Cần chi tiết hóa đơn → dùng [Công nợ phải thu](cong-no-phai-thu.md).
- **Khách số dư âm:** khách trả trước nhiều hơn nợ → số dư Có (ta đang giữ tiền khách).
- **Chọn cách tính tuổi nợ:** "theo Hạn thanh toán" phản ánh đúng quá hạn thực tế; "theo Ngày hóa đơn" phù hợp khi không dùng điều khoản thanh toán.
- **Báo cáo chuẩn của hệ thống:** nếu trống, kiểm tra đã có hóa đơn ghi sổ cho công ty trong kỳ chưa.

## Báo cáo liên quan

- [Công nợ phải thu](cong-no-phai-thu.md): bản chi tiết từng hóa đơn.
- [Hóa đơn bán hàng](hoa-don-ban-hang.md): chứng từ gốc.
- [BC bán hàng](bc-ban-hang.md): phân tích doanh số.

## FAQ

**Q: Bảng tổng hợp này khác Công nợ phải thu thế nào?**
**A:** Bảng tổng hợp gộp 1 dòng/khách (số dư + tuổi nợ). Báo cáo Công nợ phải thu liệt kê chi tiết từng hóa đơn còn nợ.

**Q: Tổng số ở đây có khớp số dư TK 131 trên Sổ Cái không?**
**A:** Có — cùng nguồn số liệu, chỉ khác cách trình bày (gộp theo khách). Nếu lệch, kiểm tra ngày báo cáo và bộ lọc công ty.

**Q: Tính tuổi nợ theo "Ngày báo cáo" hay "Hôm nay"?**
**A:** Báo cáo cho chọn tính tuổi nợ theo Ngày báo cáo (mặc định) hoặc theo ngày hiện tại — đặt trong bộ lọc.
