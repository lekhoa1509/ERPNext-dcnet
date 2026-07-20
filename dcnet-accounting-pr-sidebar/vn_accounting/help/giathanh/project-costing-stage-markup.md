---
title: 6 phương pháp markup cho giai đoạn
section: Giá thành
doctype: Project Costing Stage
---

# 6 phương pháp markup cho giai đoạn

Mỗi giai đoạn của công trình chọn 1 trong 6 phương pháp tính giá xuất hóa đơn. Trong cùng 1 công trình, các giai đoạn có thể dùng phương pháp khác nhau.

## Bảng 6 phương pháp

| # | Phương pháp | Công thức | Khi dùng |
|---|---|---|---|
| 1 | **Hệ số** (Coefficient) | `chi_phí × hệ_số` (vd 1.5) | Công trình đơn giản, biên lợi nhuận chuẩn |
| 2 | **% trên chi phí** (Percent on Cost) | `chi_phí × (1 + %)` (vd +30%) | KTT nghĩ theo % thay vì hệ số |
| 3 | **Số tiền cố định** (Fixed Amount) | KTT input số tiền | Có thỏa thuận cứng, không phụ thuộc chi phí |
| 4 | **Theo HĐ / phụ lục** (From Contract) | KTT input số tiền lấy từ hợp đồng | HĐ khung ghi sẵn giá mỗi mốc |
| 5 | **% trên giá trị HĐ khung** (Percent of Contract) | `HĐ_value × %` | Tạm ứng theo % HĐ (vd 30% trước khởi công) |
| 6 | **% trên cost đã phát sinh + uplift** (Cost-to-Date Uplift) | `cost_to_date × (1 + %)` | Nghiệm thu giữa kỳ — theo tiến độ chi phí thực |

## Ví dụ cho 1 công trình HĐ khung 300 triệu

| Giai đoạn | Phương pháp | Markup value | Giá đề xuất |
|---|---|---|---|
| Tạm ứng 30% | % trên HĐ khung | 30 | 90.000.000 |
| Thi công + nghiệm thu giữa (cost đã pin = 100tr) | % trên cost + uplift | 25 | 125.000.000 |
| Nghiệm thu cuối | Theo HĐ / phụ lục | 85.000.000 | 85.000.000 |
| | | **Tổng** | **300.000.000** |

## Giá KTT chốt vs Giá đề xuất

Hệ thống tự động tính **Giá đề xuất** theo công thức. KTT có thể **override** bằng cách điền số tiền khác vào ô **Giá KTT chốt** trên form Giai đoạn.

Audit trail tự ghi: ai override, khi nào, lý do (KTT điền vào ô **Lý do override**).

## Trường hợp đặc biệt

**Markup âm (giá < chi phí):** hệ thống cảnh báo nhưng KHÔNG block. KTT có thể bypass với lý do (vd: bán lỗ để giành thầu).

**Markup = 0 (cost-only):** cho phép (vd: HĐ phụ kiện không lãi).

**Stage tạm ứng đầu (cost = 0):** Phương pháp #3, #4, hoặc #5 vẫn ra giá xuất HĐ bình thường. Lúc đó báo cáo lãi/lỗ stage tạm ứng = giá HĐ - 0 = giá HĐ (chưa có cost thực).

**"Theo HĐ" nhưng cost > giá HĐ (over-budget):** hiển thị cảnh báo đỏ. KTT có thể (a) chấp nhận lỗ, (b) đàm phán phụ lục tăng giá rồi update markup_value, (c) di chuyển cost sang giai đoạn sau.

## Cấu hình markup mặc định cho công trình

Trên form **Công trình & Giá thành** → trường **Phương pháp markup mặc định** → chọn 1 trong 6 phương pháp. Mọi giai đoạn mới tạo sẽ kế thừa giá trị này (có thể đổi sau).
