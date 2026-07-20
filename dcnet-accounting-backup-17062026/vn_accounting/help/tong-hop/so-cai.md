---
title: Sổ cái (S03b-DN)
order: 7
summary: Sổ kế toán tổng hợp phát sinh của một tài khoản kèm số dư đầu/cuối kỳ, mẫu S03b-DN theo TT99/2025.
---

## Mục đích

**Sổ cái (S03b-DN)** ghi lại toàn bộ phát sinh của MỘT tài khoản kế toán trong kỳ, kèm số dư đầu kỳ và số dư cuối kỳ. Theo Phụ lục IV Thông tư 99/2025/TT-BTC, mỗi tài khoản có một trang sổ cái riêng (mẫu S03b-DN). Báo cáo có 3 dòng tóm tắt ghim ở đầu bảng (số dư đầu kỳ, cộng phát sinh, số dư cuối kỳ) và 4 thẻ tổng hợp nổi phía trên để quét nhanh. Chỉ TRA CỨU, không tạo chứng từ.

## Khi nào dùng

- **In sổ cái từng tài khoản** để lưu và nộp cơ quan thuế.
- **Đối chiếu số dư** một tài khoản cụ thể cuối kỳ.
- **Truy vết phát sinh** của một tài khoản theo thời gian, kèm cột số dư lũy kế.

## Cách thực hiện

1. Mở **Tổng hợp → Sổ cái (S03b-DN)**.
2. Nhập bộ lọc:
   - **Công ty** (bắt buộc).
   - **Tài khoản** (bắt buộc — chọn 1 tài khoản chi tiết, không phải tài khoản nhóm; danh sách đã lọc theo công ty và chỉ hiện tài khoản chi tiết).
   - **Từ ngày / Đến ngày** (mặc định đầu năm → cuối năm tài chính).
3. Bấm **Chạy báo cáo**.
4. Xem 3 dòng tóm tắt đầu bảng + 4 thẻ tổng (Số dư đầu kỳ, PS Nợ, PS Có, Số dư cuối kỳ).
5. Xuất Excel theo định dạng S03b-DN qua **Thực đơn → Tải về**.

### Các cột chính

| Cột | Ý nghĩa |
|---|---|
| Ngày ghi sổ | Ngày hạch toán |
| Số CT | Số hiệu chứng từ (bấm để mở chứng từ gốc) |
| Ngày CT | Ngày chứng từ gốc |
| Diễn giải | Nội dung nghiệp vụ |
| TK đối ứng | Tài khoản đối ứng của bút toán |
| PS Nợ / PS Có | Số phát sinh bên Nợ / bên Có của tài khoản này |

Số dư đầu kỳ và số dư cuối kỳ (Nợ hoặc Có) hiển thị ở các dòng tóm tắt và thẻ tổng.

## Định khoản tự động

Không tự định khoản — đây là sổ tra cứu chi tiết một tài khoản. Không tạo chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Phải chọn 1 tài khoản chi tiết:** không xem được tài khoản nhóm (tài khoản tổng hợp). Muốn xem tổng nhóm, dùng [Bảng cân đối số phát sinh](trial-balance.md).
- **Số dư đầu kỳ:** tính từ toàn bộ phát sinh TRƯỚC ngày bắt đầu kỳ. Nếu chưa nhập số dư đầu kỳ (Opening Balance), số dư đầu = 0.
- **Chỉ gồm bút toán đã ghi sổ:** phiếu Nháp không xuất hiện.
- **Xuất nhiều tài khoản:** mỗi lần chỉ một tài khoản. Cần nhiều tài khoản thì chạy lần lượt rồi gộp file Excel.

## Báo cáo liên quan

- [Sổ chi tiết tài khoản](so-chi-tiet-tai-khoan.md): như sổ cái nhưng thêm cột Đối tượng (khách/NCC) + Bộ phận + Tham chiếu — lọc được theo đối tượng.
- [Sổ nhật ký chung (S03a-DN)](so-nhat-ky-chung.md): mọi nghiệp vụ theo thời gian.
- [Bảng cân đối số phát sinh](trial-balance.md): tổng hợp số dư toàn bộ tài khoản.

## FAQ

**Q: Số dư đầu kỳ không khớp?**
**A:** Kiểm tra đã nhập Số dư đầu kỳ (Opening Balance) chưa. Chưa có thì số dư đầu kỳ = 0.

**Q: Muốn xuất sổ cái toàn bộ tài khoản?**
**A:** Hiện mỗi lần xuất một tài khoản. Chạy lần lượt từng tài khoản và tổng hợp vào một file Excel.

**Q: Sổ cái khác Sổ chi tiết tài khoản ở điểm nào?**
**A:** Sổ cái là mẫu chuẩn S03b-DN (nộp thuế), tập trung số dư + phát sinh. Sổ chi tiết tài khoản bổ sung cột Đối tượng, Bộ phận, Tham chiếu và cho phép lọc theo đối tượng — tiện đối chiếu công nợ.
