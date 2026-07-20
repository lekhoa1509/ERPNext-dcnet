---
section: Hợp đồng
title: Hợp đồng vs Phương án kinh doanh
summary: Khi nào dùng Hợp đồng, khi nào dùng PAKD — phân biệt 2 chứng từ song song.
---

## Tóm tắt phân biệt

| | Hợp đồng | PAKD |
|---|---|---|
| Mục đích | Pháp lý + vận hành | Phân tích tài chính nội bộ |
| In trên hợp đồng giấy | ✅ Có | ❌ Không |
| Khách nhìn thấy | ✅ Có | ❌ Không |
| Đối tượng dùng | Tất cả | NVKD + Quản lý + Kế toán |
| Số lượng | 1 HĐ / thoả thuận | 1 PAKD / HĐ (đa số) hoặc nhiều PAKD/tháng (FTTH HGD) |
| Trạng thái | Bản nháp → Đang hoạt động → ... | Bản nháp → Chờ duyệt (4 bước) → Đã duyệt / Từ chối |
| Sinh dữ liệu gì | Lịch thu tiền, hoá đơn bán hàng | Dòng hoa hồng, Lương bổ sung HRMS |

## Mối quan hệ

Hợp đồng là **nguồn dữ liệu chuẩn**. PAKD fetch hầu hết trường từ HĐ (khách hàng, NVKD, loại dịch vụ, hạng mục).

```
Hợp đồng (HD-2026-00156)
    ↓ fetch
PAKD (PAKD-2026-00012)
    ↓ phân tích tài chính
biên lãi, hoa hồng NVKD
    ↓ duyệt
Lương bổ sung (Additional Salary HRMS)
```

## Khi sửa cái nào?

| Việc cần làm | Sửa ở đâu |
|---|---|
| Đổi số tiền, đơn giá, đơn vị (Hạng mục) | **Hợp đồng** (PAKD sẽ hiện cảnh báo lệch ⚠) |
| Đổi điều khoản pháp lý (Bên A, dates, payment_mode) | **Hợp đồng** |
| Đổi channel (Staff/Board) cho HĐ này | **PAKD** |
| Đổi tỷ lệ hoa hồng | **PAKD Commission Rule Template** (mẫu, không phải PAKD cụ thể) |
| Đổi doanh thu thực tế FTTH HGD tháng | **PAKD** (revenue_actual mỗi item) |

## Drift (lệch dữ liệu)

Khi HĐ thay đổi Hạng mục sau khi PAKD đã tạo, hệ thống hiện cảnh báo lệch trên thẻ Tóm tắt PAKD. Bấm "Update from Contract" để đồng bộ lại.

**Lệch là bình thường** — không phải lỗi. Nó nghĩa là HĐ đã được điều chỉnh, PAKD chưa cập nhật. Quyết định:

- Đồng bộ ngay → để PAKD phản ánh đúng HĐ hiện tại
- Giữ nguyên → khi PAKD đang chờ duyệt và muốn ghi nhận snapshot cũ
