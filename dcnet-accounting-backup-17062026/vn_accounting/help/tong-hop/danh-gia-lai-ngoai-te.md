---
title: Đánh giá lại ngoại tệ
order: 1
summary: Lập phiếu đánh giá lại số dư gốc ngoại tệ cuối kỳ, ghi nhận lãi/lỗ chênh lệch tỷ giá chưa thực hiện.
---

## Mục đích

Chức năng **Đánh giá lại ngoại tệ** rà soát toàn bộ tài khoản có số dư bằng ngoại tệ tại ngày cuối kỳ, tính lại giá trị quy đổi theo tỷ giá mới và ghi nhận khoản **chênh lệch tỷ giá chưa thực hiện** (lãi → TK 515, lỗ → TK 635, qua trung gian TK 413). Đây là bước bắt buộc trước khi lập Báo cáo tài chính cho doanh nghiệp có giao dịch / số dư ngoại tệ, theo nguyên tắc VAS.

## Khi nào dùng

- **Cuối tháng/quý/năm** trước khi lập Báo cáo tài chính, khi công ty còn số dư các tài khoản gốc ngoại tệ: tiền mặt ngoại tệ (1112), tiền gửi ngoại tệ (1122), phải thu (131) / phải trả (331) bằng ngoại tệ, vay ngoại tệ (341)...
- Khi tỷ giá cuối kỳ chênh lệch đáng kể so với tỷ giá ghi sổ ban đầu của các khoản mục tiền tệ.
- **Phải thực hiện TRƯỚC bước kết chuyển cuối kỳ** — vì chênh lệch tỷ giá vào TK 515/635 sẽ tham gia xác định kết quả kinh doanh.

## Cách thực hiện

1. Mở danh sách **Đánh giá lại ngoại tệ** → bấm **+ Thêm**.
2. Chọn **Công ty** và **Ngày hạch toán** (= ngày cuối kỳ cần đánh giá lại).
3. Bấm **Lấy tài khoản** (Get Entries) → hệ thống quét mọi tài khoản có số dư ngoại tệ khác 0, tính tỷ giá mới tại ngày hạch toán và điền vào bảng:
   - **Số dư ngoại tệ** (giữ nguyên — không đổi).
   - **Tỷ giá hiện tại** và **Tỷ giá mới**.
   - **Lãi/Lỗ** = (Số dư ngoại tệ × Tỷ giá mới) − Số dư ghi sổ hiện tại.
4. Kiểm tra cột **Lãi/Lỗ** từng dòng; những dòng không phát sinh chênh lệch sẽ tự bị loại.
5. **Ghi sổ** (Submit). Sau khi ghi sổ, mở nút tạo phiếu kế toán điều chỉnh tỷ giá để hệ thống sinh bút toán quy đổi.

## Định khoản tự động

Hệ thống sinh phiếu kế toán (loại Exchange Gain Or Loss) với định khoản:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Lãi tỷ giá tài sản (tiền/phải thu ngoại tệ tăng giá) | Tài khoản gốc (1112/1122/131) | 413 | Tăng giá trị quy đổi của khoản mục tài sản |
| Lỗ tỷ giá tài sản | 413 | Tài khoản gốc | Giảm giá trị quy đổi |
| Lãi tỷ giá nợ phải trả (331/341 ngoại tệ giảm giá) | Tài khoản gốc | 413 | |
| Lỗ tỷ giá nợ phải trả | 413 | Tài khoản gốc | |
| Kết chuyển lãi tỷ giá chưa thực hiện cuối kỳ | 413 | 515 | Doanh thu hoạt động tài chính |
| Kết chuyển lỗ tỷ giá chưa thực hiện cuối kỳ | 635 | 413 | Chi phí tài chính |

> Tài khoản chênh lệch tỷ giá lấy từ cấu hình **TK chênh lệch tỷ giá chưa thực hiện** của công ty (mặc định TK 413). Nếu công ty chưa khai báo tài khoản này, hệ thống dùng tài khoản mặc định — cần kiểm tra lại để đúng TK 413 theo VAS.

## Tình huống đặc biệt & cảnh báo

- **Chỉ đánh giá lại khoản mục tiền tệ** (tiền, phải thu, phải trả, vay). KHÔNG đánh giá lại khoản mục phi tiền tệ (hàng tồn kho, TSCĐ, doanh thu/chi phí đã ghi).
- **Phải làm trước kết chuyển 911:** nếu kết chuyển cuối kỳ chạy trước, kết quả kinh doanh sẽ thiếu phần lãi/lỗ tỷ giá.
- **Tỷ giá nguồn:** hệ thống lấy tỷ giá tại ngày hạch toán từ bảng tỷ giá. Cần cập nhật tỷ giá cuối kỳ (tỷ giá mua/bán của ngân hàng giao dịch chính) trước khi lấy tài khoản.
- **Bút toán chỉ tạm thời:** chênh lệch tỷ giá chưa thực hiện sang đầu kỳ sau thường được hoàn nhập; theo dõi để không trùng lặp.
- **Cấu hình tài khoản 413 trống:** nếu công ty chưa đặt tài khoản chênh lệch tỷ giá chưa thực hiện, mở phần Cài đặt công ty để khai báo TK 413 trước khi ghi sổ.

## Báo cáo liên quan

- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): chạy SAU khi đánh giá lại ngoại tệ.
- [Sổ chi tiết tài khoản](so-chi-tiet-tai-khoan.md): kiểm tra số dư ngoại tệ TK 1122/131/331 trước/sau đánh giá lại.
- [Bảng cân đối số phát sinh](trial-balance.md): đối chiếu số dư cuối kỳ TK 413/515/635.

## FAQ

**Q: Đánh giá lại ngoại tệ và kết chuyển cuối kỳ, làm cái nào trước?**
**A:** Đánh giá lại ngoại tệ TRƯỚC. Phần lãi/lỗ tỷ giá kết chuyển sang TK 515/635 phải có mặt trước khi kết chuyển doanh thu/chi phí về TK 911.

**Q: Tài khoản nào cần đánh giá lại?**
**A:** Mọi tài khoản tiền tệ còn số dư gốc ngoại tệ: 1112 (tiền mặt ngoại tệ), 1122 (tiền gửi ngoại tệ), 131/331 phần phát sinh ngoại tệ, 341 (vay ngoại tệ). Hệ thống tự quét và liệt kê.

**Q: Vì sao có dòng chênh lệch = 0 không hiển thị?**
**A:** Hệ thống tự loại các tài khoản không có chênh lệch tỷ giá (lãi/lỗ = 0) để bảng gọn — chỉ giữ những tài khoản thực sự cần điều chỉnh.

**Q: Lãi tỷ giá ghi vào TK nào?**
**A:** Lãi chưa thực hiện cuối kỳ kết chuyển qua TK 413 rồi sang TK 515 (doanh thu tài chính); lỗ kết chuyển sang TK 635 (chi phí tài chính).
