---
title: Hóa đơn bán hàng
order: 4
summary: Phát hành hóa đơn — ghi nhận doanh thu (511), thuế GTGT đầu ra (3331) và công nợ phải thu (131).
---

## Mục đích

**Hóa đơn bán hàng** là chứng từ phát hành hóa đơn cho khách — bước **ghi nhận doanh thu** chính thức. Khi ghi sổ, hệ thống tự tạo bút toán Sổ Cái: công nợ phải thu (TK 131), doanh thu (TK 511) và thuế GTGT đầu ra (TK 3331). Đây cũng là cơ sở để xuất **hóa đơn điện tử** và theo dõi **công nợ phải thu**.

## Khi nào dùng

- Giao hàng/cung cấp dịch vụ xong, cần phát hành hóa đơn ghi nhận doanh thu.
- Bán lẻ giao ngay: lập thẳng hóa đơn (không qua đơn bán hàng).
- Từ đơn bán hàng/phiếu xuất kho: "Tạo > Hóa đơn bán hàng" để kế thừa dữ liệu.
- Dịch vụ trả trước nhiều kỳ: lập hóa đơn rồi tạo **lịch doanh thu chưa thực hiện** (TK 3387).

## Cách thực hiện

1. Mở **Hóa đơn bán hàng** → "+ Thêm" (hoặc từ đơn bán hàng / phiếu xuất kho: "Tạo > Hóa đơn bán hàng").
2. Chọn **Khách hàng**, **ngày ghi sổ** (= ngày hóa đơn).
3. Kiểm tra các dòng mặt hàng + đơn giá + thuế GTGT (10% / 8% / 5% / 0% / không chịu thuế).
4. (Hàng hóa) Nếu chưa giao kho riêng, bật cập nhật tồn kho để hóa đơn đồng thời ghi giảm tồn (Nợ 632 / Có 156).
5. Lưu và ghi sổ → bút toán Sổ Cái sinh tự động.
6. Bước tiếp theo:
   - **"Tạo > Phiếu thanh toán"** để thu tiền (xem phân hệ Tiền mặt / Ngân hàng).
   - **"Hành động > + Lịch ghi nhận DT chưa thực hiện"** cho dịch vụ trả trước — xem [Doanh thu chưa thực hiện (3387)](doanh-thu-chua-thuc-hien.md).

## Định khoản tự động

Hóa đơn bán hàng ghi sổ tự sinh bút toán:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Doanh thu chưa thuế | 131 | 511 | Theo tổng tiền hàng |
| Thuế GTGT đầu ra | 131 | 3331 | Theo % thuế từng dòng |
| Giá vốn (nếu hóa đơn đồng thời xuất kho) | 632 | 156 | Theo phương pháp xuất kho |
| Hàng giảm giá / chiết khấu thương mại | 5211/5213 | 131 | Nếu áp dụng |

Khi thu tiền (qua phiếu thanh toán): Nợ 111/112 / Có 131.

## Tình huống đặc biệt & cảnh báo

- **Tách thuế GTGT theo từng mức:** một hóa đơn có thể gồm nhiều dòng với mức thuế khác nhau (10%, 8%, 0%); hệ thống tách đúng phần TK 3331 theo từng mức.
- **Doanh thu chưa thực hiện:** với dịch vụ khách trả trước nhiều kỳ, ban đầu vẫn lập hóa đơn nhưng phần doanh thu phân bổ dần qua TK 3387 — xem [Doanh thu chưa thực hiện (3387)](doanh-thu-chua-thuc-hien.md).
- **Công trình xây lắp:** trường **Giai đoạn công trình** trên hóa đơn cho phép gắn hóa đơn với một giai đoạn nghiệm thu — phục vụ tập hợp doanh thu/chi phí theo công trình.
- **Số chứng từ Misa:** trường **Số chứng từ Misa** lưu số chứng từ gốc khi chuyển dữ liệu từ phần mềm cũ — phục vụ đối chiếu, không ảnh hưởng kế toán.
- **Hủy hóa đơn đã thu tiền:** nếu đã có phiếu thanh toán gắn vào, hủy hóa đơn sẽ ảnh hưởng phiếu thanh toán — cân nhắc lập hóa đơn điều chỉnh thay vì hủy.
- **Hóa đơn điện tử:** sau khi ghi sổ, phát hành hóa đơn điện tử qua tích hợp riêng; mã cơ quan thuế cấp lưu kèm hóa đơn.

## Báo cáo liên quan

- [Công nợ phải thu](cong-no-phai-thu.md): chi tiết hóa đơn còn nợ, tuổi nợ.
- [Bảng tổng hợp công nợ KH](tong-hop-cong-no-kh.md): số dư công nợ theo khách.
- [BC bán hàng](bc-ban-hang.md): phân tích doanh số.
- [Phiếu xuất kho](phieu-xuat-kho.md): chứng từ giao hàng và giá vốn.

## FAQ

**Q: Hóa đơn bán hàng đã tự ghi giảm tồn kho chưa?**
**A:** Tùy. Nếu đã lập **phiếu xuất kho** riêng trước đó, hóa đơn chỉ ghi doanh thu. Nếu lập thẳng hóa đơn có bật cập nhật tồn, hóa đơn sẽ đồng thời ghi giá vốn (Nợ 632 / Có 156).

**Q: Khách trả trước cả năm dịch vụ — ghi doanh thu một lần hay phân bổ?**
**A:** Theo VAS, phân bổ dần. Lập hóa đơn rồi tạo lịch doanh thu chưa thực hiện (TK 3387) để kết chuyển sang TK 511 từng kỳ.

**Q: Hóa đơn 0% thuế (xuất khẩu) định khoản thế nào?**
**A:** Nợ 131 / Có 511; TK 3331 = 0. Lưu ý điều kiện hồ sơ xuất khẩu để được áp dụng thuế suất 0%.
