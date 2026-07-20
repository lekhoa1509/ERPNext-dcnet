---
title: HĐ GTGT đầu ra
order: 2
summary: Hóa đơn bán hàng nhìn từ khía cạnh thuế GTGT đầu ra (TK 3331) phục vụ kê khai.
---

## Mục đích

**HĐ GTGT đầu ra** liệt kê các **hóa đơn bán hàng** đã lập, nhìn dưới góc độ **thuế GTGT đầu ra** (TK **3331**). Đây là nguồn số liệu cho phần B của Tờ khai 01/GTGT. Mục này dùng chung chứng từ hóa đơn bán hàng với phân hệ Bán hàng — tại đây kế toán thuế tập trung theo dõi thuế suất, tiền thuế đầu ra và tính hợp lệ của hóa đơn để kê khai.

> Hướng dẫn lập và quản lý hóa đơn bán hàng đầy đủ (doanh thu, công nợ, xuất hóa đơn điện tử) xem trong phân hệ **Bán hàng** › Hóa đơn bán hàng. Trang này chỉ làm rõ khía cạnh **thuế GTGT đầu ra**.

## Khi nào dùng

- Theo dõi thuế GTGT đầu ra phát sinh trong kỳ theo từng thuế suất (5%, 8%, 10%).
- Đối chiếu tổng thuế đầu ra với chỉ tiêu [29] trên Tờ khai 01/GTGT.
- Rà soát hóa đơn bán hàng trước khi khóa sổ kê khai thuế.
- Kiểm tra hóa đơn xuất khẩu 0% và hàng không phải kê khai tính nộp thuế.

## Cách thực hiện

1. Bấm **HĐ GTGT đầu ra** trên menu Thuế → danh sách hóa đơn bán hàng.
   ![Danh sách HĐ GTGT đầu ra](_images/hd-gtgt-dau-ra-1.png)
2. Lọc theo công ty và khoảng ngày (ngày ghi sổ); xem các cột tổng tiền, thuế.
3. Mở từng hóa đơn để xem dòng thuế (thuế suất, tài khoản thuế chứa "33311", tiền thuế).
4. Để xem tổng hợp theo thuế suất phục vụ kê khai, mở [Tờ khai thuế GTGT (01/GTGT)](to-khai-gtgt.md).

## Định khoản tự động

Khi **ghi sổ** một hóa đơn bán hàng có thuế GTGT, hệ thống tự sinh bút toán thuế đầu ra:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Bán hàng/dịch vụ chịu thuế 10% | 131 / 111 / 112 | 511 + **33311** (10%) | Mẫu thuế bán hàng 10% |
| Bán hàng/dịch vụ chịu thuế 5% | 131 / 111 / 112 | 511 + **33311** (5%) | Mẫu thuế bán hàng 5% |
| Bán hàng/dịch vụ chịu thuế 8% | 131 / 111 / 112 | 511 + **33311** (8%) | Theo chính sách giảm thuế từng thời kỳ |
| Xuất khẩu thuế suất 0% | 131 | 511 | Không phát sinh thuế đầu ra; vào [23] |
| Hàng không phải kê khai tính nộp thuế | 131 | 511 | Vào [22] |
| Hàng bán bị trả lại (điều chỉnh giảm) | 511 + **33311** | 131 | Giảm thuế đầu ra, vào [26b] |

## Tình huống đặc biệt & cảnh báo

- **Tài khoản thuế đầu ra:** tờ khai chỉ nhận hóa đơn có tài khoản thuế chứa **"33311"** (thuế GTGT đầu ra hàng hóa dịch vụ). Mẫu thuế bán hàng phải trỏ đúng tài khoản này, nếu không số liệu sẽ không vào tờ khai.
- **Điều chỉnh kỳ trước:** hàng bán trả lại (hóa đơn trả hàng) làm **giảm** thuế đầu ra [26b]; hóa đơn điều chỉnh tăng (debit note) làm **tăng** [26a].
- **Hóa đơn nháp không tính:** chỉ hóa đơn **đã ghi sổ** mới vào tờ khai. Hóa đơn còn nháp chưa phát sinh thuế.
- **Thuế suất 8%:** áp dụng theo chính sách giảm thuế GTGT từng giai đoạn — kiểm tra thời điểm hiệu lực trước khi lập mẫu thuế 8%.
- **Hóa đơn điện tử:** việc xuất hóa đơn điện tử (ký số, gửi cơ quan thuế) được xử lý ở luồng hóa đơn bán hàng — xem phân hệ Bán hàng.

## Báo cáo liên quan

- **HĐ GTGT đầu vào**: hóa đơn mua hàng (thuế khấu trừ TK 1331).
- **Tờ khai thuế GTGT (01/GTGT)**: tổng hợp thuế đầu ra theo thuế suất (chỉ tiêu [22]–[29]).
- **Mẫu thuế bán hàng**: cấu hình thuế suất và tài khoản 33311 áp cho hóa đơn bán.
- **Sổ Cái TK 33311**: chi tiết phát sinh thuế đầu ra.

## FAQ

**Q: Hóa đơn bán hàng đã có ở Bán hàng, sao lại có ở Thuế?**
**A:** Cùng một chứng từ, hai góc nhìn. Phân hệ Bán hàng quản lý toàn bộ vòng đời hóa đơn (doanh thu, công nợ, xuất HĐĐT); phân hệ Thuế chỉ tập trung khía cạnh thuế GTGT đầu ra để kê khai 01/GTGT.

**Q: Vì sao một hóa đơn không xuất hiện trong tờ khai?**
**A:** Thường do (1) hóa đơn còn nháp chưa ghi sổ, hoặc (2) tài khoản thuế trên mẫu thuế bán hàng không chứa "33311". Kiểm tra hai điểm này.

**Q: Hàng bán trả lại kê khai thế nào?**
**A:** Hóa đơn trả hàng làm giảm thuế đầu ra, được đưa vào chỉ tiêu điều chỉnh giảm [26b] của tờ khai.
