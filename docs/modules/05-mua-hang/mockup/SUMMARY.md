# 05 - Mua hàng: Mockup Summary

> **Tạo:** 17/02/2026
> **Design system:** Frappe v16 Espresso Theme

## Danh sách mockup

| File | Màn hình | Tag | Spec ref |
|------|----------|-----|----------|
| `purchase-plan.mockup.html` | Kế hoạch Mua hàng (Form View) | `NEW` | 3.2.1 |
| `delivery-schedule.mockup.html` | Kế hoạch Giao hàng (Form View) | `NEW` | 3.2.3 |
| `bulk-image-import.mockup.html` | Import Ảnh Hàng loạt (Custom Page) | `EXT` | 3.1.2 |
| `index.html` | Landing page (link tới 3 mockup trên) | — | — |

## Thiết kế chính

### 1. Kế hoạch Mua hàng (Purchase Plan)

- **Layout:** Frappe Form View — navbar + sidebar + form content
- **Đặc biệt:** Child table rộng với 12 cột tháng (T1-T12), cuộn ngang
- **Trường đặc thù:** Family, Year, Category, Sub Category, Shaft, Loại mua (Purchase/Demo)
- **Data mẫu:** 7 dòng sản phẩm golf Titleist/FootJoy, giá USD
- **Interactive:** Tab switching (Chi tiết / Liên kết / Ghi chú)

### 2. Kế hoạch Giao hàng (Delivery Schedule)

- **Layout:** Frappe Form View — navbar + sidebar + form content
- **Đặc biệt:** Child table rất rộng (~22 cột), import từ Excel hãng Acushnet
- **Cảnh báo:** Highlight dòng vàng khi tên VT từ hãng khác tên trong DCNET
- **Ship Mode badges:** Sea (xanh), Air (cam), Express (đỏ)
- **Data mẫu:** 5 dòng với PO Number, EAN, UPC, Confirm Ship Date
- **Interactive:** Tab switching, nút "Import Excel"

### 3. Import Ảnh Hàng loạt (Bulk Image Import)

- **Layout:** Custom Page — wizard 3 bước
- **Bước 1:** Upload zone (drag & drop hoặc chọn file)
- **Bước 2:** Grid hiển thị kết quả matching — card matched (xanh) vs unmatched (đỏ)
- **Bước 3:** Kết quả import — bảng chi tiết từng file
- **Stats bar:** Tổng file, Khớp, Không khớp, Dung lượng
- **Data mẫu:** 8 file ảnh, 6 khớp mã SP, 2 không khớp
- **Interactive:** Stepper navigation giữa 3 bước

## Quy tắc thiết kế

- Frappe v16 design tokens (colors, typography, spacing, shadows)
- Standalone HTML + inline CSS — mở trực tiếp trong browser
- Vietnamese diacritics cho tất cả nội dung
- Realistic golf equipment data (Titleist, FootJoy)
- ARIA labels và focus-visible cho accessibility
- prefers-reduced-motion media query
- Cursor pointer trên tất cả clickable elements
- Không dùng emoji — chỉ dùng inline SVG icons (Lucide-style)
