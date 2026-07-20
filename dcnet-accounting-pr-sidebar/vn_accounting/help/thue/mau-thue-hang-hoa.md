---
title: Mẫu thuế hàng hóa
order: 6
summary: Gắn thuế suất GTGT riêng cho từng nhóm hàng hóa / mặt hàng có thuế suất khác mức chung.
---

## Mục đích

**Mẫu thuế hàng hóa** dùng để gán **thuế suất GTGT riêng cho từng mặt hàng** khi các mặt hàng trên cùng một hóa đơn có thuế suất khác nhau (ví dụ một hóa đơn vừa có hàng 10% vừa có hàng 5%). Mẫu này gắn vào mặt hàng (hoặc nhóm hàng) trong danh mục; khi mặt hàng đó lên hóa đơn, hệ thống áp đúng thuế suất của mặt hàng thay vì thuế suất chung của mẫu thuế bán/mua.

## Khi nào dùng

- Khi doanh nghiệp kinh doanh nhiều mặt hàng có thuế suất GTGT khác nhau.
- Khi một hóa đơn chứa cả hàng chịu thuế 10% và hàng chịu thuế 5% (hoặc 0%, không chịu thuế).
- Khi cần ghi đè thuế suất chung của mẫu thuế bán/mua cho riêng một mặt hàng.

## Cách thực hiện

1. Mở **Mẫu thuế hàng hóa** trên menu Thuế → danh sách các mẫu.
   ![Danh sách mẫu thuế hàng hóa](_images/mau-thue-hang-hoa-1.png)
2. Bấm **+ Thêm** để tạo mẫu mới.
3. Nhập **Tên mẫu** (ví dụ "Hàng chịu thuế 5%") và **Công ty**.
4. Trong bảng thuế, với mỗi loại thuế thêm dòng:
   - **Tài khoản thuế**: tài khoản thuế đầu ra (33311) và/hoặc đầu vào (133) tương ứng.
   - **Thuế suất (%)**: thuế suất riêng của mặt hàng.
5. Lưu, rồi gán mẫu này vào mặt hàng trong **danh mục hàng hóa** (mục "Thuế" trên mặt hàng). Từ đó, mọi hóa đơn chứa mặt hàng sẽ áp đúng thuế suất.

## Định khoản tự động

Mẫu thuế hàng hóa là cấu hình, không tự định khoản. Khi mặt hàng có mẫu thuế riêng lên hóa đơn và ghi sổ:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Bán mặt hàng gắn mẫu thuế 5% | 131 | 511 + **33311** (5%) | Ghi đè thuế suất chung của hóa đơn |
| Mua mặt hàng gắn mẫu thuế 5% | 152/156... + **1331** (5%) | 331 | Ghi đè thuế suất chung của hóa đơn |

## Tình huống đặc biệt & cảnh báo

- **Ghi đè thuế suất chung:** thuế suất trên mẫu thuế hàng hóa **ưu tiên** hơn thuế suất chung của mẫu thuế bán/mua đối với mặt hàng được gắn — dùng để xử lý hóa đơn nhiều thuế suất.
- **Tài khoản đúng chiều:** nếu mặt hàng dùng cho cả bán và mua, cấu hình tài khoản đầu ra (33311) cho chiều bán và đầu vào (133) cho chiều mua.
- **Chỉ dùng khi cần:** nếu toàn bộ mặt hàng cùng một thuế suất, không cần mẫu thuế hàng hóa — dùng mẫu thuế bán/mua chung là đủ.
- **Kiểm tra tổng hợp tờ khai:** thuế suất gắn theo mặt hàng vẫn phải trỏ tài khoản chứa "33311"/"133" để vào đúng chỉ tiêu tờ khai.

## Báo cáo liên quan

- **Mẫu thuế bán hàng**: thuế suất chung áp toàn hóa đơn bán.
- **Mẫu thuế mua hàng**: thuế suất chung áp toàn hóa đơn mua.
- **Tờ khai thuế GTGT (01/GTGT)**: tổng hợp doanh thu và thuế theo từng thuế suất.

## FAQ

**Q: Khi nào cần mẫu thuế hàng hóa?**
**A:** Khi các mặt hàng có thuế suất GTGT khác nhau trên cùng hóa đơn. Nếu mọi mặt hàng cùng thuế suất, chỉ cần mẫu thuế bán/mua chung.

**Q: Mẫu thuế hàng hóa và mẫu thuế bán/mua, cái nào thắng?**
**A:** Mẫu thuế hàng hóa gắn theo mặt hàng sẽ ghi đè thuế suất chung cho riêng mặt hàng đó trên hóa đơn.

**Q: Gắn mẫu thuế hàng hóa ở đâu?**
**A:** Trong danh mục hàng hóa, mở mặt hàng và chọn mẫu thuế ở mục thuế của mặt hàng.
