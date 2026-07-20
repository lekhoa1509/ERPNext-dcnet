---
title: Nhân viên
order: 6
summary: Danh mục hồ sơ nhân sự — dùng chung cho tạm ứng (TK 141) và tiền lương (TK 334).
---

## Mục đích

Danh mục **Nhân viên** lưu hồ sơ nhân sự của doanh nghiệp. Đây là **dữ liệu nền dùng chung**: cùng một hồ sơ nhân viên được tham chiếu khi theo dõi tạm ứng (TK 141 — tạm ứng cho nhân viên) và khi tính tiền lương (TK 334 — phải trả người lao động). Khai một lần, dùng cho cả hai nghiệp vụ.

Thông tin chính của một nhân viên:

- **Mã / Tên nhân viên**: định danh dùng trên phiếu tạm ứng, bảng lương.
- **Phòng ban / Chức danh**: phân loại tổ chức, phục vụ báo cáo.
- **Công ty / Ngày vào làm**: nhân viên thuộc công ty nào, thâm niên.
- **Thông tin cá nhân**: phục vụ tính thuế TNCN, bảo hiểm (nếu dùng phân hệ tiền lương).
- **Thông tin ngân hàng**: tài khoản nhận lương (nếu trả lương qua ngân hàng).

## Khi nào dùng

- **Khi có nhân viên mới:** tuyển dụng, cần theo dõi tạm ứng hoặc trả lương.
- **Khi lập phiếu tạm ứng / hoàn tạm ứng:** chọn nhân viên là đối tượng của TK 141.
- **Khi tính lương:** nhân viên là đối tượng của TK 334; hồ sơ cung cấp thông tin tính thuế, bảo hiểm.
- **Khi tra cứu công nợ nội bộ:** xem số tạm ứng còn lại theo từng người.

## Cách thực hiện

1. Mở **Nhân viên** trên menu Danh mục → danh sách nhân viên hiện ra.
2. Bấm **+ Thêm** → nhập **Tên nhân viên**, chọn **Công ty**, **Phòng ban**, **Chức danh**, **Ngày vào làm**.
3. (Tùy chọn) nhập thông tin cá nhân và tài khoản ngân hàng nếu dùng phân hệ tiền lương / trả lương qua ngân hàng.
4. Lưu lại → nhân viên sẵn sàng để chọn trên phiếu tạm ứng và bảng lương.

## Định khoản tự động

Danh mục nhân viên **không tự sinh bút toán**. Nhân viên là **đối tượng theo dõi** trên các tài khoản nội bộ:

| Trường hợp (chứng từ) | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Chi tạm ứng cho nhân viên | 141 (theo NV) | 111 / 112 | Theo dõi tạm ứng chi tiết theo từng người |
| Hoàn tạm ứng (nộp lại tiền dư) | 111 / 112 | 141 (theo NV) | |
| Quyết toán tạm ứng (chi phí thực tế) | 6xx / 152… + 1331 | 141 (theo NV) | |
| Tính lương phải trả | 622/627/641/642 | 334 (theo NV) | Lương theo bộ phận sử dụng lao động |
| Trả lương | 334 (theo NV) | 111 / 112 | |

Bút toán chỉ phát sinh khi lập phiếu tạm ứng / bảng lương thực tế.

## Tình huống đặc biệt & cảnh báo

- **Dùng chung với phân hệ Tiền lương:** đây là cùng một hồ sơ — không khai lại trong phần tiền lương. Sửa thông tin nhân viên ở một nơi cập nhật cho cả tạm ứng và lương.
- **Tạm ứng theo từng người:** TK 141 theo dõi chi tiết theo nhân viên; quyết toán tạm ứng phải đúng đối tượng để số dư khớp.
- **Nhân viên nghỉ việc:** không xóa nếu đã có phát sinh tạm ứng/lương; chuyển trạng thái sang Nghỉ việc và bảo đảm đã quyết toán hết tạm ứng.
- **Đa công ty:** nhân viên thuộc công ty nào thì phát sinh tạm ứng/lương ghi theo công ty đó.
- **Thông tin tính thuế/bảo hiểm:** nếu dùng phân hệ tiền lương, khai đủ thông tin cá nhân để tính đúng thuế TNCN và các khoản trích theo lương.

## Báo cáo liên quan

- **Sổ chi tiết tạm ứng (TK 141)**: số dư tạm ứng theo từng nhân viên.
- **Bảng lương / báo cáo tiền lương**: tổng hợp phải trả người lao động (TK 334).
- **Báo cáo thuế TNCN**: nếu dùng phân hệ tiền lương đầy đủ.

## FAQ

**Q: Nhân viên ở Danh mục và ở phân hệ Tiền lương có phải hai nơi khác nhau?**
**A:** Không. Là cùng một hồ sơ nhân viên dùng chung. Khai một lần, dùng cho cả tạm ứng (141) và lương (334).

**Q: Khai báo nhân viên mới có phát sinh công nợ/lương không?**
**A:** Không. Chỉ phát sinh khi lập phiếu tạm ứng hoặc bảng lương.

**Q: Tạm ứng cho nhân viên theo dõi như thế nào?**
**A:** Chi tạm ứng ghi Nợ TK 141 theo từng nhân viên; khi nhân viên quyết toán (chứng từ chi phí) hoặc nộp lại tiền dư thì giảm 141. Số dư 141 còn lại chính là khoản nhân viên đang giữ.

**Q: Nhân viên nghỉ việc còn nợ tạm ứng thì sao?**
**A:** Phải quyết toán hết tạm ứng (nộp tiền lại hoặc bù trừ vào lương) trước khi chuyển trạng thái nghỉ việc; không xóa hồ sơ đã có phát sinh.
