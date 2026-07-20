---
title: Chi phí không được trừ (B4)
order: 6
summary: Báo cáo chi tiết các khoản chi bị loại khi tính thuế TNDN (chỉ tiêu B4), kèm hướng dẫn nghiệp vụ — căn cứ pháp lý, 6 lý do phân loại, cách gắn cờ và các hiểu lầm phổ biến.
---

## Mục đích

**Báo cáo chi phí không được trừ (B4)** liệt kê chi tiết mọi bút toán đã gắn cờ "Không được trừ (TNDN)" trong kỳ, tổng hợp từ tất cả nguồn (phiếu kế toán, hóa đơn mua hàng, đề nghị thanh toán, phiếu lương, bút toán khấu hao). Số tổng cộng chính là **chỉ tiêu B4** trong Tờ khai 03/TNDN — điều chỉnh tăng thu nhập chịu thuế.

Tài liệu này gồm hai phần: **phần báo cáo** (cách chạy, đọc số) và **phần nghiệp vụ** (căn cứ pháp lý, cách gắn cờ, các hiểu lầm) — trước đây tách riêng, nay gộp chung một chỗ.

## Khi nào dùng

- Cuối năm: lấy chi tiết để giải trình B4 với cơ quan thuế hoặc kế toán dịch vụ.
- Trong năm: rà soát các khoản đã gắn cờ, phát hiện gắn nhầm hoặc còn sót.
- Đối chiếu với báo cáo [Quyết toán TNDN](quyet-toan-tndn.md) — tổng ở đây phải khớp dòng B4.

## Cách thực hiện

1. Vào **Báo cáo tài chính → Chi phí không được trừ (B4)**.
2. Chọn **Công ty** và **kỳ** (Từ ngày — Đến ngày). Mặc định tháng hiện hành.
3. (Tùy chọn) Lọc thêm: **Tài khoản**, **Loại chứng từ**, **Lý do không được trừ**.
4. Báo cáo hiển thị danh sách chi tiết với các cột:
   - **Ngày**, **Loại CT**, **Số CT** (bấm để mở chứng từ gốc)
   - **Tài khoản**, **Loại bên**, **Bên liên quan**
   - **Lý do** — lý do phân loại
   - **Số tiền** — giá trị bên Nợ
   - **Ghi chú**
5. Dòng cuối **"TỔNG CỘNG (B4)"** cộng toàn bộ số tiền.
6. **Biểu đồ** dưới báo cáo gom số tiền theo từng lý do (dạng cột).
7. Thẻ tóm tắt: Tổng CP không được trừ (B4) + kỳ báo cáo.

## Định khoản tự động

Báo cáo này **không tự định khoản — chỉ tra cứu**. Nó chỉ đọc các bút toán đã gắn cờ "Không được trừ (TNDN)" với điều kiện: đã ghi sổ (không bị hủy) và có phát sinh bên Nợ. Việc gắn cờ thực hiện khi hạch toán — xem phần **Cách gắn cờ trong hệ thống** bên dưới.

## Tình huống đặc biệt & cảnh báo

- **Tổng = 0:** đúng nếu trong kỳ không có khoản nào gắn cờ. Hiếm với doanh nghiệp thực (thường có ít nhất tiền phạt chậm nộp). Nếu nghi thiếu, rà lại việc gắn cờ khi hạch toán.
- **Báo cáo chỉ đọc cờ, không tự phân loại:** một khoản chỉ xuất hiện ở đây nếu đã được tick "Không được trừ" lúc lập chứng từ. Quên tick = không lên báo cáo.
- **Số tiền lấy bên Nợ:** chỉ cộng phát sinh bên Nợ (debit > 0) — đúng bản chất chi phí. Bút toán điều chỉnh ghi ngược (giảm chi phí) cần kế toán trưởng rà.
- **Bút toán đã hủy bị loại tự động** (is_cancelled).

---

# Hướng dẫn nghiệp vụ

Phần dưới đây dành cho kế toán trưởng: vì sao phải tách CP không được trừ, căn cứ pháp lý, cách phân loại, cách gắn cờ trong hệ thống, và các hiểu lầm phổ biến.

## Vì sao phải tách CP không được trừ

Doanh nghiệp ghi nhận **đầy đủ** mọi chi phí thực phát sinh vào sổ kế toán → BCTC chính thức (B01/B02/B03/B09) phản ánh đúng đời sống. Nhưng khi nộp thuế TNDN, một phần chi phí KHÔNG được trừ (vì không đủ chứng từ, vượt định mức, hoặc không liên quan SXKD). Cuối năm cộng phần đó vào chỉ tiêu B4 của Tờ khai 03/TNDN để tính ra thu nhập chịu thuế.

Vì vậy cần **đánh dấu phân loại** tại thời điểm hạch toán, để cuối năm dễ tổng hợp + tránh sót.

## Căn cứ pháp lý

| Văn bản | Nội dung chính | Hiệu lực |
|---|---|---|
| **Nghị định 320/2025/NĐ-CP** Điều 9 | Điều kiện chi phí được trừ: thực tế phát sinh + liên quan SXKD + có hóa đơn chứng từ hợp pháp + chứng từ thanh toán không tiền mặt ≥5 triệu | Từ 15/12/2025 |
| **Nghị định 320/2025/NĐ-CP** Điều 10 | Liệt kê 23 nhóm chi phí KHÔNG được trừ | Từ 15/12/2025 |
| **Chuẩn mực kế toán VN số 17** (VAS 17) | Phân loại chênh lệch vĩnh viễn vs chênh lệch tạm thời giữa Lợi nhuận kế toán và Thu nhập chịu thuế | Đang hiệu lực |
| **Thông tư 99/2025/TT-BTC** | Hệ thống tài khoản kế toán + biểu mẫu BCTC | Từ 01/01/2026 |
| **Luật Kế toán 2015** Điều 13 | Cấm "ghi sổ kép, hai sổ" — chỉ một sổ trung thực | Đang hiệu lực |

## Phân biệt 2 loại chênh lệch (VAS 17)

| Loại | Định nghĩa | Ví dụ | Xử lý trong hệ thống |
|---|---|---|---|
| **Chênh lệch vĩnh viễn** | KHÔNG bao giờ đảo ngược. CP đã chi nhưng KHÔNG được trừ vĩnh viễn. | Tiền phạt thuế, BHXH chậm nộp; tiếp khách vượt định mức (phần vượt); chi cho từ thiện vượt 5% LN trước thuế | **Tag cờ `Không được trừ` + Lý do** → cộng vào B4 |
| **Chênh lệch tạm thời** | SẼ đảo ngược trong các kỳ sau. Khấu hao kế toán ≠ khấu hao thuế, dự phòng… | Khấu hao xe ≤9 chỗ giá >1.6 tỷ — phần vượt định mức ghi nhận sớm hơn thuế cho phép | KHÔNG dùng cờ này. Hạch toán riêng qua Thuế hoãn lại (TK 243/347) — tài liệu khác |

**Quy tắc**: Cờ `is_non_deductible` trong hệ thống CHỈ dùng cho chênh lệch vĩnh viễn. Đừng tick cho khấu hao chênh lệch — đó là vấn đề khác.

## Các lý do phân loại (6 lý do)

Khi tick cờ "Không được trừ (TNDN)", bắt buộc chọn 1 trong 6 lý do:

| Lý do | Khi nào dùng | Ví dụ điển hình |
|---|---|---|
| **Không HĐ hợp lệ** | Chi phí thực phát sinh nhưng không có hóa đơn / chứng từ hợp pháp | Trả tiền cá nhân không khấu trừ TNCN, không có HĐLĐ; NCC ngừng hoạt động sau 1/7/2025; HĐ giả mạo bị cơ quan thuế loại |
| **Vượt định mức quy định** | Chi phí có HĐ đầy đủ nhưng số tiền VƯỢT định mức Bộ Tài chính quy định — phần vượt non-deductible | Tiếp khách vượt định mức nội bộ DN; chi cho lao động nữ vượt 1 tháng lương BQ; phúc lợi vượt 1 tháng lương BQ/người/năm; lãi vay vượt 30% EBITDA (NĐ 132) |
| **Không liên quan SXKD** | Chi phí cá nhân của giám đốc/cổ đông, hoạt động phúc lợi không SXKD | TSCĐ phục vụ phúc lợi cá nhân (xe nhà giám đốc); chi du lịch không phải khen thưởng theo quy chế; tiền tài trợ không có cam kết quảng bá |
| **Tiền phạt (thuế / BHXH / hợp đồng)** | Mọi khoản phạt nộp cho cơ quan nhà nước hoặc đối tác | Phạt nộp thuế chậm; phạt BHXH chậm nộp; phạt vi phạm hợp đồng kinh tế; phạt vi phạm môi trường |
| **Related-party không TP doc** | Chi phí cho bên liên kết (nội bộ tập đoàn) không có Hồ sơ giá chuyển nhượng (NĐ 132/2020) | Phí quản lý trả công ty mẹ FDI không có TP doc; phí royalty intra-group không justify ALP; phí dịch vụ chung tập đoàn không hợp đồng ALP |
| **Khác** | Không thuộc 5 loại trên — bổ sung diễn giải vào ô Ghi chú | Chi phí khác bị cơ quan thuế loại sau kiểm tra |

## Cách gắn cờ trong hệ thống

### Bước 1 — Tại thời điểm hạch toán

**Bút toán kế toán (Phiếu kế toán):** Khi tạo dòng chi phí, tick ô "Không được trừ (TNDN)" + chọn Lý do. Hệ thống tự động yêu cầu chọn Lý do nếu đã tick cờ.

**Hóa đơn mua hàng:** Trên từng dòng hàng hóa/dịch vụ, tick "Không được trừ" + chọn Lý do tại dòng tương ứng. Cờ sẽ tự lan truyền xuống sổ cái khi xuất hóa đơn.

**Đề nghị thanh toán (Expense Claim):** Tương tự — tick trên từng dòng chi phí trước khi gửi duyệt.

**Thành phần lương:** Cài đặt 1 lần ở danh mục Thành phần lương (vd: "Phạt BHXH chậm nộp" → tick mặc định). Mọi Phiếu lương dùng thành phần này sẽ tự đánh cờ.

**TSCĐ phúc lợi:** Tick ô "TSCĐ phúc lợi" trên Tài sản. Bút toán khấu hao tự động sẽ được đánh dấu khi chạy.

### Bước 2 — Tự động phát hiện

Hệ thống tự đánh cờ trong một số trường hợp rõ ràng:

- **PAKD — Phí Quản lý / Phí ngoài / Hoa hồng môi giới**: Nếu người nhận là cá nhân (có tên) + không khấu trừ TNCN + không có HĐ → tự đánh cờ "Không HĐ hợp lệ"
- **Hóa đơn mua hàng từ NCC đã ngừng hoạt động**: tự đánh cờ ở thời điểm validate hóa đơn

Mọi auto-set đều có thể **chỉnh tay** (untick + chọn Lý do khác) trước khi chốt phiếu.

### Bước 3 — Xem báo cáo tổng hợp

Vào sidebar **Báo cáo tài chính**:

- **"Chi phí không được trừ (B4)"** — danh sách chi tiết tất cả dòng đã đánh dấu trong kỳ, nhóm theo Lý do, tổng cộng B4 ở dòng cuối (chính là báo cáo này)
- **"Quyết toán TNDN (Form 03)"** — báo cáo điều phối từ Lợi nhuận kế toán → cộng B4 → ra Thu nhập chịu thuế → tính Thuế TNDN phải nộp + phân tích tỷ lệ thuế hiệu lực

### Bước 4 — Cuối năm

1. Mở "Quyết toán TNDN (Form 03)" cho năm tài chính
2. Đối chiếu số B4 với chi tiết bên báo cáo này — nếu cần in để gửi kế toán dịch vụ thuế
3. Nhập tay các điều chỉnh khác (Lỗ chuyển từ năm trước B5, Thu nhập miễn thuế B6) nếu có
4. Sao chép số liệu sang Tờ khai 03/TNDN trên phần mềm HTKK/eTax

## Hiểu lầm phổ biến — phải tránh

### Hiểu lầm 1: "BCTC official phải loại CP không được trừ"

**SAI.** Theo VAS 01 (Khuôn khổ chung) + VAS 17 (Thuế TNDN):
- BCTC B01/B02/B03/B09 ghi nhận **toàn bộ** chi phí thực phát sinh, bất kể có được trừ thuế hay không
- Lợi nhuận kế toán trên B02 = Doanh thu thuần − Tổng chi phí (đầy đủ)
- Quyết toán TNDN tính riêng: lấy LN kế toán + B4 + ... → Thu nhập chịu thuế

Cờ `is_non_deductible` chỉ là **phân loại để báo cáo thuế**, KHÔNG ảnh hưởng số tiền ghi sổ.

### Hiểu lầm 2: "Cờ Không trừ = bút toán sai"

**SAI.** Chi phí đánh cờ vẫn là chi phí HỢP PHÁP về mặt kế toán — vẫn có chứng từ chi tiền, vẫn vào sổ đầy đủ. Cờ chỉ phân loại "khi quyết toán thuế thì không được trừ".

Ví dụ: tiền phạt nộp chậm BHXH 10 triệu. Đầy đủ biên lai. Hạch toán Dr 811 / Cr 112. Đánh cờ Lý do = "Tiền phạt". Đây là bút toán ĐÚNG.

### Hiểu lầm 3: "Người nhận có khấu trừ TNCN → chắc chắn được trừ"

**SAI.** Khấu trừ TNCN là một dấu hiệu CÓ chứng từ DV cá nhân, nhưng KHÔNG đảm bảo deductible:
- Phải đủ HĐ DV (nếu cá nhân không có HĐ DV → chỉ có TNCN khấu trừ thì vẫn thiếu chứng từ)
- Phải có hợp đồng + biên bản hoặc xác nhận DV
- Phải có chứng từ thanh toán không tiền mặt (nếu ≥5tr)

Khi nghi ngờ, tham khảo kế toán thuế chuyên nghiệp trước khi tick/untick.

### Hiểu lầm 4: "Lợi nhuận kế toán phải bằng Thu nhập chịu thuế"

**SAI.** Trong BCTC chuẩn của doanh nghiệp đang hoạt động lành mạnh, LN kế toán × 20% thường KHÁC số thuế TNDN phải nộp. Chênh lệch do:
- B4 (CP không trừ) cộng thêm → thuế cao hơn LN × 20%
- B6 (Thu nhập miễn thuế) trừ bớt → thuế thấp hơn
- Ưu đãi thuế suất (10/15/17 thay vì 20)

Tỷ lệ thuế hiệu lực ≠ 20% là **bình thường + kỳ vọng**, không phải bug. Báo cáo "Quyết toán TNDN" có phần "Phân tích hiệu lực" giải trình chênh lệch.

### Hiểu lầm 5: "Giữ 2 sổ — sổ thật và sổ thuế"

**SAI + VI PHẠM PHÁP LUẬT.** Luật Kế toán 2015 Điều 13 cấm rõ ràng. Pattern thực tế sai phổ biến:
- Sổ "thật" ghi đầy đủ chi phí (kể cả off-book)
- Sổ "thuế" chỉ ghi entries có HĐ → BCTC = quyết toán khớp nhau

Đây là rủi ro pháp lý khi thanh tra. Đường ĐÚNG: 1 sổ trung thực + cờ phân loại = đạt cùng mục tiêu hợp pháp.

### Hiểu lầm 6: "Báo cáo B4 hiển thị âm → có lỗi"

**Có thể đúng + có thể sai.** Dòng B4 chỉ aggregate `WHERE is_non_deductible=1 AND debit > 0`. Nếu thấy số âm, kiểm tra:
- Bút toán đảo ngược (cancel) chưa được lọc — hệ thống đã lọc `is_cancelled=0`, nếu vẫn âm thì là entry điều chỉnh thủ công
- Bút toán giảm chi phí (Dr 6xx ngược) — hiếm gặp, cần KTT review

## FAQ

**Q: Một khoản chi không hiện trong báo cáo dù tôi biết nó không được trừ?**
A: Báo cáo chỉ liệt kê khoản đã gắn cờ "Không được trừ" lúc hạch toán. Nếu quên tick, mở lại chứng từ (nếu chưa khóa) hoặc dùng bút toán điều chỉnh để gắn cờ.

**Q: Bút toán đã chốt rồi, tôi muốn đổi cờ thì làm sao?**
A: Bút toán chốt thì cờ khóa. Cần hủy bút toán (revert) → tạo bút toán mới → tick lại cờ. HOẶC tạo bút toán điều chỉnh ngược chiều có cờ đúng.

**Q: Nếu tôi quên đánh cờ trong năm, cuối năm có cách bổ sung không?**
A: Hệ thống có script `vn_accounting.api.backfill_non_deductible_from_pakd` để re-scan PAKD (phương án kinh doanh) và đánh cờ retro cho các trường hợp rõ ràng. Cho các trường hợp khác (PI, EC, JE thủ công) cần KTT review thủ công.

**Q: Tổng B4 ở đây và ở "Quyết toán TNDN" lệch nhau?**
A: Thường do hai báo cáo lọc kỳ khác nhau. Báo cáo này lọc theo Từ ngày — Đến ngày; "Quyết toán TNDN" lọc theo cả năm tài chính. Đặt cùng kỳ để khớp.

**Q: Tổng = 0 — có sai không?**
A: Đúng nếu không có entry nào đánh cờ trong kỳ. Với DN demo có dùng PAKD: phải có ít nhất một số entry tự đánh cờ. Nếu thật sự không có → DN không phát sinh CP không trừ (hiếm với DN VN thực, thường có ít nhất tiền phạt BHXH).

**Q: Có thể lọc theo từng lý do không?**
A: Có. Dùng bộ lọc "Lý do không được trừ" để xem riêng từng nhóm, hoặc xem biểu đồ gom theo lý do.

**Q: TSCĐ phúc lợi đánh cờ → khấu hao bao nhiêu kỳ bị tag?**
A: Toàn bộ vòng đời khấu hao. Mỗi kỳ khấu hao auto-JE đều được đánh cờ "Không liên quan SXKD". Đến khi TSCĐ thanh lý.

**Q: Đối tác là công ty mẹ FDI có nên đánh cờ "Related-party không TP doc"?**
A: CÓ — nếu chưa lập Hồ sơ giá chuyển nhượng (NĐ 132/2020). Sau khi lập TP doc justify giá ALP → bỏ cờ và bổ sung diễn giải. Hồ sơ TP cần làm trước thời hạn quyết toán năm.

## Liên hệ + tham khảo

- **Câu hỏi nội bộ:** liên hệ KTT trưởng hoặc Trưởng phòng Kế toán
- **Tham vấn ngoài:** kế toán thuế dịch vụ — đặc biệt khi có giao dịch FDI/related-party
- **Tham khảo pháp lý:**
  - Nghị định 320/2025/NĐ-CP — toàn văn trên Cổng thông tin Chính phủ
  - Thông tư 99/2025/TT-BTC — Bộ Tài chính
  - VAS 17 — Bộ chuẩn mực kế toán VN
  - NĐ 132/2020/NĐ-CP — giao dịch liên kết

## Báo cáo liên quan

- [Quyết toán TNDN (Form 03)](quyet-toan-tndn.md) — dòng B4 lấy tổng từ báo cáo này.
- [B02 — Kết quả HĐKD](b02-ket-qua-kinh-doanh.md).
