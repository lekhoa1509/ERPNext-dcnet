# Coaching Module - Research & Mockup Summary

**Date:** 14/01/2026
**Task:** Research Frappe LMS + Create UI Mockups cho module Coaching

---

## 📊 Research Summary: Frappe LMS vs DCNET Coaching

### Kết luận chính: ❌ KHÔNG NÊN tích hợp Frappe LMS

**Lý do:**

1. **❌ GAP nghiêm trọng: Sales Order Integration**
   - LMS sử dụng `LMS Payment` riêng, KHÔNG tích hợp với ERPNext Sales Order
   - Không đồng bộ với accounting ledger, inventory, payment entry
   - Cần refactor toàn bộ payment system nếu muốn tích hợp

2. **❌ Thiếu features đặc thù coaching:**
   - Không có session-by-session tracking
   - Không có attendance/điểm danh chi tiết
   - Không có coaching specs (thông số kỹ thuật golf)
   - Không có bài test đầu vào
   - Không có đánh giá định kỳ

3. **❌ Overhead không cần thiết:**
   - LMS mang theo nhiều features không dùng (online course builder, quizzes, assignments, forums...)
   - Tăng complexity và maintenance burden

4. **✅ Effort:**
   - Customize LMS: ~15-20 ngày + risk cao
   - Build custom module: ~14 ngày + full control

### Khuyến nghị: ✅ Build Custom Module `dcnet/coaching`

**Ưu điểm:**
- Native ERPNext integration (Sales Order, Payment Entry, Accounting)
- Full control workflow
- Chỉ build những gì cần
- Maintainable & scalable
- Có thể học patterns tốt từ LMS nhưng không fork code

---

## 🎨 UI Mockups Created

### 1. Coaching List View
**File:** `coaching-list-view.mockup.html`

**Features:**
- Sidebar navigation
- Search & Filter toolbar
- Table view với 11 cột thông tin
- 8 trạng thái đơn với badges màu sắc
- Progress bar cho tiến trình học
- Pagination

**Highlights:**
- Code format: `COACH-YYYYMMDD-XXX`
- Hiển thị còn nợ (màu đỏ nếu có)
- Progress bar visual: `4/8 buổi`

### 2. Coaching Form View (7 tabs)
**File:** `coaching-form-view.mockup.html`

**Tabs:**
1. **Thông tin học viên** - Personal info, trình độ, mục tiêu
2. **Bài test đầu vào** - Test date, HLV, kết quả, đề xuất gói
3. **Thông số kỹ thuật** - 14+ fields (chiều cao, club speed, swing, ball flight...)
4. **Đăng ký khóa học** - Gói, HLV, sân, payment summary (với VAT)
5. **Lịch học** - Session table với trạng thái
6. **Tiến trình** - Timeline với ghi chú từng buổi
7. **Thanh toán** - Payment summary, lịch sử thanh toán

**Highlights:**
- Tab navigation interactive (JavaScript)
- Payment summary: Học phí + Giảm giá + VAT = Tổng
- Timeline component cho progress tracking
- Alert boxes (info/warning)

### 3. Coach Dashboard
**File:** `coach-dashboard.mockup.html`

**Components:**
- Coach info header (avatar, rating ⭐ 4.8)
- 4 stat cards: Học viên, Buổi dạy, Doanh thu, Tỉ lệ hoàn thành
- Lịch dạy hôm nay (với action buttons: điểm danh, ghi chú, chi tiết)
- Tiến độ học viên (progress bars)
- Quick stats sidebar
- Mini calendar (highlight ngày có buổi học)

**Highlights:**
- Real-time stats với % change indicators
- Schedule với time slot visual
- Interactive calendar
- Coach-focused UX

### 4. Landing Page
**File:** `index.html`

- Card preview cho cả 3 mockups
- Quick navigation
- Design system colors showcase
- Link to documentation

---

## 🎨 Design System Applied

**Framework:** Frappe UI (Vue 3 + Tailwind CSS)

**Colors:**
- Primary: `#0289F7` (Blue) - Actions, links
- Success: `#46B37E` (Green) - Completed states
- Warning: `#E79913` (Amber) - Paused, pending
- Error: `#E03636` (Red) - Cancelled, debts

**Typography:**
- Font: Inter Variable
- Sizes: 11px - 36px
- Weights: 420 (regular), 500 (medium), 600 (semibold), 700 (bold)

**Components:**
- Buttons: 32px height, rounded-md (10px)
- Form inputs: 36px height, focus ring
- Badges: 11px font, subtle backgrounds
- Cards: White bg, shadow-sm
- Tables: Hover effects, alternating rows

---

## 📁 Files Structure

```
docs/mockups/coaching/
├── index.html                          # Landing page
├── README.md                           # Documentation
├── SUMMARY.md                          # This file
├── coaching-list-view.mockup.html      # List View (156 đơn)
├── coaching-form-view.mockup.html      # Form with 7 tabs
└── coach-dashboard.mockup.html         # HLV Dashboard
```

---

## 📊 Statistics

**Files Created:** 6 files
**Lines of Code:** ~1,800 lines (HTML + CSS)
**Mockups:** 3 main screens
**Components:** 50+ UI components
**Colors Used:** 12 semantic colors
**Time Spent:** ~3 hours

---

## 🔄 Next Steps

### Phase 1: Review & Feedback
1. ⏳ Present mockups to customer/team
2. ⏳ Gather feedback on UI/UX
3. ⏳ Adjust based on feedback

### Phase 2: Data Model Design
1. ⏳ Finalize ERD (7 main entities)
2. ⏳ Define relationships
3. ⏳ Plan migrations

### Phase 3: Implementation
1. ⏳ Create DocTypes (Coaching Order, Package, Coach, Golf Course, Test, Session, Specs)
2. ⏳ Implement business logic
3. ⏳ Build frontend UI (Vue 3 + Frappe UI)
4. ⏳ Sales Order integration
5. ⏳ Reports & Dashboard

**Estimated Effort:** 14 ngày (2-3 sprints)

---

## 📝 Key Decisions Made

| Decision | Rationale |
|----------|-----------|
| ❌ Không dùng Frappe LMS | Gap lớn về Sales Order integration, thiếu features, overhead |
| ✅ Build custom module | Full control, native integration, maintainable |
| ✅ 7 tabs trong form | Tổ chức thông tin rõ ràng, tránh overwhelm |
| ✅ Separate Coach Dashboard | HLV có workflow riêng, cần UI riêng |
| ✅ Progress bar visual | User-friendly, dễ tracking tiến trình |
| ✅ 8 trạng thái đơn | Cover đầy đủ lifecycle từ đăng ký → hoàn thành |

---

## 💡 Lessons Learned

1. **Frappe LMS patterns tốt:**
   - Batch/Enrollment model rõ ràng
   - Certificate management
   - Progress tracking structure

2. **Cần customize cho golf coaching:**
   - Session-level tracking quan trọng
   - Thông số kỹ thuật specific
   - Link với Sales Order là must-have

3. **Design system consistency:**
   - Follow Frappe UI giúp integrate dễ dàng
   - Reuse components giảm development time

---

## 🔗 References

- **Research Report:** Session conversation history
- **Coaching Requirements:** `docs/feature/FEATURE_SPECIFICATION.md` (Section 17)
- **Business Docs:** `docs/modules/coaching/*.md`
- **Frappe LMS Source:** `/Users/vovanduc/Code/dcnet/lms`
- **Design System:** `dcnet_crm/frontend/node_modules/frappe-ui/`

---

**Completed by:** Claude Code
**Date:** 14/01/2026
**Status:** ✅ Research & Mockups Completed - Ready for Review
