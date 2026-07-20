---
title: Chi phí chờ phân bổ
order: 3
summary: Liệt kê các chi phí mua hàng đang treo trên TK 1388 chưa được phân bổ vào giá vốn hàng tồn kho.
---

## Mục đích

Báo cáo **Chi phí chờ phân bổ** liệt kê các khoản chi phí mua hàng đã phát sinh và đang **treo trên tài khoản chờ phân bổ** (mặc định nhóm TK 1388 — "Phải thu khác / chi phí chờ phân bổ") nhưng **chưa được cộng vào giá vốn hàng tồn kho** qua phiếu phân bổ chi phí mua hàng.

Mục đích là nhắc kế toán: còn những phụ phí nào (vận chuyển, hải quan, bảo hiểm...) chưa được kết chuyển vào giá vốn, để lập phiếu phân bổ kịp thời. Đây là báo cáo **tra cứu — không tự sinh bút toán**.

## Khi nào dùng

- Cuối tháng, trước khi khóa sổ: rà soát các chi phí mua hàng còn treo chưa phân bổ.
- Sau khi nhận hóa đơn vận chuyển / hải quan nhưng chưa kịp lập phiếu phân bổ.
- Kiểm tra số dư TK 1388 (chi phí chờ phân bổ) còn bao nhiêu, thuộc về lô hàng / nhà cung cấp nào.

## Cách thực hiện

1. Vào **Giá thành → Chi phí chờ phân bổ**.
2. Chọn bộ lọc:
   - **Công ty** (bắt buộc).
   - **Từ ngày** / **Đến ngày** (tùy chọn — lọc theo ngày hạch toán).
   - **TK** (tùy chọn) — nếu bỏ trống, hệ thống mặc định quét nhóm **TK 1388** (các tài khoản bắt đầu bằng 1388). Nhập TK khác nếu công ty treo chi phí chờ phân bổ ở tài khoản riêng.
3. Báo cáo hiển thị các bút toán phát sinh **bên Nợ** (chi phí treo) với các cột: Ngày, Số CT, Loại CT, Nhà cung cấp, TK, Số tiền, Diễn giải.
4. Bấm vào **Số CT** để mở chứng từ gốc; từ đó lập phiếu **Phân bổ chi phí mua hàng** để kết chuyển vào giá vốn.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tra cứu các bút toán đã phát sinh bên Nợ trên tài khoản chờ phân bổ. Việc kết chuyển vào giá vốn thực hiện ở [Phân bổ chi phí mua hàng](lcv-co-ban.md).

## Tình huống đặc biệt & cảnh báo

- **Báo cáo trống (0 dòng)** là bình thường nếu công ty không dùng tài khoản treo 1388 cho phụ phí — nhiều đơn vị treo chi phí mua hàng trực tiếp ở TK 331 (phải trả người bán) rồi phân bổ thẳng. Khi đó nhập TK 331 (hoặc TK đang dùng) vào bộ lọc TK để xem.
- Báo cáo chỉ hiển thị **phát sinh Nợ** (chi phí treo vào). Khi đã phân bổ và đảo khoản treo, dòng tương ứng vẫn còn (báo cáo theo phát sinh, không trừ phần đã phân bổ) — dùng số dư TK 1388 trên [Sổ Cái] để biết phần còn lại thực tế.
- Chi phí treo lâu ngày không phân bổ làm sai giá vốn hàng tồn — nên xử lý trong kỳ.

## Báo cáo liên quan

- [Phân bổ chi phí mua hàng](lcv-co-ban.md): lập phiếu kết chuyển phụ phí vào giá vốn.
- [Phân bổ chi phí hàng nhập khẩu](lcv-nhap-khau.md): xử lý thuế NK, VAT NK.
- [Phân bổ phụ phí vào giá vốn (cuối kỳ)](inventory-cost-reallocation.md): kết chuyển phụ phí của hàng đã bán.

## FAQ

**Q: Vì sao báo cáo không hiện gì dù công ty có mua hàng có phụ phí?**
**A:** Mặc định báo cáo chỉ quét nhóm TK 1388. Nếu công ty treo phụ phí ở TK khác (ví dụ 331), hãy chọn đúng TK đó ở bộ lọc **TK**.

**Q: Lọc theo nhà cung cấp được không?**
**A:** Báo cáo hiển thị cột Nhà cung cấp; để lọc, dùng tính năng lọc/sắp xếp trên bảng kết quả hoặc xem [Sổ Cái] của tài khoản treo theo đối tượng.
