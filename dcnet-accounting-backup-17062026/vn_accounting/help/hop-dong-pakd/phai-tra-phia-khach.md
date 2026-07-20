---
title: Phải trả phía khách (giới thiệu / chênh lệch giá / dịch vụ quản lý)
order: 7
summary: Danh sách công việc — các khoản phải trả người nhận ngoài (dịch vụ quản lý, chi phí ngoài, hoa hồng giới thiệu) của kỳ đã thu tiền, chờ kế toán ghi sổ.
---

## Mục đích

**Phải trả phía khách** liệt kê các dòng khoản phải trả (trên PAKD) đang **chờ ghi sổ** mà hợp đồng đã có ít nhất một kỳ **thu được tiền** — tức đã đủ điều kiện ghi sổ theo cơ sở tiền. Đây là danh sách công việc cho kế toán: ghi sổ tiếp các khoản phải trả người nhận ngoài.

Ba loại khoản (theo cấu hình PAKD):
- **Dịch vụ quản lý** (Manager Services)
- **Chi phí ngoài** (Add Costs)
- **Hoa hồng giới thiệu** (Referral)

Mỗi khoản có thể gắn **người nhận đích danh** (tên + mã số thuế/CCCD) và **tỷ lệ khấu trừ TNCN**.

## Khi nào dùng

- Sau khi khách thanh toán một kỳ: ghi sổ các khoản phải trả người nhận ngoài tương ứng.
- Rà soát khoản nào có người nhận đích danh + khấu trừ TNCN (bút toán 3 vế).
- Lọc theo PAKD, theo loại khoản, hoặc chỉ xem khoản có người nhận đích danh.

## Cách thực hiện

1. Mở **Phải trả phía khách**.
2. Bộ lọc:
   - **PAKD**: chỉ khoản của một PAKD.
   - **Loại**: Dịch vụ quản lý / Chi phí ngoài / Hoa hồng giới thiệu.
   - **Chỉ có người nhận đích danh (3-leg TNCN)**: chỉ hiện khoản gắn người nhận (sinh bút toán 3 vế khấu trừ TNCN).
3. Các cột: PAKD, trạng thái PAKD, hợp đồng, loại, người nhận, MST/CCCD, tỷ lệ, **số tiền/kỳ**, **TNCN**, **net**, chu kỳ, khách hàng.
4. Bấm vào PAKD để mở phương án → tại dòng khoản tương ứng, dùng tác vụ **"Đăng JE ngay"** để tạo bút toán nháp → kế toán duyệt.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ là worklist. Việc ghi sổ thực hiện từ PAKD. Hình mẫu bút toán khi đăng:

| Trường hợp | TK Nợ (chi phí) | TK Có | Số vế |
|---|---|---|---|
| Không có người nhận đích danh | TK chi phí theo loại | TK phải trả (3388) | 2 |
| Có người nhận + khấu trừ TNCN | TK chi phí theo loại | TK phải trả người ngoài (3388) = net; TK thuế TNCN tạm giữ (3335) = phần TNCN | 3 |
| Có người nhận, không khấu trừ TNCN | TK chi phí theo loại | TK phải trả người ngoài (3388) | 2 |

> **Lưu ý thuế:** khoản phải trả phía khách cho cá nhân ngoài lương, không có hóa đơn hợp pháp, mặc định bị đánh dấu **không được trừ khi tính thuế TNDN** trên vế Nợ. Khấu trừ TNCN (sắc thuế người nhận) ≠ được trừ TNDN (sắc thuế doanh nghiệp). Kế toán xác nhận trên hộp thoại khi đăng.

## Tình huống đặc biệt & cảnh báo

- **Điều kiện hiện dòng:** khoản ở trạng thái **chờ** + hợp đồng đã có ≥ 1 kỳ thu tiền. Khoản đã đăng hoặc hợp đồng chưa thu tiền không hiện.
- **Bút toán 3 vế khi có khấu trừ TNCN:** vế Có tách thành net trả người nhận (3388) + TNCN giữ lại (3335). Nếu số gộp ≠ net + TNCN, hệ thống yêu cầu lưu lại PAKD để tính lại.
- **Trung lập nghiệp vụ:** "phải trả phía khách" (giới thiệu / chênh lệch giá / dịch vụ quản lý) được ghi nhận theo cấu hình người dùng; tài liệu mô tả cơ chế ghi sổ, không đánh giá bản chất khoản chi.
- **Khác với hoa hồng NVKD:** khoản ở đây trả cho **người nhận ngoài**, không phải nhân viên kinh doanh. Hoa hồng NVKD xem [Sổ hoa hồng NVKD](so-hoa-hong-nvkd.md).

## Báo cáo liên quan

- [Phương án kinh doanh](phuong-an-kinh-doanh.md): nơi khai báo + đăng khoản phải trả.
- [Sổ hoa hồng NVKD](so-hoa-hong-nvkd.md): hoa hồng cho nhân viên kinh doanh.
- [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md): căn cứ kỳ đã thu tiền.

## FAQ

**Q: "Phải trả phía khách" gồm những khoản nào?**
**A:** Dịch vụ quản lý, chi phí ngoài, và hoa hồng giới thiệu — các khoản trả cho người nhận ngoài phát sinh từ hợp đồng, khai báo trên PAKD.

**Q: Khi nào sinh bút toán 3 vế?**
**A:** Khi khoản gắn người nhận đích danh và có tỷ lệ khấu trừ TNCN > 0 — vế Có tách thành net cho người nhận và phần TNCN giữ lại nộp thuế.

**Q: Báo cáo có dữ liệu cho DCNET không?**
**A:** Có — hiện đang có các dòng phải trả phía khách của kỳ đã thu tiền, chờ ghi sổ.
