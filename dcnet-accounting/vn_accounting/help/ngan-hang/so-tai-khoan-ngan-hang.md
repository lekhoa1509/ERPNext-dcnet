---
title: Sổ Tài khoản ngân hàng
order: 3
summary: Sổ kế toán chi tiết TK 112 — số dư lũy kế theo trình tự thời gian cho từng tài khoản ngân hàng.
---

## Mục đích

**Sổ Tài khoản ngân hàng** là sổ kế toán chi tiết tài khoản ngân hàng — TK 112 (1121 nội tệ, 1122 ngoại tệ). Hiển thị toàn bộ phát sinh Gửi vào/Rút ra theo trình tự thời gian và cột số dư lũy kế cho từng tài khoản ngân hàng riêng biệt.

## Khi nào dùng

- **Cuối ngày/tuần:** đối chiếu sổ với sao kê ngân hàng. Số dư cuối kỳ phải khớp với số dư trên sao kê.
- **Cuối tháng/quý/năm:** in sổ chi tiết tài khoản ngân hàng để đóng quyển và ký chữ.
- **Tra cứu chi tiết:** xem 1 dòng cụ thể → mở chứng từ gốc.
- **Đối chiếu chéo:** so sánh với báo cáo Thu ngân hàng / Chi ngân hàng cùng kỳ.

## Cách thực hiện

1. Bấm **Sổ Tài khoản ngân hàng** trên menu Ngân hàng → báo cáo Sổ Tài khoản ngân hàng mở.
2. Lọc theo:
   - **Công ty** (bắt buộc, mặc định công ty đang làm việc).
   - **Tài khoản ngân hàng** (tùy chọn — lọc theo TK 112%. Để trống để xem tất cả).
   - **Loại giao dịch** (tùy chọn): Gửi vào / Rút ra / Tất cả.
   - **Từ ngày / Đến ngày** (bắt buộc, mặc định 1 tháng gần nhất).
3. Bấm **Refresh**.
4. Bảng hiển thị theo thứ tự thời gian tăng dần (cũ trước → mới sau) với các cột:

| Cột | Mô tả |
|---|---|
| Ngày | Ngày ghi sổ |
| Số chứng từ | Link đến chứng từ gốc |
| Loại chứng từ | Bút toán / Phiếu thanh toán |
| Diễn giải | Nội dung giao dịch |
| TK đối ứng | Tài khoản đối ứng (trích từ `against` field của GL Entry) |
| Gửi vào | Số tiền gửi vào (debit TK 112) |
| Rút ra | Số tiền rút ra (credit TK 112) |
| Số dư | Số dư lũy kế tại thời điểm phát sinh |

5. Bấm vào một dòng để xem chứng từ gốc.

Báo cáo có 3 nút tạo nhanh ở góc trên: **Nhận thanh toán**, **Chi thanh toán**, và **Bút toán ngân hàng**.

### Tạo giao dịch mới

- **Nhận thanh toán**: mở biểu mẫu Phiếu thanh toán loại Thu với phương thức Chuyển khoản.
- **Chi thanh toán**: mở biểu mẫu Phiếu thanh toán loại Chi với phương thức Chuyển khoản.
- **Bút toán ngân hàng**: mở biểu mẫu Phiếu kế toán loại Bank Entry.

## Cấu trúc báo cáo

Báo cáo hiển thị:
- **Dòng số dư đầu kỳ**: số dư trước ngày bắt đầu (= tổng debit - tổng credit các TK 112% trước `from_date`).
- **Các dòng giao dịch**: mỗi dòng GL Entry có `account` khớp TK 112%, kèm số dư lũy kế (running balance). Có thể lọc theo loại "Gửi vào" hoặc "Rút ra" qua bộ lọc Loại giao dịch.
- **Dòng số dư cuối kỳ**: tổng Gửi vào, tổng Rút ra, và số dư cuối kỳ.

## Tình huống đặc biệt & cảnh báo

- **Nhiều tài khoản ngân hàng:** Mỗi tài khoản ngân hàng (VND, USD, EUR) có sổ riêng. Bộ lọc "Tài khoản ngân hàng" cho phép chọn từng TK.
- **Số dư đầu kỳ không khớp sao kê:** Kiểm tra các giao dịch cuối kỳ trước — có thể ngân hàng hạch toán lệch 1-2 ngày so với sổ sách (treasury float).
- **Ngoại tệ (TK 1122):** Chọn tài khoản 1122 để xem sổ riêng cho từng ngoại tệ; tỷ giá hiển thị theo từng dòng.
- **Số dư âm:** nếu số dư âm tại bất kỳ điểm nào, có dấu hiệu sai (quên phiếu thu hoặc phiếu chi thừa). Đối chiếu chéo với báo cáo Thu ngân hàng và Chi ngân hàng.
- **Đối soát sao kê:** Sử dụng công cụ Đối soát sao kê để tự động khớp từng dòng giữa sổ sách và file sao kê ngân hàng.

## Báo cáo liên quan

- **Thu ngân hàng**: chỉ riêng phát sinh Gửi vào.
- **Chi ngân hàng**: chỉ riêng phát sinh Rút ra.
- **Đối soát sao kê**: công cụ đối chiếu tự động.
- **Bảng cân đối số phát sinh**: tổng phát sinh và số dư TK 112 cuối kỳ.
- **Sổ cái kế toán**: chi tiết hơn (gồm tất cả TK).

## FAQ

**Q: Sao kê ngân hàng khác số dư sổ sách 1-2 ngày — xử lý thế nào?**
**A:** Khoảng lệch 1-2 ngày là bình thường (treasury float) — do ngân hàng hạch toán chậm hơn giao dịch thực tế. Đối chiếu theo ngày phát sinh thực tế, không theo ngày ngân hàng ghi nhận. Công cụ Đối soát sao kê có cài đặt "dung sai ngày" để khớp tự động.

**Q: Có thể xem đồng thời tất cả tài khoản ngân hàng không?**
**A:** Có — để trống bộ lọc "Tài khoản ngân hàng" để xem tổng hợp tất cả TK 112.

**Q: Tại sao cột tiền ghi là "Gửi vào" / "Rút ra" thay vì "Nợ" / "Có"?**
**A:** Đây là cách gọi thân thiện với người dùng ngân hàng. "Gửi vào" = debit TK 112 (tiền vào tài khoản), "Rút ra" = credit TK 112 (tiền ra khỏi tài khoản). Về bản chất kế toán vẫn là Nợ/Có.

**Q: Có thể lọc chỉ xem giao dịch gửi vào hoặc rút ra không?**
**A:** Có. Sử dụng bộ lọc "Loại giao dịch" → chọn "Gửi vào" hoặc "Rút ra". Để trống để xem tất cả.
