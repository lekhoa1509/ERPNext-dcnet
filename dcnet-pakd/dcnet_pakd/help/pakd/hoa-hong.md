---
section: PAKD
title: Quy trình hoa hồng
summary: Hoa hồng tính như thế nào — Dòng hoa hồng, Lương bổ sung, khi nào chi trả qua HRMS.
---

## Vòng đời hoa hồng

```
PAKD Bản nháp → Chờ duyệt (4 bước) → Đã duyệt
                                          ↓
                                  Sinh Dòng hoa hồng
                                          ↓
                                  Tạo Lương bổ sung (Additional Salary)
                                          ↓
                                  Chi trả qua HRMS Payroll
```

## Dòng hoa hồng (commission_lines)

Khi PAKD được **Đã duyệt**, hệ thống tự sinh `commission_lines`:

- 1 dòng cho mỗi (kỳ thu tiền × thành phần chi phí)
- Thành phần: DV quản lý / Chi phí ngoài / Phí GPVT / Hoa hồng NVKD
- Mỗi dòng có `state` = "Pending" (chờ thu tiền), "Eligible" (đã thu, sẵn sàng chi), "Paid" (đã chi)

## Tổng DT dịch vụ (total_revenue_service)

Công thức:

```
DT dịch vụ = DT HĐ − Phí GPVT − DV quản lý
```

Đây là **doanh thu ròng** dùng để tính:

- **Biên lãi** = (DT dịch vụ − Tổng chi phí) / DT dịch vụ
- **Hoa hồng NVKD** = f(DT dịch vụ, channel, rule template)

DT dịch vụ KHÔNG bao gồm:

- Chi phí ngoài (phí vận chuyển, thi công ngoài)
- Phí GPVT (đã trừ — là chi phí chính phủ)
- DV quản lý (đã trừ — chi cho cấp quản lý nội bộ)

## Lương bổ sung (Additional Salary)

- Bản ghi HRMS sinh ra cùng lúc PAKD được Duyệt
- Tham chiếu Employee = NVKD ký HĐ
- Salary Component = **Lương KD** (cấu hình ở PAKD Settings)
- Số tiền = Tổng hoa hồng NVKD
- Payroll Entry tháng kế tiếp sẽ tự include khoản này

## Khi nào commission posts tự động vs thủ công

Xem **PAKD Settings > commission_post_on_approval**:

- **Bật (mặc định)**: tự đăng AS + JE ngay khi Duyệt
- **Tắt**: nút **Đăng hoa hồng** xuất hiện trên thẻ Tóm tắt; kế toán bấm để đăng

Tắt chế độ tự động hữu ích khi cần kiểm soát thời điểm hạch toán (ví dụ: chỉ đăng khi đã thu tiền).
