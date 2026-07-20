# DCNET CRM — Opportunity detail readiness

> Ngày: 13/07/2026  
> Phạm vi: `/desk/dcnet-crm?view=opportunity-detail`

## Nguồn và giới hạn

- Nguồn nghiệp vụ: `docs/feature/FEATURE_SPECIFICATION.md`, mục quản lý Cơ hội.
- Nguồn chi tiết CRM: `dcnet-crm/docs/SPEC-CRM-tinh-nang.md`.
- Không tạo quan hệ dữ liệu Hỗ trợ mới vì đặc tả chưa xác định mapping với Opportunity.

## Thay đổi

- Sales Order trong tab Bán hàng chỉ lấy bản ghi liên kết với Opportunity khi field
  `custom_opportunity` tồn tại, thay vì lấy toàn bộ đơn hàng của Customer.
- Tổng tiền Opportunity được tính từ các dòng Opportunity Item khi tạo mới.
- Đồng bộ lại tổng tiền cho 10 Opportunity test `DCNET-CRM-TEST`.
- Tab Ghi chú & đính kèm có thao tác thêm ghi chú và tải nhiều tệp.
- Tab Hoạt động có thao tác tạo Công việc và Lịch hẹn.
- Dòng Liên hệ mở trang chi tiết Contact nội bộ.
- Thanh tab chuyển sang cấu trúc dữ liệu thống nhất, có badge, ARIA tab semantics,
  sticky position và cuộn ngang responsive.
- Bổ sung toolbar, focus/hover state và empty state rõ ràng cho các tab.
- Panel liên quan ở danh sách Cơ hội có layout riêng gồm hàng thao tác, hàng tab và
  vùng nội dung cuộn; không còn bị kéo giãn tab hoặc đẩy bình luận xuống cuối panel.
- Tab Hoạt động tại panel danh sách chỉ đọc dữ liệu đã có, không hiển thị ô nhập và
  gửi ghi chú trực tiếp; thao tác thêm mới được thực hiện trong trang chi tiết.

## Kiểm tra

- `npm run build`: pass.
- Python compile và `git diff --check`: pass.
- API smoke test với `CRM-OPP-2026-00010`: số tiền `4.000.000`, một Sales Order
  liên kết `SAL-ORD-2026-00010`.
- Asset `/assets/dcnet_crm/dist/crm.bundle.js` trả về thành công.
