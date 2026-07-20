---
section: Ngân hàng
title: Tổng quan Ngân hàng
summary: Giới thiệu phân hệ Ngân hàng với 11 mục menu và quy trình điển hình.
---

## Mục đích

Phân hệ **Ngân hàng** quản lý mọi nghiệp vụ thu/chi/chuyển khoản liên quan đến tài khoản ngân hàng (TK 112). Ngoài các giao dịch cơ bản, phân hệ còn bao gồm công cụ đối soát sao kê, quản lý tiền gửi có kỳ hạn, khoản vay ngân hàng, và dự báo dòng tiền.

## Khi nào dùng

- Hằng ngày: tạo phiếu thu/chi ngân hàng từ nút "Tạo > Phiếu thanh toán" trên hóa đơn bán hàng / hóa đơn mua hàng, hoặc bấm "+ Thêm" trong danh sách phiếu kế toán.
- Cuối ngày: đối soát sao kê ngân hàng để khớp số dư với sổ sách.
- Định kỳ: xem **Sổ Tài khoản ngân hàng** để chốt số dư; theo dõi **Tiền gửi có kỳ hạn** và **Khoản vay**.
- Cuối tháng/quý/năm: in sổ chi tiết tài khoản ngân hàng, báo cáo tổng hợp khoản vay, dự báo dòng tiền.

## Cách thực hiện

Cấu trúc menu **Ngân hàng** gồm 11 mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Thu ngân hàng | Báo cáo | Tổng hợp THU ngân hàng (gồm phiếu kế toán và phiếu thanh toán) |
| 2 | Chi ngân hàng | Báo cáo | Tổng hợp CHI ngân hàng (gồm phiếu kế toán và phiếu thanh toán) |
| 3 | Sổ Tài khoản ngân hàng | Báo cáo | Sổ chi tiết TK 112 theo từng tài khoản |
| 4 | Đối soát sao kê | Trang | Công cụ đối chiếu sao kê ngân hàng với sổ sách |
| 5 | Điều chuyển nội bộ | Báo cáo | Tổng hợp điều chuyển giữa tiền mặt (111) và ngân hàng (112) |
| 6 | Bút toán ngân hàng | Danh sách | Danh sách phiếu kế toán loại Bank Entry |
| 7 | Tiền gửi có kỳ hạn | Danh sách | Quản lý sổ tiền gửi có kỳ hạn |
| 8 | Tổng hợp tiền gửi có kỳ hạn | Báo cáo | Báo cáo tổng hợp tiền gửi có kỳ hạn |
| 9 | Khoản vay ngân hàng | Danh sách | Quản lý khoản vay ngân hàng |
| 10 | Tổng hợp khoản vay ngân hàng | Báo cáo | Báo cáo tổng hợp khoản vay |
| 11 | Dự báo dòng tiền | Trang | Dự báo dòng tiền tương lai |

### Quy trình điển hình

1. **Hằng ngày — tạo chứng từ:** mở hóa đơn bán hàng / hóa đơn mua hàng → bấm "Tạo > Phiếu thanh toán", chọn phương thức Chuyển khoản để sinh phiếu thanh toán; hoặc mở danh sách phiếu kế toán (mục Tổng hợp) → "+ Thêm" để tạo phiếu kế toán Bank Entry.
2. **Tra cứu trong ngày:** bấm "Thu ngân hàng" / "Chi ngân hàng" để xem báo cáo tổng hợp.
3. **Cuối ngày/tuần:** bấm "Đối soát sao kê" → nhập file sao kê ngân hàng → hệ thống tự động gợi ý khớp.
4. **Cuối tháng:** xem "Sổ Tài khoản ngân hàng"; cập nhật "Tiền gửi có kỳ hạn" và "Khoản vay ngân hàng" nếu có phát sinh mới.
5. **Định kỳ:** xem các báo cáo tổng hợp + dự báo dòng tiền.

### Liên kết tới các bài hướng dẫn chi tiết

- **Báo cáo giao dịch**: [Thu ngân hàng](thu-ngan-hang.md), [Chi ngân hàng](chi-ngan-hang.md), [Sổ Tài khoản ngân hàng](so-tai-khoan-ngan-hang.md), [Điều chuyển nội bộ](dieu-chuyen-noi-bo.md)
- **Công cụ**: [Đối soát sao kê](doi-soat-sao-ke.md), [Dự báo dòng tiền](du-bao-dong-tien.md)
- **Quản lý**: [Bút toán ngân hàng](but-toan-ngan-hang.md), [Tiền gửi có kỳ hạn](tien-gui-co-ky-han.md), [Khoản vay ngân hàng](khoan-vay-ngan-hang.md)
- **Báo cáo tổng hợp**: [Tổng hợp tiền gửi có kỳ hạn](tong-hop-tien-gui-co-ky-han.md), [Tổng hợp khoản vay ngân hàng](tong-hop-khoan-vay-ngan-hang.md)

## Định khoản tự động

Phân hệ này không tự động tạo bút toán — kế toán viên định khoản thủ công trong từng phiếu kế toán hoặc phiếu thanh toán. Các bút toán phổ biến liên quan đến TK 112:

| Nghiệp vụ | TK Nợ | TK Có |
|---|---|---|
| Khách hàng thanh toán chuyển khoản | 1121 | 131 |
| Trả nhà cung cấp chuyển khoản | 331 | 1121 |
| Rút tiền mặt từ ngân hàng về quỹ | 1111 | 1121 |
| Nộp tiền mặt vào ngân hàng | 1121 | 1111 |
| Điều chuyển giữa các TK ngân hàng | 1121-B | 1121-A |
| Gửi tiền có kỳ hạn | 128 (hoặc TK theo dõi riêng) | 1121 |
| Nhận vốn vay ngân hàng | 1121 | 341 |

## Tình huống đặc biệt & cảnh báo

- **Hai loại chứng từ ngân hàng:** Phiếu kế toán loại Bank Entry cho bút toán tổng quát; Phiếu thanh toán phương thức Chuyển khoản cho việc thanh toán hóa đơn bán/mua. Hai mục báo cáo **Thu ngân hàng** / **Chi ngân hàng** tổng hợp CẢ HAI nguồn.
- **Chênh lệch sao kê:** sử dụng công cụ Đối soát sao kê để tìm và xử lý chênh lệch. Xem [Đối soát sao kê](doi-soat-sao-ke.md).
- **Tiền gửi có kỳ hạn:** ghi nhận riêng trên TK 128 (đầu tư nắm giữ đến ngày đáo hạn) hoặc TK theo dõi riêng, không gộp vào TK 112.
- **Lãi vay phải trả:** ghi nhận định kỳ vào TK 635; không để dồn cuối năm.
- **Tỷ giá ngoại tệ:** TK 1122 dành cho ngoại tệ; đánh giá lại cuối kỳ qua công cụ Đánh giá lại ngoại tệ.

## FAQ

**Q: Tại sao không có mục "+ Thu ngân hàng" / "+ Chi ngân hàng" trên menu?**
**A:** Menu được thiết kế theo hướng báo cáo. Tạo phiếu thu/chi ngân hàng đi qua đường tự nhiên: hóa đơn bán hàng → "Tạo > Phiếu thanh toán"; hoặc danh sách phiếu kế toán → "+ Thêm" với số hiệu chứng từ Bank Entry.

**Q: Có thể import sao kê tự động không?**
**A:** Có. Công cụ Đối soát sao kê hỗ trợ import file sao kê định dạng CSV/Excel từ hầu hết các ngân hàng Việt Nam. Xem [Đối soát sao kê](doi-soat-sao-ke.md).

**Q: Lãi tiền gửi có kỳ hạn ghi nhận thế nào?**
**A:** Ghi nhận khi đáo hạn hoặc định kỳ: Nợ TK 112 / Có TK 515 (doanh thu tài chính).
