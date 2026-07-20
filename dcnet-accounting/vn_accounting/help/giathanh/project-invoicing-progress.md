---
title: Tiến độ xuất hóa đơn công trình
order: 6
summary: Theo dõi từng giai đoạn công trình — ngày dự kiến xuất hóa đơn, trạng thái, số ngày còn lại, giá xuất và hóa đơn đã gắn.
---

## Mục đích

Báo cáo **Tiến độ xuất hóa đơn** liệt kê tất cả các **giai đoạn** của các công trình và cho biết: giai đoạn nào sắp đến hạn xuất hóa đơn, đã xuất chưa, còn bao nhiêu ngày, giá dự kiến xuất và hóa đơn đã gắn (nếu có). Giúp kế toán trưởng và quản lý dự án không bỏ lỡ mốc nghiệm thu — xuất hóa đơn đúng kỳ. Đây là báo cáo **tra cứu — không tự sinh bút toán**.

## Khi nào dùng

- Đầu tháng / đầu tuần: rà các giai đoạn sắp đến hạn xuất hóa đơn.
- Theo dõi công trình nào còn giai đoạn chưa xuất hóa đơn (chậm tiến độ thu tiền).
- Đối chiếu giai đoạn nào đã gắn hóa đơn, đã thu tiền.

## Cách thực hiện

1. Vào **Giá thành → Tiến độ xuất hóa đơn**.
2. Chọn bộ lọc:
   - **Công ty**.
   - **Công trình** (tùy chọn — bỏ trống xem tất cả).
   - **Trạng thái** (tùy chọn) — lọc theo trạng thái giai đoạn.
   - **Đến hạn trong (ngày)** (tùy chọn) — chỉ hiện giai đoạn còn ≤ N ngày tới hạn.
3. Báo cáo hiển thị các cột: Công trình, Thứ tự, Giai đoạn, Trạng thái, Ngày dự kiến, Còn (ngày), CP đã pin, Giá xuất HĐ, Hóa đơn.
4. Bấm vào **Công trình** để mở hồ sơ giá thành, hoặc **Hóa đơn** để mở hóa đơn bán hàng đã gắn.

**Ý nghĩa cột:**
- **Còn (ngày)**: số ngày từ hôm nay đến ngày dự kiến xuất (âm = đã quá hạn).
- **CP đã pin**: chi phí đã được pin vào giai đoạn (qua Pivot Tool).
- **Giá xuất HĐ**: giá kế toán trưởng chốt, nếu chưa chốt thì lấy giá đề xuất theo phương pháp markup.

**Màu trạng thái:** Đã xuất HĐ / Đã thu tiền → xanh lá; Đã có HĐ nháp → xanh dương; Chờ xuất HĐ → cam; Đang thi công → xanh dương; Dự kiến → xám; Đã hủy → đỏ.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tổng hợp trạng thái các giai đoạn. Bút toán giá vốn (Dr 632 / Cr 154) chỉ sinh khi hóa đơn của giai đoạn được ghi sổ (xem [Pivot Tool](project-costing-pivot-tool.md)).

## Tình huống đặc biệt & cảnh báo

- **Còn (ngày) âm** = giai đoạn đã quá hạn dự kiến mà chưa xuất hóa đơn → ưu tiên xử lý.
- Báo cáo dựa trên **ngày dự kiến xuất hóa đơn** khai trên từng giai đoạn — nếu không khai ngày, cột "Còn (ngày)" để trống và không lọc được theo "Đến hạn trong (ngày)".
- Giai đoạn chỉ xuất hiện khi công trình đã có hồ sơ giá thành và đã tạo giai đoạn.

## Báo cáo liên quan

- [Dự án — Giá thành](project-costing-tinh-gia-thanh.md): tổng quan công cụ tính giá thành công trình.
- [Pivot Tool — gán chi phí vào giai đoạn](project-costing-pivot-tool.md): pin chi phí và tạo hóa đơn theo giai đoạn.
- [6 phương pháp markup cho giai đoạn](project-costing-stage-markup.md): cách tính giá xuất từng giai đoạn.

## FAQ

**Q: Vì sao có giai đoạn không có "Giá xuất HĐ"?**
**A:** Giai đoạn chưa được tính giá đề xuất hoặc chưa pin chi phí. Mở Pivot Tool, pin chi phí và bấm "Tính lại".

**Q: Lọc các giai đoạn sắp đến hạn trong 7 ngày làm sao?**
**A:** Nhập `7` vào bộ lọc "Đến hạn trong (ngày)" — báo cáo chỉ hiện giai đoạn còn ≤ 7 ngày (gồm cả đã quá hạn).
