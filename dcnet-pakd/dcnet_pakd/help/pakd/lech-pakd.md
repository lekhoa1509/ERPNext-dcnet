---
section: PAKD
title: PAKD lệch so với Hợp đồng
summary: Khi PAKD lệch — nguyên nhân, cách giải quyết (đồng bộ vs giữ nguyên), khi nào tạo PAKD mới.
---

## Lệch là gì

PAKD fetch hầu hết trường từ Hợp đồng tại thời điểm tạo. Nếu HĐ thay đổi **Hạng mục** sau đó (qty, unit_price, item_label, uom), PAKD sẽ "lệch" — Hạng mục PAKD không khớp Hạng mục HĐ.

**Cảnh báo lệch (⚠)** hiển thị trên thẻ Tóm tắt PAKD khi tổng signature các hạng mục PAKD ≠ tổng signature các hạng mục HĐ.

## Nguyên nhân thường gặp

1. **Sửa HĐ sau khi tạo PAKD**: phổ biến nhất — kế toán thấy có sửa, muốn biết PAKD đã được tính theo dữ liệu nào
2. **Sửa Hạng mục PAKD trực tiếp**: ít gặp hơn (hệ thống cho phép edit Hạng mục PAKD độc lập với HĐ)
3. **Áp Mẫu HĐ mới**: nếu HĐ Re-apply Template, Hạng mục sẽ thay → PAKD lệch

## Cách giải quyết

### Lựa chọn 1: Đồng bộ từ HĐ

Bấm nút **Update from Contract** (xuất hiện ở section Hạng mục khi PAKD ở trạng thái Bản nháp). Hệ thống:

- Copy lại Hạng mục từ HĐ
- Recompute totals (DT, chi phí, hoa hồng, biên lãi)
- Hiện toast "Items updated from contract"

Dùng khi: HĐ là chuẩn, PAKD cần cập nhật.

### Lựa chọn 2: Giữ nguyên

Không bấm gì. PAKD giữ snapshot Hạng mục tại thời điểm tạo.

Dùng khi: PAKD đã được duyệt (hoặc đang chờ duyệt) và bạn muốn ghi nhận điều kiện gốc, không phản ánh thay đổi HĐ sau này.

### Lựa chọn 3: Tạo PAKD mới

Nếu HĐ thay đổi căn bản (đổi cấu trúc giá, đổi loại dịch vụ, thêm phụ lục thay đổi nhiều khoản):

1. Huỷ PAKD hiện tại (đặt status = Cancelled)
2. Tạo PAKD mới, link với HĐ
3. PAKD mới sẽ tự fetch dữ liệu HĐ mới nhất

Dùng khi: thay đổi quá lớn để chỉ sync Hạng mục.

## PAKD đã duyệt — có nên đồng bộ không?

**Không khuyến nghị**. Khi PAKD đã duyệt:

- Dòng hoa hồng đã được sinh
- Additional Salary đã có
- Đồng bộ Hạng mục sẽ KHÔNG tự recompute hoa hồng (cần huỷ + tạo lại)

Nếu thực sự cần: huỷ PAKD → tạo PAKD mới → đi qua quy trình duyệt lại.

## Sự kiện làm lệch không hồi tố

Khi HĐ chuyển trạng thái **Đã huỷ**, các PAKD liên quan **không tự huỷ** — nhưng cảnh báo lệch sẽ luôn đúng (HĐ huỷ = Hạng mục trên HĐ về 0). NVKD nên huỷ PAKD thủ công.
