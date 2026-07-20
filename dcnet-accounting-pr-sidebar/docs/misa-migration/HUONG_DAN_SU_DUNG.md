# Hướng dẫn sử dụng Misa Migration Hub

Công cụ chuyển toàn bộ số liệu kế toán từ **Misa SME** sang hệ thống mới.
Quy trình chỉ gồm **3 thao tác**: chọn công ty → thả file Excel → bấm một nút.
Hệ thống tự chạy đến khi ra bảng cân đối, có thanh tiến trình hiển thị từng bước.

## Chuẩn bị

1. **Công ty nhận dữ liệu**: tạo công ty mới với **tiền tệ VND** (Danh mục →
   Công ty → Tạo mới, hoặc gõ tên ở ô chọn công ty trong Hub và bấm "Tạo công
   ty mới"). Hệ thống tài khoản TT99/2025 và các tài khoản con từ file Misa
   sẽ được cài tự động — không cần cấu hình trước.
2. **File Excel xuất từ Misa SME**: xem danh mục file cần xuất tại
   [DANH_MUC_FILE_MISA.md](DANH_MUC_FILE_MISA.md). Giữ nguyên tên file Misa
   đặt — hệ thống nhận diện loại file theo tên.

## Các bước thực hiện

1. Mở **Công cụ Import → Misa Migration Hub** trên thanh điều hướng.
2. Gõ tên **Công ty nhận dữ liệu** và chọn từ gợi ý.
3. Kéo thả **toàn bộ** file Excel vào vùng nhận file (hoặc bấm để chọn nhiều
   file cùng lúc). Bảng liệt kê hiện ra với cột "Loại đã nhận diện" — kiểm tra
   nhanh; file nào hiện "Unknown" thì chọn lại loại đúng hoặc để Skip.
4. Bấm **🚀 Bắt đầu migration**.
5. Theo dõi thanh tiến trình. Pipeline chạy tự động 6 bước:

   | Bước | Việc hệ thống làm |
   |---|---|
   | Phân tích file | Đọc từng file Excel, đếm số dòng |
   | Cài đặt tài khoản & danh mục | Hệ thống TK TT99 + TK con, khách hàng, NCC, vật tư, kho… (tự suy ra từ dữ liệu nếu thiếu file danh mục) |
   | Kiểm tra dữ liệu | Soát lỗi chặn trước khi ghi sổ |
   | Tạo & ghi sổ chứng từ | Ghi toàn bộ chứng từ bằng đường bulk (vài giây đến ~1 phút) |
   | Tinh chỉnh sổ cái theo nguồn | Đối chiếu lại từng chứng từ với Sổ nhật ký chung |
   | Đối chiếu số liệu | So Số dư cuối kỳ từng TK + Tồn kho với chính file đã upload |

6. Khi hoàn tất, màn hình kết quả hiển thị:
   - **Bảng cân đối CÂN** (tổng Nợ = tổng Có) hay không;
   - **Số dư cuối kỳ khớp file Misa**: số TK khớp / tổng số TK;
   - **Tồn kho khớp file Misa**: số dòng kho-vật tư khớp;
   - Bảng số chứng từ đã ghi sổ theo từng loại.
   Nút **Mở Bảng cân đối số phát sinh** để xem ngay trên hệ thống.

## Khi pipeline tạm dừng

- **Dừng vì dữ liệu có vấn đề (màu vàng)**: đọc danh sách lỗi chặn, sửa
  (thường là thiếu file danh mục, hoặc file sai loại) rồi bấm **Chạy tiếp**.
- **Dừng vì lỗi hệ thống (màu đỏ)**: bấm **Chạy tiếp từ chỗ dừng** — pipeline
  chạy lại từ bước gần nhất, các bước đã xong không chạy lại.
- **Bỏ đợt này / Bắt đầu lại**: hủy đợt hiện tại, dữ liệu đã ghi sổ của đợt
  được giữ nguyên; muốn xóa sạch dùng nút xóa trong Lịch sử Migration.

## Migration nhiều kỳ (nối tiếp)

Chạy đợt **năm trước** xong → tạo đợt mới với bộ file **tháng tiếp theo**
(cùng công ty). Hệ thống tự nhận biết công ty đã có sổ và **bỏ qua phần số dư
đầu kỳ** của đợt sau (tránh ghi trùng), chỉ ghi chứng từ phát sinh mới.

## Lưu ý

- Chứng từ migrate giữ nguyên **số chứng từ Misa** (trường "Số chứng từ Misa"
  trên mỗi chứng từ) để tra cứu ngược.
- Hóa đơn điều chỉnh Misa không đưa vào Bảng kê bán ra/mua vào vẫn được ghi
  sổ đủ chân Nợ/Có (dưới dạng Phiếu kế toán) — sổ cái không mất số liệu.
- Sau migration nên kiểm tra: Bảng cân đối số phát sinh, Sổ cái vài TK chính
  (111, 112, 131, 331, 511), và Tổng hợp tồn kho.
- Kết quả test thực tế với dữ liệu DCNET: xem
  [KET_QUA_TEST_2026-06-11.md](KET_QUA_TEST_2026-06-11.md).
