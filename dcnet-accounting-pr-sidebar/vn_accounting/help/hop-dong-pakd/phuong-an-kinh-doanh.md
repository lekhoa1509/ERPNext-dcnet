---
title: Phương án kinh doanh (PAKD)
order: 2
summary: PAKD gắn hợp đồng — tính hoa hồng NVKD, phí giấy phép viễn thông và các khoản phải trả phía khách; duyệt nhiều cấp; ghi sổ hoa hồng theo cơ sở tiền.
---

## Mục đích

**Phương án kinh doanh (PAKD)** gắn với một hợp đồng và tính ra các khoản "chi" nội bộ phát sinh từ hợp đồng đó:

- **Hoa hồng NVKD** (Sales Commission): hoa hồng trả cho nhân viên kinh doanh.
- **Phí giấy phép viễn thông — GPVT** (License Fee): phí, lệ phí phải nộp nhà nước.
- **Khoản phải trả phía khách** (PAKD Beneficiary Line) gồm ba loại: **Dịch vụ quản lý** (Manager Services), **Chi phí ngoài** (Add Costs) và **Hoa hồng giới thiệu** (Referral). Mỗi khoản có thể gắn người nhận đích danh + khấu trừ thuế TNCN.

PAKD áp **bộ quy tắc hoa hồng** (mẫu tính theo loại PAKD / loại dịch vụ / chi nhánh / kênh) để tự tính tỷ lệ và số tiền, hiển thị biên lãi, rồi đi qua **quy trình duyệt nhiều cấp**. Sau khi duyệt và khách thanh toán, kế toán ghi sổ hoa hồng.

Hai loại PAKD: **Recurring Telecom** (dịch vụ viễn thông định kỳ) và **One-off Sale/Project** (bán đứt / dự án).

## Khi nào dùng

- Tính hoa hồng cho NVKD trên một hợp đồng cụ thể.
- Khai báo phí giấy phép viễn thông và các khoản phải trả phía khách kèm theo hợp đồng.
- Theo dõi tiến trình duyệt và xem biên lãi (margin) của phương án.
- Sau khi khách thanh toán: ghi sổ hoa hồng theo tỷ lệ thực thu.

## Cách thực hiện

1. Mở **Phương án kinh doanh** → "+ Thêm" → chọn **hợp đồng** + **NVKD** (sales_person).
2. Hệ thống tự tính: doanh thu hợp đồng, hoa hồng NVKD, phí GPVT, các khoản phải trả phía khách, tổng chi phí, doanh thu dịch vụ ròng và **biên lãi %** (xanh/vàng/đỏ theo ngưỡng cấu hình).
3. Có thể **ghi đè tỷ lệ** từng khoản hoa hồng tại bảng "Ghi đè hoa hồng" (để trống = dùng tỷ lệ mẫu).
4. Khai báo **khoản phải trả phía khách** (nếu có): chọn loại (Dịch vụ quản lý / Chi phí ngoài / Hoa hồng giới thiệu), tỷ lệ, người nhận, % thuế TNCN.
5. Bấm **Gửi duyệt** — phương án đi qua các cấp tùy loại: GĐ Kinh doanh → Phòng Tổng hợp → GĐ Chi nhánh → Ban Lãnh đạo. Nút **Nhắc duyệt** gửi email cho người cần duyệt (có giới hạn tần suất).
6. Sau khi **đã duyệt** + kỳ thu tiền đã thanh toán: ghi sổ hoa hồng — qua nút **Đăng hoa hồng** trên thẻ tóm tắt, hoặc tự động khi đối soát phiếu thu (đăng theo tỷ lệ thực thu).
7. Nếu bị từ chối: xem lý do, **Sửa & gửi lại**.

## Định khoản tự động

PAKD sinh **bút toán** ghi nhận chi phí hoa hồng/phải trả. Mỗi loại khoản tạo một bút toán riêng (để truy vết riêng cho quyết toán thuế). Bút toán tạo ở dạng **nháp** để kế toán rà soát rồi duyệt. Tài khoản dùng để định khoản **không cố định trong mã** — cấu hình tại **Thiết lập PAKD**.

| Trường hợp | TK Nợ (chi phí) | TK Có (phải trả) | Số vế | Ghi chú |
|---|---|---|---|---|
| Hoa hồng NVKD — không qua lương | TK chi phí hoa hồng NVKD | TK phải trả NVKD (3341, gắn người lao động) | 2 | Khi tắt "Dùng HRMS" |
| Hoa hồng NVKD — qua lương | — | — | — | Khi bật "Dùng HRMS": đẩy qua **Lương bổ sung**, không sinh bút toán riêng |
| Phí giấy phép viễn thông (GPVT) | TK phí GPVT | TK phí, lệ phí phải nộp (vd 3338 / 33382) | 2 | Phí nhà nước |
| Dịch vụ quản lý / Chi phí ngoài (không có người nhận đích danh) | TK chi phí tương ứng | TK phải trả (3388) | 2 | |
| Phải trả phía khách có người nhận + khấu trừ TNCN | TK chi phí | TK phải trả người ngoài (3388) = net; TK thuế TNCN tạm giữ (3335) = phần TNCN giữ lại | 3 | Net trả người nhận, TNCN giữ nộp thuế |
| Phải trả phía khách có người nhận, không khấu trừ TNCN | TK chi phí | TK phải trả người ngoài (3388) | 2 | Người nhận dưới ngưỡng chịu thuế |

> **Đánh dấu "không trừ TNDN":** khoản chi phải trả phía khách cho cá nhân ngoài lương, không có hóa đơn hợp pháp, mặc định bị đánh dấu **không được trừ khi tính thuế TNDN** trên vế Nợ. Khấu trừ TNCN (sắc thuế của người nhận) ≠ được trừ TNDN (sắc thuế của doanh nghiệp) — đây là hai việc khác nhau. Kế toán xác nhận tích/bỏ tích trên hộp thoại khi đăng.

**Cơ sở tiền:** khi đăng theo tỷ lệ từ phiếu thu, số ghi sổ = số tiền hoa hồng × (tiền thực thu / tổng doanh thu hợp đồng). Mỗi loại khoản gộp thành một bút toán tổng (không tách từng kỳ) để kế toán dễ duyệt.

## Tình huống đặc biệt & cảnh báo

- **Mỗi hợp đồng chỉ một PAKD hiệu lực:** không thể lập PAKD thứ hai cho cùng hợp đồng nếu đã có một PAKD chưa hủy.
- **Hợp đồng đã hủy:** không cho lập/sửa PAKD gắn hợp đồng đã hủy.
- **Chỉ ghi sổ hoa hồng cho kỳ đã thu tiền:** PAKD phải ở trạng thái **đã duyệt** và kỳ trong lịch hóa đơn phải **đã thanh toán**.
- **Khôi phục dòng hoa hồng đã đăng:** nếu bút toán còn nháp → tự xóa khi khôi phục; nếu đã ghi sổ → phải đảo bút toán thủ công.
- **Bỏ qua một khoản hoa hồng:** cần nhập lý do (≥ 3 ký tự).
- **Trung lập nghiệp vụ:** các khoản "phải trả phía khách" (giới thiệu / chênh lệch giá / dịch vụ quản lý) được ghi nhận theo cấu hình người dùng; tài liệu mô tả cơ chế ghi sổ, không đánh giá bản chất.

## Báo cáo liên quan

- [Sổ hoa hồng NVKD](so-hoa-hong-nvkd.md): theo dõi hoa hồng đã/đang ghi sổ theo từng NVKD.
- [Phải trả phía khách](phai-tra-phia-khach.md): danh sách khoản phải trả người nhận, chờ ghi sổ.
- [Danh sách hợp đồng](danh-sach-hop-dong.md): chứng từ gốc gắn PAKD.
- [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md): căn cứ xác định kỳ đã thu để ghi sổ hoa hồng.

## FAQ

**Q: Tại sao biên lãi PAKD hiển thị màu đỏ?**
**A:** Biên lãi = (doanh thu dịch vụ ròng − tổng chi phí) / doanh thu dịch vụ ròng. So với ngưỡng cấu hình trong Thiết lập PAKD (mặc định ≥ 25% xanh, ≥ 15% vàng, dưới đó đỏ). Đỏ là dấu hiệu phương án ít lãi, cần rà lại tỷ lệ hoa hồng và chi phí.

**Q: Tôi muốn NVKD nhận tỷ lệ hoa hồng khác mẫu chuẩn — làm sao?**
**A:** Tại bảng "Ghi đè hoa hồng", nhập tỷ lệ riêng cho khoản đó. Để trống = dùng tỷ lệ mẫu. Cũng có thể ghi đè riêng từng dòng (từng kỳ) trên bảng dòng hoa hồng.

**Q: Khoản "phải trả phía khách" có khấu trừ TNCN khác gì khoản không khấu trừ?**
**A:** Có khấu trừ → bút toán 3 vế: vế Có tách thành phần net trả người nhận (3388) và phần TNCN giữ lại nộp thuế (3335). Không khấu trừ → bút toán 2 vế, ghi toàn bộ vào phải trả người ngoài.
