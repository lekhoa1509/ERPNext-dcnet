---
section: TSCĐ
title: Tổng quan Tài sản cố định
summary: Phân hệ Tài sản cố định — danh sách, khấu hao, sửa chữa, bàn giao, kiểm kê, thanh lý và sổ TSCĐ theo TT99/2025.
---

## Mục đích

Phân hệ **TSCĐ** (tài sản cố định) quản lý toàn bộ vòng đời tài sản: ghi tăng (nguyên giá TK 211), tính khấu hao (hao mòn lũy kế TK 2141, chi phí khấu hao TK 627/641/642/154 tùy bộ phận sử dụng), sửa chữa, bàn giao giữa người/bộ phận, kiểm kê thực tế và thanh lý/nhượng bán. Menu bên trái gom đủ các nghiệp vụ này cùng hai sổ tra cứu: **Sổ S21-DN** (sổ TSCĐ) và **Lịch sử khấu hao**.

## Khi nào dùng

- Khi mua/nhận tài sản mới: ghi nhận tài sản và đưa vào sử dụng.
- Định kỳ (thường hằng tháng): lập lịch và ghi nhận khấu hao.
- Khi tài sản hỏng/cần nâng cấp: lập phiếu sửa chữa, phân loại chi phí hay vốn hóa.
- Khi điều chuyển tài sản giữa người giữ/bộ phận/địa điểm: lập biên bản bàn giao.
- Cuối kỳ/đột xuất: kiểm kê thực tế, đối chiếu sổ sách.
- Khi tài sản hết giá trị sử dụng hoặc bán: lập phiếu thanh lý/nhượng bán.
- Cuối tháng/quý/năm: in Sổ S21-DN để đóng quyển; tra Lịch sử khấu hao để đối chiếu chi phí khấu hao.

## Cách thực hiện

Cấu trúc menu **TSCĐ** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Danh sách | Danh sách tài sản | Toàn bộ tài sản cố định (đã ghi sổ) |
| 2 | Tính khấu hao | Danh sách | Lịch khấu hao của từng tài sản |
| 3 | Sửa chữa | Danh sách | Phiếu sửa chữa kèm hạch toán nội bộ |
| 4 | Bàn giao TSCĐ | Danh sách | Biên bản bàn giao tài sản (phạm vi TSCĐ) |
| 5 | Kiểm kê TSCĐ | Danh sách | Biên bản kiểm kê tài sản (phạm vi TSCĐ) |
| 6 | Thanh lý tài sản | Danh sách | Phiếu thanh lý/nhượng bán tài sản |
| 7 | Sổ S21-DN | Báo cáo | Sổ TSCĐ — nguyên giá, khấu hao, giá trị còn lại |
| 8 | Lịch sử khấu hao | Báo cáo | Chi tiết từng lần ghi khấu hao theo tài sản |

> Lưu ý: hai mục **Bàn giao** và **Kiểm kê** dùng chung biểu mẫu với phân hệ CCDC (công cụ dụng cụ) — cùng một loại chứng từ, chỉ khác trường **Phạm vi** (TSCĐ hoặc CCDC). Khi mở từ menu TSCĐ, hệ thống đã lọc sẵn phạm vi = TSCĐ.

### Quy trình điển hình

1. **Ghi tăng tài sản:** tạo tài sản từ hóa đơn mua hàng (mục "Tạo > Tài sản") hoặc nhập trực tiếp trong **Danh sách**. Tài sản nhập trực tiếp (không qua hóa đơn) cần một bút toán ghi tăng Nợ TK 211.
2. **Lập khấu hao:** mở **Tính khấu hao** → tạo lịch khấu hao cho tài sản → ghi sổ. Mỗi kỳ hệ thống sinh bút toán Nợ TK chi phí (627/641/642/154) / Có TK 2141.
3. **Sửa chữa khi phát sinh:** mở **Sửa chữa** → chọn phân loại (chi phí / vốn hóa / nâng cấp) → ghi sổ để sinh bút toán.
4. **Bàn giao khi điều chuyển:** mở **Bàn giao TSCĐ** → chọn người/bộ phận nhận → ghi sổ; hệ thống cập nhật người giữ + địa điểm và tạo phiếu điều chuyển tài sản.
5. **Kiểm kê định kỳ:** mở **Kiểm kê TSCĐ** → tải danh sách → ghi nhận tình trạng thực tế → duyệt; mục "Mất" sinh bút toán ghi nhận thiếu (Nợ TK 1381 / Có TK 211).
6. **Thanh lý cuối đời:** mở **Thanh lý tài sản** → chọn hình thức (bán / loại bỏ) → thực thi để sinh bút toán xóa sổ.
7. **Đối chiếu cuối kỳ:** in **Sổ S21-DN** để đóng quyển; tra **Lịch sử khấu hao** để khớp chi phí khấu hao đã ghi.

### Liên kết tới các bài hướng dẫn chi tiết

- **Quản lý tài sản:** [Danh sách tài sản](danh-sach.md).
- **Khấu hao:** [Tính khấu hao](tinh-khau-hao.md), [Lịch sử khấu hao](lich-su-khau-hao.md).
- **Sửa chữa & nâng cấp:** [Sửa chữa tài sản](sua-chua.md).
- **Điều chuyển & kiểm kê:** [Bàn giao tài sản](ban-giao.md), [Kiểm kê tài sản](kiem-ke.md).
- **Thanh lý:** [Thanh lý tài sản](thanh-ly.md).
- **Sổ sách:** [Sổ S21-DN](so-s21-dn.md), [Lịch sử khấu hao](lich-su-khau-hao.md).

## Định khoản tự động (tổng quát)

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Ghi tăng tài sản (mở sổ trực tiếp) | 211 | 331/112/411 | Bút toán mở khi tạo tài sản không qua hóa đơn |
| Khấu hao kỳ | 627/641/642/154 | 2141 | TK chi phí tùy bộ phận sử dụng |
| Sửa chữa — chi phí | 6427 | 111 | Sửa chữa thường xuyên, tính thẳng chi phí |
| Sửa chữa lớn — vốn hóa | 2413 | 331 | Tập hợp chi phí sửa chữa lớn |
| Nâng cấp cải tạo | 2412 | 331 | Tăng nguyên giá tài sản |
| VAT đầu vào (nếu có) | 1331 | (theo TK Có) | Thuế GTGT khấu trừ |
| Kiểm kê — mất tài sản | 1381 | 211 | Tài sản thiếu chờ xử lý |
| Thanh lý — xóa sổ | 2141 + 811 | 211 | Hao mòn lũy kế + giá trị còn lại / nguyên giá |
| Thanh lý — thu nhập bán (nếu bán) | 131 | 711 | Ghi nhận qua hóa đơn bán hàng |

> Mọi số hiệu TK trên chỉ là gợi ý mặc định theo TT99/2025. Tài khoản thực tế được lấy từ **Loại tài sản** (cho TK 211, 2141) và **Cài đặt VN Accounting** (cho TK thanh lý 811/711) — kế toán có thể chỉnh tài khoản trên từng chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Tài sản nhập trực tiếp thiếu bút toán ghi tăng:** tài sản tạo bằng tay (không qua hóa đơn mua hàng) không tự ghi Nợ TK 211, nhưng vẫn chạy khấu hao → hao mòn lũy kế lớn dần trong khi không có nguyên giá trên sổ. Cần lập bút toán mở Nợ TK 211 / Có TK 411 (hoặc 331/112) khi đưa tài sản đang dùng vào hệ thống.
- **Ngưỡng ghi nhận TSCĐ:** theo TT99, tài sản dưới ngưỡng (mặc định 30 triệu, cấu hình trong Cài đặt) nên ghi nhận là **CCDC** thay vì TSCĐ.
- **Ngưỡng duyệt:** thanh lý ≥ ngưỡng (mặc định 50 triệu) và bàn giao ≥ ngưỡng (mặc định 100 triệu) cần người ký duyệt — cấu hình trong Cài đặt VN Accounting, mục "Phân quyền TSCĐ & CCDC".
- **TSCĐ phúc lợi:** tài sản có cờ "TSCĐ phúc lợi" thì khấu hao không được trừ khi tính thuế TNDN — xem báo cáo Chi phí không được trừ.
- **Hủy chứng từ:** thanh lý đã thực thi có thể hủy để khôi phục tài sản; bàn giao và sửa chữa khi hủy sẽ đảo lại trạng thái/bút toán liên quan.

## Báo cáo liên quan

- **Sổ S21-DN:** sổ TSCĐ tổng hợp nguyên giá, khấu hao lũy kế, giá trị còn lại.
- **Lịch sử khấu hao:** chi tiết từng lần ghi khấu hao của tài sản.
- **Sổ S22-DN:** theo dõi TSCĐ và CCDC (in từ biên bản bàn giao).
- **Bảng cân đối số phát sinh:** số dư TK 211, 2141 cuối kỳ.
- **Chi phí không được trừ:** khấu hao TSCĐ phúc lợi loại khỏi chi phí tính thuế.

## FAQ

**Q: Tạo tài sản mới ở đâu?**
**A:** Hai đường: (1) từ hóa đơn mua hàng → "Tạo > Tài sản" (đường tự nhiên, đã có bút toán ghi tăng); (2) mở **Danh sách** trong menu TSCĐ → "+ Thêm" để nhập trực tiếp (nhớ lập bút toán mở Nợ TK 211 nếu là tài sản đang dùng đưa vào hệ thống).

**Q: Bàn giao và Kiểm kê sao lại thấy cả mục TSCĐ lẫn CCDC?**
**A:** Hai chứng từ này dùng chung biểu mẫu cho cả tài sản cố định và công cụ dụng cụ, phân biệt bằng trường **Phạm vi**. Menu TSCĐ mở sẵn phạm vi = TSCĐ; menu CCDC mở sẵn phạm vi = CCDC.

**Q: Khấu hao ghi vào tài khoản chi phí nào?**
**A:** Tùy bộ phận sử dụng: bộ phận sản xuất → TK 627, bán hàng → TK 641, quản lý doanh nghiệp → TK 642, công trình dở dang → TK 154. Tài khoản hao mòn lũy kế luôn là TK 2141. Lấy theo cấu hình trên **Loại tài sản**.
