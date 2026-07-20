# Spec — Rebuild 3 sidebar sections: Giá thành / Tổng hợp / BCTC

**Date:** 2026-05-11
**Branch:** `feat/giathanh-tonghop-bctc` (19 commits ahead of `78af380`)
**Replaces:** `docs/specs/2026-05-11-giathanh-tonghop-bctc.md` (916 dòng, sonnet — giữ git history, không xoá)
**Context docs:**
- `docs/reviews/2026-05-11-session-handoff-rebuild-4-sections.md`
- `docs/reviews/2026-05-11-sidebar-review-giathanh-tonghop-bctc.md`
- `docs/reviews/2026-05-11-realtime-accounting-conflict-analysis.md`

---

## 1. Decisions (chốt qua brainstorm 2026-05-11)

| # | Decision | Why |
|---|---|---|
| D1 | **DN target: thương mại + dịch vụ.** Drop toàn bộ manufacturing | Tránh real-time conflict + over-engineering cho DN không sản xuất |
| D2 | **3 sổ TT99/2025 (S03a/S03b/Account Detail): rewrite from scratch** | Code sonnet chưa verify layout TT99/2025 Phụ lục IV |
| D3 | **4 BCTC (B01/B02/B03 + B09) + BCTC Mapping: rewrite from scratch + seed default** | Cùng lý do D2, mission-critical (nộp cơ quan thuế) |
| D4 | **Section "Phân tích & Quản trị": DROP khỏi sidebar** | 4 ERPNext native reports nằm rải rác ở các phần khác / search bar |
| D5 | **Cleanup: hard-delete dead code (page/doctype/report/fixtures/tests)** | Tránh dead code làm migrate chậm + nhiễu tree |
| D6 | **PCV: giữ custom field `vn_lock_unlock_reason` + validate hook** | Audit trail VAS — KTT bắt buộc nhập lý do khoá/mở kỳ |
| D7 | **Period closing wizard `period-closing-911`: BỎ (Option A)** | Duplicate ERPNext PCV native, có 3 bug nghiêm trọng (real-time analysis §2.1) |
| D8 | **Implement order: spec → user duyệt → code per section → live test → commit → next** | Tránh multi-session pattern "structurally OK, business wrong" |

---

## 2. Final sidebar shape — 15 items / 3 sections

Hiện tại (sau commit `f0c5e42` + `4fc5302`, theo handoff §1): 6 + 7 + 5 + 4 = **22 items**.

| Section | Final # | Hiện tại # | Drop |
|---|---|---|---|
| Giá thành | 3 | 6 | -3 (mfg-costing-wizard, WIP Valuation, Production Cost Aggregation) |
| Tổng hợp | 7 | 7 | 0 — shape đã đúng, chỉ rewrite content 3 sổ |
| Báo cáo tài chính | 5 | 5 | 0 — shape đã đúng, chỉ rewrite content 4 BCTC + Mapping |
| Phân tích & Quản trị | — | 4 | -4 (drop toàn section) |
| **Total** | **15** | **22** | **-7** |

---

## 3. Section 1 — Giá thành (3 items)

### Sidebar items

| Label | link_type | link_to | Status |
|---|---|---|---|
| Phân bổ chi phí mua hàng | DocType | `Landed Cost Voucher` | ✅ kept |
| Chi phí chờ phân bổ | Report | `Landed Cost Pending Allocation` | ✅ kept |
| Cấu hình phân bổ chi phí mua hàng | DocType | `LCV Allocation Settings` | ✅ kept |

### Keep as-is (per handoff §5)
- Custom fields `vn_is_import_lcv`, `vn_is_subject_to_import_duty` on LCV
- `landed_cost_voucher.js` (155 lines)
- `lcv_hooks.py` + `seed.py` (COA resolver)
- `LCV Allocation Settings` (Single, 11 expense types seeded)
- Helper button "Tạo phiếu VAT NK khấu trừ"

### Hard-delete (Cleanup phase)
```
vn_accounting/costing/                                            # entire dir
vn_accounting/vn_accounting/page/manufacturing_costing_wizard/
vn_accounting/vn_accounting/doctype/work_in_progress_valuation/
vn_accounting/vn_accounting/doctype/manufacturing_costing_settings/
vn_accounting/vn_accounting/report/production_cost_aggregation/
```

Update `hooks.py`: remove any doc_events / scheduler hooks targeting deleted modules (audit grep first).

Update `fixtures/custom_field.json`: remove rows referencing `Work In Progress Valuation` / `Manufacturing Costing Settings` (if any).

Update sidebar JSON `vn_accounting/workspace_sidebar/vn_accounting.json`: remove items linking to `manufacturing-costing-wizard`, `Work In Progress Valuation`, `Production Cost Aggregation`, `BOM`, `Work Order`.

### Live test
1. `/app/landed-cost-voucher/new` → check toggle `vn_is_import_lcv` shows/hides VAT row dynamically
2. Run report `Landed Cost Pending Allocation` → ≥0 rows, no error
3. `/app/lcv-allocation-settings` → 11 expense_type rows seeded
4. Grep `bench --site dcnet.localhost migrate` log → no ModuleNotFoundError from deleted dirs

---

## 4. Section 2 — Tổng hợp (7 items)

### Sidebar items

| Label | link_type | link_to | Source |
|---|---|---|---|
| Đánh giá lại ngoại tệ | DocType | `Exchange Rate Revaluation` | ERPNext native |
| Phiếu khoá sổ kỳ | DocType | `Period Closing Voucher` | ERPNext native + vn hook |
| Định nghĩa kỳ kế toán | DocType | `Accounting Period` | ERPNext native, relabel |
| Sổ nhật ký chung (S03a-DN) | Report | `S03a-DN So Nhat Ky Chung` | Custom **rewrite** |
| Sổ cái (S03b-DN) | Report | `S03b-DN So Cai` | Custom **rewrite** |
| Sổ chi tiết tài khoản | Report | `Account Detail Ledger` | Custom **rewrite** |
| Bảng cân đối số phát sinh | Report | `Trial Balance Sheet` | ERPNext native |

### PCV custom layer (per D6)

**Custom field** on `Period Closing Voucher`:
- `vn_lock_unlock_reason` — Text, reqd=1, label "Lý do khoá/mở kỳ"

**Hooks** in `period_closing/pcv_hooks.py` (already exists, verify only):
- `pcv_validate_vn_requirements(doc, method)` — throw if `vn_lock_unlock_reason` empty at submit
- `pcv_on_submit(doc, method)` — comment to Activity Log: "Khoá kỳ: {reason}"
- `pcv_on_cancel(doc, method)` — comment to Activity Log: "Mở khoá: {reason}"

### 3 sổ TT99/2025 — column spec (Phụ lục IV)

**S03a-DN Sổ nhật ký chung** (Script Report, type=Script)
- Filters: `from_date` (Date, reqd), `to_date` (Date, reqd), `company` (Link Company, reqd)
- Columns (đúng thứ tự Phụ lục IV):
  1. Ngày tháng ghi sổ (`posting_date`)
  2. Chứng từ — Số (`voucher_no`)
  3. Chứng từ — Ngày (`voucher_date`)
  4. Diễn giải (`remarks`)
  5. Đã ghi Sổ Cái (✓ if voucher posted, computed)
  6. STT dòng (running counter per voucher)
  7. Số hiệu TK đối ứng (`against`)
  8. Số phát sinh — Nợ (`debit`)
  9. Số phát sinh — Có (`credit`)
- Footer: tổng cộng Nợ / Có
- Source: `tabGL Entry` filter by date range + company, order by posting_date / voucher_no / idx
- Output xuất Excel theo đúng cột → KTT nộp được luôn

**S03b-DN Sổ cái** (Script Report)
- Filters: `from_date`, `to_date`, `company`, `account` (Link Account, reqd, single TK)
- Columns:
  1. Ngày tháng ghi sổ
  2. Chứng từ — Số
  3. Chứng từ — Ngày
  4. Diễn giải
  5. TK đối ứng
  6. Số phát sinh — Nợ
  7. Số phát sinh — Có
- Opening balance row (số dư đầu kỳ)
- Transaction rows
- Closing balance row (số dư cuối kỳ)
- Source: GL Entry filter by account + date range

**Sổ chi tiết tài khoản** (Script Report)
- Same shape as S03b-DN nhưng thêm cột:
  - Đối tượng (party — customer/supplier name)
  - Bộ phận (cost_center)
  - Tham chiếu (`against_voucher_type/no`)
- Use case: KTT phân tích chi tiết TK 131/331/154 by party / cost_center

### Live test
1. Submit PCV draft không nhập `vn_lock_unlock_reason` → ValidationError "Vui lòng nhập lý do khoá kỳ"
2. Submit PCV với reason "Khoá năm 2025" → success + Activity Log có entry
3. Run S03a-DN cho FY2025 → cột đúng thứ tự Phụ lục IV, tổng Nợ = tổng Có
4. Run S03b-DN cho TK `1111 - Tiền mặt VND - DC` → opening + transactions + closing đúng số
5. Run Account Detail Ledger cho TK 131 → cột Đối tượng hiển thị customer name

---

## 5. Section 3 — Báo cáo tài chính (5 items)

### Sidebar items

| Label | link_type | link_to | Source |
|---|---|---|---|
| Báo cáo tình hình tài chính (B01-DN) | Report | `B01-DN Bao Cao Tinh Hinh Tai Chinh` | Custom **rewrite** |
| Báo cáo kết quả HĐKD (B02-DN) | Report | `B02-DN Bao Cao KQHDKD` | Custom **rewrite** |
| Báo cáo lưu chuyển tiền tệ (B03-DN) | Report | `B03-DN Bao Cao LCTT` | Custom **rewrite** |
| Thuyết minh BCTC (B09-DN) | Page | `b09-dn-generator` | Custom Page **rewrite** |
| Cấu hình BCTC Mapping | DocType | `BCTC Mapping` | Custom DocType **rewrite** |

### BCTC Mapping engine

**DocType `BCTC Mapping`** (1 record per Company per report_code):
- `company` — Link Company, reqd
- `report_code` — Select: B01 / B02 / B03, reqd
- `lines` — child table `BCTC Line`:
  - `line_number` — Data (e.g., "110", "111", "112")
  - `line_label` — Data (VN label)
  - `parent_line` — Data (for indent/sub-total)
  - `accounts` — child table `BCTC Line Account`:
    - `account` — Link Account
    - `sign` — Select: + / − (Cr-Dr or Dr-Cr depending on report)
    - `value_type` — Select: balance / period_movement / closing_only

**Seed** in `bctc/seed.py`: on `after_install` + `after_migrate` (idempotent), for each Company with `country=Vietnam` + has TK 111/112, create 3 BCTC Mapping records (B01 ~50 lines, B02 ~20 lines, B03 ~25 lines) with default account refs per TT99/2025.

KTT có thể override mapping qua UI BCTC Mapping form.

### B01-DN structure (~50 lines)

- **A. TÀI SẢN NGẮN HẠN (100)** = (110) + (120) + (130) + (140) + (150)
  - I. Tiền và tương đương tiền (110) = (111) + (112)
    - 1. Tiền (111) = TK 111+112+113
    - 2. Tương đương tiền (112) = TK 1281+1288 (≤3m)
  - II. Đầu tư tài chính NH (120)
  - III. Phải thu NH (130)
  - IV. Hàng tồn kho (140)
  - V. Tài sản NH khác (150)
- **B. TÀI SẢN DÀI HẠN (200)**
- **TỔNG TÀI SẢN (270) = (100) + (200)**
- **C. NỢ PHẢI TRẢ (300)** = (310) + (330)
- **D. VỐN CHỦ SỞ HỮU (400)** = (410) + (430)
- **TỔNG NGUỒN VỐN (440) = (300) + (400)**
- Assertion: (270) = (440) tolerance ±1000 VND

### B02-DN structure (~20 lines)

- 1. Doanh thu BH&CCDV (01) = Cr TK 511+512
- 2. Các khoản giảm trừ DT (02)
- 3. DT thuần (10) = (01) − (02)
- 4. Giá vốn HB (11) = Dr TK 632
- 5. LN gộp (20) = (10) − (11)
- ... (per Phụ lục II TT99/2025)
- 18. LN sau thuế TNDN (60) = (50) − (51)

### B03-DN — phương pháp gián tiếp (indirect)

- I. Lưu chuyển tiền từ HĐKD (01 → 20)
- II. Lưu chuyển tiền từ HĐ đầu tư (21 → 30)
- III. Lưu chuyển tiền từ HĐ tài chính (31 → 40)
- LCT thuần trong kỳ (50) = (20) + (30) + (40)
- Tiền tồn đầu kỳ (60) = closing TK 111+112+113 đầu kỳ
- Tiền tồn cuối kỳ (70) = (50) + (60) — assertion vs closing GL

Direct method (phương pháp trực tiếp): defer.

### B09-DN multi-sheet Excel

Frappe Page `b09-dn-generator`:
- Filters: company, fiscal_year
- Button "Tạo Excel": generate `.xlsx` with 5 sheets:
  1. Thông tin chung (company info, fiscal year)
  2. Chính sách kế toán áp dụng (template VN, KTT điền tay)
  3. Bổ sung cho B01 (chi tiết TK lớn — 131/331/154/211 v.v.)
  4. Bổ sung cho B02 (chi tiết doanh thu/chi phí lớn)
  5. Bổ sung cho B03 (chi tiết hoạt động đầu tư/tài chính)
- Use `openpyxl` (đã có trong frappe env)
- Save → download

### Live test
1. `/app/bctc-mapping` → seeded 3 BCTC Mapping records cho DCNET, mỗi cái có ~50/20/25 lines
2. Run B01-DN cho `posting_date=2025-12-31, company=DCNET` → (270) = (440) within ±1000 VND
3. Run B02-DN → (60) LN sau thuế khớp với balance TK 421 cuối kỳ
4. Run B03-DN → (70) tiền tồn cuối kỳ khớp với closing TK 111+112+113
5. Mở B09-DN generator → click Tạo Excel → download `.xlsx` 5 sheet, mở được trong LibreOffice

---

## 6. Out of scope (defer / drop)

- Manufacturing items (M2 wizard, WIP Valuation, Production Cost Aggregation, BOM, Work Order)
- `period-closing-911` wizard (D7 — replaced by ERPNext PCV native)
- BC hợp nhất / Consolidated Financial Statement (single-entity only)
- Section "Phân tích & Quản trị" (D4 — 4 native reports via search bar)
- B03-DN phương pháp trực tiếp (chỉ implement gián tiếp)
- TT 627 phân bổ đa tiêu thức 6 tiêu chí
- Hook on Sales Invoice cancel after PCV submit (cancel-after-closing protection — defer)

---

## 7. Implementation order

| Phase | Scope | Files touched | Live test gate |
|---|---|---|---|
| **P0 Cleanup** | Hard-delete dead code + sidebar JSON + hooks.py audit | `costing/`, `mfg_costing_wizard/`, `wip_valuation/`, `mfg_costing_settings/`, `production_cost_aggregation/` | `bench migrate` no error, sidebar không còn 6 items dead |
| **P1 Section 1** | Sidebar restructure only | `workspace_sidebar/vn_accounting.json` | LCV stack 3 items hoạt động |
| **P2 Section 2** | 3 sổ Script Reports + PCV hook verify | `report/s03a_dn*/`, `report/s03b_dn*/`, `report/account_detail_ledger/`, `period_closing/pcv_hooks.py` | 5 live tests §4 pass |
| **P3 Section 3** | BCTC engine + seed + 4 reports/page | `doctype/bctc_mapping*/`, `bctc/seed.py`, `report/b01_dn*/`, `report/b02_dn*/`, `report/b03_dn*/`, `page/b09_dn_generator/` | 5 live tests §5 pass + assertion B01 cân |

Sau mỗi phase: live test → commit → user duyệt → next.

---

## 8. Self-review notes

- Tất cả file path đã verify tồn tại trên disk (find queries).
- LCV stack giữ nguyên 100% — handoff §5 list rõ "đã wire JS + COA resolver, hoạt động".
- PCV hook đã có sẵn ở `period_closing/pcv_hooks.py` — P2 chỉ verify, không viết lại.
- ERPNext native targets (Exchange Revalue / PCV / Accounting Period / Trial Balance Sheet) không cần custom code.
- 3 sổ + 4 BCTC + B09 page là **rewrite** — code sonnet cũ sẽ bị xoá content khi viết mới (giữ file shell + thay nội dung).
- Acceptance criteria là live functional test (browser/UI), không phải structural assert (per handoff §3 lesson).
- Spec dưới 300 dòng (≈260).
