# Notification Badge + Browser Alert

## Context

Người dùng cần thấy rõ số thông báo trên icon chuông và nhận cảnh báo ở góc màn hình khi đang chuyển qua tab khác, đặc biệt với thông báo đơn hàng mới.

## Changes

- Thêm badge số unread trên icon chuông Desk/Desktop.
- Thêm browser notification với tiêu đề `Bạn có thông báo đơn hàng mới` khi unread mới liên quan `Sales Order`/đơn hàng và tab DCNET không active.
- Giữ fallback in-app alert khi người dùng đang ở tab DCNET.
- Luồng gửi duyệt tạo ToDo im lặng và chỉ gửi 1 Notification Log tùy biến, tránh trùng dòng `assigned a new task`.

## Files

- `dcnet_apps/dcnet_apps/notifications.py`
- `dcnet_apps/dcnet_apps/public/js/notification_badge.js`
- `dcnet_apps/dcnet_apps/public/css/dcnet_theme.css`
- `dcnet_apps/dcnet_apps/hooks.py`
- `dcnet_apps/dcnet_apps/mobile_push/api.py`
- `dcnet_apps/dcnet_apps/mobile_push/events/notification_log.py`
