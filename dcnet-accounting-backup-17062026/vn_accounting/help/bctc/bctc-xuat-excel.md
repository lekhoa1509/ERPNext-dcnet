---
title: Xuất Excel BCTC để nộp thuế
order: 14
summary: Quy trình khóa sổ, xuất Excel bộ báo cáo tài chính TT99/2025, ký đóng dấu và nộp cơ quan thuế.
---

## Mục đích

Hướng dẫn quy trình hoàn chỉnh để xuất bộ **báo cáo tài chính TT99/2025** ra Excel và nộp cơ quan thuế. Theo TT99/2025, doanh nghiệp nộp 4 báo cáo bắt buộc:

| Mã | Tên báo cáo | Cách xuất |
|---|---|---|
| B01-DN | Báo cáo tình hình tài chính | Nút menu Excel của báo cáo |
| B02-DN | Báo cáo kết quả HĐKD | Nút menu Excel của báo cáo |
| B03-DN | Báo cáo lưu chuyển tiền tệ | Nút menu Excel của báo cáo |
| B09-DN | Thuyết minh BCTC | Trang sinh file riêng (nhiều sheet) |

## Khi nào dùng

- Cuối năm tài chính: chuẩn bị hồ sơ nộp thuế.
- Khi cần bản Excel để lưu trữ hoặc gửi kế toán dịch vụ thuế.

## Cách thực hiện

### Bước 1 — Khóa sổ

Trước khi xuất, đảm bảo:
- Mọi bút toán của kỳ đã ghi sổ (không còn Nháp).
- Đã kết chuyển cuối kỳ (911 → 4212) ở phân hệ Tổng hợp.
- B01 đã cân (Mã 270 = Mã 440).

### Bước 2 — Xuất B01, B02, B03

1. Mở từng báo cáo (B01-DN / B02-DN / B03-DN), chọn công ty + kỳ.
2. Để báo cáo chạy ra số liệu trên màn hình.
3. Bấm nút **menu (•••)** ở góc trên báo cáo → chọn **Xuất / Export** → chọn định dạng **Excel**.
4. File Excel tải về theo đúng cấu trúc cột của báo cáo (Mã, Tên chỉ tiêu, số liệu kỳ này/kỳ trước).

> Lưu ý: B01/B02/B03 dùng cơ chế xuất Excel chung của hệ thống (qua nút menu báo cáo), không phải nút riêng trên màn hình.

### Bước 3 — Xuất B09 (Thuyết minh)

B09 có **trang sinh file riêng** vì gồm nhiều sheet (văn xuôi + chi tiết). Xem hướng dẫn: [Thuyết minh BCTC (B09-DN)](b09-thuyet-minh.md). Tóm tắt: vào trang, chọn công ty + năm tài chính, bấm "Sinh file B09-DN", tải file về, điền phần văn xuôi.

### Bước 4 — Kiểm tra file

Mở từng file, kiểm tra: tên công ty / mã số thuế, kỳ báo cáo, số liệu khớp màn hình, và Mã 270 = Mã 440 trên B01.

### Bước 5 — Ký, đóng dấu, nộp

- In ra giấy: người lập ký, kế toán trưởng ký, người đại diện pháp luật ký + đóng dấu.
- Nộp qua cổng thuế điện tử (thuedientu.gdt.gov.vn) hoặc phần mềm hỗ trợ kê khai — ký điện tử bằng token/CA.

## Định khoản tự động

Quy trình này **không tạo bút toán — chỉ xuất file**. Mọi số liệu lấy từ báo cáo trên màn hình (tức từ Sổ Cái). Không sửa số trực tiếp trên Excel — nếu sai, quay về sửa bút toán gốc rồi xuất lại.

## Tình huống đặc biệt & cảnh báo

- **Không sửa công thức/số trên file Excel:** chỉ điền vào ô trắng (phần văn xuôi B09). Sửa số trên Excel làm lệch với sổ sách.
- **Sai số → sửa bút toán, không sửa file:** phát hiện số sai thì về hệ thống sửa chứng từ gốc và xuất lại.
- **Lưu bản gốc:** giữ file Excel gốc trước khi điền/ký; mỗi lần xuất sinh file mới.
- **Thời hạn nộp:** doanh nghiệp thông thường không quá 90 ngày kể từ ngày kết thúc năm tài chính (DN nhà nước 60 ngày). Kiểm tra quy định hiện hành theo loại hình.
- **Định dạng nộp:** kiểm tra yêu cầu định dạng của cổng thuế (Excel/XML) tại thời điểm nộp — quy định có thể cập nhật.

## Báo cáo liên quan

- [B01](b01-cau-truc.md), [B02](b02-ket-qua-kinh-doanh.md), [B03](b03-luu-chuyen-tien-te.md), [B09 — Thuyết minh](b09-thuyet-minh.md).
- [Cấu hình BCTC Mapping](bctc-mapping.md) — nếu số liệu chỉ tiêu sai trước khi xuất.

## FAQ

**Q: B01/B02/B03 có nút "Xuất Excel" riêng không?**
**A:** Không có nút riêng. Dùng nút menu (•••) chung của báo cáo → Xuất → Excel. Riêng B09 mới có trang sinh file riêng vì gồm nhiều sheet.

**Q: Xuất ra số khác trên màn hình?**
**A:** Đảm bảo báo cáo đã chạy ra số liệu trước khi bấm xuất; file luôn lấy đúng số đang hiển thị. Nếu vẫn khác, kiểm tra bộ lọc kỳ.

**Q: Phát hiện số sai sau khi đã xuất, sửa thế nào?**
**A:** Về hệ thống sửa bút toán gốc (mở chứng từ, điều chỉnh), chạy lại báo cáo và xuất file mới. Tuyệt đối không sửa tay trên Excel.
