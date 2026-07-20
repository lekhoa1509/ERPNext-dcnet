---
title: Sử dụng Pivot Tool gán chi phí vào giai đoạn
section: Giá thành
doctype: null
---

# Pivot Tool — Gán chi phí vào giai đoạn

Pivot Tool là **nơi duy nhất** KTT/PM thay đổi mapping chi phí ↔ giai đoạn. Không có 2 đường khác để giảm bug đồng bộ.

## Mở Pivot Tool

Pivot Tool nay nhúng sẵn trong **form Project Costing**, không còn là page riêng. Cách mở:

1. Vào **Giá thành dự án → Dự án — Giá thành (Master)** từ sidebar
2. Mở công trình cần làm việc
3. Bấm tab **Stages & Pin chi phí** — pivot hiện ở đây

URL form: `/app/project-costing/<tên-công-trình>`. Tab Stages có thể link trực tiếp bằng `#stages_tab`.

## Bố cục

```
┌──────────────────────────────────────────────────────────────────────┐
│ [Tên công trình] [Khách hàng] [Trạng thái]              [Mở form] │
├──────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐        │
│  │ Stage 1  │  │ Stage 2  │  │ Stage 3  │  │ Common Pool  │ ←scroll │
│  │ Markup:1.5│ │ Markup:25%│ │ Cố định  │  │              │        │
│  │ CP: 50tr │  │ CP: 80tr │  │ CP: 0    │  │ CP: 15tr     │        │
│  │ Giá: 75tr│  │ Giá: 100tr│ │ Giá: 50tr│  │              │        │
│  │ ───────  │  │ ───────  │  │ ───────  │  │ ───────      │        │
│  │ Card CP  │  │ Card CP  │  │          │  │ Card CP      │        │
│  │ Card CP  │  │ Card CP  │  │          │  │ Card CP      │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘        │
└──────────────────────────────────────────────────────────────────────┘
```

## Pin chi phí vào giai đoạn

1. Trên thẻ chi phí (card), bấm nút **Pin**
2. Dialog hiện danh sách giai đoạn — chọn 1
3. (Hoặc chọn **(Common Pool — bỏ pin)** để gỡ chi phí khỏi giai đoạn cũ)
4. Bấm **Pin** trong dialog

Hệ thống cập nhật chi phí vào giai đoạn mới + tính lại **CP đã pin** và **Giá đề xuất** của giai đoạn.

## Quy tắc pin

- **1 chứng từ có thể chia ra ≥1 giai đoạn** (Phase 1 chưa hỗ trợ split — 1 dòng = 1 giai đoạn atomic; nếu cần split, sửa chứng từ gốc tách thành 2 dòng).
- **Khi 1 giai đoạn đã có hóa đơn submitted**, chi phí đã pin vào giai đoạn đó **bị khóa** — không edit, không di chuyển. Đảm bảo truy vết HĐ ↔ chi phí.
- **Common pool dương cuối công trình** là OK. KTT chọn cách xử lý khi đóng công trình.
- **Common pool âm (over-allocated):** UI block — không pin > nguyên giá.

## Cảnh báo pin sai pattern

Nếu KTT/PM thử pin 1 Phiếu mua hàng vào **nhiều công trình**, hệ thống hiển thị dialog:

> ⚠️ Phiếu mua hàng này đang được pin vào nhiều công trình.
> Nếu hàng hóa thực tế chia ra nhiều công trình theo số lượng, khuyến nghị:
> 1. Hủy thao tác pin này
> 2. Tạo Phiếu xuất kho cho từng công trình theo đúng số lượng dùng
> 3. Pin các Phiếu xuất kho đó (không pin Phiếu mua hàng gốc)
>
> Lý do: số liệu kho + báo cáo công trình chính xác hơn.

## Tạo hóa đơn từ giai đoạn

Trên thẻ giai đoạn:

1. Đảm bảo đã pin đủ chi phí + đã tính giá đề xuất
2. Bấm **Tạo HĐ**
3. Hệ thống sinh **Hóa đơn bán hàng** DRAFT với:
   - 1 dòng "[Tên công trình] — [Tên giai đoạn]"
   - Số tiền = Giá KTT chốt (hoặc Giá đề xuất nếu chưa override)
   - Khách hàng = Customer của Project
   - Link ngược về Project Costing + Stage

4. Tab mới mở form Hóa đơn → KTT review:
   - Đổi diễn giải (description) nếu cần
   - Tách 1 dòng thành nhiều dòng
   - Đổi số tiền (sẽ cảnh báo lệch với Giá xuất HĐ)
   - Thêm thuế VAT

5. Bấm **Submit** trên form → hệ thống tự sinh **Bút toán giá vốn** (Dr 632 / Cr 154) và đổi trạng thái giai đoạn sang **Đã xuất HĐ**.

## Hủy hóa đơn sau Submit

Nếu hóa đơn bị Cancel sau Submit:
- Giai đoạn quay về trạng thái **Chờ xuất HĐ**
- Chi phí của giai đoạn **mở khóa** (có thể pin lại)
- Bút toán giá vốn tự động cancel (đảo dấu)
- KTT có thể tạo hóa đơn mới cho giai đoạn

## Tính lại giá đề xuất

Sau khi pin xong, bấm **Tính lại** trên thẻ giai đoạn để cập nhật **Giá đề xuất**. Tự động chạy mỗi lần pin nhưng có nút thủ công cho an toàn.
