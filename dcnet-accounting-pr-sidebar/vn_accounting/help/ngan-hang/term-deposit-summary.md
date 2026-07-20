---
title: Tổng hợp tiền gửi có kỳ hạn
order: 1
summary: Báo cáo tổng hợp các khoản tiền gửi có kỳ hạn (TK 1281) — gốc, lãi suất, ngày gửi, ngày đáo hạn, lãi đã hạch toán.
---

## Mục đích

Báo cáo cho kế toán cái nhìn tổng quan các khoản tiền gửi có kỳ hạn (TK 1281): đang còn bao nhiêu khoản, gốc bao nhiêu, lãi suất, ngày đáo hạn sắp tới, lãi đã ghi nhận và lãi còn phải hạch toán. Hỗ trợ 3 chế độ xem cho 3 mục đích nghiệp vụ khác nhau.

## Khi nào dùng

- Cuối tháng/quý tổng hợp số dư các khoản gửi để chốt sổ.
- Đầu tuần/tháng kiểm tra các khoản sắp đáo hạn (cột "Số ngày tới đáo hạn" highlighted cam khi ≤30 ngày, đỏ khi đã quá hạn).
- Đối chiếu tổng số dư báo cáo với Sổ tài khoản 1281.
- Cung cấp cho kiểm toán viên danh sách đầy đủ các khoản gửi đầu kỳ + cuối kỳ + lãi phát sinh.

## 3 chế độ xem

| Chế độ | Lọc theo | Use case |
|---|---|---|
| Đang gửi tại ngày (mặc định) | Tất cả các khoản start_date ≤ Đến ngày, lọc thêm theo Trạng thái | Snapshot — "tại ngày X có những khoản gửi nào còn hiệu lực" |
| Phát sinh trong kỳ | start_date BETWEEN Từ ngày AND Đến ngày | "Trong kỳ này có khoản gửi nào mới mở" |
| Đáo hạn trong kỳ | maturity_date BETWEEN Từ ngày AND Đến ngày | "Trong kỳ này có khoản gửi nào đáo hạn cần xử lý" |

## Cột báo cáo

- **Số phiếu / Số sổ TK / Ngân hàng / TK 1281**: chứng từ và TK kế toán.
- **Gốc**: principal_amount đã gửi.
- **Lãi suất % / Kỳ hạn / Ngày gửi / Ngày đáo hạn**: thông số khoản gửi.
- **Số ngày tới đáo hạn**: tự tính từ Đến ngày (filter). Cam khi ≤30 ngày, đỏ khi âm (đã quá hạn).
- **Hình thức trả lãi**: End of Term / Monthly / Quarterly / Prepaid / Compound.
- **Tổng lãi dự kiến**: total_interest đã được tính khi tạo phiếu.
- **Lãi đã hạch toán**: Σ Term Deposit Interest có status='Booked' AND due_date ≤ Đến ngày.
- **Lãi còn phải hạch toán**: Tổng lãi dự kiến − Lãi đã hạch toán.
- **Trạng thái**: Active / Matured / Settled / Early Settled / Cancelled.

## Lưu ý

- Báo cáo CHỈ tính các phiếu đã submit (docstatus=1). Phiếu Draft không xuất hiện.
- Cột "Lãi đã hạch toán" lấy từ child table Term Deposit Interest có status='Booked' — tức đã có Bút toán Dr 138 / Cr 515 ghi nhận. Phiếu lãi ở trạng thái Draft Created (chưa submit) không tính.
- Tổng cột (totals row) chỉ có ý nghĩa cho các cột số liệu (Gốc, Tổng lãi, Lãi đã hạch toán, Lãi còn phải hạch toán).

## Xem thêm

- [Tổng hợp khoản vay ngân hàng](bank-loan-summary.md) — báo cáo song song cho TK 3411 (vay).
