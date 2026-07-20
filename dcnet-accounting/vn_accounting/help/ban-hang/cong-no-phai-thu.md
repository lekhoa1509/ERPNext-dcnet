---
title: Công nợ phải thu
order: 7
summary: Chi tiết công nợ TK 131 theo từng hóa đơn, kèm tuổi nợ 30/60/90/120 ngày.
---

## Mục đích

Báo cáo **Công nợ phải thu** liệt kê **chi tiết** từng hóa đơn bán hàng còn nợ của khách hàng tại một thời điểm, kèm **tuổi nợ** phân theo các mốc 30/60/90/120 ngày. Đây là công cụ chính để theo dõi nợ phải thu (TK 131), phát hiện nợ quá hạn và lập kế hoạch thu hồi.

## Khi nào dùng

- Cuối ngày/tuần/tháng: rà soát các hóa đơn còn nợ và mức độ quá hạn.
- Thúc thu nợ: lọc theo khách hàng để biết khách nào nợ bao nhiêu, quá hạn bao lâu.
- Đối chiếu công nợ với khách hàng vào cuối kỳ.
- Lập dự phòng phải thu khó đòi dựa trên tuổi nợ.

## Cách thực hiện

1. Mở mục **Công nợ phải thu**.
2. Đặt bộ lọc:
   - **Công ty** (bắt buộc) và **Ngày báo cáo** (số dư công nợ tính đến ngày này).
   - **Khách hàng / Nhóm khách** để thu hẹp.
   - **Trung tâm chi phí** nếu theo dõi theo bộ phận.
3. Báo cáo hiển thị từng dòng: khách hàng, hóa đơn, ngày hóa đơn, hạn thanh toán, số tiền còn nợ, và các cột tuổi nợ (0–30, 31–60, 61–90, 91–120, trên 120 ngày).
4. Xuất Excel để gửi/lưu trữ nếu cần.

## Định khoản tự động

**Không tự định khoản — chỉ tra cứu.** Báo cáo đọc số dư từ Sổ Cái (TK 131) và các hóa đơn bán hàng; không tạo bút toán.

## Tình huống đặc biệt & cảnh báo

- **Tuổi nợ theo hạn thanh toán:** mốc tuổi nợ tính từ hạn của từng kỳ; hóa đơn chia nhiều kỳ (xem [Điều khoản thanh toán](dieu-khoan-thanh-toan.md)) có thể có kỳ trong hạn và kỳ quá hạn cùng lúc.
- **Khách trả trước (số âm):** khoản khách ứng trước hiển thị như số dư Có TK 131 — không phải khách nợ ta mà ta đang giữ tiền của khách.
- **Số dư đến ngày báo cáo:** đổi "Ngày báo cáo" sẽ thay đổi số dư — để xem công nợ quá khứ, đặt ngày báo cáo về thời điểm cần.
- **Báo cáo chuẩn của hệ thống:** đây là báo cáo công nợ chi tiết chuẩn — nếu dữ liệu trống, kiểm tra đã có hóa đơn bán hàng ghi sổ cho công ty trong kỳ chưa.

## Báo cáo liên quan

- [Bảng tổng hợp công nợ KH](tong-hop-cong-no-kh.md): bản tổng hợp theo từng khách (không chi tiết hóa đơn).
- [Hóa đơn bán hàng](hoa-don-ban-hang.md): chứng từ gốc phát sinh công nợ.
- [BC bán hàng](bc-ban-hang.md): phân tích doanh số.

## FAQ

**Q: Dùng báo cáo chi tiết hay bảng tổng hợp?**
**A:** Dùng **Công nợ phải thu** khi cần xem từng hóa đơn còn nợ và tuổi nợ. Dùng **Bảng tổng hợp công nợ KH** khi chỉ cần số dư gộp theo từng khách.

**Q: Vì sao có khách hiển thị số dư âm?**
**A:** Khách đó đã trả trước/ứng trước nhiều hơn số hóa đơn đã phát hành — ta đang nợ lại khách (hoặc chưa lập đủ hóa đơn cho khoản đã thu).

**Q: Đổi mốc tuổi nợ được không?**
**A:** Được — báo cáo cho phép chỉnh dải tuổi nợ (mặc định 30, 60, 90, 120 ngày) trong bộ lọc.
