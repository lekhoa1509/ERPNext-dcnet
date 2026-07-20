---
title: Điều khoản thanh toán
order: 4
summary: Mẫu kỳ hạn thanh toán dùng chung cho nhà cung cấp và khách hàng — tự tính ngày đến hạn và chia đợt thanh toán.
---

## Mục đích

**Điều khoản thanh toán** (mẫu kỳ hạn thanh toán) định nghĩa cách tính hạn trả và chia đợt thanh toán cho một chứng từ: ví dụ "trả ngay", "30 ngày kể từ ngày hóa đơn", hoặc "đặt cọc 30% — 40% khi giao — 30% sau 30 ngày". Khi gắn mẫu này vào đơn mua hàng / hóa đơn mua hàng (hoặc đơn/hóa đơn bán hàng), hệ thống tự sinh lịch thanh toán với ngày đến hạn và số tiền từng đợt.

## Khi nào dùng

- Khi muốn chuẩn hóa kỳ hạn trả NCC (hoặc thu khách hàng) thay vì nhập tay từng lần.
- Khi hợp đồng chia thanh toán nhiều đợt (đặt cọc, theo tiến độ, sau giao hàng).
- Khi cần báo cáo dòng tiền / tuổi nợ chính xác theo ngày đến hạn.

## Cách thực hiện

1. Bấm **Điều khoản thanh toán** trên menu Mua hàng → danh sách mẫu kỳ hạn.
2. Bấm **+ Thêm** → đặt **Tên mẫu** (ví dụ "Trả sau 30 ngày", "Cọc 30/40/30").
3. Thêm các **dòng kỳ hạn**: với mỗi dòng chọn cách tính hạn (số ngày kể từ ngày hóa đơn / ngày cuối tháng...) và tỷ lệ % hoặc số tiền của đợt đó. Tổng các dòng phải bằng 100%.
4. **Lưu**.
5. Gắn mẫu vào chứng từ: trên đơn mua hàng / hóa đơn mua hàng, chọn mẫu ở phần **Điều khoản thanh toán** → hệ thống tự sinh lịch thanh toán (ngày đến hạn + số tiền từng đợt).

## Định khoản tự động

Điều khoản thanh toán **không sinh bút toán** — đây là mẫu cấu hình. Nó chỉ tạo **lịch thanh toán** (ngày đến hạn, số tiền đợt) trên chứng từ, phục vụ tính tuổi nợ và dự báo dòng tiền. Bút toán phát sinh khi ghi sổ chứng từ (hóa đơn mua/bán) và khi thanh toán (phiếu thanh toán).

## Tình huống đặc biệt & cảnh báo

- **Ngày đến hạn mặc định:** nếu chứng từ tự sinh lịch thanh toán mà không gắn mẫu, ngày đến hạn thường mặc định bằng ngày ghi sổ — nên gắn mẫu hoặc sửa ngày đến hạn để báo cáo dòng tiền không bị dồn về sớm.
- **Tổng tỷ lệ phải đủ 100%:** nếu các dòng kỳ hạn cộng lại không đủ 100% giá trị, lịch thanh toán sẽ thiếu phần còn lại.
- **Mẫu dùng chung mua/bán:** cùng một mẫu có thể gắn cho cả NCC (phải trả) và khách hàng (phải thu). Đặt tên rõ ràng để tránh nhầm.
- **Đổi mẫu sau khi ghi sổ:** không tự cập nhật lịch thanh toán của chứng từ đã ghi sổ; cần điều chỉnh trực tiếp trên chứng từ đó.

## Báo cáo liên quan

- [Công nợ phải trả](cong-no-phai-tra.md) — tuổi nợ tính theo ngày đến hạn từ lịch thanh toán.
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — nơi gắn mẫu kỳ hạn cho NCC.
- Dự báo dòng tiền (phân hệ Tổng hợp/Ngân hàng) — dùng ngày đến hạn để dự báo chi.

## FAQ

**Q: Điều khoản thanh toán có tự định khoản không?**
**A:** Không. Nó chỉ là mẫu cấu hình tạo lịch thanh toán (ngày đến hạn, số tiền đợt). Định khoản phát sinh ở hóa đơn và phiếu thanh toán.

**Q: Vì sao nên gắn mẫu thay vì để mặc định?**
**A:** Nếu không gắn mẫu, ngày đến hạn thường bằng ngày ghi sổ → báo cáo tuổi nợ và dòng tiền bị dồn về sớm, không phản ánh đúng kỳ hạn thực tế với NCC.

**Q: Một mẫu chia 3 đợt 30/40/30 thì cấu hình thế nào?**
**A:** Tạo 3 dòng kỳ hạn: đợt 1 = 30% (ví dụ ngay ngày hóa đơn), đợt 2 = 40% (khi giao), đợt 3 = 30% (sau 30 ngày). Tổng 3 dòng = 100%.
