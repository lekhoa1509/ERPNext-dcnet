---
title: Mở khoá kỳ kế toán đã đóng
order: 4
summary: Quy trình ngoại lệ mở lại kỳ đã khoá để điều chỉnh số liệu, kèm nhật ký kiểm toán bất biến.
---

## Mục đích

**Mở khoá kỳ kế toán** là thao tác ngoại lệ cho phép Kế toán trưởng mở lại một kỳ đã đóng để sửa/bổ sung chứng từ, sau đó khoá lại. Mọi lần mở khoá đều ghi vào nhật ký kiểm toán không thể xóa, bảo đảm minh bạch về việc ai điều chỉnh số liệu kỳ nào, vì lý do gì.

## Khi nào dùng

- Phát hiện lỗi sai trong kỳ đã khoá mà không thể điều chỉnh bằng bút toán kỳ sau.
- Hóa đơn chậm về từ nhà cung cấp sau khi đã khoá sổ tháng.
- Kiểm toán yêu cầu điều chỉnh số liệu kỳ đã đóng.
- Phát hiện chứng từ bị hạch toán nhầm kỳ.

> **Không nên mở khoá thường xuyên** — ảnh hưởng đến tính toàn vẹn và độ tin cậy của số liệu. Ưu tiên điều chỉnh bằng chứng từ ở kỳ tiếp theo.

## Cách thực hiện

1. Mở **Định nghĩa kỳ kế toán** → tìm kỳ cần mở khoá (lọc theo Công ty + khoảng ngày).
2. Trong bảng **Chứng từ đóng**, bỏ tick loại chứng từ cần mở (hoặc đặt kỳ về Vô hiệu hóa tạm thời) → Lưu. Kỳ trở lại trạng thái cho phép hạch toán.
3. *(Nếu là Phiếu khoá sổ cuối năm)*: mở Phiếu khoá sổ tương ứng → **Hủy** (Cancel) → hệ thống đảo bút toán kết chuyển.
4. Thực hiện điều chỉnh cần thiết (sửa chứng từ sai, tạo bút toán điều chỉnh, thêm/bớt chứng từ trong kỳ).
5. **Khoá lại ngay** sau khi hoàn tất — không để kỳ ở trạng thái mở quá lâu.

## Định khoản tự động

Việc mở khoá Kỳ kế toán KHÔNG sinh bút toán — chỉ gỡ rào chặn ngày. Riêng **Hủy Phiếu khoá sổ cuối năm** sẽ tự đảo (hoàn nhập) bút toán kết chuyển lợi nhuận mà phiếu đó đã tạo:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Hủy phiếu khoá sổ → đảo bút toán kết chuyển | (đảo ngược bút toán gốc) | (đảo ngược bút toán gốc) | Hệ thống tự sinh bút toán đảo |

## Tình huống đặc biệt & cảnh báo

- **Ai được phép:** chỉ Kế toán trưởng (hoặc vai trò miễn trừ trên Kỳ kế toán). Kế toán viên thường không mở khoá được.
- **Nhật ký kiểm toán bất biến:** mọi thao tác khoá/mở khoá ghi tự động thời điểm, người thực hiện, lý do — không thể xóa hoặc sửa, kể cả Quản trị hệ thống. Xem ở tab **Lịch sử** của chứng từ.
- **Lưu báo cáo trước khi mở khoá:** nếu kỳ đã nộp báo cáo thuế, lưu PDF báo cáo gốc trước, ghi rõ lý do điều chỉnh để đối chiếu về sau.
- **Thông báo toàn team:** trước khi mở khoá, báo cho các kế toán viên khác để tránh xung đột dữ liệu trong lúc kỳ đang mở.
- **Không mở khoá kỳ đã nộp thuế** nếu không có lệnh điều chỉnh chính thức từ cơ quan thuế.

## Báo cáo liên quan

- [Khoá sổ kỳ kế toán](khoa-so-ky.md): quy trình khoá sổ.
- [Định nghĩa kỳ kế toán](dinh-nghia-ky-ke-toan.md): nơi quản lý trạng thái khoá/mở từng loại chứng từ.
- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): nếu cần kết chuyển lại sau điều chỉnh.

## FAQ

**Q: Mở khoá kỳ có làm thay đổi số liệu không?**
**A:** Tự nó không thay đổi — chỉ gỡ rào để bạn được phép sửa. Số liệu thay đổi khi bạn thực hiện điều chỉnh sau đó.

**Q: Có nên mở khoá hay tạo bút toán điều chỉnh kỳ sau?**
**A:** Ưu tiên điều chỉnh ở kỳ sau (thường được kiểm toán chấp nhận hơn). Chỉ mở khoá khi điều chỉnh kỳ sau không phản ánh đúng bản chất.

**Q: Audit log có thể bị xóa để giấu việc mở khoá không?**
**A:** Không. Nhật ký khoá/mở khoá là bất biến trong hệ thống — không ai xóa hoặc sửa được, là bằng chứng quan trọng khi có tranh chấp số liệu.

**Q: Hủy phiếu khoá sổ cuối năm có ảnh hưởng bút toán không?**
**A:** Có. Hủy phiếu khoá sổ sẽ tự đảo bút toán kết chuyển lợi nhuận mà phiếu đã tạo, đưa số dư các tài khoản kết quả về trạng thái trước khi khoá.
