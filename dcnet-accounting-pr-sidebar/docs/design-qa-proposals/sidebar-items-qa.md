## Session 2026-04-22 08:28 — Sidebar Items Design QA

### Scope
Rà soát tất cả sidebar items trong VN Accounting workspace sidebar, kiểm tra mỗi item có mở đúng nội dung theo ý nghĩa label không.

### Summary
- **Total items:** 84 active + 10 pending = 94
- **Tested:** 84 active items
- **Skipped:** 10 items `[Pending]` → link tới page `under-development` (đúng thiết kế)
- **Result:** 80 OK, 4 findings

### Findings

| # | Section | Item | Severity | Issue | Suggested Fix |
|---|---------|------|----------|-------|---------------|
| 1 | Danh mục | Hệ thống tài khoản | **HIGH** | 404 "Không tìm thấy" — `link_type: Page, link_to: app/accounts/chart-of-accounts` → Frappe prefix `/desk/` → URL thành `/desk/app/accounts/...` → page không tồn tại | Đổi sang `link_type: URL, url: /app/accounts/chart-of-accounts` hoặc `link_type: DocType, link_to: Account` (tree view) |
| 2 | Tài sản cố định | Ghi tăng TSCĐ vs Thanh lý TSCĐ | **MEDIUM** | Cả 2 items đều link tới `/desk/asset` list **không có route_options phân biệt**. Click "Thanh lý TSCĐ" thấy tất cả assets, không filter thanh lý | Thêm `route_options: {"status": "Sold"}` cho Thanh lý TSCĐ |
| 3 | Công cụ dụng cụ | Ghi tăng CCDC & Phân bổ CCDC | **MEDIUM** | "Ghi tăng CCDC" → Asset list chung (không filter asset_category cho CCDC). "Phân bổ CCDC" → Journal Entry list chung (không filter). User không phân biệt CCDC vs TSCĐ | Thêm route_options filter phù hợp (asset_category cho CCDC, voucher_type cho JE) |
| 4 | Giá thành | Tập hợp chi phí SX | **LOW** | Label "Tập hợp chi phí SX" (cost accumulation) nhưng mở BOM list (Bill of Materials = định mức vật tư). BOM phục vụ tính giá thành nhưng bản chất là định mức, label hơi misleading | Đổi label thành "Định mức vật tư (BOM)" hoặc giữ nguyên nếu quy ước nội bộ |

### Section-by-section Results

| Section | Items tested | Status | Notes |
|---------|-------------|--------|-------|
| Tổng quan | 1 | OK | Dashboard page load đúng |
| Quỹ tiền mặt | 6 | OK | Reports + Cash Count + Forecast + JE filtered |
| Ngân hàng | 9 | OK | Reports + Bank Reconcile + Term Deposit + Bank Loan |
| Mua hàng | 10 | OK | PO/PI/PR + returns filter + reports |
| Bán hàng | 8+1pending | OK | Quotation/SO/SI + returns filter + reports |
| Kho | 11 | OK | 5 Stock Entry types filtered + reports |
| Tài sản cố định | 6 | **2 findings** | Ghi tăng vs Thanh lý cùng URL không filter |
| Công cụ dụng cụ | 3+1pending | **2 findings** | CCDC items thiếu filter phân biệt với TSCĐ |
| Tiền lương | 4+2pending | OK | |
| Giá thành | 2+1pending | **1 finding** | Label "Tập hợp chi phí SX" vs BOM |
| Thuế | 2+1pending | OK | Purchase/Sales Register đúng mapping VN |
| Tổng hợp | 6 | OK | JE + Period Closing + GL + Trial Balance Sheet |
| Báo cáo tài chính | 9+4pending | OK | BS, P&L, Cash Flow, ratios, consolidated |
| Danh mục | 6 | **1 finding** | Hệ thống tài khoản 404 |
| Thiết lập | 7 | OK | All settings pages load correctly |

### Console Errors
Chỉ socket.io 404 (bình thường ở dev mode, không chạy socketio server). Không có business logic errors.

### Priority
1. Fix #1 (HIGH) ngay — user không truy cập được Chart of Accounts từ sidebar
2. Fix #2-3 (MEDIUM) — cải thiện UX cho kế toán viên
3. Fix #4 (LOW) — label adjustment, có thể giữ nếu quy ước nội bộ

---

## Session 2026-04-22 16:20 — Re-QA After Fixes

### Changes Applied
| # | Fix | Detail |
|---|-----|--------|
| 1 | Hệ thống tài khoản | `link_type: Page` → `link_type: DocType, link_to: Account` (tree view) |
| 2 | Thanh lý TSCĐ | Added `route_options: {"status": "Sold"}` |
| 3a | Ghi tăng CCDC | Added `route_options: {"asset_category": "CCDC"}` |
| 3b | Phân bổ CCDC | Added `route_options: {"voucher_type": "Depreciation Entry"}` |
| 4 | Label BOM | "Tập hợp chi phí SX" → "Định mức vật tư (BOM)" |

### Re-QA Results (Playwright MCP)
| # | Item | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 1 | Hệ thống tài khoản | Account tree view, no 404 | `/desk/account`, title "Hệ thống Tài khoản" | **PASS** |
| 2 | Thanh lý TSCĐ | Asset list filtered by Sold | `/desk/asset/view/list?status=Sold`, dropdown "Đã bán" selected | **PASS** |
| 3a | Ghi tăng CCDC | Asset list filtered by CCDC category | `/desk/asset/view/list?asset_category=CCDC` | **PASS** |
| 3b | Phân bổ CCDC | JE list filtered by Depreciation Entry | `/desk/journal-entry/view/list?voucher_type=Depreciation%20Entry` | **PASS** |
| 4 | Label BOM | "Định mức vật tư (BOM)" | Sidebar shows "Định mức vật tư (BOM)" | **PASS** |

### Console Errors
0 errors during re-QA (only socket.io 404 in dev mode — expected).

### Verdict
All 4 findings resolved. 84/84 active sidebar items now correct.
