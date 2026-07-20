---
title: Kiểm kê CCDC
order: 5
summary: Biên bản kiểm kê thực tế công cụ dụng cụ — tải danh sách theo kho, ghi nhận mất/hỏng, dùng chung biểu mẫu với TSCĐ.
---

## Mục đích

**Kiểm kê CCDC** lập biên bản kiểm kê thực tế công cụ dụng cụ, đối chiếu với sổ sách. Biểu mẫu **dùng chung với phân hệ TSCĐ** — phân biệt bằng trường **Phạm vi (Scope)**: chọn **CCDC** để kiểm kê công cụ dụng cụ. Hệ thống hỗ trợ **tải nhanh danh sách** công cụ theo kho/phòng ban, và khi duyệt sẽ **tự xử lý kế toán** cho các trường hợp mất/hỏng.

## Khi nào dùng

- Kiểm kê định kỳ (cuối kỳ kế toán, cuối năm) đối chiếu thực tế công cụ dụng cụ với sổ sách.
- Kiểm kê đột xuất khi bàn giao, đổi người quản lý kho.
- Phát hiện và xử lý công cụ bị mất / hỏng.

## Cách thực hiện

1. Bấm **Kiểm kê CCDC** trên menu CCDC → **+ Thêm**.
2. Chọn **Phạm vi = CCDC**, khai báo **Công ty**, **Ngày kiểm kê**, **Kho/Địa điểm**, **Phòng ban**.
3. Bấm nút **Tải danh sách** (Load Items) → hệ thống nạp các công cụ đã duyệt thuộc kho/phòng ban đã chọn vào bảng kiểm kê, kèm giá trị sổ sách.
4. Với mỗi dòng, ghi nhận **tình trạng thực tế** (Physical Status): bình thường / **Mất** / **Hỏng**.
5. Cập nhật trạng thái biên bản: Draft → In Progress → Completed → **Approved**.
6. Khi **Duyệt (Approve)**, hệ thống tự xử lý kế toán cho các dòng Mất/Hỏng (xem mục Định khoản).

   ![Kiểm kê CCDC](_images/kiem-ke-ccdc-1.png)

## Định khoản tự động

Khi **Duyệt (Approve)** biên bản, hệ thống xử lý từng dòng theo tình trạng thực tế:

| Tình trạng | Xử lý | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|---|
| Mất (công cụ dụng cụ) | Ghi bút toán | 1381 | 153 | Tài sản thiếu chờ xử lý / giá trị công cụ |
| Hỏng | Đổi trạng thái công cụ | — | — | Đặt công cụ thành "Out of Order", không sinh bút toán |
| Bình thường | Không xử lý | — | — | Chỉ ghi nhận kết quả kiểm kê |

> Với phạm vi TSCĐ, dòng "Mất" ghi Nợ 1381 / Có 211 (nguyên giá tài sản). Với phạm vi CCDC, ghi Nợ 1381 / Có 153.

## Tình huống đặc biệt & cảnh báo

- **Chọn phạm vi trước khi tải danh sách:** phải chọn Phạm vi = CCDC, nếu không hệ thống báo "Chọn phạm vi kiểm kê (TSCĐ / CCDC) trước".
- **Tải lại danh sách ghi đè:** mỗi lần bấm Tải danh sách sẽ xóa và nạp lại bảng theo bộ lọc kho/phòng ban hiện tại.
- **Khoản thiếu chờ xử lý (TK 1381):** giá trị công cụ mất ghi vào TK 1381 chờ quyết định xử lý (bồi thường / ghi vào chi phí). Bước xử lý tiếp theo thực hiện qua phiếu kế toán riêng.
- **Hỏng không sinh bút toán:** chỉ đánh dấu công cụ "Out of Order"; nếu cần xóa khỏi sổ, lập [Ghi giảm CCDC](ghi-giam-ccdc.md).
- **Nếu thiếu tài khoản:** khi không tìm thấy TK 1381 hoặc 153 của công ty, hệ thống ghi nhật ký lỗi và bỏ qua dòng đó — cần khai báo đủ tài khoản trước khi kiểm kê.

## Báo cáo liên quan

- [Ghi giảm CCDC](ghi-giam-ccdc.md): xóa công cụ mất/hỏng khỏi sổ.
- [Danh sách CCDC](danh-sach-ccdc.md): cập nhật trạng thái công cụ sau kiểm kê.
- [Sổ S22-DN](so-s22-dn.md): theo dõi tình trạng và vị trí.

## FAQ

**Q: Tải danh sách công cụ theo gì?**
**A:** Theo Phạm vi (CCDC) + Kho/Địa điểm đã chọn. Hệ thống nạp các công cụ đã duyệt thuộc kho đó.

**Q: Phát hiện mất công cụ — kế toán ghi thế nào?**
**A:** Đánh dấu dòng đó là "Mất", khi Duyệt biên bản hệ thống tự ghi Nợ 1381 (chờ xử lý) / Có 153.

**Q: Công cụ hỏng có tự xóa khỏi sổ không?**
**A:** Không. Hỏng chỉ đặt trạng thái "Out of Order". Muốn xóa khỏi sổ, lập phiếu Ghi giảm CCDC.

**Q: Biểu mẫu giống kiểm kê TSCĐ — có nhầm không?**
**A:** Dùng chung biểu mẫu; trường Phạm vi quyết định kiểm kê tài sản (TSCĐ) hay công cụ dụng cụ (CCDC).
