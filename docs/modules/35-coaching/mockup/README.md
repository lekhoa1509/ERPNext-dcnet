# Coaching Module - UI Mockups

Đây là các mockups UI cho module Coaching của DCNET Flow.

## 📁 Files

### 1. coaching-list-view.mockup.html
**Danh sách đơn Coaching (List View)**

Màn hình hiển thị danh sách tất cả đơn Coaching với đầy đủ thông tin và filters.

**Features:**
- Sidebar navigation
- Search & Filter toolbar
- Table view với các cột:
  - Mã đơn (COACH-YYYYMMDD-XXX)
  - Học viên & SĐT
  - Gói học & HLV
  - Trạng thái (8 loại với badges màu)
  - Tiến trình (progress bar)
  - Sân tập, Còn nợ, Ngày bắt đầu
- Pagination
- Calendar view option

**Trạng thái đơn:**
- 🆕 Mới
- ✅ Đã test
- 💬 Đã tư vấn
- 💳 Đã thanh toán
- 📚 Đang học
- ⏸️ Tạm dừng
- ✔️ Hoàn thành
- ❌ Hủy

---

### 2. coaching-form-view.mockup.html
**Form tạo/sửa đơn Coaching (7 tabs)**

Form chi tiết để tạo mới hoặc chỉnh sửa đơn Coaching.

**Tabs:**

**Tab 1: Thông tin học viên**
- Thông tin cá nhân (họ tên, SĐT, email, ngày sinh)
- Trình độ hiện tại & Handicap
- Mục tiêu học

**Tab 2: Bài test đầu vào**
- Ngày test & HLV thực hiện
- Trình độ đánh giá
- Điểm số (nếu có)
- Nhận xét chi tiết
- Đề xuất gói học

**Tab 3: Thông số kỹ thuật**
- Thông số cơ thể (chiều cao, cân nặng, size tay)
- Thông số kỹ thuật:
  - Tốc độ đầu gậy & tốc độ bóng
  - Hình swing (Inside-out, Outside-in, Square)
  - Đường bóng (Straight, Draw, Fade, Hook, Slice)
  - Khoảng cách gậy sắt & driver
- Tình trạng bộ gậy hiện tại
- Nhu cầu riêng

**Tab 4: Đăng ký khóa học**
- Chọn gói huấn luyện (với giá)
- HLV phụ trách (với rating)
- Sân tập
- Ngày bắt đầu dự kiến
- Mã ưu đãi
- Hình thức thanh toán (Trọn gói/Đặt cọc/Theo buổi)
- Payment Summary (học phí, giảm giá, VAT, tổng)

**Tab 5: Lịch học**
- Table lịch các buổi học
- Thông tin: Buổi, Ngày, Giờ, HLV, Sân, Trạng thái
- Button tùy chỉnh lịch học

**Tab 6: Tiến trình**
- Timeline lịch sử học tập
- Ghi chú từng buổi học
- Nhận xét của HLV

**Tab 7: Thanh toán**
- Tổng quan thanh toán (Tổng học phí, Đã thanh toán, Còn nợ)
- Lịch sử thanh toán (table)
- Button thêm thanh toán

---

### 3. coach-dashboard.mockup.html
**Dashboard dành cho Huấn luyện viên**

Màn hình dashboard tổng quan cho HLV.

**Components:**

**Header:**
- Coach info với avatar & rating
- Date filter (Hôm nay/Tuần này/Tháng này)

**Stats Grid (4 cards):**
- 👥 Học viên đang dạy
- 📚 Buổi dạy tháng này
- 💰 Doanh thu tháng
- ✅ Tỉ lệ hoàn thành

**Lịch dạy hôm nay:**
- Danh sách các buổi học trong ngày
- Thông tin: Giờ, Học viên, Sân tập, Buổi thứ mấy
- Action buttons: Điểm danh, Ghi chú, Chi tiết

**Tiến độ học viên:**
- Danh sách học viên với progress bar
- Hiển thị số buổi đã học / tổng buổi

**Quick Stats:**
- Buổi hôm nay
- Buổi tuần này
- Học viên mới
- Sắp hoàn thành

**Mini Calendar:**
- Tháng hiện tại
- Highlight ngày có buổi học (màu xanh)
- Highlight ngày hôm nay

---

## 🎨 Design System

**Framework:** Frappe UI (Vue 3 + Tailwind CSS)

**Colors:**
- Primary: `#0289F7` (Blue)
- Success: `#46B37E` (Green)
- Warning: `#E79913` (Amber)
- Error: `#E03636` (Red)

**Typography:**
- Font: Inter Variable
- Sizes: 11px - 28px
- Weights: 420 (regular), 500 (medium), 600 (semibold), 700 (bold)

**Spacing:**
- Scale: 4px, 8px, 12px, 16px, 24px, 32px

**Border Radius:**
- sm: 4px
- md: 10px
- lg: 12px

**Shadows:**
- sm: `0px 1px 2px rgba(0, 0, 0, 0.1)`
- md: `0px 0.5px 2px rgba(0, 0, 0, 0.15), 0px 2px 3px rgba(0, 0, 0, 0.16)`

---

## 🖥️ Cách xem Mockups

### 1. Mở landing page (khuyến nghị):
```bash
open docs/mockups/coaching/index.html
```

### 2. Mở trực tiếp từng mockup:
```bash
cd docs/mockups/coaching/

open coaching-list-view.mockup.html
open coaching-form-view.mockup.html
open coach-dashboard.mockup.html
```

### 3. Hoặc sử dụng VS Code Live Server:
- Right-click file → "Open with Live Server"

---

## 📝 Notes

- Tất cả mockups đều responsive với layout 2 cột
- Sidebar có thể collapse (tương lai)
- Form có validation (visual feedback khi focus)
- Interactive elements: buttons, tabs, progress bars
- Data là mock data, không connect với backend

---

## 🔄 Next Steps

1. ✅ Mockups đã tạo (3 màn hình chính)
2. ⏳ Review với khách hàng
3. ⏳ Adjust based on feedback
4. ⏳ Implement actual UI với Vue 3 + Frappe UI
5. ⏳ Connect với backend API

---

**Created:** 14/01/2026
**Designer:** Claude Code
**Project:** DCNET Flow - Coaching Module
