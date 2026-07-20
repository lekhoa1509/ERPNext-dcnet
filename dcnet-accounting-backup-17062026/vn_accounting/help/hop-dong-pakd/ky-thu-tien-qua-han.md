---
title: Kỳ thu tiền quá hạn
order: 9
summary: Liệt kê các kỳ trong lịch hợp đồng đã quá hạn nhưng chưa thu đủ — kèm số ngày quá hạn, NVKD và chi nhánh để phân công đôn thúc.
---

## Mục đích

**Kỳ thu tiền quá hạn** liệt kê từng **kỳ trong lịch của hợp đồng** ở trạng thái **quá hạn** (đến hạn nhưng chưa thu đủ), trên các hợp đồng đã ghi sổ. Mỗi dòng là một kỳ quá hạn, kèm hợp đồng, khách hàng, khoảng thời gian, hạn thanh toán, **số ngày quá hạn**, số tiền, hóa đơn (nếu có), **NVKD** và **chi nhánh**. Báo cáo giúp phân công đôn thúc theo NVKD/chi nhánh và ưu tiên kỳ trễ lâu nhất.

## Khi nào dùng

- Họp công nợ định kỳ: rà các kỳ quá hạn theo chi nhánh.
- Phân công NVKD/chi nhánh đi đôn thúc khách.
- Ưu tiên kỳ trễ lâu nhất (sắp xếp theo hạn thanh toán).

## Cách thực hiện

1. Mở **Kỳ thu tiền quá hạn**.
2. Bộ lọc:
   - **Công ty**.
   - **Chi nhánh**: chỉ kỳ quá hạn của một chi nhánh.
3. Các cột: hợp đồng, khách hàng, kỳ, từ, đến, đến hạn, **số ngày quá hạn**, số tiền, hóa đơn, **NVKD**, chi nhánh.
4. Bấm hợp đồng/hóa đơn để mở chứng từ; dùng cột NVKD để giao việc đôn thúc.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tra cứu. Thu nợ ghi nhận khi lập phiếu thu: Nợ TK 111/112 (tiền) / Có TK 131 (phải thu khách).

## Tình huống đặc biệt & cảnh báo

- **Chỉ kỳ trạng thái "Quá hạn"** trên hợp đồng đã ghi sổ. Kỳ "dự kiến" hoặc "đã xuất hóa đơn" chưa quá hạn không hiện ở đây — xem [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md).
- **Theo kỳ lịch, không theo hóa đơn:** một kỳ quá hạn có thể chưa có số hóa đơn (nếu chưa kịp phát hành). Khác với [Hóa đơn quá hạn cần đôn thúc](hoa-don-qua-han-don-thuc.md) (theo hóa đơn đã phát hành).
- **Số ngày quá hạn** tính đến ngày hiện tại — dùng để ưu tiên.

## Báo cáo liên quan

- [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md): toàn bộ kỳ chưa thu (gồm cả chưa quá hạn).
- [Hóa đơn quá hạn cần đôn thúc](hoa-don-qua-han-don-thuc.md): quá hạn theo hóa đơn đã phát hành.
- [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md): kỳ đã thu.

## FAQ

**Q: Vì sao một kỳ quá hạn ở đây không có số hóa đơn?**
**A:** Đó là kỳ trong lịch hợp đồng đã đến hạn nhưng chưa phát hành hóa đơn (hoặc hóa đơn chưa gắn về kỳ). Vẫn cần đôn thúc và xử lý phát hành.

**Q: Báo cáo này và "Hóa đơn quá hạn cần đôn thúc" — dùng cái nào?**
**A:** Dùng cả hai. Báo cáo này theo kỳ lịch (bắt cả kỳ chưa có hóa đơn); báo cáo kia theo hóa đơn đã phát hành còn nợ.

**Q: Báo cáo có dữ liệu cho DCNET không?**
**A:** Có — hiện đang có nhiều kỳ quá hạn trải trên các hợp đồng.
