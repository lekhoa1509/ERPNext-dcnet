---
section: Hợp đồng
title: Đơn bán hàng nội bộ
summary: Đơn bán hàng nội bộ tự sinh cho HĐ One-off — quản lý xuất kho qua ERPNext, không thao tác trực tiếp.
---

## Khi nào xuất hiện

**Đơn bán hàng nội bộ** (shadow Sales Order) chỉ tự sinh khi:

- Hợp đồng có `Loại HĐ = One-off`
- Hạng mục có ít nhất 1 item gắn `erpnext_item` (link tới ERPNext Item)
- Hợp đồng được **Submit** (chuyển từ Draft sang Active)

Với HĐ Recurring (P2P/MPLS/ILL/FTTH DN/FTTH HGD/IT Managed), **không** sinh Đơn bán hàng nội bộ.

## Mục đích

Đơn bán hàng nội bộ làm cầu nối với ERPNext core để:

- Sinh **Phiếu giao hàng** (Delivery Note) → xuất kho item
- Cập nhật tồn kho ERPNext
- Cho phép kiểm soát số lượng giao thực tế vs số lượng cam kết trong HĐ

## Không thao tác trực tiếp

- **KHÔNG sửa** Đơn bán hàng nội bộ — sẽ desync với HĐ
- **KHÔNG huỷ** Đơn bán hàng nội bộ — huỷ HĐ sẽ tự huỷ Đơn
- Mọi thay đổi điều khoản/giá phải thực hiện trên HĐ — Đơn sẽ tự cập nhật

## Khi huỷ HĐ

Huỷ HĐ One-off sẽ:

1. Tự huỷ Đơn bán hàng nội bộ
2. Tự huỷ các Phiếu giao hàng đã xuất từ Đơn này (nếu chưa được xuất hoá đơn)
3. Sinh Credit Note cho các Hoá đơn đã xuất

## Trường hợp lỗi thường gặp

- **HĐ Submit báo lỗi "item phải có erpnext_item"**: phải link Hạng mục với 1 ERPNext Item (master) trước khi Submit
- **Đơn bán hàng nội bộ không xuất hiện sau Submit**: kiểm tra `contract_type == "One-off"` và ít nhất 1 hạng mục có `erpnext_item`
