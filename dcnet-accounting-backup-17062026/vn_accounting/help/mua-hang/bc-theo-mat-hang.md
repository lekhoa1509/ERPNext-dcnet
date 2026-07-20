---
title: BC theo mặt hàng
order: 8
summary: Sổ chi tiết mua hàng theo từng mặt hàng — liệt kê từng dòng mua kèm NCC, số lượng, đơn giá, thuế.
---

## Mục đích

**BC theo mặt hàng** (sổ chi tiết mua theo mặt hàng) liệt kê chi tiết từng dòng hàng mua trong kỳ: mặt hàng, nhà cung cấp, hóa đơn, số lượng, đơn giá, giá trị, thuế GTGT đầu vào. Dùng để truy chi tiết lịch sử mua một mặt hàng, kiểm tra biến động giá mua và đối chiếu với kê khai thuế. Đây là báo cáo chuẩn của hệ thống ERP, chỉ tra cứu.

## Khi nào dùng

- Khi cần xem toàn bộ lịch sử mua một mặt hàng cụ thể (từ NCC nào, giá bao nhiêu, mỗi lần bao nhiêu).
- Khi kiểm tra biến động đơn giá mua giữa các lần/các NCC.
- Khi đối chiếu chi tiết thuế GTGT đầu vào theo từng dòng hàng để kê khai.

## Cách thực hiện

1. Bấm **BC theo mặt hàng** trên menu Mua hàng → báo cáo mở.
2. Chọn **Công ty**, **Từ ngày / Đến ngày**, và lọc theo **Mặt hàng** / **Nhóm hàng** / **Nhà cung cấp** (tùy chọn).
3. Bấm **Refresh** → bảng liệt kê từng dòng mua: ngày, số hóa đơn, mặt hàng, NCC, số lượng, đơn giá, thành tiền, thuế.
4. Bấm vào số hóa đơn để mở chứng từ gốc (hóa đơn mua hàng) xem chi tiết.

## Định khoản tự động

Báo cáo **không sinh bút toán** — liệt kê chi tiết dòng hàng từ hóa đơn mua hàng.

## Tình huống đặc biệt & cảnh báo

- **Một dòng một mặt hàng trên một hóa đơn:** báo cáo tách đến cấp dòng hàng nên một hóa đơn nhiều mặt hàng sẽ thành nhiều dòng.
- **Đơn giá hiển thị là giá trên hóa đơn:** với hàng tồn kho, giá vốn ghi sổ có thể khác (gồm chi phí thu mua phân bổ qua Landed Cost) — đối chiếu khi cần giá vốn thực.
- **Thuế GTGT theo dòng:** dùng để kê khai chi tiết; tổng thuế phải khớp tờ khai và phát sinh Nợ TK 1331.

## Báo cáo liên quan

- [BC mua hàng](bc-mua-hang.md) — phân tích tổng hợp dạng bảng chéo.
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — chứng từ nguồn của từng dòng.
- [Mua không VAT](mua-khong-vat.md) — rà hóa đơn chưa có hóa đơn VAT điện tử.

## FAQ

**Q: Khác gì với BC mua hàng?**
**A:** BC mua hàng phân tích tổng hợp dạng bảng chéo (theo kỳ, theo NCC/nhóm). BC theo mặt hàng là sổ chi tiết, liệt kê từng dòng mua — phù hợp truy lịch sử và đối chiếu giá/thuế.

**Q: Đơn giá ở đây có phải giá vốn nhập kho không?**
**A:** Là đơn giá trên hóa đơn mua hàng. Giá vốn nhập kho có thể cao hơn nếu phân bổ thêm chi phí thu mua (vận chuyển, bốc xếp) qua phiếu chi phí nhập hàng.
