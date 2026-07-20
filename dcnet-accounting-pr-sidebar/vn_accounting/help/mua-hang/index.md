---
section: Mua hàng
title: Tổng quan Mua hàng
summary: Giới thiệu phân hệ Mua hàng — từ đơn mua hàng, nhập kho, hóa đơn mua hàng đến công nợ phải trả và các báo cáo phân tích.
---

## Mục đích

Phân hệ **Mua hàng** quản lý toàn bộ chu trình mua: lập **đơn mua hàng** gửi nhà cung cấp → **nhập kho** hàng về → ghi nhận **hóa đơn mua hàng** (công nợ phải trả + thuế GTGT đầu vào) → theo dõi **công nợ phải trả** và phân tích chi tiêu. Menu bên trái gom các chứng từ nhập liệu và các báo cáo tra cứu liên quan đến mua hàng và công nợ NCC.

## Khi nào dùng

- Khi đặt mua hàng/dịch vụ: lập đơn mua hàng để theo dõi cam kết với nhà cung cấp.
- Khi hàng về kho: lập phiếu nhập kho (nếu là hàng tồn kho cần theo dõi số lượng).
- Khi nhận hóa đơn: lập hóa đơn mua hàng để ghi nhận công nợ phải trả (TK 331) và thuế GTGT đầu vào (TK 1331).
- Định kỳ: theo dõi công nợ phải trả, đôn đốc lấy hóa đơn VAT, phân tích chi tiêu mua hàng.

## Cách thực hiện

Cấu trúc menu **Mua hàng** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Đơn mua hàng | Danh sách | Toàn bộ đơn mua hàng đặt NCC |
| 2 | Đơn mua hàng cần lập hóa đơn | Danh sách | Đơn mua đã nhận hàng nhưng chưa có hóa đơn (lọc "To Bill") |
| 3 | Hoá đơn mua hàng | Danh sách | Hóa đơn mua — ghi nhận công nợ + thuế đầu vào |
| 4 | Nhập kho mua hàng | Danh sách | Phiếu nhập kho hàng mua về |
| 5 | Điều khoản thanh toán | Danh sách | Mẫu kỳ hạn thanh toán cho NCC/khách hàng |
| 6 | Công nợ phải trả | Báo cáo | Chi tiết công nợ TK 331 theo NCC, tuổi nợ |
| 7 | Bảng tổng hợp công nợ NCC | Báo cáo | Tổng hợp số dư phải trả theo NCC |
| 8 | BC mua hàng | Báo cáo | Phân tích mua hàng theo NCC/mặt hàng/kỳ |
| 9 | BC theo mặt hàng | Báo cáo | Sổ chi tiết mua theo từng mặt hàng |
| 10 | Bút toán chung | Danh sách | Phiếu kế toán điều chỉnh, kết chuyển công nợ |
| 11 | Mua không VAT | Báo cáo | Hóa đơn mua chưa nhận hóa đơn VAT điện tử từ NCC |

### Quy trình điển hình

1. **Đặt mua:** lập **đơn mua hàng** (mục Đơn mua hàng → "+ Thêm"), gửi NCC. Đơn mua hàng KHÔNG sinh bút toán.
2. **Nhận hàng:** từ đơn mua hàng bấm "Tạo > Phiếu nhập kho", hoặc lập **nhập kho mua hàng** trực tiếp. Nếu là hàng tồn kho, phiếu nhập kho ghi tăng kho (Dr 152/153/156) đối ứng TK chờ nhận hóa đơn (TK 3388/151).
3. **Nhận hóa đơn:** từ đơn mua hàng hoặc phiếu nhập kho bấm "Tạo > Hóa đơn mua hàng" để kế thừa dòng hàng; hoặc mở mục **Đơn mua hàng cần lập hóa đơn** để thấy đơn nào còn thiếu hóa đơn. Hóa đơn mua hàng ghi công nợ phải trả (Cr 331) + thuế GTGT đầu vào (Dr 1331).
4. **Theo dõi & thanh toán:** xem **Công nợ phải trả** để biết tuổi nợ; thanh toán bằng phiếu thanh toán (từ hóa đơn mua hàng bấm "Tạo > Phiếu thanh toán").
5. **Định kỳ:** chạy **Mua không VAT** đôn đốc NCC giao hóa đơn; xem **BC mua hàng** / **BC theo mặt hàng** để phân tích chi tiêu.

### Liên kết tới các bài hướng dẫn chi tiết

- **Chứng từ nhập liệu**: [Đơn mua hàng](don-mua-hang.md), [Hóa đơn mua hàng](hoa-don-mua-hang.md), [Nhập kho mua hàng](nhap-kho-mua-hang.md), [Điều khoản thanh toán](dieu-khoan-thanh-toan.md), [Bút toán chung](but-toan-chung.md).
- **Báo cáo công nợ**: [Công nợ phải trả](cong-no-phai-tra.md), [Bảng tổng hợp công nợ NCC](tong-hop-cong-no-ncc.md).
- **Báo cáo phân tích**: [BC mua hàng](bc-mua-hang.md), [BC theo mặt hàng](bc-theo-mat-hang.md), [Mua không VAT](mua-khong-vat.md).

## Định khoản tự động

Đơn mua hàng và điều khoản thanh toán **không sinh bút toán**. Hai chứng từ sinh bút toán khi ghi sổ:

| Chứng từ | Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|---|
| Nhập kho mua hàng | Nhận hàng tồn kho trước hóa đơn | 152/153/156 | 3388 / 151 | Chờ nhận hóa đơn (TK 151 "Hàng mua đang đi đường") |
| Hóa đơn mua hàng | Mua hàng tồn kho (đã có nhập kho) | 151 (tất toán) + 1331 | 331 | Khớp với phiếu nhập kho |
| Hóa đơn mua hàng | Mua hàng/dịch vụ không qua kho | 152/153/156/211/242/627/641/642 + 1331 | 331 | Tùy bản chất chi phí |

Số hiệu TK theo TT99/2025: TK 1331 = thuế GTGT đầu vào, TK 331 = phải trả người bán, TK 151 = hàng mua đang đi đường.

## Tình huống đặc biệt & cảnh báo

- **Hàng về trước hóa đơn:** lập nhập kho mua hàng trước, hóa đơn mua hàng sau và khớp với phiếu nhập kho để tránh ghi tăng kho hai lần.
- **Mua không có hóa đơn VAT:** dùng báo cáo [Mua không VAT](mua-khong-vat.md) để rà soát và đòi hóa đơn từ NCC trước hạn kê khai thuế.
- **Mục "Đơn mua hàng cần lập hóa đơn"** chỉ là danh sách Đơn mua hàng lọc theo trạng thái "To Bill / To Receive and Bill" — cùng dữ liệu với "Đơn mua hàng", không phải chứng từ riêng.
- **Phòng ban đề xuất:** field "Phòng ban đề xuất" trên đơn mua hàng/hóa đơn mua hàng (FB-2026-00616) tự kế thừa khi tạo hóa đơn từ đơn mua hàng; phục vụ quản trị nội bộ và giải trình thanh tra.
- **Ghi giảm/điều chỉnh công nợ:** dùng phiếu kế toán (Bút toán chung) hoặc Credit Note (hóa đơn trả lại) khi NCC giảm giá/trả hàng.

## Báo cáo liên quan

- **Công nợ phải trả**: chi tiết tuổi nợ TK 331 theo NCC.
- **Bảng tổng hợp công nợ NCC**: tổng hợp số dư phải trả.
- **BC mua hàng / BC theo mặt hàng**: phân tích chi tiêu.
- **Bảng cân đối số phát sinh** (phân hệ Tổng hợp): kiểm tra phát sinh và số dư TK 331, 1331.

## FAQ

**Q: Đơn mua hàng có ghi sổ kế toán không?**
**A:** Không. Đơn mua hàng chỉ là cam kết đặt mua, không sinh bút toán. Bút toán phát sinh khi lập phiếu nhập kho (ghi tăng kho) và hóa đơn mua hàng (ghi công nợ + thuế đầu vào).

**Q: Sao có hai mục "Đơn mua hàng" và "Đơn mua hàng cần lập hóa đơn"?**
**A:** Cùng một loại chứng từ. Mục thứ hai chỉ lọc sẵn các đơn ở trạng thái "cần lập hóa đơn" (đã nhận hàng nhưng chưa ghi nhận hóa đơn) để kế toán dễ theo dõi việc hoàn thiện chứng từ.

**Q: Khi nào cần phiếu nhập kho, khi nào chỉ cần hóa đơn mua hàng?**
**A:** Hàng tồn kho cần theo dõi số lượng (vật tư, hàng hóa) nên lập phiếu nhập kho. Dịch vụ, chi phí mua ngoài không qua kho thì chỉ cần hóa đơn mua hàng (tích "Cập nhật tồn kho" hoặc để hệ thống ghi thẳng chi phí).
