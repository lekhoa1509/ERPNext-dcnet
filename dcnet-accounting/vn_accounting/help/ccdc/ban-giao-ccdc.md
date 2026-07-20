---
title: Bàn giao CCDC
order: 4
summary: Điều chuyển công cụ dụng cụ giữa người giữ / phòng ban / kho — dùng chung biểu mẫu với TSCĐ, chọn phạm vi CCDC.
---

## Mục đích

**Bàn giao CCDC** ghi nhận việc **điều chuyển công cụ dụng cụ** từ người giữ này sang người giữ khác, hoặc giữa các phòng ban / kho. Biểu mẫu này **dùng chung với phân hệ TSCĐ** — phân biệt bằng trường **Phạm vi (Scope)**: chọn **CCDC** để bàn giao công cụ dụng cụ. Khi duyệt, hệ thống cập nhật người giữ và kho mới cho từng công cụ trong phiếu.

## Khi nào dùng

- Nhân viên nghỉ việc / chuyển bộ phận, cần bàn giao công cụ đang giữ cho người khác.
- Điều chuyển công cụ giữa các kho / địa điểm.
- Lập biên bản bàn giao có người ký duyệt cho lô công cụ giá trị lớn.

## Cách thực hiện

1. Bấm **Bàn giao CCDC** trên menu CCDC → **+ Thêm**.
2. Chọn **Phạm vi = CCDC** (bắt buộc, để chỉ thao tác trên công cụ dụng cụ).
3. Khai báo:
   - **Công ty**, **Ngày bàn giao**.
   - **Từ nhân viên / Từ phòng ban** → **Đến nhân viên / Đến phòng ban / Đến kho**.
   - **Người ký duyệt (Co-Signer)** — bắt buộc khi tổng giá trị vượt ngưỡng cấu hình.
   - **Lý do** (Chuyển bộ phận / Nghỉ việc / Điều chuyển kho / Khác).
4. Thêm các dòng công cụ vào bảng **Danh sách bàn giao** (Handover Items) — mỗi dòng trỏ tới một công cụ dụng cụ.
5. Bấm **Lưu** rồi **Duyệt (Submit)** → hệ thống lưu ảnh chụp trạng thái trước, rồi cập nhật người giữ + kho mới cho từng công cụ.

   ![Bàn giao CCDC](_images/ban-giao-ccdc-1.png)

## Định khoản tự động

Bàn giao CCDC **không tự sinh bút toán** — đây là nghiệp vụ quản lý hiện vật (đổi người giữ / kho), không thay đổi giá trị sổ sách. Hệ thống chỉ cập nhật trường Người giữ và Kho/Địa điểm trên từng công cụ.

> Lưu ý: với phạm vi **TSCĐ**, biểu mẫu này còn tạo thêm chứng từ điều chuyển tài sản (Asset Movement). Với phạm vi **CCDC** thì không — chỉ cập nhật người giữ và kho.

## Tình huống đặc biệt & cảnh báo

- **Chọn đúng phạm vi:** phải đặt Phạm vi = CCDC; nếu để dòng trỏ tới tài sản (TSCĐ) trong khi phạm vi là CCDC, hệ thống báo lỗi không khớp.
- **Ngưỡng ký duyệt:** nếu bật kiểm soát ngưỡng trong cài đặt và tổng giá trị ≥ ngưỡng (mặc định 100.000.000), bắt buộc có **Người ký duyệt** mới duyệt được phiếu.
- **Hủy phiếu (Cancel):** hệ thống khôi phục người giữ + kho cũ theo ảnh chụp trạng thái trước khi bàn giao.
- **Ảnh chụp trước bàn giao:** lưu lại để hoàn tác chính xác khi hủy — không chỉnh tay trường này.

## Báo cáo liên quan

- [Danh sách CCDC](danh-sach-ccdc.md): xem người giữ / kho hiện tại của từng công cụ.
- [Kiểm kê CCDC](kiem-ke-ccdc.md): kiểm kê thực tế sau bàn giao.
- [Sổ S22-DN](so-s22-dn.md): theo dõi vị trí và người giữ.

## FAQ

**Q: Bàn giao CCDC có làm thay đổi số dư kế toán không?**
**A:** Không. Đây là nghiệp vụ quản lý hiện vật, chỉ đổi người giữ và kho; không sinh bút toán.

**Q: Tại sao biểu mẫu giống hệt bàn giao TSCĐ?**
**A:** Vì dùng chung một biểu mẫu cho cả hai phân hệ. Trường **Phạm vi** quyết định thao tác trên tài sản (TSCĐ) hay công cụ dụng cụ (CCDC).

**Q: Khi nào cần người ký duyệt?**
**A:** Khi cài đặt bật kiểm soát ngưỡng và tổng giá trị bàn giao đạt/vượt ngưỡng cấu hình.

**Q: Hủy phiếu bàn giao có trả lại người giữ cũ không?**
**A:** Có. Hệ thống lưu ảnh chụp trạng thái trước và khôi phục người giữ + kho cũ khi hủy.
