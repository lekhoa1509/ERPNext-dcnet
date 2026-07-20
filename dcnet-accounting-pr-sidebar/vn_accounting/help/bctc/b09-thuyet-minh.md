---
title: Thuyết minh BCTC (B09-DN)
order: 4
summary: Trang sinh khung Excel thuyết minh nhiều sheet — app điền số liệu chi tiết, kế toán điền phần văn xuôi.
---

## Mục đích

**Thuyết minh báo cáo tài chính (B09-DN)** theo Thông tư 99/2025/TT-BTC là tài liệu bắt buộc đi kèm B01/B02/B03, giải thích chi tiết các con số trên báo cáo. Hệ thống cung cấp một **trang chức năng** sinh sẵn khung file Excel nhiều sheet:

- **Phần số liệu chi tiết (sheet 5.x):** app tự lấy từ Sổ Cái — kế toán không cần nhập.
- **Phần văn xuôi (sheet 1):** kế toán trưởng điền thủ công (đặc điểm doanh nghiệp, chính sách kế toán).

## Khi nào dùng

- Cuối năm: sau khi đã lập B01/B02/B03, sinh khung B09 để hoàn thiện bộ BCTC nộp thuế.
- Khi cần bảng chi tiết phải thu/phải trả/biến động tài sản theo định dạng thuyết minh.

## Cách thực hiện

1. Vào **Báo cáo tài chính → Thuyết minh BCTC (B09-DN)**.
2. Chọn **Công ty** (lọc các công ty Việt Nam).
3. Chọn **Năm tài chính** — số liệu sheet chi tiết tổng hợp theo niên độ này.
4. Bấm **Sinh file B09-DN**.
5. Hệ thống tạo file Excel nhiều sheet, liệt kê các sheet đã tạo và hiện nút **Tải file B09-DN**.

### Các sheet trong file

| Sheet | Tên | Nội dung | Nguồn |
|---|---|---|---|
| 1 | `1_Van_xuoi` | Thuyết minh văn xuôi (đặc điểm DN, chính sách kế toán) | ✍️ Kế toán điền |
| 5.1 | `5.1_Chi_tiet_phai_thu` | Chi tiết các khoản phải thu (TK 131) | 🤖 Tự động |
| 5.2 | `5.2_Chi_tiet_phai_tra` | Chi tiết các khoản phải trả (TK 331) | 🤖 Tự động |
| 5.3 | `5.3_Bien_dong_TSCD` | Biến động tài sản cố định | 🤖 Tự động |
| 5.4 | `5.4_Bien_dong_HTK` | Biến động hàng tồn kho | 🤖 Tự động |
| 5.6 | `5.6_Bien_dong_VCSH` | Biến động vốn chủ sở hữu | 🤖 Tự động |

> Các sheet 5.x chỉ xuất hiện khi có dữ liệu tương ứng. Nếu trong kỳ không phát sinh, sheet đó sẽ không được tạo.

### Quy ước màu trong file

- **Nền xám:** ô do app điền sẵn từ hệ thống — **không xóa, không sửa**.
- **Nền trắng:** ô kế toán cần điền thêm.

## Định khoản tự động

Chức năng này **không tạo bút toán** — chỉ tổng hợp số liệu từ Sổ Cái thành file Excel. Sheet chi tiết lấy số dư tài khoản tại ngày kết thúc năm tài chính; biến động tài sản/vốn lấy theo cả niên độ.

## Tình huống đặc biệt & cảnh báo

- **Phần văn xuôi do kế toán trưởng chịu trách nhiệm:** app không thể tự điền ngành nghề, chính sách ghi nhận doanh thu, phương pháp khấu hao, phương pháp tính giá hàng tồn kho — kế toán phải điền trước khi nộp.
- **File tạo mới mỗi lần bấm:** mỗi lần sinh ra một file mới. Nếu đã điền văn xuôi vào file cũ rồi sinh lại, phần điền sẽ không tự chuyển sang — hãy giữ bản đã điền cẩn thận.
- **Sự kiện sau ngày kết thúc kỳ (Phần VI):** ghi nhận thủ công các sự kiện từ ngày khóa sổ đến ngày ký BCTC (kiện tụng mới, thanh lý tài sản lớn, thay đổi cổ đông...).
- **Chỉ áp dụng công ty Việt Nam:** ô chọn công ty lọc theo quốc gia Việt Nam.

## Báo cáo liên quan

- [B01 — Tình hình tài chính](b01-cau-truc.md), [B02 — Kết quả HĐKD](b02-ket-qua-kinh-doanh.md), [B03 — Lưu chuyển tiền tệ](b03-luu-chuyen-tien-te.md).
- [Xuất Excel BCTC](bctc-xuat-excel.md) — quy trình nộp toàn bộ bộ báo cáo.

## FAQ

**Q: Sinh file xong mà thiếu sheet chi tiết TSCĐ/HTK?**
**A:** Sheet 5.x chỉ tạo khi có dữ liệu. Nếu năm đó không có biến động TSCĐ hoặc không phát sinh hàng tồn kho, sheet tương ứng sẽ không xuất hiện — đúng thiết kế.

**Q: Tôi đã điền văn xuôi nhưng bấm "Sinh file" lại, có mất không?**
**A:** Lần sinh sau tạo file mới hoàn toàn (phần văn xuôi trống). Hãy điền văn xuôi vào file tải về và lưu riêng; chỉ sinh lại khi cần làm lại từ đầu.

**Q: Ô nền xám có được sửa không?**
**A:** Không nên. Ô nền xám là số liệu hệ thống lấy từ Sổ Cái. Nếu thấy sai, quay về sửa bút toán gốc rồi sinh lại, đừng sửa tay trên Excel.
