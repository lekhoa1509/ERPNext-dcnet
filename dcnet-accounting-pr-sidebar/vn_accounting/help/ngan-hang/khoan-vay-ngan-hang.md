---
title: Khoản vay ngân hàng
order: 9
summary: Quản lý khoản vay ngân hàng — tạo mới, theo dõi lịch trả nợ gốc + lãi, cập nhật lãi suất thả nổi.
---

## Mục đích

**Khoản vay ngân hàng** là DocType quản lý các khoản vay của doanh nghiệp tại ngân hàng. Mỗi khoản vay ghi nhận số tiền vay, ngày giải ngân, lãi suất (cố định hoặc thả nổi), lịch trả nợ, và tự động tạo bút toán giải ngân khi ghi sổ.

## Các trường chính

### Thông tin khoản vay (Loan Info)
- **Company**: Công ty vay (bắt buộc).
- **Bank**: Ngân hàng cho vay (Link → Bank doctype). **Không cần tạo Nhà cung cấp** — dùng trực tiếp Bank doctype.
- **Bank Account**: Tài khoản ngân hàng nhận tiền giải ngân (Link → Bank Account, bắt buộc).
- **Loan Account (3411)**: Tài khoản kế toán ghi nhận nợ vay (bắt buộc, mặc định từ VN Accounting Settings).
- **Loan Number**: Số hợp đồng vay (tùy chọn).
- **Interest Expense Account (635)**: Tài khoản chi phí lãi vay (bắt buộc, mặc định từ VN Accounting Settings).
- **Interest Payable Account**: Tài khoản lãi phải trả (mặc định từ VN Accounting Settings).
- **Rate Type**: Loại lãi suất — **Fixed** (cố định) hoặc **Floating** (thả nổi).

### Điều khoản (Terms)
- **Loan Amount**: Số tiền vay (bắt buộc).
- **Outstanding Amount**: Dư nợ còn lại (read-only, tự động cập nhật).
- **Annual Interest Rate (%)**: Lãi suất năm (Percent field, bắt buộc).
- **Repayment Type**: Phương thức trả nợ — chọn 1 trong 2 loại:
  - **Interest Only**: Trả lãi định kỳ, gốc trả 1 lần khi đáo hạn.
  - **EMI**: Trả góp đều hàng kỳ (gốc + lãi bằng nhau mỗi kỳ).
- **Disbursement Date**: Ngày giải ngân (bắt buộc).
- **Maturity Date**: Ngày đáo hạn (bắt buộc).
- **Repayment Frequency**: Tần suất trả nợ — Monthly hoặc Quarterly.

### Lịch trả nợ (Repayment Schedule)
Child table **Bank Loan Repayment** — hệ thống tự sinh khi lưu (trừ khi docstatus=1):
- **Due Date**: Ngày đến hạn trả.
- **Principal Amount**: Gốc phải trả kỳ này.
- **Interest Amount**: Lãi phải trả kỳ này.
- **Total Amount**: Tổng phải trả kỳ này (= gốc + lãi).
- **Outstanding After**: Dư nợ còn lại sau kỳ này.
- **Status**: Trạng thái dòng — Pending → Draft Created → Booked.
- **Journal Entry**: Link đến phiếu kế toán trả nợ (sau khi booked).

### Tổng kết (Summary)
- **Total Interest**: Tổng lãi cả kỳ (tự động tính, read-only).
- **Total Repayment**: Tổng phải trả (= gốc + lãi, read-only).
- **Status**: Trạng thái khoản vay — Draft → Active (sau submit) → Matured → Settled → Cancelled.

## Cách thực hiện

1. Bấm **Khoản vay ngân hàng** trên menu Ngân hàng → danh sách khoản vay mở.
2. Bấm **+ Thêm** để tạo khoản vay mới → biểu mẫu Bank Loan mở.
3. Điền các trường bắt buộc: Company, Bank Account, Loan Account, Interest Expense Account, Loan Amount, Interest Rate, Repayment Type, Disbursement Date, Maturity Date, Repayment Frequency.
4. Lưu → hệ thống tự động sinh lịch trả nợ (Repayment Schedule).
5. **Ghi sổ (Submit)** → hệ thống tự động:
   - Tạo bút toán giải ngân (Nợ Bank Account / Có Loan Account).
   - Cập nhật status = Active, Outstanding Amount = Loan Amount.
   - Lưu tên phiếu kế toán vào trường Disbursement Journal Entry.

### Các thao tác sau khi ghi sổ (nút trên form)

- **Create Accrual**: Tạo bút toán dồn tích lãi cuối kỳ (Nợ Interest Expense / Có Interest Payable). Ghi nhận lãi phát sinh trong kỳ dù chưa đến hạn trả.
- **Settle Early**: Tất toán trước hạn — trả toàn bộ dư nợ gốc + lãi pro-rata đến ngày tất toán. Cập nhật status = Settled, Outstanding Amount = 0.
- **Update Rate**: Cập nhật lãi suất mới (chỉ áp dụng cho Rate Type = Floating). Hệ thống giữ nguyên các dòng đã Booked, sinh lại lịch trả nợ cho các dòng Pending từ ngày hiệu lực.

## Định khoản

| Giai đoạn | TK Nợ | TK Có | Phương thức |
|---|---|---|---|
| Giải ngân (submit) | bank_account | loan_account | `create_disbursement_je()` |
| Dồn tích lãi (accrual) | interest_expense_account | interest_payable_account | `create_accrual(date)` |
| Tất toán trước hạn (settle_early) | loan_account + interest_expense | bank_account | `settle_early(date)` |
| Cập nhật lãi suất (update_rate) | (không tạo JE) | — | `update_rate(new_rate, date)` |

## Tình huống đặc biệt & cảnh báo

- **Lịch trả nợ không đổi sau khi ghi sổ:** Sau khi submit, `_build_schedule()` return sớm — lịch trả nợ không bị ghi đè khi lưu lại.
- **Interest Only vs EMI:** Với Interest Only, gốc trả 1 lần vào kỳ cuối (outstanding_after = 0 ở dòng cuối). Với EMI, tổng phải trả mỗi kỳ bằng nhau nhưng tỷ lệ gốc/lãi thay đổi (gốc tăng dần, lãi giảm dần).
- **Lãi suất thả nổi (Floating):** Dùng `update_rate()` khi ngân hàng điều chỉnh lãi suất. Hệ thống giữ nguyên các kỳ đã trả (Booked), tính lại lịch cho các kỳ còn lại dựa trên dư nợ hiện tại và lãi suất mới.
- **Tài khoản mặc định:** Nếu chưa chọn loan_account / interest_expense_account / interest_payable_account, hệ thống tự lấy từ VN Accounting Settings.
- **Không có logic phạt trả trước:** `settle_early()` chỉ tính gốc + lãi pro-rata, không áp dụng phí phạt. Nếu ngân hàng có phí phạt, kế toán cần tự tạo thêm 1 dòng phí (Nợ 642x / Có bank_account).
- **Vay ngoại tệ:** Loan Account cần là tài khoản ngoại tệ riêng. Tỷ giá ghi nhận theo ngày giải ngân.

## Báo cáo liên quan

- **Sổ Tài khoản ngân hàng**: sổ chi tiết TK 112 (theo dõi nhận giải ngân và trả nợ).
- **Sổ cái kế toán**: chi tiết Loan Account (341x), TK 635.
- **Báo cáo lãi lỗ**: TK 635 (chi phí lãi vay) trong kỳ.

## FAQ

**Q: Cần tạo Nhà cung cấp cho ngân hàng không?**
**A:** Không — Bank Loan dùng trường **Bank** (Link → Bank doctype) để chọn ngân hàng. Không cần tạo Supplier. Bank doctype đã có sẵn trong hệ thống ERP.

**Q: Khi nào dùng Interest Only vs EMI?**
**A:** Interest Only phù hợp với vay lưu động (hạn mức) — trả lãi hàng tháng, gốc trả khi đáo hạn. EMI phù hợp với vay trung dài hạn trả góp — gốc và lãi trả đều mỗi kỳ.

**Q: Làm sao để cập nhật lãi suất khi ngân hàng thay đổi?**
**A:** Chọn Rate Type = Floating khi tạo khoản vay. Khi có thay đổi, mở form khoản vay → nút **Update Rate** → nhập lãi suất mới và ngày hiệu lực. Hệ thống tự động tính lại lịch trả nợ cho các kỳ chưa trả.

**Q: Lịch trả nợ có tự động tạo bút toán không?**
**A:** Không — lịch trả nợ là công cụ theo dõi. Kế toán viên cần tạo Bank Entry thủ công vào mỗi kỳ trả nợ, sau đó cập nhật trạng thái dòng lịch thành Booked.

**Q: Trả nợ gốc + lãi cùng lúc — ghi 1 hay 2 bút toán?**
**A:** 1 Bank Entry với 2 dòng Nợ: Loan Account (gốc) và Interest Expense Account (lãi) + 1 dòng Có Bank Account.
