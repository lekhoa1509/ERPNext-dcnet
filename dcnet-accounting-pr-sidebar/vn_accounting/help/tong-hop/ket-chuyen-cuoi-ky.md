---
title: Kết chuyển cuối kỳ (TK 911)
order: 12
summary: Khái niệm và quy trình kết chuyển doanh thu/chi phí về TK 911 rồi lãi/lỗ sang TK 4212 cuối kỳ kế toán.
---

## Mục đích

**Kết chuyển cuối kỳ** xác định kết quả kinh doanh của một kỳ kế toán: chuyển toàn bộ doanh thu (5xx, 7xx) và chi phí (6xx, 8xx) về TK 911 (Xác định kết quả kinh doanh), sau đó chuyển lãi/lỗ thuần về TK 4212 (Lợi nhuận sau thuế chưa phân phối năm nay) theo TT99/2025. Trong hệ thống, nghiệp vụ này được thực hiện bằng chứng từ [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md) — bài này giải thích khái niệm và quy trình tổng thể.

## Khi nào dùng

- **Cuối tháng/quý:** để biết kết quả kinh doanh kỳ này (không bắt buộc theo luật, giúp theo dõi quản trị).
- **Cuối năm tài chính:** bắt buộc theo VAS trước khi lập Báo cáo tài chính.
- Sau khi đã nhập đủ chứng từ, đã [đánh giá lại ngoại tệ](danh-gia-lai-ngoai-te.md) (nếu có ngoại tệ) và đã hạch toán thuế TNDN (cuối năm).

## Cách thực hiện

1. Mở **Phiếu kết chuyển định kỳ** (Tổng hợp) → **+ Thêm**.
2. Chọn **Loại kỳ** (Tháng/Quý/Năm) và **Ngày kết thúc kỳ**. Hệ thống tự nhận biết cuối năm hay cuối kỳ trung gian (cuối năm gồm cả TK 8211 — chi phí thuế TNDN — kết chuyển về 911).
3. Bấm **Xem trước các TK** để kiểm tra các tài khoản và số dư sẽ kết chuyển.
4. Kiểm tra số liệu kỹ, sau đó **Ghi sổ** → hệ thống tự sinh phiếu kế toán kết chuyển.
5. Mở phiếu kế toán kết chuyển, soát lại lần cuối.

## Định khoản tự động

Ba nhóm bút toán kết chuyển:

| Bút toán | TK Nợ | TK Có | Nội dung |
|---|---|---|---|
| Kết chuyển doanh thu | 5xx / 7xx | 911 | Đưa doanh thu về 911 |
| Kết chuyển chi phí | 911 | 6xx / 8xx (gồm 8211 nếu cuối năm) | Đưa chi phí về 911 |
| Kết chuyển lãi | 911 | 4212 | Khi tổng DT > tổng CP |
| Kết chuyển lỗ | 4212 | 911 | Khi tổng CP > tổng DT |

> Tài khoản 911 và 4212 lấy từ **Cài đặt kế toán**. KTT có thể chỉnh sang tài khoản chi tiết hơn nếu cần. Hệ thống tự xác định chiều Nợ/Có theo dấu số dư thực tế của từng tài khoản.

## Tình huống đặc biệt & cảnh báo

- **Làm trước khi lập báo cáo kết quả kinh doanh:** kết quả trên báo cáo phụ thuộc bút toán kết chuyển này.
- **Chênh lệch tỷ giá:** nếu có giao dịch ngoại tệ, [đánh giá lại ngoại tệ](danh-gia-lai-ngoai-te.md) (515/635) TRƯỚC khi kết chuyển.
- **Thuế TNDN cuối năm:** trước khi kết chuyển cuối năm cần đã có bút toán Nợ 8211 / Có 3334.
- **Không kết chuyển nhiều lần:** mỗi kỳ kết chuyển một lần sau khi đã nhập đủ chứng từ. Phiếu kết chuyển định kỳ có cơ chế chống ghi trùng theo Ngày kết thúc kỳ.
- **TK 4212 (không phải 421):** theo TT99/2025, lãi/lỗ năm hiện hành vào 4212; 4211 là năm trước.

## Báo cáo liên quan

- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): chứng từ thực hiện kết chuyển.
- [Đánh giá lại ngoại tệ](danh-gia-lai-ngoai-te.md): chạy trước kết chuyển nếu có ngoại tệ.
- [Khoá sổ kỳ kế toán](khoa-so-ky.md): khoá kỳ sau khi kết chuyển xong.
- [Bảng cân đối số phát sinh](trial-balance.md): kiểm tra TK 5xx-8xx về 0 sau kết chuyển.

## FAQ

**Q: Có thể kết chuyển nhiều lần trong tháng không?**
**A:** Không nên — tạo bút toán trùng. Nên kết chuyển một lần duy nhất cuối kỳ sau khi đã nhập đủ chứng từ.

**Q: Bút toán kết chuyển sinh ra có sửa được không?**
**A:** Phiếu được tạo và ghi sổ tự động. Cần điều chỉnh thì Hủy phiếu kết chuyển (đảo bút toán), sửa chứng từ gốc, rồi kết chuyển lại.

**Q: Vì sao dùng 4212 chứ không phải 421?**
**A:** TT99/2025 dùng 4212 cho lợi nhuận sau thuế chưa phân phối năm nay; 4211 cho năm trước.
