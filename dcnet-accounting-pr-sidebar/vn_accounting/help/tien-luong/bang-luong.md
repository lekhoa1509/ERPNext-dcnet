---
title: Bảng lương
order: 3
summary: Tính lương hàng loạt theo kỳ cho một nhóm nhân viên, sinh phiếu lương và bút toán hạch toán chi phí lương cùng các khoản trích.
---

## Mục đích

**Bảng lương** là chứng từ tính lương hàng loạt: chọn kỳ, công ty và nhóm nhân viên → hệ thống tạo hàng loạt phiếu lương, rồi khi duyệt sẽ sinh **bút toán hạch toán chi phí lương và các khoản trích theo lương**. Đây là **chứng từ duy nhất** trong phân hệ Tiền lương tạo bút toán Sổ Cái.

## Khi nào dùng

- Cuối mỗi kỳ lương (thường là cuối tháng): chạy lương cho toàn bộ hoặc một phòng ban nhân viên.
- Khi cần hạch toán chi phí nhân công vào TK 622/627/641/642 và ghi nhận công nợ phải trả người lao động (TK 334).
- Khi cần trích các khoản theo lương (BHXH/BHYT/BHTN/KPCĐ) và khấu trừ thuế TNCN.

## Cách thực hiện

1. Bấm **Bảng lương** → bấm **+ Thêm**.
2. Chọn **Loại** (Lương/Thưởng), **Công ty**, **Ngày bắt đầu — kết thúc** kỳ lương, **TK Phải trả lương** (TK 334), và bộ lọc nhân viên (Phòng ban, Chi nhánh, Chỉ định/Bộ phận...).
3. Bấm **Lấy danh sách nhân viên** → hệ thống nạp các nhân viên thỏa điều kiện đã có Gán Cơ cấu lương.
4. Bấm **Tạo phiếu lương** → sinh hàng loạt phiếu lương ở trạng thái nháp (xử lý nền nếu trên 30 nhân viên).
5. Kiểm tra từng [Phiếu lương](phieu-luong.md), đối chiếu số ngày công và số tiền.
6. **Gửi/Duyệt phiếu lương** → **Ghi sổ kế toán** (Tạo bút toán hạch toán) để sinh bút toán chi phí lương và các khoản trích.
7. Sau đó tạo bút toán/phiếu thanh toán **chi lương** (Dr 334 / Cr 111/112) khi thực chi.

## Định khoản tự động

Khi ghi sổ Bảng lương, hệ thống lập **bút toán hạch toán (accrual)** dựa trên TK khai ở từng Thành phần lương:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Hạch toán chi phí lương theo bộ phận | 622 / 627 / 641 / 642 | 334 | TK Nợ = TK của thành phần lương loại Thu nhập |
| Trích bảo hiểm/KPCĐ — phần doanh nghiệp chịu | 622 / 627 / 641 / 642 | 3383 / 3384 / 3386 / 3382 | Tính vào chi phí theo bộ phận |
| Khấu trừ bảo hiểm — phần người lao động chịu | 334 | 3383 / 3384 / 3386 | Trừ vào lương người lao động |
| Khấu trừ thuế TNCN | 334 | 3335 | Theo biểu lũy tiến |

Bút toán **chi trả lương** (Dr 334 / Cr 111/112) và **nộp bảo hiểm, TNCN** (Dr 338x/3335 / Cr 112) được lập riêng sau, không nằm trong bút toán hạch toán của Bảng lương.

## Tình huống đặc biệt & cảnh báo

- **TK Phải trả lương (334) phải là loại "Phải trả".** Nếu để trống hoặc gán sai loại tài khoản, hệ thống chặn duyệt. TK 334 cần được khai cả trên Bảng lương VÀ trên Gán Cơ cấu lương của từng nhân viên.
- **Xử lý nền cho lô lớn:** trên 30 nhân viên, việc tạo phiếu lương chạy nền — chờ hoàn tất rồi mới ghi sổ. Trên môi trường không có tiến trình nền, chạy đồng bộ.
- **TK chi phí lấy từ Thành phần lương.** Bút toán chỉ đúng khi mỗi Thành phần lương đã khai đúng TK theo bộ phận sử dụng lao động.
- **Hủy để sửa:** nếu phát hiện sai sau khi ghi sổ, hủy Bảng lương (kéo theo hủy phiếu lương và bút toán liên quan), sửa dữ liệu gốc rồi chạy lại — không sửa trực tiếp bút toán.
- **Phụ thuộc số ngày công:** thành phần lương có thiết lập "phụ thuộc số ngày công" sẽ tính theo số ngày làm thực tế lấy từ Bảng chấm công.

## Báo cáo liên quan

- [Phiếu lương](phieu-luong.md): chi tiết tính lương từng người do Bảng lương sinh ra.
- [Gán Cơ cấu lương](gan-co-cau-luong.md): nguồn cấu hình mức lương và TK phải trả lương.
- **Sổ Cái / Bảng cân đối số phát sinh:** kiểm tra phát sinh TK 334, 338x, 3335 sau khi ghi sổ.

## FAQ

**Q: Bảng lương tạo bút toán gì?**
**A:** Bút toán hạch toán: Dr chi phí lương (622/627/641/642) và Cr 334; đồng thời trích các khoản theo lương (Cr 338x phần DN qua Dr 62x/64x, và Dr 334 / Cr 338x phần người lao động) cùng khấu trừ TNCN (Dr 334 / Cr 3335).

**Q: Bút toán chi lương có tự tạo cùng lúc không?**
**A:** Không. Bảng lương chỉ hạch toán chi phí (accrual). Khi thực chi lương, lập bút toán/phiếu thanh toán riêng Dr 334 / Cr 111 (hoặc 112).

**Q: Vì sao không lấy được nhân viên vào Bảng lương?**
**A:** Nhân viên phải có Gán Cơ cấu lương hiệu lực trong kỳ và thỏa bộ lọc (công ty/phòng ban/chi nhánh). Kiểm tra lại Gán Cơ cấu lương.

**Q: Tổng lương trên Bảng lương nằm ở đâu?**
**A:** Cộng tổng lương thực lĩnh của các phiếu lương thuộc kỳ. Để tổng hợp, xem danh sách phiếu lương hoặc Sổ Cái TK 334.
