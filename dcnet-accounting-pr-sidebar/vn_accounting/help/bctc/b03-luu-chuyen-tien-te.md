---
title: Báo cáo lưu chuyển tiền tệ (B03-DN)
order: 3
summary: Báo cáo dòng tiền vào/ra theo phương pháp gián tiếp, TT99/2025, kèm so sánh cùng kỳ năm trước.
---

## Mục đích

**Báo cáo lưu chuyển tiền tệ (B03-DN)** theo Thông tư 99/2025/TT-BTC trình bày dòng tiền **thực tế thu vào và chi ra** trong kỳ, chia làm 3 hoạt động: kinh doanh, đầu tư, tài chính. Báo cáo giúp trả lời câu hỏi "tiền doanh nghiệp đến từ đâu và đi về đâu" — khác với B02 (lợi nhuận trên cơ sở dồn tích, có thể chưa thu/chưa chi tiền).

Hệ thống lập B03 theo **phương pháp gián tiếp**: xuất phát từ lợi nhuận kế toán rồi điều chỉnh các thay đổi vốn lưu động.

## Khi nào dùng

- Cuối tháng/quý/năm: lập báo cáo lưu chuyển tiền tệ bắt buộc trong bộ BCTC.
- Phân tích thanh khoản: kiểm tra dòng tiền từ kinh doanh có dương không.
- Đối chiếu: biến động tiền cuối kỳ phải khớp số dư tiền (TK 111+112+113) trên B01.

## Cách thực hiện

1. Vào **Báo cáo tài chính → Báo cáo lưu chuyển tiền tệ (B03-DN)**.
2. Chọn **Công ty** và **kỳ báo cáo** (Từ ngày — Đến ngày). Mặc định là tháng hiện hành.
3. Báo cáo hiển thị 4 cột: **Mã**, **Tên chỉ tiêu** (dòng tổng in đậm), **Kỳ này**, **Kỳ trước** (cùng khoảng năm trước).

### Cấu trúc 3 phần (phương pháp gián tiếp)

| Phần | Nội dung | Cách tính |
|---|---|---|
| **I. Lưu chuyển tiền từ HĐKD** | Lợi nhuận trước thuế + điều chỉnh khấu hao, dự phòng + biến động vốn lưu động | Dựa trên thay đổi số dư các khoản phải thu, hàng tồn kho, phải trả |
| **II. Lưu chuyển tiền từ đầu tư** | Mua/bán tài sản cố định, đầu tư | Biến động TK 211, 221, 222... |
| **III. Lưu chuyển tiền từ tài chính** | Vay/trả nợ, góp vốn, chia cổ tức | Biến động TK 341, 411... |
| | Lưu chuyển tiền thuần trong kỳ | = I + II + III |
| | Tiền đầu kỳ + Tiền cuối kỳ | Đối chiếu với TK 111+112+113 |

## Định khoản tự động

Báo cáo này **không tự định khoản — chỉ tra cứu**. Cách tính dòng tiền vốn lưu động dựa trên **chênh lệch số dư đầu kỳ và cuối kỳ** của từng nhóm tài khoản:

| Loại biến động | Ý nghĩa dòng tiền |
|---|---|
| Phải thu (131) tăng | Tiền chưa thu về → **trừ** khỏi dòng tiền |
| Hàng tồn kho (15x) tăng | Tiền bỏ ra mua hàng → **trừ** |
| Phải trả (331) tăng | Tiền chưa chi → **cộng** vào dòng tiền |

Các bút toán kết chuyển cuối kỳ được loại trừ giống B02 để không làm sai luồng phát sinh.

## Tình huống đặc biệt & cảnh báo

- **Phương pháp gián tiếp:** B03 trong hệ thống lập theo phương pháp gián tiếp (xuất phát từ lợi nhuận, điều chỉnh vốn lưu động) — không phải phương pháp trực tiếp (liệt kê từng khoản thu/chi tiền). Đây là phương pháp phổ biến và được chấp nhận theo TT99/2025.
- **Kiểm tra đối chiếu:** "Tiền và tương đương tiền cuối kỳ" trên B03 phải bằng Mã 110 trên B01 cùng ngày. Nếu lệch, kiểm tra mapping B03 (thường do thiếu một nhóm tài khoản biến động).
- **Kỳ trước = cùng khoảng năm trước**, có thể bằng 0 nếu năm trước chưa có dữ liệu.
- **Chưa có mapping:** báo cáo hiện dòng nhắc thiết lập BCTC Mapping.

## Báo cáo liên quan

- [B01 — Tình hình tài chính](b01-cau-truc.md) (đối chiếu tiền cuối kỳ), [B02 — Kết quả HĐKD](b02-ket-qua-kinh-doanh.md).
- [Cấu hình BCTC Mapping](bctc-mapping.md) — sửa công thức dòng tiền (dùng cách tính chênh lệch số dư).
- [Xuất Excel BCTC](bctc-xuat-excel.md).

## FAQ

**Q: Dòng tiền cuối kỳ trên B03 không khớp số dư tiền trên B01?**
**A:** Kiểm tra mapping B03 — thường do một nhóm tài khoản biến động (phải thu, hàng tồn, phải trả, vay) chưa được đưa vào công thức. Mở Cấu hình BCTC Mapping tab B03 để soát.

**Q: Vì sao phải thu tăng lại làm giảm dòng tiền?**
**A:** Phải thu tăng nghĩa là doanh nghiệp đã ghi nhận doanh thu nhưng chưa thu được tiền về — nên phần đó bị trừ khỏi lợi nhuận khi quy về dòng tiền thực.

**Q: Hệ thống lập theo phương pháp trực tiếp hay gián tiếp?**
**A:** Phương pháp gián tiếp. Nếu doanh nghiệp cần phương pháp trực tiếp, liên hệ quản trị hệ thống để cấu hình mapping riêng.
