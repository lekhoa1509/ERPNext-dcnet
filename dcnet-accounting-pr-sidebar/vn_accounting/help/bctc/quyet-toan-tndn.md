---
title: Quyết toán TNDN (Form 03)
order: 5
summary: Điều phối lợi nhuận kế toán → thu nhập chịu thuế → thuế TNDN phải nộp, tích hợp chi phí không được trừ (B4).
---

## Mục đích

**Quyết toán TNDN (Form 03)** là báo cáo điều phối, nối **lợi nhuận kế toán** (từ B02) sang **thu nhập chịu thuế** và **số thuế TNDN phải nộp**. Cấu trúc mô phỏng Tờ khai quyết toán 03/TNDN: lấy lợi nhuận kế toán, cộng chi phí không được trừ (B4), trừ các khoản miễn/giảm, rồi nhân thuế suất.

Chỉ tiêu **B4 (chi phí không được trừ) tự động lấy** từ các bút toán đã gắn cờ "Không được trừ (TNDN)" trong Sổ Cái.

## Khi nào dùng

- Cuối năm: lập số liệu để điền Tờ khai 03/TNDN nộp cơ quan thuế.
- Trong năm: ước tính thuế TNDN tạm tính, theo dõi tỷ lệ thuế hiệu lực.
- Đối chiếu: kiểm tra chênh lệch giữa lợi nhuận kế toán và thu nhập chịu thuế.

## Cách thực hiện

1. Vào **Báo cáo tài chính → Quyết toán TNDN (Form 03)**.
2. Chọn **Công ty** và **Năm tài chính** (bắt buộc). Hệ thống tự lấy khoảng ngày từ năm tài chính.
3. (Tùy chọn) Điều chỉnh **Thuế suất TNDN** — mặc định 20%.
4. Báo cáo hiển thị 4 cột: **Mã chỉ tiêu**, **Diễn giải**, **Giá trị**, **Ghi chú**, chia 4 phần:

| Mã | Diễn giải | Cách tính |
|---|---|---|
| A1 | Doanh thu thuần (TK 511, 515, 711) | Tổng Có − Nợ của tài khoản loại Doanh thu |
| A2 | Tổng chi phí (TK 6xx, 8xx) | Tổng Nợ − Có của tài khoản loại Chi phí |
| **A** | **Lợi nhuận kế toán trước thuế** | = A1 − A2 |
| **B4** | **Chi phí không được trừ** | Tự động từ bút toán gắn cờ "Không được trừ" |
| B5 | Lỗ năm trước chuyển sang | Nhập tay (mặc định 0) |
| B6 | Thu nhập miễn thuế | Nhập tay (mặc định 0) |
| **C** | **Thu nhập chịu thuế** | = A + B4 − B5 − B6 |
| **D** | **Thuế TNDN phải nộp** | = C × thuế suất (nếu C > 0) |

Phần **Phân tích hiệu lực** giải trình chênh lệch: X1 (thuế theo LN × 20%), X2 (chênh lệch D − X1), X3 (tỷ lệ thuế hiệu lực %).

5. Thẻ tóm tắt trên đầu báo cáo: LN kế toán, CP không trừ (B4), Thu nhập chịu thuế, Thuế phải nộp, Tỷ lệ hiệu lực.

## Định khoản tự động

Báo cáo này **không tự định khoản — chỉ tra cứu và tính toán**. Cách lấy số liệu:

- **A1, A2** dựa trên loại tài khoản (Doanh thu / Chi phí), loại trừ bút toán kết chuyển cuối kỳ để không tính trùng.
- **B4** cộng giá trị bên Nợ của mọi bút toán đã gắn cờ "Không được trừ (TNDN)" trong kỳ. Cờ này được đặt khi hạch toán — xem [Chi phí không được trừ (B4)](chi-phi-khong-duoc-tru.md).

## Tình huống đặc biệt & cảnh báo

- **B5, B6 phải nhập tay:** lỗ chuyển từ năm trước và thu nhập miễn thuế hệ thống chưa tự lấy — mặc định 0, kế toán tự điều chỉnh khi điền Tờ khai 03/TNDN.
- **Tỷ lệ thuế hiệu lực ≠ 20% là bình thường:** do B4 đẩy thuế cao hơn LN × 20%, hoặc B6/ưu đãi đẩy thấp hơn. Phần "Phân tích hiệu lực" giải trình.
- **Thu nhập chịu thuế âm (lỗ):** khi C ≤ 0, thuế phải nộp D = 0.
- **B4 phải khớp báo cáo chi tiết:** số B4 ở đây phải bằng tổng cộng trong báo cáo [Chi phí không được trừ (B4)](chi-phi-khong-duoc-tru.md). Nếu lệch, kiểm tra kỳ lọc của hai báo cáo.

## Báo cáo liên quan

- [Chi phí không được trừ (B4)](chi-phi-khong-duoc-tru.md) — chi tiết từng khoản tạo nên B4.
- [Chi phí không được trừ (B4)](chi-phi-khong-duoc-tru.md) — chi tiết các khoản + cách gắn cờ, 6 lý do, căn cứ pháp lý.
- [B02 — Kết quả HĐKD](b02-ket-qua-kinh-doanh.md) — nguồn lợi nhuận kế toán.

## FAQ

**Q: Vì sao thuế phải nộp khác lợi nhuận kế toán × 20%?**
**A:** Vì cộng thêm chi phí không được trừ (B4) làm thu nhập chịu thuế lớn hơn lợi nhuận kế toán. Đây là bản chất của quyết toán thuế, không phải lỗi — xem phần "Phân tích hiệu lực".

**Q: B4 đang là 0, có sai không?**
**A:** Đúng nếu trong năm không có bút toán nào gắn cờ "Không được trừ". Với doanh nghiệp thực tế thường có ít nhất một số khoản (tiền phạt chậm nộp, chi không hóa đơn). Kiểm tra lại việc gắn cờ khi hạch toán.

**Q: Lỗ chuyển năm trước (B5) tại sao không tự lấy?**
**A:** Số lỗ được chuyển phụ thuộc quyết định của doanh nghiệp (chuyển bao nhiêu, trong 5 năm). Hệ thống để kế toán tự nhập để chủ động kiểm soát.
