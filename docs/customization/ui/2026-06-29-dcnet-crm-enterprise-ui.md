# DCNET CRM Enterprise UI

## 1. Overview

Chuẩn hóa giao diện `dcnet-crm` theo phong cách ERP chuyên nghiệp, ưu tiên khả năng quét dữ liệu nhanh, mật độ thông tin hợp lý và thao tác bàn phím.

## 2. Requirements

- Giữ nguyên luồng nghiệp vụ và dữ liệu hiện có.
- Tạo phân cấp thị giác rõ cho dashboard, danh sách và hồ sơ khách hàng.
- Dùng SVG đồng nhất thay cho ký hiệu trang trí.
- Hỗ trợ responsive, keyboard focus và `prefers-reduced-motion`.

Nguồn nghiệp vụ: không bổ sung tính năng mới; đây là thay đổi trình bày cho các chức năng CRM hiện có.

## 3. Implementation

- Bổ sung design tokens dùng chung: màu, radius, shadow, focus ring và trạng thái.
- Thiết kế lại dashboard với KPI có biểu tượng, phễu cơ hội dễ quét và nhóm thao tác nhanh.
- Chuẩn hóa bảng khách hàng, toolbar, tìm kiếm, phân trang và trạng thái dòng được chọn.
- Kết nối checkbox chọn tất cả/chọn từng dòng với state có sẵn.
- Tối ưu trang chi tiết khách hàng và breakpoint 1280/900/640 px.
- Tinh chỉnh riêng trang chi tiết Cơ hội: header hồ sơ, pipeline đơn sắc, KPI trung tính, empty state và activity rail.
- Bổ sung saved view cho danh sách Liên hệ: chọn giao diện, cấu hình/reorder cột, trường tổng, sắp xếp, lưu và nhân bản cấu hình.
- Kết nối xuất Excel danh sách Liên hệ; file `.xlsx` giữ tìm kiếm, bộ lọc, thứ tự cột và sắp xếp của saved view hiện tại.
- Cho workspace danh sách Liên hệ giãn theo chiều cao viewport Desk, không còn khoảng trắng 48px phía dưới; bảng và hai panel bên phải vẫn cuộn độc lập.
- Loại bỏ cụm quick actions trùng lặp ở rail phải của chi tiết Liên hệ và đưa tab Hoạt động/Mua hàng lên sát toolbar.
- Thiết kế lại tab Thông tin chi tiết của Liên hệ theo form ERP hai cột: card trắng, giá trị gạch chân, tìm kiếm trường và công tắc ẩn/hiện dữ liệu trống hoạt động thực tế.

## 4. Technical Notes

Các rule mới được scope dưới `.dcnet-crm` và đặt cuối `frontend/src/styles.css` để tạo một lớp override ổn định, không thay đổi logic API.

## 5. Deployment

```bash
cd dcnet-crm
npm run build
bench --site flow.local clear-cache
```

Sau đó hard reload trình duyệt.

## 6. Future Updates

- Các màn nghiệp vụ mới nên tái sử dụng design tokens `--crm-*`.
- Không dùng màu hard-code nếu token tương ứng đã tồn tại.
- Giữ chiều cao control chính ở 34–40 px để phù hợp môi trường ERP.

## 7. Troubleshooting

- Nếu style cũ còn hiển thị: clear cache và hard reload.
- Nếu layout hẹp: kiểm tra zoom trình duyệt và chiều rộng viewport.
- Nếu theme tùy chỉnh lệch màu: kiểm tra các biến `--st-primary`, `--fg-color`, `--bg-color`.

## 8. Verification Checklist

- [x] Build frontend thành công.
- [x] Không dùng emoji làm icon thao tác mới.
- [x] Có focus state rõ cho keyboard.
- [x] Có reduced-motion fallback.
- [x] Có breakpoint cho desktop, tablet và mobile.
- [x] Luồng nghiệp vụ không thay đổi.
