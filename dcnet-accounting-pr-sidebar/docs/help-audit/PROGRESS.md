# VN Accounting — Help Authoring + Frontend Audit (toàn bộ sidebar)

Chuẩn: theo template `help/tien-mat/` (Mục đích / Khi nào dùng / Cách thực hiện / Định khoản tự động / Tình huống đặc biệt & cảnh báo / Báo cáo liên quan / FAQ). Căn cứ code thực tế + VAS TT99/2025. Dùng "ERP" không dùng "ERPNext".

Quy trình mỗi item: frontend check (console/data/UX) → pump data nếu báo cáo rỗng (dcnet_sample, DCNET, đúng lifecycle) → viết/rewrite help → fix lỗi nhẹ inline / flag lỗi nặng.

## Tiến độ theo section (20 sections, 150 link items)
- [x] 1. Tổng quan (1) — help mới + đăng ký page_mapping; dashboard 0 lỗi, dữ liệu đủ
- [x] 2. Tiền mặt (6) — help đã chuẩn (template gốc); verify FE: Cash Receipts/Cash Book/So Noi Bo đều có data, 0 lỗi
- [x] 3. Ngân hàng (11) — help đã có; verify FE: 6 report data đủ (141/73/215/3/6/29 rows), 2 page (bank-reconcile, cash-flow-forecast) 0 lỗi
- [ ] 4. Mua hàng (12)
- [ ] 5. Bán hàng (11)
- [ ] 6. Hợp đồng & PAKD (8)
- [ ] 7. Kho (11)
- [ ] 8. TSCĐ (8)
- [ ] 9. CCDC (7)
- [ ] 10. Tiền lương (11)
- [ ] 11. Giá thành (10)
- [ ] 12. Thuế (7)
- [ ] 13. Tổng hợp (10)
- [ ] 14. Báo cáo tài chính (13)
- [ ] 15. Danh mục (7)
- [ ] 16. Thiết lập (14)
- [ ] 17. Công cụ Import (2)

## Issues found (per section) — điền dần


### Section 1 — Tổng quan
- Dashboard `vn-accounting-dashboard`: 5 KPI + 8 chart + filter Tháng/Quý/Năm/Tuần. 0 console error, KPI có số (DT 1.13B). KHÔNG có vấn đề. Đã viết help/tong-quan/index.md.

### Section 2 — Tiền mặt
- Cash Receipts/Cash Book/So Noi Bo: data đủ (1-7 rows), 0 console error, realtime toggle hoạt động. Help đã đạt chuẩn — không cần viết lại.

### Section 3 — Ngân hàng
- 6 report custom data đủ. bank-reconcile (bank account picker đủ 7 TK NH) + cash-flow-forecast (sources/forecast/history) đều 0 console error. Help 11 article đã có — cần verify code-accuracy (giao subagent rà soát ở batch sau nếu cần).

## TẤT CẢ 17 SECTION ĐÃ VIẾT HELP (2026-05-29, qua 14 subagent song song)
Sections: Tổng quan, Tiền mặt, Ngân hàng, Mua hàng, Bán hàng, Hợp đồng & PAKD, Kho, TSCĐ, CCDC, Tiền lương, Giá thành, Thuế, Tổng hợp, Báo cáo tài chính, Danh mục, Thiết lập, Công cụ Import.
hooks.py vn_help_sources: 74 doctype + 51 report + 6 page mapping (đã verify mọi default_article tồn tại).

## LỖI/PHÁT HIỆN (theo mức độ)
### Đã sửa ngay (minor, hợp lệ VAS)
- [FIXED] S22-DN report: `table_exists("tabCCDC Item")` → `"CCDC Item"` (double-prefix → CCDC luôn 0 dòng dù có 16 CCDC item).
- [FIXED] Asset Stocktake.approve() thiếu @frappe.whitelist() → kế toán không duyệt được kiểm kê (bút toán mất mát Nợ 1381 không ghi). Đã thêm whitelist.
- [FIXED] vn_help precedence: native_items shadow app help → đảo thứ tự (app mapping ưu tiên, native = fallback). 5 doctype core (JE/PE/SI/PI/Asset) giờ hiện help mới.
- [FIXED] hooks cũ map Asset/Journal Entry/Payment Entry/CCDC Item → help/asset|journal_entry|... (thư mục KHÔNG tồn tại = 404). Đã trỏ lại đúng help mới.
- [REMOVED] 3 file help rác ở gốc: ccdc_item.md, ccdc_template.md (mô tả SAI khái niệm = hoa hồng, không phải công cụ dụng cụ), cash_count.md (trùng tien-mat/kiem-ke-quy).

### Cần thảo luận / theo dõi (chưa sửa)
- [SERIOUS] hooks.py có KEY TRÙNG: doc_events["Sales Invoice"] khai 2 lần (auto_source classify_and_register_si BỊ GHI ĐÈ bởi cogs_engine) + permission_query_conditions khai 2 lần. Python giữ bản cuối → hook đăng ký lần đầu mất tác dụng. Cần gộp. (Phát hiện khi sửa hooks; KHÔNG do mình gây ra.)
- [SERIOUS] page `period-closing-911` đã chết (không còn page, chức năng chuyển sang DocType VN Period Close). Đã bỏ khỏi page_mapping, map VN Period Close thay thế.
- [MEDIUM] Cross-app help collision: dcnet_pakd + dcnet_contract tự đăng ký vn_help_sources cho 8 key (DCNET Contract, DCNET Contract Template, Phuong An Kinh Doanh, PAKD Settings, PAKD Reminder Log, Commission Register, Overdue Billing Periods, Outstanding Receivables by Contract). Do merge last-app-wins, help của 2 app này THẮNG help mới của vn_accounting cho 8 key đó. Cần quyết định: gộp về vn_accounting hay giữ per-app.
- [DATA] EInvoice Inward (HĐ GTGT đầu vào): 0 bản ghi trên DCNET → danh sách rỗng. Tờ khai GTGT (vat_return_01_gtgt) VẪN có data (26 dòng). Đề xuất bơm HĐĐT đầu vào mẫu (chưa làm — không gây mất cân đối vì là log sync).
- [DATA] Landed Cost Pending Allocation: 0 dòng (DCNET không treo phụ phí ở TK 1388) — empty hợp lệ, không phải lỗi.
- [MINOR] Sidebar đặt nhầm: "Cài đặt PAKD" + "Lịch sử nhắc duyệt PAKD" nằm trong section Kho (nên ở Hợp đồng/Thiết lập). 2 dòng "Bút toán chung" trùng trong Mua hàng. "Đơn mua/bán cần lập HĐ" = list lọc, không phải doctype riêng. Employee xuất hiện 2 lần.
- [MINOR] Stock Reconciliation TK chênh lệch mặc định = 632 (không phải 1381/3381 theo VAS) — đã hướng dẫn đổi trong help.
- [MINOR] Company DCNET chưa khai TK 413 (chênh lệch tỷ giá chưa thực hiện) — đánh giá lại ngoại tệ rơi vào TK mặc định.
- [MINOR] Budget Variance Report cần Budget docstatus=1 + distribute_equally để có số.
