# Non-Deductible Expense Tracking — Spec

**Status:** Draft → Phase 1 in implementation
**Created:** 2026-05-25
**Owner:** vn_accounting (core flag + report). Consumers: dcnet_pakd (Phase 1), ERPNext PI/EC/Asset/Payroll (Phase 2).
**Legal basis:** Nghị định 320/2025/NĐ-CP Điều 9-10 (chi phí được trừ); Form 03/TNDN chỉ tiêu B4; VAS Chuẩn mực 17 (Thuế TNDN — chênh lệch vĩnh viễn).

---

## 1. Business Context

VAS yêu cầu ghi nhận đầy đủ chi phí thực phát sinh vào sổ cái → BCTC official (B01/B02/B03/B09) phản ánh đúng đời sống DN. Khi quyết toán TNDN (Form 03/TNDN), kế toán cộng lại chi phí non-deductible vào chỉ tiêu B4 → ra Thu nhập chịu thuế.

**Pattern A** (per-voucher tag): đánh dấu cờ `is_non_deductible` trên từng JE Account row tại entry-point. Báo cáo B4 aggregate `WHERE is_non_deductible=1`. Pattern này được chọn (over Pattern B sub-account split) vì:

- Auto-set khả thi cao tại entry-point có đủ context (PAKD MS/AC, PI bill_no, etc.)
- Multi-company không cần config bội số
- Rule năm thay năm: retro-tag mềm dẻo, không cần JE correction
- Combinable với `is_related_party` (Phase 4 FDI overlay) — 2 dimension độc lập trên cùng row

**Không hỗ trợ practice "2 sổ"** (Luật Kế toán 2015 Điều 13 cấm) — 1 sổ trung thực + flag phân loại là cách hợp pháp duy nhất.

---

## 2. Scope & Phasing

### Phase 1 — Foundation + dcnet_pakd (THIS SESSION)
- Core flag trên `Journal Entry Account` row (vn_accounting fixture)
- Auto-set heuristic trong `dcnet_pakd.integrations.accounting.post_beneficiary_je` + `post_journal_entry`
- Script Report "BC chi phí không được trừ" (vn_accounting)
- Unit tests cho heuristic
- Sample demo entries (deferred — needs dcnet_sample touch)

### Phase 2 — Source-doc propagation (next session)
- Purchase Invoice Item.is_non_deductible → propagate xuống GL on submit
- Expense Claim Detail.is_non_deductible
- Asset.is_welfare_asset + Asset Category convention → propagate vào depreciation auto-JE
- Salary Component config field → propagate qua Salary Slip

### Phase 3 — Report integration + thuyết minh (next session)
- Form 03/TNDN autofill B4 (cần check vn_accounting đã có Form 03 chưa)
- B09 Thuyết minh — section "Giải trình chênh lệch thuế TNDN" (effective tax rate analysis)
- Annual reconciliation: LN kế toán + B4 + B5/B6 - ... = Thu nhập chịu thuế

### Phase 4 (optional, defer) — Related-party overlay
- Custom Field `is_related_party` trên cùng JE Account row
- Convention sub-account `.RP` cho intra-group transactions
- Transfer Pricing Documentation tracking (NĐ 132/2020 + NĐ 20/2025)
- FCT withholding (TT 103/2014) cho cross-border MS

---

## 3. Phase 1 Detail

### 3.1 Core Custom Fields

`Journal Entry Account` (child table — ship via `apps/vn_accounting/vn_accounting/fixtures/custom_field.json`):

| Field | Type | Reqd | Default | Notes |
|---|---|---|---|---|
| `is_non_deductible` | Check | 0 | 0 | Tracked (Frappe Version) for audit trail |
| `non_deductible_reason` | Select | 0 | "" | Options: rỗng / "Không HĐ hợp lệ" / "Vượt định mức quy định" / "Không liên quan SXKD" / "Tiền phạt (thuế / BHXH / hợp đồng)" / "Related-party không TP doc" / "Khác" |

**Placement:** insert after `project_costing_stage` (existing Custom Field on JE Account). Both fields visible in default JE form via "in_list_view: 0" + "in_standard_filter: 1" so list view stays clean; KTT có thể filter.

**Validation** — controller hook on `Journal Entry.validate()` in vn_accounting:
```python
for row in doc.accounts:
    if row.is_non_deductible and not row.non_deductible_reason:
        frappe.throw(_("Dòng {0}: Phải chọn lý do khi đánh dấu Không được trừ").format(row.idx))
    if row.non_deductible_reason and not row.is_non_deductible:
        # User picked reason but forgot to tick — auto-tick (helpful)
        row.is_non_deductible = 1
```

### 3.2 Helper module — `vn_accounting.api.non_deductible`

Single public helper `mark_non_deductible(je_account_row, reason)` so caller code stays clean:
```python
def mark_non_deductible(row, reason: str) -> None:
    row.is_non_deductible = 1
    row.non_deductible_reason = reason
```
Used by Phase 1 (PAKD) + Phase 2 callers (PI/EC/Asset/Payroll). Single point of change if schema evolves.

### 3.3 PAKD Auto-set Logic

**File:** `apps/dcnet_pakd/dcnet_pakd/dcnet_pakd/integrations/accounting.py`

Heuristic for `post_beneficiary_je()` (MS/AC/Referral):
```python
def _is_non_deductible_beneficiary(line) -> tuple[bool, str]:
    """Return (flag, reason) per VAS NĐ 320/2025 Điều 9-10."""
    # Has invoice → deductible regardless of recipient type
    if (line.invoice_no or "").strip():
        return False, ""
    # Recipient không khấu trừ TNCN + không HĐ → khả năng cao non-deductible
    if line.recipient_name and float(line.recipient_tax_pct or 0) == 0:
        return True, "Không HĐ hợp lệ"
    # Generic (no recipient — internal allocation) → defer to manual review
    return False, ""
```

Heuristic for `post_journal_entry()` SC/LF components:
- Sales Commission via bypass-HRMS → posted as DR 6411 / CR Employee Payable: **deductible** (đã có party Employee + đi qua bảng lương sau này)
- License Fee → **deductible** (phí nhà nước, có biên lai/HĐ)
- → both default `is_non_deductible=0`, no auto-set needed in Phase 1

Mark only on DR expense leg (not CR liability leg) — B4 aggregate WHERE debit > 0 + flag.

### 3.4 Manual Override

KTT có thể tick/untick flag trên JE form trước khi submit. Validation hook ensures reason chosen. After submit, flag editable via Customize Form → set `allow_on_submit: 1` OR provide a "Cập nhật phân loại thuế" wizard (deferred to Phase 3 — for now flag immutable post-submit).

### 3.5 Script Report — "BC chi phí không được trừ"

**Path:** `apps/vn_accounting/vn_accounting/report/bao_cao_chi_phi_khong_duoc_tru/`

**Filters:**
- Company (Link → Company, reqd)
- From Date / To Date (default = current fiscal year)
- Group By: Account / Party / Reason / Voucher (default Account)
- Include Cancelled JEs: Check (default 0)

**Query:**
```sql
SELECT
    jea.account, jea.party_type, jea.party,
    jea.non_deductible_reason AS reason,
    je.name AS voucher, je.posting_date,
    jea.debit_in_account_currency AS amount,
    je.user_remark AS remark
FROM `tabJournal Entry Account` jea
JOIN `tabJournal Entry` je ON je.name = jea.parent
WHERE jea.is_non_deductible = 1
  AND je.docstatus = 1
  AND je.company = %(company)s
  AND je.posting_date BETWEEN %(from_date)s AND %(to_date)s
  AND jea.debit_in_account_currency > 0
ORDER BY je.posting_date, jea.account
```

**Output columns:** Posting Date | Voucher | Account | Party | Reason | Amount | Remark
**Footer:** "Tổng cộng B4: {total}" — to be entered manually on Form 03/TNDN until Phase 3 autofill.

### 3.6 Permission

- Anyone with `Journal Entry` write can set flag (no separate role).
- Audit trail via Frappe Version (tracking=True on Custom Field) — auditor sees who set/changed.
- Report accessible to Accounts User + Accounts Manager (default DocPerm).

---

## 4. Phase 2 Detail (spec only, defer to next session)

### 4.1 Purchase Invoice

Custom Field on `Purchase Invoice Item`:
- `is_non_deductible` (Check)
- `non_deductible_reason` (Select — same options as JE Account)

**Auto-set on PI.validate()** in vn_accounting:
- `bill_no` IS NULL or empty → suggest flag (notification, not auto — bill_no có thể nhập sau)
- `supplier.disabled = 1` (NCC đã ngừng hoạt động) → auto-flag with reason "Không HĐ hợp lệ"
- Manual flag always allowed

**Propagation to GL** — hook `Purchase Invoice.on_submit`:
- For each PI Item with is_non_deductible=1, find the matching expense GL Entry (account = item.expense_account) and mirror flag onto corresponding JE Account row.
- Catch: ERPNext doesn't create JE for PI by default — creates GL Entry directly. So flag goes onto GL Entry, not JE Account. Need a parallel Custom Field on `GL Entry`?

**Decision:** keep flag at JE Account level (Phase 1 schema). For PI/EC/Payroll which post via GL Entry directly (not via JE), add Custom Field on `GL Entry` AS WELL. Report queries both:
```sql
SELECT ... FROM `tabGL Entry` WHERE is_non_deductible=1 AND debit > 0 ...
UNION
SELECT ... FROM `tabJournal Entry Account` jea JOIN tabJournal Entry je ... WHERE jea.is_non_deductible=1 ...
```
Or simpler: report queries ONLY `GL Entry` (which is the source of truth for B4) — both PI direct-GL and JE Account write to GL Entry. **Phase 1 should also add flag to GL Entry** to keep schema consistent.

→ **AMEND PHASE 1 SCOPE:** add Custom Field `is_non_deductible` + `non_deductible_reason` to BOTH `Journal Entry Account` AND `GL Entry`. PAKD posts JE directly so JE Account is primary path; report aggregates from GL Entry which receives propagated value via JE.on_submit hook.

### 4.2 Expense Claim

Custom Field on `Expense Claim Detail`:
- `is_non_deductible` (Check)
- `non_deductible_reason` (Select)

**Auto-set on EC.validate():** none — manual flag, but offer category-based suggestion via JS hook (e.g. category in {Tiếp khách, Du lịch nội bộ} → show toast "Cân nhắc đánh dấu không được trừ").

Propagate to GL Entry on EC.on_submit.

### 4.3 Asset Depreciation

Custom Field on `Asset`:
- `is_welfare_asset` (Check) — TSCĐ phục vụ phúc lợi cá nhân (không phải SXKD)

Custom Field on `Asset Category`:
- `vehicle_seat_limit_applied` (Check) — áp dụng giới hạn xe ≤9 chỗ giá >1.6 tỷ (NĐ 320/2025)
- `vehicle_cost_threshold` (Currency) — default 1,600,000,000

**Auto-set on Asset Depreciation schedule generation:**
- If `asset.is_welfare_asset = 1` → flag entire depreciation amount as non-deductible
- If `asset_category.vehicle_seat_limit_applied = 1` AND `asset.purchase_cost > vehicle_cost_threshold`:
  - Deductible portion: `purchase_cost × (threshold / purchase_cost)` of each period's depreciation
  - Non-deductible portion: balance — needs TWO JE rows per period (one deductible, one not)
  - Complex — needs careful design

→ Phase 2 may split into 2.A (welfare flag, simple) + 2.B (vehicle cap, complex split logic).

### 4.4 Payroll

Custom Field on `Salary Component`:
- `is_non_deductible` (Check) — applied to entire component when present in Salary Slip
- `non_deductible_reason` (Select)

**Examples:**
- Component "Tiền phạt BHXH chậm nộp" → flag=1, reason="Tiền phạt"
- Component "Phúc lợi vượt mức" → flag=1, reason="Vượt định mức"
- Standard salary components → flag=0

**Propagation:** Salary Slip submit → JE auto-created by ERPNext → for each component row, propagate flag onto matching JE Account row.

### 4.5 Manual JE — KTT post tiền phạt thuế

No auto-set. Just expose the field on JE form. Document in KTT training: post tiền phạt thuế → tick non_deductible + reason="Tiền phạt".

---

## 5. Phase 3 Detail (spec only, defer)

### 5.1 Form 03/TNDN autofill B4

If vn_accounting has Form 03/TNDN script report (check needed): add B4 row that auto-fills from `_b4_total = SUM(is_non_deductible=1 GL Entry debits in fiscal year)`. If no Form 03 yet, build standalone.

### 5.2 B09 Thuyết minh — Giải trình chênh lệch thuế TNDN

Section trong B09 mẫu:
```
6. Chi phí thuế thu nhập doanh nghiệp
   Lợi nhuận kế toán trước thuế: X
   × thuế suất 20%
   = Thuế TNDN theo LN kế toán: 0.2X

   Điều chỉnh:
   + Chi phí không được trừ (B4): Y
   - Thu nhập miễn thuế: Z
   = Thu nhập chịu thuế: X + Y - Z
   × 20%
   = Thuế TNDN phải nộp: 0.2(X + Y - Z)

   Tỷ lệ thuế hiệu lực: thuế thực nộp / LN kế toán = K%
   Chênh lệch K% so với 20% chuẩn được giải trình bởi:
   - CP không được trừ Y, chi tiết: ...
   - Thu nhập miễn thuế Z, chi tiết: ...
```

### 5.3 Annual Reconciliation Report

Standalone Script Report: `Quyết toán TNDN — Reconciliation`. Output:
- Section A: LN kế toán từng tháng (B02 KQKD aggregate)
- Section B: Adjustments
  - B4 (CP không trừ) — drill-down link to "BC chi phí không được trừ"
  - B5/B6/... (other adjustments per Form 03)
- Section C: Thu nhập chịu thuế + Thuế phải nộp
- Comparison vs CIT advance payments made through year (TK 3334)
- Output: số phải nộp thêm hoặc thu hồi cuối năm

---

## 6. Edge Cases

### 6.1 Khi nào auto-set sai?

- **PAKD MS/AC với recipient_tax_pct=0** nhưng thực tế recipient có HĐ → false positive non-deductible
  → Manual override allowed (KTT untick before submit). Reason field surfaces issue cho audit.
- **PAKD MS/AC với recipient_tax_pct>0** nhưng HĐ không hợp lệ (hết hạn, sai mẫu) → false negative
  → Manual flag required (no auto).
- **PI bill_no** entered AFTER initial save (procurement workflow) → flag không nên auto on first save
  → Use validate hook on SUBMIT not on SAVE. KTT có thời gian update.

### 6.2 Khi nào reason field không phù hợp?

- Multi-reason scenario (vd: vừa vượt định mức vừa không HĐ) → Select chỉ 1 value
  → Decision: pick most material reason; document the secondary in user_remark. Phase 4 có thể đổi sang Table MultiSelect nếu thường xuyên cần.

### 6.3 Cancellation / Reversal

- JE cancelled (docstatus=2): GL Entry `is_cancelled=1`. Report MUST filter `is_cancelled=0` else double-count.
- Amend (copy + new docstatus=0): new JE inherits flag values from amended_from? **NO** — Frappe copy_doc copies child rows verbatim including Custom Field values. ✓
- Credit Note for PI: reverses GL with opposite sign. Reversal GL Entry inherits flag → SUM net = 0 → no impact on B4 (correct behavior).

### 6.4 Cross-fiscal-year

- Flag persisted on row, not on a yearly setting → no special handling.
- Rule changes year-to-year (e.g. NĐ 320 hạ ngưỡng tiền mặt từ 20tr → 5tr 1/7/2025): retro-tag entries pre/post threshold via batch script. Provide `vn_accounting.api.audit_non_deductible(from_date, to_date, rules)` utility.

### 6.5 Permission edge

- User without Accounts role tries to flag → no row-level permission on Custom Field. Inherit JE Account perm = inherit parent JE perm. Acceptable.
- Audit auditor wants read-only view → existing Accounts Manager read access sufficient.

### 6.6 GL Entry direct vs JE Account

- PI/EC/Payroll/Sales Invoice → ERPNext creates GL Entry directly (not via JE)
- JE manual → JE Account row → on_submit creates GL Entry mirroring values
- → Flag must be on BOTH `Journal Entry Account` AND `GL Entry` schemas.
- → JE.on_submit hook propagates flag from JE Account → newly-created GL Entry rows.
- → PI/EC/Asset/Payroll on_submit hooks (Phase 2) set flag on GL Entry directly.

### 6.7 Backfill historical data

- Misa migration imported 5090 GL entries — none flagged. Batch script `vn_accounting.api.backfill_non_deductible_from_pakd()` re-scans PAKD posted JEs and tags retroactively where heuristic matches.
- Other sources: manual review with KTT — auto-set heuristics too risky for historical bulk.

### 6.8 Multi-company

- Flag is row-level → multi-company native support. Report filter on company explicitly.
- PAKD Settings already per-company aware (resolver pattern from prior session). Auto-set logic doesn't need company-specific config.

---

## 7. Self-Review

### 7.1 Spec coverage — every Phase 1 task covered?
- [x] Phase 1.1 Custom Fields — Section 3.1, 3.2 + amended to include GL Entry per Edge Case 6.6
- [x] Phase 1.2 Auto-set in dcnet_pakd — Section 3.3
- [x] Phase 1.3 Script Report — Section 3.5
- [x] Phase 1.4 Tests — implied by 3.3 heuristic function (pure, testable)

### 7.2 Placeholder scan
- No TBD / TODO in Phase 1 sections
- Phase 2/3 marked "spec only, defer to next session" explicitly

### 7.3 Type consistency
- `is_non_deductible: int` (0/1) across JE Account + GL Entry + PI Item + EC Detail + Asset + Salary Component — consistent
- `non_deductible_reason: str` Select — consistent
- helper `mark_non_deductible(row, reason)` accepts any row with these fields → duck-typed

### 7.4 Copy-paste test for code blocks
- Heuristic function `_is_non_deductible_beneficiary(line)` references `line.invoice_no`, `line.recipient_name`, `line.recipient_tax_pct` — all exist on `PAKD Beneficiary Line` (verified via prior session reads)
- Validation hook references `doc.accounts`, `row.is_non_deductible`, `row.non_deductible_reason`, `row.idx` — all valid Frappe JE Account fields
- SQL query: `tabJournal Entry Account`, `tabJournal Entry` — valid table names; field names match Custom Field declarations

### 7.5 Risks
- **R1:** Validation hook on JE.validate() might break existing JE saves if KTT had set reason without flag (unlikely on fresh field, no data yet). Mitigation: ensure default both fields = 0 / "" on fixture install.
- **R2:** Auto-set heuristic in PAKD might surprise KTT (unexpected flag). Mitigation: log auto-set to user_remark on the DR row: "Tự động đánh dấu: Không HĐ hợp lệ".
- **R3:** GL Entry Custom Field requires ERPNext version compat — verify Frappe v16 + ERPNext v16.18 allows Custom Field on GL Entry (mostly readonly system DocType). Need check.
- **R4:** Report performance on 5090+ GL entries — single-table query on indexed columns (company, posting_date, is_non_deductible) → acceptable. Add DB index on `(is_non_deductible, company, posting_date)` if slow.

### 7.6 Why-questions answered
- Why not Pattern B? — See Section 1 + prior conversation comparison.
- Why JE Account + GL Entry both? — Edge Case 6.6. Different post paths need different host fields.
- Why default `is_non_deductible=0`? — Most expenses are deductible. Flag is exception, not norm.
- Why Select for reason (not Free Text)? — Aggregation in report needs canonical values. "Khác" + remark for edge cases.

---

## 8. Implementation Order (Phase 1)

1. **vn_accounting fixture: Custom Field on JE Account + GL Entry** (Edge Case 6.6 amendment)
2. **vn_accounting.api.non_deductible: helper `mark_non_deductible()`**
3. **vn_accounting JE validate hook: reason required if flag**
4. **vn_accounting JE on_submit hook: propagate JE Account flag → GL Entry**
5. **dcnet_pakd accounting.py: heuristic `_is_non_deductible_beneficiary` + apply in post_beneficiary_je + post_journal_entry**
6. **Unit tests for heuristic + integration test for JE+GL flag mirror**
7. **vn_accounting Script Report "BC chi phí không được trừ"**
8. **bench migrate + bench restart + smoke test**
9. **Session-last update with Phase 2/3 next-session tasks**

---

## 9. Out of scope (Phase 1)

- Phase 2 source-doc propagation (PI/EC/Asset/Payroll)
- Phase 3 Form 03/TNDN + B09 + reconciliation
- Phase 4 related-party overlay
- Sample data seeding in dcnet_sample (deferred to spec follow-up)
- KTT training documentation (deferred)
- UI on JE form for editing flag after submit (use Customize Form if needed urgently)
