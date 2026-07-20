---
title: Tính khấu hao
order: 2
summary: Lập lịch khấu hao cho tài sản; mỗi kỳ sinh bút toán Nợ chi phí / Có hao mòn lũy kế TK 2141.
---

## Mục đích

**Tính khấu hao** quản lý lịch khấu hao của từng tài sản: số kỳ, ngày bắt đầu, giá trị khấu hao mỗi kỳ và hao mòn lũy kế. Khi đến kỳ, hệ thống ghi nhận chi phí khấu hao — Nợ TK chi phí (627/641/642/154 tùy bộ phận) / Có TK 2141 (hao mòn lũy kế).

## Khi nào dùng

- Ngay sau khi ghi sổ một tài sản mới: lập lịch khấu hao.
- Định kỳ hằng tháng: ghi nhận chi phí khấu hao của kỳ.
- Khi cần xem lịch khấu hao dự kiến của một tài sản (giá trị từng kỳ, ngày, lũy kế).
- Khi điều chỉnh phương pháp/thời gian khấu hao của tài sản.

## Cách thực hiện

1. Bấm **Tính khấu hao** trên menu TSCĐ → danh sách lịch khấu hao mở.
2. Bấm "+ Thêm" để lập lịch mới.
3. Chọn **Tài sản** ở trường liên kết. **Danh sách chỉ hiện các tài sản chưa có lịch khấu hao đã ghi sổ** — tránh lập trùng lịch cho cùng một tài sản.
4. Hệ thống tự điền số kỳ, tỷ lệ, ngày bắt đầu từ thông tin của tài sản (Loại tài sản → Sổ tài chính). Kiểm tra lại bảng lịch các kỳ.
5. **Ghi sổ** lịch khấu hao.
6. Đến mỗi kỳ, chi phí khấu hao được ghi nhận tự động (qua tiến trình khấu hao định kỳ của hệ thống) — sinh bút toán Nợ chi phí / Có TK 2141.

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Khấu hao tài sản bộ phận sản xuất | 627 | 2141 | Chi phí sản xuất chung |
| Khấu hao tài sản bộ phận bán hàng | 641 | 2141 | Chi phí bán hàng |
| Khấu hao tài sản bộ phận quản lý | 642 | 2141 | Chi phí quản lý doanh nghiệp |
| Khấu hao tài sản phục vụ công trình | 154 | 2141 | Chi phí sản xuất dở dang (đơn vị xây lắp) |

> TK chi phí khấu hao và TK hao mòn lũy kế (2141) lấy từ khai báo trên **Loại tài sản** của tài sản, không nhập tay từng lịch.

## Tình huống đặc biệt & cảnh báo

- **Chỉ chọn được tài sản chưa có lịch:** trường liên kết tài sản lọc sẵn những tài sản chưa có lịch khấu hao đã ghi sổ. Nếu không thấy tài sản cần tìm, có thể tài sản đó đã có lịch khấu hao rồi (mở chính lịch đó để xem/sửa).
- **Tài sản nhập trực tiếp:** khấu hao vẫn chạy dựa trên nguyên giá của tài sản, nhưng nếu chưa lập bút toán ghi tăng Nợ TK 211 (xem [Danh sách tài sản](danh-sach.md)) thì hao mòn lũy kế Có TK 2141 sẽ không có nguyên giá đối ứng → mất cân đối. Lập bút toán mở trước.
- **TSCĐ phúc lợi:** khấu hao của tài sản đánh cờ "TSCĐ phúc lợi" không được trừ khi tính thuế TNDN — xem báo cáo Chi phí không được trừ và Quyết toán TNDN.
- **Phương pháp khấu hao:** hệ thống hỗ trợ đường thẳng và các phương pháp khác theo khai báo; TT99/2025 yêu cầu phương pháp phù hợp khung thời gian khấu hao của Bộ Tài chính.

## Báo cáo liên quan

- **Lịch sử khấu hao:** xem từng lần ghi khấu hao đã phát sinh (chi phí, lũy kế, giá trị còn lại).
- **Sổ S21-DN:** tổng hợp khấu hao lũy kế và giá trị còn lại của toàn bộ tài sản.
- **Danh sách tài sản:** hồ sơ tài sản gốc.

## FAQ

**Q: Khấu hao có tự chạy hằng tháng không, hay phải bấm tay?**
**A:** Sau khi lịch khấu hao đã ghi sổ, hệ thống tự ghi nhận chi phí khấu hao đến từng kỳ qua tiến trình định kỳ. Kế toán không cần bấm thủ công từng tháng, chỉ cần đối chiếu qua **Lịch sử khấu hao**.

**Q: Lập nhầm lịch khấu hao thì sửa thế nào?**
**A:** Nếu lịch chưa ghi sổ, mở ra sửa trực tiếp. Nếu đã ghi sổ và đã có kỳ khấu hao phát sinh, cần hủy theo trình tự (hủy các bút toán khấu hao liên quan trước) — nên nhờ kế toán trưởng xử lý để tránh lệch sổ.

**Q: Một tài sản có thể có nhiều lịch khấu hao không?**
**A:** Mỗi tài sản chỉ nên có một lịch khấu hao đã ghi sổ tại một thời điểm. Đó là lý do trường chọn tài sản lọc bỏ các tài sản đã có lịch.
