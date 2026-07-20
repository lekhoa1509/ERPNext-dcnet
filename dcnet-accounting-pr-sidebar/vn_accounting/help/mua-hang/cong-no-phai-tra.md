---
title: Công nợ phải trả
order: 5
summary: Báo cáo chi tiết công nợ phải trả người bán (TK 331) theo nhà cung cấp và tuổi nợ.
---

## Mục đích

Báo cáo **Công nợ phải trả** liệt kê chi tiết số tiền còn phải trả nhà cung cấp (TK 331) theo từng hóa đơn/chứng từ, phân tích **tuổi nợ** (quá hạn bao nhiêu ngày) và số dư đến ngày báo cáo. Dùng để lập kế hoạch thanh toán, kiểm soát hạn trả và đối chiếu công nợ với NCC. Đây là báo cáo chuẩn của hệ thống ERP, chỉ tra cứu — không nhập liệu, không sinh bút toán.

## Khi nào dùng

- Định kỳ (tuần/cuối tháng): rà soát công nợ sắp đến hạn và quá hạn để lên kế hoạch chi.
- Đối chiếu công nợ với NCC trước khi thanh toán hoặc cuối kỳ.
- Kiểm tra tuổi nợ để đánh giá rủi ro/áp lực thanh toán.

## Cách thực hiện

1. Bấm **Công nợ phải trả** trên menu Mua hàng → báo cáo mở.
2. Hệ thống tự đặt sẵn **Loại đối tượng = Nhà cung cấp** (Supplier) cho báo cáo này.
3. Nhập điều kiện lọc: **Công ty**, **Ngày báo cáo** (tính số dư đến ngày này), **Nhà cung cấp** (tùy chọn), các mốc tuổi nợ (30/60/90 ngày...).
4. Bấm **Refresh** → bảng hiển thị từng chứng từ phải trả: NCC, ngày hóa đơn, ngày đến hạn, số tiền, đã trả, còn lại, số ngày quá hạn và phân bổ theo cột tuổi nợ.
5. Bấm vào dòng để mở chứng từ gốc (hóa đơn mua hàng / phiếu kế toán) xem chi tiết.

## Định khoản tự động

Báo cáo này **không sinh bút toán** — chỉ tổng hợp số liệu từ Sổ Cái TK 331. Số liệu phản ánh:

- Phát sinh Có 331 từ hóa đơn mua hàng / phiếu kế toán ghi công nợ.
- Phát sinh Nợ 331 từ phiếu thanh toán / Credit Note làm giảm nợ.
- Số dư còn lại theo từng hóa đơn đến ngày báo cáo.

## Tình huống đặc biệt & cảnh báo

- **Loại đối tượng tự đặt Nhà cung cấp:** báo cáo này dùng chung khung với Công nợ phải thu; hệ thống tự đặt "Nhà cung cấp" để tránh hiện nhầm khách hàng (FB-2026-00616). Nếu thấy trống, kiểm tra lại bộ lọc Loại đối tượng.
- **Tuổi nợ tính theo ngày đến hạn:** nếu hóa đơn không gắn [điều khoản thanh toán](dieu-khoan-thanh-toan.md), ngày đến hạn có thể bằng ngày ghi sổ → công nợ "quá hạn" sai. Gắn mẫu kỳ hạn để tuổi nợ chính xác.
- **Tạm ứng/đặt cọc cho NCC:** khoản trả trước (Nợ 331 hoặc TK 331 dư Nợ) có thể hiện số âm — đối chiếu với phiếu thanh toán đặt cọc.
- **Ngoại tệ:** công nợ NCC ngoại tệ quy đổi theo tỷ giá; chênh lệch đánh giá lại cuối kỳ ghi TK 413/635/515.

## Báo cáo liên quan

- [Bảng tổng hợp công nợ NCC](tong-hop-cong-no-ncc.md) — số dư tổng hợp theo NCC (không chi tiết từng hóa đơn).
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — chứng từ phát sinh công nợ.
- [Điều khoản thanh toán](dieu-khoan-thanh-toan.md) — cơ sở tính ngày đến hạn/tuổi nợ.
- Bảng cân đối số phát sinh (phân hệ Tổng hợp) — kiểm tra tổng số dư TK 331.

## FAQ

**Q: Đây là báo cáo của hệ thống ERP — số liệu lấy từ đâu?**
**A:** Từ Sổ Cái TK 331 (phải trả người bán), gom theo từng chứng từ phải trả và tính tuổi nợ. Báo cáo chỉ tra cứu, không cho tạo/sửa chứng từ trực tiếp.

**Q: Vì sao "Loại đối tượng" mặc định là Nhà cung cấp?**
**A:** Báo cáo này phục vụ công nợ phải trả nên hệ thống tự đặt Loại đối tượng = Nhà cung cấp. Việc này tránh phải chọn tay và tránh hiện nhầm khách hàng.

**Q: Công nợ quá hạn báo sai (đến hạn = ngày ghi sổ) thì sửa thế nào?**
**A:** Gắn [điều khoản thanh toán](dieu-khoan-thanh-toan.md) cho hóa đơn để tự tính ngày đến hạn, hoặc sửa trực tiếp ngày đến hạn trên lịch thanh toán của hóa đơn.
