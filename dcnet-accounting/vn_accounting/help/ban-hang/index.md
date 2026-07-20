---
section: Bán hàng
title: Tổng quan Bán hàng
summary: Giới thiệu phân hệ Bán hàng — từ báo giá, đơn bán hàng, hóa đơn, xuất kho tới công nợ phải thu và doanh thu chưa thực hiện.
---

## Mục đích

Phân hệ **Bán hàng** quản lý toàn bộ chu trình bán hàng theo VAS: từ **báo giá** gửi khách → **đơn bán hàng** xác nhận → **xuất kho** giao hàng → **hóa đơn bán hàng** ghi nhận doanh thu và thuế GTGT đầu ra → **thu tiền** và theo dõi **công nợ phải thu** (TK 131). Phân hệ cũng xử lý các nghiệp vụ đặc thù: **điều khoản thanh toán** (chia kỳ thanh toán), **doanh thu chưa thực hiện** (TK 3387 — dịch vụ trả trước nhiều kỳ), và **bút toán chung** cho các điều chỉnh bán hàng.

## Khi nào dùng

- Trước khi bán: lập **báo giá** gửi khách, theo dõi báo giá đã/chưa chốt.
- Khi khách đồng ý: tạo **đơn bán hàng**, gắn **điều khoản thanh toán** nếu chia nhiều kỳ.
- Khi giao hàng hóa: lập **phiếu xuất kho** để ghi giảm tồn kho và giá vốn.
- Khi phát hành hóa đơn: lập **hóa đơn bán hàng** — ghi nhận doanh thu (TK 511), thuế GTGT đầu ra (TK 3331) và công nợ phải thu (TK 131).
- Dịch vụ trả trước nhiều kỳ (cước Internet, hosting, giấy phép phần mềm): tạo **lịch doanh thu chưa thực hiện** (TK 3387) để phân bổ doanh thu dần sang TK 511.
- Định kỳ: theo dõi **công nợ phải thu**, **bảng tổng hợp công nợ khách hàng** và **báo cáo bán hàng** để chốt doanh số, tuổi nợ.

## Cách thực hiện

Cấu trúc menu **Bán hàng** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Báo giá | Danh sách | Lập và theo dõi báo giá gửi khách hàng |
| 2 | Đơn bán hàng | Danh sách | Đơn bán hàng đã xác nhận với khách |
| 3 | Đơn bán hàng cần xuất hóa đơn | Danh sách lọc | Đơn đã giao nhưng chưa lập hóa đơn (lọc "cần xuất HĐ") |
| 4 | Hóa đơn bán hàng | Danh sách | Hóa đơn ghi nhận doanh thu + thuế GTGT đầu ra |
| 5 | Doanh thu chưa thực hiện (3387) | Danh sách | Lịch phân bổ doanh thu trả trước nhiều kỳ |
| 6 | Điều khoản thanh toán | Danh sách | Mẫu chia kỳ thanh toán (đặt cọc, trả góp...) |
| 7 | Công nợ phải thu | Báo cáo | Chi tiết công nợ TK 131 theo từng hóa đơn, tuổi nợ |
| 8 | Bảng tổng hợp công nợ KH | Báo cáo | Tổng hợp công nợ theo từng khách hàng |
| 9 | BC bán hàng | Báo cáo | Phân tích doanh số theo khách/mặt hàng/kỳ |
| 10 | Phiếu xuất kho | Danh sách | Giao hàng, ghi giảm tồn kho và giá vốn |
| 11 | Bút toán chung | Danh sách | Phiếu kế toán điều chỉnh/ghi nhận bán hàng |

### Quy trình điển hình

1. **Lập báo giá:** mở **Báo giá** → "+ Thêm" → nhập khách hàng, mặt hàng, đơn giá (đã gồm VAT theo thông lệ báo giá VN) → gửi khách.
2. **Chốt đơn:** từ báo giá đã chấp nhận → "Tạo > Đơn bán hàng"; chọn **điều khoản thanh toán** nếu chia kỳ.
3. **Giao hàng (hàng hóa):** từ đơn bán hàng → "Tạo > Phiếu xuất kho" → ghi sổ để giảm tồn kho (Nợ 632 / Có 156).
4. **Phát hành hóa đơn:** từ đơn bán hàng hoặc phiếu xuất kho → "Tạo > Hóa đơn bán hàng" → ghi sổ (Nợ 131 / Có 511 + Có 3331).
5. **Dịch vụ trả trước:** trên hóa đơn đã ghi sổ → "Hành động > + Lịch ghi nhận DT chưa thực hiện" → phân bổ dần Nợ 3387 / Có 511.
6. **Thu tiền:** từ hóa đơn bán hàng → "Tạo > Phiếu thanh toán" (xem phân hệ Tiền mặt / Ngân hàng).
7. **Theo dõi định kỳ:** xem **Công nợ phải thu**, **Bảng tổng hợp công nợ KH**, **BC bán hàng**.

### Liên kết tới các bài hướng dẫn chi tiết

- **Trước bán hàng:** [Báo giá](bao-gia.md), [Đơn bán hàng](don-ban-hang.md), [Điều khoản thanh toán](dieu-khoan-thanh-toan.md)
- **Ghi nhận doanh thu:** [Hóa đơn bán hàng](hoa-don-ban-hang.md), [Doanh thu chưa thực hiện (3387)](doanh-thu-chua-thuc-hien.md)
- **Kho và bút toán:** [Phiếu xuất kho](phieu-xuat-kho.md), [Bút toán chung](but-toan-chung.md)
- **Báo cáo:** [Công nợ phải thu](cong-no-phai-thu.md), [Bảng tổng hợp công nợ KH](tong-hop-cong-no-kh.md), [BC bán hàng](bc-ban-hang.md)

## Định khoản tự động

Các bút toán bán hàng phổ biến theo VAS (TT99/2025):

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Phát hành hóa đơn bán hàng | 131 | 511 | Doanh thu chưa thuế |
| — phần thuế GTGT đầu ra | 131 | 3331 | Thuế GTGT phải nộp |
| Xuất kho giao hàng (hàng hóa) | 632 | 156 | Ghi giá vốn theo phương pháp xuất kho |
| Khách trả trước dịch vụ nhiều kỳ | 131 / 112 | 3387 | Doanh thu chưa thực hiện |
| Kết chuyển doanh thu chưa thực hiện từng kỳ | 3387 | 511 | Phân bổ dần theo lịch |
| Khách thanh toán | 111 / 112 | 131 | Qua phiếu thanh toán |

> **Báo giá** và **đơn bán hàng** KHÔNG tạo bút toán Sổ Cái — đó là chứng từ cam kết, chưa phát sinh kế toán. Bút toán chỉ phát sinh khi lập **phiếu xuất kho** (giá vốn) và **hóa đơn bán hàng** (doanh thu).

## Tình huống đặc biệt & cảnh báo

- **Báo giá đơn giá đã gồm VAT:** thông lệ báo giá VN thường niêm yết đơn giá đã bao gồm thuế GTGT 10%. Khi nhập, để hệ thống tính ngược phần chưa thuế (đánh dấu dòng thuế "đã gồm trong giá") để tránh sai lệch làm tròn qua nhiều dòng.
- **Doanh thu chưa thực hiện (TK 3387):** chỉ áp dụng cho dịch vụ/hàng hóa khách trả trước cho NHIỀU kỳ tương lai (cước thuê bao, hosting, bảo trì cả năm). Không dùng cho bán hàng giao ngay.
- **Công trình xây lắp:** trên **phiếu xuất kho** có thể chọn **Loại chi phí** (Trực tiếp / Phân bổ) và **TK tập hợp chi phí công trình** (mặc định TK 154) — hệ thống tự tạo bút toán bù sau khi ghi sổ để tập hợp chi phí theo công trình.
- **Tách bút toán đặt cọc:** khách đặt cọc trước khi có hóa đơn → thu vào TK 131 (ứng trước), khi có hóa đơn sẽ tự phân bổ lại.
- **Tuổi nợ:** báo cáo công nợ tính tuổi nợ theo các mốc 30/60/90/120 ngày để cảnh báo nợ quá hạn.

## Báo cáo liên quan

- **Công nợ phải thu:** chi tiết từng hóa đơn còn nợ, tuổi nợ theo khách.
- **Bảng tổng hợp công nợ KH:** số dư công nợ gộp theo từng khách hàng.
- **BC bán hàng:** phân tích doanh số theo khách hàng / mặt hàng / nhóm hàng và theo kỳ.
- **Sổ Cái** (phân hệ Tổng hợp): chi tiết phát sinh TK 131, 511, 3331, 3387, 632.

## FAQ

**Q: Khác nhau giữa báo giá, đơn bán hàng và hóa đơn bán hàng?**
**A:** Báo giá = chào giá (chưa cam kết, chưa kế toán). Đơn bán hàng = khách đã xác nhận mua (cam kết, chưa kế toán). Hóa đơn bán hàng = phát hành hóa đơn, ghi nhận doanh thu và thuế — đây mới phát sinh bút toán Sổ Cái.

**Q: Khi nào dùng "Đơn bán hàng cần xuất hóa đơn"?**
**A:** Đây chỉ là danh sách đơn bán hàng được lọc theo trạng thái "đã giao nhưng chưa lập hóa đơn" — giúp kế toán không bỏ sót việc xuất hóa đơn. Xem [Đơn bán hàng](don-ban-hang.md).

**Q: Doanh thu nhận trước cả năm phải ghi nhận thế nào?**
**A:** Ghi vào TK 3387 "Doanh thu chưa thực hiện" rồi phân bổ dần sang TK 511 từng tháng/quý qua lịch ghi nhận. Xem [Doanh thu chưa thực hiện (3387)](doanh-thu-chua-thuc-hien.md).
