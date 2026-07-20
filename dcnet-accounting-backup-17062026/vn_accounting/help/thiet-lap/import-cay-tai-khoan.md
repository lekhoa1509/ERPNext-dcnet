---
title: Import cây tài khoản
order: 3
summary: Công cụ nạp cả hệ thống tài khoản từ file bảng tính (8 cột) — tải mẫu, điền theo cấu trúc cha-con, tải lên và tạo hàng loạt.
---

## Mục đích

**Import cây tài khoản** là công cụ nạp toàn bộ hệ thống tài khoản vào một công ty từ một file bảng tính, thay vì tạo từng TK thủ công. Phù hợp khi mới khởi tạo công ty hoặc khi cần thay thế toàn bộ cây TK theo một hệ thống tài khoản chuẩn (TT99/2025).

## Khi nào dùng

- **Khi tạo công ty mới** chưa có phát sinh kế toán: nạp cả cây TT99/2025 một lần.
- **Khi muốn áp một mẫu cây TK chuẩn** đã chuẩn bị sẵn trong Excel/CSV.
- **Khi cần xem mẫu định dạng:** tải mẫu để biết cấu trúc 8 cột rồi điền theo.

## Cách thực hiện

1. Mở **Import cây tài khoản** trên menu Công cụ Import.
2. Chọn **Công ty** đích.
3. **Tải mẫu** (template) — file mẫu có đúng 8 cột chuẩn. Mở mẫu, điền các tài khoản theo cấu trúc cha-con (TK cha phải nằm trên TK con).
4. **Tải file lên** (đính kèm). Hệ thống kiểm tra: file phải có đúng 8 cột, không rỗng.
5. Xem trước cây sẽ tạo, rồi bấm **Import** để tạo hàng loạt.

### Cấu trúc 8 cột

File phải có đúng **8 cột** theo mẫu (nếu sai số cột, hệ thống báo "Sai mẫu, vui lòng so sánh file với mẫu chuẩn"). Các cột mô tả: số hiệu TK, tên TK, TK cha, là nhóm hay không, loại gốc (Tài sản/Nợ phải trả/Vốn/Thu nhập/Chi phí), loại TK, số dư đầu... theo đúng thứ tự trong file mẫu. **Luôn dùng file mẫu tải từ hệ thống** để đảm bảo đúng định dạng.

## Định khoản tự động

Công cụ này **không sinh bút toán** — chỉ tạo các tài khoản trong danh mục. Để nhập **số dư đầu kỳ** (bút toán mở sổ), dùng nghiệp vụ số dư đầu kỳ riêng ở phân hệ Tổng hợp sau khi cây TK đã sẵn sàng.

## Tình huống đặc biệt & cảnh báo

- **CHỈ import được khi công ty chưa có phát sinh.** Nếu công ty đã có bút toán (Sổ Cái có dữ liệu), công cụ sẽ chặn import để tránh phá vỡ dữ liệu kế toán đang dùng. Khi đó phải tạo/sửa TK lẻ thủ công trong [Cây tài khoản](cay-tai-khoan.md).
- **Import thay thế toàn bộ cây hiện có** của công ty (xóa cây mặc định nếu chưa phát sinh) — kiểm tra kỹ file trước khi chạy.
- **File phải đúng 8 cột**, không thừa/thiếu cột, không có dòng trống ở giữa. Chấp nhận Excel (.xlsx/.xls) hoặc CSV.
- **TK cha phải xuất hiện trước TK con** trong file, nếu không hệ thống không xác định được cấp bậc.
- **Công ty con** (child company) không import trực tiếp được — phải import vào công ty mẹ hoặc bật quyền tạo TK cho công ty con.

## Báo cáo liên quan

- [Cây tài khoản](cay-tai-khoan.md) — chỉnh sửa cây sau khi import.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — chọn TK mặc định sau khi cây đã có.

## FAQ

**Q: Tôi đã import xong nhưng muốn thêm vài TK chi tiết — có import lại được không?**
**A:** Sau khi công ty đã phát sinh thì không import lại được. Hãy thêm TK lẻ thủ công trong [Cây tài khoản](cay-tai-khoan.md) — nhanh và không ảnh hưởng dữ liệu cũ.

**Q: File của tôi báo "Sai mẫu" dù trông giống mẫu?**
**A:** Hệ thống đếm đúng 8 cột. Kiểm tra có cột thừa (ô trống bên phải), cột gộp, hoặc dòng tiêu đề lặp. Tốt nhất là chép dữ liệu vào đúng file mẫu tải từ hệ thống.

**Q: Import có nhập luôn số dư đầu kỳ không?**
**A:** Không sinh bút toán mở sổ. Sau khi cây TK có rồi, nhập số dư đầu kỳ qua nghiệp vụ riêng ở phân hệ Tổng hợp.
