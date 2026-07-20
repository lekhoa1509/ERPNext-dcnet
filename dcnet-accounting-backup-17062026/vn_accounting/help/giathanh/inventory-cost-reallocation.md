---
title: Phân bổ phụ phí vào giá vốn (cuối kỳ)
order: 7
summary: Cuối kỳ kết chuyển phần chi phí thu mua (1562) của hàng đã bán về tài khoản giá mua (1561) theo tỷ trọng giá vốn.
---

## Mục đích

Đây là **lớp 3** (kết chuyển cuối kỳ) của cơ chế tách TK kho theo VAS TT99/2025. Khi lập phiếu phân bổ chi phí mua hàng, phụ phí được chuyển sang **TK 1562 — Chi phí thu mua hàng hóa**. Nhưng khi xuất bán, hệ thống ghi giá vốn **Dr 632 / Cr 1561** theo full giá vốn (giá mua + phụ phí). Vì 1561 chỉ chứa phần giá mua, càng bán hàng 1561 càng âm, còn 1562 chỉ tăng từ phiếu phân bổ và không bao giờ giảm.

**Phân bổ phụ phí vào giá vốn (cuối kỳ)** lập bút toán **Dr 1561 / Cr 1562** để đưa phần phụ phí tương ứng với hàng **đã bán trong kỳ** về giá vốn, làm cân lại hai tài khoản. Mỗi phiếu là một bản ghi phục vụ truy vết; bút toán thực tế sinh khi ghi sổ phiếu.

Dùng cho kế toán tổng hợp / kế toán kho, chạy cuối tháng hoặc cuối quý.

## Khi nào dùng

- Cuối tháng / cuối quý, sau khi đã lập phiếu phân bổ chi phí mua hàng và có phát sinh bán hàng trong kỳ.
- Khi thấy TK 1561 có số dư âm hoặc TK 1562 tăng cao chưa kết chuyển.

## Cách thực hiện

1. Vào **Giá thành → Phân bổ phụ phí vào giá vốn (cuối kỳ)** → **+ Thêm**.
2. Chọn **Công ty**, **Từ ngày**, **Đến ngày** (kỳ phân bổ), **Ngày hạch toán**.
3. Chọn **TK nguồn** (mặc định 1562 — TK chi phí thu mua) và **TK đích** (mặc định 1561 — TK giá mua). Hai TK phải khác nhau và cùng công ty.
4. Bấm **Tính lại** → hệ thống đề xuất **Số tiền phân bổ** theo công thức (xem dưới) và hiển thị diễn giải công thức.
5. Kiểm tra số tiền, **Ghi sổ** → hệ thống sinh bút toán Dr 1561 / Cr 1562 và gắn liên kết bút toán vào phiếu (xem ở phần Bình luận, có hyperlink).

**Công thức số tiền đề xuất** (phương pháp "Theo tỉ trọng COGS kỳ"):

```
Số tiền = số dư TK 1562 × (giá vốn phát sinh trong kỳ ÷ tổng giá trị nhập kho lũy kế)
```

- Giá vốn phát sinh trong kỳ = tổng phát sinh Nợ TK giá vốn (632) trong [Từ ngày, Đến ngày].
- Số dư TK 1562 = số dư lũy kế đến Đến ngày.
- Tổng giá trị nhập kho lũy kế = tổng phát sinh Nợ các TK nhóm 156 đến Đến ngày.
- Số tiền không bao giờ vượt quá số dư 1562 (chặn trên).

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Kết chuyển phụ phí của hàng đã bán vào giá vốn | **1561** (TK đích — cộng lại giá vốn phụ phí) | **1562** (TK nguồn — giảm số dư phụ phí) | Số tiền = đề xuất theo tỷ trọng COGS kỳ |

> Sau khi phân bổ: 1561 = phần giá mua của hàng còn tồn (đúng VAS), 1562 = phụ phí của hàng còn tồn (đúng VAS), 632 = giá vốn xuất kho gồm cả giá mua và phụ phí (đúng VAS). Hủy phiếu → bút toán phân bổ tự hủy.

## Tình huống đặc biệt & cảnh báo

- **Phải bấm "Tính lại"** để hệ thống đề xuất số tiền — số tiền phải > 0 mới ghi sổ được.
- **TK nguồn và TK đích phải khác nhau** và cùng thuộc công ty.
- Đây là **phương pháp xấp xỉ theo tỷ trọng**, được kiểm toán VAS chấp nhận. Độ chính xác theo từng mặt hàng (per-Item) chưa hỗ trợ.
- Mục này xuất hiện **nhiều lần trong menu** (ở các phân hệ liên quan) nhưng cùng một chức năng — chỉ cần dùng một nơi.
- Chỉ chạy khi đã có phiếu phân bổ chi phí mua hàng (làm tăng 1562) và có phát sinh bán hàng (làm giảm 1561).

## Báo cáo liên quan

- [Phân bổ chi phí mua hàng](lcv-co-ban.md): lớp 1 và lớp 2 của cơ chế tách TK kho.
- [Cấu hình phân bổ chi phí mua hàng](lcv-allocation-settings.md): đặt TK 1562 và bật bút toán bù.
- [Chi phí chờ phân bổ](landed-cost-pending-allocation.md): chi phí mua hàng còn treo chưa phân bổ.

## FAQ

**Q: Số tiền đề xuất bằng 0, vì sao?**
**A:** Trong kỳ chưa có phát sinh giá vốn (632), hoặc TK 1562 chưa có số dư, hoặc chưa có nhập kho lũy kế. Cần có cả ba: phụ phí trong 1562, hàng bán ra (632), và nhập kho.

**Q: Có cần chạy mỗi kỳ không?**
**A:** Nên chạy cuối mỗi kỳ kế toán (tháng/quý) khi có phát sinh bán hàng để 1561/1562 phản ánh đúng giá trị hàng còn tồn.
