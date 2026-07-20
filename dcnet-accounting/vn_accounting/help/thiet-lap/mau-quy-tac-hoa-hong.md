---
title: Mẫu quy tắc hoa hồng
order: 11
summary: Định nghĩa bộ quy tắc tính hoa hồng PAKD theo phạm vi (chi nhánh, loại dịch vụ, loại PAKD, kênh) với các thành phần và tỷ lệ áp dụng.
---

## Mục đích

**Mẫu quy tắc hoa hồng** định nghĩa cách tính hoa hồng cho phương án kinh doanh (PAKD): gồm các **thành phần** (component) và tỷ lệ, áp dụng theo **phạm vi** — chi nhánh, loại dịch vụ, loại PAKD và kênh (nhân viên / ban lãnh đạo). PAKD khi tính hoa hồng sẽ chọn mẫu phù hợp phạm vi để áp tỷ lệ.

## Khi nào dùng

- **Khi triển khai chính sách hoa hồng:** dựng các mẫu theo từng nhóm dịch vụ/chi nhánh/kênh.
- **Khi chính sách thay đổi theo thời gian:** tạo mẫu mới với "Hiệu lực từ/đến" để áp dụng theo giai đoạn.
- **Khi cần chính sách riêng cho ban lãnh đạo so với nhân viên:** đặt kênh áp dụng tương ứng.

## Cách thực hiện

1. Mở **Mẫu quy tắc hoa hồng** trên menu.
2. Bấm **+ Thêm**:
   - **Tên mẫu.**
   - **Hiệu lực từ / Hiệu lực đến:** khoảng thời gian áp dụng.
   - **Phạm vi:** Chi nhánh, Loại dịch vụ (P2P, MPLS, ILL, FTTH DN, IT Managed, VTTB, Thi công), Loại PAKD (Recurring Telecom / One-off Sale-Project), Kênh áp dụng (Nhân viên / Ban lãnh đạo).
   - **Thành phần (bảng):** từng dòng là một thành phần hoa hồng với tỷ lệ/cách tính.
3. Lưu. Đặt một mẫu làm mặc định trong [Cài đặt PAKD](cai-dat-pakd.md) nếu muốn.

## Định khoản tự động

Mẫu này **không sinh bút toán** — nó chỉ cung cấp **tỷ lệ và thành phần** để PAKD tính ra số tiền hoa hồng. Bút toán hoa hồng do PAKD sinh, dùng TK khai ở [Cài đặt PAKD](cai-dat-pakd.md) (TK 6427 / 334 / 3388 / 3335 / 3338 tùy trường hợp).

## Tình huống đặc biệt & cảnh báo

- **Mẫu chọn theo phạm vi khớp nhất.** Nếu nhiều mẫu cùng phạm vi và cùng hiệu lực, PAKD có thể chọn nhầm — đặt phạm vi đủ rõ và không chồng lấn hiệu lực.
- **Kiểm tra "Hiệu lực từ/đến".** Mẫu hết hiệu lực sẽ không được PAKD chọn; tạo mẫu mới khi chính sách đổi thay vì sửa mẫu cũ (giữ vết lịch sử).
- **Phân biệt kênh Nhân viên vs Ban lãnh đạo** để áp đúng chính sách — kênh sai dẫn tới tính hoa hồng sai đối tượng.
- **Thành phần rỗng → hoa hồng = 0.** Đảm bảo bảng thành phần có đủ dòng với tỷ lệ trước khi dùng mẫu.

## Báo cáo liên quan

- [Cài đặt PAKD](cai-dat-pakd.md) — chọn mẫu mặc định + TK đăng hoa hồng.
- [Lịch sử nhắc duyệt PAKD](lich-su-nhac-duyet-pakd.md).

## FAQ

**Q: Chính sách hoa hồng đổi giữa năm, tôi nên sửa mẫu cũ hay tạo mẫu mới?**
**A:** Tạo mẫu mới với "Hiệu lực từ" là ngày áp dụng chính sách mới, và đặt "Hiệu lực đến" cho mẫu cũ. Cách này giữ đúng lịch sử và PAKD cũ vẫn tính theo mẫu cũ.

**Q: Một PAKD áp được nhiều mẫu không?**
**A:** PAKD chọn một mẫu khớp phạm vi (chi nhánh + loại dịch vụ + loại PAKD + kênh) và còn hiệu lực. Đặt phạm vi rõ để hệ thống chọn đúng.

**Q: "Loại PAKD" Recurring và One-off khác gì khi tính hoa hồng?**
**A:** Recurring (viễn thông thuê bao) tính theo kỳ; One-off (bán hàng/dự án) tính một lần. Mẫu áp đúng loại để công thức thành phần khớp bản chất doanh thu.
