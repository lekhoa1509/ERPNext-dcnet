---
title: Doanh thu chưa thực hiện (3387)
order: 5
summary: Lịch phân bổ doanh thu khách trả trước nhiều kỳ — kết chuyển dần TK 3387 sang TK 511 theo VAS.
---

## Mục đích

**Lịch doanh thu chưa thực hiện** quản lý việc phân bổ doanh thu khi khách **trả tiền trước cho dịch vụ kéo dài nhiều kỳ** (cước Internet, hosting, giấy phép phần mềm, bảo trì cả năm). Theo VAS, khoản tiền nhận trước chưa được tính hết vào doanh thu ngay mà ghi vào **TK 3387 "Doanh thu chưa thực hiện"**, rồi **kết chuyển dần sang TK 511** theo từng kỳ đã hoàn thành nghĩa vụ.

Lịch này tự sinh các kỳ ghi nhận và tạo bút toán Nợ 3387 / Có 511 cho mỗi kỳ.

## Khi nào dùng

- Khách trả trước cước/dịch vụ cho nhiều tháng/quý/năm.
- Bán giấy phép phần mềm, gói bảo trì, hợp đồng dịch vụ trọn gói trả trước.
- Cần phân bổ doanh thu đều theo thời gian thay vì ghi nhận một lần.

## Cách thực hiện

### Cách 1 — Tạo từ hóa đơn bán hàng (khuyến nghị)

1. Mở **hóa đơn bán hàng** đã ghi sổ → **"Hành động > + Lịch ghi nhận DT chưa thực hiện"**.
2. Trong hộp thoại, nhập:
   - **Ngày bắt đầu / Ngày kết thúc** (khoảng thời gian dịch vụ).
   - **Tổng số tiền hoãn lại** (mặc định = tổng tiền hóa đơn; sửa lại nếu chỉ một phần là trả trước).
   - **Phương pháp phân bổ**: Theo tháng / Theo quý / Theo ngày / Một lần.
   - **TK doanh thu sẽ ghi nhận** (TK 511 — ví dụ 5111, 51131–51136).
   - **TK doanh thu chưa thực hiện** (mặc định TK 3387 lấy từ Cài đặt kế toán).
3. Bấm **"Tạo lịch + Sinh các kỳ"** → hệ thống tạo lịch, sinh các kỳ và ghi sổ luôn.

### Cách 2 — Tạo lịch độc lập

1. Mở **Doanh thu chưa thực hiện (3387)** → "+ Thêm".
2. Điền **Công ty, Khách hàng, Ngày bắt đầu, Ngày kết thúc, Tổng số tiền hoãn lại**, chọn **TK doanh thu chưa thực hiện** và **TK doanh thu sẽ ghi nhận**.
3. Bấm **"Hành động > Sinh lịch tự động"** để tạo các dòng kỳ ghi nhận (số tiền chia đều, phần lẻ dồn vào kỳ cuối).
4. Kiểm tra tổng các kỳ = tổng số tiền hoãn lại → **Ghi sổ** (trạng thái chuyển sang "Đang chạy").

### Ghi nhận từng kỳ

- Khi đến kỳ, mở lịch (đã ghi sổ) → **"Hành động > Ghi nhận tất cả kỳ đến hạn"** → nhập ngày → hệ thống tạo bút toán cho mọi kỳ có ngày kết thúc ≤ ngày chọn.
- Khi tất cả kỳ đã ghi nhận, trạng thái tự chuyển **"Hoàn tất"**.

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Khách trả trước (chứng từ gốc) | 131 / 112 | 3387 | Ghi nhận khoản nhận trước |
| Kết chuyển doanh thu từng kỳ | 3387 | 511 | Mỗi kỳ một bút toán, theo lịch |

- Bút toán kết chuyển kỳ kèm tham chiếu hóa đơn nguồn (nếu tạo từ hóa đơn) và đối tượng khách hàng.
- Số tiền phân bổ chia đều cho số kỳ; **phần lẻ làm tròn dồn vào kỳ cuối** để tổng các kỳ đúng bằng tổng số tiền hoãn lại.

## Tình huống đặc biệt & cảnh báo

- **Phải sinh lịch trước khi ghi sổ:** chưa bấm "Sinh lịch tự động" thì không ghi sổ được — hệ thống cảnh báo.
- **Tổng các kỳ phải khớp:** tổng số tiền các kỳ phải bằng tổng số tiền hoãn lại (sai lệch cho phép ≤ 1 đồng), nếu không sẽ chặn ghi sổ.
- **TK phải là chi tiết, cùng công ty:** cả TK 3387 và TK doanh thu phải là tài khoản chi tiết (không phải tài khoản tổng hợp) và thuộc đúng công ty.
- **Hủy lịch:** khi hủy, các bút toán kết chuyển đã ghi sổ của lịch sẽ **tự động hủy theo** — số dư TK 3387 trở lại như cũ.
- **Một phần là trả trước:** nếu hóa đơn vừa có phần giao ngay vừa có phần trả trước, chỉ nhập **phần trả trước** vào "Tổng số tiền hoãn lại".
- **Ghi nhận tự động định kỳ:** hệ thống có thể tự ghi nhận các kỳ đến hạn cho mọi lịch đang chạy (chạy nền theo lịch) — kế toán chỉ cần kiểm tra kết quả.

## Báo cáo liên quan

- [Hóa đơn bán hàng](hoa-don-ban-hang.md): chứng từ gốc tạo khoản trả trước.
- **Sổ Cái** (phân hệ Tổng hợp): theo dõi phát sinh và số dư TK 3387, 511.
- [BC bán hàng](bc-ban-hang.md): doanh số sau khi đã phân bổ.

## FAQ

**Q: TK 3387 là gì?**
**A:** "Doanh thu chưa thực hiện" — khoản tiền khách trả trước cho dịch vụ tương lai, chưa đủ điều kiện ghi vào doanh thu (TK 511) ngay. Phân bổ dần sang TK 511 theo từng kỳ hoàn thành nghĩa vụ.

**Q: Phương pháp "Một lần" dùng khi nào?**
**A:** Khi muốn ghi nhận toàn bộ vào một thời điểm cuối (ví dụ nghiệm thu một lần) — lịch chỉ có 1 kỳ.

**Q: Lỡ ghi nhận sai kỳ thì sao?**
**A:** Hủy lịch → các bút toán kết chuyển tự hủy theo → tạo lại lịch mới với thông số đúng.

**Q: Khoản trả trước có tính thuế GTGT không?**
**A:** Thuế GTGT xử lý trên hóa đơn gốc tại thời điểm phát hành; lịch này chỉ phân bổ phần **doanh thu** (3387 → 511), không tác động TK 3331.
