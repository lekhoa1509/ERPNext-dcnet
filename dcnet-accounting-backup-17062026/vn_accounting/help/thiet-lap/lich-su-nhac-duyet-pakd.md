---
title: Lịch sử nhắc duyệt PAKD
order: 12
summary: Nhật ký các lần gửi nhắc duyệt phương án kinh doanh — ghi người gửi, thời điểm, trạng thái duyệt và người nhận.
---

## Mục đích

**Lịch sử nhắc duyệt PAKD** là nhật ký (chỉ đọc, do hệ thống ghi) lưu vết mỗi lần gửi nhắc duyệt một phương án kinh doanh đang chờ duyệt. Dùng để kiểm soát tần suất nhắc và phục vụ truy vết khi PAKD chậm được duyệt.

> **Lưu ý:** Mục này xuất hiện ở cả phân hệ **Kho** và **Thiết lập**. Cùng một nhật ký.

## Khi nào dùng

- **Khi PAKD chờ duyệt lâu:** xem đã nhắc ai, lúc nào.
- **Khi kiểm soát chống spam nhắc:** đối chiếu với "Khoảng cách tối thiểu giữa 2 lần nhắc" trong [Cài đặt PAKD](cai-dat-pakd.md).
- **Khi rà soát quy trình duyệt:** thống kê thời gian chờ duyệt.

## Cách thực hiện

1. Mở **Lịch sử nhắc duyệt PAKD** trên menu — danh sách các bản ghi nhắc.
2. Mỗi bản ghi gồm:
   - **PAKD** được nhắc.
   - **Trạng thái duyệt tại thời điểm gửi** (workflow state).
   - **Người gửi** và **Thời điểm gửi**.
   - **Người nhận** (danh sách).
3. Bản ghi do hệ thống tự tạo khi gửi nhắc — người dùng thường chỉ tra cứu, không nhập tay.

## Định khoản tự động

Nhật ký này **không sinh bút toán** — chỉ ghi vết hoạt động nhắc duyệt.

## Tình huống đặc biệt & cảnh báo

- **Đây là dữ liệu hệ thống ghi tự động** — không sửa/tạo thủ công để giữ tính chính xác của vết.
- **Khoảng cách nhắc tối thiểu** do [Cài đặt PAKD](cai-dat-pakd.md) quy định (mặc định 24 giờ): hệ thống chặn nhắc lại quá sớm từ cùng một người cho cùng một PAKD.
- **Nội dung email nhắc** lấy từ mẫu trong Cài đặt PAKD (biến: tên PAKD, đường dẫn, khách hàng, doanh thu, số ngày chờ, người nhắc).

## Báo cáo liên quan

- [Cài đặt PAKD](cai-dat-pakd.md) — cấu hình tần suất + mẫu email nhắc.
- [Mẫu quy tắc hoa hồng](mau-quy-tac-hoa-hong.md).

## FAQ

**Q: Vì sao tôi không nhắc lại được PAKD vừa nhắc?**
**A:** Hệ thống áp khoảng cách tối thiểu giữa 2 lần nhắc (mặc định 24 giờ) cho cùng người + cùng PAKD. Chờ hết khoảng đó hoặc nhờ người khác nhắc.

**Q: Tôi có cần tạo bản ghi nhắc thủ công không?**
**A:** Không. Bản ghi tự sinh khi gửi nhắc. Màn hình này để tra cứu.

**Q: Xem được PAKD nào chờ duyệt lâu nhất không?**
**A:** Lọc/sắp xếp theo thời điểm gửi và đối chiếu trạng thái duyệt; số ngày chờ cũng có trong nội dung email nhắc.
