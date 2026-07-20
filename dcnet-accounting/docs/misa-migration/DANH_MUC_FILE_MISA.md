# Danh mục file cần xuất từ Misa SME

Hai trường hợp sử dụng, mỗi trường hợp một bộ file. Giữ **nguyên tên file**
Misa đặt khi xuất — hệ thống nhận diện loại file theo tên (chấp nhận thêm
hậu tố kỳ, ví dụ `So_nhat_ky_chung_2025.xlsx`, `... T1.2026.xlsx`).

## Trường hợp 1 — Migrate đầy đủ cả năm (lần đầu)

Bộ ~40 file, xuất từ Misa SME cho kỳ cần chuyển (ví dụ cả năm 2025).
File mẫu thực tế: thư mục [mau-file/nam-2025/](mau-file/nam-2025/).

### Bắt buộc — chứng từ phát sinh

| File Misa | Nội dung |
|---|---|
| `So_nhat_ky_chung_*.xlsx` | Sổ nhật ký chung — nguồn gốc mọi chứng từ, **quan trọng nhất** |
| `Bang_ke_hoa_don_..._ban_ra_*.xlsx` | Bảng kê hóa đơn bán ra (mẫu quản trị) — chi tiết dòng hàng cho hóa đơn bán |
| `Bang_ke_hoa_don_..._mua_vao_*.xlsx` | Bảng kê hóa đơn mua vào (mẫu quản trị) — chi tiết dòng hàng cho hóa đơn mua |
| `So_chi_tiet_vat_tu_hang_hoa_*.xlsx` | Sổ chi tiết vật tư hàng hóa — chi tiết nhập/xuất kho cho phiếu kho |

### Bắt buộc — số dư đầu kỳ

| File Misa | Nội dung |
|---|---|
| `Danh_sach_so_du_tai_khoan.xlsx` | Số dư đầu kỳ mọi TK (nguồn duy nhất ghi sổ đầu kỳ) |
| `Danh_sach_cong_no_khach_hang.xlsx` | Chi tiết công nợ 131 theo khách hàng (thay thế chân 131 tổng) |
| `Danh_sach_cong_no_nha_cung_cap.xlsx` | Chi tiết công nợ 331 theo NCC |
| `Danh_sach_cong_no_nhan_vien.xlsx` | Chi tiết tạm ứng 141 theo nhân viên |
| `Danh_sach_ton_kho_vthh.xlsx` | Tồn kho đầu kỳ theo kho - vật tư |
| `Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx` | Số dư đầu kỳ từng TK ngân hàng |
| `Danh_sach_chi_phi_tra_truoc_dau_ky.xlsx` | Chi phí trả trước (TK 242) đầu kỳ |
| `Danh_sach_tai_san_co_dinh_dau_ky.xlsx` | TSCĐ đầu kỳ (nguyên giá, hao mòn) |
| `Danh_sach_cong_cu_dung_cu_dau_ky.xlsx` | CCDC đầu kỳ |

### Bắt buộc — danh mục

| File Misa | Nội dung |
|---|---|
| `Danh_sach_he_thong_tai_khoan_.xlsx` | Hệ thống tài khoản (gồm TK con tự mở) |
| `Danh_sach_khach_hang.xlsx` | Khách hàng (mã + tên + MST) |
| `Danh_sach_nha_cung_cap.xlsx` | Nhà cung cấp |
| `Danh_sach_nhan_vien.xlsx` | Nhân viên |
| `Danh_sach_hang_hoa_dich_vu.xlsx` | Vật tư hàng hóa dịch vụ |
| `Danh_sach_kho.xlsx` | Kho |
| `Danh_sach_don_vi_tinh.xlsx` | Đơn vị tính |

### Nên có — danh mục bổ trợ

| File Misa | Nội dung |
|---|---|
| `Danh_sach_nhom_khach_hang_nha_cung_cap.xlsx` | Nhóm KH/NCC |
| `Danh_sach_nhom_vat_tu_hang_hoa_dich_vu.xlsx` | Nhóm vật tư |
| `Danh_sach_ngan_hang.xlsx` + `Danh_sach_tai_khoan_ngan_hang.xlsx` | Ngân hàng + TK ngân hàng |
| `Danh_sach_co_cau_to_chuc.xlsx` | Cơ cấu tổ chức (phòng ban) |
| `Danh_sach_cong_trinh.xlsx` | Công trình/dự án |
| `Danh_sach_loai_tai_san_co_dinh.xlsx` | Loại TSCĐ |
| `Danh_sach_loai_cong_cu_dung_cu.xlsx` | Loại CCDC |
| `Doi_tuong_tap_hop_chi_phi.xlsx` | Đối tượng tập hợp chi phí (trung tâm chi phí) |
| `Danh_sach_tai_khoan_ngam_dinh.xlsx` | TK ngầm định Misa |
| `Danh_sach_tai_khoan_ket_chuyen.xlsx` | TK kết chuyển Misa |

Các file Misa khác trong bộ xuất chuẩn (biểu thuế, ký hiệu chấm công, loại
tiền, mã thống kê…) hệ thống nhận diện và **tự bỏ qua** — thả cùng cũng
không sao.

## Trường hợp 2 — Migrate theo tháng (bộ rút gọn 6 file)

Dùng khi: (a) migrate nối tiếp tháng mới trên công ty đã có sổ, hoặc
(b) bắt đầu sử dụng từ một tháng cụ thể (không cần lịch sử cả năm).
File mẫu thực tế: thư mục [mau-file/thang-1-2026/](mau-file/thang-1-2026/).

| # | File Misa | Nội dung |
|---|---|---|
| 1 | `So_nhat_ky_chung_<kỳ>.xlsx` | Sổ nhật ký chung của tháng |
| 2 | `Bang_can_doi_tai_khoan_mau_quan_tri_<kỳ>.xlsx` | Bảng cân đối tài khoản (mẫu quản trị): cột Đầu kỳ dùng ghi sổ dư đầu, cột Cuối kỳ dùng đối chiếu kết quả |
| 3 | `Bang_ke_hoa_don_..._ban_ra_<kỳ>.xlsx` | Bảng kê bán ra của tháng |
| 4 | `Bang_ke_hoa_don_..._mua_vao_<kỳ>.xlsx` | Bảng kê mua vào của tháng |
| 5 | `So_chi_tiet_vat_tu_hang_hoa_<kỳ>.xlsx` | Sổ chi tiết vật tư của tháng |
| 6 | `Tong_hop_ton_kho.xlsx` | Tổng hợp tồn kho — đối chiếu tồn cuối |

Bộ rút gọn **không có file danh mục** — hệ thống tự suy ra khách hàng, NCC,
vật tư, kho, TK con từ chính Sổ nhật ký chung + bảng kê (đặt tên theo mã
Misa). Khi chạy **nối tiếp** trên công ty đã có sổ, phần Đầu kỳ của Bảng cân
đối tài khoản được tự bỏ qua để không ghi trùng.

## Cách xuất file từ Misa SME

- Sổ/bảng kê: mở đúng báo cáo trong Misa (Sổ nhật ký chung, Bảng kê bán
  ra/mua vào **mẫu quản trị**, Sổ chi tiết vật tư hàng hóa, Bảng cân đối tài
  khoản **mẫu quản trị**) → chọn kỳ → Xuất khẩu Excel.
- Danh mục + số dư đầu kỳ: Tệp → Xuất khẩu dữ liệu → chọn các danh mục →
  Misa tự đặt tên file như bảng trên.
- Xuất **.xlsx** (mặc định). Không đổi tên file, không sửa nội dung.
