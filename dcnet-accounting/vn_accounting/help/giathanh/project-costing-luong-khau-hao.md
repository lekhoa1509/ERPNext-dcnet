---
title: Phân bổ lương + khấu hao thiết bị vào công trình
section: Giá thành
doctype: Cost Allocation Run
---

# Phân bổ lương + khấu hao thiết bị vào công trình

Bài này hướng dẫn KTT hạch toán **lương kỹ sư on-site** và **khấu hao thiết bị thi công** vào TK 154 của công trình — 2 nguồn chi phí phổ biến nhưng KHÔNG có trường project gắn sẵn trong hệ thống ERP.

## Phương án 1 — Lương kỹ sư on-site **trực tiếp 100% 1 công trình**

Áp dụng khi: kỹ sư A 100% thời gian làm cho công trình X (toàn bộ tháng).

### Bước 1 — Chạy bảng lương như bình thường
1. Mở **Bảng tính lương → Đợt tính lương**
2. Ghi sổ đợt tính lương → tự sinh bút toán:
   ```
   Dr 622 Chi phí nhân công trực tiếp     X.XXX.XXX
          Cr 334 Phải trả người lao động           X.XXX.XXX
          Cr 3338 Các loại thuế khác               X.XXX
          ...
   ```
   Bút toán trên Sổ Cái chưa gắn công trình.

### Bước 2 — KTT post JE bù re-classify cost vào project
1. Mở **Tổng hợp → Bút toán chung → + Tạo mới**
2. Loại chứng từ: Phiếu kế toán. Ngày: cùng ngày tính lương.
3. Hàng:
   ```
   Dr 154 [project=X, project_costing_stage=Y]   X.XXX.XXX
          Cr 622                                          X.XXX.XXX
   ```
4. **User Remark** ghi rõ: "Re-classify lương kỹ sư A tháng MM/YYYY vào công trình X"
5. Submit JE

Sau submit:
- Bảng tập hợp chi phí công trình thấy dòng `JE thủ công — TK 154` cho project X
- Khi SI stage Y submit → engine sinh JE COGS Dr 632 / Cr 154 (project X) tự động

## Phương án 2 — Lương PM chia **nhiều công trình**

Áp dụng khi: PM Tuấn lương 25tr/tháng, làm cho công trình A 40h, B 30h, việc khác 10h (theo bảng chấm công).

### Bước 1 — Chạy bảng lương → tự sinh bút toán Dr 642 hoặc 627 / Cr 334

### Bước 2 — KTT tạo Đợt phân bổ chi phí gián tiếp (Cost Allocation Run)
1. Mở **Giá thành → Đợt phân bổ chi phí gián tiếp → + Tạo mới**
2. Điền:
   - **Kỳ**: 01/MM/YYYY → 31/MM/YYYY
   - **Phương pháp**: Thủ công
   - **TK ghi Có (override)**: chọn **TK 627** (nếu bảng lương ghi Có 627) hoặc **TK 642** (nếu ghi Có 642)
3. **Nguồn chi phí**:
   - Loại chứng từ: Phiếu lương
   - Chứng từ: chọn phiếu lương PM Tuấn
   - Mô tả: "Lương PM Tuấn tháng MM/YYYY"
   - Số tiền: 25.000.000
4. **Phân bổ ra công trình** (theo % giờ từ bảng chấm công):
   - Project A: 50% (40h / 80h tổng)
   - Project B: 37.5% (30h / 80h)
   - Để phần còn lại: 12.5% → KTT có thể đẩy vào project khác hoặc bỏ qua (write-off khi đóng kỳ)
5. Submit → engine sinh JE:
   ```
   Dr 154 [project=A]    12.500.000
   Dr 154 [project=B]     9.375.000
          Cr 627                       21.875.000
   ```

## Phương án 3 — Khấu hao thiết bị thi công

Áp dụng khi: xe cẩu khấu hao 1.9tr/tháng dùng chia nhiều công trình.

### Bước 1 — Lịch khấu hao tài sản tự sinh bút toán mỗi tháng
Hệ thống ERP tự sinh bút toán Nợ TK 6424 (Chi phí khấu hao TSCĐ) / Có TK 214 (Khấu hao luỹ kế) — chưa gắn công trình.

### Bước 2 — KTT tạo Cost Allocation Run
1. Mở **Đợt phân bổ chi phí gián tiếp → + Tạo mới**
2. **Kỳ**: tháng tương ứng
3. **Phương pháp**: Thủ công (hoặc Đều nếu xe dùng đều)
4. **TK ghi Có (override)**: chọn **TK 6424**
5. **Nguồn chi phí**:
   - Loại chứng từ: Phiếu kế toán
   - Chứng từ: chọn bút toán khấu hao tháng đó
   - Mô tả: "Khấu hao xe cẩu tháng MM/YYYY"
   - Số tiền: 1.900.000
6. **Phân bổ ra projects**: % theo số ngày xe dùng cho từng công trình (KTT ghi nhật ký sử dụng xe)
7. Submit → engine sinh JE Dr 154-project / Cr 6424.

## Bảng tóm tắt phương án

| Nguồn chi phí | Phương án | TK ghi Có |
|---|---|---|
| Lương kỹ sư on-site 100% 1 công trình | Phiếu kế toán bù thủ công Dr 154 / Cr 622 | TK 622 |
| Lương PM chia nhiều công trình | Đợt kết chuyển, nguồn = phiếu lương | TK 627 hoặc 642 (theo bút toán lương) |
| Khấu hao thiết bị thi công | Đợt kết chuyển, nguồn = bút toán khấu hao | TK 6424 |
| Bảo dưỡng thiết bị | Đã có chứng từ sửa chữa tài sản | (tự động Dr 154) |
| Văn phòng phẩm chung | Đợt kết chuyển, nguồn = hóa đơn mua hàng | TK 627 |

## Kiểm tra sau khi phân bổ

1. Mở Pivot Tool của công trình → thấy mục mới trong Common Pool (hoặc đã pin nếu CAR có stage)
2. Mở form Công trình & Giá thành → section "Bút toán liên quan" → group "Phân bổ chi phí gián tiếp" thêm JE mới
3. Báo cáo P&L công trình chi tiết → cột "CP phân bổ" tăng

## Vì sao bảng chấm công KHÔNG được tính là chi phí?

Bảng chấm công chỉ ghi nhận **thời gian làm việc** — không phát sinh bút toán trên Sổ Cái. Lương được hạch toán qua phiếu lương / đợt tính lương. Nếu pin bảng chấm công vào giai đoạn:
- Chi phí đã pin tăng giả → giá đề xuất sai
- Bút toán giá vốn Dr 632 / Cr 154 (công trình) với số tiền > số dư 154 → TK 154 ra số dư âm

**Bảng chấm công vẫn hữu ích như bằng chứng** để kế toán trưởng tính % phân bổ lương trong Đợt kết chuyển (Phương án 2 ở trên).

## Hướng cải tiến (chưa làm)

- Tiện ích "phân loại lại chi phí" trên phiếu kế toán (tự sinh Dr 154 / Cr 622 chỉ với một thao tác).
- Pivot Tool nhập tỷ lệ phân bổ từ bảng chấm công (tự tính % theo giờ).
- Trường công trình trên phiếu lương cho trường hợp lương trực tiếp 100% một công trình (bỏ bước phiếu kế toán bù thủ công).
