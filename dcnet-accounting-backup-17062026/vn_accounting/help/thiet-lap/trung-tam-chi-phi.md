---
title: Trung tâm chi phí
order: 6
summary: Khai báo chiều phân tích quản trị (bộ phận/chi nhánh) để phân bổ và theo dõi chi phí, doanh thu theo từng đơn vị.
---

## Mục đích

**Trung tâm chi phí** (TTCP) là chiều phân tích quản trị cho phép gắn mỗi bút toán chi phí/doanh thu vào một đơn vị (phòng ban, chi nhánh, bộ phận, mảng kinh doanh). Nhờ đó kế toán quản trị xem được lãi/lỗ, chi phí theo từng TTCP — bổ sung cho góc nhìn theo tài khoản.

TTCP tổ chức dạng cây cha-con (TTCP tổng → TTCP chi tiết), giống cây tài khoản.

## Khi nào dùng

- **Khi triển khai kế toán quản trị:** dựng cây TTCP theo cơ cấu tổ chức (chi nhánh, phòng ban).
- **Khi cần báo cáo lãi/lỗ theo bộ phận:** gắn TTCP vào chứng từ để chạy báo cáo phân tích.
- **Trong xây lắp:** kết hợp TTCP với Dự án để theo dõi chi phí gián tiếp (TK 627) trước khi phân bổ về công trình.

## Cách thực hiện

1. Mở **Trung tâm chi phí** trên menu.
2. Bấm vào TTCP nhóm → **Thêm trung tâm chi phí con** để tạo cấp dưới.
3. Khai:
   - **Tên trung tâm chi phí.**
   - **Là nhóm:** bật nếu là TTCP tổng (có con), tắt nếu là TTCP hạch toán trực tiếp.
   - **Công ty.**
   - **TTCP cha.**
4. Lưu. Trên các chứng từ (hóa đơn, phiếu kế toán, đề nghị thanh toán), chọn TTCP cho từng dòng để gắn chiều phân tích.

## Định khoản tự động

Danh mục này **không sinh bút toán** — chỉ cung cấp **chiều phân tích** gắn vào bút toán. Khi ghi sổ, mỗi dòng Sổ Cái mang theo TTCP đã chọn; báo cáo quản trị tổng hợp theo TTCP.

Trong nghiệp vụ **giá thành công trình (xây lắp)**, chi phí gián tiếp gom vào TK 627 thường gắn TTCP để theo dõi nguồn phát sinh, sau đó phân bổ về các công trình (TK 154) theo tỷ lệ — xem [Cài đặt kế toán](cai-dat-ke-toan.md) nhóm Giá thành công trình.

## Tình huống đặc biệt & cảnh báo

- **TTCP nhóm không gắn vào chứng từ.** Chỉ TTCP lá (là nhóm = tắt) mới chọn được khi hạch toán.
- **TTCP khác Dự án.** TTCP theo cơ cấu tổ chức (bộ phận/chi nhánh — lâu dài); Dự án theo công trình/hợp đồng (có thời hạn). Trong xây lắp có thể dùng cả hai: TTCP cho bộ phận thi công, Dự án cho từng công trình.
- **Không xóa TTCP đã phát sinh** — chỉ vô hiệu hóa.
- **Cây TTCP dùng cấu trúc cây có thứ tự (lft/rgt).** Tạo/sửa qua màn hình, tránh thao tác trực tiếp vào dữ liệu để không hỏng cấu trúc cây.

## Báo cáo liên quan

- [Dự án](du-an.md) — chiều phân tích theo công trình/hợp đồng.
- [Ngân sách](ngan-sach.md) — lập ngân sách theo TTCP và so sánh thực tế.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — chuỗi 627→154 cho giá thành công trình.

## FAQ

**Q: Khi nào dùng Trung tâm chi phí, khi nào dùng Dự án?**
**A:** TTCP cho đơn vị tổ chức cố định (phòng kinh doanh, chi nhánh Hà Nội). Dự án cho từng công trình/hợp đồng có vòng đời riêng. Xây lắp thường dùng cả hai song song.

**Q: Một dòng bút toán có gắn được cả TTCP lẫn Dự án không?**
**A:** Có. Mỗi dòng Sổ Cái có thể mang nhiều chiều phân tích cùng lúc (TTCP + Dự án), giúp báo cáo chéo.

**Q: Tôi đổi tên/cấu trúc cây TTCP, báo cáo cũ có sai không?**
**A:** Đổi tên không ảnh hưởng số liệu. Chuyển TTCP sang nhánh cha khác chỉ đổi cách tổng hợp, không đổi giá trị từng dòng đã ghi.
