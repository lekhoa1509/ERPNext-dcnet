---
title: Hóa đơn quá hạn cần đôn thúc
order: 4
summary: Danh sách công việc — hóa đơn gắn hợp đồng đã ghi sổ, quá hạn thanh toán, còn nợ; cột số ngày quá hạn để ưu tiên đôn thúc.
---

## Mục đích

**Hóa đơn quá hạn cần đôn thúc** liệt kê các **hóa đơn bán hàng gắn hợp đồng** đã ghi sổ, trạng thái **quá hạn** và **còn nợ > 0**. Đây là danh sách công việc cho kế toán/thu hồi công nợ: gọi đôn thúc khách nợ lâu nhất trước. Cột **"Quá hạn (ngày)"** tính sẵn để xếp ưu tiên.

## Khi nào dùng

- Định kỳ (hằng tuần/tháng): rà hóa đơn quá hạn để đôn thúc thu hồi.
- Lọc theo hợp đồng / khách hàng cụ thể để gọi từng khách.
- Lọc theo "Quá hạn tối thiểu (ngày)" để chỉ tập trung nhóm nợ lâu.

## Cách thực hiện

1. Mở **Hóa đơn quá hạn cần đôn thúc**.
2. Bộ lọc:
   - **Hợp đồng**: chỉ hóa đơn của một hợp đồng.
   - **Khách hàng**: chỉ hóa đơn của một khách.
   - **Quá hạn tối thiểu (ngày)**: chỉ hiện hóa đơn quá hạn ≥ số ngày nhập (vd 30 ngày).
3. Đọc cột **"Quá hạn (ngày)"** (tô màu cảnh báo) và **"Còn nợ"** để ưu tiên. Bấm số hóa đơn để mở chứng từ, xem chi tiết và liên hệ khách.
4. Khi khách trả: lập phiếu thu gắn hợp đồng (xuất hiện trên [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md)); hóa đơn rời khỏi báo cáo khi còn nợ về 0.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tra cứu/worklist. Việc thu tiền (ghi giảm công nợ) thực hiện qua phiếu thu: Nợ TK 111/112 (tiền) / Có TK 131 (phải thu khách).

## Tình huống đặc biệt & cảnh báo

- **Điều kiện hiện dòng:** hóa đơn đã ghi sổ + trạng thái "Quá hạn" + còn nợ > 0 + gắn hợp đồng.
- **Khác với "Kỳ thu tiền quá hạn":** báo cáo này theo **hóa đơn** đã ghi sổ; còn [Kỳ thu tiền quá hạn](ky-thu-tien-qua-han.md) theo **kỳ trong lịch hợp đồng** (gồm cả kỳ có thể chưa kịp xuất hóa đơn). Dùng kết hợp để không bỏ sót.
- **Đã thu một phần:** vẫn hiện nếu còn nợ; cột "Còn nợ" nhỏ hơn "Tổng tiền".

## Báo cáo liên quan

- [Kỳ thu tiền quá hạn](ky-thu-tien-qua-han.md): quá hạn theo kỳ lịch hợp đồng.
- [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md): toàn bộ kỳ chưa thu.
- [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md): dòng tiền thực thu.

## FAQ

**Q: Hóa đơn quá hạn ở đây và kỳ quá hạn ở "Kỳ thu tiền quá hạn" có trùng không?**
**A:** Có thể trùng nhưng góc nhìn khác: ở đây là hóa đơn đã phát hành còn nợ; bên kia là kỳ trong lịch hợp đồng (kể cả kỳ chưa xuất hóa đơn). Nên dùng cả hai.

**Q: Làm sao chỉ xem khách nợ trên 60 ngày?**
**A:** Nhập 60 vào bộ lọc "Quá hạn tối thiểu (ngày)".

**Q: Báo cáo có dữ liệu cho DCNET không?**
**A:** Có — hiện đang có hóa đơn quá hạn gắn hợp đồng còn nợ.
