---
section: Tiền lương
title: Tổng quan Tiền lương
summary: Giới thiệu phân hệ Tiền lương — chấm công, tính lương, định khoản chi phí lương và các khoản trích theo lương theo VAS.
---

## Mục đích

Phân hệ **Tiền lương** quản lý toàn bộ quy trình từ **chấm công** → **tính lương** → **định khoản chi phí lương và các khoản trích theo lương** → **chi trả lương**. Kế toán viên dùng phân hệ này để hạch toán chi phí nhân công (TK 622/627/641/642), các khoản trích bảo hiểm và kinh phí công đoàn (TK 338x), khấu trừ thuế thu nhập cá nhân (TK 3335) và theo dõi công nợ phải trả người lao động (TK 334).

## Khi nào dùng

- **Hằng ngày/cuối tháng:** chấm công cho nhân viên (Bảng chấm công), ghi nhận giờ công theo dự án (Bảng giờ công).
- **Cuối kỳ lương:** chạy Bảng lương để tính lương hàng loạt, sinh Phiếu lương cho từng nhân viên.
- **Thiết lập ban đầu:** khai báo Thành phần lương, dựng Cơ cấu lương, gán cơ cấu cho từng nhân viên.
- **Phát sinh bất thường:** thưởng, phụ cấp một lần, khấu trừ riêng → Lương bổ sung.
- **Quản trị hồ sơ:** cập nhật Danh sách nhân viên (thông tin cá nhân, mã số thuế, số sổ BHXH, tài khoản ngân hàng).

## Cách thực hiện

Cấu trúc menu **Tiền lương** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Bảng chấm công | Danh sách | Ghi nhận ngày công/ca làm của nhân viên |
| 2 | Bảng giờ công (theo dự án) | Danh sách | Ghi nhận giờ làm theo dự án/công việc |
| 3 | Bảng lương | Danh sách | Tính lương hàng loạt theo kỳ, sinh phiếu lương + bút toán lương |
| 4 | Phiếu lương | Danh sách | Phiếu lương chi tiết của từng nhân viên |
| 5 | Cơ cấu lương | Danh sách | Khuôn mẫu các thành phần lương áp dụng cho nhóm nhân viên |
| 6 | Thành phần lương | Danh sách | Khai báo từng khoản lương/khấu trừ và TK hạch toán |
| 7 | Gán Cơ cấu lương | Danh sách | Gán cơ cấu lương + mức lương gốc cho từng nhân viên |
| 8 | Lương bổ sung | Danh sách | Thưởng/phụ cấp/khấu trừ một lần ngoài cơ cấu |
| 9 | Danh sách nhân viên | Danh sách | Hồ sơ nhân viên (MST, sổ BHXH, tài khoản nhận lương) |
| 10 | Thuế TNCN | Trang (đang phát triển) | Tổng hợp khấu trừ thuế TNCN theo biểu lũy tiến |
| 11 | BC lương theo phòng ban | Trang (đang phát triển) | Báo cáo chi phí lương phân bổ theo phòng ban |

### Quy trình điển hình

1. **Thiết lập (làm 1 lần):** khai báo [Thành phần lương](thanh-phan-luong.md) với TK hạch toán đúng → dựng [Cơ cấu lương](co-cau-luong.md) → [Gán Cơ cấu lương](gan-co-cau-luong.md) cho từng nhân viên với mức lương gốc.
2. **Trong kỳ:** chấm công qua [Bảng chấm công](bang-cham-cong.md); nếu cần phân bổ chi phí theo dự án thì ghi [Bảng giờ công](bang-gio-cong.md).
3. **Cuối kỳ lương:** mở [Bảng lương](bang-luong.md) → chọn kỳ, công ty, phòng ban → tạo phiếu lương hàng loạt → kiểm tra [Phiếu lương](phieu-luong.md) từng người.
4. **Ghi sổ:** duyệt Bảng lương → hệ thống sinh bút toán hạch toán chi phí lương và các khoản trích (Dr 622/627/641/642, Cr 334 và các TK 338x/3335).
5. **Chi trả:** tạo bút toán/phiếu thanh toán chi lương (Dr 334 / Cr 111/112); nộp bảo hiểm và TNCN cho cơ quan (Dr 338x/3335 / Cr 112).
6. **Phát sinh thêm:** dùng [Lương bổ sung](luong-bo-sung.md) cho thưởng/phụ cấp/khấu trừ một lần.

### Liên kết tới các bài hướng dẫn chi tiết

- **Chấm công & giờ công:** [Bảng chấm công](bang-cham-cong.md), [Bảng giờ công (theo dự án)](bang-gio-cong.md).
- **Tính lương:** [Bảng lương](bang-luong.md), [Phiếu lương](phieu-luong.md), [Lương bổ sung](luong-bo-sung.md).
- **Thiết lập:** [Thành phần lương](thanh-phan-luong.md), [Cơ cấu lương](co-cau-luong.md), [Gán Cơ cấu lương](gan-co-cau-luong.md).
- **Hồ sơ:** [Danh sách nhân viên](danh-sach-nhan-vien.md).
- **Đang phát triển:** [Thuế TNCN](thue-tncn.md), [BC lương theo phòng ban](bc-luong-phong-ban.md).

## Định khoản tự động

**Bảng lương** là chứng từ duy nhất trong phân hệ tự động sinh bút toán. Khi duyệt (ghi sổ), hệ thống lập bút toán hạch toán dựa trên TK đã khai báo ở từng Thành phần lương:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Hạch toán chi phí lương (theo bộ phận sử dụng lao động) | 622 / 627 / 641 / 642 | 334 | TK Nợ lấy theo TK của thành phần lương loại Thu nhập |
| Trích các khoản theo lương — phần doanh nghiệp chịu | 622 / 627 / 641 / 642 | 3383 / 3384 / 3386 / 3382 | BHXH/BHYT/BHTN/KPCĐ phần DN tính vào chi phí |
| Khấu trừ các khoản theo lương — phần người lao động chịu | 334 | 3383 / 3384 / 3386 | Khoản trừ vào lương người lao động |
| Khấu trừ thuế TNCN | 334 | 3335 | Theo biểu lũy tiến từng phần |
| Chi trả lương cho người lao động | 334 | 111 / 112 | Bút toán/phiếu thanh toán chi lương (lập riêng) |
| Nộp bảo hiểm & TNCN cho cơ quan | 3383/3384/3386 / 3335 / 3382 | 112 | Bút toán nộp tiền (lập riêng) |

Các mục còn lại (Chấm công, Giờ công, Cơ cấu/Thành phần lương, Gán cơ cấu, Lương bổ sung, Danh sách nhân viên) **không tự định khoản** — chỉ là dữ liệu đầu vào hoặc thiết lập phục vụ cho Bảng lương tính ra số liệu hạch toán.

## Tình huống đặc biệt & cảnh báo

- **TK 334 phải là loại "Phải trả".** Trước khi chạy Bảng lương, kiểm tra TK 334 (và TK Phải trả lương đã khai trên công ty/Gán cơ cấu lương) được gán đúng loại tài khoản; nếu không hệ thống sẽ chặn duyệt.
- **TK hạch toán nằm ở Thành phần lương.** Mỗi thành phần lương cần khai TK Nợ/Có theo bộ phận sử dụng lao động (622 sản xuất, 627 quản lý phân xưởng, 641 bán hàng, 642 quản lý doanh nghiệp). Khai sai TK → bút toán lương vào sai khoản chi phí.
- **Phân biệt phần DN chịu và phần người lao động chịu.** Phần doanh nghiệp đóng bảo hiểm/KPCĐ tính vào chi phí (Dr 62x/64x); phần người lao động đóng thì trừ vào lương (Dr 334). Hai phần này định khoản khác nhau dù cùng nộp vào TK 338x.
- **Tỷ lệ trích theo lương** theo quy định hiện hành: BHXH, BHYT, BHTN, KPCĐ — cập nhật tỷ lệ trong công thức của từng Thành phần lương khi nhà nước thay đổi.
- **Bảng chấm công và Bảng giờ công không sinh bút toán.** Chấm công chỉ ảnh hưởng số ngày công để tính lương; giờ công theo dự án dùng để phân bổ/theo dõi chi phí nhân công theo công trình, không tự tạo Sổ Cái.
- **Đã ghi sổ rồi mới phát hiện sai:** hủy Bảng lương (sẽ hủy phiếu lương và bút toán liên quan), sửa dữ liệu gốc rồi chạy lại — KHÔNG sửa trực tiếp bút toán đã ghi sổ.

## Báo cáo liên quan

- **Sổ Cái / Bảng cân đối số phát sinh:** kiểm tra phát sinh và số dư các TK 334, 338x, 3335 cuối kỳ.
- **Báo cáo chi phí lương theo phòng ban** (đang phát triển): phân bổ chi phí lương theo bộ phận.
- **Quyết toán thuế TNCN** (đang phát triển): tổng hợp khấu trừ TNCN của người lao động trong năm.

## FAQ

**Q: Chứng từ nào trong phân hệ tạo bút toán?**
**A:** Chỉ **Bảng lương** (khi duyệt). Phiếu lương là chi tiết tính toán cho từng người; bút toán tổng hợp do Bảng lương lập. Chấm công, giờ công và các mục thiết lập không sinh Sổ Cái.

**Q: Chi phí lương vào TK 622 hay 642?**
**A:** Tùy bộ phận sử dụng lao động: công nhân sản xuất trực tiếp → 622; quản lý phân xưởng → 627; nhân viên bán hàng → 641; bộ phận quản lý doanh nghiệp → 642. TK này khai ở Thành phần lương, không cố định.

**Q: Khấu trừ thuế TNCN ghi vào đâu?**
**A:** Khấu trừ tại nguồn ghi Có TK 3335 (Dr 334 / Cr 3335). Khi nộp cho cơ quan thuế: Dr 3335 / Cr 112. Mục "Thuế TNCN" trong menu hiện đang phát triển; trước mắt tính theo biểu lũy tiến thủ công.

**Q: Bảng giờ công theo dự án có làm tăng chi phí dự án không?**
**A:** Giờ công ghi nhận thời gian và giá trị nhân công theo dự án nhưng KHÔNG tự sinh Sổ Cái. Chi phí lương thực tế vào dự án thông qua bút toán lương (phân bổ vào TK 154/627 theo dự án) hoặc bút toán phân bổ riêng — xem phân hệ Giá thành.
