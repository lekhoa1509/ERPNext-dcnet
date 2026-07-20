---
title: Ghi giảm CCDC
order: 3
summary: Xử lý công cụ dụng cụ hỏng/mất/thanh lý — xóa số dư còn lại trên TK 242 vào chi phí, ghi nhận bồi thường nếu có.
---

## Mục đích

**Ghi giảm CCDC** xử lý khi công cụ dụng cụ **hỏng, mất, hoặc hết nhu cầu sử dụng**: đẩy phần giá trị **chưa phân bổ hết** còn nằm trên TK 242 vào chi phí, hủy các kỳ phân bổ còn lại, và ghi nhận khoản bồi thường nếu cá nhân/đơn vị phải đền. Sau khi ghi giảm, công cụ chuyển sang trạng thái **Đã ghi giảm**.

## Khi nào dùng

- Công cụ dụng cụ hỏng không sửa được, không còn giá trị sử dụng.
- Công cụ bị mất, cần xóa khỏi sổ và xử lý trách nhiệm bồi thường.
- Thanh lý công cụ trước khi phân bổ hết.

## Cách thực hiện

1. Bấm **Ghi giảm CCDC** trên menu CCDC → **+ Thêm**.
2. Chọn **Công cụ** (CCDC Item) cần ghi giảm. Hệ thống tự tính **số dư còn lại trên TK 242** (phần các kỳ phân bổ còn Pending; hoặc toàn bộ giá trị nếu công cụ còn ở trạng thái "Mới mua").
3. Nhập **Ngày ghi giảm** và **Số tiền bồi thường** (nếu có người/đơn vị đền).
4. Bảng **Hạch toán** tự điền các dòng định khoản theo số dư còn lại + bồi thường. Có thể chỉnh tay.
5. Bấm **Lưu** rồi **Duyệt (Submit)** → hệ thống ghi bút toán, hủy các kỳ phân bổ còn lại và đặt trạng thái công cụ thành **Đã ghi giảm**.

   ![Ghi giảm CCDC](_images/ghi-giam-ccdc-1.png)

## Định khoản tự động

Khi **Duyệt**, hệ thống ghi 1–2 bút toán tùy tình huống:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Xóa số dư còn lại TK 242 | 6423 | 242 | Phần chưa phân bổ hết đẩy vào chi phí công cụ dụng cụ |
| Có khoản bồi thường | 1388 | 711 | Phải thu bồi thường / thu nhập khác |

> Trường hợp còn số dư trên TK 153 (hiếm, do quy trình cũ) sẽ ghi Nợ 632 / Có 153. Trong quy trình chuẩn hiện tại, giá trị nằm hoàn toàn ở TK 242 nên chỉ phát sinh dòng 6423/242.

## Tình huống đặc biệt & cảnh báo

- **Không ghi giảm hai lần:** công cụ đã ở trạng thái "Đã ghi giảm" sẽ bị chặn khi cố tạo phiếu ghi giảm mới.
- **Hủy phân bổ còn lại:** khi duyệt phiếu ghi giảm, mọi kỳ phân bổ còn Pending của công cụ sẽ chuyển sang **Cancelled** và lịch phân bổ chuyển **Cancelled** — tránh phân bổ tiếp sau khi đã thanh lý.
- **Số dư 242 còn lại được tính tự động:** lấy tổng các kỳ phân bổ còn Pending; nếu công cụ còn "Mới mua" (chưa phân bổ kỳ nào) thì lấy toàn bộ giá trị.
- **Bồi thường:** chỉ ghi dòng 1388/711 khi nhập Số tiền bồi thường > 0. Số bồi thường độc lập với số dư 242 xóa đi.
- **Hủy phiếu ghi giảm (Cancel):** hệ thống tự hủy bút toán đã ghi. Lưu ý các kỳ phân bổ đã bị hủy không tự khôi phục — cần kiểm tra lại lịch nếu muốn dùng tiếp.

## Báo cáo liên quan

- [Danh sách CCDC](danh-sach-ccdc.md): trạng thái công cụ chuyển "Đã ghi giảm" sau khi ghi giảm.
- [Lịch phân bổ CCDC](lich-phan-bo-ccdc.md): các kỳ còn lại bị hủy khi ghi giảm.
- **Sổ Cái** TK 242, 6423, 1388, 711: kiểm tra bút toán ghi giảm và bồi thường.

## FAQ

**Q: Ghi giảm khi công cụ chưa phân bổ hết thì phần còn lại đi đâu?**
**A:** Toàn bộ số dư còn lại trên TK 242 được đẩy vào chi phí (Nợ 6423 / Có 242) ngay trong phiếu ghi giảm.

**Q: Có người làm mất công cụ và phải đền — ghi thế nào?**
**A:** Nhập Số tiền bồi thường > 0; hệ thống thêm dòng Nợ 1388 (phải thu bồi thường) / Có 711 (thu nhập khác).

**Q: Lỡ ghi giảm nhầm thì sao?**
**A:** Hủy (Cancel) phiếu ghi giảm để hủy bút toán; sau đó kiểm tra lại trạng thái công cụ và lịch phân bổ (các kỳ đã hủy không tự khôi phục).

**Q: Số dư còn lại trên TK 242 có tự tính không?**
**A:** Có. Khi chọn công cụ, hệ thống tự cộng các kỳ phân bổ còn Pending để ra số dư cần xóa.
