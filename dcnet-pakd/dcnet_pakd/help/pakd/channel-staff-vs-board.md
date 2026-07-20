---
section: PAKD
title: Channel — Staff vs Board
summary: Phân biệt 2 channel Staff và Board — khác nhau ở đâu, tỷ lệ hoa hồng có khác không.
---

## Channel = Staff (NVKD tự bán)

- NVKD chủ động tìm và đóng thoả thuận với khách
- Hoa hồng theo tỷ lệ chuẩn (xem **PAKD Settings > default_commission_channel**)
- Là channel mặc định cho hầu hết HĐ telecom

## Channel = Board (Ban Lãnh đạo giới thiệu)

- HĐ được giới thiệu bởi Ban Lãnh đạo (BLD) cho NVKD đóng
- Có thể áp **tỷ lệ hoa hồng khác** so với Staff (thường thấp hơn vì BLD đã làm phần lớn việc tìm khách)
- Tỷ lệ cụ thể được cấu hình trong **PAKD Commission Rule Template** với `scope_channel = Board`

## Cách hệ thống tính

Quy trình lookup hoa hồng theo Channel:

1. Tìm **PAKD Commission Rule Template** matching nhất với (`pakd_type`, `service_type`, `branch`, `channel`)
2. Mẫu nào có `scope_channel = Board` sẽ được ưu tiên cho HĐ channel Board
3. Mẫu fallback (không có scope_channel) áp dụng nếu không tìm thấy mẫu Board

## Khi nào chọn Channel = Board

- HĐ được giới thiệu trực tiếp từ Giám đốc, Phó Giám đốc, Ban Lãnh đạo
- HĐ có tính chất đặc biệt (gia hạn lớn, khách VIP, deal chiến lược) cần BLD can thiệp
- Thoả thuận nội bộ giữa BLD và NVKD về việc chia hoa hồng

**Không** chọn Board nếu NVKD đã tự tìm khách — đây là Staff. Sai channel = sai hoa hồng = mất tin tưởng.

## Default

Channel mặc định cho PAKD mới = giá trị trong **PAKD Settings > default_commission_channel** (mặc định: Staff).
