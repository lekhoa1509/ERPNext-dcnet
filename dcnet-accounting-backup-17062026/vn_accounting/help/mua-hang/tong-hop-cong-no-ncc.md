---
title: Bảng tổng hợp công nợ NCC
order: 6
summary: Tổng hợp số dư phải trả theo từng nhà cung cấp — một dòng một NCC, gom theo tuổi nợ.
---

## Mục đích

**Bảng tổng hợp công nợ NCC** tổng hợp số dư phải trả người bán (TK 331) theo từng nhà cung cấp — mỗi NCC một dòng, kèm phân bổ theo các mốc tuổi nợ. Khác với báo cáo chi tiết, bảng này không liệt kê từng hóa đơn mà cho cái nhìn nhanh "tổng còn nợ ai bao nhiêu". Đây là báo cáo chuẩn của hệ thống ERP, chỉ tra cứu.

## Khi nào dùng

- Cuối tháng/quý: nhìn tổng quan tổng nợ phải trả theo từng NCC để ưu tiên thanh toán.
- Khi cần báo cáo nhanh số dư công nợ cho ban giám đốc.
- Khi đối chiếu tổng số dư TK 331 trên Bảng cân đối với chi tiết theo NCC.

## Cách thực hiện

1. Bấm **Bảng tổng hợp công nợ NCC** trên menu Mua hàng → báo cáo mở.
2. Hệ thống tự đặt **Loại đối tượng = Nhà cung cấp** (Supplier).
3. Nhập **Công ty**, **Ngày báo cáo**, mốc tuổi nợ.
4. Bấm **Refresh** → mỗi dòng là một NCC với tổng còn phải trả và phân bổ theo cột tuổi nợ (chưa đến hạn / quá hạn 30 / 60 / 90+ ngày).
5. Cần xem chi tiết từng hóa đơn của một NCC → mở [Công nợ phải trả](cong-no-phai-tra.md) và lọc theo NCC đó.

## Định khoản tự động

Báo cáo **không sinh bút toán** — tổng hợp số dư TK 331 theo NCC từ Sổ Cái.

## Tình huống đặc biệt & cảnh báo

- **Chỉ tổng hợp, không chi tiết:** cần truy ra hóa đơn cụ thể thì sang [Công nợ phải trả](cong-no-phai-tra.md).
- **Loại đối tượng tự đặt Nhà cung cấp** (FB-2026-00616) — nếu trống, kiểm tra bộ lọc.
- **NCC có dư Nợ (trả trước):** hiển thị số âm hoặc ở cột riêng; đối chiếu các phiếu đặt cọc/tạm ứng.
- **Tuổi nợ phụ thuộc ngày đến hạn:** gắn [điều khoản thanh toán](dieu-khoan-thanh-toan.md) để mốc tuổi nợ chính xác.

## Báo cáo liên quan

- [Công nợ phải trả](cong-no-phai-tra.md) — chi tiết từng hóa đơn theo NCC.
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — chứng từ phát sinh công nợ.
- Bảng cân đối số phát sinh (phân hệ Tổng hợp) — kiểm tra tổng số dư TK 331.

## FAQ

**Q: Khác gì với "Công nợ phải trả"?**
**A:** Bảng tổng hợp gom mỗi NCC một dòng (tổng số dư). "Công nợ phải trả" liệt kê chi tiết từng hóa đơn. Xem tổng quan dùng bảng tổng hợp; truy chi tiết dùng báo cáo chi tiết.

**Q: Tổng của bảng này có khớp số dư TK 331 trên Bảng cân đối không?**
**A:** Có, đến cùng ngày báo cáo và cùng công ty, tổng còn phải trả phải khớp số dư Có TK 331 trên Bảng cân đối số phát sinh. Nếu lệch, kiểm tra phiếu kế toán ghi 331 không qua hóa đơn hoặc bút toán ngoại tệ.
