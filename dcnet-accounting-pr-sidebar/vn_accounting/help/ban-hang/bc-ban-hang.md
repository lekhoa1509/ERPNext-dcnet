---
title: BC bán hàng
order: 9
summary: Phân tích doanh số theo khách hàng, mặt hàng, nhóm hàng và theo kỳ (tuần/tháng/quý/năm).
---

## Mục đích

**Báo cáo bán hàng** (phân tích bán hàng) cho phép xem doanh số theo nhiều chiều: theo **khách hàng**, **mặt hàng**, **nhóm hàng/lãnh thổ**, và theo **kỳ thời gian** (tuần/tháng/quý/năm). Có thể chọn xem theo **giá trị tiền** hoặc **số lượng**, dựa trên đơn bán hàng / hóa đơn bán hàng / phiếu xuất kho. Đây là công cụ phân tích doanh thu, không phải báo cáo công nợ.

## Khi nào dùng

- Đánh giá doanh số theo tháng/quý để báo cáo lãnh đạo.
- Tìm mặt hàng/khách hàng đóng góp doanh thu lớn nhất.
- So sánh xu hướng bán hàng giữa các kỳ.
- Phân tích cơ cấu doanh thu theo nhóm hàng / khu vực.

## Cách thực hiện

1. Mở mục **BC bán hàng**.
2. Đặt bộ lọc:
   - **Phân tích theo** (Tree Type): Khách hàng / Mặt hàng / Nhóm khách / Nhóm hàng / Lãnh thổ...
   - **Dựa trên** (Based On): Đơn bán hàng / Hóa đơn bán hàng / Phiếu xuất kho.
   - **Giá trị hay Số lượng**: chọn xem theo tiền hoặc số lượng.
   - **Từ ngày / Đến ngày**, **Công ty**.
   - **Kỳ** (Range): Tuần / Tháng / Quý / Năm — cột thời gian sẽ chia theo kỳ này.
3. Báo cáo hiển thị dạng cây (có thể bung/thu theo nhóm) + biểu đồ xu hướng theo kỳ.
4. Xuất Excel nếu cần.

## Định khoản tự động

**Không tự định khoản — chỉ tra cứu/phân tích.** Báo cáo tổng hợp số liệu từ chứng từ bán hàng; không tạo bút toán.

## Tình huống đặc biệt & cảnh báo

- **Chọn đúng "Dựa trên":** doanh số theo **hóa đơn bán hàng** = doanh thu đã ghi nhận; theo **đơn bán hàng** = giá trị đã chốt (có thể chưa giao/chưa lập hóa đơn). Chọn nhầm sẽ ra con số khác ý nghĩa.
- **Giá trị vs số lượng:** với mặt hàng nhiều đơn vị tính, xem theo "Số lượng" cần nhất quán đơn vị; xem theo "Giá trị" an toàn hơn để so sánh.
- **Theo kỳ:** đổi "Kỳ" (Tuần/Tháng/Quý/Năm) thay đổi cách chia cột thời gian — chọn phù hợp khoảng "Từ ngày–Đến ngày".
- **Báo cáo chuẩn của hệ thống:** nếu trống, kiểm tra đã có chứng từ bán hàng (theo loại đã chọn ở "Dựa trên") ghi sổ trong khoảng thời gian lọc chưa.

## Báo cáo liên quan

- [Hóa đơn bán hàng](hoa-don-ban-hang.md): nguồn doanh thu đã ghi nhận.
- [Đơn bán hàng](don-ban-hang.md): nguồn giá trị đã chốt.
- [Công nợ phải thu](cong-no-phai-thu.md): theo dõi tiền chưa thu của doanh số đã lập hóa đơn.

## FAQ

**Q: Doanh số ở đây là doanh thu đã ghi nhận?**
**A:** Tùy chọn "Dựa trên". Chọn "Hóa đơn bán hàng" = doanh thu đã ghi nhận (đã ghi sổ). Chọn "Đơn bán hàng" = giá trị đã chốt, có thể chưa thành doanh thu.

**Q: Báo cáo này có trừ chiết khấu/trả lại hàng không?**
**A:** Số liệu lấy từ giá trị trên chứng từ đã chọn; chiết khấu thể hiện theo cách ghi trên chứng từ. Để có doanh thu thuần chính xác, đối chiếu thêm với Sổ Cái TK 511/521.

**Q: Có biểu đồ xu hướng không?**
**A:** Có — báo cáo hiển thị biểu đồ theo kỳ (tuần/tháng/quý/năm) bên cạnh bảng số liệu.
