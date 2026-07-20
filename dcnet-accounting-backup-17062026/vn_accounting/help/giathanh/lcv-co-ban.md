---
title: Phân bổ chi phí mua hàng
order: 1
summary: Cộng các chi phí vận chuyển, bốc dỡ, bảo hiểm... vào giá trị hàng tồn kho (152/156) theo VAS TT99/2025.
---

## Mục đích

Khi mua hàng, ngoài giá mua còn phát sinh chi phí liên quan trực tiếp đến lô hàng: vận chuyển, bốc dỡ, kho bãi, bảo hiểm, thuế nhập khẩu... Theo VAS TT99/2025, các chi phí này phải được cộng vào **giá gốc hàng tồn kho** (TK 152 với nguyên vật liệu, TK 156 với hàng hóa) chứ không hạch toán thẳng vào chi phí trong kỳ.

**Phiếu phân bổ chi phí mua hàng** cho phép:
- Ghi nhận các khoản phụ phí của một hoặc nhiều lô hàng đã nhập
- Tự động phân bổ phụ phí vào từng mặt hàng theo tỷ lệ (theo giá trị / số lượng / trọng lượng)
- Cập nhật đúng giá vốn (giá trị tồn kho) của từng mặt hàng

Dùng cho kế toán kho và kế toán mua hàng.

## Khi nào dùng

- Mua hàng trong nước có hóa đơn vận chuyển, bốc dỡ riêng (nhà vận chuyển xuất hóa đơn tách khỏi hóa đơn hàng).
- Mua hàng có chi phí bảo hiểm hàng hóa riêng.
- Mua hàng có chi phí kho bãi, lưu container.
- Hàng nhập khẩu có thuế nhập khẩu, thuế tiêu thụ đặc biệt, phí hải quan (xem bài [Phân bổ chi phí hàng nhập khẩu](lcv-nhap-khau.md)).
- Bất kỳ chi phí nào trực tiếp gắn với lô hàng và cần cộng vào giá tồn kho.

## Cách thực hiện

1. Vào **Giá thành → Phân bổ chi phí mua hàng** → bấm **+ Thêm**.
2. Chọn **Công ty** và **Ngày chứng từ** (nên trùng hoặc sau ngày nhận hàng).
3. Tab **Hàng hóa**: bấm **Lấy hàng hóa từ phiếu nhập** → chọn phiếu nhập kho / hóa đơn mua hàng đã ghi sổ. Hệ thống tự điền danh sách mặt hàng, số lượng, giá trị.
4. Tab **Chi phí** (mỗi dòng = 1 loại phụ phí):
   - Chọn **Loại chi phí** (vận chuyển, bốc dỡ, bảo hiểm...) → hệ thống tự điền tài khoản chi phí phù hợp theo cấu hình (xem [Cấu hình phân bổ chi phí mua hàng](lcv-allocation-settings.md)).
   - Nhập **Số tiền** từng dòng.
   - Chọn **Phương pháp phân bổ**: theo giá trị / số lượng / trọng lượng.
5. Bấm **Phân bổ** → hệ thống tính tỷ lệ và điền cột **Chi phí phân bổ** cho từng mặt hàng. Kiểm tra tổng chi phí phân bổ khớp tổng phụ phí.
6. Bấm **Ghi sổ**. Hệ thống cộng phụ phí vào giá tồn kho từng mặt hàng và sinh bút toán.

> Tài khoản đích để tách phụ phí (mặc định 1562) và việc tự lập bút toán bù được cấu hình tại **Cấu hình phân bổ chi phí mua hàng**.

## Định khoản tự động

Theo VAS TT99/2025, TK 156 tách thành **1561 — Giá mua hàng hóa** và **1562 — Chi phí thu mua hàng hóa**. Hệ thống ERP gốc chỉ cộng phụ phí vào tài khoản kho của mặt hàng (1561). Để khớp đúng VAS, hệ thống tự lập thêm một **bút toán bù** sau mỗi phiếu (cơ chế 2 lớp + kết chuyển cuối kỳ).

### Lớp 1 — Bút toán phiếu phân bổ (tự động khi ghi sổ)

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Vận chuyển / bốc dỡ / kho bãi / bảo hiểm hàng mua | **1561** (tăng giá tồn kho mặt hàng) | 331 hoặc 111/112 | Áp dụng cả mua nội địa và nhập khẩu |

### Lớp 2 — Bút toán bù (tự động ngay khi ghi sổ phiếu phân bổ)

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Chuyển phụ phí từ TK giá mua sang TK chi phí thu mua | **1562** | **1561** | Bút toán bù link tham chiếu về phiếu phân bổ; xem ở phần Bình luận của phiếu (có liên kết tới bút toán) |

→ Kết quả Sổ Cái: 1561 = +giá mua (từ phiếu nhập kho), 1562 = +tổng phụ phí, các TK chi phí gốc (331/111...) = −tổng phụ phí. Sổ kho (giá trị tồn) vẫn đúng vì hệ thống đã cập nhật đơn giá vốn mặt hàng bao gồm cả phụ phí.

### Lớp 3 — Kết chuyển phụ phí vào giá vốn cuối kỳ (thủ công)

Khi xuất kho, hệ thống ghi **Dr 632 / Cr 1561** theo full giá vốn (giá mua + phụ phí). Vì 1561 chỉ chứa phần giá mua nên càng xuất kho 1561 càng âm, trong khi 1562 chỉ tăng từ phiếu phân bổ. Cuối tháng/quý kế toán chạy [Phân bổ phụ phí vào giá vốn (cuối kỳ)](inventory-cost-reallocation.md) để lập bút toán **Dr 1561 / Cr 1562** đưa phần phụ phí của hàng đã xuất về giá vốn.

## Tình huống đặc biệt & cảnh báo

- **Chỉ phân bổ 1 lần cho 1 lô hàng** — không tạo 2 phiếu phân bổ cho cùng 1 phiếu nhập.
- **Chi phí phải trực tiếp gắn với lô hàng** — chi phí quản lý chung (điện, thuê văn phòng) không được cộng vào giá vốn hàng mua.
- **Hủy phiếu phân bổ → bút toán bù tự hủy** (hệ thống đảo dấu kèm).
- **Đơn vị chưa tách TK 156** (vẫn để 156 phẳng): bút toán bù sẽ là no-op (Nợ và Có cùng tài khoản, cùng số tiền) → hệ thống tự bỏ qua, không sinh bút toán thừa.
- **Chưa cấu hình TK 1562**: hệ thống cảnh báo và bỏ qua bút toán bù (phiếu vẫn ghi sổ bình thường) → mở **Cấu hình phân bổ chi phí mua hàng** để thiết lập.
- **Ngày chứng từ** nên trùng hoặc sau ngày nhận hàng.

## Báo cáo liên quan

- [Chi phí chờ phân bổ](landed-cost-pending-allocation.md): liệt kê các chi phí treo TK 1388 chưa được phân bổ vào giá vốn.
- [Phân bổ phụ phí vào giá vốn (cuối kỳ)](inventory-cost-reallocation.md): kết chuyển 1562 → 1561 theo tỷ trọng hàng đã xuất.
- [Cấu hình phân bổ chi phí mua hàng](lcv-allocation-settings.md): khai báo loại chi phí, TK mặc định, tách TK kho.
- [Phân bổ chi phí hàng nhập khẩu](lcv-nhap-khau.md): thuế NK và VAT NK.

## FAQ

**Q: Đã ghi sổ phiếu nhưng kiểm tra Sổ Cái thấy 1562 không tăng?**
**A:** Kiểm tra **Cấu hình phân bổ chi phí mua hàng** xem đã bật "Tự lập bút toán bù" và đã đặt TK kho mặc định (1562) chưa. Nếu cấu hình thiếu, hệ thống bỏ qua bút toán bù.

**Q: Tách phụ phí vào nhiều TK khác nhau cho từng dòng chi phí được không?**
**A:** Được. Trên mỗi dòng phụ phí có trường TK kho riêng — ví dụ vận chuyển vào 1562, thuế nhập khẩu vào 1561 — hệ thống gom theo TK đích khi lập bút toán bù.

**Q: Có cần xuất hóa đơn cho từng phụ phí không?**
**A:** Không. Phiếu này chỉ cộng phụ phí vào giá vốn; hóa đơn của nhà vận chuyển/bảo hiểm hạch toán riêng (thường là hóa đơn mua hàng treo 331).
