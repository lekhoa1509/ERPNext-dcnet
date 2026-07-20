---
title: Tiền gửi có kỳ hạn
order: 7
summary: Quản lý sổ tiền gửi có kỳ hạn (tiết kiệm) — tạo mới, theo dõi đáo hạn, ghi nhận lãi định kỳ.
---

## Mục đích

**Tiền gửi có kỳ hạn** là DocType quản lý các sổ tiền gửi có kỳ hạn (tiết kiệm có kỳ hạn, chứng chỉ tiền gửi) của doanh nghiệp. Mỗi sổ ghi nhận số tiền gửi, ngày gửi, ngày đáo hạn, lãi suất, lịch trả lãi, và tự động tạo bút toán điều chuyển khi ghi sổ.

## Các trường chính

### Thông tin sổ (Deposit Info)
- **Company**: Công ty sở hữu sổ (bắt buộc).
- **Bank**: Ngân hàng nơi mở sổ (Link → Bank doctype).
- **Bank Account**: Tài khoản ngân hàng nguồn tiền (Link → Bank Account, bắt buộc).
- **Deposit Number**: Số sổ tiết kiệm (tùy chọn).
- **Deposit Account (1281)**: Tài khoản kế toán ghi nhận tiền gửi có kỳ hạn (mặc định từ VN Accounting Settings).
- **Interest Income Account (515)**: Tài khoản ghi nhận lãi (mặc định từ VN Accounting Settings).
- **Interest Receivable Account**: Tài khoản lãi dự thu (mặc định từ VN Accounting Settings).

### Điều khoản (Terms)
- **Principal Amount**: Số tiền gửi (bắt buộc).
- **Annual Interest Rate (%)**: Lãi suất năm (Percent field, bắt buộc).
- **Interest Payment Type**: Phương thức trả lãi — chọn 1 trong 5 loại:
  - **End of Term**: Trả lãi 1 lần khi đáo hạn.
  - **Monthly**: Trả lãi hàng tháng.
  - **Quarterly**: Trả lãi hàng quý.
  - **Prepaid**: Trả lãi trước (khấu trừ vào gốc ngay khi gửi).
  - **Compound**: Lãi nhập gốc định kỳ (lãi kép).
- **Start Date**: Ngày gửi (bắt buộc).
- **Term (Months)**: Kỳ hạn, số tháng (Int, bắt buộc).
- **Maturity Date**: Ngày đáo hạn (tự động tính = Start Date + Term Months, read-only).
- **Early Withdrawal Rate (%)**: Lãi suất áp dụng khi rút trước hạn.

### Lịch lãi (Interest Schedule)
Child table **Term Deposit Interest** — hệ thống tự sinh khi lưu (trừ khi docstatus=1):
- **Due Date**: Ngày đến hạn trả lãi.
- **Interest Amount**: Số tiền lãi kỳ này.
- **Principal at Start**: Số dư gốc đầu kỳ.
- **Status**: Trạng thái dòng lịch — Pending → Draft Created → Booked.
- **Journal Entry**: Link đến phiếu kế toán ghi nhận lãi (sau khi booked).

### Tổng kết (Summary)
- **Total Interest**: Tổng lãi cả kỳ (tự động tính, read-only).
- **Status**: Trạng thái sổ — Draft → Active (sau submit) → Matured (đến hạn) → Settled / Early Settled → Cancelled.
- **Alert Days Before Maturity**: Số ngày cảnh báo trước đáo hạn (mặc định 7).

## Cách thực hiện

1. Bấm **Tiền gửi có kỳ hạn** trên menu Ngân hàng → danh sách sổ tiền gửi mở.
2. Bấm **+ Thêm** để tạo sổ mới → biểu mẫu Term Deposit mở.
3. Điền các trường bắt buộc: Company, Bank Account, Deposit Account, Interest Income Account, Principal Amount, Interest Rate, Interest Payment Type, Start Date, Term (Months).
4. Lưu → hệ thống tự động tính Maturity Date và sinh lịch lãi (Interest Schedule).
5. **Ghi sổ (Submit)** → hệ thống tự động:
   - Tạo bút toán điều chuyển (Nợ Deposit Account / Có Bank Account).
   - Cập nhật status = Active.
   - Lưu tên phiếu kế toán vào trường Deposit Journal Entry.

### Các thao tác sau khi ghi sổ (nút trên form)

- **Create Accrual**: Tạo bút toán dồn tích lãi cuối kỳ (Nợ Interest Receivable / Có Interest Income). Dùng cho kế toán dồn tích — ghi nhận lãi phát sinh trong kỳ dù chưa đến hạn trả.
- **Settle**: Tất toán sổ khi đáo hạn (hoặc trước hạn nếu nhập ngày < maturity_date). Tự động tạo bút toán tất toán và cập nhật status = Settled / Early Settled.
- **Renew**: Gia hạn — tạo sổ Term Deposit mới từ sổ đã đáo hạn (status = Matured). Nếu Interest Payment Type là Compound hoặc End of Term, lãi được nhập vào gốc sổ mới.

## Định khoản

Khi ghi sổ (on_submit), hệ thống tạo bút toán với các tài khoản được cấu hình trong chính sổ đó (deposit_account, bank_account):

| Giai đoạn | TK Nợ | TK Có | Phương thức |
|---|---|---|---|
| Gửi tiền (submit) | deposit_account | bank_account | `create_deposit_je()` |
| Dồn tích lãi (accrual) | interest_receivable_account | interest_income_account | `create_accrual(date)` |
| Tất toán (settle) | bank_account | deposit_account + interest_income_account | `settle(date)` |

## Tình huống đặc biệt & cảnh báo

- **Lịch lãi không đổi sau khi ghi sổ:** Sau khi submit (docstatus=1), `_build_schedule()` return sớm — lịch lãi không bị ghi đè khi lưu lại.
- **Rút trước hạn (Early Settled):** Gọi `settle(settlement_date)` với ngày < maturity_date. Lãi suất áp dụng là Early Withdrawal Rate thay vì lãi suất gốc.
- **Gia hạn (Renew):** Chỉ khả dụng khi status = Matured. Với loại Compound hoặc End of Term, lãi lũy kế được nhập vào gốc sổ mới.
- **Sổ mở bằng ngoại tệ:** Tạo Deposit Account riêng cho ngoại tệ. Tỷ giá ghi nhận theo ngày gửi.
- **Tài khoản mặc định:** Nếu chưa chọn deposit_account / interest_income_account / interest_receivable_account, hệ thống tự lấy từ VN Accounting Settings (nếu có).

## Báo cáo liên quan

- **Sổ Tài khoản ngân hàng**: sổ chi tiết TK 112 (theo dõi tiền ra khi gửi).
- **Sổ cái kế toán**: chi tiết Deposit Account, TK 515.

## FAQ

**Q: Tiền gửi có kỳ hạn có ghi vào TK 112 không?**
**A:** Không. TK 112 là tiền gửi thanh toán (không kỳ hạn). Tiền gửi có kỳ hạn ghi vào Deposit Account (thường là TK 128x) — tài khoản này do kế toán chọn trên form.

**Q: Lịch lãi (Interest Schedule) có tự động cập nhật không?**
**A:** Có, khi lưu bản nháp. Sau khi ghi sổ (submit), lịch lãi được khóa — không thay đổi khi lưu lại. Các dòng lịch lãi chuyển trạng thái: Pending → Draft Created (khi tạo JE nháp) → Booked (khi ghi sổ JE).

**Q: Khi nào dùng Create Accrual?**
**A:** Cuối kỳ kế toán (tháng/quý/năm), nếu lãi đã phát sinh nhưng chưa đến hạn trả (với loại End of Term hoặc Quarterly), dùng Create Accrual để ghi nhận lãi dự thu — đảm bảo nguyên tắc dồn tích.

**Q: Có cần tạo bút toán riêng khi mở sổ không?**
**A:** Không — hệ thống tự động tạo bút toán điều chuyển khi ghi sổ (submit). Phiếu kế toán được lưu vào trường Deposit Journal Entry.

**Q: Lãi suất rút trước hạn (Early Withdrawal Rate) dùng khi nào?**
**A:** Khi gọi `settle(settlement_date)` với ngày tất toán < maturity_date, hệ thống áp dụng Early Withdrawal Rate thay vì lãi suất gốc để tính lãi thực nhận.
