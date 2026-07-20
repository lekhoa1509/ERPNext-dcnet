---
title: Mẫu thuế mua hàng
order: 5
summary: Cấu hình mẫu thuế GTGT đầu vào (TK 1331) áp tự động lên hóa đơn mua hàng.
---

## Mục đích

**Mẫu thuế mua hàng** định nghĩa cách tính **thuế GTGT đầu vào được khấu trừ** áp lên hóa đơn mua hàng và đơn mua hàng. Mỗi mẫu chứa một dòng thuế "Trên giá trị thuần" với thuế suất 5%/8%/10% trỏ tới **tài khoản thuế đầu vào TK 1331** (133). Mẫu này còn được hệ thống dùng để **tự khớp** khi tạo hóa đơn mua hàng từ hóa đơn điện tử đầu vào.

## Khi nào dùng

- Cấu hình ban đầu: lập mẫu thuế đầu vào cho từng thuế suất doanh nghiệp gặp khi mua hàng.
- Khi tiếp nhận hóa đơn điện tử đầu vào: hệ thống tự chọn mẫu khớp thuế suất để áp lên hóa đơn mua hàng tạo mới.
- Khi cần mẫu mặc định để áp nhanh trên hóa đơn mua.

## Cách thực hiện

1. Mở **Mẫu thuế mua hàng** trên menu Thuế → danh sách các mẫu.
   ![Danh sách mẫu thuế mua hàng](_images/mau-thue-mua-hang-1.png)
2. Bấm **+ Thêm** để tạo mẫu mới.
3. Nhập:
   - **Tên mẫu**: ví dụ "GTGT đầu vào 10%".
   - **Công ty**: công ty áp dụng.
   - **Mặc định**: đánh dấu nếu là mẫu áp tự động.
4. Trong bảng thuế, thêm dòng:
   - **Loại tính**: chọn **Trên giá trị thuần** (On Net Total).
   - **Tài khoản thuế**: chọn tài khoản chứa **133** (thuế GTGT đầu vào được khấu trừ — TK 1331).
   - **Thuế suất (%)**: nhập 5 / 8 / 10.
5. Lưu. Mẫu sẵn sàng để áp tay trên hóa đơn mua hoặc để hệ thống tự khớp khi xử lý hóa đơn điện tử đầu vào.

## Định khoản tự động

Mẫu thuế là cấu hình, không tự định khoản. Bút toán phát sinh khi **ghi sổ hóa đơn mua hàng** có áp mẫu:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Hóa đơn mua áp mẫu thuế 10% | 152/156/642... + **1331** | 331 (NCC) | Thuế khấu trừ = giá trị thuần × 10% |

## Tình huống đặc biệt & cảnh báo

- **Tài khoản phải chứa "133":** Tờ khai 01/GTGT nhận diện thuế đầu vào qua tài khoản chứa "133". Mẫu trỏ sai tài khoản → thuế đầu vào không vào chỉ tiêu [31]/[32].
- **Tự khớp theo thuế suất:** khi tạo hóa đơn mua hàng từ hóa đơn điện tử đầu vào, hệ thống tìm mẫu mua hàng có thuế suất khớp; nếu công ty **chưa có mẫu nào** sẽ báo lỗi yêu cầu tạo mẫu. Vì vậy phải lập sẵn các mẫu thuế mua hàng.
- **Nhiều mẫu cùng thuế suất:** nếu có nhiều mẫu khớp, hệ thống ưu tiên mẫu **mặc định** — nên chỉ định rõ một mẫu mặc định.
- **Không khớp thuế suất:** nếu không có mẫu đúng thuế suất, hệ thống dùng mẫu mặc định kèm cảnh báo — kế toán phải kiểm tra lại.
- **Thuế đầu vào không khấu trừ:** với hóa đơn không đủ điều kiện khấu trừ, không dùng mẫu trỏ TK 1331 mà tính thẳng vào chi phí.

## Báo cáo liên quan

- **HĐ GTGT đầu vào**: hóa đơn điện tử đầu vào dùng mẫu này khi tạo hóa đơn mua hàng.
- **Mẫu thuế bán hàng**: mẫu tương ứng cho thuế đầu ra.
- **Mẫu thuế hàng hóa**: gắn thuế suất theo từng mặt hàng mua.
- **Tờ khai thuế GTGT (01/GTGT)**: tổng hợp thuế đầu vào (chỉ tiêu [31]/[32]).

## FAQ

**Q: Vì sao tạo hóa đơn mua hàng từ hóa đơn điện tử báo lỗi "chưa có mẫu thuế"?**
**A:** Công ty chưa có mẫu thuế mua hàng nào. Hãy lập trước ít nhất các mẫu 5%, 8%, 10% và một mẫu mặc định.

**Q: Hệ thống chọn mẫu nào khi tạo hóa đơn từ hóa đơn điện tử?**
**A:** Mẫu có thuế suất khớp với thuế suất trên hóa đơn điện tử; nếu nhiều mẫu khớp thì ưu tiên mẫu mặc định; nếu không khớp thì dùng mặc định kèm cảnh báo.

**Q: Thuế đầu vào không được khấu trừ thì làm sao?**
**A:** Không áp mẫu trỏ TK 1331 — tính thẳng vào chi phí hoặc giá trị tài sản; khoản này không kê vào tờ khai.
