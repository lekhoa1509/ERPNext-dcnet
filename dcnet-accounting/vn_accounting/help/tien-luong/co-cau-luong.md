---
title: Cơ cấu lương
order: 5
summary: Khuôn mẫu tập hợp các thành phần lương (thu nhập và khấu trừ) áp dụng cho một nhóm nhân viên.
---

## Mục đích

**Cơ cấu lương** là khuôn mẫu định nghĩa một bộ các **thành phần lương** — gồm các khoản thu nhập (lương cơ bản, phụ cấp, thưởng) và các khoản khấu trừ (bảo hiểm phần người lao động, thuế TNCN) — áp dụng chung cho một nhóm nhân viên. Sau khi dựng cơ cấu, kế toán/nhân sự gán cơ cấu cho từng nhân viên kèm mức lương gốc để dùng khi tính lương.

## Khi nào dùng

- Thiết lập ban đầu: dựng các cơ cấu lương theo nhóm (ví dụ: khối văn phòng, khối sản xuất, khối bán hàng).
- Khi chính sách lương thay đổi: tạo cơ cấu mới hoặc điều chỉnh thành phần.
- Trước khi gán cơ cấu cho nhân viên và chạy lương.

## Cách thực hiện

1. Bấm **Cơ cấu lương** → bấm **+ Thêm**.
2. Đặt **Tên**, chọn **Công ty**.
3. Thêm vào bảng **Thu nhập** các thành phần lương loại thu nhập (lương cơ bản, phụ cấp...); thêm vào bảng **Khấu trừ** các thành phần khấu trừ (bảo hiểm, thuế TNCN...).
4. Với mỗi dòng, đặt **công thức** hoặc **số tiền** (ví dụ phụ cấp = % của lương cơ bản).
5. Bấm **Lưu** → **Duyệt** để cơ cấu sẵn sàng gán cho nhân viên.

## Định khoản tự động

Cơ cấu lương **không tự định khoản** — chỉ là khuôn mẫu cấu hình. TK hạch toán nằm trên từng [Thành phần lương](thanh-phan-luong.md). Bút toán chỉ phát sinh khi chạy [Bảng lương](bang-luong.md).

## Tình huống đặc biệt & cảnh báo

- **TK hạch toán không khai ở cơ cấu** mà ở từng Thành phần lương — kiểm tra Thành phần lương đã khai đúng TK theo bộ phận (622/627/641/642) trước khi chạy lương.
- **Công thức phụ thuộc lẫn nhau:** thành phần này có thể tham chiếu thành phần khác (ví dụ thuế TNCN tính trên thu nhập chịu thuế) — đặt đúng thứ tự tính.
- **Một nhân viên một cơ cấu hiệu lực:** mỗi nhân viên nên có một Gán Cơ cấu lương hiệu lực tại một thời điểm; nhiều gán chồng kỳ sẽ gây nhầm khi tính lương.

## Báo cáo liên quan

- [Thành phần lương](thanh-phan-luong.md): các khoản cấu thành cơ cấu, nơi khai TK.
- [Gán Cơ cấu lương](gan-co-cau-luong.md): gán cơ cấu này cho từng nhân viên.
- [Bảng lương](bang-luong.md): dùng cơ cấu để tính lương.

## FAQ

**Q: Cơ cấu lương có khai tài khoản kế toán không?**
**A:** Không. TK khai ở từng Thành phần lương. Cơ cấu chỉ tập hợp các thành phần đó lại.

**Q: Một công ty có thể có nhiều cơ cấu lương không?**
**A:** Có. Thường dựng theo nhóm/bộ phận để phản ánh đúng chính sách lương và TK chi phí khác nhau.

**Q: Đổi công thức trong cơ cấu thì kỳ lương cũ có bị ảnh hưởng?**
**A:** Không. Phiếu lương đã duyệt giữ nguyên số liệu; thay đổi chỉ áp dụng cho các kỳ tính lương sau.
