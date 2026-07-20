---
title: Cấu hình BCTC Mapping
order: 12
summary: Màn hình sửa công thức tính từng chỉ tiêu B01/B02/B03 — cú pháp công thức tài khoản, cách tính, khôi phục mặc định TT99/2025.
---

## Mục đích

**BCTC Mapping** ánh xạ **mã chỉ tiêu** trong báo cáo TT99/2025 (B01/B02/B03) sang **tài khoản kế toán** hoặc **công thức tính** từ các mã khác. Mỗi công ty có một bản mapping riêng. Hệ thống đã cài sẵn công thức theo TT99/2025 — phần lớn doanh nghiệp dùng hệ thống tài khoản chuẩn **không cần sửa gì**.

## Khi nào dùng

Chỉ sửa khi doanh nghiệp có cấu trúc tài khoản đặc thù:

- DN mở tài khoản chi tiết khác chuẩn cần đưa vào đúng chỉ tiêu.
- Chính sách kế toán nội bộ khác mặc định.
- Có thông tư/quy định ngành mới cần cập nhật.
- B01 mất cân đối do tài khoản mới chưa được map.

## Cách thực hiện

1. Vào **Báo cáo tài chính → Cấu hình BCTC Mapping**, mở bản mapping của công ty.
2. Bảng chia 3 nhóm: **B01-DN**, **B02-DN**, **B03-DN** — mỗi dòng là một chỉ tiêu.
3. Sửa trực tiếp trên dòng cần điều chỉnh, rồi **Lưu**.
4. Chạy lại báo cáo B01/B02/B03 để xem hiệu lực.

Mỗi dòng có các trường:

| Trường | Ý nghĩa |
|---|---|
| **Mã** | Mã chỉ tiêu (110, 120, 01, ...) |
| **Tên chỉ tiêu** | Nhãn hiển thị trên báo cáo |
| **Cách tính** (value_type) | Chọn cách lấy số liệu (xem bảng dưới) |
| **TK / Mã** (account_formula) | Công thức tài khoản |
| **Công thức mã** (line_formula) | Chỉ dùng khi Cách tính = formula |
| **Thụt lề** | Cấp bậc hiển thị |
| **Dòng tổng** | Tick để in đậm dòng tổng |
| **Hệ số dấu** | +1 giữ nguyên, −1 đảo dấu |

### Cú pháp công thức tài khoản

| Cú pháp | Ý nghĩa |
|---|---|
| `+111` | Lấy TK 111 đúng prefix (không tự match TK con) |
| `+111%` | Lấy TK 111 **và mọi TK con** (1111, 1112...) — `%` là ký tự đại diện |
| `+111,+112,+113` | Cộng tổng số dư 3 tài khoản |
| `+511,-521` | Cộng TK 511, trừ TK 521 (giảm trừ doanh thu) |

> Lưu ý: trong hệ thống này, `+111` (không có `%`) vẫn được hiểu là mẫu khớp đầu chuỗi `111` — nhưng để chắc chắn bao trùm tài khoản con, nên dùng `+111%`.

### Công thức mã (chỉ khi Cách tính = formula)

| Cú pháp | Ý nghĩa |
|---|---|
| `=110+120+130` | Cộng giá trị mã 110, 120, 130 đã tính ở dòng khác |
| `=100+200` | Mã 270 = mã 100 + mã 200 (Tổng tài sản) |

### Các cách tính (value_type)

| Mã | Khi nào dùng |
|---|---|
| `closing_debit` | Số dư cuối kỳ bên Nợ (tài sản: 111, 131, 156...) |
| `closing_credit` | Số dư cuối kỳ bên Có (nợ phải trả/vốn: 331, 333, 411, 421...) |
| `period_debit` | Tổng phát sinh Nợ trong kỳ (loại bút toán kết chuyển) — chi phí trong P&L |
| `period_credit` | Tổng phát sinh Có trong kỳ — doanh thu trong P&L |
| `period_net` | PS Có − PS Nợ trong kỳ — gộp lãi/lỗ một dòng |
| `net_credit` | Lũy kế Có − Nợ (có dấu) — dùng cho TK 4211 có thể âm (lỗ) |
| `net_debit` | Lũy kế Nợ − Có (có dấu) — đối ứng net_credit |
| `delta_debit` | Số dư Nợ cuối kỳ − đầu kỳ — dùng cho B03 (∆phải thu, ∆hàng tồn) |
| `delta_credit` | Số dư Có cuối kỳ − đầu kỳ — dùng cho B03 (∆phải trả, ∆vay) |
| `formula` | Tính từ mã khác qua công thức mã (`=01+02+...`) |

### Ba cách khôi phục/sao chép

- **Khôi phục mặc định TT99/2025:** chọn báo cáo (B01/B02/B03), khôi phục toàn bộ hoặc một số mã cụ thể về công thức chuẩn của khuôn mẫu (theo loại COA của công ty — vd doanh nghiệp lớn / thương mại nhỏ).
- **Sao chép từ công ty khác:** nếu nhiều công ty con cùng cấu trúc, sao chép B01/B02/B03 từ mapping của công ty nguồn.

## Định khoản tự động

Màn hình này **không tạo bút toán — chỉ cấu hình công thức báo cáo**. Việc sửa mapping chỉ ảnh hưởng cách hiển thị/tính số liệu trên B01/B02/B03, không thay đổi dữ liệu Sổ Cái.

## Tình huống đặc biệt & cảnh báo

- **Mỗi tài khoản chỉ nên xuất hiện ở 1 chỉ tiêu** trong cùng một báo cáo — nếu xuất hiện ở 2 chỉ tiêu, tổng tài sản bị tính đôi → B01 mất cân.
- **Mọi tài khoản đều phải được map:** tài khoản không nằm trong chỉ tiêu nào sẽ không lên báo cáo → ảnh hưởng cân bằng B01.
- **Thêm tài khoản mới nhớ kiểm tra mapping:** khi mở tài khoản mới, xác minh nó đã được bao gồm (qua wildcard `%` hoặc thêm thủ công).
- **Chọn đúng Cách tính:** tài sản dùng `closing_debit`, nợ/vốn dùng `closing_credit`, P&L dùng `period_*`, B03 dùng `delta_*`. Chọn sai → số liệu sai dấu hoặc sai kỳ.
- **Sau khi sửa luôn chạy lại báo cáo và kiểm tra Mã 270 = Mã 440.**

## Báo cáo liên quan

- [B01 — Tình hình tài chính](b01-cau-truc.md), [B02 — Kết quả HĐKD](b02-ket-qua-kinh-doanh.md), [B03 — Lưu chuyển tiền tệ](b03-luu-chuyen-tien-te.md).
- [Bảng cân đối số phát sinh](bang-can-doi-so-phat-sinh.md) — đối chiếu số dư từng tài khoản.

## FAQ

**Q: Tôi tách TK 111 thành 1111/1112, mã 110 có tự gồm cả không?**
**A:** Có nếu công thức dùng wildcard `+111%`. Nếu công thức là `+111` thuần, hãy đổi sang `+111%` để chắc chắn bao gồm tài khoản con.

**Q: Lỡ sửa sai hết, về mặc định thế nào?**
**A:** Dùng "Khôi phục mặc định TT99/2025" — chọn báo cáo và khôi phục toàn bộ hoặc từng mã cụ thể.

**Q: Sửa mapping có làm thay đổi số liệu sổ sách không?**
**A:** Không. Mapping chỉ đổi cách báo cáo gom số từ các tài khoản, không động đến bút toán hay số dư thực tế.
