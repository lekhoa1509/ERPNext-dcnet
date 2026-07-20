---
title: Cấu hình phân bổ chi phí mua hàng
order: 8
summary: Khai báo danh mục loại phụ phí, tài khoản mặc định, tách TK kho 1562 và bút toán bù cho phiếu phân bổ chi phí mua hàng.
---

## Mục đích

**Cấu hình phân bổ chi phí mua hàng** là nơi kế toán trưởng thiết lập một lần các giá trị mặc định để [Phân bổ chi phí mua hàng](lcv-co-ban.md) chạy đúng theo VAS TT99/2025:

- Danh mục các **loại phụ phí** (vận chuyển, bảo hiểm, thuế NK...) và tài khoản tương ứng.
- **Tài khoản kho đích** để tách phụ phí (mặc định 1562) và bật/tắt **bút toán bù** tự động.
- Mặc định **% VAT nhập khẩu được khấu trừ**.

Đây là một hồ sơ cài đặt dùng chung toàn công ty (Single) — không sinh bút toán.

## Khi nào dùng

- Lần đầu triển khai phân hệ Giá thành: khai báo danh mục loại phụ phí và tài khoản.
- Khi thêm loại phụ phí mới (ví dụ phí giám định, phí lưu kho).
- Khi công ty chuyển sang tách TK 156 theo TT99/2025 (cần đặt TK 1562 + bật bút toán bù).

## Cách thực hiện

1. Vào **Giá thành → Cấu hình phân bổ chi phí mua hàng** (hoặc tìm "Cấu hình phân bổ chi phí mua hàng").
2. Mục **Danh sách loại phụ phí**: mỗi dòng khai báo một loại:
   - **Loại phụ phí** (tên hiển thị, ví dụ "Vận chuyển nội địa").
   - **Mã nội bộ** (định danh duy nhất, ví dụ `inland_freight`) — không trùng nhau.
   - **TK ghi Có mặc định** — tài khoản hệ thống tự điền vào dòng chi phí khi kế toán chọn loại này.
   - **Chỉ hàng NK** — tích nếu loại này chỉ dùng cho hàng nhập khẩu (sẽ ẩn khi phiếu không phải hàng NK).
   - **Tiêu thức phân bổ** — theo giá trị / số lượng / khối lượng.
3. Mục **Tách TK kho cho phụ phí (VAS TT99/2025)**:
   - **TK kho mặc định cho phụ phí mua hàng** — đặt **1562** (TK chi phí thu mua).
   - **Tự lập bút toán bù phụ phí khi ghi sổ phiếu phân bổ** — tích để hệ thống tự sinh bút toán Dr 1562 / Cr 1561 sau mỗi phiếu.
4. Mục **Cài đặt tự động khác**:
   - **Tự điền TK khi tạo phiếu phân bổ mới** — tự điền TK kho mặc định lên phiếu mới.
   - **% VAT NK mặc định được khấu trừ** — giá trị 0–100, gợi ý khi xử lý VAT nhập khẩu.
5. Lưu.

## Định khoản tự động

Hồ sơ cấu hình này **không tự định khoản**. Nó cung cấp tài khoản và quy tắc cho [Phân bổ chi phí mua hàng](lcv-co-ban.md) sinh bút toán. Bút toán bù (Dr 1562 / Cr 1561) chỉ sinh khi ghi sổ phiếu phân bổ, nếu đã bật tùy chọn tương ứng tại đây.

## Tình huống đặc biệt & cảnh báo

- **Mã nội bộ phải duy nhất** — trùng mã sẽ bị chặn khi lưu.
- **% VAT NK khấu trừ phải trong khoảng 0–100** — ngoài khoảng sẽ bị chặn.
- Nếu **chưa đặt TK kho 1562**, phiếu phân bổ vẫn ghi sổ được nhưng hệ thống bỏ qua bút toán bù (kèm cảnh báo) → giá vốn theo VAS không tách đúng.
- Đơn vị **chưa tách TK 156** (vẫn dùng 156 phẳng) có thể để trống / tắt bút toán bù — hệ thống tự bỏ qua bút toán no-op.
- Một số loại phụ phí dùng cho cả mua hàng và sản xuất: nguồn là phiếu nhập kho mua hàng thì phụ phí tăng giá vốn hàng mua (1562); nguồn là phiếu nhập xuất kho sản xuất thì tăng giá thành sản phẩm (155/152).

## Báo cáo liên quan

- [Phân bổ chi phí mua hàng](lcv-co-ban.md): dùng các tài khoản và loại phụ phí khai ở đây.
- [Phân bổ chi phí hàng nhập khẩu](lcv-nhap-khau.md): dùng % VAT NK khấu trừ mặc định.
- [Phân bổ phụ phí vào giá vốn (cuối kỳ)](inventory-cost-reallocation.md): kết chuyển 1562 → 1561.

## FAQ

**Q: Đặt TK ghi Có mặc định cho từng loại phụ phí để làm gì?**
**A:** Khi kế toán chọn loại phụ phí trên phiếu, hệ thống tự điền tài khoản này — nhưng chỉ điền khi dòng chưa có tài khoản, nên kế toán vẫn có thể sửa tay (không bị ghi đè).

**Q: "TK kho mặc định" khác gì TK ghi Có của loại phụ phí?**
**A:** "TK ghi Có" là phía Có khi ghi nhận phụ phí (331/111...). "TK kho mặc định" (1562) là tài khoản đích của bút toán bù — nơi tách phụ phí ra khỏi TK giá mua (1561) theo VAS.
