---
title: Số seri
order: 6
summary: Quản lý hàng tồn kho theo từng số seri riêng lẻ để theo dõi bảo hành và truy vết từng đơn vị.
---

## Mục đích

**Số seri** dùng để theo dõi từng đơn vị hàng hóa riêng lẻ qua một mã seri duy nhất — phục vụ **bảo hành**, truy vết từng chiếc, biết mỗi seri đang ở kho nào hoặc đã giao cho khách nào. Phù hợp với thiết bị giá trị cao, hàng có bảo hành (modem, router, máy móc, thiết bị điện tử).

Mỗi số seri ghi nhận: **mặt hàng**, **kho hiện tại**, **trạng thái**, **hạn bảo hành**, chứng từ mua, và lô (nếu có).

## Khi nào dùng

- Quản lý hàng bảo hành: tra cứu seri để biết hạn bảo hành, ngày bán.
- Truy vết từng đơn vị: seri này đang ở kho nào, đã giao cho ai.
- Hàng giá trị cao cần kiểm soát chặt từng chiếc.
- Xử lý đổi/trả/bảo hành: xác định đúng chiếc hàng theo seri.

## Cách thực hiện

1. Bật theo dõi seri trên **mặt hàng** (trong Danh mục): tích "Có số seri" và đặt quy tắc tạo mã seri.
2. Khi **nhập kho**, hệ thống tạo các số seri tương ứng số lượng nhập; khai **hạn bảo hành** nếu có.
3. Mở mục **Số seri** trên menu Kho để xem danh sách seri.
   ![Danh sách số seri](_images/so-seri-1.png)
4. Mỗi seri hiển thị **trạng thái**:
   - **Đang hoạt động (Active):** còn trong kho, sẵn sàng xuất.
   - **Đã giao (Delivered):** đã xuất bán/giao cho khách.
   - **Tiêu hao (Consumed):** đã dùng vào sản xuất.
   - **Hết hạn (Expired):** quá hạn theo dõi.
   - **Ngừng (Inactive):** tạm ngưng sử dụng.
5. Khi **xuất kho**, chọn đúng số seri cần xuất.

## Định khoản tự động

**Không tự định khoản** — số seri chỉ theo dõi từng đơn vị hàng (số lượng = 1) và trạng thái. Bút toán giá trị do phiếu nhập/xuất kho hoặc hóa đơn sinh ra; seri được gắn vào dòng chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Một seri – một đơn vị:** mỗi seri đại diện đúng một chiếc; số lượng dòng hàng theo seri phải khớp số seri khai.
- **Seri đã giao:** không thể xuất lại seri đã ở trạng thái "Đã giao" trừ khi có hàng trả về (chuyển seri về kho).
- **Hàng trả về:** khi nhận lại hàng bảo hành/đổi trả, seri chuyển về trạng thái phù hợp và quay lại kho.
- **Hạn bảo hành:** theo dõi để cảnh báo khi hết hạn; thông tin này dùng khi tiếp nhận bảo hành.
- **Vừa lô vừa seri:** mặt hàng có thể bật cả hai — mỗi seri có thể thuộc một lô.
- **Hủy phiếu sinh seri:** nếu seri đã được giao/tiêu thụ, hủy phiếu nhập tạo seri có thể bị chặn.

## Báo cáo liên quan

- **Sổ chi tiết kho:** truy vết lịch sử di chuyển của hàng theo seri.
- **Nhập xuất kho:** chứng từ gắn seri vào dòng hàng.
- **Số lô:** dùng kèm khi hàng vừa theo lô vừa theo seri.

## FAQ

**Q: Có bắt buộc khai số seri không?**
**A:** Chỉ khi mặt hàng được bật theo dõi seri. Khi đó mỗi phiếu nhập/xuất phải khai số seri tương ứng từng đơn vị.

**Q: Trạng thái seri có những giá trị nào?**
**A:** Đang hoạt động (còn kho), Đã giao (đã bán), Tiêu hao (dùng sản xuất), Hết hạn, Ngừng.

**Q: Khách trả lại hàng theo seri thì xử lý thế nào?**
**A:** Lập phiếu/hóa đơn trả hàng cho đúng số seri → seri chuyển về kho và trạng thái phù hợp, sẵn sàng cho lần xuất sau.

**Q: Seri khác lô thế nào?**
**A:** Seri quản lý từng đơn vị riêng lẻ (một seri = một chiếc), thường cho bảo hành. Lô quản lý theo nhóm/đợt số lượng, thường gắn hạn dùng.
