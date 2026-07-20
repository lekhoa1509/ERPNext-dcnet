---
title: Báo giá
order: 1
summary: Lập báo giá gửi khách hàng — chưa phát sinh bút toán, là bước khởi đầu chu trình bán hàng.
---

## Mục đích

**Báo giá** là chứng từ chào giá gửi khách hàng trước khi chốt đơn. Báo giá liệt kê mặt hàng/dịch vụ, số lượng, đơn giá và thời hạn hiệu lực. Đây là bước đầu chu trình bán hàng — **chưa phát sinh bút toán kế toán** vì chưa có cam kết mua bán chính thức.

## Khi nào dùng

- Khách hàng hỏi giá, cần gửi bảng chào giá chính thức.
- Theo dõi các báo giá đang chờ khách phản hồi (đã gửi / đã chấp nhận / hết hạn / hủy).
- Cần chuyển báo giá đã chấp nhận thành đơn bán hàng mà không nhập lại dữ liệu.

## Cách thực hiện

1. Mở **Báo giá** → "+ Thêm".
2. Chọn **Khách hàng** (hoặc khách tiềm năng), nhập **ngày báo giá** và **hạn hiệu lực**.
3. Thêm các dòng mặt hàng: mặt hàng, số lượng, đơn giá.
   - Theo thông lệ báo giá VN, đơn giá thường niêm yết **đã gồm thuế GTGT 10%** — đánh dấu dòng thuế là "đã gồm trong giá" để hệ thống tính ngược phần chưa thuế.
4. Lưu và ghi sổ (gửi cho khách). In bản PDF gửi khách.
5. Khi khách đồng ý → từ báo giá bấm **"Tạo > Đơn bán hàng"** để chuyển tiếp.

## Định khoản tự động

**Không tự định khoản.** Báo giá là chứng từ cam kết chào giá, không phát sinh bút toán Sổ Cái. Kế toán chỉ phát sinh ở các bước sau (phiếu xuất kho, hóa đơn bán hàng).

## Tình huống đặc biệt & cảnh báo

- **Báo giá hết hạn:** quá hạn hiệu lực, trạng thái chuyển "Hết hạn" — nên lập báo giá mới thay vì sửa báo giá cũ.
- **Đơn giá đã gồm VAT:** nếu nhập sai (để đơn giá chưa thuế nhưng vẫn cộng thêm thuế), tổng tiền gửi khách sẽ lệch. Luôn thống nhất quy ước "đã gồm VAT" cho cả bảng.
- **Nhiều quy cách cùng một mặt hàng:** nếu cần liệt kê cùng một mã hàng trên nhiều dòng (nhiều quy cách), hệ thống cho phép — không bị chặn như trên đơn bán hàng.
- **Báo giá nhiều phương án:** lập các báo giá riêng cho từng phương án để khách dễ so sánh.

## Báo cáo liên quan

- [Đơn bán hàng](don-ban-hang.md): bước tiếp theo sau khi khách chấp nhận báo giá.
- [BC bán hàng](bc-ban-hang.md): có thể phân tích theo báo giá.

## FAQ

**Q: Báo giá có ghi nhận doanh thu không?**
**A:** Không. Báo giá chỉ là chào giá, chưa có cam kết. Doanh thu chỉ ghi nhận khi phát hành hóa đơn bán hàng.

**Q: Khách đồng ý qua điện thoại, có cần lập báo giá không?**
**A:** Không bắt buộc — có thể tạo thẳng đơn bán hàng. Báo giá hữu ích khi cần bản chào giá chính thức và theo dõi tỷ lệ chốt đơn.

**Q: Sửa giá sau khi đã gửi báo giá thì sao?**
**A:** Tạo báo giá mới (phiên bản cập nhật) để giữ lịch sử bản đã gửi, thay vì sửa đè bản cũ.
