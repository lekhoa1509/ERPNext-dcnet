---
title: Phân bổ chi phí hàng nhập khẩu
order: 2
summary: Xử lý thuế nhập khẩu, thuế TTĐB, phí hải quan và VAT nhập khẩu (khấu trừ / không khấu trừ) khi phân bổ chi phí mua hàng.
---

## Mục đích

Mở rộng của bài [Phân bổ chi phí mua hàng](lcv-co-ban.md) cho trường hợp hàng nhập khẩu. Khi nhập khẩu, ngoài cước vận chuyển quốc tế còn phát sinh:

1. **Thuế nhập khẩu (NK)** — cộng vào giá vốn hàng nhập (treo TK 3333 phải nộp).
2. **Thuế tiêu thụ đặc biệt (TTĐB)** nếu có — cộng vào giá vốn (TK 3332).
3. **Phí hải quan, giám định, lưu container, phí đại lý hải quan** — cộng vào giá vốn.
4. **VAT hàng nhập khẩu** — chia 2 trường hợp:
   - **Được khấu trừ** (hàng dùng cho hoạt động chịu thuế GTGT): ghi TK 1331, **KHÔNG cộng vào giá vốn**.
   - **Không được khấu trừ**: cộng vào giá vốn hàng nhập.

## Khi nào dùng

- Nhập khẩu hàng hóa / nguyên vật liệu có tờ khai hải quan.
- Có thuế NK, thuế TTĐB phải nộp theo tờ khai.
- Cần tách phần VAT NK được khấu trừ ra khỏi giá vốn.

## Cách thực hiện

1. Tạo phiếu **Phân bổ chi phí mua hàng** như bài cơ bản, sau đó bật trường **Hàng nhập khẩu** = ✓. Hệ thống hiển thị thêm các loại chi phí dành riêng cho nhập khẩu (thuế NK, thuế TTĐB, VAT NK không khấu trừ, phí hải quan, lưu container, phí đại lý).
2. Tab **Chi phí** → thêm dòng **Thuế nhập khẩu** → hệ thống điền tài khoản theo cấu hình → nhập số thuế NK theo tờ khai. Thuế NK luôn cộng vào giá vốn.
3. Thêm dòng **VAT nhập khẩu không khấu trừ** (nếu có) → nhập số tiền phần không khấu trừ. Phần này sẽ cộng vào giá vốn.
4. **VAT NK được khấu trừ KHÔNG nhập ở tab Chi phí.** Sau khi ghi sổ phiếu, bấm nút **"Tạo phiếu VAT NK khấu trừ"** trên phiếu phân bổ → nhập số tiền VAT được khấu trừ → hệ thống sinh một bút toán nháp riêng (Dr 1331 / Cr 33312) để kế toán soát xét và ghi sổ.
5. Phân bổ, kiểm tra, **Ghi sổ** như bài cơ bản.

> **Vì sao VAT NK khấu trừ phải tách ra một bút toán riêng?** Phiếu phân bổ chi phí mua hàng luôn cộng mọi khoản chi phí vào giá tồn kho (Dr 156 / Cr ...). VAT NK được khấu trừ KHÔNG được làm tăng giá tồn kho theo VAS, nên không thể đưa vào tab Chi phí mà phải hạch toán bằng một phiếu kế toán riêng.

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Ghi nhận giá CIF hàng nhập | 156 / 152 / 153 | 331 (phải trả nước ngoài) | Từ phiếu nhập kho / hóa đơn mua |
| Thuế NK phát sinh | 156 / 152 / 153 | 3333 | Cộng vào giá vốn (qua phiếu phân bổ) |
| Thuế TTĐB phát sinh | 156 / 152 / 153 | 3332 | Cộng vào giá vốn |
| Phí hải quan, giám định, lưu container | 156 / 152 / 153 | 111 / 112 / 331 | Cộng vào giá vốn |
| VAT NK **không** khấu trừ | 156 / 152 / 153 | 33312 | Cộng vào giá vốn |
| VAT NK **được** khấu trừ (phiếu riêng) | **1331** | **33312** | Bút toán nháp do nút "Tạo phiếu VAT NK khấu trừ" sinh ra; KHÔNG cộng vào giá vốn |

> Phiếu VAT NK khấu trừ sinh ở trạng thái **nháp** — kế toán review rồi ghi sổ thủ công. Nếu công ty thiếu TK 1331 hoặc 33312, hệ thống báo lỗi để bổ sung vào hệ thống tài khoản.

## Tình huống đặc biệt & cảnh báo

- **Tờ khai hải quan** là căn cứ nhập số thuế NK, TTĐB, VAT NK — giữ lại để đối chiếu.
- **Ngày phiếu phân bổ** nên là ngày thông quan (ngày trên tờ khai).
- **VAT NK không khấu trừ phải ≥ 0** — hệ thống chặn nếu nhập số âm.
- Nhiều lô cùng một tờ khai → tạo 1 phiếu phân bổ, nhiều dòng chi phí.
- Hàng vừa dùng cho hoạt động chịu thuế vừa không chịu thuế GTGT → tách tỷ lệ VAT khấu trừ / không khấu trừ tương ứng.

## Báo cáo liên quan

- [Phân bổ chi phí mua hàng](lcv-co-ban.md): hướng dẫn cơ bản và cơ chế 2 lớp.
- [Chi phí chờ phân bổ](landed-cost-pending-allocation.md): theo dõi chi phí treo chưa phân bổ.

## FAQ

**Q: Nhập số thuế NK ở đâu cho đúng — tab Chi phí hay nút riêng?**
**A:** Thuế NK, thuế TTĐB, VAT NK **không khấu trừ**, phí hải quan → nhập ở tab Chi phí (đều cộng vào giá vốn). Chỉ riêng VAT NK **được khấu trừ** dùng nút "Tạo phiếu VAT NK khấu trừ".

**Q: Hàng dùng 100% cho sản xuất kinh doanh chịu thuế thì VAT NK xử lý sao?**
**A:** Khấu trừ 100% → toàn bộ qua nút "Tạo phiếu VAT NK khấu trừ" (Dr 1331 / Cr 33312), không cộng đồng nào vào giá vốn.
