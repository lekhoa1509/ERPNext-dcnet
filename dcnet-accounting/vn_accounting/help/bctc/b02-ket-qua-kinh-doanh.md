---
title: Báo cáo kết quả hoạt động kinh doanh (B02-DN)
order: 2
summary: Báo cáo doanh thu, chi phí và lợi nhuận trong kỳ theo TT99/2025, kèm so sánh cùng kỳ năm trước.
---

## Mục đích

**Báo cáo kết quả hoạt động kinh doanh (B02-DN)** theo Thông tư 99/2025/TT-BTC trình bày toàn bộ doanh thu, chi phí và lợi nhuận của doanh nghiệp **trong một khoảng thời gian** (tháng/quý/năm). Khác với B01 (chụp số dư tại một thời điểm), B02 phản ánh **luồng phát sinh trong kỳ**.

Mỗi chỉ tiêu được tính bằng tổng phát sinh của các tài khoản loại 5xx/6xx/7xx/8xx trong kỳ, theo công thức cấu hình trong [BCTC Mapping](bctc-mapping.md).

## Khi nào dùng

- Cuối tháng/quý/năm: lập báo cáo lãi lỗ chính thức để nộp thuế.
- Theo dõi định kỳ: xem doanh thu và lợi nhuận có đạt kế hoạch không.
- Đối chiếu với báo cáo quản trị và quyết toán thuế TNDN (lợi nhuận kế toán là điểm xuất phát của Form 03).

## Cách thực hiện

1. Vào **Báo cáo tài chính → Báo cáo kết quả HĐKD (B02-DN)**.
2. Chọn **Công ty** và **kỳ báo cáo** (Từ ngày — Đến ngày). Mặc định là tháng hiện hành.
3. Báo cáo hiển thị 4 cột:
   - **Mã** — mã chỉ tiêu (01, 02, ...)
   - **Tên chỉ tiêu** — dòng tổng in đậm
   - **Kỳ này** — số phát sinh trong kỳ đã chọn
   - **Kỳ trước** — cùng khoảng thời gian của năm liền trước (để so sánh)
4. Bấm vào con số để xem chi tiết chứng từ.

### Cấu trúc các chỉ tiêu chính (TT99/2025)

| Mã | Chỉ tiêu | Nguồn |
|---|---|---|
| 01 | Doanh thu bán hàng và cung cấp dịch vụ | TK 511 |
| 02 | Các khoản giảm trừ doanh thu | TK 521 |
| 10 | Doanh thu thuần | = 01 − 02 |
| 11 | Giá vốn hàng bán | TK 632 |
| 20 | Lợi nhuận gộp | = 10 − 11 |
| 21 | Doanh thu hoạt động tài chính | TK 515 |
| 22 | Chi phí tài chính | TK 635 |
| 25 | Chi phí bán hàng | TK 641 |
| 26 | Chi phí quản lý doanh nghiệp | TK 642 |
| 30 | Lợi nhuận thuần từ HĐKD | = 20+21−22−25−26 |
| 50 | Tổng lợi nhuận kế toán trước thuế | |
| 51 | Chi phí thuế TNDN hiện hành | TK 8211 |
| 60 | Lợi nhuận sau thuế TNDN | |

## Định khoản tự động

Báo cáo này **không tự định khoản — chỉ tra cứu**. Một điểm quan trọng về cách tính:

- Hệ thống tự **loại trừ bút toán kết chuyển cuối kỳ** (bút toán khóa sổ năm của hệ thống + bút toán kế toán được gắn cờ kết chuyển, gồm cả bút toán "Kết chuyển lãi lỗ" dạng nhập liệu). Nếu không loại, doanh thu/chi phí sẽ bị tính trùng (vừa phát sinh gốc, vừa bút toán kết chuyển sang 911).
- Nhờ vậy số liệu B02 phản ánh đúng phát sinh thực, không phụ thuộc việc đã chạy kết chuyển hay chưa.

## Tình huống đặc biệt & cảnh báo

- **Kỳ trước = cùng khoảng năm trước:** cột "Kỳ trước" lấy đúng khoảng ngày tương ứng của năm liền trước (vd kỳ này 01/01–31/03/2026 thì kỳ trước là 01/01–31/03/2025). Nếu năm trước chưa có dữ liệu, cột này bằng 0.
- **Lợi nhuận kế toán ≠ thu nhập chịu thuế:** lợi nhuận trên B02 ghi nhận đầy đủ chi phí thực phát sinh. Để ra số thuế phải nộp cần cộng thêm chi phí không được trừ — xem [Quyết toán TNDN](quyet-toan-tndn.md).
- **Giảm trừ doanh thu / chi phí hiển thị âm:** một số chỉ tiêu dùng hệ số dấu −1 để trừ khỏi tổng — đây là cấu hình mapping bình thường.
- **Chưa có mapping:** nếu công ty chưa cấu hình BCTC Mapping, báo cáo hiện dòng nhắc thiết lập.

## Báo cáo liên quan

- [B01 — Tình hình tài chính](b01-cau-truc.md), [B03 — Lưu chuyển tiền tệ](b03-luu-chuyen-tien-te.md).
- [Quyết toán TNDN (Form 03)](quyet-toan-tndn.md) — lấy lợi nhuận kế toán làm điểm xuất phát.
- [BC lãi lỗ quản trị](lai-lo-quan-tri.md) — phiên bản phân tích quản trị của kết quả kinh doanh.
- [Cấu hình BCTC Mapping](bctc-mapping.md), [Xuất Excel BCTC](bctc-xuat-excel.md).

## FAQ

**Q: Tôi đã chạy kết chuyển 911, số liệu B02 có bị tính trùng không?**
**A:** Không. Hệ thống tự loại các bút toán kết chuyển khi tính B02, nên chạy kết chuyển hay chưa, số liệu vẫn đúng.

**Q: Cột "Kỳ trước" trống/bằng 0?**
**A:** Do năm liền trước chưa có bút toán trong khoảng tương ứng. Bình thường với năm đầu hoạt động hoặc năm đầu chuyển dữ liệu.

**Q: Lợi nhuận sau thuế trên B02 có phải số thuế TNDN phải nộp không?**
**A:** Không. B02 phản ánh lợi nhuận kế toán. Số thuế phải nộp tính riêng tại "Quyết toán TNDN" sau khi điều chỉnh chi phí không được trừ và các khoản miễn/giảm.
