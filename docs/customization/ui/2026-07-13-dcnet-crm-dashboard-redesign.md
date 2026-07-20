# DCNET CRM Dashboard Redesign

**Ngày:** 13/07/2026  
**App:** `dcnet_crm`  
**Route:** `/desk/dcnet-crm?view=dashboard`

## Phạm vi

Thiết kế lại màn hình tổng quan CRM theo hướng dashboard ERP chuyên nghiệp,
giữ nguyên API và nghiệp vụ hiện có.

Nguồn nghiệp vụ:

- `docs/feature/FEATURE_SPECIFICATION.md` mục 14.1–14.4.
- `docs/modules/dcnet-crm/SPEC_MAPPING.md`.

## Thay đổi giao diện

- Thay banner cũ bằng header điều hành sáng, phân cấp tiêu đề rõ và sửa lỗi màu
  tiêu đề thiếu tương phản.
- Chuẩn hóa năm KPI thành card có icon SVG, mô tả ngắn và điều hướng đến danh
  sách tương ứng.
- Bổ sung nút làm mới với trạng thái đang tải; không thay đổi API dữ liệu.
- Trình bày phễu cơ hội bằng tổng số lượng, tổng giá trị và thanh tỷ trọng theo
  giai đoạn từ chính dữ liệu API hiện có.
- Thiết kế lại quick actions và empty state, giữ nguyên bốn hành động nghiệp vụ.
- Bổ sung responsive cho desktop, tablet, mobile; giữ focus state và
  `prefers-reduced-motion` từ design system dùng chung.

## File thay đổi

- `dcnet-crm/frontend/src/features/dashboard/template.js`
- `dcnet-crm/frontend/src/features/dashboard/composable.js`
- `dcnet-crm/frontend/src/styles.css`
- `dcnet-crm/dcnet_crm/public/dist/crm.bundle.js`

## Kiểm tra

- `npm test` — pass (31 frontend modules, bundle build thành công).
- Không thêm DocType, API hoặc trường dữ liệu mới.
- Không thay đổi công thức KPI phía backend.

## Tinh chỉnh v2 theo ảnh kiểm tra thực tế

- Đổi header sáng thành hero navy có chiều sâu và tương phản rõ hơn.
- Chuyển KPI từ card dọc nhiều khoảng trắng thành card compact ngang.
- Tăng nhịp thị giác cho phễu bằng màu phân biệt từng giai đoạn.
- Chuyển thao tác nhanh sang lưới tile 2×2 trên desktop, tối ưu lại theo
  breakpoint nhỏ hơn.
- Giảm số lượng đường viền, dùng surface và shadow nhẹ để tách lớp nội dung.

## Thiết kế v3 theo dashboard tham chiếu

- Chuyển sang nền xám xanh nhẹ và hệ card trắng tối giản theo bố cục bento.
- Loại bỏ hero; dùng toolbar phẳng với CTA màu vàng cam.
- KPI chuyển sang dạng số lớn, nhãn icon nhỏ và microcopy tương tự mẫu.
- Bổ sung donut cơ cấu cơ hội từ dữ liệu stage thật, kèm legend và bảng phễu
  làm phương án đọc dữ liệu accessible.
- Xếp `Phễu cơ hội`, `Cơ cấu cơ hội` và `Thao tác nhanh` thành lưới 2 cột,
  tự chuyển một cột trên màn hình nhỏ.

## Điều hướng dashboard

- Mục `Bàn làm việc` trong CRM sidebar mở Page `dcnet-crm` với
  `{"view": "dashboard"}`.
- Xóa mục `Tất cả` khỏi sidebar để dashboard chỉ có một điểm truy cập.
- Đồng bộ active state của dashboard sang mục `Bàn làm việc`.

## Sửa lỗi quick actions

- Reset kích thước và layout của wrapper nội dung trong từng quick action.
- Ngăn style icon legacy ép phần chữ xuống chiều rộng 34px.
- Khóa bố cục `icon | nội dung | mũi tên` và ellipsis cho màn hình hẹp.
