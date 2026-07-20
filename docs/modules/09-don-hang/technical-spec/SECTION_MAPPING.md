# Module: Sales Order - Section Mapping Table

**Spec gốc:** `docs/feature/ERP_SPECIFICATION.md` Section 2: Quản lý Bán hàng

**Date created:** 2026-01-14

---

## Quy trình Bán buôn (12 bước)

| # | Section | Tiêu đề đầy đủ | Line | Status | File đích | Use Case |
|---|---------|----------------|------|--------|-----------|----------|
| 2.1 | Bước 1 | Kế hoạch bán hàng theo năm | 50-56 | ⏳ | ORDER_SPEC.md | UC-01 |
| 2.2 | Bước 2 | Bảng giá bán niêm yết | 58-70 | ⏳ | ORDER_SPEC.md | UC-02 |
| 2.3 | Bước 3 | Chính sách chiết khấu bán buôn | 72-84 | ⏳ | ORDER_SPEC.md | UC-03 |
| 2.4 | Bước 4 | **Đơn đặt hàng bán (CORE)** | 86-100 | ⏳ | ORDER_SPEC.md, ORDER_WORKFLOW.md | UC-04 |
| 2.5 | Bước 5 | Kiểm tra tồn kho | 102-108 | ⏳ | ORDER_WORKFLOW.md | UC-05 |
| 2.6 | Bước 6 | Lệnh xuất hàng | 110-134 | ⏳ | ORDER_WORKFLOW.md | UC-06 |
| 2.7 | Bước 7 | Kiểm tra hạn mức công nợ | 136-150 | ⏳ | ORDER_WORKFLOW.md | UC-07 |
| 2.8 | Bước 8 | Kiểm tra công nợ quá hạn | 152-162 | ⏳ | ORDER_WORKFLOW.md | UC-08 |
| 2.9 | Bước 9 | Hóa đơn bán buôn | 164-182 | ⏳ | ORDER_WORKFLOW.md | UC-09 |
| 2.10 | Bước 10 | Lệnh nhập hàng trả lại | 184-201 | ⏳ | ORDER_WORKFLOW.md | UC-10 |
| 2.11 | Bước 11 | Hàng bán bị trả lại | 203-218 | ⏳ | ORDER_WORKFLOW.md | UC-11 |
| 2.12 | Bước 12 | Tính thưởng đạt kế hoạch doanh số | 220-226 | ⏳ | ORDER_WORKFLOW.md | UC-12 |

---

## Quy trình Bán lẻ (3 bước)

| # | Section | Tiêu đề đầy đủ | Line | Status | File đích | Use Case |
|---|---------|----------------|------|--------|-----------|----------|
| 2.13 | Bước 1 | Bảng giá bán niêm yết (Bán lẻ) | 232-238 | ⏳ | ORDER_SPEC.md | UC-13 |
| 2.14 | Bước 2 | Chính sách chiết khấu bán lẻ | 240-252 | ⏳ | ORDER_SPEC.md | UC-14 |
| 2.15 | Bước 3 | Hóa đơn bán lẻ | 254-267 | ⏳ | ORDER_WORKFLOW.md | UC-15 |

---

## Danh mục liên quan

| # | Section | Tiêu đề đầy đủ | Line | Status | File đích | Use Case |
|---|---------|----------------|------|--------|-----------|----------|
| 2.16 | Danh mục | Danh mục đối tượng (Khách hàng) | 273-277 | ⏳ | ORDER_SPEC.md | Master Data |
| 2.17 | Danh mục | Danh mục vật tư hàng hóa | 279-286 | ⏳ | ORDER_SPEC.md | Master Data |
| 2.18 | Danh mục | Kế hoạch doanh số năm | 288-296 | ⏳ | ORDER_SPEC.md | Master Data |

---

## Tổng kết

**Total sections:** 18
- Quy trình Bán buôn: 12 bước (2.1 - 2.12)
- Quy trình Bán lẻ: 3 bước (2.13 - 2.15)
- Danh mục liên quan: 3 items (2.16 - 2.18)

**Core Sales Order:** Bước 4 (line 86-100) - Đơn đặt hàng bán

**Coverage target:** 18/18 sections (100%)

---

## Chú thích

- ⏳ Chưa làm
- 🔄 Đang làm
- ✅ Đã xong
- ❌ Bỏ qua (ghi lý do)

---

**Source:** ERP_SPECIFICATION.md Section 2 (lines 46-298)
