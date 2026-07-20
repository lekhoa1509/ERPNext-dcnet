---
title: Định nghĩa kỳ kế toán
order: 5
summary: Khai báo các kỳ kế toán (tháng/quý/năm) và chọn loại chứng từ bị cấm hạch toán lùi trong kỳ đã đóng.
---

## Mục đích

**Định nghĩa kỳ kế toán** khai báo các khoảng thời gian kế toán (tháng, quý, năm) của công ty và quản lý việc **cấm hạch toán lùi ngày**. Với mỗi kỳ, bạn chọn những loại chứng từ bị "đóng" — sau khi đóng, không ai được tạo/sửa/hủy chứng từ loại đó có ngày rơi trong kỳ. Đây là cơ chế thực thi việc khoá sổ ở cấp dữ liệu.

> Mục này dùng chung giữa phân hệ **Tổng hợp** (khoá sổ cuối kỳ) và phần **Thiết lập** (cấu hình ban đầu các kỳ kế toán của công ty).

## Khi nào dùng

- **Thiết lập ban đầu:** khi mới triển khai, khai báo các kỳ kế toán của năm tài chính.
- **Cuối mỗi kỳ:** sau khi đối soát xong, đóng các loại chứng từ để cấm hạch toán lùi.
- **Khi cần mở lại kỳ:** bỏ đóng (mở khoá) một loại chứng từ để điều chỉnh — xem [Mở khoá kỳ](mo-khoa-ky.md).

## Cách thực hiện

1. Mở danh sách **Định nghĩa kỳ kế toán** → **+ Thêm**.
2. Nhập **Tên kỳ** (VD "Tháng 04/2026"), **Công ty**, **Ngày bắt đầu**, **Ngày kết thúc**.
3. Trong bảng **Chứng từ đóng**, thêm các loại chứng từ cần cấm hạch toán lùi (Phiếu kế toán, Hóa đơn bán hàng, Hóa đơn mua hàng, Phiếu thanh toán, Phiếu nhập xuất kho...) và tick cột **Đã đóng** cho từng loại.
4. *(Tùy chọn)* Chọn **Vai trò miễn trừ** — người mang vai trò này vẫn hạch toán được vào kỳ đã đóng (chỉ cấp cho Kế toán trưởng).
5. Lưu. Từ đó, hệ thống tự kiểm tra mọi chứng từ khi tạo/sửa/hủy: nếu ngày hạch toán rơi trong kỳ và loại chứng từ đã đóng → chặn lại.

## Định khoản tự động

Không tự định khoản — đây là cấu hình kỳ kế toán và rào chặn ngày. Không sinh bút toán.

## Tình huống đặc biệt & cảnh báo

- **Các kỳ không được chồng lấp:** hệ thống chặn việc khai báo hai kỳ có khoảng ngày giao nhau cho cùng công ty.
- **Đóng theo từng loại chứng từ:** bạn có thể đóng Hóa đơn nhưng vẫn mở Phiếu kế toán trong cùng kỳ — kiểm soát chi tiết.
- **Vai trò miễn trừ dùng thận trọng:** vai trò được miễn trừ phá vỡ rào chặn — chỉ cấp cho KTT, không cấp đại trà.
- **Vô hiệu hóa kỳ (Disabled):** đặt kỳ ở trạng thái Vô hiệu hóa sẽ tạm gỡ toàn bộ rào chặn của kỳ đó — dùng khi cần mở khoá nhanh.
- **Một số chứng từ dùng ngày khác posting_date:** Tài sản dùng "Ngày sẵn sàng sử dụng", Phiếu sửa chữa TSCĐ dùng "Ngày hoàn thành", Phiếu khoá sổ dùng "Ngày kết thúc kỳ" — hệ thống tự dùng đúng ngày tương ứng để kiểm tra.

## Báo cáo liên quan

- [Khoá sổ kỳ kế toán](khoa-so-ky.md): quy trình khoá sổ cuối kỳ/cuối năm.
- [Mở khoá kỳ kế toán đã đóng](mo-khoa-ky.md): mở lại kỳ để điều chỉnh.
- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): kết chuyển trước khi đóng kỳ.

## FAQ

**Q: Kỳ kế toán khác Năm tài chính thế nào?**
**A:** Năm tài chính xác định phạm vi năm sổ sách. Kỳ kế toán (mục này) chia nhỏ thành tháng/quý để quản lý việc đóng/mở từng kỳ và cấm hạch toán lùi.

**Q: Tôi quên đóng một loại chứng từ, sau đó có người hạch toán lùi — phải làm gì?**
**A:** Bổ sung loại chứng từ đó vào bảng Chứng từ đóng để chặn từ nay; với chứng từ đã lỡ hạch toán, kiểm tra và điều chỉnh thủ công.

**Q: Vì sao tạo chứng từ báo "Kỳ ... đã bị khóa"?**
**A:** Ngày hạch toán của chứng từ rơi vào một kỳ đã đóng loại chứng từ đó. Đổi ngày sang kỳ mở, hoặc nhờ KTT mở khoá kỳ nếu thực sự cần hạch toán vào kỳ đã đóng.
