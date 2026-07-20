---
section: PAKD
title: Quy trình duyệt PAKD
summary: 4 bước duyệt, ai phụ trách bước nào, khi nào áp dụng từng bước.
---

## 4 bước duyệt tuần tự

```
NVKD tạo (Bản nháp)
    ↓ Gửi duyệt
Chờ Giám đốc Kinh doanh (theo chi nhánh)
    ↓ Duyệt
Chờ Phòng Tổng hợp
    ↓ Duyệt
Chờ Giám đốc Chi nhánh
    ↓ Duyệt
Chờ Ban Lãnh đạo (chỉ HĐ giá trị lớn)
    ↓ Duyệt
Đã duyệt → sinh hoa hồng + Additional Salary
```

Mỗi bước, người duyệt có 2 lựa chọn:
- **Duyệt** → chuyển sang bước tiếp
- **Từ chối** → mở dialog nhập **Lý do từ chối** → PAKD chuyển trạng thái "Bị từ chối"

## Ai phụ trách bước nào

| Trạng thái | Vai trò Frappe (Role) | Người thực |
|---|---|---|
| Bản nháp | `PAKD Sales Rep` | NVKD đã ký HĐ |
| Chờ Giám đốc Kinh doanh | `PAKD Sales Director HCM` hoặc `PAKD Sales Director HN` (theo chi nhánh) | GĐ KD chi nhánh |
| Chờ Phòng Tổng hợp | `PAKD General Department` | Phòng Tổng hợp (TC + Kế hoạch) |
| Chờ Giám đốc Chi nhánh | `PAKD Branch Director HN` (hoặc HCM) | GĐ Chi nhánh |
| Chờ Ban Lãnh đạo | `PAKD Board` | Ban LĐ — chỉ áp dụng PAKD giá trị lớn |
| Đã duyệt | (System) | Hệ thống tự sinh hoa hồng |
| Bị từ chối | (System) | NVKD sửa lại + gửi lại |

## Khi nào ÁP DỤNG bước nào

- Bước Ban Lãnh đạo có thể bỏ qua nếu workflow rule cho phép (cho PAKD giá trị thấp)
- Một số HĐ có thể bỏ qua bước Giám đốc Chi nhánh (cấu hình workflow nội bộ)
- Cấu hình bước nào áp dụng cho PAKD nào nằm trong **Workflow** doctype của Frappe

## Nút "Nhắc duyệt"

Trên thẻ Tóm tắt PAKD, khi đang ở trạng thái chờ duyệt, có nút **Nhắc duyệt**. Bấm nút sẽ:

1. Gửi email tới TẤT CẢ user có role tương ứng (BCC list)
2. Ghi vào **Lịch sử nhắc duyệt PAKD** (audit log)
3. Tự khoá 24h cho cùng người dùng + cùng PAKD (rate limit để tránh spam)

## Lý do từ chối

Khi bấm "Từ chối", dialog yêu cầu nhập **Lý do từ chối** (bắt buộc). Lý do sẽ:

- Lưu vào trường `rejection_reason` của PAKD
- Hiển thị trên thẻ Tóm tắt khi trạng thái là "Bị từ chối"
- NVKD đọc lý do, sửa PAKD, gửi lại workflow
