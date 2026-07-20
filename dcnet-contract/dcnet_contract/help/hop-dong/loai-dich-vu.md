---
section: Hợp đồng
title: Loại dịch vụ
summary: 8 loại dịch vụ telecom + thi công — khi nào dùng và trường nào cần điền cho mỗi loại.
---

## 8 loại dịch vụ

| Loại | Là gì | Loại HĐ |
|---|---|---|
| **P2P** | Point-to-point — đường truyền 2 điểm cố định | Recurring |
| **MPLS** | Multi-Protocol Label Switching — mạng riêng giữa nhiều chi nhánh | Recurring |
| **ILL** | Internet Leased Line — đường truyền Internet riêng | Recurring |
| **FTTH DN** | Fiber To The Home cho Doanh Nghiệp | Recurring |
| **FTTH HGD** | Fiber To The Home cho Hộ Gia Đình (cá nhân) | Recurring |
| **IT Managed** | Dịch vụ quản trị CNTT | Recurring |
| **VTTB** | Vật Tư Thiết Bị — bán thiết bị | One-off |
| **Thi công** | Thi công lắp đặt | One-off |

## Trường cần điền theo loại

Chọn `Loại dịch vụ` để biểu mẫu hiện các trường phù hợp:

| Loại | Trường bổ sung hiện ra |
|---|---|
| P2P, MPLS | Điểm đầu (A), Điểm cuối (B) |
| FTTH HGD | Số CMND/CCCD, Ngày cấp, Nơi cấp, Ngày sinh |
| P2P, MPLS, ILL, FTTH DN, IT Managed | Tên gói / băng thông |
| VTTB | Hạng mục phải liên kết ERPNext Item (để xuất kho) |

## Tự động hoá khi chọn

- Recurring dịch vụ (P2P/MPLS/ILL/FTTH DN/FTTH HGD/IT Managed) → `contract_type` tự đặt thành "Recurring"
- One-off (VTTB/Thi công) → `contract_type` thành "One-off", `payment_mode` thành "OneOff"
- FTTH HGD / VTTB / Thi công → mục "Kỹ thuật" tự đóng (không cần)
- P2P / MPLS / ILL / FTTH DN / IT Managed → mục "Kỹ thuật" tự mở (cần điền điểm A-B, băng thông)

## Project Category vs Service Type

- `Loại dịch vụ` = bản chất kỹ thuật/sản phẩm
- `Danh mục dự án` (Telecom / IT / Equipment / Construction) = phân loại doanh thu nội bộ cho báo cáo

Cùng 1 HĐ có thể là `Loại dịch vụ = P2P` và `Danh mục dự án = Telecom`. Hoặc `VTTB` và `Equipment`.
