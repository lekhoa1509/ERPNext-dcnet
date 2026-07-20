---
title: Phiếu lương
order: 4
summary: Phiếu lương chi tiết của từng nhân viên — thu nhập, khấu trừ, lương thực lĩnh trong một kỳ.
---

## Mục đích

**Phiếu lương** là bảng tính lương chi tiết cho một nhân viên trong một kỳ: liệt kê các khoản **thu nhập** (lương cơ bản, phụ cấp, thưởng), các khoản **khấu trừ** (bảo hiểm phần người lao động, thuế TNCN, tạm ứng) và **lương thực lĩnh**. Phiếu lương thường được sinh hàng loạt từ Bảng lương, nhưng cũng có thể tạo lẻ cho một người.

## Khi nào dùng

- Kiểm tra chi tiết lương của một nhân viên: từng khoản thu nhập và khấu trừ.
- Đối chiếu số ngày công, mức lương, thuế TNCN khấu trừ trước khi duyệt Bảng lương.
- In phiếu lương phát cho người lao động.
- Tạo lẻ phiếu lương cho trường hợp cá biệt (nhân viên vào/nghỉ giữa kỳ).

## Cách thực hiện

1. Bấm **Phiếu lương** → danh sách phiếu lương mở ra (lọc theo nhân viên/kỳ).
2. Mở một phiếu để xem **Thu nhập**, **Khấu trừ**, **Tổng thu nhập**, **Tổng khấu trừ**, **Lương thực lĩnh**, và **số ngày được trả lương**.
3. Tạo lẻ: bấm **+ Thêm**, chọn **Nhân viên** và **kỳ** → hệ thống lấy Cơ cấu lương đã gán để tính.
4. **Gửi/Duyệt** phiếu lương để chốt (thường duyệt hàng loạt từ Bảng lương).

## Định khoản tự động

Phiếu lương **không tự sinh bút toán riêng lẻ**. Bút toán hạch toán chi phí lương và các khoản trích được lập **tổng hợp** từ Bảng lương khi ghi sổ. Phiếu lương chỉ là chi tiết tính toán cho từng người (xem bảng định khoản tại [Bảng lương](bang-luong.md)).

## Tình huống đặc biệt & cảnh báo

- **Số ngày được trả lương** lấy từ Bảng chấm công; nghỉ không lương làm giảm lương ở các thành phần "phụ thuộc số ngày công".
- **Thuế TNCN trên phiếu** tính theo biểu lũy tiến lũy kế trong năm; nếu thu nhập biến động, số thuế từng kỳ có thể chênh — tính lại đúng khi quyết toán năm.
- **Thành phần lương không phụ thuộc số ngày công** (ví dụ một số phụ cấp cố định) được trả đủ dù nghỉ — kiểm tra thiết lập "phụ thuộc số ngày công" trên Thành phần lương.
- **Phiếu lương lẻ vs hàng loạt:** nên dùng Bảng lương để đảm bảo bút toán tổng hợp đầy đủ; phiếu lẻ chỉ dùng cho trường hợp cá biệt.

## Báo cáo liên quan

- [Bảng lương](bang-luong.md): sinh phiếu lương hàng loạt và lập bút toán.
- [Lương bổ sung](luong-bo-sung.md): các khoản một lần được cộng/trừ vào phiếu lương.
- [Thành phần lương](thanh-phan-luong.md): định nghĩa từng khoản thu nhập/khấu trừ.

## FAQ

**Q: Phiếu lương có tạo bút toán không?**
**A:** Không tạo riêng. Bút toán chi phí lương được hạch toán tổng hợp từ Bảng lương.

**Q: Lương thực lĩnh tính thế nào?**
**A:** Lương thực lĩnh = Tổng thu nhập − Tổng khấu trừ (bảo hiểm phần người lao động + thuế TNCN + tạm ứng/khấu trừ khác).

**Q: Tạo phiếu lương lẻ cho nhân viên vào giữa kỳ được không?**
**A:** Được. Tạo phiếu lương cho đúng khoảng ngày làm việc; số ngày được trả lương sẽ tính theo chấm công thực tế trong khoảng đó.
