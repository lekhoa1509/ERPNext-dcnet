---
section: Hợp đồng
title: Hình thức thanh toán
summary: Giải thích 3 chế độ Prepay / Monthly / OneOff với ví dụ thực tế.
---

## 3 chế độ thanh toán

| Chế độ | Khi nào dùng | Lịch thu tiền |
|---|---|---|
| **Prepay** | Thu trước kỳ. Khách trả tiền tháng X vào đầu tháng X. | Mỗi kỳ có ngày đến hạn = ngày đầu kỳ |
| **Monthly** | Thu sau kỳ. Khách trả tiền tháng X vào cuối tháng X hoặc đầu tháng X+1. | Mỗi kỳ có ngày đến hạn = ngày cuối kỳ |
| **OneOff** | Thu 1 lần khi giao hàng/thi công xong. CHỈ áp dụng cho HĐ One-off. | 1 kỳ duy nhất khi kích hoạt |

## Ví dụ — HĐ Recurring, Thời hạn 12 tháng, Đơn giá 5tr/tháng, Phí lắp đặt 2tr

### Prepay
- Kỳ 0 (phí lắp đặt): 2.000.000 ₫, đến hạn ngày kích hoạt
- Kỳ 1 (T1): 5.000.000 ₫, đến hạn 01/T1
- Kỳ 2 (T2): 5.000.000 ₫, đến hạn 01/T2
- ...
- Tổng giá trị HĐ = 12 × 5tr + 2tr = 62.000.000 ₫

### Monthly
- Kỳ 0 (phí lắp đặt): 2.000.000 ₫, đến hạn ngày kích hoạt
- Kỳ 1 (T1): 5.000.000 ₫, đến hạn cuối T1
- Kỳ 2 (T2): 5.000.000 ₫, đến hạn cuối T2
- ...

### OneOff (cho HĐ One-off)
- Chỉ 1 kỳ duy nhất: tổng giá trị HĐ, đến hạn ngày nghiệm thu
- Không nhân với chu kỳ — Phí lắp đặt cộng trực tiếp vào tổng

## Lưu ý

- **Phí lắp đặt** (`setup_fee`) là khoản thu **1 lần** khi kích hoạt — KHÔNG nhân với chu kỳ
- Đổi `payment_mode` sau khi đã sinh Lịch thu tiền sẽ **không tự cập nhật** Lịch — phải huỷ và sinh lại
