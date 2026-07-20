# DCNET CRM Order Related Documents Compact UI

## 1. Overview

Thu gọn giao diện tab Chứng từ liên quan trong chi tiết Đơn hàng, giúp xem nhanh Báo giá, Phiếu giao hàng, Hóa đơn và Thanh toán mà không tạo khoảng trắng lớn.

## 2. Requirements

- Nguồn: yêu cầu trực tiếp và ảnh màn hình khách hàng ngày 14/07/2026.
- Giao diện phải đẹp, gọn và đồng nhất với DCNET CRM.
- Mã chứng từ phải dễ nhận biết và có thể bấm mở.
- Địa chỉ giao hàng không được hiển thị thẻ HTML thô.

## 3. Implementation

- Đổi bốn section xếp dọc thành lưới card 2 cột; tự chuyển 1 cột khi màn hình hẹp.
- Thêm icon theo loại chứng từ, badge số lượng và empty state compact.
- Dòng chứng từ hiển thị mã link xanh, ngày, trạng thái và số tiền căn phải.
- Thêm hover, focus-visible và reduced-motion cho khả năng truy cập.
- Chuẩn hóa chuỗi địa chỉ HTML thành nội dung dấu phẩy dễ đọc.

## 4. Technical Notes

- Chỉ thay đổi presentation; giữ nguyên API và quy tắc điều hướng/permission hiện tại.
- Dùng Vue template hiện hữu và CSS namespace `sod-related-*` để tránh ảnh hưởng màn khác.

## 5. Deployment

Build frontend và chạy `bench --site flow.local clear-cache`, sau đó hard refresh trình duyệt.

## 6. Future Updates

Chỉ bổ sung action tạo chứng từ tại card khi có yêu cầu workflow được khách hàng xác nhận.

## 7. Troubleshooting

- Nếu vẫn thấy giao diện cũ, hard refresh để tải lại `crm.bundle.js`.
- Nếu card không có dữ liệu, kiểm tra quyền đọc DocType và liên kết chứng từ nguồn.

## 8. Verification Checklist

- [x] Lưới 2 cột trên desktop và 1 cột dưới 900px.
- [x] Link chứng từ có hover/focus rõ ràng.
- [x] Empty state giảm chiều cao.
- [x] Không còn hiển thị `<br>` trong địa chỉ.
- [x] Frontend check 31 modules và build thành công.
