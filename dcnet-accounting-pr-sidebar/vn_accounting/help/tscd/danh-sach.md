---
title: Danh sách tài sản
order: 1
summary: Quản lý hồ sơ tài sản cố định — ghi tăng, đưa vào sử dụng và theo dõi trạng thái.
---

## Mục đích

**Danh sách** là nơi quản lý hồ sơ từng tài sản cố định: mã, tên, loại tài sản, nguyên giá, ngày mua, ngày đưa vào sử dụng, người giữ và địa điểm. Mỗi tài sản là một hồ sơ riêng theo dõi suốt vòng đời từ ghi tăng đến thanh lý. Nguyên giá hạch toán vào TK 211.

## Khi nào dùng

- Khi mua/nhận tài sản mới cần ghi nhận vào hệ thống.
- Khi đưa tài sản đang sử dụng (mua từ trước) vào quản lý lần đầu.
- Tra cứu thông tin tài sản: nguyên giá, giá trị còn lại, người giữ, trạng thái khấu hao.
- Theo dõi danh mục tài sản theo loại, bộ phận, địa điểm.

## Cách thực hiện

1. Bấm **Danh sách** trên menu TSCĐ → danh sách tài sản (đã ghi sổ) mở.
2. Tạo tài sản mới theo một trong hai cách:
   - **Từ hóa đơn mua hàng** (khuyến nghị): mở hóa đơn mua hàng có dòng tài sản → "Tạo > Tài sản". Cách này tự ghi tăng Nợ TK 211 theo hóa đơn.
   - **Nhập trực tiếp:** bấm "+ Thêm" → chọn **Loại tài sản**, nhập **Tên**, **Nguyên giá**, **Ngày mua**, **Ngày đưa vào sử dụng**, người giữ, địa điểm.
3. Điền thông tin khấu hao: hệ thống lấy số kỳ khấu hao và tỷ lệ từ **Loại tài sản** (Sổ tài chính).
4. **Ghi sổ** (duyệt) tài sản để chuyển sang trạng thái đang dùng.
5. Sau khi ghi sổ, lập lịch khấu hao ở mục [Tính khấu hao](tinh-khau-hao.md).

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Tạo từ hóa đơn mua hàng | 211 | 331 (qua TK 1331 nếu có VAT) | Bút toán ghi tăng đi theo hóa đơn |
| Nhập trực tiếp (tài sản đang dùng) | 211 | 411 (hoặc 331/112) | **Cần lập bút toán mở thủ công** — xem cảnh báo |
| Đưa vào sử dụng | — | — | Chỉ đổi trạng thái, không sinh bút toán |

## Tình huống đặc biệt & cảnh báo

- **Tài sản nhập trực tiếp không tự ghi tăng:** khi tạo tài sản bằng tay (không qua hóa đơn mua hàng), hệ thống **không** tự sinh bút toán Nợ TK 211. Nếu để vậy mà vẫn chạy khấu hao, hao mòn lũy kế (Có TK 2141) sẽ lớn dần trong khi sổ không có nguyên giá → mất cân đối. Hãy lập một bút toán mở: Nợ TK 211 / Có TK 411 (nguồn vốn) khi đưa tài sản đang dùng vào hệ thống.
- **Ngưỡng ghi nhận TSCĐ:** theo TT99/2025, tài sản có nguyên giá dưới ngưỡng (mặc định 30 triệu, cấu hình trong Cài đặt VN Accounting) nên ghi nhận là **CCDC** (công cụ dụng cụ) thay vì TSCĐ.
- **TSCĐ phúc lợi:** đánh dấu cờ "TSCĐ phúc lợi" cho tài sản dùng cho phúc lợi (nhà ăn, xe đưa đón…) — khấu hao của nhóm này **không được trừ** khi tính thuế TNDN.
- **Loại tài sản phải có sẵn tài khoản:** trước khi tạo tài sản, **Loại tài sản** phải được khai báo đầy đủ TK nguyên giá (211), TK hao mòn lũy kế (2141) và TK chi phí khấu hao — nếu thiếu, khấu hao sẽ báo lỗi.

## Báo cáo liên quan

- **Sổ S21-DN:** tổng hợp toàn bộ tài sản với nguyên giá và giá trị còn lại.
- **Lịch sử khấu hao:** xem từng lần ghi khấu hao của tài sản.
- **Tính khấu hao:** bước tiếp theo sau khi ghi sổ tài sản.

## FAQ

**Q: Tài sản đã ghi sổ rồi có sửa được nguyên giá không?**
**A:** Sau khi ghi sổ, nguyên giá khóa lại. Muốn điều chỉnh giá trị, dùng nghiệp vụ nâng cấp/cải tạo (qua [Sửa chữa](sua-chua.md) loại "Nâng cấp cải tạo") để tăng nguyên giá, hoặc hủy ghi sổ nếu tài sản chưa khấu hao.

**Q: Tài sản mua nhiều cái giống nhau khai báo từng cái hay gộp?**
**A:** Mỗi tài sản vật lý nên là một hồ sơ riêng để theo dõi người giữ, địa điểm, kiểm kê và thanh lý độc lập. Có thể tạo nhiều hồ sơ một lần từ một hóa đơn mua hàng nhiều số lượng.

**Q: Vì sao danh sách chỉ hiện tài sản đã ghi sổ?**
**A:** Menu lọc sẵn tài sản đã ghi sổ (đang quản lý). Tài sản nháp chưa ghi sổ vẫn xem được khi bỏ bộ lọc trạng thái trên danh sách.
