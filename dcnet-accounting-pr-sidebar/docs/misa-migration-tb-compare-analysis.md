# Misa Migration: TB Compare Divergence Analysis (Phase E Real-Data)

End-of-period analysis from running full-year 2025 + 01-2026 Misa data
through the migration pipeline (real client data: DCNET TEST company,
80k+ NKC rows, 9.5k Jan-2026 rows). All findings here are from
diagnostic queries during the Phase E E2E re-test.

## Divergence Roll-Up

After commits `6641441` / `0b790c1` / `c205884` (perf push), `cf95f31`
(SE purpose, allow_negative_stock, PI credit_to, batch.modified),
`081257b` (PE retry + TB logic + audit comments), `733adb4` (salary-UNC
handling), and `78b965d` (parser dedup), the TB compare at end-of-Jan-2026
shows ~36 divergences. The 4 top buckets and their root causes:

| TK | Misa expected | ERPNext (pre-fix) | Gap | Root cause | Fix status |
|---|---:|---:|---:|---|---|
| 334/3341 | -2.19B | -19.17B | -17B | UNC salary handler refs + backfill + parser 3× | **Fixed: 733adb4, 78b965d** |
| 141 | +63.72B | +71.91B | +8.19B | Activity inflation from parser 3× + handler | **Partial: 78b965d covers ~5B** |
| 1561/156 | +6.4B / +6.4B | +15.3B / +17.2B | +8.9B / +10.8B | PI posts Dr 1561 GL but no SLE → SE PX has valuation_rate=0 | **Open: needs PI update_stock=1** |
| 1121.20 / 11218 / others | ~+0 / -14M | +2.95B / +8.12B | +2.93B / +8.13B | Parser 3× × multi-leg UNC handler inflation | **Fixed: 78b965d** |

## Per-Bucket Root Causes

### TK 334 / 3341 (Phải trả công nhân viên) — FIXED

**Symptom:** -17B over-credited on TK 3341. Misa source has 59 UNC
vouchers paying salary (Dr 3341 / Cr bank, party_code="DCNET"), but:
- 36 failed to create at all
- 20 cancelled by backfill, never re-amended
- 2 stayed all-cancelled
- Only 1 active PE

**Root cause chain:**
1. Parser doesn't dedup Misa NKC's 3 reporting-axis duplicates → 6 legs instead of 2.
2. Multi-leg path triggered, computes `party_amount = 3× actual`.
3. UNC handler attaches FIFO open-PI references for party_code="DCNET" — but the PIs use `credit_to=331` while PE uses `party_account=3341`.
4. PE.insert() validates references against party_account → `ValidationError: associated with 331, but Party Account is 3341` → entire creation fails.
5. For the few that DID create, PE backfill cancels the working salary PE, tries to amend with PI refs → amend fails for same mismatch → original stays cancelled.

**Fixes applied:**
- `733adb4`: UNC handler skips `_resolve_pe_references` when `party_account` is employee-payable (334/141). Also adds `reference_no`/`reference_date` to multi-leg UNC path (Bank Draft requires it). PE backfill restricts to PEs with `paid_to LIKE '331%'` or `paid_from LIKE '131%'` only.
- `78b965d`: nkc_parser collapses legs with identical `(account, debit, credit, leg_desc)` per voucher.
- `cf95f31`: PI handler derives `credit_to` from voucher Cr leg (was using Supplier master default, which for DCNET-as-Supplier was 3341 because the company also acts as salary payer).

**Expected after clean re-run:** near-zero divergence.

### TK 141 (Tạm ứng nhân viên) — PARTIAL FIX

**Symptom:** +8.19B over on TK 141.

**Diagnosis:**

| Source | Dr | Cr | Net |
|---|---:|---:|---:|
| Misa OB fixture | 63.72B | 0 | +63.72B |
| Misa TB end-Jan-2026 | — | — | +63.72B |
| ERPNext OB JE | 63.72B | 0 | +63.72B ✓ |
| ERPNext PE activity | 13.26B | 0 | +13.26B |
| ERPNext JE activity | 0 | 5.07B | -5.07B |
| **ERPNext total** | **77.0B** | **5.07B** | **+71.91B** |

The OB JE matches Misa fixture (+63.72B). The +8.19B over comes from
2025 activity that **Misa expects to be net-zero** on TK 141 — every
advance Dr should be balanced by a Cr return.

Misa raw NKC for TK 141 shows Dr 13.3B / Cr 5.07B (raw, 3×-duplicated).
After parser dedup, real activity ≈ Dr 4.4B / Cr 1.7B = +2.7B net.

**Fix status:** Parser dedup (78b965d) reduces inflation but doesn't
fully solve. Residual ~2-3B gap may be:
- Genuine business reality (advances given > recovered in 2025)
- Or remaining PE handler logic issues (UNC paying advance to party_code that's not a registered Employee)

**Recommendation:** measure after clean re-run, then decide if further
handler changes needed.

### TK 1561 / 156 (Hàng hoá - inventory) — OPEN, architectural fix needed

**Symptom:** +8.9B over-Dr on TK 1561. Misa expects 6.4B net, ERPNext shows 15.3B net.

**Diagnosis:**

```
ERPNext TK 1561 GL by voucher_type:
  Journal Entry         Dr  2.75B  /  Cr  33M     (OB only)
  Purchase Invoice      Dr 12.55B  /  Cr   0      ← stock-in via PI Dr leg
  Stock Entry           Dr     0   /  Cr   0      ← STOCK ENTRIES POST NOTHING

Misa raw TK 1561:
  PN  (Phiếu nhập, 269 vouchers)   Dr 12.7B   ← inflows (matches PI Dr ✓)
  PX  (Phiếu xuất, 820 vouchers)   Cr  6.0B   ← outflows MISSING from ERPNext
  PXHN (Stock transfer, 253)       Cr 645M    ← MISSING
  PNHN (Phiếu nhập nội bộ, 66)     Dr 525M    ← MISSING
```

**Root cause:** Stock Entries are submitted (1,179 docstatus=1) but
**zero GL Entries** from `voucher_type='Stock Entry'`. Why?

1. Company has `enable_perpetual_inventory=1` ✓
2. But all Warehouses have `account=None` — no warehouse-to-account binding
3. Even if accounts were bound, SE Material Issue uses `valuation_rate` (computed from SLE), not `basic_rate` (input). 
4. The PI handler with `update_stock=0` posts Dr 1561 GL but does NOT create SLE.
5. When SE PX submits, SLE has 0 value (no prior stock-in via SLE) → `stock_value_difference=0` → no GL impact.

**Why this is structural, not a bug:** Misa "PN" voucher is one accounting+stock document. Our pipeline splits it into:
- PI doc with `update_stock=0` (accounting Dr 1561 / Cr 331)
- No corresponding SE Material Receipt

So stock VALUE never flows through SLE. The SE PX (issue) then has nothing to draw down.

**Fix options:**

1. **PI handler `update_stock=1` for stock items** (recommended)
   - Pre-condition: each item line has a warehouse
   - Effect: PI creates both SLE (stock-in) AND GL (Dr 1561 / Cr 331). Then SE PX can draw from real stock value.
   - Side effects: requires warehouse on every item; PI rate must be set
   - Misa NKC + Bang kê provides item + qty + rate, but not always warehouse — would need to default to a company-level warehouse for PI

2. **PN handler routes to Material Receipt SE** instead of PI
   - Effect: Stock-in via SE with explicit `basic_rate` from Bang kê. SE Material Receipt posts Dr 1561 (warehouse account) / Cr 331 (party).
   - Bigger refactor: current PN→PI route would split into PN→SE+JE (SE for stock, JE for any tax/expense splits).
   - Closer to Misa semantics.

3. **SE PX handler sets `valuation_rate`** from SCT instead of relying on stock balance
   - When stock balance is 0, use SCT's `rate` as the valuation
   - Smallest code change, but loses Stock Ledger integrity (SE no longer reflects real inventory value chain)

**Recommendation:** Option 1 for the next iteration (PI `update_stock=1` for stock items). Single-file edit in `purchase_invoice.py`, plus warehouse-defaulting logic. Estimated 30-60 LOC change.

### TK 1121.20 / 11218 / 11219 / 1121.21 (bank sub-accounts) — FIXED

**Symptom:** small-to-medium over-Dr on bank sub-accounts. 11218 is the biggest: +8.13B.

**Root cause:** Parser 3× duplication × multi-leg UNC handler inflation. Every PE Pay (Cr bank) and PE Receive (Dr bank) was posting 3× the actual transfer amount.

**Fix status:** Both root causes fixed by `78b965d` (parser dedup) and `733adb4` (UNC refs skip → simple 2-leg path now triggers for salary UNCs).

**Expected after clean re-run:** all bank sub-accounts within ±100M VND of Misa (essentially zero net).

## Summary of Code Changes (commit chain)

| Commit | Files | Issue Addressed |
|---|---|---|
| `cf95f31` | stock_entry.py, purchase_invoice.py, phase_4_orchestrator.py | SE purpose + allow_negative_stock + PI credit_to + watchdog batch.modified |
| `081257b` | phase_4_orchestrator.py, test_trial_balance_t1_2026.py | PE retry as unallocated + TB compare logic + orphan PE Comment |
| `733adb4` | payment_entry.py, phase_4_orchestrator.py | Salary-UNC PE: skip refs + reference_no + restrict backfill |
| `78b965d` | nkc_parser.py | Dedup identical legs per voucher (Misa 3× reporting-axis) — initial, over-aggressive |
| `b4db28f` | purchase_receipt.py, docs | PN PI uses stock-eligible placeholder so SLE creates → TK 1561 outflow chain works |
| `285e4e0` | nkc_parser.py | Parser dedup safety: only collapse when ALL leg tuples have uniform count >1 (preserves complex BH/PX/PN vouchers) |

## Post-fix Baseline (2026-05-21 clean E2E re-run)

**Clean cleanup → re-run both shards → TB compare at 2026-01-31.**

- Shard A (MM-2026-01000, full year 2025): POSTED — 74150 posted / 6138 failed / 19573 ignored
- Shard B (MM-2026-01001, Jan 2026): POSTED — 6966 posted / 880 failed / 1626 ignored
- Submitted docs: PE 7651 / SI 5853 / PI 4561 / SE 1223 / JE 3938. GL entries: ~110k.

**TB compare result: 38 accounts divergent >1k VND (was ~36 pre-fix). Roll-up impact distorts count — same gap can appear at parent + leaf row.**

## Post-fix-fix Baseline (2026-05-21, after 289fdcc + 9d594e0)

**Validation methodology: `retry_failed_rows`-equivalent via direct `post_job.post_batch` call (bypasses preflight's `check_no_existing_posted` false-positive on a batch's own previously-Posted rows). Resets Failed→Ready, bumps batch REVIEWED, re-runs only the 7018 previously-Failed rows.**

- Shard A retry: 3m3s → +5724 Posted (now 79874) / 414 Failed
- Shard B retry: 22s → +880 Posted (now 7846) / 0 Failed
- **Total failure count: 7018 → 414 (94.1% reduction)**

The 414 residual = 9 distinct bug classes from the doc's "Failed posting inventory" table, none of them VIETTEL or 156-group. Validates both 289fdcc fixes resolved their targeted failure modes completely.

### Post-fix-fix TB compare (2026-01-31)

| TK | Misa expected | ERPNext (post-fix) | ERPNext (post-fix-fix) | Change | Diagnosis |
|---|---:|---:|---:|---|---|
| 156 / 1561 | +2.70B | not in top 30 | **+15.47B / +15.46B** | **REGRESSED by ~12.8B** | The 2756 newly-Posted PIs (previously blocked by group-self-heal) now correctly post Dr 1561. But PI handler still uses `update_stock=0` → no SLE → SE PX has nothing to draw → Dr accumulates without Cr. Same `update_stock=1` fix from previous round needed again. |
| 141 | +63.72B | +71.91B | +71.91B | unchanged | Activity inflation unrelated to the 2 fixes |
| 4211 / 421 | -13.45B / -19.74B | -19.75B / -24.98B | -19.75B / -24.98B | unchanged | P&L close-out missing |
| 331 | -6.20B | +10.79B | **-3.01B** | **+13.8B improvement** ✓ | The 2756 self-healed PI posts now correctly post Cr 331 (was missing in pre-fix). Remaining +3.2B gap likely from MH/PNHN handlers + 222 PBCC failures (PBCC actually hits TK 242 not 331, so not the cause). |
| 341 / 3411 | -10.72B | -15.01B | -15.01B | unchanged | Long-term debt over-stated, unrelated to fixes |
| 333 / 3334 | -3.14B / -1.65B | -1.25B / 0 | -1.25B / 0 | unchanged | PI taxes child table not hooking 3334 |
| 112 / 1121 / 11215 | +728M | -877M | -877M / -901M | unchanged | Bank sub-accounts unrelated to fixes |
| 131 | +2.5B | (not top) | +966M | NEW in top 30 | -1.6B under-Dr on receivable |
| 4212 | -6.29B | -5.23B | -5.23B | unchanged | P&L close issue |
| **334 / 3341** | -2.19B | -2.54B | **-2.54B** | **holds (98% fix retained)** ✓ | Previous fix chain (733adb4, 78b965d) intact |

### Final residual failure inventory (414 across both shards)

| Count | Issue | Effect on TB |
|---:|---|---|
| 222 | `No handler registered for prefix 'PBCC'` — Phân bổ chi phí CCDC (monthly tooling allocation) | Affects TK 242 (~565M diff observed) and corresponding 632/6XX expense recognition |
| 52 | `NVK20250...: cannot resolve TK '8211'` | TK 8211 CIT current — small absolute, affects P&L |
| 36 | `bảng kê BR invoice not provided for BH...` | Sales-side, 24 SI not created |
| 28 | `UOMMustBeIntegerError` | PI vouchers blocked (some fractional UOMs); affects 331 Cr + 156 Dr |
| 24 | `Grand Total must be >= 0` | Likely credit notes on Sales Invoice |
| 22 | `Party Type and Party is required for 131/331` | Multi-leg JE missing party on receivable/payable legs |
| 14 | `... is not a stock Item` | PI handler failing on non-stock items where update_stock=1 attempted |
| 12 | `MandatoryError: cost_center on Payment Entry` | Multi-leg UNC missing cost_center default |
| 4 | `voucher PN...missing party_code` | 2 PN vouchers (Phiếu nhập) lack party_code |

### TK 331 deep-dive (post-fix-fix)

**ERPNext side (by voucher_type):**
| voucher_type | Dr 331 | Cr 331 | Net | n |
|---|---:|---:|---:|---:|
| Purchase Invoice | 0 | 43.36B | -43.36B | 3726 |
| Payment Entry | 45.56B | 0 | +45.56B | 2334 |
| Journal Entry | 1.96B | 7.16B | -5.20B | 313 |
| **TOTAL** | **47.52B** | **50.52B** | **-3.00B** | 6373 |

**Misa NKC raw (by voucher prefix, multi-axis dup not yet deduped):**
| Prefix | Dr | Cr | Net | n_rows |
|---|---:|---:|---:|---:|
| UNC (pay supplier) | 44.54B | 0 | +44.54B | 1447 |
| MDV (purchase invoice main) | 0 | 36.52B | -36.52B | 14104 |
| PN (Phiếu nhập) | 0 | 13.74B | -13.74B | 1335 |
| NVK (other JE) | 1.73B | 0.73B | +1.00B | 215 |
| PC (cash pay) | 1.05B | 0 | +1.05B | 649 |
| PNHN (internal receipt) | 0 | 0.57B | -0.57B | 137 |
| MH (merchandise purchase) | 0 | 0.33B | -0.33B | 746 |
| BC (bank credit) | 0 | 1.8M | -1.8M | 1 |
| **TOTAL** | **47.32B** | **51.89B** | **-4.57B** | |

**Comparison & residual gap analysis:**

- ERPNext PE Dr (45.56B) ≈ Misa UNC+PC Dr (45.59B) — payment side reconciles within 30M
- ERPNext PI Cr (43.36B) vs Misa MDV+PN+PNHN+MH Cr (50.84B) — PI handler under-credits by ~7.5B
- Misa NVK touches TK 331 with net +1B Dr (rare adjustment); ERPNext JE shows -5.20B net — likely OB JE + currency revaluation entries on JE side

**Hypothesis for the remaining +3.2B gap:**
1. MH/PNHN handlers may not post Cr 331 (route to different account, or missing handler). Misa's MH+PNHN contribute -0.9B Cr that may be missing in ERPNext.
2. Bigger contribution: the 14 "not stock Item" + 28 UOM-integer + 4 party_code failures = ~46 PI vouchers that didn't post their Cr 331 leg.
3. JE class differences explain remaining variance.

## Post-fix-fix-fix Baseline (2026-05-21, after PBCC handler)

PBCC = "Phân bổ chi phí CCDC" (Tools & Equipment monthly allocation) — same shape as PBPTT (prepaid expense allocation), 1:1 leg mapping JE. Routed `journal_entry.create_je_from_pbcc` with `voucher_type='Journal Entry'`.

**Validation result:**
- 222 PBCC Failed rows → all Posted (failures 414 → 192)
- 12 JE created (matches 12 distinct PBCC vouchers in NKC)
- GL impact: Dr 6423 209M + Dr 6324 29M + Dr 6323 9M = 248M; Cr 242 248M (balanced)
- TB compare TK 242: 1,837M → 1,589M (closer to Misa 1,272M); diff +565M → +317M (-44%)

### Remaining 192 Failed (after PBCC + party-cache + group-self-heal fixes)

| Count | Issue | Suggested fix |
|---:|---|---|
| 52 | `NVK20250...: cannot resolve TK '8211'` | Add TK 8211 to Misa Account Mapping fixture |
| 36 | `bảng kê BR invoice not provided for BH...` | Bảng kê BR file missing for these 24 invoices |
| 28 | `UOMMustBeIntegerError: Quantity (22.5) cannot be a fraction` | Item's UOM `must_be_whole_number=1`; toggle off OR change item UOM |
| 24 | `Grand Total must be >= 0` | Sales return / credit-note semantics on SI not handled |
| 22 | `Party Type and Party is required for 131/331` | Multi-leg JE handler not setting party on receivable/payable legs |
| 14 | `... is not a stock Item` | PI handler attempts update_stock=1 on non-stock items |
| 12 | `MandatoryError: cost_center on Payment Entry` | Multi-leg UNC missing cost_center default |
| 4 | `voucher PN...missing party_code` | 2 PN vouchers (Phiếu nhập) lack party_code in source |

## Post-6-bug-class-fix Baseline (2026-05-21, after small-class fixes)

6 bug classes fixed in one commit + validated via retry on shard A:

| Bug class | Pre-fix Failed | Post-fix Failed | Fix mechanism |
|---|---:|---:|---|
| NVK-8211 mapping | 52 | 0 | `_resolve_account` group→leaf descent fallback (uses `lft`/`rgt` to find first leaf child when account_number matches a group) |
| UOM-integer | 28 | 0 | New `ensure_uoms_allow_fractional()` setup helper toggles `must_be_whole_number=0` on Nos / Unit / Pair / Set / Box; called from phase_4_orchestrator |
| Grand Total negative | 24 | 0 | PI handler detects per-line negative amount → sets `is_return=1` + qty negative / rate positive |
| Party Type missing on 131/331 JE legs | 22 | 0 | Parser captures per-leg `Mã đối tượng`; JE handler prefers leg.party_code over voucher.party_code |
| Not stock Item on PI/SE | 14 | 0 | `_ensure_item_stub` upgrades existing Items from `is_stock_item=0` to 1 |
| PE cost_center mandatory | 12 | 0 | `_default_cost_center(company)` helper added; cost_center now set on both PE payloads + deductions rows |

**Residual 40 Failed** (data-only, not code-fixable):
- 36 = bảng kê BR file missing for 2 BH invoices (BH20252600 + BH20252217)
- 4 = 2 PN vouchers lacking party_code in Misa source (PN20250034, PN20250073)

**Cumulative session result: 7018 → 40 (99.4% reduction).**

### TB compare delta after 6 fixes

| TK | Before 6 fixes | After 6 fixes | Δ | Notes |
|---|---:|---:|---:|---|
| 156 / 1561 | +12.77B | +12.89B | +113M | Slight up — 14 not-stock-Item-fixed PIs added Dr 1561; architectural fix still needed |
| 421 / 4211 / 4212 (P&L close group) | sum −10.48B | sum +0.0B | **−10.48B** | The is_return=1 fix correctly classifies 24 PI credit notes → P&L close-out balance now matches Misa group total (gap redistributed across sub-codes) |
| 331 | +3.20B | +3.10B | -100M | Minor — bulk of 331 gap is PNHN routing (still deferred) + parser dedup nuances |
| 242 | +317M | +323M | +6M | Small drift from PBCC re-post |
| Total divergent codes | 38 | 38 | unchanged | Same set of accounts diverge; magnitudes redistribute |

## TK 156/1561 Deep-Dive (deferred — needs architectural fix)

Initial hypothesis "apply PI update_stock=1 for stock items" turned out to be **already in place**. The 281 PN-prefix PIs all have `update_stock=1` and DO create SLE with correct valuation_rate (verified: 18547, 16981, etc.) and stock_value_difference > 0.

**True root cause:** Stock-value chain broken at the *item* level, not GL level.

- PI handler (`purchase_invoice.py` MDV/MH AND `purchase_receipt.py` PN) creates rows with `PLACEHOLDER_ITEM_CODE` for every line (imported from `sales_invoice` module). PIs add stock value to the warehouse under the placeholder item.
- SE Material Issue (PX) consumes real item codes from bảng kê MV — items that have never been stocked under their real code.
- Result: 7076 SLE entries from Stock Entry but every one has `stock_value_difference=0` (no prior stock under those item codes). Hence 0 GL impact on TK 156* outflow.
- ERPNext side: SE Material Issue submitted 858, Material Transfer 257, Material Receipt 85 — all docstatus=1, all with `total_outgoing_value=0` / `total_incoming_value=0`.

**Why warehouses also have `account=None`:** With `enable_perpetual_inventory=1`, ERPNext falls back to `Company.default_inventory_account` (1561) when warehouse.account is empty. So the lack of warehouse binding does NOT block GL posting — the 0 stock_value_difference does.

**Fix paths (deferred to architecture decision):**

1. **Map placeholder → real items in PI** — PI uses real item code per bảng kê MV line. Pros: cleanest semantics, SE PX outflows would resolve. Cons: requires Misa→ERPNext item mapping at PI time (currently we don't import items into ERPNext, just use a placeholder). Adds full Item master import as a prerequisite.

2. **Bridge SE per PN** — auto-create a synthetic Material Receipt SE per PN that converts placeholder stock → real-item stock at PI's `valuation_rate`. Pros: keeps PI placeholder logic intact; SE PX can now draw from real-item stock. Cons: doubles SE volume; needs item master.

3. **SE PX uses placeholder item** — drop real item code from SE PX, all stock issues use placeholder. Pros: smallest code change. Cons: loses any per-item stock traceability, breaks downstream reporting on item-level stock movement.

4. **Accept the +12.8B inflation as known limitation** — document that TK 1561 won't match Misa under this migration design without item master import. Run a year-end JE `Dr 632 / Cr 1561 = 12.8B` to clear inflation cosmetically.

All four paths require business + engineering decision. None are quick safe code edits.

## TK 331 +3.2B Deep-Dive (continued)

After PBCC handler + better per-prefix TK 331 query (LIKE 'MDV%' not LEFT(name,4)):

**ERPNext TK 331 Cr contributions by voucher prefix:**
| Prefix | n_vouchers (in 331 GL) | Cr 331 | Misa raw Cr 331 (post-dedup ≈ÿ/3) | Gap |
|---|---:|---:|---:|---:|
| MDV | 3352 | 29.24B | ~12.17B (36.52B / 3) | unclear — Misa raw inflated 3x |
| PN | 286 | 13.79B | ~4.58B (13.74B / 3) | unclear |
| MH | 88 | 0.33B | ~0.11B (0.33B / 3) | unclear |
| PNHN | **0** | **0** | **~0.19B (0.57B / 3)** | **-190M Cr 331 missing** |
| **Total PI Cr** | 3726 | **43.36B** | ~17B (50.84B / 3 raw) | (raw inflated) |

NOTE: Misa NKC raw counts include 3× reporting-axis duplication. After parser dedup the actual contribution is ~1/3 of raw values. The "expected" Misa Cr 331 from PI-class = ~17B. ERPNext shows 43.36B PI Cr — much HIGHER than 17B. This means ERPNext is OVER-Cr on PI side by ~26B vs Misa's pure (post-dedup) PI-Cr expectation.

But: Misa TB fixture says total TK 331 balance = -6.20B Cr. And ERPNext shows -3.00B Cr (Dr 47.52B - Cr 50.52B). Within balance the gap is 3.2B Dr-leaning. The +26B over-Cr in PI is offset by +28B over-Dr in PE — net 3.2B Dr direction.

This suggests **parser dedup may not have run for these vouchers in the current Posted state**. The 78b965d / 285e4e0 parser dedup operates at parse time; if these vouchers were posted in an earlier session before dedup landed, they'd carry the 3× duplication into the final docs. A clean re-run would resolve.

**Real PNHN bug (confirmed):**
- 71 PNHN vouchers in Misa NKC, ERPNext creates 71 SE (Material Receipt) — 0 PI, 0 JE
- `create_se_from_pnhn` at `nkc_handlers/stock_entry.py:703` routes pure stock-receipt; ignores Cr 331 leg
- Misa PNHN docs are functionally a stock-in + supplier liability (Cr 331). Current routing loses the 331 leg
- Fix: route PNHN through `purchase_receipt.create_pi_pr_from_pn` (PI with update_stock=1) instead of pure Stock Entry — requires bảng kê MV with item lines, which PNHN may not have

## Recommended Next Steps (revised priority order, post-PBCC)

1. **TK 156/1561 — architectural decision needed.** See deep-dive above. Pick from 4 paths.

2. **TK 331 — investigate parser dedup application to existing Posted docs.** If 3× duplication persists in already-Posted PI/PE, a clean re-run (full migration) would resolve. PNHN bug separately (568M Cr 331 routing fix).

3. **TK 4211/4212/421 close-out missing** (~-11.5B combined). P&L closing entries to enter from Misa OB JE comparison.

4. **TK 141 root cause** — +8.19B activity inflation. Likely UNC paying advances to non-Employee party.

5. **TK 341/3411** — long-term debt over-stated by 4.3B. Likely bank-loan handling redundancy.

6. **NVK 8211 mapping** (52 failed) — add TK 8211 to Misa Account Mapping fixture.

7. **PE cost_center fallback** (12 failed) — multi-leg UNC missing cost_center default.

8. **PI handler item-class detection** (14 failed "is not a stock Item") — gate `update_stock=1` on `is_stock_item=1` check.

### Top buckets after fix

| TK | Misa expected | ERPNext (pre-fix) | ERPNext (post-fix) | Change | Diagnosis |
|---|---:|---:|---:|---|---|
| 334 / 3341 | -2.19B | -19.17B | -2.54B | **+98% fixed** ✓ | Parser dedup + UNC salary fix worked exactly as designed |
| 1121.20 / 11218 | ~0 | +8.13B | within ±100M | **Fixed** ✓ | Parser dedup eliminated 3× bank inflation |
| 1561 / 156 | +2.69B / +2.70B | +15.3B / +17.2B | not in top 30 | **Fixed** ✓ | PI uses stock-eligible placeholder → SLE works |
| 141 | +63.72B | +71.91B | +71.91B | **No change** | Activity inflation NOT from parser 3×; root cause elsewhere |

### New issues surfaced (now top of stack)

| TK | Misa | ERPNext | Gap | Diagnosis |
|---|---:|---:|---:|---|
| 331 | -6.20B | +10.79B | **+17B** | NEW: Cr 331 not posting where expected. PI `credit_to` resolution may be wrong, OR PE allocation creating spurious Dr 331 entries. |
| 4211 / 421 | -13.45B / -19.74B | -19.75B / -24.98B | -6.3B / -5.2B | P&L close not reflected. Misa OB JE may need 632/511 close-out entries. |
| 341 / 3411 | -10.72B | -15.01B | -4.3B | Long-term debt over-stated. Likely Misa NKC has bank-loan repayment entries that import as Cr 341 redundantly. |
| 112 / 1121 / 1121.81 / 11215 | +728M | -877M / -31M / -901M | -1.6B (multiple sub-accounts) | Bank sub-accounts swing negative — over-payment via PE or duplicate UNC. |
| 4212 | -6.29B | -5.23B | +1.06B | P&L close issue (same root as 4211). |
| 244 | +329M | +449M | +120M | Investment account, small. |
| 333 / 3334 | -3.14B / -1.65B | -1.25B / 0 | +1.9B / +1.65B | Tax payable under-posted. PI taxes child table may not be hooking 3334. |

### Failed posting inventory (10k from total 119k = 8.4% failure rate)

7018 row failures across both shards:
| Count | Issue |
|---:|---|
| 3848 | `Supplier 'VIETTEL' not found` — `_party_cache.is_supplier` case-sensitive while MariaDB case-insensitive → "VIETTEL" voucher_party_code doesn't match "Viettel" Supplier name |
| 2756 | `selected the account group 156 as Expense Account` — PI line `expense_account` resolution returns the group account `156` instead of leaf `1561`, fails ERPNext validation |
| 222 | `No handler registered for prefix 'PBCC'` — handler dispatch missing PBCC (likely a Misa voucher type for bank wire batch) |
| 50 | `NVK20250331: cannot resolve TK '8211'` — TK 8211 (Chi phí thuế TNDN hiện hành) missing from account mapping |
| 36 | `bảng kê BR invoice not provided for BH...` — BH voucher requires `Bảng kê BR` companion file that's not attached |
| 28 | `UOMMustBeIntegerError` — Item UOM "Cái" or similar non-integer-allowed UOM, but voucher has fractional qty |
| 24 | `Grand Total must be >= 0` — credit-note semantics on Sales Invoice not handled |
| 24 | `MandatoryError: cost_center` on Payment Entry — multi-leg UNC fallback path missing cost_center |
| 28 | `is not a stock Item` — PI line tries to update_stock=1 on Item where is_stock_item=0 |
| 22 | `Party Type and Party is required for 131/331` — multi-leg JE handler not setting party on receivable/payable legs |

## Recommended Next Steps (priority order)

1. **Fix `_party_cache` case-insensitivity** — store lowercase keys in `_CUSTOMERS`/`_SUPPLIERS`/`_EMPLOYEES` sets; lookup via `code.lower()`. Eliminates ~3848 failures. ~10 LOC.

2. **Fix expense_account leaf resolution** — `_resolve_account` for expense lines must descend to a leaf if it lands on `is_group=1`. ERPNext rejects group accounts on PI items. Either (a) pre-cache `account_number → leaf_name` mapping, or (b) when resolving "156" prefer leaf "1561"/"1562" by suffix policy. Eliminates ~2756 failures.

3. **Investigate TK 331 +17B** — query GL Entry by voucher_type to identify which docs are posting Dr 331 unexpectedly. Likely PE backfill amend pass mis-allocating, OR PI handler picking 331 Dr by accident on credit-note-like vouchers.

4. **Add PBCC handler / NVK 8211 mapping / cost_center fallback** — incremental handler additions. ~30-50 LOC each.

5. **TK 141 root cause** — activity inflation persists even after parser dedup. Likely UNC paying advances to non-Employee party (Misa stores party_code that doesn't match any Employee record), OR the OB JE itself includes activity that Misa expects to net out.

6. **TK 4211/4212/421 close-out missing** — P&L closing entries (Dr 511 / Cr 421 + Dr 421 / Cr 632 + similar) may not be in Misa OB JE. Compare Misa SCT 421 entry-by-entry against ERPNext.

7. **Optional: PN → Material Receipt SE refactor** — defer until business prioritizes inventory-value-traceability.
