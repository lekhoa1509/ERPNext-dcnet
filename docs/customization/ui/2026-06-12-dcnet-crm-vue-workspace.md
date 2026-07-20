# DCNET CRM Vue Workspace

**Ngày:** 12/06/2026

## Nguồn

- Yêu cầu nghiệp vụ: `docs/feature/FEATURE_SPECIFICATION.md`
- Phân tích đối thủ: `docs/competitor-analysis/misa-amis/crm/ANALYSIS.md`
- Video tham khảo: `videos crm/`
- Design spec: `docs/superpowers/specs/2026-06-12-dcnet-crm-design.md`

## Thay đổi UI

- Tạo Desk Page `/app/dcnet-crm`.
- Tạo sidebar CRM cố định bên trái, nền trắng, icon nét mảnh và active state
  xanh nhạt theo giao diện tham khảo.
- Sidebar gồm: Bàn làm việc, Tiềm năng, Liên hệ, Khách hàng, Cơ hội, Báo giá,
  Đơn hàng, Hoạt động, Thẻ chăm sóc và Tất cả.
- Các mục chưa có nghiệp vụ được đánh dấu disabled, không tự bổ sung chức năng
  ngoài đặc tả khách hàng.
- Tạo tri-pane list: bộ lọc, bảng dữ liệu, activity feed.
- Tạo dashboard hero, KPI có icon/accent, quick actions và funnel cơ hội.
- Empty state có hướng dẫn và CTA thay cho vùng trắng không có ngữ cảnh.
- Chuẩn hóa radius, shadow, spacing và màu semantic trên toàn bộ CRM.
- Responsive: ẩn filter panel dưới 1180px, ẩn activity panel dưới 820px.
- Có focus state, reduced-motion và contrast theo WCAG AA.

## Nguyên tắc

Giao diện học pattern thao tác từ MISA nhưng không sao chép logo, hình ảnh hoặc
source code. Dữ liệu và validation vẫn do DocType chuẩn ERPNext quản lý.
