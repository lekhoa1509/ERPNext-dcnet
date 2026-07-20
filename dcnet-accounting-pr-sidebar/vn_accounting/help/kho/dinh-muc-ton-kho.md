---
title: Định mức tồn kho
order: 10
summary: Gợi ý mức tồn kho tối thiểu (điểm đặt hàng lại) dựa trên lượng xuất bình quân trong kỳ.
---

## Mục đích

**Định mức tồn kho** (mức đặt hàng lại gợi ý theo mặt hàng) phân tích **lượng hàng đã xuất** trong một khoảng thời gian để tính **lượng xuất bình quân mỗi ngày**, từ đó **đề xuất mức tồn kho tối thiểu** và điểm đặt hàng lại cho từng mặt hàng. Giúp tránh hết hàng (gián đoạn bán/sản xuất) và tránh tồn quá nhiều (ứ đọng vốn).

## Khi nào dùng

- Lập kế hoạch mua hàng: biết khi tồn xuống mức nào thì cần đặt mua lại.
- Thiết lập tồn an toàn: tính mức tồn tối thiểu theo nhịp tiêu thụ thực tế.
- Định kỳ rà soát: cập nhật điểm đặt hàng lại khi nhu cầu thay đổi theo mùa.
- Đối chiếu với cấu hình điểm đặt hàng đang khai trên mặt hàng.

## Cách thực hiện

1. Bấm **Định mức tồn kho** trên menu Kho → báo cáo mở.
   ![Báo cáo định mức tồn kho](_images/dinh-muc-ton-kho-1.png)
2. Nhập bộ lọc:
   - **Từ ngày / Đến ngày** (khoảng tính lượng xuất — bắt buộc).
   - **Nhóm hàng**, **Thương hiệu** (tùy chọn).
3. Bấm **Refresh** → bảng hiển thị mỗi mặt hàng với các cột: **Mặt hàng**, **Tên hàng**, **Nhóm hàng**, **Thương hiệu**, **Mô tả**, **Tồn an toàn**, **Số ngày giao hàng (lead time)**, **Lượng tiêu hao**, **Lượng đã giao**, **Tổng xuất**, **Lượng xuất bình quân/ngày**, **Mức đặt hàng lại gợi ý**.
4. Dùng cột "Mức đặt hàng lại gợi ý" để cập nhật điểm đặt hàng lại trên danh mục mặt hàng.

## Định khoản tự động

**Không tự định khoản** — báo cáo phân tích, chỉ tra cứu và gợi ý mức tồn, không sinh bút toán.

## Tình huống đặc biệt & cảnh báo

- **Bắt buộc chọn khoảng ngày:** thiếu "Từ ngày"/"Đến ngày" báo cáo sẽ báo lỗi cần nhập đủ; "Từ ngày" phải trước "Đến ngày".
- **Chọn kỳ đại diện:** chọn khoảng đủ dài và đại diện cho nhịp tiêu thụ; kỳ quá ngắn hoặc bất thường (mùa cao điểm) làm lệch lượng xuất bình quân.
- **Số ngày giao hàng:** mức gợi ý phụ thuộc lead time khai trên mặt hàng; lead time sai làm mức đặt hàng lại sai.
- **Hàng mới/không xuất:** mặt hàng chưa có lịch sử xuất sẽ cho lượng bình quân 0 — cần đặt mức thủ công.
- **Báo cáo nền tảng ERP:** báo cáo chuẩn của hệ thống, mô tả theo nghiệp vụ VN.

## Báo cáo liên quan

- **BC nhập xuất tồn:** tồn hiện tại so với mức đặt hàng lại gợi ý.
- **Sổ chi tiết kho:** chi tiết các lần xuất tạo nên lượng xuất bình quân.
- **BC tuổi kho:** cân đối giữa mua thêm và xả hàng tồn lâu.

## FAQ

**Q: "Mức đặt hàng lại gợi ý" tính thế nào?**
**A:** Dựa trên lượng xuất bình quân mỗi ngày (tổng xuất trong kỳ chia số ngày) nhân với số ngày giao hàng, cộng tồn an toàn. Là con số gợi ý để tham khảo.

**Q: Có tự đặt mua hàng từ báo cáo này không?**
**A:** Không. Báo cáo chỉ gợi ý mức tồn; việc đặt mua đi qua phân hệ Mua hàng (đơn mua hàng).

**Q: Vì sao một mặt hàng không có mức gợi ý?**
**A:** Thường do mặt hàng chưa có lượng xuất trong kỳ chọn, hoặc thiếu khai số ngày giao hàng/tồn an toàn trên danh mục.

**Q: Khoảng ngày nên chọn bao lâu?**
**A:** Đủ dài để đại diện cho nhịp tiêu thụ thực tế (thường 1–3 tháng), tránh chọn kỳ có biến động bất thường.
