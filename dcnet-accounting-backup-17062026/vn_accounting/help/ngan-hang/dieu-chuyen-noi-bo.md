---
title: Điều chuyển nội bộ
order: 5
summary: Báo cáo tổng hợp các giao dịch điều chuyển tiền giữa các tài khoản tiền mặt (111) và ngân hàng (112) trong cùng công ty.
---

## Mục đích

Báo cáo **Điều chuyển nội bộ** tổng hợp tất cả giao dịch chuyển tiền giữa các tài khoản tiền mặt (TK 111%) và ngân hàng (TK 112%) trong cùng một công ty. Hệ thống phát hiện điều chuyển nội bộ bằng cách tìm các phiếu kế toán có đồng thời dòng Nợ và dòng Có đều thuộc nhóm tài khoản tiền mặt/ngân hàng — bao gồm cả chuyển tiền mặt↔ngân hàng, ngân hàng↔ngân hàng, và tiền mặt↔tiền mặt.

## Khi nào dùng

- Chuyển tiền từ tài khoản VND sang tài khoản USD (mua ngoại tệ) trong cùng hoặc khác ngân hàng.
- Chuyển tiền từ tài khoản thanh toán sang tài khoản tiền gửi có kỳ hạn.
- Chuyển tiền từ ngân hàng A sang ngân hàng B (cùng chủ tài khoản, khác ngân hàng).
- Rút tiền từ ngân hàng về quỹ tiền mặt (TK 1121 → 1111) hoặc nộp tiền mặt vào ngân hàng (1111 → 1121).
- Chuyển tiền giữa các quỹ tiền mặt (1111-A → 1111-B).
- Theo dõi tất cả luồng tiền nội bộ giữa các tài khoản tiền mặt và ngân hàng.

## Cách thực hiện

1. Bấm **Điều chuyển nội bộ** trên menu Ngân hàng → báo cáo Điều chuyển nội bộ mở.
2. Lọc theo: **Công ty** (bắt buộc), **Từ ngày / Đến ngày** (bắt buộc). Báo cáo tự động quét tất cả các TK 111% và 112% — không có bộ lọc riêng cho từng tài khoản.
3. Bấm **Refresh**. Bảng hiển thị các lần điều chuyển với các cột:

| Cột | Mô tả |
|---|---|
| Ngày | Ngày ghi sổ |
| Số chứng từ | Link đến chứng từ gốc |
| Loại chứng từ | Bút toán / Phiếu thanh toán |
| Diễn giải | Nội dung giao dịch |
| TK chuyển | Tài khoản nguồn (bên Có) — hiển thị dạng rút gọn `Mã TK - Tên` |
| TK nhận | Tài khoản đích (bên Nợ) — hiển thị dạng rút gọn `Mã TK - Tên` |
| Số tiền | Số tiền điều chuyển |

4. Bấm vào dòng để mở chứng từ gốc.
5. Dòng cuối bảng hiển thị **Tổng cộng**.

### Tạo điều chuyển nội bộ mới

Báo cáo có nút **Bút toán điều chuyển** ở góc trên — mở trực tiếp biểu mẫu Phiếu kế toán loại **Bank Entry** để tạo bút toán điều chuyển mới.

Ngoài ra có thể tạo từ đường tự nhiên:
1. Mở danh sách phiếu kế toán → "+ Thêm".
2. Chọn loại **Bank Entry** và tạo 2 dòng:
   - Dòng 1: Nợ TK đích / [số tiền]
   - Dòng 2: Có TK nguồn / [số tiền]

## Định khoản tự động

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Chuyển VND từ NH A sang NH B | 1121-NHB | 1121-NHA | Cùng loại tiền, khác ngân hàng |
| Mua ngoại tệ (VND → USD) | 1122-USD | 1121-VND | Khác loại tiền, cần nhập tỷ giá |
| Nộp tiền mặt vào ngân hàng | 1121 | 1111 | Nộp tiền mặt |
| Rút tiền từ ngân hàng về quỹ | 1111 | 1121 | Rút tiền mặt |
| Chuyển tiền giữa các quỹ tiền mặt | 1111-B | 1111-A | Cùng loại tiền, khác quỹ |

## Tình huống đặc biệt & cảnh báo

- **Tỷ giá khi mua/bán ngoại tệ:** Bút toán với 2 loại tiền khác nhau (VND ↔ USD) cần nhập tỷ giá thực tế tại thời điểm giao dịch. Chênh lệch tỷ giá ghi vào TK 515 (lãi) hoặc TK 635 (lỗ).
- **Cùng ngân hàng, khác tài khoản:** Điều chuyển nội bộ giữa 2 tài khoản cùng ngân hàng (vd: TK thanh toán → TK ký quỹ) — phí chuyển tiền thường bằng 0.
- **Khác ngân hàng:** Điều chuyển giữa 2 ngân hàng khác nhau — có thể mất phí chuyển tiền. Ghi nhận phí riêng: Nợ 642x / Có 1121-nguồn.
- **Thời gian chuyển tiền:** Chuyển khác ngân hàng có thể mất 1-2 ngày làm việc. Ghi nhận ngày phát sinh là ngày lệnh chuyển, không phải ngày tiền đến.
- **Sai số dư sau điều chuyển:** Đảm bảo tài khoản nguồn có đủ số dư trước khi tạo bút toán.
- **Logic phát hiện:** Báo cáo tự động phát hiện điều chuyển nội bộ bằng cách nhóm GL Entry theo `voucher_no` và kiểm tra xem phiếu có đồng thời dòng Nợ và dòng Có cùng thuộc nhóm TK tiền mặt/ngân hàng không. Không cần đánh dấu thủ công.

## Báo cáo liên quan

- **Sổ Tài khoản ngân hàng**: theo dõi số dư từng TK 112.
- **Sổ quỹ tiền mặt**: theo dõi số dư TK 111.
- **Thu ngân hàng / Chi ngân hàng**: báo cáo giao dịch (điều chuyển nội bộ có thể xuất hiện trong cả hai).

## FAQ

**Q: Điều chuyển nội bộ có cần phiếu thanh toán không?**
**A:** Không — dùng phiếu kế toán loại Bank Entry. Phiếu thanh toán dành cho giao dịch với đối tác bên ngoài (khách hàng, nhà cung cấp).

**Q: Có cần tạo chứng từ riêng cho phí chuyển tiền không?**
**A:** Tùy ngân hàng. Nếu phí chuyển tiền được trừ riêng (vd: chuyển 100M, phí 11.000đ), tạo thêm 1 dòng Nợ 642x / Có 1121. Nếu ngân hàng trừ gộp (chỉ nhận 99.989.000đ), ghi nhận số tiền thực nhận và tạo 1 dòng phí riêng trên cùng Bank Entry.

**Q: Báo cáo có bao gồm chuyển tiền mặt↔ngân hàng không?**
**A:** Có. Báo cáo quét cả TK 111% (tiền mặt) và TK 112% (ngân hàng). Các giao dịch như nộp tiền mặt vào ngân hàng (Nợ 1121 / Có 1111) hoặc rút tiền từ ngân hàng về quỹ (Nợ 1111 / Có 1121) đều được phát hiện và hiển thị.

**Q: Làm sao để tạo nhanh một điều chuyển nội bộ?**
**A:** Bấm nút "Bút toán điều chuyển" trên báo cáo → biểu mẫu Bank Entry mở sẵn. Nhập 2 dòng Nợ/Có với các TK nguồn và đích.
