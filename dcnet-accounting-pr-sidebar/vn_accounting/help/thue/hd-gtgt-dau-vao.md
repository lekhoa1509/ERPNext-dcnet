---
title: HĐ GTGT đầu vào
order: 1
summary: Tiếp nhận hóa đơn điện tử đầu vào tải về từ nhà cung cấp HĐĐT, ghép nối hoặc tạo hóa đơn mua hàng.
---

## Mục đích

**HĐ GTGT đầu vào** là nơi tiếp nhận và xử lý các **hóa đơn điện tử đầu vào** (hóa đơn mua hàng) mà hệ thống tự động tải về từ nhà cung cấp dịch vụ hóa đơn điện tử (HĐĐT). Đây là bản nháp trung gian (staging) — kế toán kiểm tra rồi **ghép nối** với hóa đơn mua hàng đã có, hoặc **tạo mới** hóa đơn mua hàng từ dữ liệu hóa đơn. Mục tiêu là không bỏ sót hóa đơn đầu vào và đảm bảo thuế GTGT đầu vào (TK 1331) được kê khai khấu trừ đầy đủ.

## Khi nào dùng

- Hằng ngày: kiểm tra các hóa đơn điện tử đầu vào mới về, đối chiếu với chứng từ thực nhận.
- Khi đã có hóa đơn mua hàng nhập tay: **ghép nối** hóa đơn điện tử với hóa đơn mua hàng đó để gắn mã tra cứu.
- Khi chưa có hóa đơn mua hàng: **tạo hóa đơn mua hàng** trực tiếp từ hóa đơn điện tử.
- Khi hóa đơn không liên quan (sai đối tượng, trùng): **bỏ qua** hóa đơn.

## Cách thực hiện

1. Bấm **HĐ GTGT đầu vào** trên menu Thuế → danh sách hóa đơn điện tử đầu vào.
   ![Danh sách HĐ GTGT đầu vào](_images/hd-gtgt-dau-vao-1.png)
2. Lọc theo **Trạng thái** (Mới / Đã ghép / Đã tạo hóa đơn / Bỏ qua / Lỗi) và theo công ty.
3. Mở một hóa đơn để xem chi tiết: nhà cung cấp, mã số thuế, số hóa đơn, ngày lập, dòng hàng hóa, tổng trước thuế, thuế suất, tiền thuế.
4. Chọn cách xử lý:
   - **Ghép nối**: bấm nút ghép → chọn hóa đơn mua hàng đã có → hệ thống gắn `mã tra cứu` và liên kết hai chứng từ, chuyển trạng thái sang **Đã ghép**.
   - **Tạo hóa đơn mua hàng**: bấm nút tạo → hệ thống lập một hóa đơn mua hàng nháp (Draft) với nhà cung cấp (tự tìm theo MST hoặc tạo mới), một dòng hàng theo tổng trước thuế, và áp **mẫu thuế mua hàng** khớp thuế suất. Sau đó kế toán kiểm tra và ghi sổ (submit).
   - **Bỏ qua**: bấm bỏ qua → trạng thái chuyển **Bỏ qua**.

### Tự khớp mẫu thuế

Khi tạo hóa đơn mua hàng, hệ thống tự tìm **mẫu thuế mua hàng** của công ty có thuế suất khớp với thuế suất trên hóa đơn điện tử (loại "On Net Total"). Nếu tìm thấy đúng 1 mẫu → áp ngay; nếu nhiều mẫu khớp → ưu tiên mẫu mặc định; nếu không khớp → dùng mẫu mặc định kèm cảnh báo "Vui lòng kiểm tra".

## Định khoản tự động

Bản thân màn hình HĐ GTGT đầu vào **không tự định khoản** — nó chỉ tạo ra hóa đơn mua hàng (ở trạng thái nháp). Định khoản phát sinh khi kế toán **ghi sổ** hóa đơn mua hàng đó:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Mua hàng/dịch vụ có thuế GTGT đầu vào | 152/153/156/642... + **1331** | 331 (NCC) | Thuế khấu trừ ghi TK 1331 theo mẫu thuế mua hàng |
| Thuế đầu vào không được khấu trừ | tính thẳng vào chi phí/giá trị tài sản | 331 | Không ghi TK 1331, không kê tờ khai |

## Tình huống đặc biệt & cảnh báo

- **Đối chiếu thuế:** khi tạo hóa đơn mua hàng, hệ thống so sánh tiền thuế tính theo mẫu với tiền thuế trên hóa đơn điện tử; chênh lệch quá 1% sẽ cảnh báo — kiểm tra lại thuế suất hoặc số tiền.
- **Hóa đơn nháp cần ghi sổ:** hóa đơn mua hàng tạo ra ở trạng thái **nháp (Draft)** — chưa phát sinh Sổ Cái/thuế đầu vào cho tới khi được ghi sổ (submit). Đừng quên bước này, nếu không tờ khai sẽ thiếu thuế đầu vào.
- **Nhà cung cấp tự tạo:** nếu MST nhà cung cấp chưa có trong danh mục, hệ thống tự tạo nhà cung cấp mới theo tên + MST trên hóa đơn — nên kiểm tra lại thông tin sau đó.
- **Trùng hóa đơn:** mỗi hóa đơn điện tử có `ID trên hệ thống provider` và `mã tra cứu` riêng để chống trùng; nếu thấy 2 dòng cùng số hóa đơn, kiểm tra trước khi xử lý.
- **Chưa có dữ liệu:** màn hình này phụ thuộc kết nối tới nhà cung cấp HĐĐT. Nếu chưa cấu hình provider hoặc chưa đến kỳ tải, danh sách sẽ trống.

## Báo cáo liên quan

- **HĐ GTGT đầu ra**: hóa đơn bán hàng (thuế đầu ra TK 3331).
- **Tờ khai thuế GTGT (01/GTGT)**: chỉ tiêu [31]/[32] lấy thuế đầu vào từ hóa đơn mua hàng đã ghi sổ.
- **Mẫu thuế mua hàng**: mẫu áp khi tạo hóa đơn mua hàng từ hóa đơn điện tử.

## FAQ

**Q: Hóa đơn điện tử đầu vào lấy từ đâu?**
**A:** Hệ thống tự động tải về từ nhà cung cấp dịch vụ HĐĐT đã cấu hình (theo MST của doanh nghiệp). Mỗi hóa đơn được lưu thành một bản nháp trung gian để kế toán xử lý.

**Q: Ghép nối khác tạo hóa đơn mua hàng thế nào?**
**A:** Ghép nối dùng khi đã nhập tay hóa đơn mua hàng — chỉ gắn mã tra cứu và liên kết. Tạo hóa đơn mua hàng dùng khi chưa có — hệ thống lập một hóa đơn mua hàng nháp mới từ dữ liệu hóa đơn điện tử.

**Q: Vì sao thuế tính ra khác với thuế trên hóa đơn?**
**A:** Mẫu thuế mua hàng tính lại thuế trên giá trị chưa thuế; nếu nhà cung cấp làm tròn khác, sẽ có chênh lệch nhỏ. Hệ thống cảnh báo khi chênh lệch trên 1% — kiểm tra thuế suất của mẫu đang áp.

**Q: Tạo hóa đơn mua hàng xong thì thuế đầu vào đã được khấu trừ chưa?**
**A:** Chưa — hóa đơn mua hàng ở trạng thái nháp. Phải **ghi sổ (submit)** hóa đơn đó thì TK 1331 mới phát sinh và mới vào tờ khai 01/GTGT.
