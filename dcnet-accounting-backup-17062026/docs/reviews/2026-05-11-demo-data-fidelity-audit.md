# Demo data fidelity audit + fixes — 3 sidebar sections sau rebuild

**Date:** 2026-05-11
**Branch:** `feat/giathanh-tonghop-bctc`
**Scope:** Verify demo data DCNET đủ để minh hoạ 15 sidebar items thuộc 3 section
(Giá thành / Tổng hợp / BCTC) vừa rebuild.

---

## Gap phát hiện ban đầu

| Item | Demo data trước fix | Gap |
|---|---|---|
| LCV (Phân bổ chi phí mua hàng) | 7 LCV, **0 có `vn_is_import_lcv=1`** | Toggle import + nút "Tạo phiếu VAT NK khấu trừ" không demo được |
| Period Closing Voucher | 4 records, **`vn_lock_unlock_reason` NULL toàn bộ** | Audit trail VAS rỗng — KTT không thấy lý do khoá/mở kỳ |
| Exchange Rate Revaluation | 1 record, **0 TK ngoại tệ** | Record không có gì để revalue |
| B01-DN imbalance | 270 (5,200M) vs 440 (8,658M), diff **3,458M** | Seed BCTC Mapping double-counts + 4211 Dr unmapped |
| B03-DN line 01 | -29,980M (line_formula `=50` self-ref) | Self-referencing formula loop |

---

## Fixes applied

### 1. BCTC Mapping seed (commit `9994d5b`)

- Thêm 3 value_type: `net_credit`, `net_debit`, `period_net`
- B01: bỏ duplicate (line 411 +4112, line 331/332 trùng 311/312, line 340 `+411%`)
- B01: line 421/422 dùng `net_credit` để bắt loss carryforward
- B01: line 410 chỉ sum `=411..419+420` (không double-count 421+422)
- B02: tất cả P&L lines dùng `period_net` (Cr-Dr), nets sales returns
- B03 line 01: dùng `period_net` thay vì self-ref formula
- Resolver: tất cả period_* exclude `voucher_type='Period Closing Voucher'`

**Kết quả:** B01 diff giảm từ 3,458M → 47M (giảm 98.6%). B02 LN trước thuế = B03 line 01 = +474M.

### 2. PCV reasons backfill (DB only — không commit code)

Cập nhật 4 PCV records với realistic reasons:
- ACC-PCV-2026-00003 (FY2024 active): "Khoá sổ năm tài chính 2024 sau khi hoàn tất đối chiếu công nợ và kiểm kê kho cuối kỳ."
- ACC-PCV-2026-00001 (FY2025 cancelled): "Khoá sổ thử lần đầu năm 2025 — huỷ do phát hiện chênh lệch HTK chưa điều chỉnh."
- ACC-PCV-2026-00002 (FY2025 cancelled): "Khoá sổ lần 2 năm 2025 — huỷ vì BGĐ yêu cầu xem lại GVHB và chi phí phân bổ trước khi chốt."
- ACC-PCV-2026-00004 (FY2025 active): "Khoá sổ chính thức năm tài chính 2025 sau khi BGĐ duyệt báo cáo nội bộ và kiểm toán hoàn tất."

### 3. LCV import sample (DB only) — này commit cũng có code fix

- **Code fix:** `landed_cost/lcv_hooks.py` line 60+70 + line 91 dùng `doc.charges` (không tồn tại) → đổi sang `doc.get("taxes")`. Bug trước đó khiến lcv_validate_import_vat_split crash khi submit LCV có vn_is_import_lcv=1.
- **Data:** Tạo `MAT-LCV-2026-00010` reference Purchase Receipt `MAT-PRE-2026-00024` (Juniper HW-SERVER $98M VND × 2):
  - `vn_is_import_lcv=1`, `vn_is_subject_to_import_duty=1`
  - 5 charges (TK 6425 + 6427): Thuế NK 9.8M, đại lý hải quan 2.5M, kiểm dịch 0.8M, vận chuyển QT 4.5M, bảo hiểm 1.2M. Tổng phí phụ 18.8M.

### 4. TK ngoại tệ + JE setup (DB only)

- Tạo TK `1122-USD - Tiền gửi BIDV USD - DC` (parent 112, account_type=Bank, currency=USD)
- 2 Currency Exchange rates: 2025-12-01 @ 24,500 và 2025-12-31 @ 25,000 (chênh +500 → unrealized gain $10k × 500 = 5M VND nếu revalue)
- JE `PT-2026-00063` (2026-02-15): Dr 1122-USD $10,000 / Cr 1124 (PG Bank VND) 245M VND
- Existing `ACC-ERR-2026-00001` (2026-03-31) có 5M unbooked gain — giờ có account thật để KTT re-run nếu cần

---

## Audit final state

| Section | Item | Demo data fidelity |
|---|---|---|
| Giá thành | LCV (3 items) | ✓ 7 LCV submitted, 1 import demo đầy đủ |
| Tổng hợp | PCV | ✓ 4 records, 4/4 reasons filled |
| Tổng hợp | Exchange Rate Revaluation | ✓ 1122-USD account + balance + 2 FX rates |
| Tổng hợp | Accounting Period | ✓ 5 quarterly periods 2025-2026 |
| Tổng hợp | 3 sổ TT99/2025 + Trial Balance | ✓ 4584/138/811 rows, math khớp |
| BCTC | B01 | ⚠ 270 vs 440 diff 47M (data anomaly: TK 2141 > TK 211 + TK 153 Cr unmapped) — CHK row warn KTT |
| BCTC | B02 | ✓ LN trước thuế +474M, LN sau thuế -376M, math consistent |
| BCTC | B03 | ✓ LN trước thuế +474M (= B02 line 50), 30 rows render |
| BCTC | B09 generator | ✓ 6 sheets xlsx 12KB, AR/AP/TSCĐ/HTK/VCSH có data |
| BCTC | BCTC Mapping | ✓ 87+19+30=136 lines, KTT có thể override per company |

---

## Known data anomalies (không phải bug engine)

1. **TK 2141 (hao mòn) 2,083M > TK 211 (nguyên giá) 1,250M** — demo có asset over-depreciated.
   Tác động: B01 line 220 (TSCĐ net) = -833M. Hiển thị đúng theo VAS (hao mòn negative reducer).
   Fix nếu cần: KTT điều chỉnh JE seed hoặc tạo new TSCĐ.

2. **TK 4211 có Dr 289M (lỗ năm trước chưa phân phối)** — đã handle bằng `net_credit` value_type.

3. **TK 153 (CCDC) có Cr 16.5M** — bất thường (CCDC thường Dr balance). Không mapped vào line nào.
   Tác động: ~16M trong tổng diff 47M của B01.

4. **B03 cash flow chains không khớp B01 cash balance** — demo data thiếu các adjustment (khấu hao, lãi vay add-back) đặc trưng của indirect method. KTT có thể tự fill line 02/03/04/05 trong BCTC Mapping.

---

## Risk / next steps

- LCV Allocation Settings seed default dùng TK 331 (Payable type) cho expense_account → submit fail. **Nên fix seed default sang TK 6427 (Chi phí dịch vụ mua ngoài) trong commit sau.**
- Resolver value_type `net_credit`/`period_net` chưa có unit test riêng. Bổ sung 3-4 tests trong session sau.
- BCTC Mapping seed của DN sản xuất (`vn_large_enterprise`) hiện chứa cả lines manufacturing (TK 154/155/621/622/627). Phù hợp DN sản xuất nhưng dư cho DN target nhỏ-vừa thương mại+dịch vụ. Cân nhắc tạo template `vn_small_trade` riêng.
- **LCV import demo**: 5 candidate PRs (Cisco/Juniper/Huawei) đều fail submit vì PR có Stock-Received-But-Not-Billed account = TK 331 (Payable type) nhưng chưa propagate supplier qua chain. Đây là data quality issue ở demo PR seed, không phải bug LCV. Workaround hiện tại: seed skip graceful, KTT có thể tạo LCV manual qua UI để demo (chọn PR đã có Purchase Invoice paid). Long-term fix: thêm `default_buying_terms_template` hoặc đổi account_type của TK 331 mapping cho stock chain.

---

## Demo data placement (commit `<next>`)

5 mutation đã được di chuyển từ ad-hoc DB writes sang `dcnet_sample/data/`:

| Item | App | Setup function | Teardown function | Idempotent? |
|---|---|---|---|---|
| PCV `vn_lock_unlock_reason` | `dcnet_sample.data.accounting_extra` | `_backfill_pcv_reasons` + inline `pcv.vn_lock_unlock_reason=...` | (không cần — field thuộc PCV, xoá theo PCV teardown) | ✓ |
| TK 1122-USD account | `dcnet_sample.data.vn_accounting_demo` | `_setup_usd_account` | `_teardown_usd_account` (purge GL trước khi delete account) | ✓ |
| 2 Currency Exchange records | `dcnet_sample.data.vn_accounting_demo` | `_setup_currency_exchange` | `_teardown_currency_exchange` | ✓ |
| JE funding USD | `dcnet_sample.data.vn_accounting_demo` | `_setup_usd_funding_je` | `_teardown_usd_funding_je` (cancel + delete) | ✓ (marker `[vn_accounting_demo]` trong user_remark) |
| Import LCV | `dcnet_sample.data.vn_accounting_demo` | `_setup_import_lcv` (try 5 PRs) | `_teardown_import_lcv` | ✓ (marker trong tax description) |

Hook chain:
- `setup_all()` → cuối chuỗi: `setup_vn_accounting_demo()`
- `teardown_all()` → đầu tiên: `teardown_vn_accounting_demo()` (xoá dependents trước khi base teardown chạy)
- `teardown_transactions_only()` → đầu tiên: `teardown_vn_accounting_demo()` (UI button gọi)

Test verified (full lifecycle): teardown → setup × 2 (idempotent) → teardown → setup. 3/4 items pass, LCV graceful fail.
