# DCNET CRM Discussion #9 Feedback Batch

## Overview

Đối chiếu và xử lý 50 phản hồi giao diện/nghiệp vụ từ khách hàng trong [dcnet-crm Discussion #9](https://github.com/dcnet-cloud/dcnet-crm/discussions/9). Nguồn yêu cầu trực tiếp: nội dung Discussion #9 và ảnh feedback do khách hàng cung cấp ngày 14/07/2026.

## Requirements

- Chuẩn hóa UI Bàn làm việc, Tiềm năng, Liên hệ, Khách hàng, Cơ hội, Báo giá, Đơn hàng, Tài khoản và Hoạt động.
- Giữ điều hướng Cơ hội/Báo giá/Đơn hàng trong DCNET CRM; chỉ Hóa đơn được chuyển sang kế toán sau khi kiểm tra quyền.
- Bổ sung action còn thiếu, Account trên dòng đơn hàng và quyền sửa Tài khoản dịch vụ.
- Có checklist độc lập để QA lại đủ 50 phản hồi.

## Implementation

- Frontend: sửa template/composable/CSS theo từng module; bổ sung tab Tổng quan khách hàng, tab Bán hàng cơ hội, tab Thu chi/Thực xuất/Hỗ trợ/Khác của đơn hàng.
- Backend: fallback Account cho dòng đơn hàng cũ; endpoint cập nhật Tài khoản dịch vụ có kiểm tra quyền `write` và whitelist field.
- QA artifact: `dcnet-crm/docs/DISCUSSION_9_FEEDBACK_CHECKLIST.html`, có bộ lọc và checkbox QA lưu bằng `localStorage`.

## Technical Notes

- Không dùng `ignore_permissions`; mọi cập nhật Account đi qua `doc.check_permission("write")` và `doc.save()`.
- Không thay đổi `dcnet_crm/workspace_sidebar/crm.json` vì đây là file shared/user-owned đang có thay đổi riêng.
- Các mục cần đánh giá trực quan được gắn trạng thái “Chờ QA giao diện” trong checklist; trạng thái source không thay thế nghiệm thu trình duyệt.

## Deployment

1. Build frontend bằng `npm run build` trong repository `dcnet-crm`.
2. Chạy migrate nếu site chưa đồng bộ endpoint/app code.
3. Chạy `bench --site flow.local clear-cache` và hard refresh trình duyệt.

## Future Updates

Không bổ sung tính năng ngoài Discussion #9. Các action chưa có quy trình/API trong spec tiếp tục ẩn theo `show_unready_features` hoặc cần khách hàng clarify trước khi phát triển.

## Troubleshooting

- Nếu nút sửa Account không hiện: kiểm tra quyền `write` của `DCNET Service Account`.
- Nếu UI cũ còn cache: build lại bundle, clear cache và hard refresh.
- Nếu liên kết Hóa đơn báo không có quyền: cấp quyền đọc `Sales Invoice`; không chuyển route bằng cách bỏ qua permission.

## Verification Checklist

- [x] Frontend check 31 modules.
- [x] Frontend production build.
- [x] 21 integration tests `dcnet_crm.tests.test_api` pass.
- [x] Checklist chứa đủ liên tục 50 mục.
- [ ] QA trực quan các mục có nhãn “Chờ QA giao diện”.

