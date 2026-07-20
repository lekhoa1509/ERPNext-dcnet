---
section: Báo cáo tài chính
title: Tổng quan Báo cáo tài chính
summary: Bộ báo cáo tài chính TT99/2025 (B01/B02/B03/B09), quyết toán thuế TNDN, phân tích lợi nhuận và cấu hình mapping.
---

## Mục đích

Phân hệ **Báo cáo tài chính** tập hợp toàn bộ báo cáo cuối kỳ của doanh nghiệp: bộ báo cáo tài chính bắt buộc theo **Thông tư 99/2025/TT-BTC** (B01/B02/B03/B09), Bảng cân đối số phát sinh, quyết toán thuế TNDN, các báo cáo phân tích lợi nhuận theo dự án/trung tâm chi phí, và màn hình cấu hình công thức tính từng chỉ tiêu (BCTC Mapping).

Tất cả báo cáo lấy số liệu trực tiếp từ Sổ Cái (các bút toán đã ghi sổ). Mỗi chỉ tiêu trên B01/B02/B03 đều được tính bằng một **công thức tài khoản** hoặc **công thức mã** do người dùng xem được và sửa được — không có con số nào "ẩn" trong mã nguồn.

## Khi nào dùng

- **Cuối tháng/quý/năm:** lập bộ báo cáo tài chính TT99/2025 để nộp cơ quan thuế.
- **Theo dõi nội bộ:** xem B02 (kết quả kinh doanh) và Bảng cân đối số phát sinh để kiểm tra số dư các tài khoản.
- **Quyết toán năm:** chạy "Quyết toán TNDN" để điều phối lợi nhuận kế toán sang thu nhập chịu thuế, và "Chi phí không được trừ (B4)" để xem chi tiết các khoản bị loại.
- **Phân tích quản trị:** xem lợi nhuận theo dự án/trung tâm chi phí, so sánh thực tế với ngân sách, tóm tắt dự án.
- **Khi mở tài khoản chi tiết đặc thù:** vào Cấu hình BCTC Mapping để điều chỉnh công thức tính chỉ tiêu.

## Cách thực hiện

Cấu trúc menu **Báo cáo tài chính** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Báo cáo tình hình tài chính (B01-DN) | Báo cáo | Bảng cân đối kế toán theo TT99/2025 — tài sản & nguồn vốn tại 1 thời điểm |
| 2 | Báo cáo kết quả HĐKD (B02-DN) | Báo cáo | Doanh thu, chi phí, lợi nhuận trong kỳ |
| 3 | Báo cáo lưu chuyển tiền tệ (B03-DN) | Báo cáo | Dòng tiền vào/ra theo phương pháp gián tiếp |
| 4 | Thuyết minh BCTC (B09-DN) | Trang chức năng | Sinh khung Excel nhiều sheet, kế toán điền văn xuôi |
| 5 | Quyết toán TNDN (Form 03) | Báo cáo | Điều phối LN kế toán → thu nhập chịu thuế → thuế TNDN phải nộp |
| 6 | Chi phí không được trừ (B4) | Báo cáo | Danh sách chi tiết khoản chi bị loại, gom theo lý do |
| 7 | Tư vấn — Chi phí không trừ TNDN | Tài liệu | Hướng dẫn nghiệp vụ xử lý chi phí không được trừ |
| 8 | Phân tích lợi nhuận (TTCP/Dự án) | Báo cáo | Lãi/lỗ theo trung tâm chi phí hoặc dự án |
| 9 | So sánh ngân sách (Thực tế vs KH) | Báo cáo | Chênh lệch giữa số thực tế và ngân sách đã lập |
| 10 | BC lãi lỗ quản trị | Báo cáo | Kết quả kinh doanh dạng quản trị (có so sánh kỳ) |
| 11 | Tóm tắt dự án | Báo cáo | Tổng hợp doanh thu/chi phí/lợi nhuận theo từng dự án |
| 12 | Cấu hình BCTC Mapping | Danh mục | Sửa công thức tính từng chỉ tiêu B01/B02/B03 |
| 13 | Bảng cân đối số phát sinh | Báo cáo | Số dư đầu kỳ, phát sinh, số dư cuối kỳ của mọi tài khoản |

### Quy trình điển hình (cuối năm)

1. **Khóa sổ:** ghi sổ toàn bộ bút toán của kỳ (không còn Nháp), thực hiện kết chuyển cuối kỳ (911 → 421).
2. **Kiểm tra cân đối:** mở Bảng cân đối số phát sinh — tổng phát sinh Nợ phải bằng tổng phát sinh Có.
3. **Lập B01:** mở Báo cáo tình hình tài chính, chọn ngày lập → kiểm tra **Mã 270 = Mã 440**.
4. **Lập B02, B03:** mở từng báo cáo, chọn kỳ.
5. **Lập B09:** vào trang Thuyết minh BCTC, sinh file Excel, kế toán điền phần văn xuôi.
6. **Quyết toán thuế:** chạy "Quyết toán TNDN (Form 03)", đối chiếu B4 với báo cáo "Chi phí không được trừ".
7. **Nộp:** xuất Excel từng báo cáo, ký tên đóng dấu, nộp qua cổng thuế điện tử.

### Liên kết tới các bài hướng dẫn chi tiết

- **Bộ BCTC TT99/2025:** [B01 — Tình hình tài chính](b01-cau-truc.md), [B02 — Kết quả HĐKD](b02-ket-qua-kinh-doanh.md), [B03 — Lưu chuyển tiền tệ](b03-luu-chuyen-tien-te.md), [B09 — Thuyết minh](b09-thuyet-minh.md).
- **Thuế TNDN:** [Quyết toán TNDN (Form 03)](quyet-toan-tndn.md), [Chi phí không được trừ (B4)](chi-phi-khong-duoc-tru.md).
- **Phân tích quản trị:** [Phân tích lợi nhuận](phan-tich-loi-nhuan.md), [So sánh ngân sách](so-sanh-ngan-sach.md), [Lãi lỗ quản trị](lai-lo-quan-tri.md), [Tóm tắt dự án](tom-tat-du-an.md).
- **Tra cứu & cấu hình:** [Bảng cân đối số phát sinh](bang-can-doi-so-phat-sinh.md), [Cấu hình BCTC Mapping](bctc-mapping.md), [Xuất Excel BCTC](bctc-xuat-excel.md).

## Định khoản tự động

Phân hệ này **không tự động tạo bút toán** — toàn bộ là báo cáo tra cứu và màn hình cấu hình. Số liệu được tính từ các bút toán đã ghi sổ ở những phân hệ khác (Tiền mặt, Ngân hàng, Mua hàng, Bán hàng, Tổng hợp). Việc kết chuyển cuối kỳ (911 → 4212) được thực hiện ở phân hệ Tổng hợp, không phải tại đây.

## Tình huống đặc biệt & cảnh báo

- **Báo cáo lấy từ bút toán ĐÃ ghi sổ:** bút toán còn ở trạng thái Nháp không được tính. Nếu số liệu thiếu, kiểm tra xem có bút toán chưa ghi sổ không.
- **B01 chưa kết chuyển vẫn cân:** hệ thống tự động bù lợi nhuận chưa phân phối của kỳ hiện hành vào nguồn vốn (dòng "421b"), nên Mã 270 = Mã 440 ngay cả khi chưa chạy kết chuyển 911 → 421.
- **Bút toán kết chuyển bị loại khỏi báo cáo kết quả kinh doanh:** B02, B03, Quyết toán TNDN tự động loại các bút toán kết chuyển (bút toán khóa sổ năm + bút toán gắn cờ kết chuyển) để không tính trùng doanh thu/chi phí.
- **TT99/2025 hiệu lực 01/01/2026:** mọi mã chỉ tiêu, tên báo cáo và mapping mặc định theo TT99/2025. B01-DN có tên "Báo cáo tình hình tài chính" (thay tên "Bảng cân đối kế toán" của TT200 cũ).

## Báo cáo liên quan

- **Sổ Cái, Sổ Nhật ký chung:** xem ở phân hệ Tổng hợp — chi tiết phát sinh từng tài khoản.
- **Tờ khai thuế GTGT (01/GTGT):** xem ở phân hệ Thuế.
- **Bảng cân đối số phát sinh:** điểm khởi đầu để soát số dư trước khi lập BCTC.

## FAQ

**Q: Báo cáo nào là bắt buộc nộp cho cơ quan thuế?**
**A:** Theo TT99/2025, bộ báo cáo tài chính bắt buộc gồm B01-DN, B02-DN, B03-DN và B09-DN (thuyết minh). Tờ khai quyết toán thuế TNDN (Form 03/TNDN) nộp riêng theo Luật Quản lý thuế.

**Q: Vì sao lợi nhuận trên B02 khác số thuế TNDN × 20%?**
**A:** Đó là bình thường. Lợi nhuận kế toán (B02) ghi nhận đầy đủ chi phí; thu nhập chịu thuế phải cộng thêm chi phí không được trừ (B4) và trừ thu nhập miễn thuế (B6). Báo cáo "Quyết toán TNDN" giải trình chênh lệch này.

**Q: Tôi mở tài khoản con khác chuẩn, báo cáo có tự cập nhật không?**
**A:** Nếu mã tài khoản con bắt đầu đúng đầu số chuẩn (vd 1111, 1112 đều bắt đầu 111) và công thức dùng wildcard (`+111%`), thì tự bao gồm. Nếu mở đầu số đặc thù, vào Cấu hình BCTC Mapping để bổ sung.

**Q: Báo cáo "Phân tích lợi nhuận", "So sánh ngân sách" là báo cáo gì?**
**A:** Đây là báo cáo phân tích quản trị có sẵn trong hệ thống (không phải biểu mẫu thuế). Dùng để theo dõi lãi/lỗ theo dự án, trung tâm chi phí và so sánh với ngân sách đã lập.
