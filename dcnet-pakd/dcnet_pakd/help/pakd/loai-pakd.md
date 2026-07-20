---
section: PAKD
title: Loại PAKD
summary: 3 loại PAKD với ví dụ tính toán cho mỗi loại.
---

## 3 loại PAKD

### 1. Recurring Telecom

Cho HĐ định kỳ telecom: P2P, MPLS, ILL, FTTH DN, IT Managed.

- **1 PAKD cho cả vòng đời HĐ** (không lập lại hàng tháng)
- Doanh thu = `qty × unit_price` cho mỗi hạng mục
- Tổng DT HĐ = doanh thu/kỳ × thời hạn gói

**Ví dụ:** HĐ ILL 100Mbps, đơn giá 5tr/tháng, thời hạn 12 tháng
- DT HĐ = 5tr × 12 = 60.000.000 ₫
- Chi phí ngoài, GPVT, DV quản lý: tính theo công thức nội bộ
- Hoa hồng NVKD: theo channel + doanh thu dịch vụ

### 2. Monthly FTTH Rollup

Cho HĐ FTTH hộ gia đình (FTTH HGD).

- **Lập mới mỗi tháng** — gộp doanh thu thực tế của nhiều hộ
- Doanh thu = **revenue_actual** (doanh thu thực tế tháng) — KHÔNG dùng qty × unit_price
- Hệ số lương (salary_coefficient) áp dụng cho dòng hoa hồng

**Ví dụ:** PAKD tháng 5/2026 — gộp 200 hộ FTTH HGD
- Mỗi dòng có revenue_actual riêng (thu tiền tháng 5 từ hộ đó)
- Tổng DT PAKD = ΣΣ revenue_actual

### 3. One-off Sale/Project

Cho HĐ VTTB hoặc Thi công.

- **1 PAKD cho 1 HĐ** — duyệt 1 lần, đăng hoa hồng 1 lần
- Doanh thu = qty × unit_price
- Có thể có chi phí ngoài lớn (vận chuyển, thi công thuê ngoài)

**Ví dụ:** HĐ VTTB cung cấp 10 router 1tr/cái
- DT HĐ = 10 × 1tr = 10.000.000 ₫
- Chi phí ngoài: phí vận chuyển 500k
- Hoa hồng NVKD: theo channel + DT dịch vụ ròng
