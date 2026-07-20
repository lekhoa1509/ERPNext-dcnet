---
title: Bảng cân đối số phát sinh
order: 13
summary: Số dư đầu kỳ, phát sinh và số dư cuối kỳ của mọi tài khoản — điểm khởi đầu để soát số trước khi lập BCTC.
---

## Mục đích

**Bảng cân đối số phát sinh (BCDPS)** liệt kê toàn bộ tài khoản kế toán với 6 cột: số dư đầu kỳ (Nợ/Có), phát sinh trong kỳ (Nợ/Có), số dư cuối kỳ (Nợ/Có). Đây là báo cáo soát số quan trọng nhất trước khi lập BCTC: tổng phát sinh Nợ phải bằng tổng phát sinh Có, tổng dư Nợ phải bằng tổng dư Có.

Báo cáo dùng lại logic cân đối phát sinh của hệ thống nền tảng, **đổi tên cột sang thuật ngữ VAS/Misa** cho dễ đọc.

## Khi nào dùng

- Trước khi lập B01/B02/B03: kiểm tra sổ đã khóa đúng (phát sinh Nợ = Có).
- Soát số dư bất thường: tài khoản có dư ngược chiều, dư bất hợp lý.
- Đối chiếu với B01: số dư cuối kỳ từng tài khoản phải khớp chỉ tiêu B01 tương ứng.

## Cách thực hiện

1. Vào **Báo cáo tài chính → Bảng cân đối số phát sinh**.
2. Chọn **Công ty** (bắt buộc) và **Năm tài chính** — hệ thống tự điền Từ ngày — Đến ngày theo niên độ.
3. (Tùy chọn) Lọc thêm **Trung tâm chi phí**, **Dự án**.
4. Báo cáo hiển thị các cột (đã đổi tên VAS):

| Cột | Ý nghĩa |
|---|---|
| Dư đầu kỳ Nợ | Số dư bên Nợ tại đầu kỳ |
| Dư đầu kỳ Có | Số dư bên Có tại đầu kỳ |
| Phát sinh Nợ | Tổng phát sinh bên Nợ trong kỳ |
| Phát sinh Có | Tổng phát sinh bên Có trong kỳ |
| Dư cuối kỳ Nợ | Số dư bên Nợ tại cuối kỳ |
| Dư cuối kỳ Có | Số dư bên Có tại cuối kỳ |

## Định khoản tự động

Báo cáo này **không tự định khoản — chỉ tra cứu**. Số liệu tính trực tiếp từ phát sinh và số dư các tài khoản trên Sổ Cái theo kỳ đã chọn.

## Tình huống đặc biệt & cảnh báo

- **Một tài khoản có CẢ Phát sinh Nợ và Phát sinh Có là bình thường:** cột "Phát sinh" thể hiện luồng phát sinh trong kỳ (tiền vào + tiền ra, hóa đơn + thanh toán), không phải số dư cuối cùng. Đây là lý do hệ thống đổi tên cột từ "Ghi nợ/Ghi có" (dễ hiểu nhầm là chiều số dư) sang "Phát sinh Nợ/Có".
- **Kiểm tra cân đối:** tổng cột Phát sinh Nợ = tổng Phát sinh Có; tổng Dư cuối kỳ Nợ = tổng Dư cuối kỳ Có. Lệch = có bút toán một vế hoặc dữ liệu bất thường.
- **Đối chiếu với B01:** dư cuối kỳ từng tài khoản cộng theo nhóm phải khớp chỉ tiêu B01. Đây là cách dò khi B01 mất cân.
- **Đây là báo cáo của hệ thống nền tảng (ERP) đã Việt hóa cột:** cấu trúc và bộ lọc giống báo cáo cân đối phát sinh gốc, chỉ khác nhãn cột.

## Báo cáo liên quan

- [B01 — Tình hình tài chính](b01-cau-truc.md) — đối chiếu số dư cuối kỳ.
- [Cấu hình BCTC Mapping](bctc-mapping.md) — khi cần soát tài khoản nào vào chỉ tiêu nào.
- Sổ Cái, Sổ Nhật ký chung (phân hệ Tổng hợp) — xem chi tiết phát sinh từng tài khoản.

## FAQ

**Q: Vì sao nhiều tài khoản có cả Phát sinh Nợ và Phát sinh Có?**
**A:** Cột Phát sinh thể hiện tất cả nghiệp vụ trong kỳ của tài khoản đó (cả tăng lẫn giảm), không phải số dư. Ví dụ TK tiền mặt có thu (Nợ) và chi (Có) — cả hai cột đều có số là đúng.

**Q: Tổng phát sinh Nợ ≠ tổng phát sinh Có?**
**A:** Dấu hiệu có bút toán mất cân (một vế) hoặc lỗi dữ liệu. Soát lại các bút toán phát sinh trong kỳ, ưu tiên bút toán nhập tay.

**Q: Số dư cuối kỳ ở đây khác B01?**
**A:** Kiểm tra mapping (tài khoản đã vào đúng chỉ tiêu chưa) và bộ lọc trung tâm chi phí/dự án — bảng này có thể đang lọc một phần.
