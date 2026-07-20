---
title: Lương bổ sung
order: 8
summary: Ghi nhận các khoản thưởng, phụ cấp hoặc khấu trừ một lần ngoài cơ cấu lương, áp vào phiếu lương của kỳ.
---

## Mục đích

**Lương bổ sung** dùng để ghi nhận các khoản **một lần** không nằm trong cơ cấu lương cố định: thưởng dự án, thưởng lễ tết, phụ cấp đột xuất, hoặc khấu trừ một lần (phạt, thu hồi tạm ứng). Khoản này được tự động cộng/trừ vào phiếu lương của nhân viên trong kỳ tương ứng.

## Khi nào dùng

- Thưởng năng suất, thưởng dự án, thưởng lễ tết cho một hoặc nhiều nhân viên.
- Phụ cấp đột xuất phát sinh trong kỳ.
- Khấu trừ một lần: thu hồi tạm ứng, khoản phạt.
- Bất kỳ khoản nào không lặp lại đều đặn nên không đưa vào cơ cấu lương cố định.

## Cách thực hiện

1. Bấm **Lương bổ sung** → bấm **+ Thêm**.
2. Chọn **Nhân viên**, **Thành phần lương** (khoản thu nhập hoặc khấu trừ tương ứng), **Số tiền**.
3. Chọn **kỳ áp dụng** (ngày/tháng phát hành) để khoản này gắn vào phiếu lương đúng kỳ.
4. Đặt loại **Thu nhập** hoặc **Khấu trừ** theo bản chất khoản.
5. Bấm **Lưu** → **Duyệt**.

## Định khoản tự động

Lương bổ sung **không tự sinh bút toán riêng**. Khoản này được gộp vào [Phiếu lương](phieu-luong.md) của kỳ, và bút toán hạch toán được lập tổng hợp khi ghi sổ [Bảng lương](bang-luong.md):

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Thưởng/phụ cấp một lần (thu nhập) | 622 / 627 / 641 / 642 | 334 | Theo TK của thành phần lương đã chọn |
| Khấu trừ một lần (thu hồi tạm ứng) | 334 | 141 | Giảm phải trả người lao động, giảm tạm ứng |
| Khấu trừ phạt | 334 | 1388 / 711 | Theo chính sách doanh nghiệp |

## Tình huống đặc biệt & cảnh báo

- **Thưởng chịu thuế TNCN:** thưởng thường là thu nhập chịu thuế → làm tăng thuế TNCN khấu trừ của kỳ. Kiểm tra số thuế trên phiếu lương sau khi thêm thưởng.
- **Đúng kỳ áp dụng:** đặt sai kỳ → khoản rơi vào phiếu lương kỳ khác. Chọn kỳ trùng với kỳ Bảng lương sẽ chạy.
- **Khoản lặp lại nhiều kỳ:** nếu một khoản lặp đều đặn, nên đưa vào cơ cấu lương thay vì tạo lương bổ sung từng kỳ.
- **TK lấy từ Thành phần lương đã chọn** — đảm bảo thành phần đó khai đúng TK chi phí/đối ứng.

## Báo cáo liên quan

- [Phiếu lương](phieu-luong.md): nơi khoản bổ sung được cộng/trừ.
- [Thành phần lương](thanh-phan-luong.md): cung cấp TK hạch toán cho khoản bổ sung.
- [Bảng lương](bang-luong.md): lập bút toán tổng hợp gồm cả khoản bổ sung.

## FAQ

**Q: Lương bổ sung có tạo bút toán ngay không?**
**A:** Không. Nó được gộp vào phiếu lương của kỳ; bút toán lập tổng hợp khi ghi sổ Bảng lương.

**Q: Thưởng Tết khai ở Lương bổ sung hay cơ cấu lương?**
**A:** Khoản một lần như thưởng Tết nên khai ở Lương bổ sung. Cơ cấu lương dành cho khoản lặp đều đặn hằng kỳ.

**Q: Thu hồi tạm ứng qua lương làm thế nào?**
**A:** Tạo Lương bổ sung loại Khấu trừ với thành phần khấu trừ tạm ứng; bút toán giảm phải trả lương đối ứng TK 141 (Dr 334 / Cr 141).
