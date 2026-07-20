---
title: Bàn giao tài sản
order: 4
summary: Biên bản bàn giao tài sản giữa người giữ/bộ phận/địa điểm — cập nhật người giữ và tạo phiếu điều chuyển.
---

## Mục đích

**Bàn giao TSCĐ** lập biên bản chuyển giao tài sản giữa người giữ, bộ phận hoặc địa điểm. Khi ghi sổ, hệ thống cập nhật người giữ + địa điểm mới cho từng tài sản và tạo phiếu điều chuyển tài sản tương ứng. Đây là chứng từ theo dõi, **không sinh bút toán tài chính** (không làm thay đổi giá trị sổ sách của tài sản).

## Khi nào dùng

- Khi điều chuyển tài sản từ người này sang người khác (nhân viên nghỉ việc, đổi vị trí).
- Khi chuyển tài sản giữa các bộ phận/phòng ban.
- Khi di dời tài sản giữa các địa điểm/kho.
- Cần biên bản có chữ ký bàn giao (in mẫu S22-DN).

## Cách thực hiện

1. Bấm **Bàn giao TSCĐ** trên menu TSCĐ → danh sách biên bản (phạm vi TSCĐ) mở. Bấm "+ Thêm".
2. **Phạm vi** đã đặt sẵn = TSCĐ (mở từ menu TSCĐ). Chọn **Công ty**, **Ngày bàn giao**.
3. Khai báo bên giao (người/bộ phận) và bên nhận (**người nhận**, **bộ phận nhận**, **địa điểm nhận**).
4. Thêm các dòng tài sản vào bảng **Danh sách bàn giao**: chọn từng tài sản, hệ thống lấy tên và giá trị sổ sách.
5. Nếu tổng giá trị ≥ ngưỡng (mặc định 100 triệu), bắt buộc chọn **Người đồng ký**.
6. Chọn **Lý do** (chuyển bộ phận / nghỉ việc / điều chuyển kho / khác) và ghi chú nếu cần.
7. **Ghi sổ** biên bản → hệ thống: (a) lưu ảnh chụp người giữ/địa điểm cũ để có thể hoàn tác, (b) tạo phiếu điều chuyển tài sản, (c) cập nhật người giữ + địa điểm mới cho từng tài sản.
8. In biên bản theo mẫu S22-DN nếu cần chữ ký.

## Định khoản tự động

Bàn giao tài sản **không tự định khoản** — đây là chứng từ điều chuyển nội bộ (đổi người giữ/địa điểm), không làm thay đổi nguyên giá hay giá trị còn lại. Hệ thống chỉ tạo **phiếu điều chuyển tài sản** để ghi nhận lịch sử di chuyển, không tạo bút toán kế toán.

## Tình huống đặc biệt & cảnh báo

- **Phạm vi phải khớp loại chứng từ:** biên bản phạm vi TSCĐ chỉ nhận tài sản cố định; phạm vi CCDC chỉ nhận công cụ dụng cụ. Thêm nhầm loại sẽ bị chặn khi lưu.
- **Ngưỡng đồng ký:** tổng giá trị bàn giao ≥ ngưỡng (mặc định 100 triệu, cấu hình trong Cài đặt) bắt buộc có **Người đồng ký** mới ghi sổ được. Có thể tắt kiểm tra ngưỡng trong Cài đặt VN Accounting.
- **Hủy biên bản khôi phục trạng thái cũ:** khi hủy biên bản đã ghi sổ, hệ thống dùng ảnh chụp đã lưu để trả người giữ và địa điểm về như trước khi bàn giao.
- **Tạo phiếu điều chuyển trước, cập nhật sau:** với tài sản cố định, phiếu điều chuyển tài sản được tạo trước khi cập nhật người giữ/địa điểm (để địa điểm nguồn còn đúng).

## Báo cáo liên quan

- **Sổ S22-DN:** mẫu in biên bản bàn giao TSCĐ/CCDC.
- **Danh sách tài sản:** xem người giữ và địa điểm hiện tại sau bàn giao.
- **Kiểm kê tài sản:** đối chiếu người giữ/địa điểm thực tế khi kiểm kê.

## FAQ

**Q: Bàn giao có làm thay đổi giá trị tài sản trên sổ không?**
**A:** Không. Bàn giao chỉ đổi người giữ và địa điểm. Nguyên giá, hao mòn lũy kế và giá trị còn lại giữ nguyên. Không có bút toán tài chính nào được tạo.

**Q: Một biên bản bàn giao được nhiều tài sản không?**
**A:** Có. Thêm nhiều dòng vào bảng Danh sách bàn giao — tất cả cùng chuyển sang bên nhận trong một lần ghi sổ. Tổng giá trị các tài sản dùng để xét ngưỡng đồng ký.

**Q: Lỡ bàn giao sai người thì làm sao?**
**A:** Hủy biên bản — hệ thống tự khôi phục người giữ và địa điểm cũ từ ảnh chụp đã lưu, rồi lập biên bản mới đúng người nhận.

**Q: Vì sao menu Bàn giao TSCĐ và Bàn giao CCDC mở cùng một loại chứng từ?**
**A:** Hai chứng từ dùng chung biểu mẫu, phân biệt bằng trường Phạm vi. Mở từ menu TSCĐ thì phạm vi đặt sẵn = TSCĐ; mở từ menu CCDC thì phạm vi = CCDC.
