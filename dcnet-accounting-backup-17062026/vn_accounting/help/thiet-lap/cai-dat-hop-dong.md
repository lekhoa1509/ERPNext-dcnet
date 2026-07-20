---
title: Cài đặt Hợp đồng
order: 14
summary: Cấu hình mặc định cho phân hệ Hợp đồng — TK doanh thu, mẫu thuế VAT, điều khoản thanh toán, cách tính lịch thu tiền, người đại diện và ánh xạ chi nhánh — trung tâm chi phí.
---

## Mục đích

**Cài đặt Hợp đồng** khai báo các giá trị mặc định cho phân hệ **Hợp đồng**: tài khoản doanh thu, mẫu thuế VAT áp cho hóa đơn tự sinh, điều khoản thanh toán, quy tắc làm tròn và đơn vị hiển thị tiền, cách tính lịch thu tiền theo ngày, người đại diện mặc định (Bên B), và bảng ánh xạ chi nhánh — trung tâm chi phí.

Màn hình **không tạo bút toán** — nó quyết định TK doanh thu và mẫu thuế mà hóa đơn của hợp đồng sẽ dùng khi ghi sổ.

## Khi nào dùng

- **Khi triển khai phân hệ Hợp đồng:** khai TK doanh thu, mẫu thuế VAT, điều khoản thanh toán trước khi tạo hợp đồng và xuất hóa đơn.
- **Khi đổi chính sách thanh toán/làm tròn:** cập nhật chế độ làm tròn, đơn vị hiển thị, công thức tính theo ngày.
- **Khi nhiều chi nhánh:** khai bảng ánh xạ chi nhánh → trung tâm chi phí để hóa đơn gắn đúng chiều phân tích.

## Cách thực hiện

1. Mở **Cài đặt Hợp đồng** trên menu Thiết lập.
2. Khai các nhóm:

**Cài đặt chung**
- *Điều khoản thanh toán mặc định* (Payment Terms Template).
- *Chế độ làm tròn:* Làm tròn lên (Half-up) hoặc Làm tròn ngân hàng (Bankers).
- *Đơn vị hiển thị tiền tệ:* VND hoặc 1000 VND.

**Người đại diện mặc định (Bên B)**
- *Người đại diện* và *Chức vụ* mặc định để điền vào hợp đồng.

**Lịch thu tiền**
- *Thời gian gia hạn quá hạn (ngày)* (mặc định 15).
- *Công thức tính theo ngày:* theo số ngày thực trong tháng (days_in_month) hoặc cố định 30 ngày (fixed_30).
- *Gộp phí lắp đặt vào kỳ đầu* (mặc định tắt).

**Vòng đời hợp đồng**
- *Thông báo hết hạn trước (ngày)* (mặc định 30).
- *Tự động gia hạn* (mặc định tắt).

**Tài khoản (Accounting)**

| Ô cấu hình | TK gợi ý | Vai trò |
|---|---|---|
| TK doanh thu mặc định | 5113 | Doanh thu cho hóa đơn hợp đồng (ghi đè mặc định công ty) |
| Mẫu thuế bán hàng mặc định | (mẫu VAT) | Áp thuế GTGT cho hóa đơn tự sinh |

**Chi nhánh — Trung tâm chi phí**
- *Bảng ánh xạ chi nhánh → TTCP:* mỗi dòng gán một chi nhánh với một trung tâm chi phí để hóa đơn gắn đúng chiều phân tích.

3. Lưu.

## Định khoản tự động

Màn hình này **không sinh bút toán**. Nó **quyết định TK + mẫu thuế** dùng khi hóa đơn của hợp đồng được tạo và ghi sổ:

| Khi hóa đơn hợp đồng ghi sổ | TK lấy từ Cài đặt Hợp đồng |
|---|---|
| Doanh thu | TK doanh thu mặc định (vd 5113) |
| Thuế GTGT đầu ra | Theo mẫu thuế bán hàng mặc định (vd 3331) |
| Chiều phân tích (TTCP) | Theo bảng ánh xạ chi nhánh → TTCP |

## Tình huống đặc biệt & cảnh báo

- **TK doanh thu ở đây ghi đè TK doanh thu mặc định của công ty** cho hóa đơn hợp đồng — đặt đúng TK 511x theo chính sách (vd 5113 cho dịch vụ).
- **Mẫu thuế bán hàng phải khớp thuế suất GTGT** áp dụng (8% / 10% theo từng giai đoạn quy định) — sai mẫu thuế dẫn tới sai số thuế trên hóa đơn.
- **Công thức tính theo ngày ảnh hưởng số tiền kỳ đầu/cuối** khi hợp đồng bắt đầu/kết thúc giữa tháng — chọn days_in_month hoặc fixed_30 theo chính sách và giữ nhất quán.
- **Ánh xạ chi nhánh → TTCP nên khai đủ** nếu công ty nhiều chi nhánh, để báo cáo lãi/lỗ theo chi nhánh chính xác.
- **Làm tròn ảnh hưởng tổng tiền** — chọn chế độ làm tròn theo chuẩn kế toán công ty áp dụng.

## Báo cáo liên quan

- [Mẫu hợp đồng](mau-hop-dong.md) — biểu mẫu văn bản hợp đồng.
- [Cây tài khoản](cay-tai-khoan.md) — TK doanh thu (511x) và TK thuế (3331).
- [Trung tâm chi phí](trung-tam-chi-phi.md) — đích của bảng ánh xạ chi nhánh.
- Phân hệ **Hợp đồng & PAKD** — lịch thu tiền, hóa đơn định kỳ.

## FAQ

**Q: Hóa đơn hợp đồng ghi doanh thu vào TK nào?**
**A:** Vào "TK doanh thu mặc định" khai ở đây (ví dụ 5113). Giá trị này ghi đè TK doanh thu mặc định của công ty cho riêng hóa đơn hợp đồng.

**Q: Tôi để trống "Mẫu thuế bán hàng mặc định" thì sao?**
**A:** Hóa đơn tự sinh có thể không tự áp thuế GTGT đúng. Nên khai mẫu thuế khớp thuế suất hiện hành để số thuế và TK 3331 lên đúng.

**Q: "Gộp phí lắp đặt vào kỳ đầu" để làm gì?**
**A:** Khi bật, phí lắp đặt một lần được cộng vào dòng kỳ thu tiền đầu tiên thay vì tách dòng riêng — gọn hóa đơn kỳ đầu.

**Q: Bảng ánh xạ chi nhánh — trung tâm chi phí dùng khi nào?**
**A:** Khi hóa đơn hợp đồng phát sinh theo chi nhánh, hệ thống tra bảng này để gắn đúng trung tâm chi phí, phục vụ báo cáo lãi/lỗ theo chi nhánh.
