---
title: Công nợ theo hợp đồng
order: 8
summary: Tổng hợp các kỳ chưa thu — dự kiến / đã xuất hóa đơn / quá hạn — của từng hợp đồng, lọc theo khách, chi nhánh, loại dịch vụ, trạng thái và khoảng hạn thanh toán.
---

## Mục đích

**Công nợ theo hợp đồng** tổng hợp các **kỳ thu tiền chưa hoàn tất** trong lịch của hợp đồng — gồm kỳ **dự kiến** (chưa xuất hóa đơn), **đã xuất hóa đơn** và **quá hạn**. Mỗi dòng là một kỳ, kèm khách hàng, hợp đồng, loại dịch vụ, chi nhánh, khoảng thời gian, hạn thanh toán, số tiền, trạng thái và hóa đơn (nếu có). Báo cáo cho kế toán cái nhìn toàn cảnh công nợ còn phải thu, kể cả kỳ chưa kịp phát hành hóa đơn.

## Khi nào dùng

- Rà toàn bộ công nợ còn phải thu theo hợp đồng.
- Dự báo dòng tiền: xem các kỳ "dự kiến" sắp đến hạn.
- Lọc theo khách hàng / chi nhánh / loại dịch vụ.
- Lọc theo trạng thái kỳ hoặc khoảng hạn thanh toán.

## Cách thực hiện

1. Mở **Công nợ theo hợp đồng**.
2. Bộ lọc:
   - **Khách hàng**, **Chi nhánh**, **Loại dịch vụ**.
   - **Trạng thái kỳ**: mặc định gồm Dự kiến / Đã xuất hóa đơn / Quá hạn (chọn một trạng thái để thu hẹp).
   - **Từ ngày / Đến ngày**: lọc theo hạn thanh toán.
3. Các cột: khách hàng, hợp đồng, loại dịch vụ, chi nhánh, từ ngày, đến ngày, hạn thanh toán, **số tiền**, trạng thái, hóa đơn.
4. Bấm hợp đồng hoặc hóa đơn để mở chứng từ liên quan.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tra cứu công nợ. Số liệu lấy từ lịch xuất hóa đơn của hợp đồng. Doanh thu/thuế ghi nhận khi hóa đơn từng kỳ được ghi sổ; thu nợ ghi nhận khi lập phiếu thu.

## Tình huống đặc biệt & cảnh báo

- **Mặc định loại trừ kỳ đã thu và đã hủy:** chỉ hiện Dự kiến / Đã xuất hóa đơn / Quá hạn. Kỳ "Đã thu" xem trên [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md).
- **Bao gồm cả kỳ chưa có hóa đơn:** khác với báo cáo theo hóa đơn, ở đây có cả kỳ "dự kiến" — hữu ích để dự báo dòng tiền tương lai.
- **Lọc theo hạn thanh toán** (không phải ngày phát sinh): dùng để xem các kỳ đến hạn trong một khoảng.

## Báo cáo liên quan

- [Kỳ thu tiền quá hạn](ky-thu-tien-qua-han.md): chỉ riêng các kỳ đã quá hạn.
- [Hóa đơn quá hạn cần đôn thúc](hoa-don-qua-han-don-thuc.md): quá hạn theo hóa đơn đã phát hành.
- [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md): kỳ đã thu.

## FAQ

**Q: Báo cáo này khác "Kỳ thu tiền quá hạn" thế nào?**
**A:** Báo cáo này gồm tất cả kỳ chưa thu (Dự kiến + Đã xuất hóa đơn + Quá hạn). "Kỳ thu tiền quá hạn" chỉ lọc các kỳ đã quá hạn.

**Q: Vì sao có dòng chưa có số hóa đơn?**
**A:** Đó là kỳ "dự kiến" — đến lịch nhưng hệ thống chưa sinh hóa đơn, hoặc chưa đến kỳ phát hành. Cột số tiền vẫn hiện để dự báo công nợ.

**Q: Báo cáo có dữ liệu cho DCNET không?**
**A:** Có — hiện đang có hàng trăm dòng kỳ công nợ trải trên các hợp đồng.
