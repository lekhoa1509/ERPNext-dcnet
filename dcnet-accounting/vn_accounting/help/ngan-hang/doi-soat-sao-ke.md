---
title: Đối soát sao kê
order: 4
summary: Công cụ đối chiếu sao kê ngân hàng với sổ sách kế toán — import file sao kê và khớp tự động.
---

## Mục đích

**Đối soát sao kê** là công cụ giúp kế toán viên đối chiếu file sao kê từ ngân hàng (CSV, Excel) với dữ liệu sổ sách trên hệ thống. Hệ thống tự động gợi ý khớp từng dòng dựa trên số tiền, ngày giao dịch, và nội dung; kế toán viên xác nhận hoặc điều chỉnh thủ công.

## Khi nào dùng

- **Cuối ngày/tuần:** import sao kê mới từ ngân hàng, đối chiếu toàn bộ giao dịch.
- **Phát hiện chênh lệch:** khi Sổ Tài khoản ngân hàng không khớp với app ngân hàng.
- **Định kỳ:** rà soát toàn bộ giao dịch trong kỳ để đảm bảo không sót hoặc sai lệch.
- **Kiểm toán:** cung cấp bằng chứng đối chiếu cho kiểm toán viên.

## Cách thực hiện

1. Bấm **Đối soát sao kê** trên menu Ngân hàng → trang công cụ Đối soát sao kê mở.
2. Chọn **Tài khoản ngân hàng** và **Ngày sao kê** (mặc định hôm nay).
3. **Import sao kê**: tải lên file CSV hoặc Excel từ ngân hàng. Hỗ trợ hầu hết các ngân hàng Việt Nam (BIDV, Vietcombank, Techcombank, Sacombank, Agribank, MB Bank, ...).
4. Hệ thống phân tích file và hiển thị bảng đối chiếu gồm 3 cột:
   - **Sổ sách**: các giao dịch trong hệ thống (phiếu kế toán, phiếu thanh toán).
   - **Sao kê**: các dòng từ file ngân hàng.
   - **Kết quả khớp**: ✓ đã khớp / ⚠ chênh lệch / ✗ chưa có đối ứng.
5. **Xác nhận khớp**: bấm vào từng dòng chưa khớp để gán thủ công hoặc tạo bút toán điều chỉnh.
6. **Tạo bút toán bù** (nếu cần): các dòng có trên sao kê nhưng chưa có trong sổ sách (phí ngân hàng, lãi nhập gốc) → hệ thống gợi ý tạo bút toán bổ sung.

### Hỗ trợ import sao kê

Công cụ hỗ trợ các định dạng phổ biến:
- **CSV**: phân cách dấu phẩy hoặc tab, có dòng tiêu đề.
- **Excel (.xlsx/.xls)**: hỗ trợ cả file Excel thật và file HTML giả .xls (một số ngân hàng xuất ra HTML với đuôi .xls).
- **Tự động nhận diện cột**: hệ thống cố gắng xác định cột Ngày, Số tiền, Diễn giải dựa trên tên cột tiếng Việt/Anh.

## Định khoản tự động

Công cụ này không tự tạo bút toán, nhưng gợi ý các bút toán cần tạo:

| Trường hợp | Gợi ý bút toán |
|---|---|
| Phí ngân hàng trên sao kê nhưng chưa có trong sổ | Nợ 642x / Có 1121 |
| Lãi nhập gốc trên sao kê nhưng chưa có trong sổ | Nợ 1121 / Có 515 |
| Thu từ khách nhưng khác số tiền (chênh lệch nhỏ do phí) | Điều chỉnh thủ công |
| Chuyển khoản nội bộ giữa các TK ngân hàng | Nợ 1121-B / Có 1121-A |

## Tình huống đặc biệt & cảnh báo

- **Chênh lệch do phí ngân hàng:** khách hàng chuyển 100M, ngân hàng trừ phí 11.000đ → nhận 99.989.000đ. Hệ thống báo chênh lệch; cần tạo thêm dòng phí ngân hàng.
- **Sao kê HTML giả .xls:** Một số ngân hàng (PG Bank, ...) xuất file .xls nhưng thực chất là HTML. Hệ thống tự động phát hiện và xử lý.
- **Dung sai ngày:** Mặc định dung sai 1 ngày để khớp các giao dịch cuối ngày (ngân hàng hạch toán sáng hôm sau).
- **Số tiền khớp nhưng khác ngày > 3 ngày:** Cần xác nhận thủ công — có thể là giao dịch khác trùng số tiền.
- **Khớp sai:** Luôn kiểm tra lại các dòng đã khớp tự động trước khi xác nhận hoàn tất.

## Báo cáo liên quan

- **Sổ Tài khoản ngân hàng**: sổ chi tiết TK 112.
- **Thu ngân hàng / Chi ngân hàng**: báo cáo giao dịch ngân hàng.

## FAQ

**Q: Import file sao kê bị lỗi — làm thế nào?**
**A:** Kiểm tra định dạng file. Nếu là file Excel nhưng thực chất là HTML (đuôi .xls), hệ thống sẽ tự xử lý. Nếu vẫn lỗi, thử lưu lại file dưới dạng CSV UTF-8 từ Excel và import lại.

**Q: Có thể đối soát nhiều tài khoản ngân hàng cùng lúc không?**
**A:** Không — mỗi lần đối soát là cho 1 tài khoản ngân hàng. Chọn tài khoản trong bộ lọc, import sao kê của tài khoản đó.

**Q: Dữ liệu đối soát có lưu lại không?**
**A:** Có. Kết quả đối soát được lưu lại để tham khảo sau này và phục vụ kiểm toán.

**Q: Có hỗ trợ sao kê ngân hàng nước ngoài không?**
**A:** Có, miễn là file CSV/Excel có cấu trúc cột Ngày, Số tiền, Diễn giải. Với ngân hàng nước ngoài, có thể cần ánh xạ cột thủ công trước khi import.
