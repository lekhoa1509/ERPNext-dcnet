---
title: Năm tài chính
order: 4
summary: Khai báo năm tài chính (kỳ kế toán năm) để hệ thống xác định khung thời gian ghi sổ, kết chuyển và lập báo cáo tài chính.
---

## Mục đích

**Năm tài chính** khai báo khoảng thời gian một năm kế toán của công ty (ngày bắt đầu — ngày kết thúc). Mọi chứng từ ghi sổ phải nằm trong một năm tài chính đã khai; báo cáo tài chính, kết chuyển cuối kỳ và các báo cáo so sánh đều dựa vào khung năm tài chính này.

## Khi nào dùng

- **Khi mới triển khai:** tạo năm tài chính hiện tại (và năm trước nếu nhập số dư đầu kỳ/dữ liệu lịch sử).
- **Đầu mỗi năm:** tạo năm tài chính mới trước khi ghi chứng từ của năm đó.
- **Khi nhập dữ liệu chuyển đổi (migration):** tạo các năm tài chính quá khứ tương ứng với dữ liệu lịch sử.

## Cách thực hiện

1. Mở **Năm tài chính** trên menu Thiết lập.
2. Bấm **+ Thêm**:
   - **Tên năm tài chính:** thường đặt theo năm dương lịch, ví dụ `2026`.
   - **Ngày bắt đầu năm:** với doanh nghiệp Việt Nam thường là **01/01**.
   - **Ngày kết thúc năm:** thường là **31/12** cùng năm.
3. Lưu. Gán năm tài chính làm mặc định cho công ty nếu được hỏi.

## Định khoản tự động

Khai báo này **không sinh bút toán**. Nó cung cấp **khung thời gian** để:
- Cho phép/chặn ghi sổ theo ngày chứng từ (ngày phải nằm trong một năm tài chính đã khai).
- Trợ lý **kết chuyển cuối kỳ (TK 911)** xác định kỳ cuối năm — khi đó bổ sung TK 821 (chi phí thuế TNDN) vào danh sách kết chuyển.
- Báo cáo tài chính (B01-DN, B02-DN...) và báo cáo so sánh tính số đầu năm / cuối năm.

## Tình huống đặc biệt & cảnh báo

- **Năm tài chính Việt Nam mặc định 01/01 – 31/12.** Nếu công ty dùng năm tài chính lệch (ví dụ 01/04 – 31/03), phải khai đúng để báo cáo và kết chuyển không sai kỳ.
- **Phải tạo năm tài chính TRƯỚC khi ghi chứng từ của năm đó** — nếu ngày chứng từ không thuộc năm tài chính nào, hệ thống sẽ chặn lưu.
- **Trợ lý kết chuyển dựa vào ngày kết thúc năm để nhận diện kỳ cuối năm.** Khai sai ngày kết thúc có thể khiến TK 821 bị kết chuyển nhầm kỳ.
- **Không trùng/khớp khoảng ngày giữa các năm tài chính.** Mỗi ngày chỉ thuộc một năm tài chính.

## Báo cáo liên quan

- [Kỳ kế toán](ky-ke-toan.md) — chốt sổ theo từng kỳ con (tháng/quý) trong năm.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — TK 911/4212/4211/821 dùng khi kết chuyển cuối năm.
- Phân hệ **Báo cáo tài chính** — B01/B02/B03-DN theo năm.

## FAQ

**Q: Có cần tạo năm tài chính của năm trước không?**
**A:** Cần, nếu bạn nhập số dư đầu kỳ hoặc dữ liệu lịch sử của năm trước. Báo cáo so sánh "đầu năm — cuối năm" cũng cần năm trước để tính số đầu năm.

**Q: Tôi quên tạo năm 2027, ghi chứng từ ngày 02/01/2027 bị chặn?**
**A:** Đúng. Tạo năm tài chính 2027 (01/01/2027 – 31/12/2027) rồi ghi lại.

**Q: Năm tài chính có tự sinh các kỳ kế toán tháng không?**
**A:** Không. Kỳ kế toán (để chốt/khóa sổ từng kỳ) khai riêng — xem [Kỳ kế toán](ky-ke-toan.md).
