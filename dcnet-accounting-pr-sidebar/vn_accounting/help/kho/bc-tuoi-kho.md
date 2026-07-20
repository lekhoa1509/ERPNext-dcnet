---
title: BC tuổi kho
order: 8
summary: Phân tích tuổi hàng tồn kho theo các khoảng ngày để phát hiện hàng chậm luân chuyển.
---

## Mục đích

**Báo cáo tuổi kho** phân tích hàng tồn kho theo **độ tuổi** — số ngày hàng đã nằm trong kho kể từ khi nhập. Báo cáo chia tồn thành các khoảng tuổi (ví dụ 0–30, 31–60, 61–90, trên 90 ngày) để phát hiện hàng chậm luân chuyển, hàng ứ đọng vốn hoặc sắp hết hạn dùng. Giúp kế toán và quản lý kho ra quyết định thanh lý, giảm giá, hoặc trích lập dự phòng giảm giá hàng tồn kho.

## Khi nào dùng

- Cuối kỳ: rà soát hàng tồn lâu ngày để cân nhắc trích lập dự phòng giảm giá (TK 2294).
- Quản lý kho: phát hiện hàng chậm bán, lập kế hoạch xả hàng/khuyến mãi.
- Hàng có hạn dùng: tìm hàng tồn lâu sắp hết hạn để ưu tiên xuất.
- Đánh giá vòng quay hàng tồn kho theo mặt hàng/kho.

## Cách thực hiện

1. Bấm **BC tuổi kho** trên menu Kho → báo cáo mở.
   ![Báo cáo tuổi kho](_images/bc-tuoi-kho-1.png)
2. Nhập bộ lọc:
   - **Công ty** (mặc định công ty đang làm việc).
   - **Đến ngày** (mốc tính tuổi tồn).
   - **Kho**, **Loại kho**, **Mặt hàng**, **Thương hiệu** (tùy chọn).
   - **Khoảng tuổi (range):** mặc định `30, 60, 90` — chia thành các nhóm 0–30, 31–60, 61–90, trên 90 ngày; có thể đổi.
   - Tùy chọn hiện tồn theo từng kho.
3. Bấm **Refresh** → bảng hiển thị mỗi mặt hàng với **tuổi trung bình**, **tuổi sớm nhất**, **tuổi muộn nhất**, và số lượng tồn phân bổ vào từng khoảng tuổi.

## Định khoản tự động

**Không tự định khoản** — báo cáo phân tích, chỉ tra cứu. Nếu cần trích lập dự phòng giảm giá hàng tồn kho theo kết quả phân tích, kế toán lập bút toán riêng: Nợ 632 / Có 2294 (dự phòng giảm giá hàng tồn kho).

## Tình huống đặc biệt & cảnh báo

- **Tuổi tính theo ngày nhập:** độ tuổi đo từ thời điểm hàng vào kho đến "Đến ngày"; nhập lại hàng cũ làm trẻ hóa tuổi.
- **Hàng có hạn dùng:** tuổi cao + sắp hết hạn → ưu tiên xuất/thanh lý ngay.
- **Khoảng tuổi tùy chỉnh:** đổi giá trị "range" để phù hợp đặc thù ngành (hàng mau hỏng nên dùng khoảng ngắn hơn).
- **Dự phòng giảm giá:** báo cáo chỉ gợi ý; quyết định trích lập theo chính sách kế toán và giá thị trường.
- **Báo cáo nền tảng ERP:** báo cáo chuẩn của hệ thống, mô tả theo nghiệp vụ VN.

## Báo cáo liên quan

- **BC nhập xuất tồn:** số tồn tổng hợp làm cơ sở cho phân tích tuổi.
- **Sổ chi tiết kho:** truy vết ngày nhập từng lượng hàng.
- **Số lô:** xem hạn dùng của hàng tồn lâu ngày.

## FAQ

**Q: Tuổi kho tính từ thời điểm nào?**
**A:** Từ ngày hàng được nhập vào kho đến mốc "Đến ngày" trong bộ lọc.

**Q: Đổi khoảng tuổi như thế nào?**
**A:** Sửa ô **range** (mặc định `30, 60, 90`) thành các mốc mong muốn, cách nhau dấu phẩy.

**Q: Báo cáo có tự trích lập dự phòng không?**
**A:** Không. Báo cáo chỉ phân tích tuổi tồn; trích lập dự phòng (Nợ 632 / Có 2294) là bút toán kế toán lập riêng theo chính sách.

**Q: Vì sao hàng vừa bán nhiều nhưng vẫn có tuổi cao?**
**A:** Phương pháp tính giá quyết định lượng còn lại thuộc đợt nhập nào; phần tồn còn lại có thể là hàng nhập từ lâu nếu chưa được xuất hết.
