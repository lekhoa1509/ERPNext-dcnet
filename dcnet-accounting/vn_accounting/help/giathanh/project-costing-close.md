---
title: Đóng công trình và xử lý chi phí dư
section: Giá thành
doctype: Project Costing
---

# Đóng công trình

Khi mọi giai đoạn đã có hóa đơn submitted, KTT đóng công trình để chốt lãi/lỗ + đảm bảo TK 154 cho công trình về 0.

## Khi nào đóng

Khi tất cả giai đoạn ở trạng thái terminal:
- **Đã xuất HĐ**
- **Đã thu tiền**
- **Đã hủy** (nếu giai đoạn bị bỏ giữa chừng)

Nếu có giai đoạn ở **Dự kiến / Đang thi công / Chờ xuất HĐ / Đã có SI draft** → hệ thống block, KTT phải hoàn tất các giai đoạn trước.

## Quy trình đóng

1. Mở form **Công trình & Giá thành**
2. Bấm nút **Đóng công trình** (góc trên bên phải)
3. Hệ thống tính **số dư TK 154** của công trình (Dr - Cr):
   - = 0: đóng sạch, không cần JE bổ sung
   - > 0: cost dư — hiện dialog hỏi KTT chọn xử lý
   - < 0: hiếm, đảo dấu (cost âm — hệ thống tự xử lý khi force)

4. Nếu dư > 0, dialog hiện 3 lựa chọn:
   - **Write-off 642 (Chi phí QLDN)** — cost dư là chi phí ngoài giới hạn dự án
   - **Write-off 632 (Giá vốn không phân bổ)** — cost dư là giá vốn không phân bổ được
   - **Hủy thao tác đóng** — KTT quay lại pin chi phí vào giai đoạn nào đó

5. KTT chọn → bấm **Đóng + Write-off** → hệ thống sinh JE write-off + chuyển status

## Bút toán write-off

Khi dư > 0 và KTT chọn write-off:

```
Nợ 642 (hoặc 632)        <dư>
       Có 154 (Project=X)        <dư>
```

Marker: `[PROJECT_COSTING:<costing>][TYPE:CLOSE_WRITEOFF]`. JE link lưu vào trường **Bút toán write-off** trên form.

## Sau khi đóng

- Trạng thái công trình chuyển sang **Đã hoàn thành**
- Trường **Ngày đóng** auto-fill
- Section **Bút toán liên quan** trên form thêm dòng `Write-off khi đóng công trình`
- Báo cáo P&L công trình khóa số liệu

## Mở lại công trình đã đóng

Trường hợp thực tế: sau bảo hành phát sinh chi phí mới, hoặc chủ đầu tư yêu cầu sửa.

1. Mở form công trình đã đóng
2. Bấm **Mở lại**
3. Hệ thống đổi status về **Đang thi công**, xóa ngày đóng

**Lưu ý:** Mở lại KHÔNG cancel bút toán write-off (giữ nguyên audit trail). KTT tự tạo JE bù nếu cần.

## Hủy công trình giữa chừng

Khác với "đóng" — khi công trình BỊ HỦY trước khi hoàn tất:

1. Trên form bấm **Hủy công trình** (Phase 1 chưa làm — Phase 2)
2. **Giai đoạn đã có hóa đơn submitted**: GIỮ NGUYÊN (đã giao khách). Chi phí khóa.
3. **Giai đoạn chưa có hóa đơn**: chuyển sang **Đã hủy**. Chi phí trong giai đoạn này + Common pool → KTT write-off riêng.

## Số dư công trình hiện tại

Trên form **Công trình & Giá thành** → section **Bút toán liên quan** → cuối cùng hiển thị **Số dư TK WIP công trình hiện tại**:

- Màu **xanh (≈ 0)** — sẵn sàng đóng sạch
- Màu **vàng (> 0)** — cost dư, sẽ phải write-off khi đóng
- Màu **đỏ (< 0)** — cost âm bất thường, cần kiểm tra ngay (có thể do JE bù sai)

Số dư tính tức thời từ Sổ Cái, không lưu đệm.
