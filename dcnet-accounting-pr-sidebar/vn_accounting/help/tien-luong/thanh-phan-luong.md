---
title: Thành phần lương
order: 6
summary: Khai báo từng khoản lương (thu nhập hoặc khấu trừ) cùng tài khoản hạch toán và công thức tính.
---

## Mục đích

**Thành phần lương** là đơn vị nhỏ nhất cấu thành lương: mỗi thành phần là một khoản **thu nhập** (lương cơ bản, phụ cấp, thưởng) hoặc **khấu trừ** (bảo hiểm phần người lao động, thuế TNCN, tạm ứng). Đây là nơi khai **tài khoản hạch toán** của khoản đó — quyết định bút toán lương sẽ vào TK chi phí nào (622/627/641/642) và đối ứng với TK nào (334, 338x, 3335).

## Khi nào dùng

- Thiết lập ban đầu: khai báo toàn bộ các khoản lương và khấu trừ mà doanh nghiệp sử dụng.
- Khi thêm khoản phụ cấp/khấu trừ mới (ví dụ phụ cấp xăng xe, phụ cấp điện thoại).
- Khi cần sửa TK hạch toán hoặc công thức của một khoản.

## Cách thực hiện

1. Bấm **Thành phần lương** → bấm **+ Thêm**.
2. Đặt **Tên** (ví dụ "Lương cơ bản", "Phụ cấp ăn ca", "BHXH (người lao động)").
3. Chọn **Loại**: Thu nhập (Earning) hoặc Khấu trừ (Deduction).
4. Khai **Tài khoản** hạch toán theo công ty: với khoản thu nhập, đặt TK chi phí theo bộ phận sử dụng lao động (622 sản xuất / 627 phân xưởng / 641 bán hàng / 642 quản lý); với khoản khấu trừ, đặt TK đối ứng (3383/3384/3386/3335...).
5. Đặt **công thức** hoặc để tính theo số tiền nhập tay; bật/tắt **phụ thuộc số ngày công** tùy khoản.
6. Bấm **Lưu**.

## Định khoản tự động

Thành phần lương **không tự định khoản** — nhưng TK khai ở đây quyết định bút toán mà [Bảng lương](bang-luong.md) lập ra:

| Loại thành phần | Vai trò trong bút toán | TK thường dùng |
|---|---|---|
| Thu nhập (lương, phụ cấp) | Vế Nợ chi phí | 622 / 627 / 641 / 642 |
| Khấu trừ — bảo hiểm phần người lao động | Vế Có (đối ứng Dr 334) | 3383 / 3384 / 3386 |
| Khấu trừ — thuế TNCN | Vế Có (đối ứng Dr 334) | 3335 |
| Khoản trích phần doanh nghiệp chịu | Vế Có (đối ứng Dr 62x/64x) | 3383 / 3384 / 3386 / 3382 |

## Tình huống đặc biệt & cảnh báo

- **Khai sai TK = bút toán lương sai khoản chi phí.** Đây là điểm dễ sai nhất: phụ cấp của nhân viên bán hàng phải vào 641, không vào 642.
- **Phân biệt phần doanh nghiệp và người lao động:** tạo thành phần riêng cho phần DN chịu (tính vào chi phí) và phần người lao động chịu (trừ vào lương) vì hai phần định khoản khác vế.
- **"Phụ thuộc số ngày công":** bật cho lương cơ bản/phụ cấp theo công; tắt cho khoản cố định không phụ thuộc ngày công. Lưu ý đặt thiết lập này trên cả thành phần lẫn cơ cấu cho nhất quán.
- **Công thức tham chiếu thành phần khác** cần đúng thứ tự (ví dụ thuế TNCN tính sau khi đã có thu nhập chịu thuế).

## Báo cáo liên quan

- [Cơ cấu lương](co-cau-luong.md): tập hợp các thành phần thành khuôn mẫu.
- [Bảng lương](bang-luong.md): dùng TK của thành phần để lập bút toán.

## FAQ

**Q: TK chi phí lương khai ở đâu?**
**A:** Ở chính Thành phần lương (mục Tài khoản theo công ty). Không khai ở Cơ cấu lương hay Bảng lương.

**Q: Một khoản phụ cấp dùng cho nhiều bộ phận khác nhau thì khai TK nào?**
**A:** Nếu bộ phận khác nhau cần TK chi phí khác nhau (641 vs 642), nên tạo thành phần riêng theo bộ phận hoặc cấu hình TK theo trung tâm chi phí để bút toán vào đúng khoản.

**Q: BHXH phần công ty và phần người lao động có phải hai thành phần riêng?**
**A:** Nên tách: phần công ty là khoản trích tính vào chi phí (Dr 62x/64x / Cr 3383); phần người lao động là khoản khấu trừ vào lương (Dr 334 / Cr 3383). Định khoản khác nhau nên để hai thành phần riêng cho rõ ràng.
