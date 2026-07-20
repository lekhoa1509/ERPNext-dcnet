---
title: BC mua hàng
order: 7
summary: Báo cáo phân tích mua hàng theo nhà cung cấp, mặt hàng, nhóm hàng và theo kỳ — dạng bảng chéo và biểu đồ.
---

## Mục đích

**BC mua hàng** (báo cáo phân tích mua hàng) tổng hợp giá trị/số lượng mua theo nhiều chiều: nhà cung cấp, mặt hàng, nhóm hàng, theo tháng/quý/năm. Hiển thị dạng bảng chéo (pivot) và biểu đồ xu hướng, giúp đánh giá cơ cấu chi tiêu mua hàng và so sánh giữa các kỳ. Đây là báo cáo phân tích chuẩn của hệ thống ERP, chỉ tra cứu.

## Khi nào dùng

- Cuối tháng/quý/năm: phân tích cơ cấu mua theo NCC và mặt hàng.
- Khi cần đánh giá NCC nào chiếm tỷ trọng mua lớn, mặt hàng nào mua nhiều.
- Khi so sánh xu hướng mua giữa các kỳ để lập kế hoạch mua.

## Cách thực hiện

1. Bấm **BC mua hàng** trên menu Mua hàng → báo cáo mở.
2. Chọn **Công ty**, **Kỳ** (Tháng/Quý/Năm), **Khoảng thời gian**, chiều phân tích **Theo** (Nhà cung cấp / Mặt hàng / Nhóm hàng...).
3. Chọn **Dựa trên** (giá trị mua hay số lượng) tùy nhu cầu.
4. Bấm **Refresh** → bảng chéo hiển thị giá trị mua theo từng kỳ và biểu đồ xu hướng.
5. Mở rộng/thu gọn nhóm để xem chi tiết theo từng NCC/mặt hàng.

## Định khoản tự động

Báo cáo **không sinh bút toán** — chỉ phân tích số liệu mua từ hóa đơn mua hàng / phiếu nhập kho.

## Tình huống đặc biệt & cảnh báo

- **Báo cáo phân tích, không phải sổ chi tiết:** cần truy từng chứng từ thì sang [BC theo mặt hàng](bc-theo-mat-hang.md) hoặc danh sách hóa đơn mua hàng.
- **Số liệu theo ngày ghi sổ chứng từ:** kỳ phân tích dựa trên ngày ghi sổ hóa đơn/nhập kho, không phải ngày hóa đơn NCC.
- **Giá trị gồm hay chưa gồm thuế:** kiểm tra cấu hình "Dựa trên" — thường lấy giá trị trước thuế (net). Đối chiếu với mục đích phân tích.

## Báo cáo liên quan

- [BC theo mặt hàng](bc-theo-mat-hang.md) — sổ chi tiết mua theo từng mặt hàng.
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) / [Đơn mua hàng](don-mua-hang.md) — chứng từ nguồn.
- [Công nợ phải trả](cong-no-phai-tra.md) — theo dõi nghĩa vụ thanh toán.

## FAQ

**Q: Báo cáo này lấy số liệu theo giá có thuế hay chưa thuế?**
**A:** Thường lấy giá trị trước thuế (net amount) để phân tích cơ cấu chi tiêu. Kiểm tra tùy chọn "Dựa trên" để chắc chắn.

**Q: Muốn xem chi tiết từng lần mua một mặt hàng thì dùng báo cáo nào?**
**A:** Dùng [BC theo mặt hàng](bc-theo-mat-hang.md) để xem sổ chi tiết từng dòng mua, hoặc mở danh sách hóa đơn mua hàng và lọc theo mặt hàng.
