---
section: Hợp đồng
title: Lịch thu tiền
summary: Lịch thu tiền — cách sinh ra, 6 trạng thái dòng, khi nào xuất hoá đơn.
---

## Cách sinh ra

Lịch thu tiền (`billing_schedule`) được sinh tự động khi Hợp đồng được **Submit** (chuyển từ Bản nháp sang Đang hoạt động). Quy tắc sinh:

```
Số kỳ = package_term_months (Recurring) hoặc 1 (One-off)
Ngày đến hạn = Ngày kích hoạt + offset theo payment_mode
Số tiền mỗi kỳ = unit_price_total (cố định, không nhân thuế)
Kỳ 0 (nếu setup_fee > 0) = setup_fee
```

Mỗi dòng tương ứng **1 hoá đơn dự kiến** sẽ xuất.

## 6 trạng thái dòng

Màu nền của mỗi dòng cho biết trạng thái:

| Trạng thái | Màu | Ý nghĩa |
|---|---|---|
| **Projected** | Xám nhạt | Kỳ chưa tới hạn, chưa xuất hoá đơn |
| **Invoiced** | Xanh dương | Đã xuất hoá đơn, chờ thu tiền |
| **Paid** | Xanh lá | Đã thu đủ tiền |
| **Overdue** | Đỏ | Đã xuất hoá đơn, quá hạn, chưa thu đủ |
| **Cancelled** | Xám | Đã huỷ (HĐ huỷ giữa kỳ) |
| **Written Off** | Cam | Đã ghi nợ khó đòi |

## Vòng đời 1 dòng điển hình

```
Projected → (xuất hoá đơn) → Invoiced → (thu đủ tiền) → Paid
                                      ↘ (quá hạn) → Overdue → (thu đủ) → Paid
                                                          ↘ (ghi nợ) → Written Off
```

## Khi nào xuất hoá đơn

Hệ thống KHÔNG tự xuất hoá đơn. Kế toán phải:

1. Mở danh sách Hợp đồng → lọc trạng thái "Đang hoạt động"
2. Mở từng HĐ → xem dòng Projected sắp tới hạn
3. Click vào dòng → tạo Sales Invoice (hoặc dùng utility tạo hàng loạt nếu có)
4. Submit Sales Invoice → trạng thái dòng tự cập nhật thành "Invoiced"

Để tránh quên: dùng sidebar item **Kỳ thu tiền quá hạn** (báo cáo) để quét hằng tuần.

## Khi huỷ HĐ giữa kỳ

- Kỳ **Projected** → tự chuyển thành Cancelled
- Kỳ **Invoiced/Overdue** (đã xuất hoá đơn nhưng chưa thu) → tự sinh **Credit Note** (giấy báo có) + đánh dấu Cancelled
- Kỳ **Paid** (đã thu) → **không tự refund** — chỉ cảnh báo, kế toán xử lý refund thủ công nếu cần
