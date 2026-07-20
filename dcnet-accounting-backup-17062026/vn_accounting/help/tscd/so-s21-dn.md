---
title: Sổ S21-DN
order: 7
summary: Sổ tài sản cố định theo TT99/2025 — nguyên giá, số kỳ và tỷ lệ khấu hao, GTKH lũy kế, giá trị còn lại.
---

## Mục đích

**Sổ S21-DN** là sổ tài sản cố định (mẫu 01-TSCĐ theo TT99/2025), tổng hợp toàn bộ tài sản đang quản lý của công ty với các cột chuẩn: nguyên giá, số kỳ khấu hao, tỷ lệ khấu hao năm, giá trị khấu hao năm, giá trị khấu hao lũy kế và giá trị còn lại. Đây là sổ tra cứu/in ấn, không nhập liệu.

## Khi nào dùng

- Cuối tháng/quý/năm: in sổ TSCĐ để đóng quyển, ký xác nhận.
- Tra cứu nhanh giá trị còn lại của toàn bộ tài sản.
- Đối chiếu khấu hao lũy kế với số dư TK 2141 trên Bảng cân đối số phát sinh.
- Lọc tài sản theo loại, địa điểm, trạng thái.

## Cách thực hiện

1. Bấm **Sổ S21-DN** trên menu TSCĐ → báo cáo mở.
2. Lọc theo:
   - **Company** (bắt buộc) — mặc định công ty đang dùng.
   - **Asset Category** (loại tài sản) — tùy chọn.
   - **Location** (địa điểm) — tùy chọn.
   - **Status** (trạng thái) — In Location / Issued / Partially Depreciated / Fully Depreciated.
3. Bấm **Refresh**. Bảng hiển thị các cột: Mã TS | Tên tài sản | Ngày đưa vào SD | Nguyên giá | Số kỳ KH | % KH năm | GTKH năm | GTKH lũy kế | Giá trị còn lại | Ghi chú.
4. Bấm vào mã tài sản để mở hồ sơ tài sản gốc.

## Định khoản tự động

Sổ S21-DN là báo cáo, **không tự định khoản** — chỉ tổng hợp số liệu từ hồ sơ tài sản. Các cột phản ánh:

| Cột | Nguồn | Ghi chú |
|---|---|---|
| Nguyên giá | Tổng chi phí tài sản (TK 211) | Bao gồm chi phí liên quan đã vốn hóa |
| Số kỳ KH, % KH năm | Sổ tài chính của tài sản (Loại tài sản) | Lấy dòng sổ tài chính đầu tiên |
| GTKH năm | Nguyên giá × tỷ lệ KH năm | Tính trên báo cáo |
| GTKH lũy kế | Nguyên giá − giá trị còn lại | Đối ứng số dư TK 2141 |
| Giá trị còn lại | Giá trị sau khấu hao của tài sản | — |

## Tình huống đặc biệt & cảnh báo

- **Phải chọn công ty:** không chọn công ty thì báo cáo báo lỗi yêu cầu chọn — đây là lọc bắt buộc.
- **Loại trừ tài sản đã loại bỏ:** sổ chỉ liệt kê tài sản đã ghi sổ và **không** bao gồm tài sản trạng thái "Scrapped" (đã loại bỏ). Tài sản đã bán vẫn xuất hiện theo trạng thái tương ứng.
- **Tỷ lệ khấu hao lấy từ sổ tài chính đầu tiên:** cột số kỳ/% KH lấy dòng sổ tài chính đầu tiên của tài sản; nếu tài sản chưa khai báo sổ tài chính thì hai cột này = 0.
- **GTKH năm là ước tính theo tỷ lệ:** cột "GTKH năm" tính bằng nguyên giá × tỷ lệ KH năm; với phương pháp khấu hao không đều, con số này mang tính tham khảo, số khấu hao thực tế xem ở [Lịch sử khấu hao](lich-su-khau-hao.md).
- **Mẫu in chính thức:** in sổ S21-DN theo TT99/2025 bằng mẫu in đã có (chữ ký người lập, kế toán trưởng).

## Báo cáo liên quan

- **Lịch sử khấu hao:** chi tiết từng lần ghi khấu hao theo tài sản (số khấu hao thực tế).
- **Sổ S22-DN:** theo dõi TSCĐ và CCDC.
- **Bảng cân đối số phát sinh:** đối chiếu số dư TK 211, 2141 cuối kỳ.
- **Danh sách tài sản:** hồ sơ tài sản gốc.

## FAQ

**Q: Tổng giá trị còn lại trên sổ có khớp với Bảng cân đối số phát sinh không?**
**A:** Khớp với chênh lệch số dư TK 211 trừ TK 2141 (giá trị còn lại của TSCĐ). Nếu lệch, kiểm tra tài sản nhập trực tiếp thiếu bút toán ghi tăng Nợ TK 211, hoặc tài sản đã thanh lý chưa xóa sổ đầy đủ.

**Q: Vì sao không thấy tài sản vừa thanh lý loại bỏ?**
**A:** Sổ loại trừ tài sản trạng thái "Scrapped". Đây là hành vi đúng — sổ TSCĐ chỉ phản ánh tài sản đang quản lý. Xem lịch sử thanh lý qua Sổ Cái (bút toán TK 811/211).

**Q: GTKH năm trên sổ có phải số khấu hao đã ghi không?**
**A:** Không hẳn. Đó là giá trị ước tính theo tỷ lệ năm (nguyên giá × % KH năm). Số khấu hao thực tế đã ghi nhận từng kỳ xem ở báo cáo [Lịch sử khấu hao](lich-su-khau-hao.md).
