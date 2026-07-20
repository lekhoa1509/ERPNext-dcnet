# Misa Migration Hub — tài liệu

Chuyển số liệu kế toán từ Misa SME sang vn_accounting (ERPNext/Frappe) bằng
một màn hình duy nhất: chọn công ty → thả file → một nút, pipeline 6 bước
tự chạy đến khi ra bảng cân đối.

| Tài liệu | Nội dung |
|---|---|
| [HUONG_DAN_SU_DUNG.md](HUONG_DAN_SU_DUNG.md) | Hướng dẫn thao tác Migration Hub cho người dùng |
| [DANH_MUC_FILE_MISA.md](DANH_MUC_FILE_MISA.md) | Danh mục file cần xuất từ Misa cho 2 trường hợp (cả năm / theo tháng) |
| [KET_QUA_TEST_2026-06-11.md](KET_QUA_TEST_2026-06-11.md) | Kết quả test E2E trên site mới + công ty mới, kèm số record đã tạo |
| [mau-file/nam-2025/](mau-file/nam-2025/) | Bộ 40 file Misa thực tế — trường hợp migrate cả năm |
| [mau-file/thang-1-2026/](mau-file/thang-1-2026/) | Bộ 6 file Misa thực tế — trường hợp migrate theo tháng |

Kiến trúc pipeline + chi tiết kỹ thuật: xem
`vn_accounting/misa_migration/docs/` trong mã nguồn.
