---
title: Số lô
order: 5
summary: Quản lý hàng tồn kho theo lô và hạn sử dụng để truy xuất nguồn gốc và kiểm soát hạn dùng.
---

## Mục đích

**Số lô** dùng để theo dõi hàng tồn kho theo từng lô sản xuất/nhập hàng — quản lý **hạn sử dụng**, **ngày sản xuất** và truy xuất nguồn gốc. Mỗi lô gắn với một mặt hàng và ghi nhận số lượng còn lại của lô đó. Phù hợp với hàng có hạn dùng (thực phẩm, dược, vật tư hóa chất) hoặc cần truy vết theo đợt nhập.

## Khi nào dùng

- Quản lý hàng có hạn sử dụng → kiểm soát hàng sắp/đã hết hạn.
- Truy xuất nguồn gốc: biết một số lượng hàng thuộc lô nào, nhập/xuất khi nào.
- Áp dụng nguyên tắc xuất hàng theo hạn dùng (lô hết hạn trước xuất trước).
- Tính giá vốn theo từng lô (khi bật tính giá theo lô).

## Cách thực hiện

1. Bật theo dõi lô trên **mặt hàng** (trong Danh mục): tích "Có lô" và đặt quy tắc đặt mã lô.
2. Khi **nhập kho** mặt hàng đó, hệ thống tạo/chọn **số lô**; khai **ngày sản xuất** và **hạn sử dụng** nếu có.
3. Mở mục **Số lô** trên menu Kho để xem danh sách lô.
   ![Danh sách số lô](_images/so-lo-1.png)
4. Mỗi lô hiển thị: **mã lô**, **mặt hàng**, **ngày sản xuất**, **hạn sử dụng**, **số lượng lô**, chứng từ nguồn.
5. Khi **xuất kho**, chọn lô cần xuất (ưu tiên lô hết hạn trước).

## Định khoản tự động

**Không tự định khoản** — số lô chỉ là thông tin theo dõi số lượng và truy xuất nguồn gốc. Bút toán giá trị do phiếu nhập/xuất kho (hoặc hóa đơn) sinh ra; số lô gắn vào dòng chứng từ để biết hàng thuộc lô nào.

## Tình huống đặc biệt & cảnh báo

- **Tính giá theo lô:** nếu bật "tính giá theo lô", mỗi lô giữ giá vốn riêng — xuất lô nào tính giá lô đó. Khi bật, một số phiếu nhập điều chỉnh có thể bị ràng buộc chặt hơn về tồn lô.
- **Lô quá hạn:** hệ thống có thể cảnh báo khi xuất lô đã quá hạn; không nên xuất bán lô hết hạn.
- **Tồn lô âm:** xuất quá số lượng còn của lô sẽ báo lỗi tồn lô âm, kể cả khi tổng tồn mặt hàng vẫn dương.
- **Lô đã hết số lượng:** có thể đánh dấu **vô hiệu hóa** lô để ẩn khỏi danh sách chọn khi nhập/xuất.
- **Hủy phiếu tạo lô:** phiếu đã tạo lô và lô đã được tiêu thụ thì việc hủy có thể bị chặn — cần xử lý theo thứ tự thời gian.

## Báo cáo liên quan

- **Sổ chi tiết kho:** lọc theo số lô để xem lịch sử nhập/xuất của lô.
- **BC tuổi kho:** đánh giá tuổi tồn theo lô.
- **Nhập xuất kho:** chứng từ gắn lô vào dòng hàng.
- **Số seri:** dùng kèm khi hàng vừa theo lô vừa theo seri.

## FAQ

**Q: Có bắt buộc khai số lô không?**
**A:** Chỉ bắt buộc khi mặt hàng được bật theo dõi lô. Khi đó mọi phiếu nhập/xuất mặt hàng này phải khai lô tương ứng.

**Q: Lô khác seri thế nào?**
**A:** Lô quản lý theo đợt/nhóm số lượng (nhiều đơn vị cùng một lô), thường gắn hạn dùng. Seri quản lý theo từng đơn vị riêng lẻ (mỗi seri một chiếc), thường cho bảo hành.

**Q: Làm sao xuất hàng hết hạn trước?**
**A:** Khi xuất, chọn lô có hạn sử dụng gần nhất trước. Hệ thống sắp xếp lô theo hạn dùng để hỗ trợ nguyên tắc này.

**Q: Lô hết hàng có cần xóa không?**
**A:** Không nên xóa (giữ lịch sử truy vết). Có thể vô hiệu hóa lô để ẩn khỏi danh sách chọn.
