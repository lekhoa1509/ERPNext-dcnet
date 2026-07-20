---
title: Mẫu hợp đồng
order: 13
summary: Tạo và quản lý mẫu hợp đồng/phụ lục (tải lên .docx, sinh biến điền tự động, duyệt phiên bản) để soạn hợp đồng nhanh và nhất quán.
---

## Mục đích

**Mẫu hợp đồng** quản lý các mẫu văn bản hợp đồng và phụ lục theo loại dịch vụ. Người dùng tải file mẫu `.docx`, hệ thống chuyển thành HTML, tự **dò các biến điền** dạng `{{...}}` (tên khách hàng, giá trị hợp đồng, thời hạn...) và quản lý theo **phiên bản + trạng thái duyệt** (Nháp → Chờ duyệt → Đã duyệt → Lưu trữ). Hợp đồng thực tế tạo từ mẫu đã duyệt, các biến được điền tự động từ dữ liệu.

## Khi nào dùng

- **Khi chuẩn hóa biểu mẫu hợp đồng:** mỗi loại dịch vụ (P2P, MPLS, ILL, FTTH DN, IT Managed, VTTB, Thi công) một mẫu chuẩn.
- **Khi cập nhật điều khoản hợp đồng:** tải file .docx mới → tạo phiên bản mới → duyệt.
- **Khi cần phụ lục:** tạo mẫu loại "Phụ lục".

## Cách thực hiện

1. Mở **Mẫu hợp đồng** trên menu Thiết lập.
2. Bấm **+ Thêm**:
   - **Tên mẫu**, **Loại mẫu** (Hợp đồng / Phụ lục), **Loại dịch vụ**, **Loại hợp đồng** (Recurring / One-off), **Hình thức thanh toán** (Prepay / Monthly / OneOff), **Thời hạn (tháng)**.
   - **Tải lên File mẫu .docx:** hệ thống tự chuyển sang HTML và **dò các biến** `{{...}}` vào bảng "Biến trong mẫu".
3. Kiểm tra bảng biến + hướng dẫn biến (placeholder guide) hệ thống sinh ra; bổ sung điều khoản mặc định nếu cần.
4. Chuyển **trạng thái** theo quy trình: Nháp → Chờ duyệt → Đã duyệt. Chỉ mẫu **Đã duyệt** mới nên dùng để soạn hợp đồng.

## Định khoản tự động

Mẫu hợp đồng **không sinh bút toán** — chỉ là biểu mẫu văn bản. Bút toán doanh thu phát sinh từ hóa đơn của hợp đồng (theo TK doanh thu khai ở [Cài đặt Hợp đồng](cai-dat-hop-dong.md)).

## Tình huống đặc biệt & cảnh báo

- **Đặt biến đúng cú pháp `{{ten_bien}}`** trong file .docx để hệ thống dò được. Biến lạ/không có trong danh mục biến sẽ được cảnh báo khi duyệt.
- **Mỗi lần đổi file .docx, hệ thống dò lại biến + có thể đánh dấu biến bị xóa** so với phiên bản trước — kiểm tra để không mất biến quan trọng.
- **Tuân thủ quy trình trạng thái:** chỉ chuyển tiến theo thứ tự Nháp → Chờ duyệt → Đã duyệt → Lưu trữ; hệ thống chặn chuyển trạng thái không hợp lệ.
- **Chỉ dùng mẫu Đã duyệt để soạn hợp đồng thật** — mẫu Nháp dễ còn thiếu biến/điều khoản.

## Báo cáo liên quan

- [Cài đặt Hợp đồng](cai-dat-hop-dong.md) — cấu hình mặc định cho hợp đồng tạo từ mẫu.
- Phân hệ **Hợp đồng & PAKD** — tạo hợp đồng từ mẫu, lịch thu tiền, xuất hóa đơn.

## FAQ

**Q: Tải .docx lên nhưng không thấy biến nào trong bảng?**
**A:** Biến phải viết đúng cú pháp `{{ten_bien}}` trong file Word. Kiểm tra lại file, tải lại; hệ thống dò biến mỗi lần đổi file.

**Q: Sửa điều khoản trong mẫu đã duyệt thì sao?**
**A:** Nên tải file .docx mới → tạo phiên bản mới → duyệt lại, thay vì sửa trực tiếp mẫu đã duyệt, để giữ vết phiên bản và không ảnh hưởng hợp đồng đã ký theo mẫu cũ.

**Q: Hợp đồng tạo từ mẫu có tự điền số liệu không?**
**A:** Có. Khi soạn hợp đồng từ mẫu, các biến `{{...}}` được điền từ dữ liệu khách hàng/hợp đồng. Mẫu càng đủ biến, hợp đồng càng ít phải gõ tay.
