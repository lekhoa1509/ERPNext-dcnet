---
title: Mẫu thuế bán hàng
order: 4
summary: Cấu hình mẫu thuế GTGT đầu ra (TK 3331) áp tự động lên hóa đơn bán hàng.
---

## Mục đích

**Mẫu thuế bán hàng** định nghĩa cách tính **thuế GTGT đầu ra** áp lên hóa đơn bán hàng và đơn bán hàng. Mỗi mẫu chứa một hay nhiều dòng thuế (thường là một dòng "Trên giá trị thuần" với thuế suất 5%/8%/10%) trỏ tới **tài khoản thuế đầu ra TK 33311**. Khi lập hóa đơn bán hàng, kế toán chọn mẫu thuế phù hợp để hệ thống tự tính tiền thuế.

## Khi nào dùng

- Cấu hình ban đầu: lập các mẫu thuế đầu ra cho từng thuế suất doanh nghiệp sử dụng (0%, 5%, 8%, 10%).
- Khi có chính sách thuế mới (ví dụ giảm thuế GTGT về 8%): tạo thêm mẫu tương ứng.
- Khi cần một mẫu mặc định để áp nhanh trên hóa đơn bán.

## Cách thực hiện

1. Mở **Mẫu thuế bán hàng** trên menu Thuế → danh sách các mẫu.
   ![Danh sách mẫu thuế bán hàng](_images/mau-thue-ban-hang-1.png)
2. Bấm **+ Thêm** để tạo mẫu mới.
3. Nhập:
   - **Tên mẫu**: ví dụ "GTGT đầu ra 10%".
   - **Công ty**: công ty áp dụng.
   - **Mặc định**: đánh dấu nếu là mẫu áp tự động khi lập hóa đơn.
4. Trong bảng thuế, thêm dòng:
   - **Loại tính** (charge type): chọn **Trên giá trị thuần** (On Net Total).
   - **Tài khoản thuế**: chọn tài khoản chứa **33311** (thuế GTGT đầu ra hàng hóa dịch vụ).
   - **Thuế suất (%)**: nhập 5 / 8 / 10.
5. Lưu. Khi lập hóa đơn bán hàng, chọn mẫu này ở mục thuế để tự tính tiền thuế đầu ra.

## Định khoản tự động

Mẫu thuế không tự định khoản — nó là cấu hình. Bút toán phát sinh khi **ghi sổ hóa đơn bán hàng** có áp mẫu:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Hóa đơn bán áp mẫu thuế 10% | 131 / 111 / 112 | 511 + **33311** | Tiền thuế = giá trị thuần × 10% |

## Tình huống đặc biệt & cảnh báo

- **Tài khoản phải chứa "33311":** Tờ khai 01/GTGT chỉ nhận diện thuế đầu ra qua tài khoản chứa chuỗi "33311". Nếu mẫu trỏ sai tài khoản, doanh thu và thuế sẽ không vào tờ khai.
- **Loại tính phải là "Trên giá trị thuần":** dùng đúng loại để thuế tính trên giá chưa thuế, khớp cách kê khai.
- **Một mẫu cho mỗi thuế suất:** không gộp nhiều thuế suất vào một mẫu — tạo mẫu riêng cho 5%, 8%, 10% để tổng hợp tờ khai chính xác.
- **Thuế 0% / không kê khai:** với hàng xuất khẩu 0% hoặc không phải kê khai tính nộp thuế, lập mẫu thuế suất 0% hoặc để hóa đơn không có thuế tùy nghiệp vụ.
- **Mẫu mặc định:** mỗi công ty nên có một mẫu mặc định để giảm thao tác chọn tay.

## Báo cáo liên quan

- **HĐ GTGT đầu ra**: hóa đơn bán hàng áp mẫu thuế này.
- **Mẫu thuế mua hàng**: mẫu tương ứng cho thuế đầu vào.
- **Mẫu thuế hàng hóa**: gắn thuế suất theo từng mặt hàng.
- **Tờ khai thuế GTGT (01/GTGT)**: tổng hợp thuế đầu ra theo thuế suất.

## FAQ

**Q: Lập mấy mẫu thuế bán hàng là đủ?**
**A:** Tùy thuế suất doanh nghiệp sử dụng — thường 10% (phổ biến), 5%, 8% (theo chính sách giảm thuế), và 0% (xuất khẩu). Mỗi thuế suất một mẫu.

**Q: Vì sao hóa đơn bán không vào tờ khai dù đã áp mẫu thuế?**
**A:** Kiểm tra tài khoản thuế của mẫu có chứa "33311" không, và hóa đơn đã ghi sổ chưa.

**Q: Mẫu thuế bán hàng và mẫu thuế hàng hóa khác nhau thế nào?**
**A:** Mẫu thuế bán hàng áp cho cả hóa đơn; mẫu thuế hàng hóa gắn thuế suất riêng cho từng mặt hàng (khi các mặt hàng trên cùng hóa đơn có thuế suất khác nhau).
