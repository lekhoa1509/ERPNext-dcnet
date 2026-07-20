---
title: Báo cáo tình hình tài chính (B01-DN)
order: 1
summary: Bảng cân đối kế toán theo TT99/2025 — tài sản và nguồn vốn tại một thời điểm, tự kiểm tra Mã 270 = Mã 440.
---

## Mục đích

**Báo cáo tình hình tài chính (B01-DN)** theo Thông tư 99/2025/TT-BTC là tên gọi mới của Bảng cân đối kế toán. Đây là báo cáo bắt buộc, cho thấy **toàn bộ tài sản và nguồn vốn** của doanh nghiệp tại một thời điểm (thường là cuối kỳ báo cáo). Nguyên tắc cốt lõi: **Tổng tài sản (Mã 270) = Tổng nguồn vốn (Mã 440)** — luôn phải bằng nhau.

Số liệu được tính từ số dư các tài khoản trên Sổ Cái tại ngày lập báo cáo. Mỗi chỉ tiêu có một công thức tài khoản riêng (xem [Cấu hình BCTC Mapping](bctc-mapping.md)).

## Khi nào dùng

- Cuối tháng/quý/năm: lập bảng cân đối để nộp cơ quan thuế hoặc theo dõi nội bộ.
- Khi cần soát nhanh số dư tài sản — nguồn vốn tại một thời điểm bất kỳ.
- Trước khi lập B02/B03/B09 — B01 cân là tín hiệu sổ sách đã khóa đúng.

## Cách thực hiện

1. Vào **Báo cáo tài chính → Báo cáo tình hình tài chính (B01-DN)**.
2. Chọn **Công ty** (bắt buộc).
3. Chọn **Năm tài chính** và **Tháng**:
   - Chọn một tháng cụ thể → hệ thống tự đặt "Tại ngày" là ngày cuối tháng đó.
   - Để trống Tháng (chọn "Cả năm") → "Tại ngày" tự đặt là ngày cuối năm tài chính.
   - Có thể chỉnh trực tiếp ô **Tại ngày** nếu muốn snapshot tại ngày bất kỳ.
4. Báo cáo hiển thị 4 cột:
   - **Mã** — mã chỉ tiêu (110, 120, ...)
   - **Tên chỉ tiêu** — có thụt lề thể hiện cấp bậc; dòng tổng in đậm
   - **Số cuối kỳ** — số dư tại ngày lập báo cáo
   - **Số đầu năm** — số dư tại ngày 31/12 của năm liền trước
5. **Drill-through:** bấm vào con số để mở danh sách chứng từ đóng góp vào con số đó.

### Cấu trúc báo cáo

**Phần Tài sản** (mã 100 / 200 / 270):

| Mã | Nội dung | Tài khoản tiêu biểu |
|---|---|---|
| 100 | A. Tài sản ngắn hạn | = 110+120+130+140+150 |
| 110 | Tiền và tương đương tiền | 111, 112, 113 |
| 130 | Các khoản phải thu ngắn hạn | 131, 133, 136, 138, 141 |
| 140 | Hàng tồn kho | 151–158 |
| 200 | B. Tài sản dài hạn | = 220+...+260 |
| 220 | Tài sản cố định (giá trị còn lại) | 211–214 |
| **270** | **TỔNG TÀI SẢN** | **= 100 + 200** |

**Phần Nguồn vốn** (mã 300 / 400 / 440):

| Mã | Nội dung | Tài khoản tiêu biểu |
|---|---|---|
| 300 | C. Nợ phải trả | = 310+330 |
| 310 | Nợ ngắn hạn | 331, 333, 334, 335, 341 (NH) |
| 400 | D. Vốn chủ sở hữu | = 410+...+430 |
| 410 | Vốn góp của chủ sở hữu | 411 |
| 421 | Lợi nhuận sau thuế chưa phân phối | 421 |
| **440** | **TỔNG NGUỒN VỐN** | **= 300 + 400** |

## Định khoản tự động

Báo cáo này **không tự định khoản — chỉ tra cứu**. Tuy nhiên hệ thống có một xử lý quan trọng cần biết:

| Trường hợp | Hệ thống làm gì | Ghi chú |
|---|---|---|
| Báo cáo chạy giữa năm, chưa kết chuyển 911→421 | Tự thêm dòng **421b — "Lợi nhuận chưa phân phối kỳ này (chưa kết chuyển)"** vào phần vốn chủ sở hữu | Gom lãi/lỗ lũy kế từ đầu năm (TK 5xx/7xx − 6xx/8xx) để Mã 270 vẫn = Mã 440 |
| Dòng 421b được cộng vào Mã 420, 400, 440 | Mô phỏng đúng việc kết chuyển cuối năm | Loại trừ bút toán kết chuyển để không tính trùng |

Nhờ vậy, **bảng cân đối luôn cân ngay cả khi chưa khóa sổ cuối năm**.

## Tình huống đặc biệt & cảnh báo

- **Tự kiểm tra cân đối:** sau mỗi lần chạy, hệ thống so Mã 270 với Mã 440. Nếu chênh lệch vượt ngưỡng cho phép (cấu hình tại Thiết lập VN Accounting, mặc định 1 đồng), một **dòng cảnh báo ⚠️ "Mất cân đối B01"** hiện cuối báo cáo kèm số chênh lệch.
- **Nguyên nhân thường gặp khi mất cân đối:**
  1. Có bút toán còn ở trạng thái Nháp (chưa ghi sổ).
  2. Cấu hình mapping sai — một tài khoản bị tính vào 2 chỉ tiêu, hoặc bị bỏ sót khỏi mọi chỉ tiêu.
  3. Có tài khoản mới mở chưa được đưa vào mapping.
- **Chưa có cấu hình mapping:** nếu công ty chưa có BCTC Mapping, báo cáo hiện dòng nhắc "Chưa có cấu hình BCTC Mapping cho công ty này".
- **Số đầu năm = số cuối năm trước:** cột "Số đầu năm" lấy số dư tại 31/12 năm liền trước, không phải đầu kỳ báo cáo.

## Báo cáo liên quan

- [Cấu hình BCTC Mapping](bctc-mapping.md) — sửa công thức tính từng chỉ tiêu.
- [Bảng cân đối số phát sinh](bang-can-doi-so-phat-sinh.md) — đối chiếu số dư từng tài khoản với B01.
- [B02 — Kết quả HĐKD](b02-ket-qua-kinh-doanh.md), [B03 — Lưu chuyển tiền tệ](b03-luu-chuyen-tien-te.md).
- [Xuất Excel BCTC](bctc-xuat-excel.md).

## FAQ

**Q: Vì sao bảng cân đối vẫn cân dù tôi chưa kết chuyển lãi lỗ?**
**A:** Hệ thống tự thêm dòng "421b — Lợi nhuận chưa phân phối kỳ này" gom toàn bộ lãi/lỗ lũy kế từ đầu năm vào phần vốn chủ sở hữu. Sau khi bạn chạy kết chuyển 911 → 4212, số đó sẽ nằm thật trên TK 421 và dòng 421b biến mất.

**Q: Báo cáo báo "Mất cân đối B01", phải làm gì?**
**A:** Lần lượt: (1) kiểm tra còn bút toán Nháp không; (2) mở Cấu hình BCTC Mapping, xác minh không có tài khoản nào bị map vào 2 chỉ tiêu hoặc bỏ sót; (3) đối chiếu với Bảng cân đối số phát sinh xem tài khoản nào lệch.

**Q: "Tại ngày" và "Tháng/Năm tài chính" liên quan thế nào?**
**A:** Năm tài chính + Tháng chỉ là tiện ích để hệ thống tự điền "Tại ngày" thành ngày cuối tháng/cuối năm. Con số thực sự dùng để chốt số dư là ô "Tại ngày".
