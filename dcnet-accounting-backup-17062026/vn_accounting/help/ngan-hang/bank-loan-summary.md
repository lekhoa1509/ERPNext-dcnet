---
title: Tổng hợp khoản vay ngân hàng
order: 2
summary: Báo cáo tổng hợp các khoản vay ngân hàng (TK 3411) — lịch trả nợ định kỳ, toàn cảnh các khoản đang vay, và các khoản đáo hạn trong kỳ.
---

## Mục đích

Báo cáo cho kế toán theo dõi các khoản vay ngân hàng (TK 3411) ở 3 mức độ chi tiết khác nhau: theo từng kỳ trả nợ, toàn cảnh tất cả các khoản đang vay, và các khoản sắp đáo hạn (tất toán). Đặc biệt phục vụ quy trình "ngày 1 và 15 hàng tháng kiểm tra các khoản tới hạn trả nợ".

## Khi nào dùng

- **Đầu tuần / nửa tháng (1 và 15)**: chế độ "Lịch trả nợ trong kỳ" — biết trong 7-15 ngày tới có bao nhiêu kỳ trả nợ, tổng số tiền cần chi, có khoản nào quá hạn chưa hạch toán.
- **Cuối tháng / quý**: chế độ "Đang vay (toàn cảnh)" — chốt tổng outstanding TK 3411, đối chiếu với Sổ tài khoản.
- **Lập kế hoạch dòng tiền dài hạn**: chế độ "Đáo hạn trong kỳ" — nắm các khoản vay sẽ đáo hạn trong 3-6 tháng tới để chuẩn bị nguồn vốn tất toán hoặc thương lượng gia hạn.

## 3 chế độ xem

| Chế độ | Cấp dữ liệu | Use case |
|---|---|---|
| Lịch trả nợ trong kỳ (mặc định) | 1 row / kỳ trả nợ trong khoảng Từ–Đến ngày | "Trong 15 ngày tới có kỳ trả nợ nào, gốc bao nhiêu, lãi bao nhiêu" |
| Đang vay (toàn cảnh) | 1 row / khoản vay (không lọc theo ngày) | "Hiện đang vay những khoản nào, outstanding bao nhiêu, đã trả tới đâu" |
| Đáo hạn trong kỳ | 1 row / khoản vay có maturity_date trong khoảng | "Có khoản vay nào đáo hạn trong 6 tháng tới cần chuẩn bị nguồn" |

## Cột báo cáo

### Chế độ "Lịch trả nợ trong kỳ" (mặc định)

- **Số phiếu vay / Ngân hàng / Số HĐ vay**: liên kết về phiếu Bank Loan cha.
- **Ngày đến hạn trả**: due_date của kỳ trả nợ.
- **Số ngày tới hạn**: tự tính từ today. **Đỏ ⚠** khi quá hạn AND chưa Booked. **Cam** khi ≤7 ngày.
- **Gốc kỳ này / Lãi kỳ này / Tổng phải trả**: số tiền của kỳ trả nợ.
- **Số dư sau trả**: outstanding_after — số dư còn lại sau khi trả kỳ này.
- **JE đã hạch toán**: link tới Bút toán đã tạo cho kỳ trả này (nếu đã booked).
- **Trạng thái kỳ**: Pending / Draft Created / Booked.
- **Trạng thái khoản vay**: Active / Matured / Settled / Cancelled (của parent Bank Loan).

### Chế độ "Đang vay (toàn cảnh)" và "Đáo hạn trong kỳ"

- **Số phiếu vay / Ngân hàng / Số HĐ / TK vay (3411)**.
- **Ngày giải ngân / Ngày đáo hạn**.
- **Số ngày tới đáo hạn**: cam ≤30 ngày, đỏ khi âm.
- **Số tiền vay / Outstanding**: số đã giải ngân và số dư còn lại.
- **Lãi suất % / Loại lãi**: Fixed hay Floating.
- **Hình thức trả / Tần suất**: Interest Only vs EMI; Monthly vs Quarterly.
- **Đã trả / Tổng kỳ**: tiến độ kỳ trả (vd "8 / 24" = đã trả 8 trong 24 kỳ).
- **Trạng thái**.

## Lưu ý

- Báo cáo CHỈ tính các phiếu vay đã submit (docstatus=1). Bank Loan ở trạng thái Draft không xuất hiện.
- Trong chế độ "Lịch trả nợ trong kỳ", nếu để trống "Từ ngày" thì hệ thống sẽ liệt kê tất cả các kỳ có due_date ≤ "Đến ngày" — kể cả các kỳ quá hạn xa lâu nay chưa hạch toán. Đặt "Từ ngày" để giới hạn phạm vi.
- Cột "Số ngày tới hạn" trong "Lịch trả nợ" tính so với hôm nay (today) chứ không so với "Đến ngày" của filter — phản ánh đúng hiện trạng quá hạn / sắp tới hạn.

## Xem thêm

- [Tổng hợp tiền gửi có kỳ hạn](term-deposit-summary.md) — báo cáo song song cho TK 1281 (gửi).
