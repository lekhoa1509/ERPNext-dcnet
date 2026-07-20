---
title: Thanh lý tài sản
order: 6
summary: Phiếu thanh lý/nhượng bán tài sản — xóa sổ qua TK 811/214, ghi nhận thu nhập bán qua TK 711.
---

## Mục đích

**Thanh lý tài sản** xử lý tài sản hết giá trị sử dụng (loại bỏ) hoặc bán/nhượng bán. Phiếu tự khấu hao bổ sung đến ngày thanh lý, sinh bút toán xóa sổ tài sản (kết chuyển hao mòn lũy kế TK 2141 + giá trị còn lại TK 811, xóa nguyên giá TK 211). Với hình thức bán, hệ thống còn tạo hóa đơn bán hàng ghi nhận thu nhập (TK 711).

## Khi nào dùng

- Tài sản hết khấu hao, hư hỏng không sửa được → loại bỏ (Scrap).
- Bán/nhượng bán tài sản cho khách → bán (Sell).
- Cần ghi nhận lỗ thanh lý (giá trị còn lại chưa khấu hao hết) hoặc thu nhập từ bán tài sản.

## Cách thực hiện

1. Bấm **Thanh lý tài sản** trên menu TSCĐ → danh sách phiếu thanh lý mở. Bấm "+ Thêm".
2. Chọn **Tài sản** (chỉ hiện tài sản đã ghi sổ, chưa bán/loại bỏ). Hệ thống tự lấy nguyên giá, hao mòn lũy kế, giá trị còn lại và các tài khoản (TK nguyên giá, TK hao mòn từ Loại tài sản; TK 811/711 từ Cài đặt).
3. Chọn **Ngày thanh lý** (không được ở tương lai, không trước ngày mua) và **Hình thức**:
   - **Scrap (loại bỏ)** — chỉ xóa sổ.
   - **Sell (bán)** — nhập thêm **Số tiền bán** và **Người mua** (khách hàng).
4. Ghi **Lý do thanh lý** và thành phần hội đồng thanh lý (bảng Participants) nếu cần.
5. Bấm nút **Execute (Thực thi)** → xác nhận. Hệ thống: (a) khấu hao bổ sung đến ngày thanh lý, (b) tạo và ghi sổ bút toán xóa sổ, (c) đổi trạng thái tài sản (Sold/Scrapped), (d) với hình thức bán: tạo hóa đơn bán hàng (nháp) cho người mua.
6. Phiếu chuyển trạng thái "Executed"; số phiếu kế toán và hóa đơn bán hàng lưu ở phần Tham chiếu.

## Định khoản tự động

Bút toán xóa sổ tài sản (tạo và ghi sổ tự động khi Thực thi):

| Vế | Tài khoản | Số tiền | Ghi chú |
|---|---|---|---|
| Nợ | 2141 (hao mòn lũy kế) | Hao mòn lũy kế | Kết chuyển hao mòn đã trích |
| Nợ | 811 (chi phí khác) | Giá trị còn lại | Lỗ thanh lý — phần chưa khấu hao hết |
| Có | 211 (nguyên giá) | Nguyên giá (tổng chi phí tài sản) | Xóa nguyên giá khỏi sổ |

Với hình thức **bán**, ngoài bút toán xóa sổ, hệ thống tạo **hóa đơn bán hàng** (nháp):

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Thu nhập bán tài sản | 131 | 711 | Hóa đơn bán hàng — số tiền bán; kế toán ghi sổ hóa đơn để hoàn tất |

> TK 811 (chi phí thanh lý) và TK 711 (thu nhập thanh lý) lấy từ **Cài đặt VN Accounting** (mục Asset Disposal). TK nguyên giá (211) và hao mòn (2141) lấy từ **Loại tài sản** của tài sản. Kế toán có thể chỉnh trên phiếu trước khi thực thi.

## Tình huống đặc biệt & cảnh báo

- **Hóa đơn bán hàng tạo ở dạng nháp:** khi bán, hệ thống tạo hóa đơn bán hàng nhưng **chưa ghi sổ** — kế toán phải mở hóa đơn và ghi sổ để ghi nhận thu nhập (Nợ 131 / Có 711) và thuế GTGT đầu ra nếu có. Hóa đơn dùng một mặt hàng dịch vụ chung "Asset Disposal Income" (không phải mã tài sản).
- **Khấu hao bổ sung đến ngày thanh lý:** với tài sản chưa khấu hao hết, hệ thống tự trích khấu hao thêm đến ngày thanh lý trước khi tính giá trị còn lại → đảm bảo lỗ thanh lý (TK 811) chính xác.
- **Ngưỡng duyệt thanh lý:** thanh lý ≥ ngưỡng (mặc định 50 triệu) cần được duyệt — cấu hình trong Cài đặt VN Accounting.
- **Hủy thanh lý khôi phục tài sản:** phiếu đã thực thi có thể hủy (nút Cancel Disposal). Với hình thức bán, **phải hủy hóa đơn bán hàng trước** rồi mới hủy được phiếu. Khi hủy: tài sản trả lại trạng thái cũ, bút toán xóa sổ bị hủy, lịch khấu hao được khôi phục.
- **Tài sản đã bán/loại bỏ không thanh lý lại:** phiếu kiểm tra trạng thái tài sản; tài sản đã Sold/Scrapped/Capitalized sẽ bị từ chối.

## Báo cáo liên quan

- **Sổ Cái:** kiểm tra bút toán xóa sổ (TK 2141, 811, 211) và thu nhập bán (TK 711).
- **Sổ S21-DN:** tài sản đã thanh lý (Scrapped) bị loại khỏi sổ TSCĐ.
- **Hóa đơn bán hàng:** chứng từ ghi nhận thu nhập khi bán tài sản.

## FAQ

**Q: Bán tài sản mà sao thu nhập chưa lên sổ?**
**A:** Hệ thống tạo hóa đơn bán hàng ở dạng **nháp**. Mở hóa đơn đó (link ở phần Tham chiếu của phiếu thanh lý) và **ghi sổ** để ghi nhận Nợ 131 / Có 711 + thuế GTGT đầu ra. Đây là bước thủ công có chủ đích để kế toán kiểm tra thuế trước khi phát hành.

**Q: Tài sản đã khấu hao hết (giá trị còn lại = 0) thì bút toán thế nào?**
**A:** Khi giá trị còn lại = 0, không phát sinh dòng Nợ TK 811. Bút toán chỉ còn Nợ TK 2141 (toàn bộ hao mòn) / Có TK 211 (nguyên giá) — cân bằng, không có lỗ thanh lý.

**Q: Thanh lý nhầm thì sửa được không?**
**A:** Được. Bấm **Cancel Disposal** trên phiếu đã thực thi. Nếu là bán, hủy hóa đơn bán hàng trước. Hệ thống khôi phục trạng thái tài sản, hủy bút toán xóa sổ và khôi phục lịch khấu hao.
