---
title: Sửa chữa tài sản
order: 3
summary: Phiếu sửa chữa TSCĐ với hạch toán nội bộ — phân loại chi phí, vốn hóa hay nâng cấp theo TT99/2025.
---

## Mục đích

**Sửa chữa** ghi nhận nghiệp vụ sửa chữa, bảo trì, nâng cấp tài sản kèm phần **hạch toán nội bộ ngay trên phiếu**. Tùy phân loại, chi phí sửa chữa được tính thẳng vào chi phí kỳ hoặc tập hợp để vốn hóa/tăng nguyên giá theo TT99/2025. Khi ghi sổ phiếu, hệ thống tự sinh một bút toán kế toán từ bảng hạch toán trên phiếu.

## Khi nào dùng

- Khi tài sản hỏng cần sửa chữa thường xuyên (tính thẳng chi phí).
- Khi thực hiện sửa chữa lớn cần tập hợp chi phí để vốn hóa.
- Khi nâng cấp/cải tạo tài sản làm tăng nguyên giá.
- Theo dõi thời gian ngừng hoạt động (downtime) của tài sản trong quá trình sửa.

## Cách thực hiện

1. Bấm **Sửa chữa** trên menu TSCĐ → danh sách phiếu sửa chữa mở. Bấm "+ Thêm".
2. Chọn **Tài sản**, nhập **Ngày hỏng**, **Ngày hoàn thành** (hệ thống tự tính số ngày ngừng hoạt động).
3. Chọn **Phân loại sửa chữa**:
   - **Chi phí** — sửa chữa thường xuyên, tính thẳng chi phí.
   - **Sửa chữa lớn vốn hóa** — tập hợp chi phí sửa chữa lớn.
   - **Nâng cấp cải tạo** — làm tăng nguyên giá tài sản.
4. Nhập **Chi phí sửa chữa**. Nếu có thuế GTGT, bật **Có VAT?** và nhập **Tỷ lệ VAT (%)** (mặc định 10%).
5. Bảng **Bút toán hạch toán** tự sinh các dòng Nợ/Có tương ứng với phân loại + dòng VAT (nếu có). Kiểm tra lại tài khoản và số tiền.
6. **Ghi sổ** phiếu → hệ thống tạo và ghi sổ một phiếu kế toán từ bảng hạch toán; số phiếu lưu ở trường "Phiếu kế toán".
7. Sau khi ghi sổ, bấm nút **Xem > Sổ Cái** để mở Sổ Cái lọc theo phiếu kế toán vừa tạo.

## Định khoản tự động

Hệ thống tự sinh bút toán theo phân loại (TT99/2025 §5.1):

| Phân loại | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Chi phí | 6427 | 111 | Sửa chữa thường xuyên, chi phí quản lý |
| Sửa chữa lớn vốn hóa | 2413 | 331 | Tập hợp chi phí sửa chữa lớn |
| Nâng cấp cải tạo | 2412 | 331 | Tăng nguyên giá tài sản |
| VAT đầu vào (khi bật "Có VAT?") | 1331 | (theo TK Có ở trên) | Thuế GTGT khấu trừ = chi phí × tỷ lệ |

> Tài khoản được tra theo số hiệu cho đúng công ty. Tổng bút toán phải khớp với chi phí sửa chữa + VAT, lệch quá 1 đồng hệ thống sẽ chặn ghi sổ.

## Tình huống đặc biệt & cảnh báo

- **Chi phí lớn nên cân nhắc vốn hóa:** nếu chọn phân loại "Chi phí" mà chi phí sửa chữa ≥ 10% nguyên giá tài sản, hệ thống cảnh báo gợi ý chuyển sang "Sửa chữa lớn vốn hóa" cho đúng bản chất.
- **Đổi phân loại = tạo lại bút toán:** khi đổi **Phân loại sửa chữa** lúc bảng hạch toán đã có dòng, hệ thống hỏi xác nhận trước khi xóa và tạo lại — vì đây là thay đổi cơ bản. Còn khi đổi chi phí/tỷ lệ VAT hoặc bật/tắt VAT thì bảng tự cập nhật ngay (không hỏi).
- **Khóa sau khi ghi sổ:** phiếu đã ghi sổ thì bảng hạch toán, cờ VAT và tỷ lệ VAT chuyển sang chỉ đọc.
- **Hủy phiếu:** hủy phiếu sửa chữa sẽ tự hủy phiếu kế toán liên quan.
- **Tài khoản phải tồn tại:** các TK 6427/2413/2412/331/111/1331 phải có trong hệ thống tài khoản của công ty; nếu thiếu sẽ báo lỗi khi tạo bút toán.

## Báo cáo liên quan

- **Sổ Cái:** xem bút toán sửa chữa qua nút "Xem > Sổ Cái" trên phiếu.
- **Sổ S21-DN:** sửa chữa lớn/nâng cấp làm tăng nguyên giá sẽ phản ánh ở giá trị tài sản.
- **Bút toán kế toán:** phiếu kế toán tự sinh từ phiếu sửa chữa.

## FAQ

**Q: Khác nhau giữa "Sửa chữa lớn vốn hóa" và "Nâng cấp cải tạo"?**
**A:** Sửa chữa lớn vốn hóa tập hợp chi phí vào TK 2413 (sửa chữa lớn TSCĐ); nâng cấp cải tạo vào TK 2412 (đầu tư nâng cấp), làm tăng nguyên giá tài sản. Chọn theo bản chất nghiệp vụ: khôi phục trạng thái ban đầu (sửa chữa) hay nâng cao công năng (nâng cấp).

**Q: Có thể sửa tài khoản trong bảng hạch toán không?**
**A:** Có, trước khi ghi sổ. Bảng sinh sẵn tài khoản mặc định theo phân loại, nhưng kế toán có thể đổi tài khoản Nợ/Có hoặc số tiền từng dòng cho phù hợp, miễn tổng vẫn khớp chi phí + VAT.

**Q: Tại sao đổi tỷ lệ VAT thì bảng tự cập nhật mà đổi phân loại lại hỏi xác nhận?**
**A:** Đổi tỷ lệ/chi phí/cờ VAT chỉ điều chỉnh số tiền nên cập nhật ngay để bảng luôn đúng. Đổi phân loại là thay đổi cơ bản (đổi cặp tài khoản) nên cần xác nhận để tránh xóa nhầm các dòng kế toán đã chỉnh.
