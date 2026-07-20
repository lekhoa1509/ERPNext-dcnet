---
title: Ngân sách
order: 8
summary: Lập ngân sách (dự toán) theo tài khoản và chiều phân tích để kiểm soát chi và chạy báo cáo so sánh ngân sách — thực tế.
---

## Mục đích

**Ngân sách** cho phép đặt mức dự toán (chi/doanh thu) cho từng tài khoản theo một chiều quản trị (Trung tâm chi phí / Dự án / chiều phân tích khác) và một năm tài chính. Hệ thống dùng ngân sách để **cảnh báo/chặn** khi chi vượt mức và để chạy **báo cáo so sánh ngân sách — thực tế (chênh lệch)**.

## Khi nào dùng

- **Đầu năm/đầu kỳ:** lập dự toán chi phí cho từng bộ phận hoặc công trình.
- **Khi cần kiểm soát chi:** đặt ngân sách để hệ thống cảnh báo khi đặt hàng/ghi chi vượt mức.
- **Định kỳ:** chạy báo cáo Chênh lệch ngân sách để so sánh thực chi với dự toán.

## Cách thực hiện

1. Mở **Ngân sách** trên menu Thiết lập.
2. Bấm **+ Thêm**:
   - **Ngân sách theo:** chọn chiều — Trung tâm chi phí, Dự án...
   - **Đối tượng:** chọn TTCP/Dự án cụ thể.
   - **Năm tài chính** áp dụng.
   - **Danh sách TK + số tiền dự toán** cho từng tài khoản.
3. **Bật phân bổ đều và chọn tần suất** (xem cảnh báo bên dưới) nếu muốn báo cáo so sánh theo tháng/quý.
4. **Lưu rồi GHI SỔ (duyệt)** — bước này bắt buộc để báo cáo nhận diện ngân sách.

## Định khoản tự động

Ngân sách **không sinh bút toán** — nó chỉ là dự toán để **kiểm soát và so sánh**. Khi chi thực tế vượt mức, hệ thống có thể cảnh báo hoặc chặn (tùy cấu hình hành động vượt ngân sách trên từng bản ngân sách).

## Tình huống đặc biệt & cảnh báo

- **Ngân sách phải được GHI SỔ (duyệt) mới chạy báo cáo.** Bản ngân sách còn ở trạng thái nháp sẽ không hiện trong báo cáo Chênh lệch ngân sách (báo cáo chỉ lấy bản đã ghi sổ). Đây là lỗi thường gặp khiến "báo cáo ra toàn số 0".
- **Muốn báo cáo so sánh theo tháng/quý, phải bật "Phân bổ đều" + chọn "Tần suất phân bổ"** (Tháng/Quý/Nửa năm/Năm). Nếu không, hệ thống không tạo bảng phân bổ kỳ → các cột kỳ trong báo cáo trống.
- **Đặt khoảng ngày ngân sách** (đầu kỳ — cuối kỳ) khớp năm tài chính, nếu không các kỳ trong báo cáo bị rỗng.
- **Ngân sách gắn theo TTCP/Dự án nào thì kiểm soát đúng chiều đó** — chi không gắn chiều tương ứng sẽ không bị đối chiếu.

## Báo cáo liên quan

- [Trung tâm chi phí](trung-tam-chi-phi.md), [Dự án](du-an.md) — chiều lập ngân sách.
- [Năm tài chính](nam-tai-chinh.md) — khung năm của ngân sách.
- Phân hệ **Tổng hợp / Báo cáo** — báo cáo Chênh lệch ngân sách.

## FAQ

**Q: Tôi lập ngân sách xong nhưng báo cáo so sánh ra toàn 0?**
**A:** Hai nguyên nhân phổ biến: (1) bản ngân sách chưa **ghi sổ (duyệt)** — báo cáo chỉ lấy bản đã ghi sổ; (2) chưa bật **Phân bổ đều** + chọn **Tần suất** → không có bảng phân bổ kỳ. Bật cả hai và ghi sổ lại.

**Q: Ngân sách có tự chặn khi tôi ghi chi vượt mức không?**
**A:** Tùy cấu hình hành động vượt ngân sách trên từng bản (cảnh báo hoặc chặn). Đặt theo nhu cầu kiểm soát của công ty.

**Q: Lập ngân sách theo cả TTCP lẫn Dự án được không?**
**A:** Mỗi bản ngân sách lập theo một chiều (TTCP hoặc Dự án). Cần kiểm soát cả hai thì lập hai bản riêng.
