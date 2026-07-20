---
title: Sổ hoa hồng NVKD (phải trả)
order: 6
summary: Sổ tổng hợp hoa hồng theo từng nhân viên kinh doanh — gồm cả khoản đi qua bút toán và qua lương, kèm trạng thái ghi sổ và truy vết hợp đồng/hóa đơn.
---

## Mục đích

**Sổ hoa hồng NVKD (phải trả)** tổng hợp mọi dòng hoa hồng trên các PAKD, theo từng **nhân viên kinh doanh (NVKD)**. Bao gồm cả hai đường ghi sổ:

- **Qua bút toán** (khi tắt "Dùng HRMS"): hoa hồng ghi Có vào TK phải trả người lao động, gắn đích danh NVKD.
- **Qua lương** (khi bật "Dùng HRMS"): hoa hồng đẩy qua **Lương bổ sung**, vào kỳ lương.

Báo cáo kèm ngữ cảnh PAKD + hợp đồng + hóa đơn để truy vết đầy đủ, và cột trạng thái cho biết khoản đã ghi sổ hay còn chờ.

## Khi nào dùng

- Cuối kỳ lương: tổng hợp hoa hồng phải trả từng NVKD.
- Kiểm tra khoản hoa hồng nào đã ghi sổ / còn chờ / đã hủy.
- Đối chiếu hoa hồng với hợp đồng + hóa đơn + phiếu thu nguồn.
- Lọc theo NVKD, theo PAKD, theo tháng lương, theo loại khoản.

## Cách thực hiện

1. Mở **Sổ hoa hồng NVKD (phải trả)**.
2. Bộ lọc:
   - **Chỉ khoản đã thu tiền KH** (mặc định bật): chỉ hiện dòng hoa hồng của kỳ khách **đã thanh toán** — bức tranh đúng cho việc chi trả theo cơ sở tiền.
   - **NVKD**, **PAKD**, **Tháng lương**, **Khoản** (loại hoa hồng).
   - **Trạng thái** (chỉ dùng khi bỏ tick "Chỉ khoản đã thu tiền KH").
3. Đọc các cột: NVKD, PAKD, hợp đồng, khách, kỳ, **khoản** (Hoa hồng NVKD / Phí GPVT...), **số tiền**, trạng thái, **phương thức** (Bút toán / HRMS), **GL** (Đã ghi sổ / Nháp / Đã hủy / Chưa đăng), hóa đơn, ngày thu, tháng lương, phiếu thu, lương bổ sung, bút toán.
4. Bấm vào số bút toán / lương bổ sung / phiếu thu để mở chứng từ liên quan.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tổng hợp tra cứu. Việc ghi sổ hoa hồng thực hiện từ PAKD (xem [Phương án kinh doanh](phuong-an-kinh-doanh.md)). Cột "GL" và "Phương thức" cho biết mỗi dòng đã ghi sổ qua đường nào:

- **Phương thức = Bút toán, GL = Đã ghi sổ/Nháp:** Nợ TK chi phí hoa hồng / Có TK phải trả NVKD (3341, gắn đích danh).
- **Phương thức = HRMS:** khoản đã đẩy vào Lương bổ sung, ghi sổ qua kỳ lương.
- **GL = Chưa đăng:** khoản đủ điều kiện nhưng kế toán chưa ghi sổ.

## Tình huống đặc biệt & cảnh báo

- **Bộ lọc "Chỉ khoản đã thu tiền KH" rất quan trọng:** bật (mặc định) chỉ hiện hoa hồng của kỳ đã thu tiền — đúng cho chi trả thực tế. Tắt để xem toàn sổ kể cả kỳ chưa thu (phục vụ rà soát).
- **Hai phương thức song song:** cùng một sổ gộp cả hoa hồng qua bút toán lẫn qua lương — đọc cột "Phương thức" để phân biệt.
- **Truy vết nguồn:** mỗi dòng dẫn về PAKD → hợp đồng → hóa đơn → phiếu thu, nên dễ đối chiếu vì sao phát sinh.

## Báo cáo liên quan

- [Phương án kinh doanh](phuong-an-kinh-doanh.md): nơi tính và đăng hoa hồng.
- [Phải trả phía khách](phai-tra-phia-khach.md): khoản phải trả người nhận ngoài (không phải NVKD).
- [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md): căn cứ kỳ đã thu.

## FAQ

**Q: Vì sao hoa hồng đã duyệt PAKD nhưng cột GL ghi "Chưa đăng"?**
**A:** Hoa hồng ghi sổ theo cơ sở tiền và cần kế toán bấm đăng. Mở PAKD tương ứng, kiểm tra kỳ đã thu tiền chưa, rồi đăng.

**Q: "Phương thức = HRMS" nghĩa là gì?**
**A:** Khoản hoa hồng được trả qua **Lương bổ sung** (vào kỳ lương) thay vì bút toán riêng — do thiết lập "Dùng HRMS" đang bật.

**Q: Báo cáo có dữ liệu cho DCNET không?**
**A:** Có — hiện đang có nhiều dòng hoa hồng (gồm cả kỳ đã thu tiền) trải trên các PAKD.
