---
title: Cài đặt PAKD
order: 10
summary: Cấu hình tài khoản kế toán và quy tắc cho phương án kinh doanh (PAKD) — TK hoa hồng nội bộ, hoa hồng ngoài, phí GPVT, khấu trừ TNCN, ngày chốt và nhắc duyệt.
---

## Mục đích

**Cài đặt PAKD** khai báo các tài khoản kế toán và quy tắc cho phân hệ **Phương án kinh doanh (PAKD)** — gồm hoa hồng nhân viên kinh doanh, hoa hồng ngoài (khách giới thiệu), phí GPVT, khấu trừ thuế TNCN tại nguồn, ngày chốt hàng tháng, và hành vi nhắc/tự đăng hoa hồng khi duyệt.

Đây là nguồn quyết định TK Nợ/Có khi PAKD sinh bút toán hoa hồng — bản thân màn hình **không tạo bút toán**.

> **Lưu ý:** Mục "Cài đặt PAKD" xuất hiện ở cả phân hệ **Kho** và **Thiết lập**. Cùng một bản cấu hình — ở Thiết lập nhấn vào việc khai báo TK và quy tắc ban đầu.

## Khi nào dùng

- **Khi triển khai phân hệ PAKD:** khai đủ các TK hoa hồng, đối ứng, khấu trừ TNCN trước khi duyệt PAKD đầu tiên.
- **Khi đổi cách chi hoa hồng:** bật/tắt dùng HRMS (qua phiếu lương bổ sung) so với ghi thẳng phiếu kế toán.
- **Khi đổi tỷ lệ khấu trừ TNCN mặc định** cho hoa hồng ngoài.
- **Khi điều chỉnh ngày chốt tháng, ngưỡng màu biên lãi, hoặc nhắc duyệt.**

## Cách thực hiện

1. Mở **Cài đặt PAKD** trên menu.
2. Khai các nhóm:

**Cài đặt chung**
- *Ngày chốt hàng tháng* (mặc định 5): thanh toán nhận trước hoặc đúng ngày này được tính vào kỳ chốt tháng hiện tại.
- *Mẫu hoa hồng mặc định*: chọn một [Mẫu quy tắc hoa hồng](mau-quy-tac-hoa-hong.md).
- *Dùng HRMS để chi hoa hồng* (mặc định **tắt**): bật → chi qua phiếu lương bổ sung (cần HRMS + chọn Khoản lương kinh doanh); tắt → ghi thẳng phiếu kế toán với đối tượng = nhân viên.

**Tài khoản kế toán (hoa hồng nội bộ)**

| Ô cấu hình | TK gợi ý | Vai trò khi đăng hoa hồng |
|---|---|---|
| TK - DV quản lý | (theo công ty) | Chi phí dịch vụ quản lý |
| TK - Chi phí ngoài | (theo công ty) | Chi phí ngoài |
| TK - Phí GPVT | (theo công ty) | Phí GPVT |
| TK - Hoa hồng NVKD (chi phí) | 6427 | Nợ — chi phí hoa hồng (chỉ khi tắt HRMS) |
| TK đối ứng - Phải trả NVKD | 334 | Có — phải trả nhân viên (chỉ khi tắt HRMS) |
| TK đối ứng - Phí GPVT | 3338 | Có — phí GPVT tạm giữ để nộp NN |

**Hoa hồng ngoài (khách giới thiệu — khấu trừ TNCN tại nguồn)**

| Ô cấu hình | TK gợi ý | Vai trò |
|---|---|---|
| TK - Hoa hồng ngoài (chi phí) | 6427 | Nợ toàn bộ số gốc |
| TK đối ứng - Phải trả người ngoài | 3388 | Có phần ròng (gốc − thuế) |
| TK - Thuế TNCN tạm giữ | 3335 | Có phần thuế đã khấu trừ |
| Tỷ lệ TNCN mặc định (%) | 10% | 10% nếu người nhận có MST, 20% nếu chưa; PAKD có thể ghi đè |

**Thẻ tóm tắt & duyệt**
- *Ngưỡng biên lãi xanh/vàng* (mặc định 25% / 15%): tô màu biên lãi trên thẻ tóm tắt PAKD.
- *Tự động đăng hoa hồng khi duyệt* (mặc định **bật**): tự đăng phiếu lương bổ sung + bút toán ngay khi PAKD được duyệt; tắt để kế toán bấm "Đăng hoa hồng" thủ công.
- *Khoảng cách tối thiểu giữa 2 lần nhắc* (mặc định 24 giờ) + *Mẫu email nhắc duyệt*.

3. Lưu.

## Định khoản tự động

Màn hình này **không tự sinh bút toán** — chỉ **quyết định TK** mà nghiệp vụ "Đăng hoa hồng" của PAKD dùng. Bút toán hoa hồng (do PAKD sinh) dùng các TK ở đây:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Hoa hồng NVKD (ghi thẳng, tắt HRMS) | 6427 (chi phí HH) | 334 (phải trả NVKD) | Đối tượng = nhân viên |
| Phí GPVT tạm giữ | (theo cấu hình) | 3338 | Phí phải nộp NN |
| Hoa hồng ngoài | 6427 (chi phí) | 3388 (ròng) + 3335 (thuế TNCN) | Khấu trừ TNCN tại nguồn |

## Tình huống đặc biệt & cảnh báo

- **Tắt HRMS (mặc định DCNET):** hoa hồng ghi thẳng phiếu kế toán với đối tượng = nhân viên (TK 334). Các ô "TK Hoa hồng NVKD" và "Phải trả NVKD" chỉ dùng ở chế độ này — phải khai đủ nếu tắt HRMS.
- **Bật HRMS:** cần module HRMS và chọn "Khoản lương kinh doanh" (Salary Component) — hoa hồng đi qua phiếu lương bổ sung.
- **Khấu trừ TNCN hoa hồng ngoài:** 10% nếu người nhận có MST, 20% nếu chưa; tỷ lệ mặc định khai ở đây, PAKD từng cái có thể ghi đè.
- **Phí GPVT tạm giữ vào TK 3338** để sau nộp nhà nước — không phải doanh thu/chi phí của công ty.
- **"Tự động đăng hoa hồng khi duyệt" bật** nghĩa là bút toán phát sinh ngay lúc duyệt PAKD — đảm bảo TK đã khai đúng trước khi duyệt, tránh phải hủy bút toán.

## Báo cáo liên quan

- [Mẫu quy tắc hoa hồng](mau-quy-tac-hoa-hong.md) — định nghĩa thành phần và tỷ lệ hoa hồng.
- [Lịch sử nhắc duyệt PAKD](lich-su-nhac-duyet-pakd.md) — vết các lần nhắc duyệt.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — TK mặc định cho các phân hệ khác (độc lập với PAKD).

## FAQ

**Q: Hoa hồng PAKD lấy TK từ Cài đặt kế toán hay Cài đặt PAKD?**
**A:** Từ **Cài đặt PAKD** (màn hình này). Cài đặt kế toán không quản TK hoa hồng.

**Q: Tôi không dùng HRMS thì khai những ô nào?**
**A:** Khai "TK Hoa hồng NVKD (chi phí)" (vd 6427) và "TK đối ứng Phải trả NVKD" (vd 334). Hai ô này chỉ dùng khi tắt HRMS.

**Q: Khác nhau giữa hoa hồng NVKD và hoa hồng ngoài?**
**A:** Hoa hồng NVKD trả cho nhân viên (đối tượng = nhân viên, TK 334). Hoa hồng ngoài trả cho người giới thiệu không phải nhân viên — phải khấu trừ TNCN tại nguồn (TK 3335) và ghi phần ròng vào phải trả khác (TK 3388).

**Q: "Ngày chốt hàng tháng" để làm gì?**
**A:** Quyết định thanh toán nhận trước/đúng ngày đó được tính vào kỳ chốt tháng hiện tại — ảnh hưởng kỳ ghi nhận hoa hồng.
