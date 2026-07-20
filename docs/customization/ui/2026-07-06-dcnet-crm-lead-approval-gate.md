# DCNET CRM Lead Approval Gate

**Ngày:** 06/07/2026  
**App:** `dcnet_crm`  
**Route:** `/desk/dcnet-crm?view=lead-detail`

## Overview

Chặn thao tác chuyển Tiềm năng sang Liên hệ trực tiếp từ màn hình chi tiết Tiềm năng.

## Requirements

- Tiềm năng không được nhảy sang Liên hệ ngay tại danh sách/chi tiết.
- Chỉ chuyển sang Liên hệ sau khi gửi phê duyệt và được duyệt OK.

## Implementation

- Đổi nút `Chuyển đổi` trong chi tiết Tiềm năng thành `Gửi phê duyệt`.
- Nút mới không gọi luồng tạo hoặc mở Contact.
- Khi bấm nút, hệ thống hiển thị thông báo rằng luồng chuyển sang Liên hệ phải chờ phê duyệt OK.

## Technical Notes

- Chưa phát hiện workflow approval hoặc field approval chuẩn cho Lead trong site hiện tại.
- Không tự tạo Workflow/Custom Field mới vì cần xác nhận quy trình phê duyệt chính thức.

## Deployment

Build lại frontend bundle của `dcnet_crm`, sau đó clear cache site.

## Future Updates

Khi có spec duyệt chính thức, nối nút `Gửi phê duyệt` vào workflow/API phê duyệt và chỉ chạy convert Lead to Contact khi trạng thái duyệt là OK.

## Troubleshooting

- Nếu vẫn thấy nút `Chuyển đổi`, hard reload browser và clear cache.
- Nếu cần chuyển đổi tự động sau duyệt, kiểm tra Workflow/Custom Field của Lead trước khi viết API convert.

## Verification Checklist

- [x] Chi tiết Tiềm năng không còn nút `Chuyển đổi`.
- [x] Nút `Gửi phê duyệt` không chuyển route sang Liên hệ.
- [x] Không tạo Contact khi bấm `Gửi phê duyệt`.
