---
title: Thu tiền theo hợp đồng
order: 5
summary: Theo dõi dòng tiền thực thu — các phiếu thu gắn hợp đồng/PAKD; cũng là căn cứ để hệ thống ghi sổ hoa hồng theo cơ sở tiền.
---

## Mục đích

**Thu tiền theo hợp đồng** liệt kê mọi **phiếu thu** (đã ghi sổ, loại thu tiền) gắn với một hợp đồng. Kế toán xem dòng tiền thực thu theo từng hợp đồng, đối chiếu với hóa đơn đã xuất. Đây cũng là **nền tảng để hệ thống ghi sổ hoa hồng theo cơ sở tiền** — chỉ ghi hoa hồng cho kỳ đã thực thu.

Phiếu thu lẻ ngoài hợp đồng nằm ở danh sách phiếu thu thông thường.

## Khi nào dùng

- Đối chiếu thu thực tế của một hợp đồng với hóa đơn đã xuất.
- Theo dõi tiến độ thu tiền của khách theo từng kỳ.
- Xác định kỳ đã thu để biết khoản hoa hồng nào đủ điều kiện ghi sổ.
- Lọc theo khoảng thời gian thu tiền.

## Cách thực hiện

1. Mở **Thu tiền theo hợp đồng**.
2. Bộ lọc:
   - **Hợp đồng**: chỉ phiếu thu của một hợp đồng.
   - **PAKD**: chỉ phiếu thu gắn một PAKD.
   - **Từ ngày / Đến ngày**: lọc theo ngày thu tiền.
3. Các cột: số phiếu thu, ngày, khách hàng, hợp đồng, PAKD, kỳ, **số tiền thu**, hình thức (tiền mặt / chuyển khoản...), tham chiếu (số chứng từ ngân hàng).
4. Bấm số phiếu thu để mở chứng từ gốc, đối chiếu với hóa đơn được khấu trừ.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tra cứu. Bản thân phiếu thu khi ghi sổ định khoản: Nợ TK 111/112 (tiền) / Có TK 131 (phải thu khách).

> **Liên kết với hoa hồng:** sau khi phiếu thu được ghi sổ và gắn hợp đồng/PAKD, kế toán có thể bấm "Đăng theo tỷ lệ" để hệ thống tạo bút toán hoa hồng tương ứng phần tiền vừa thu (xem [Phương án kinh doanh](phuong-an-kinh-doanh.md)).

## Tình huống đặc biệt & cảnh báo

- **Chỉ phiếu thu đã ghi sổ + loại thu tiền + gắn hợp đồng** mới hiện. Phiếu chi và phiếu thu lẻ không hiện ở đây.
- **Cơ sở tiền cho hoa hồng:** đây là nguồn xác định "kỳ đã thu" — hoa hồng chỉ ghi sổ cho kỳ đã có tiền về.
- **Khác với "Công nợ theo hợp đồng":** báo cáo này là tiền **đã thu**; [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md) là khoản **chưa thu**.

## Báo cáo liên quan

- [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md): khoản còn phải thu.
- [Sổ hoa hồng NVKD](so-hoa-hong-nvkd.md): hoa hồng phát sinh từ kỳ đã thu.
- [Phương án kinh doanh](phuong-an-kinh-doanh.md): nơi đăng hoa hồng theo tỷ lệ thực thu.

## FAQ

**Q: Phiếu thu của tôi không hiện ở đây — vì sao?**
**A:** Kiểm tra phiếu thu đã **ghi sổ** chưa, có đúng **loại thu tiền** không, và đã gắn trường **hợp đồng** chưa. Phiếu thu lẻ không gắn hợp đồng nằm ở danh sách phiếu thu thông thường.

**Q: Thu tiền ở đây có tự ghi sổ hoa hồng không?**
**A:** Không tự động hoàn toàn. Sau khi phiếu thu ghi sổ + link PAKD, kế toán bấm "Đăng theo tỷ lệ" trên phiếu thu/PAKD để tạo bút toán hoa hồng nháp tương ứng phần thực thu, rồi duyệt.

**Q: Báo cáo có dữ liệu cho DCNET không?**
**A:** Có — hiện đang có các phiếu thu gắn hợp đồng.
