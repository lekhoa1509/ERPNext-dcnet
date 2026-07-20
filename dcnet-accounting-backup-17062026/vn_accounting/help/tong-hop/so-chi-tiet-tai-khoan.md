---
title: Sổ chi tiết tài khoản
order: 8
summary: Sổ chi tiết phát sinh một tài khoản kèm đối tượng, bộ phận và tham chiếu chứng từ gốc; lọc được theo đối tượng.
---

## Mục đích

**Sổ chi tiết tài khoản** ghi chi tiết phát sinh của một tài khoản trong kỳ, kèm cột **Đối tượng** (khách hàng / nhà cung cấp / nhân viên), **Bộ phận** (trung tâm chi phí) và **Tham chiếu** (chứng từ gốc liên quan). So với Sổ cái, sổ này phục vụ đối chiếu công nợ và theo dõi chi phí theo bộ phận, dựa trên tinh thần mẫu S38-DN của TT99/2025. Chỉ TRA CỨU, không tạo chứng từ.

## Khi nào dùng

- **Đối chiếu công nợ** một khách hàng/nhà cung cấp trên TK 131/331 — lọc theo đối tượng.
- **Theo dõi chi phí theo bộ phận** — lọc tài khoản chi phí theo trung tâm chi phí.
- **Truy vết tham chiếu** — biết bút toán này gắn với hóa đơn/phiếu gốc nào.

## Cách thực hiện

1. Mở **Tổng hợp → Sổ chi tiết tài khoản**.
2. Nhập bộ lọc:
   - **Công ty** (bắt buộc).
   - **Tài khoản** (bắt buộc — chọn 1 tài khoản chi tiết).
   - **Từ ngày / Đến ngày** (mặc định 1 tháng gần nhất).
   - **Loại đối tượng** (Khách hàng / Nhà cung cấp / Nhân viên) và **Đối tượng** (tùy chọn — lọc 1 đối tượng cụ thể).
3. Bấm **Chạy báo cáo** → bảng hiển thị 3 dòng tóm tắt đầu (số dư đầu, cộng phát sinh, số dư cuối) + 4 thẻ tổng + danh sách phát sinh.

### Các cột chính

| Cột | Ý nghĩa |
|---|---|
| Ngày ghi sổ / Số CT / Ngày CT | Thông tin chứng từ |
| Diễn giải | Nội dung nghiệp vụ |
| Đối tượng | Khách hàng / NCC / nhân viên liên quan |
| Bộ phận | Trung tâm chi phí chịu chi phí |
| Tham chiếu | Chứng từ gốc của bút toán (phiếu nguồn) |
| TK đối ứng | Tài khoản đối ứng |
| PS Nợ / PS Có | Số phát sinh Nợ / Có |

## Định khoản tự động

Không tự định khoản — sổ tra cứu chi tiết. Không tạo chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Chọn 1 tài khoản chi tiết:** không xem tài khoản nhóm.
- **Lọc theo đối tượng ảnh hưởng cả số dư đầu kỳ:** khi chọn 1 đối tượng, số dư đầu kỳ cũng chỉ tính riêng cho đối tượng đó — dùng đúng để đối chiếu công nợ từng khách/NCC.
- **Bộ phận (cost center):** chỉ có giá trị nếu bút toán được gắn trung tâm chi phí; bút toán không gắn sẽ để trống.
- **Chỉ gồm bút toán đã ghi sổ.**

## Báo cáo liên quan

- [Sổ cái (S03b-DN)](so-cai.md): mẫu chuẩn S03b-DN nộp thuế, không có cột Đối tượng/Bộ phận.
- [Sổ nhật ký chung (S03a-DN)](so-nhat-ky-chung.md): mọi nghiệp vụ theo thời gian.
- [Bảng cân đối số phát sinh](trial-balance.md): tổng hợp số dư toàn bộ tài khoản.

## FAQ

**Q: Khi nào dùng Sổ chi tiết tài khoản thay vì Sổ cái?**
**A:** Khi cần đối chiếu công nợ theo từng khách/NCC (TK 131/331) hoặc theo dõi chi phí theo bộ phận — sổ này có cột Đối tượng, Bộ phận, Tham chiếu và lọc được theo đối tượng. Sổ cái dùng khi cần mẫu chuẩn S03b-DN để nộp thuế.

**Q: Lọc 1 khách hàng trên TK 131, số dư đầu kỳ có đúng của riêng khách đó không?**
**A:** Có. Khi lọc theo đối tượng, cả số dư đầu kỳ lẫn phát sinh đều tính riêng cho đối tượng đó.

**Q: Cột Tham chiếu để làm gì?**
**A:** Cho biết bút toán gắn với chứng từ gốc nào (ví dụ hóa đơn được thanh toán), giúp truy vết nhanh nguồn của khoản phát sinh.
