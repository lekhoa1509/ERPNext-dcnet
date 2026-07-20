---
title: Phiếu kết chuyển định kỳ (911 → 4212)
order: 2
summary: Tự động kết chuyển doanh thu/chi phí (5xx-6xx-7xx-8xx) về TK 911 rồi lãi/lỗ sang TK 4212, dùng cho cả tháng/quý/năm.
---

## Mục đích

**Phiếu kết chuyển định kỳ** (số hiệu chứng từ PCV-) tự động xác định kết quả kinh doanh của một kỳ kế toán: kết chuyển toàn bộ tài khoản doanh thu (5xx, 7xx) và chi phí (6xx, 8xx) về TK 911 (Xác định kết quả kinh doanh), sau đó chuyển lãi/lỗ thuần về TK 4212 (Lợi nhuận sau thuế chưa phân phối năm nay) theo TT99/2025. Khác với phiếu khoá sổ của hệ thống nền (chỉ chạy cuối năm), phiếu này dùng được cho **tháng / quý / năm** và có cơ chế chống ghi trùng.

## Khi nào dùng

- **Cuối tháng/quý:** muốn biết kết quả kinh doanh kỳ này để theo dõi (không bắt buộc theo luật nhưng giúp quản trị).
- **Cuối năm tài chính:** bắt buộc theo VAS trước khi lập Báo cáo tài chính.
- Sau khi đã nhập đủ chứng từ trong kỳ, đã [đánh giá lại ngoại tệ](danh-gia-lai-ngoai-te.md) (nếu có giao dịch ngoại tệ) và đã hạch toán thuế TNDN (cuối năm).

## Cách thực hiện

1. Mở danh sách **Phiếu kết chuyển định kỳ** → bấm **+ Thêm**.
2. Chọn **Loại kỳ** (Tháng / Quý / Năm) và **Ngày kết thúc kỳ** (ví dụ 31/12/2026).
3. Hai trường **TK xác định kết quả KD (911)** và **TK LN chưa phân phối (4212)** tự điền từ Cài đặt kế toán khi chọn công ty — kiểm tra lại.
4. Bấm **Hành động → Xem trước các TK**. Hệ thống quét số dư từng tài khoản 5xx/6xx/7xx/8xx tại ngày kết thúc kỳ và điền vào bảng xem trước, kèm tổng doanh thu / tổng chi phí / lãi-lỗ thuần.
5. Kiểm tra kỹ các dòng xem trước.
6. Bấm **Ghi sổ** → hệ thống tự sinh 1 phiếu kế toán kết chuyển (Nợ/Có từng TK 5xx-6xx → 911, rồi 911 → 4212).
7. Sau khi ghi sổ, bấm **Mở phiếu kế toán kết chuyển** để xem chi tiết bút toán đã sinh.

## Định khoản tự động

Phiếu này SINH bút toán kết chuyển. Định khoản (theo dấu số dư thực tế của từng tài khoản):

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Kết chuyển doanh thu (số dư Có bình thường) | 5xx / 7xx | 911 | Đưa doanh thu về 911 |
| Kết chuyển doanh thu nghịch dấu (số dư Nợ — hàng bán bị trả lại) | 911 | 5xx / 7xx | Tự nhận diện theo dấu số dư |
| Kết chuyển chi phí (số dư Nợ bình thường) | 911 | 6xx / 8xx | Đưa chi phí về 911 |
| Kết chuyển chi phí nghịch dấu (số dư Có — hoàn nhập) | 6xx / 8xx | 911 | Tự nhận diện theo dấu số dư |
| Kết chuyển lãi thuần | 911 | 4212 | Khi tổng DT > tổng CP |
| Kết chuyển lỗ thuần | 4212 | 911 | Khi tổng CP > tổng DT |

> Hệ thống xác định chiều Nợ/Có theo **dấu số dư thực tế** của từng tài khoản tại ngày kết thúc kỳ, không cứng nhắc theo loại tài khoản — nhờ vậy xử lý đúng cả trường hợp doanh thu có số dư Nợ (hàng trả lại) hoặc chi phí có số dư Có (hoàn nhập dự phòng).

## Tình huống đặc biệt & cảnh báo

- **Chống ghi trùng (idempotent):** mỗi công ty chỉ được ghi sổ MỘT phiếu kết chuyển ở trạng thái Đã ghi sổ cho cùng một Ngày kết thúc kỳ. Ghi lần hai cùng ngày kết thúc sẽ bị chặn.
- **Phân biệt với Khoá sổ kỳ kế toán:** phiếu này TẠO bút toán kết chuyển; còn [Khoá sổ kỳ kế toán](khoa-so-ky.md) chỉ NGĂN hạch toán lùi vào kỳ đã đóng (không sinh bút toán). Quy trình cuối kỳ chuẩn: (1) kết chuyển định kỳ này → (2) đối chiếu sổ → (3) khoá sổ kỳ.
- **Danh sách TK kết chuyển:** lấy từ Cài đặt kế toán (bảng tài khoản doanh thu / chi phí cần kết chuyển). Nếu cài đặt trống, hệ thống tự quét toàn bộ tài khoản gốc loại Doanh thu (Income) và Chi phí (Expense).
- **Đánh giá lại ngoại tệ trước:** nếu có giao dịch ngoại tệ, hạch toán chênh lệch tỷ giá (515/635) TRƯỚC khi kết chuyển — xem [Đánh giá lại ngoại tệ](danh-gia-lai-ngoai-te.md).
- **Thuế TNDN cuối năm:** trước khi kết chuyển cuối năm cần đã có bút toán Nợ 8211 / Có 3334; khi đó TK 8211 cũng được kết chuyển sang 911.
- **Hủy phiếu = hoàn nhập:** Hủy (Cancel) phiếu sẽ hủy luôn phiếu kế toán kết chuyển đã sinh và chuyển trạng thái về Đã đảo (Reversed).

## Báo cáo liên quan

- [Đánh giá lại ngoại tệ](danh-gia-lai-ngoai-te.md): chạy TRƯỚC kết chuyển nếu có ngoại tệ.
- [Khoá sổ kỳ kế toán](khoa-so-ky.md): chạy SAU kết chuyển để chốt kỳ.
- [Bảng cân đối số phát sinh](trial-balance.md): kiểm tra TK 5xx-8xx về 0 và số dư TK 4212 sau kết chuyển.
- [Sổ cái (S03b-DN)](so-cai.md): xem chi tiết phát sinh TK 911 và 4212.

## FAQ

**Q: Phiếu này khác gì "Kết chuyển cuối kỳ" ở phần Tổng quan?**
**A:** Đây là chứng từ kết chuyển dạng bảng (có lưu, in được, chống ghi trùng theo ngày kết thúc kỳ) dùng cho cả tháng/quý/năm. Cả hai cùng tạo ra bút toán 911 → 4212 với cùng nguyên tắc.

**Q: Có thể kết chuyển nhiều lần trong tháng không?**
**A:** Không nên. Cơ chế chống ghi trùng đã chặn việc ghi sổ hai phiếu cùng một Ngày kết thúc kỳ. Nên kết chuyển một lần duy nhất sau khi đã nhập đủ chứng từ.

**Q: Vì sao dùng TK 4212 mà không phải 421?**
**A:** Theo TT99/2025, lãi/lỗ năm hiện hành chuyển vào TK 4212 (Lợi nhuận sau thuế chưa phân phối năm nay). TK 4211 dùng cho lợi nhuận năm trước.

**Q: Phiếu kế toán kết chuyển sinh ra có sửa được không?**
**A:** Phiếu kết chuyển được tạo và ghi sổ tự động. Nếu cần điều chỉnh, Hủy phiếu kết chuyển định kỳ này (sẽ hủy luôn phiếu kế toán), sửa chứng từ gốc rồi kết chuyển lại.
