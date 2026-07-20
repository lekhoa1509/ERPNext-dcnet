---
title: Tài liệu tự động chờ duyệt
order: 10
summary: Tập trung mọi tài liệu kế toán do hệ thống tự sinh (hóa đơn, phiếu kế toán nháp...) trên một màn hình kèm trạng thái và hành động cần làm.
---

## Mục đích

**Tài liệu tự động chờ duyệt** gom mọi tài liệu kế toán do hệ thống tự sinh vào một màn hình duy nhất, kèm trạng thái và việc cần làm. Mục tiêu: kế toán không phải "đi tìm" hóa đơn nháp, phiếu khấu hao nháp, phiếu lãi tiền gửi nháp... rải rác ở các phân hệ khác nhau. Mỗi app khi tự sinh tài liệu sẽ tự khai báo nhãn + mô tả + hành động, báo cáo này tự nhận diện. Chỉ TRA CỨU, không tự tạo chứng từ.

## Khi nào dùng

- **Hằng ngày:** rà các bản nháp đang chờ duyệt, ưu tiên ghi sổ trước những bản chờ lâu.
- **Trước khi lập báo cáo / khoá sổ:** bảo đảm không còn tài liệu tự sinh ở trạng thái Nháp.
- **Kiểm tra tài liệu tự ghi sổ:** xem các phiếu hệ thống đã tự ghi sổ (phân bổ CCDC, kết chuyển...) để "biết và kiểm tra".

## Cách thực hiện

1. Mở **Tổng hợp → Tài liệu tự động chờ duyệt**.
2. Nhập bộ lọc:
   - **Công ty** (mặc định công ty của người dùng).
   - **Từ ngày / Đến ngày** (mặc định 90 ngày gần nhất).
   - **Trạng thái** (mặc định chỉ hiện **Bản nháp**; mở rộng để xem Đã ghi sổ / Đã hủy).
   - **Loại tài liệu** (lọc theo nhóm cụ thể: Khấu hao TSCĐ, Lãi tiền gửi, Hóa đơn tự động từ Hợp đồng...).
   - **Chỉ hiện quá hạn duyệt** (chỉ bản nháp quá X ngày chưa ghi sổ).
3. Bấm **Chạy báo cáo**. Đọc khối **Hướng dẫn** (bấm để mở) — giải thích từng loại tài liệu tự sinh.
4. Ưu tiên xử lý dòng có cảnh báo đỏ (chờ ≥30 ngày). Bấm mã tài liệu để mở, xem lại định khoản/ngày/giá trị → **Ghi sổ** nếu đúng; nếu sai, quay về tài liệu gốc để sửa và sinh lại.

### Các cột chính

| Cột | Ý nghĩa |
|---|---|
| Loại | Tên nhóm tài liệu (do app khai báo) |
| Mã | Mã tài liệu (bấm để mở) |
| Trạng thái | Bản nháp / Đã ghi sổ / Đã hủy |
| Hành động | Gợi ý việc cần làm ("Duyệt và ghi sổ"...) |
| Ngày | Ngày hạch toán |
| Nguồn | Khách hàng / hợp đồng / tài sản gốc |
| Tổng tiền | Giá trị tài liệu |
| Số ngày chờ | Đếm từ ngày hạch toán (⚠ vàng ≥7 ngày, ⚠⚠ đỏ ≥30 ngày — chỉ với bản nháp) |
| Ghi chú | Nội dung diễn giải |

Phía trên bảng có các thẻ tổng: số bản nháp, đã ghi sổ, đã hủy, tổng giá trị, số bản nháp quá 7/30 ngày.

## Định khoản tự động

Báo cáo không tự định khoản — chỉ liệt kê. Các tài liệu trong danh sách MỚI là thứ chứa bút toán (do từng luồng tự sinh tạo ra). Một số ví dụ định khoản của các nguồn thường gặp:

| Loại tài liệu | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Thuế GTGT hàng nhập khẩu được khấu trừ | 1331 | 33312 | Sinh khi ghi sổ phiếu phân bổ chi phí mua hàng có thuế NK |
| Tạo tiền gửi có kỳ hạn | 1281 | 112x | |
| Lãi tiền gửi định kỳ | 1281 / 112x | 515 | Lãi kép cộng dồn 1281, lãi thường ghi 112x |
| Khấu hao TSCĐ | 6xx (chi phí) | 214x | Sinh từ lõi hệ thống ERP |
| Hóa đơn tự động từ Hợp đồng | (theo hóa đơn) | 511 + 3331 | Cần duyệt rồi xuất hóa đơn điện tử |

> Định khoản cụ thể do từng nguồn quyết định và hiển thị trong khối Hướng dẫn của báo cáo. Khi một app mới thêm luồng tự sinh, mô tả định khoản của nó tự xuất hiện ở đó.

## Tình huống đặc biệt & cảnh báo

- **Mặc định chỉ hiện Bản nháp:** đó là các tài liệu CẦN kế toán duyệt. Tài liệu hệ thống tự ghi sổ ngay (phân bổ CCDC, kết chuyển...) không hiện ở danh sách mặc định — đổi bộ lọc Trạng thái sang Đã ghi sổ để xem.
- **Cảnh báo quá hạn:** bản nháp chờ ≥7 ngày (vàng) hoặc ≥30 ngày (đỏ) cần ưu tiên xử lý — tránh sót doanh thu/chi phí cuối kỳ.
- **Hóa đơn bán hàng nháp:** ghi sổ xong nhớ xuất hóa đơn điện tử theo hành động gợi ý.
- **Tài liệu sai:** đừng sửa trực tiếp ở đây — quay về tài liệu gốc (Hợp đồng, Tài sản, Khoản vay, Tiền gửi...) để sửa rồi sinh lại.

## Báo cáo liên quan

- [Bảng cân đối số phát sinh](trial-balance.md): kiểm tra cân đối — bút toán nháp chưa ghi sổ là nguyên nhân lệch phổ biến.
- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): xử lý hết tài liệu nháp trước khi kết chuyển.

## FAQ

**Q: Vì sao mặc định chỉ thấy bản nháp?**
**A:** Bản nháp là thứ cần kế toán hành động (duyệt + ghi sổ). Đổi bộ lọc Trạng thái để xem thêm Đã ghi sổ (để biết/kiểm tra) hoặc Đã hủy (kiểm tra lý do).

**Q: Tài liệu của một luồng mới có tự xuất hiện không?**
**A:** Có. Khi app sở hữu luồng khai báo nguồn tự sinh, tài liệu tự xuất hiện kèm nhãn, hành động và mô tả — không cần sửa báo cáo.

**Q: Cảnh báo đỏ nghĩa là gì?**
**A:** Bản nháp đã chờ ≥30 ngày chưa ghi sổ — rủi ro sót hạch toán. Ưu tiên xử lý ngay.

**Q: Tài liệu hệ thống tự ghi sổ có cần tôi làm gì không?**
**A:** Không bắt buộc, nhưng nên lọc Trạng thái = Đã ghi sổ để kiểm tra định kỳ rằng chúng đã hạch toán đúng.
