---
section: Thuế
title: Tổng quan Thuế GTGT
summary: Phân hệ Thuế quản lý hóa đơn GTGT đầu vào/đầu ra, các mẫu thuế và tờ khai 01/GTGT theo TT80/2021.
---

## Mục đích

Phân hệ **Thuế** tập trung mọi nghiệp vụ liên quan đến **thuế giá trị gia tăng (GTGT)**: tiếp nhận hóa đơn điện tử đầu vào, theo dõi hóa đơn đầu ra, cấu hình các mẫu thuế (bán hàng / mua hàng / hàng hóa) và lập **Tờ khai thuế GTGT mẫu 01/GTGT**. Đối tượng sử dụng chính là kế toán thuế.

Theo VAS (TT99/2025, hiệu lực 2026-01-01):
- Thuế GTGT **đầu ra** ghi vào TK **3331** (chi tiết 33311 — thuế GTGT đầu ra hàng hóa dịch vụ; 33312 — thuế GTGT hàng nhập khẩu).
- Thuế GTGT **đầu vào được khấu trừ** ghi vào TK **1331**.

## Khi nào dùng

- Hằng ngày: tiếp nhận, kiểm tra và ghép nối hóa đơn điện tử đầu vào với hóa đơn mua hàng.
- Khi bán hàng: hệ thống tự ghi nhận thuế GTGT đầu ra (TK 3331) trên hóa đơn bán hàng theo mẫu thuế áp dụng.
- Khi cấu hình ban đầu: lập các mẫu thuế bán hàng, mua hàng và mẫu thuế cho từng nhóm hàng hóa.
- Cuối kỳ (tháng/quý): lập Tờ khai thuế GTGT 01/GTGT để kê khai với cơ quan thuế.

## Cách thực hiện

Cấu trúc menu **Thuế** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | HĐ GTGT đầu vào | Danh sách | Hóa đơn điện tử đầu vào tải về từ nhà cung cấp HĐĐT |
| 2 | HĐ GTGT đầu ra | Danh sách | Hóa đơn bán hàng (khía cạnh thuế GTGT đầu ra TK 3331) |
| 3 | Tờ khai thuế GTGT (01/GTGT) | Báo cáo | Tờ khai 01/GTGT theo TT80/2021 |
| 4 | Mẫu thuế bán hàng | Danh sách | Mẫu thuế GTGT đầu ra áp cho hóa đơn bán |
| 5 | Mẫu thuế mua hàng | Danh sách | Mẫu thuế GTGT đầu vào áp cho hóa đơn mua |
| 6 | Mẫu thuế hàng hóa | Danh sách | Mẫu thuế theo từng nhóm hàng hóa / mặt hàng |
| 7 | [Đang phát triển] Kiểm tra MST | Công cụ | Tra cứu tình trạng mã số thuế nhà cung cấp (chưa hoàn thiện) |

### Quy trình điển hình

1. **Cấu hình ban đầu:** lập các mẫu thuế bán hàng (5%, 8%, 10%), mẫu thuế mua hàng, và mẫu thuế hàng hóa cho các mặt hàng có thuế suất riêng.
2. **Hằng ngày — đầu vào:** mở **HĐ GTGT đầu vào** → kiểm tra hóa đơn mới tải về → ghép nối với hóa đơn mua hàng đã có hoặc tạo hóa đơn mua hàng mới từ hóa đơn điện tử.
3. **Hằng ngày — đầu ra:** lập hóa đơn bán hàng; mẫu thuế áp tự động tính thuế GTGT đầu ra (TK 3331).
4. **Cuối kỳ:** mở **Tờ khai thuế GTGT (01/GTGT)** → chọn kỳ (Tháng / Quý) → nhập số thuế đầu vào kỳ trước chuyển sang [30] nếu có → đối chiếu các chỉ tiêu → lập tờ khai gửi cơ quan thuế.

### Liên kết tới các bài hướng dẫn chi tiết

- **Hóa đơn:** [HĐ GTGT đầu vào](hd-gtgt-dau-vao.md), [HĐ GTGT đầu ra](hd-gtgt-dau-ra.md).
- **Tờ khai:** [Tờ khai thuế GTGT (01/GTGT)](to-khai-gtgt.md).
- **Mẫu thuế:** [Mẫu thuế bán hàng](mau-thue-ban-hang.md), [Mẫu thuế mua hàng](mau-thue-mua-hang.md), [Mẫu thuế hàng hóa](mau-thue-hang-hoa.md).
- **Công cụ:** [Kiểm tra MST](kiem-tra-mst.md).

## Định khoản tự động

Phân hệ Thuế không có chứng từ tự định khoản riêng. Thuế GTGT được sinh kèm theo chứng từ gốc:

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Bán hàng có thuế GTGT đầu ra | 131 / 111 / 112 | 511 + **3331** | Mẫu thuế bán hàng áp trên hóa đơn bán hàng |
| Mua hàng có thuế GTGT đầu vào | 152/156/642... + **1331** | 331 / 111 / 112 | Mẫu thuế mua hàng áp trên hóa đơn mua hàng |
| Khấu trừ thuế GTGT cuối kỳ | **3331** | **1331** | Bút toán kết chuyển thuế khấu trừ |
| Nộp thuế GTGT vào ngân sách | **3331** | 112 | Phiếu kế toán nộp tiền vào kho bạc |

## Tình huống đặc biệt & cảnh báo

- **Đầu vào không được khấu trừ:** hóa đơn không đủ điều kiện khấu trừ (sai sót, không phục vụ sản xuất kinh doanh) thì không ghi vào TK 1331 mà tính thẳng vào chi phí — không kê vào chỉ tiêu [31]/[32] của tờ khai.
- **Hóa đơn 0%, không kê khai:** hàng xuất khẩu thuế suất 0% (chỉ tiêu [23]) và hàng không phải kê khai tính nộp thuế (chỉ tiêu [22]) vẫn ghi nhận doanh thu nhưng không phát sinh thuế GTGT đầu ra.
- **Kỳ kê khai:** doanh nghiệp nhỏ kê khai theo **Quý**, doanh nghiệp lớn theo **Tháng** — chọn đúng "Kỳ tính thuế" khi lập tờ khai.
- **Thời hạn nộp:** kê khai theo tháng nộp chậm nhất ngày 20 tháng sau; theo quý nộp chậm nhất ngày cuối tháng đầu quý sau (TT80/2021).

## Báo cáo liên quan

- **Tờ khai thuế GTGT (01/GTGT)**: tổng hợp đầu ra/đầu vào, tính số thuế phải nộp.
- **Sổ Cái TK 3331 / TK 1331**: chi tiết phát sinh thuế đầu ra/đầu vào.
- **Bảng cân đối số phát sinh**: kiểm tra số dư TK 3331, 1331 cuối kỳ.

## FAQ

**Q: Số liệu trên Tờ khai 01/GTGT lấy từ đâu?**
**A:** Đầu ra lấy từ hóa đơn bán hàng đã ghi sổ (tài khoản thuế chứa "33311"); đầu vào lấy từ hóa đơn mua hàng đã ghi sổ (tài khoản thuế chứa "133"). Tờ khai không nhập tay phần phát sinh, chỉ nhập tay số thuế đầu vào kỳ trước chuyển sang [30].

**Q: Tờ khai theo thông tư nào?**
**A:** Mẫu 01/GTGT theo **TT80/2021** về quản lý thuế. Các tài khoản kế toán theo VAS TT99/2025 (3331 đầu ra, 1331 đầu vào).

**Q: HĐ GTGT đầu vào và HĐ GTGT đầu ra khác nhau thế nào?**
**A:** Đầu vào là hóa đơn mua hàng tải về từ nhà cung cấp HĐĐT (thuế khấu trừ TK 1331); đầu ra là hóa đơn bán hàng do doanh nghiệp xuất (thuế phải nộp TK 3331).
