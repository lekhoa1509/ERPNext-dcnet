# bulk_pump SQL — Deep-Quality Audit (DCNET TEST, batch MM-2026-01018)

Date: 2026-05-26
Branch: `feature/misa-migration-perf-and-recovery` (head 04148f9e on dcnet/develop)
Reviewer: Claude (Opus 4.7) — read-only audit, no commits.

## TL;DR

Pump succeeds at the **mechanical** layer (no orphan FKs, all docs at docstatus=1, JEs balanced, AR/AP allocation drain consistent, Trial Balance reconciles to 11 VND across 48,641 GL rows). It **fails the economic layer** for two whole document classes:

1. **Stock Entry** — every Material Issue (808/808) and every Material Receipt that has GL (251/251) posts `Dr 632 / Cr 632` on the *same* account, net zero. Inventory accounts (TK 152x/155x/156x) are never touched. Bin reports **8.28B VND** of stock; GL inventory total is **2.77B VND**. **5.51B VND of inventory exists in SLE/Bin but is invisible to the balance sheet.** TK 1551 ends at **−47.5M VND** (impossible for an asset). 68 Material Receipts have no GL at all, and 236 Material Transfers have no GL at all.
2. **Purchase Invoice** — **48.9% of item value (11.75B VND of 24.06B)** is routed to `expense_account = TK 1331` (input-VAT refund) instead of a real expense account. The supplier credit (TK 331) and the VAT tax row are correct; only the cost-side debit is mis-routed. Net effect: **11.75B VND of cost is sitting on an asset/refund account instead of P&L.** P&L Net Income is overstated by the same number; VAT-input ledger is inflated by the same number.

Headline numbers (Dr=Cr balance, allocation drain) hide both bugs because they are internally consistent — the books *look* balanced, they just don't *mean* what an accountant would assume.

Outside of those two, the audit is positive: relationships clean, masters reused without duplication, depreciation schedules generated for all 175 Assets, payment allocations consistent for 500/500 SI + 500/500 PI sampled.

---

## Area 1 — Why ~2,400 rows are still Ready

**Posted vs Ready vs Skipped vs Conflict** breakdown (batch MM-2026-01018):

| Category | file_types | Total Ready | Root cause | Recommended action |
|---|---|---|---|---|
| **Master/config rows (by design)** | Account, Asset Category, Bank, Bank Account, CCDC Category, Cost Center, Customer, Customer Group, Department, Employee, Item, Item Group, Misa Closing Rule, Misa Default Account, Project, Supplier, UOM, Warehouse | ~3,500 | Masters created in the prior ORM Misa Migration phase. bulk_pump only handles transactions. Status stayed Ready because the SQL path never re-touched them. | **Accept as config-only.** Either backfill the rows to "Posted" with a one-shot script for cosmetic cleanliness, or leave them — they have no economic impact. |
| **OB rows (unposted)** | OB Account Balance, OB Bank Balance, OB CCDC, OB Customer AR, OB Employee Advance, OB Fixed Asset, OB Inventory, OB Prepaid Expense, OB Supplier AP | 1,792 | Opening Balance rows are NOT posted by bulk_pump. The opening JEs that ARE on GL (197 JEs, 154.83B Dr=Cr at posting_date<2025-01-01) appear to be from an earlier separate flow. | **Surface to user / decision.** AR/AP totals don't reconcile because of unposted OB AR (64) + OB AP (102). Either (a) post these via a separate flow, or (b) accept that AR/AP starts from go-live and pre-migration carry-forward lives in the opening JEs. |
| **Unknown (resource/currency tax reference data)** | Unknown × 1,375 | 1,375 | These are tax-resource rates (rock, coal, timber rates with `Thuế suất(%)` field) and currency rate sheets from Misa export. The parser classified them as Unknown because the sheet doesn't match any known mapper. They are MASTER reference data, not transactions. | **Re-classify in parser**: rename file_type to "Tax Resource Rate" / "Currency Rate" and route to specific (no-op) handlers so they show "Skipped: reference-only" instead of "Ready unknown". No economic impact either way. |
| **NKC "NVK20250331" with empty Dr/Cr/amt** | NKC × 53 (52 of them named NVK20250331) | 53 | All 52 rows share voucher_no `NVK20250331`, posting_date 2025-12-31, with `Tài khoản Nợ`, `Tài khoản Có`, `Số tiền` all empty. These look like header rows of a year-end consolidated JE where the line data lives in subsequent rows the parser didn't aggregate, OR rows the parser failed to read amounts from. | **Open per-row investigation.** Compare against the original Misa NKC export sheet for voucher NVK20250331 to determine if the values exist in the source. If yes → parser bug. If no → source-data gap (mark Skipped). |
| **NKC "Pre-skipped: source-data gap"** | NKC × 40 (all voucher BH20252600) | 40 | Sales invoices BH20252600 with empty invoice number — recently-issued, awaits Misa to fill in. | **Accept.** Skip-on-source-gap is the intended behavior. Surface count in pump UI summary. |
| **SCT (stock movements) with qty=0** | SCT × 483 (CK020/PNN20/PN202/PXN20/PNDNG prefix mix) | 483 | All sampled SCT rows show qty=0. They appear to be header rows of multi-line stock vouchers that already got processed as item lines OR rows where the parser failed to extract quantity. CK020 = Chuyển kho (transfer), PNN = Phiếu nhập nội bộ, PN202 = Phiếu nhập, PXN = Phiếu xuất nội bộ. | **Investigate parser.** Inspect raw_payload of 5 rows to see if qty field exists under a different key (Misa column variation). If yes → parser fix. If no → reclassify as Skipped header-row. |
| **SCT "Pre-skipped: source-data gap"** | SCT × 2 (PN20250073 + PN20250034) | 2 | Receipt vouchers with missing fields. | Accept. |
| **Bang ke BR (e-invoice rows without NKC counterpart)** | Bang ke BR × 73 | 73 | E-invoice register rows (`Ký hiệu HĐ`, `Số hóa đơn`, `Diễn giải` mostly "Điều chỉnh thông tin..." / "Điều chỉnh giảm..."). These are adjustment/cancellation e-invoices without a matching NKC entry that the builder could attach them to. | **Accept as e-invoice-only.** They have e-invoice trail in HTKK but no GL movement intended (correction-only). Builder could create a `Sales Invoice Adjustment` doc or simply log them. Low priority. |
| **Bang ke MV (VAT declaration summary)** | Bang ke MV × 4 | 4 | Tax declaration summary lines ("Nhóm HHDV mua vào: 1...", "Tổng cộng", "Nhóm HHDV mua vào: 4...", "Nhóm HHDV mua vào: 5..."). NOT transactions — these are aggregate rows from the VAT-input declaration sheet. | **Re-classify as "VAT Declaration Summary"** with explicit no-op handler. |
| **Misa Closing Rule (621→154, 627→154, etc.)** | Misa Closing Rule × 20 | 20 | Year-end closing rule definitions (rule cards, not transactions). The 20 rules define how to roll P&L accounts to TK 911/421 at year close. | **Re-classify as "Closing Rule Config"** with no-op handler. These should be loaded into a separate `Misa Closing Rule` DocType (already exists per error message) for the YE close engine to consume — not posted as GL. |
| **Account Conflicts (chart-of-accounts name mismatch)** | Account × 34 (Conflict) | 34 | The 34 TKs (2412 "Xây dựng cơ bản" vs Frappe "XDCB", 3523, 211 "TSCĐ hữu hình" vs "Tài sản cố định hữu hình", etc.) exist in Frappe with different `account_name` than what Misa has. | **Decision needed.** Pick one of: (a) rename Frappe Account.account_name to match Misa, (b) accept Frappe name and mark Conflicts as "Already exists, name-only difference", (c) augment Account.alt_name field for both. Recommend (b) with a UI "Resolve Conflicts" page so user sees both names and picks one. |
| **Skipped: explicit source gap** | NKC×40, SCT×2, Customer×1 ("Tổng" aggregate row), Supplier×1 ("Tổng"), Item×1 (header row), Misa Default Account×13 ("Không có TK nào ánh xạ được") | 58 | Various source data gaps. The Item×1 sample is the spreadsheet header row that the parser correctly identifies as non-data; same for Customer/Supplier "Tổng" rows. The 13 Misa Default Account skips are mapping rules with neither Dr nor Cr TK — incomplete config. | Accept all. |

**The "skipped_count=2 during pump"** referenced in the prompt: I believe these are the 2 SCT rows flagged "Pre-skipped: source-data gap" — voucher_no PN20250073 (warehouse THP, item Con-DCN, posting_date 2025-04-16) and PN20250034 (warehouse KTP, item TP_THANGCAP, posting_date 2025-12). Cause is empty qty/rate in source; pump correctly skipped.

**Net assessment:** the "98% success" is real for transactions, but the 2% breakdown is dominated by master/config/OB rows that bulk_pump never claimed to handle. The genuinely-problematic Ready items are the 53 NKC + 483 SCT + 4 MV + 20 Closing Rule, of which the SCT qty=0 batch deserves real investigation (could be parser bug affecting 483 stock movements).

---

## Area 2 — Doc Shape Validity

### Sales Invoice (4,461 docs, 100% submitted) — ✅ broadly correct

- Customer link 100% resolves (0 orphans).
- Single-item structure: every SI has 1 item line at `MISA-MIGRATION-SVC` (intentional generic item) with the source-truth `income_account` set per-row (51134, 51136, ...). This is acceptable for migration: GL accuracy is preserved even though item-level granularity is lost.
- Tax row present on all sampled SI (1 row each).
- Payment schedule populated (1 row each), `due_date` set, currency=VND.
- Outstanding amounts reconcile to allocation drain (500/500 sampled).

**Minor concerns:**
- All items use the same generic item code `MISA-MIGRATION-SVC` — Item-wise Sales History report will be useless (everything bucketed under one item).
- No project link (0/4461 SIs have a project), so project-billing rollup won't work for migrated data.

### Purchase Invoice (4,742 docs, 100% submitted) — ❌ CRITICAL mis-routing

- Supplier link 100% resolves.
- Single or multi-line item structure with `MISA-MIGRATION-SVC` (same as SI).
- Tax row present.
- **`expense_account` distribution** — 3,357 of 4,742 PIs (~71% by line count) have **at least one item line booked to TK 1331** (input-VAT refund account):

| expense_account | Item rows | Total amount |
|---|---|---|
| **TK 1331** (input-VAT) | **3,357** | **11.75B** |
| TK 6323 (giá vốn DV khác) | 988 | 3.64B |
| TK 6427 (CP DV mua ngoài) | 905 | 0.66B |
| TK 6322 (giá vốn viễn thông) | 864 | 3.20B |
| TK 242 (CP trả trước) | 522 | 4.40B |
| TK 6423 (đồ dùng VP) | 180 | 0.08B |
| TK 6321/6324/811/635 | ~46 | 0.32B |

**11.75B / 24.06B = 48.9% of total PI item value is mis-routed.**

Sample PI MDV20247169 (bill_no=69175, supplier=VNPTBD, telecom service Dec 2024):
```
GL:  Dr 1331  6,000,000   ←  item line (WRONG — should be 6322 telecom expense)
     Dr 1331    600,000   ←  tax line (CORRECT — VAT 10%)
     Cr 331   6,600,000   ←  supplier (CORRECT)
```

Source-data check on `Misa Migration Row`: 4 NKC rows match bill_no 69175 (mix of "Cước dịch vụ" = service cost + "Thuế GTGT" = VAT) — but `Tài khoản Nợ`, `Tài khoản Có`, `Số tiền` are all `None` in the `raw_payload` for these rows. **The parser failed to extract TK Nợ / Có / amount fields** from the source NKC sheet for many vouchers, and the builder fell back to TK 1331 as a default expense_account.

Multi-line case: PI MDV20253708 (FPT Telecom, net 1,454,545) — 3 items: TK 6322 (200,000) + TK 1331 (709,091) + TK 6323 (545,454). The 1331 line is treated as a regular cost line that summed into `net_total`, then a separate `taxes` row added 145,455 of real VAT. So **the 1331 amount is double-counted** — it appears as both a cost line and a notional expense, while the real VAT is correctly on `taxes`.

**Recommend: fix builder.**
- If the parser successfully extracts `TK Nợ` and it starts with `1331` → drop the line, fold into `pi.taxes` only.
- If parser returns null `TK Nợ` → either skip the row (and mark "parser gap") OR default to `Company.default_expense_account` (TK 642x) with a `parser_fallback=1` flag for audit.
- Backfill 3,357 existing rows: SQL UPDATE `pii.expense_account` to a derived expense based on supplier-group / source description heuristic (or to TK 642 generic), AND post a balancing JE to clear the mis-recorded Dr 1331.

### Payment Entry (7,164 docs, 100% submitted) — ✅ correct

- `party_type` + `party` populated for both Pay and Receive types.
- `paid_from` and `paid_to` set to bank/cash accounts (11215, 11218, etc.).
- `mode_of_payment` set to "Bank Draft" on all sampled.
- `references` populated where appropriate (refs=0 for direct expense/tax PEs which is correct).
- Allocation drain reconciles: 500/500 SI + 500/500 PI sampled have `grand_total - SUM(allocated) = outstanding_amount` within ±1 VND.

### Journal Entry (664 docs, 100% submitted) — ✅ correct

- All JEs balanced: Dr = Cr to ≤1 VND. **0 unbalanced JEs in the full scan.**
- `account_currency` populated, base `debit`/`credit` set explicitly per row (avoiding the multi-currency trap from the rules).
- Reference resolution: 0 unresolved JE Account `reference_type`/`_name`.

### Stock Entry (1,363 docs, 100% submitted) — ❌ CRITICAL bugs

**Warehouse fill rate on SE Detail (the form's view layer):**

| Purpose | SEs | Items | no_s_warehouse | no_t_warehouse |
|---|---|---|---|---|
| Material Issue | 808 | 2,632 | **2,632 (100%)** | 2,632 (100%) — correct |
| Material Receipt | 319 | 1,445 | 1,445 (100%) — correct | **0** |
| Material Transfer | 236 | 514 | **514 (100%)** | 0 |

For Material Issue, neither s_warehouse nor t_warehouse is set on SE Detail rows (but the SLE row IS populated with `warehouse`). The Stock Entry form will render every line with no warehouse → looks broken to the user.

**SE GL is structurally wrong** (see Area 4 for full analysis):

| Purpose | SEs total | with GL | GL distinct accts = 1 | inventory account ever touched |
|---|---|---|---|---|
| Material Issue | 808 | 808 | **808 (Dr 632 / Cr 632 same)** | Never |
| Material Receipt | 319 | 251 | **251 (Dr 632 / Cr 632)** | Never |
| Material Receipt | — | 68 missing GL | — | — |
| Material Transfer | 236 | 0 (GL-neutral expected) | — | Never |

**The Stock Entry pump is writing SLE correctly but writing GL to TK 632 on both Dr and Cr sides — net zero impact on GL. Inventory accounts (TK 152x/155x/156x) are never updated by Stock Entries.** Bin reports 8.28B VND of inventory; GL says 2.77B (only from 31 opening JEs).

### Asset (175 docs, 100% submitted) — ✅ correct

- 175/175 Assets have `calculate_depreciation=1`, status=Submitted, 1 Asset Finance Book row, and depreciation schedule populated (6-12 rows depending on useful life).
- Item link 100% resolves; item-side `is_fixed_asset=1` verified.

---

## Area 3 — ERPNext-native relationship integrity

All FK joins are clean:

| Check | Orphan count |
|---|---|
| SI → Customer | 0 |
| PI → Supplier | 0 |
| Asset → Item | 0 |
| Payment Entry Reference → SI | 0 |
| Payment Entry Reference → PI | 0 |
| PI Item → Item | 0 |
| SI Item → Item | 0 |
| SLE → Warehouse | 0 |
| GL Entry → Account | 0 |
| JE Account → reference target | 0 unresolved |

Payment allocation drain: 500/500 SI + 500/500 PI sampled — `outstanding_amount = grand_total - SUM(allocated_amount across PE Refs)` within ±1 VND.

**Master reuse** — no duplicates created:
- 1,542 Customers, 1,508 Suppliers, 2,616 Items, 1,098 Bin rows across 158 Warehouses.
- The DuplicateEntryError on 13 Bank Accounts and 56 Employees during the pump (visible in Migration Row status) confirms that the pump correctly detected pre-existing masters and refused to recreate them. No silent data corruption from those.

---

## Area 4 — Native ERPNext reports

| Report | Result | Interpretation |
|---|---|---|
| **Trial Balance (Yearly)** | Opening Dr 154.83B = Cr 154.83B (diff 0). Period Dr 572.03B = Cr 572.03B (diff 11). Closing diff 11 VND. | ✅ TB balances. The 154.83B opening originates from 197 JEs posted at `posting_date < 2025-01-01` — these are separate from bulk_pump and presumably from an earlier opening-balance flow. |
| **Stock Balance** | 729 rows, **bal_val = 8.28B VND** (matches Bin total). | ✅ Bin reconciles with the report, BUT this number does NOT match GL inventory (2.77B). See SE bug. |
| **Sales Register** | 4,461 rows, sum grand_total = 74.02B VND. | ✅ Matches direct sum of SI.grand_total. |
| **Purchase Register** | ❌ ERROR: `'NoneType' object has no attribute 'get'` at `supplier_details.get(inv.supplier).get("supplier_group")`. | At least 1 PI has a `supplier` that isn't returned by the report's `Supplier` query. Likely a disabled supplier or a `default_company` mismatch. Needs trace. |
| **AR Aging** | 8,190 voucher rows, sum outstanding = 1.78B VND. | Differs from sum(SI.outstanding)=4.07B by 2.29B. AR Aging aggregates via GL party_type=Customer, which is lower because (a) some payments went directly to TK 131 without `party` flag, OR (b) unposted OB Customer AR (64 rows) means historical receivables never landed on GL. |
| **AP Aging** | 6,702 voucher rows, sum outstanding = 7.88B VND. | Differs from sum(PI.outstanding)=6.08B by +1.81B. Same root cause as AR but in the opposite direction — unposted OB Supplier AP (102 rows) means we know about some debts that aren't on GL. |
| **AR Summary** | 97 customer rows, total_due = 1.78B (matches AR Aging). | ✅ AR Summary = AR Aging — internally consistent. |
| **AP Summary** | 336 supplier rows, total_due = 7.88B (matches AP Aging). | ✅ AP Summary = AP Aging — internally consistent. |
| **General Ledger TK 632** | 2,841 voucher rows, net change −12.59B VND. | ⚠️ Net CR position on a COGS account is structurally suspicious. Driven by SE Dr=Cr same-account (net 0 from 17.86B Dr + 17.86B Cr) + opening JEs on TK 632 children. Need to trace which JE rows account for the -12.59B net Cr. |

**BS root-type reconciliation** (`SUM(debit - credit)` per root_type):

| root_type | Net Dr−Cr (VND) | Natural sign | Verdict |
|---|---|---|---|
| Asset | +162,153,321,318 | + (Dr) | ✅ |
| Liability | −20,228,329,148 | − (Cr) | ✅ |
| Equity | −122,147,835,074 | − (Cr) | ✅ |
| Income | −10,325,846,309 | − (Cr) | ✅ |
| Expense | **−9,451,310,776** | + (Dr) expected | ⚠️ wrong sign — see note |

Total: 162.15 − 20.23 − 122.15 − 10.33 − 9.45 = −0.01B = −11 VND ✓

Expense having a net CR position is structurally wrong for a year that isn't closed. Either (a) some closing entries were partially applied in the migration, OR (b) JEs in the period have Cr-to-expense entries that exceed Dr. Worth tracing in a follow-up: query `tabGL Entry WHERE account in (expense accounts) AND credit > 0 ORDER BY credit DESC` to find the top Cr-to-expense events.

---

## Area 5 — Submittable side effects (didn't fire because direct INSERT)

| Side effect | Status |
|---|---|
| **Asset depreciation schedule** | ✅ Populated for all 175 Assets (6-12 schedule rows per Asset, 1 Asset Finance Book row each). Migration apparently re-computed these explicitly. |
| **Customer/Supplier `last_modified` / balance auto-recompute** | Not directly verifiable, but AR/AP reconcile gaps (see Area 4) suggest no full recompute happened. |
| **Item `standard_rate`** | ❌ 0/2,616 Items have `standard_rate` populated. on_submit normally derives from PI item rates. Affects valuation reports going forward. |
| **Item `last_purchase_rate`** | ❌ 21/2,616 Items have `last_purchase_rate` (0.8%). Same root cause. |
| **Item Default rows (per-Company income/expense/warehouse defaults)** | ❌ 2,479/2,616 Items have NO Item Default rows (94.8% missing). Future SI/PI entry on these items will fall back to Company defaults, not per-item defaults. |
| **Project rollup (total_billed_amount, total_purchase_cost)** | N/A — 0 SIs link to a Project. Project-side aggregation moot. |
| **Bin reserved/projected/planned/ordered qty** | All 0. Normal for closed period (no in-flight SO/PO), so no recompute needed. |
| **SI status flag vs outstanding_amount** | ⚠️ 16 SIs (of 4,461) have `status='Paid'` but `outstanding_amount > 100 VND`. Material: sum of these outstandings = 285.18M VND. Example: BH20250898 status=Paid outstanding=64.6M. |
| **PI status flag vs outstanding_amount** | ⚠️ 14 PIs (of 4,742) have `status='Paid'` with `outstanding > 100 VND`. Material: 66.27M VND. Plus 52 more PIs with tiny diffs (1-100 VND, rounding). |
| **on_submit hooks** | Did not fire. Any custom logic depending on `on_submit` (vn_accounting's reclassify guard, Non-Deductible tracking auto-set, audit chains) will not have run for any of the 18,569 docs. |

---

## Final priority list of follow-up fixes

### P0 — Critical correctness bugs that distort accounting reality

1. **Stock Entry GL: Dr/Cr to same account (TK 632)** — pump writes net-zero GL for 1,127 SEs. Inventory accounts never updated.
   - **Fix in pump:** the SE GL builder needs to emit `Dr <expense_account>` and `Cr <warehouse.account>` from `Warehouse.account` field, not the same account both sides. For Material Receipt: `Dr <warehouse.account> / Cr <stock_in_hand or supplier source>`. For Material Transfer: `Dr <target_warehouse.account> / Cr <source_warehouse.account>` (each warehouse has its own GL account in Frappe — 1561, 1562, etc.). For Material Issue: `Dr 632 / Cr <warehouse.account>`.
   - **Backfill:** for each existing SE, compute the correct Cr leg and post a balancing JE: Dr <warehouse.account> stock_value_difference / Cr 632 stock_value_difference. After all backfill JEs, TK 632 should net-out to the legitimate COGS movement; warehouse accounts should reach Bin totals.
   - **Verify:** Bin total stock_value == sum of warehouse-account GL balances within ±1 VND.

2. **PI expense_account mis-routing to TK 1331** — 11.75B VND (48.9% of PI item value) parked on input-VAT instead of expense.
   - **Diagnose first:** confirm whether the parser is failing to extract source TK Nợ (sample showed `Tài khoản Nợ`, `Tài khoản Có`, `Số tiền` all `None` in raw_payload for the affected PI). If parser bug → fix parser first.
   - **Fix in builder:** when source TK Nợ starts with `1331` → fold into `pi.taxes` row, do NOT create an item line. When source TK Nợ is null → default to `Company.default_expense_account` (typically TK 642) with a `parser_fallback=1` flag.
   - **Backfill:** for each existing PI Item with `expense_account LIKE '1331%'`, derive correct expense account (heuristic: supplier-group → service-cost mapping table), update `pii.expense_account`, post balancing JE Dr <new expense> / Cr 1331.
   - **Verify:** TK 1331 GL total Dr should reduce by ~11.75B. Real expense accounts should gain ~11.75B Dr.

3. **TK 1551 negative balance (−47.5M VND)** — finished goods inventory account is impossible-negative. Root cause likely related to bugs #1 + missing OB Inventory posting.
   - Resolves once #1 + OB Inventory posting are fixed. Monitor after fix.

### P1 — Reconciliation gaps that block trustable reports

4. **OB rows not posted (1,792 rows across OB Account/Bank/CCDC/AR/AP/Fixed Asset/Inventory/Prepaid)** — AR off 474M, AP off 8.88B, TK 331 has a debit balance (impossible for a payable).
   - Either build an explicit "Post OB to GL" step in the pump that runs BEFORE the transactions, OR document that post-pump AR/AP reconciliation requires the user to run a separate OB-posting flow.

5. **Purchase Register report broken** — `'NoneType' object has no attribute 'get'` at supplier lookup.
   - Find the offending PI (`SELECT pi.name, pi.supplier FROM tabPurchase Invoice pi LEFT JOIN tabSupplier s ON s.name=pi.supplier WHERE pi.company='DCNET TEST' AND s.name IS NULL` — but this returned 0 earlier; likely a `disabled` or `default_company` filter in the report).
   - Trace `purchase_register._execute` line 87 and look at what `frappe.db.get_all("Supplier", ...)` filter is excluding the matching supplier.

6. **SE Detail s_warehouse / t_warehouse blank** for 100% of Material Issue + Material Transfer items. Even after fixing GL, the form view will look broken.
   - Builder fix: populate `sed.s_warehouse` (and `sed.t_warehouse` for Transfer) on the SE Detail row, not just on the SLE.

### P2 — Cleanup / parser improvements

7. **Re-classify Unknown rows** (1,375 tax-resource + currency rate masters) into "Tax Resource Rate" and "Currency Rate" file_types with explicit no-op handlers. Same for Bang ke MV (4 rows = VAT declaration summary) and Misa Closing Rule (20 rows = closing config). Improves pump UI clarity without changing economics.

8. **SCT qty=0 (483 rows)** — investigate whether these are header rows (correctly skipped) or value-extraction failures. If parser bug, fixing it could surface 483 more stock movements.

9. **NKC NVK20250331 (52 rows with empty Dr/Cr/amt)** — same: header rows or parser gap?

10. **Status flag drift** — 16 SI + 14 PI have `status='Paid'` with material outstanding. Either re-run status backfill SQL after every pump cycle, or fix the backfill query (likely off-by-rounding boundary).

11. **Item Default rows missing** for 94.8% of Items — going-forward data entry will use Company defaults instead of per-item. Post-migration cleanup script can derive Item Default from observed PI/SI item lines.

### P3 — UX / documentation polish

12. **Account Conflicts (34 rows)** need a resolution UI — pick Frappe name or Misa name per TK. Currently silent.

13. **CoA bootstrap button** (already noted in `project_misa_migration_pending.md`) — for new sites that don't have a CoA yet, provide a one-click "Install VAS TT99/2025 CoA" button before letting users start migration.

---

## What the audit did NOT catch

- I did not run **Customer Ledger Summary** per individual customer (only AR Summary aggregated). Spot-checks showed per-customer GL_balance > SI_outstanding for top 4 customers (SOFTNET, HITC, ROCHDALE, MFG), but I didn't quantify the per-customer drift across all 1,542 customers.
- I did not verify **Item-wise Sales History** — it ran without rows visible in output. All SIs use the same `MISA-MIGRATION-SVC` item so per-item slicing is moot.
- I did not verify **GST/VAT reports** (Purchase Detail / Sales Detail per the VN regulator format). Given the TK 1331 mis-routing, these will be materially wrong.
- I did not re-run a **full SE backfill JE simulation** to confirm that fixing bug #1 would not over-correct.
- I did not check **Project P&L** — there are 269 Project rows but 0 are linked to DCNET TEST's transactions.
- I did not investigate **TK 632 net −12.59B credit position** to identify the source JEs putting Cr-to-expense — likely opening JE artifacts.

---

## Recommended next session

1. **Reproduce bug #1 in a minimal SE** — create a single Material Issue via the pump in a fresh batch, verify GL, then patch the SQL builder.
2. **Reproduce bug #2 with one PI** — verify whether parser or builder is the failing layer.
3. **Write backfill scripts** for both bugs that work on the existing DCNET TEST data.
4. **Add audit gates** to the pump itself: after pump, run a 3-line sanity check (Bin total == GL inventory total within ±1 VND; PI Item expense_account never TK 1331; SE GL distinct_accts >= 2 per voucher).
