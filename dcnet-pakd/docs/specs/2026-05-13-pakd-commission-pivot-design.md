# PAKD commission_lines pivot view — design spec

**Date:** 2026-05-13 · revised 2026-05-14 (v0.2.0 realignment §4.5)
**Driver:** FB-2026-00587 (Long, 2026-05-13 04:55) — "Cách thể hiện này không khoa học lắm. Nên thể hiện dạng bảng ngang với các cột là kỳ thu tiền còn hàng là Thành phần, Trạng thái, bổ sung thêm nút hành động tương ứng với trạng thái và Số tiền ở kỳ tương ứng ở hợp đồng"
**Status:** Approved 2026-05-13 → revised 2026-05-14 for revision-aware pivot + Beneficiary rows
**Skill:** brainstorming

## v0.2.0 changes — 2026-05-14

The pivot was rebuilt to align with the realignment spec (`docs/specs/2026-05-14-contract-pakd-vnacc-realignment.md`):

1. **FTTH branch removed (D4).** Monthly FTTH Rollup is gone; per-HD PAKDs use the standard Recurring Telecom layout.
2. **Rows split across two tables.**
   - `commission_lines` (existing): Sales Commission + License Fee — per-(period, component) cells with full Pending/Posted/Skipped/Cancelled lifecycle.
   - `beneficiary_lines` (new — §3.3): Manager Services + Add Costs + Referral — 1 row per kind/recipient. Pivot renders each as a row keyed `BL:<row_name>`. Per Period rows fill every billing period (`month_index >= 1`); One-off Referral shows only at the first paid period.
3. **Revision color band.** Each pivot column gets a 4px top border colour-coded by the PAKD Revision active at that period (`resolve_active_revision` — Approved revisions with `effective_from ≤ period_start_date`, latest wins). A legend below the toolbar lists revisions in play. Up to 6 distinct colours cycle (`rev_idx % 6`).
4. **Beneficiary click popover.** Beneficiary cells open `_open_beneficiary_popover` (row-level). Single "Đăng JE ngay" action calls `dcnet_pakd.dcnet_pakd.api.post_beneficiary_now`. Commission cells (SC + License) keep the existing post/skip/override popover.
5. **Per-period beneficiary tracking deferred to v0.3.0.** `beneficiary_lines` have a single row-level state (Pending → Posted), so a Per Period beneficiary that has been Posted for kỳ N still renders the same Posted style in subsequent kỳ N+1 cells until a new posting event mutates the row. The popover surfaces this limitation explicitly.

## 1. Goal & scope

Replace the 48-row vertical `commission_lines` child table on the PAKD form (`Phuong An Kinh Doanh`) with a horizontal pivot grid. Cells are clickable and open a rich Frappe Dialog popover with status-appropriate actions.

**In scope:**
- Pivot rendering for all 3 PAKD types: Recurring Telecom (N periods × 4 components), One-off Sale/Project (1 period × 4 components), Monthly FTTH Rollup (1 period × N PAKD Items).
- Per-cell click → popover (default) opening on any state.
- Posting actions: per-period (default click target inside the popover; preserves today's bundled JE shape) **and** per-cell (`Ctrl/Cmd+click` shortcut or `Chỉ đăng dòng này` button; creates a 2-leg JE for one component only).
- Skip a single cell (state transition: Pending → **Skipped**, new 4th state).
- Per-cell rate override (new `override_rate` field on `PAKD Commission Line`; engine precedence updated).
- History display in popover (sourced from `tabVersion` rows + `frappe.log_activity` events).
- Sticky first column, sticky totals row + column.
- Desktop full-pivot; mobile = horizontal scroll with sticky label column.

**Out of scope (deferred to v2):**
- Bulk per-row "Đăng toàn dòng (all periods)" — explicit user choice to defer.
- Pivot export to CSV/Excel — frappe report export already covers Commission Register.
- Real-time websocket updates if another user posts a cell.

## 2. Data model changes (`PAKD Commission Line`)

| Field | Type | Add/change | Notes |
|---|---|---|---|
| `state` | Select | extend options: `Pending\nPosted\nCancelled\nSkipped` | Skipped = user explicitly excluded this cell from posting; engine respects (does not recreate on save) |
| `override_rate` | Percent (precision 2) | new | Blank/0 = use PAKD-wide override > template rate (truthy check, matches frappe-erpnext rule about Frappe Percent fields). Description: "Để trống = dùng tỷ lệ PAKD-wide hoặc mẫu." |
| `posted_by_cell` | Check | new, default 0 | 1 when the JE was created via single-cell post (not bundled period). Surfaces in Commission Register as a separate column. |
| `skip_reason` | Small Text | new | Captured when state transitions to Skipped. Required when state=Skipped via the API. |

### Override precedence (updated)
Conceptual effective rate for any line:

```
effective_rate(line) =
  line.override_rate          if line.override_rate (truthy)
  else pakd.commission_overrides[component].override_rate  if truthy
  else template_rate(component)
```

**Implementation note:** `utils/engine.py::compute_lines` already takes a `dict[component_name → override_rate]` (PAKD-wide). It is **not** modified for this work — per-line overrides are not a function of the engine's input (engine computes totals across items; it doesn't know about billing periods).

The per-line override is applied **after the engine returns**, inside `_sync_commission_lines`, as a ratio:
```python
upstream_rate = pakd_override_map.get(line.component) or template_rate(line.component)
if line.override_rate and upstream_rate:
    line.amount = round(line.amount * line.override_rate / upstream_rate)
```
Since `total_<component>` (engine output) reflects the upstream rate, this ratio correctly rescales just the affected line. Other lines for the same component stay at the upstream rate.

Skipped + Cancelled rows are **not** re-synced (their `amount` and `state` stay fixed; engine doesn't recreate or touch them on PAKD save). If a previously-Skipped (period, component) pair appears in `needed`, the engine still skips it — the user's skip decision wins.

### Patches
- `patches/v0_2_0/add_commission_line_skipped_state.py` — `frappe.reload_doc("dcnet_pakd","doctype","pakd_commission_line", force=True)` so the new Select option, override_rate, posted_by_cell, skip_reason are in meta before any code reads them. Idempotent.

## 3. UI / pivot grid layout

### Structure
```
┌─────────────────┬──────────────┬──────────────┬─────┬───────────────┐
│  (sticky col)   │ Kỳ 1         │ Kỳ 2         │ ... │ Tổng / dòng   │
│                 │ SINV-... »   │ (chưa SI)    │     │               │
├─────────────────┼──────────────┼──────────────┼─────┼───────────────┤
│ MS    10%       │ 1 500  ✓     │ 1 500  ○     │ ... │ 18 000        │
│ AC    75%       │   500  ✓     │   500  ○     │ ... │  6 000        │
│ GPVT   2.2%     │   330  ✓     │   330  ○     │ ... │  3 960        │
│ SC     6%       │   900  ✓     │   900  ○     │ ... │ 10 800        │
├─────────────────┼──────────────┼──────────────┼─────┼───────────────┤
│ Tổng / kỳ       │ 3 230        │ 3 230        │ ... │ 38 760        │
└─────────────────┴──────────────┴──────────────┴─────┴───────────────┘
```

### Column header anatomy
- Top line: `Kỳ <month_index>` (large, bold).
- Bottom line: SI link if BS row has `sales_invoice`; PE link if BS state=Paid (preferring PE for paid rows since that's where commission posting was triggered); else muted `(chưa SI)`.
- Click the header → navigate to the linked SI/PE in a new tab.

### Row anatomy (Recurring Telecom + One-off)
- Component name + effective rate %, with a subtle indicator (italic + tooltip) when the rate differs from the template (i.e., a PAKD-wide override or a per-line override is in play for this row's cells).

### Row anatomy (Monthly FTTH Rollup)
- Each row = one PAKD Item.
- Label: `<item_code> · <description>` + `<salary_coefficient>%`
- Single column = the rollup period.

### Cells
- Number formatted with `vi-VN` locale (e.g. `1.500` not `1,500`).
- Status indicator (right side or below the amount):
  - `○` Pending  — gray text + light gray cell bg
  - `✓` Posted   — green text + light green cell bg
  - `⨯` Cancelled — red text + light red cell bg, strikethrough on amount
  - `↷` Skipped  — amber tint, strikethrough on amount
- `[posted_by_cell=1]` adds a tiny superscript `c` next to `✓` so it's distinguishable from period-bundle Posted (useful for accountants debugging fragmented JEs).
- Hover → subtle outline; click → opens popover (Frappe Dialog).

### Totals
- **Per-component (last column):** sum of `amount` across `state ∈ {Pending, Posted}` in this row (excludes Skipped + Cancelled).
- **Per-period (last row):** sum of `amount` across all components for this column where `state ∈ {Pending, Posted}`.
- **Grand total (bottom-right):** sum of all rows × all columns where `state ∈ {Pending, Posted}`.
- Tooltip on each total: "Đã trừ <N> dòng bị bỏ qua / huỷ".

### Sticky behavior
- First column (component label) sticky during horizontal scroll.
- Last column (per-component total) sticky during horizontal scroll.
- The pivot has 4-N rows total (4 components + 1 totals row for Recurring/One-off; up to M+1 for FTTH). No internal vertical scroll inside the section — drop sticky-last-row.
- Implementation: `position: sticky` with explicit `z-index` ladder so the bottom-right "grand total" cell is on top of both adjacent sticky planes.

### Mobile (<768px viewport)
- Same pivot, scrollable horizontally. Sticky first column stays.
- Visual hint: a faded right-edge gradient indicating more content. Show only when scrollable.

## 4. Cell popover (Frappe Dialog)

Title bar: `<Component | Item> · Kỳ <N> · T<MM/YY>`

### Body sections
1. **Số tiền + Trạng thái** — single line summary
2. **Tỷ lệ áp dụng** — shows the effective rate + source: "6% (mặc định mẫu)" / "3% (override PAKD-wide)" / "4% (override dòng)"
3. **Refs** — list of linked SI / PE / JE / AS, each clickable; muted dashes when not set
4. **Lịch sử** — last 5 entries from `tabVersion` + `frappe.log_activity` for this line, sorted desc

### Action area (status-dependent)

| Current state | Buttons |
|---|---|
| **Pending** | `[Đăng toàn kỳ (<P> dòng)]` (primary; P = count of Pending lines in this column) · `[Chỉ đăng dòng này]` · `[Bỏ qua dòng này]` · `[Tuỳ chỉnh tỷ lệ: __ %]` `[Áp dụng]` |
| **Posted** | `[Mở JE »]` (primary; if JE still exists) · `[Đảo bút toán]` (cancels draft JE; msgprint redirects to manual reversal if JE submitted) |
| **Cancelled** | `[Khôi phục về Chờ]` · `[Mở JE »]` if `line.journal_entry` still exists, else muted "JE đã bị xóa khi huỷ" |
| **Skipped** | `[Khôi phục về Chờ]` · displays `skip_reason` |

**HRMS-mode caveat for `[Chỉ đăng dòng này]` on Sales Commission:** when `PAKD Settings.use_hrms_for_commission = 1`, Sales Commission flows through Additional Salary (one AS per month aggregating all SC), not a JE. The `[Chỉ đăng dòng này]` button is **hidden** on SC cells in HRMS mode — only `[Đăng toàn kỳ]` is available, which creates the bundled JE for MS/AC/GPVT and an AS for SC together. Cell-mode single-component post is only meaningful for non-AS components.

**Reopen semantic:** transitioning Cancelled → Pending OR Skipped → Pending is a **state-only** change. It does **not** auto-create a new JE. The line goes back to the Pending column tint; user must explicitly click Post again afterwards if they want to re-post.

### Ctrl/Cmd+click shortcut
- On Pending cell: bypasses popover, fires "Chỉ đăng dòng này" directly.
- Tooltip on cell: "Click: chi tiết · Ctrl+click: đăng nhanh dòng này"

## 5. Backend API (whitelisted)

All endpoints validate role permissions (see §7).

```python
# api.py additions
# All endpoints: frappe.throw(PermissionError) if caller lacks role per §7.

@frappe.whitelist()
def post_pakd_commission_period(pakd: str, month_index: int) -> dict:
    """Post all Pending lines in this PAKD's column.

    Internally calls _post_pakd_commission_lines(pakd, month_index, pe_doc).
    pe_doc is the most recent submitted Receive PE for the SI of this period's
    BS row (existing _auto_post_on_approval lookup logic). If no PE exists,
    use a synthetic SimpleNamespace(name="", posting_date=today()).

    Returns: {"je": <je_name>, "as": <as_name or None>, "lines_posted": <n>}
    """

@frappe.whitelist()
def post_pakd_commission_line(line_name: str) -> dict:
    """Create a 2-leg JE for this single component+period (cell mode).

    Refuses with frappe.throw if:
      - line.component == "Sales Commission" AND PAKD Settings.use_hrms_for_commission=1
        (AS doesn't support single-row posting; force user to use period-bundle)
      - line.state != "Pending"

    Marks line.posted_by_cell=1, line.state=Posted, line.journal_entry=<je>.
    JE remark: 'PAKD commission CELL <component> <YYYY-MM> | PAKD <name> | line <line_name>'.
    payroll_month is computed via the existing cutoff_day logic with payment_date=today().

    Returns: {"je": <je_name>, "amount": <amount>}
    """

@frappe.whitelist()
def skip_pakd_commission_line(line_name: str, reason: str) -> dict:
    """Transition Pending → Skipped. Requires non-empty reason (≥3 chars).
    Writes frappe.add_comment("Comment", reason) on the parent PAKD so the
    timeline records who skipped + when + why. Returns: {"state": "Skipped"}.
    """

@frappe.whitelist()
def set_pakd_commission_line_override(line_name: str, override_rate) -> dict:
    """Set line.override_rate. Empty string, "0", 0, "null", null → clear (use upstream).

    Implementation: set the override via frappe.db.set_value, then load the
    parent PAKD and call pakd_doc.save(ignore_permissions=False). The save
    triggers _sync_commission_lines which applies the ratio rescale (§2).

    Returns: {"old_amount": <prev>, "new_amount": <new>, "effective_rate": <r>}.
    """

@frappe.whitelist()
def reopen_pakd_commission_line(line_name: str) -> dict:
    """Cancelled or Skipped → Pending (state-only; does NOT re-post).
    If line.journal_entry is set AND that JE is a Draft (docstatus=0), delete it.
    If the JE is Submitted (docstatus=1), refuse with frappe.throw and direct
    user to manual reversal. Writes add_comment on parent PAKD.

    Returns: {"state": "Pending"}.
    """
```

## 6. JE shape

| Mode | use_hrms | Shape | Remark | posted_by_cell |
|---|---|---|---|---|
| Period bundle | 0 (bypass) | 4 DR + 4 CR (including SC with party=Employee) | `PAKD commission <YYYY-MM> \| PAKD <name> \| PE <pe>` | 0 |
| Period bundle | 1 (HRMS)   | 3 DR + 3 CR for MS/AC/GPVT, + 1 AS row for SC | same remark; AS separate | 0 |
| Per-cell      | 0 (bypass) | 2 legs (DR component / CR counter; party=Employee if SC) | `PAKD commission CELL <component> <YYYY-MM> \| PAKD <name> \| line <line_name>` | 1 |
| Per-cell      | 1 (HRMS)   | 2 legs for MS/AC/GPVT only; **SC cell-post is refused** — see §4 popover note | same per-cell remark | 1 |

Period bundle uses existing `post_journal_entry()` in `integrations/accounting.py`. Per-cell uses a new `post_journal_entry_single(pakd_doc, line, payroll_month)` that takes a single line and writes the `posted_by_cell=1` marker.

## 7. Permissions

| Action | Required role(s) |
|---|---|
| View pivot | (same as current PAKD read) — PAKD Sales Rep, PAKD Sales Director, PAKD General Department, PAKD Branch Director, PAKD Board, PAKD Accountant, Accounts Manager, System Manager |
| Post period or cell | PAKD Accountant **or** PAKD Board **or** Accounts Manager |
| Skip | PAKD Board **or** Accounts Manager |
| Set override_rate (per-line) | PAKD Board **or** Accounts Manager — **disabled when state ≠ Pending** |
| Reopen Cancelled / Skipped | Accounts Manager (writes audit log) |

Enforcement via `frappe.has_permission` + explicit role check inside each API endpoint. `frappe.throw(_("Không đủ quyền — cần Accounts Manager hoặc PAKD Board"), frappe.PermissionError)` on fail.

## 8. Engine integration

`_sync_commission_lines` in `phuong_an_kinh_doanh.py`:
- Keeps current behavior for `state == 'Posted'` (preserve unchanged; pop from `needed` so we don't recreate).
- Adds: `state in ('Skipped', 'Cancelled')` → preserve unchanged AND pop from `needed` so the (period, component) is not recreated as a Pending row alongside it.
- Pending rows get their `amount` from `needed[(period, component)]` as today.
- **New step at end** (after the existing "append remaining needed" loop): walk `self.commission_lines`, and for each row where `state=='Pending' and row.override_rate`, rescale `row.amount` by the ratio `row.override_rate / upstream_rate` where `upstream_rate = pakd_override_map.get(row.component) or template_rate(row.component)`. Round to nearest đồng.
- `set_pakd_commission_line_override` API endpoint writes `override_rate` via `frappe.db.set_value`, then loads the parent PAKD doc and calls `pakd_doc.save(ignore_permissions=False)` — that triggers the validate chain including `_sync_commission_lines` which applies the rescale above. Returns the new amount.

## 9. Render & file changes

| File | Change |
|---|---|
| `dcnet_pakd/doctype/pakd_commission_line/pakd_commission_line.json` | + `Skipped` option in `state`; + `override_rate`, `posted_by_cell`, `skip_reason` fields |
| `dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.json` | hide `commission_lines` (set `hidden=1`); add `commission_pivot_html` HTML field directly above it in the `section_commission` section |
| `dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.js` | + `render_commission_pivot(frm)` (refresh hook); + `_open_cell_popover(frm, line, options)`; + Ctrl+click handler; + JS-side number formatter `vi-VN` |
| `dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.py` | `_sync_commission_lines` respects Skipped + Cancelled (no recreate) + per-line override rescale step |
| `dcnet_pakd/utils/engine.py` | **no change** — engine signature stays; per-line override is applied as a post-engine rescale in `_sync_commission_lines` (see §2) |
| `dcnet_pakd/integrations/accounting.py` | new `post_journal_entry_single(pakd_doc, line, payroll_month)`; reuses `_COMPONENT_ACCOUNT_FIELDS_*` maps |
| `dcnet_pakd/api.py` | 5 new whitelisted endpoints |
| `dcnet_pakd/events.py` | (no change; existing PE+approval hooks still call the bundled-period path) |
| `tests/test_api.py` | **new file** — tests for the 5 endpoints (see §10) |
| `patches/v0_2_0/add_commission_line_skipped_state.py` | new patch; `frappe.reload_doc("dcnet_pakd","doctype","pakd_commission_line", force=True)`; idempotent; called via `patches.txt` |
| `patches.txt` | + `dcnet_pakd.patches.v0_2_0.add_commission_line_skipped_state` |

## 10. Test plan

### Engine + sync unit tests (`tests/test_engine.py` extensions)
1. `test_per_line_override_rescales_amount` — line.amount=1500 at upstream 10%, set line.override_rate=5 → after save, line.amount=750 (ratio rescale)
2. `test_per_line_override_layered_with_pakd_override` — pakd.override[MS]=8%, line.override_rate=5% → after save, line.amount = original × 5/8 (not × 5/10)
3. `test_blank_line_override_falls_through` — line.override_rate=0 → no rescale; line.amount untouched by per-line step
4. `test_sync_skips_skipped_lines` — line in Skipped state; subsequent PAKD save preserves amount + does not append a duplicate Pending row for the same (period, component)
5. `test_sync_skips_cancelled_lines` — same as #4 for Cancelled

### API tests (`tests/test_api.py` new)
6. `test_post_period_creates_bundled_je` — bypass-mode 4-component PAKD, post_pakd_commission_period → 8-leg JE, all 4 lines Posted, posted_by_cell=0
7. `test_post_line_creates_single_je` — single Pending MS cell, bypass mode → post_pakd_commission_line → 2-leg JE, posted_by_cell=1, only this line Posted
8. `test_post_line_sc_in_hrms_mode_refused` — use_hrms=1, SC line → post_pakd_commission_line → frappe.throw (SC cell-post disabled in HRMS mode)
9. `test_skip_requires_reason` — skip with empty reason → ValidationError; skip with <3 char reason → ValidationError
10. `test_skip_transitions_state_and_audits` — Pending → Skipped + reason persisted + add_comment visible on parent PAKD timeline
11. `test_override_rescales_amount` — line.amount=1500 (template 10%), set_pakd_commission_line_override(line, 5.0) → line.amount=750 after save (ratio 5/10)
12. `test_override_clear_restores` — set override to 5%, then to 0/""/None → amount returns to upstream value
13. `test_reopen_deletes_draft_je` — Posted line with draft JE → reopen_pakd_commission_line → state=Pending, JE deleted
14. `test_reopen_refuses_submitted_je` — Posted line with submitted JE → reopen raises frappe.ValidationError directing to manual reversal
15. `test_post_permission_gate` — user with only PAKD Sales Rep role → post endpoint raises PermissionError
16. `test_skip_permission_gate` — user with PAKD Accountant role (no Skip permission) → skip endpoint raises PermissionError

### JS / UI tests (Playwright MCP, dogfood)
17. Pivot renders 4 rows × (N+2) cols (label + N billing periods + total) for Recurring Telecom; bottom totals row present
18. Pivot renders 4 rows × 3 cols for One-off (label + 1 period + total)
19. Pivot renders M rows × 3 cols (M PAKD Items + 1 period + total) for Monthly FTTH Rollup
20. Cell click opens popover with correct status-dependent buttons; primary action present
21. Per-cell post creates 2-leg JE (template MS, 10%); row updates to Posted with `c` superscript on the ✓ marker; column total recomputes without full form reload
22. Period-bundle post creates 8-leg JE (bypass mode) / 6-leg JE + AS (HRMS mode); all 4 cells in the column flip to Posted
23. Override flow: set line override to 5% on MS row (template 10%) → amount halves (1500 → 750); clear override (blank) → restores to 1500
24. Skip flow: set Skipped with reason ≥3 chars → cell shows amber `↷` + strikethrough; column + row totals recompute excluding it; reason visible in popover after re-click
25. Ctrl+click on Pending MS cell (bypass mode) → bypasses popover, creates 2-leg JE directly
26. Mobile @ 390×844: horizontal scroll works, sticky label column stays visible while swiping, no horizontal page overflow (`document.documentElement.scrollWidth > window.innerWidth === false`)
27. Console error count = 0 across all UI flows

## 11. Migration & rollback

- New fields default-blank; no data migration needed for existing rows.
- Existing Posted lines keep `posted_by_cell=0` (correct — they were bundled).
- Rollback path: re-show `commission_lines` field (`hidden=0`) + remove the HTML field. Data not destroyed.

## 12. Open questions deferred to plan

- Exact CSS approach for sticky column (probably plain CSS `position: sticky`; verify Frappe form's `.form-section` doesn't break it).
- Whether to bundle ctrl+click shortcut keypress trigger inside JS Dialog or only on grid cells.
- Format of `frappe.log_activity` entries vs leveraging `frappe.add_comment` (latter shows in form timeline — could be nicer).
- Whether to add `[Mở chi tiết »]` link in popover that opens the raw PAKD Commission Line in a new tab for power users (probably yes; minor).

These can be resolved in the implementation plan (writing-plans).

## Spec self-review (2-phase)

### Phase 1 — surface scan
1. **Placeholders:** None.
2. **Internal consistency:**
   - Permissions in §7 + API gate code in §5 reference same role set (Accounts Manager / PAKD Board / PAKD Accountant) — consistent.
   - Override precedence formula appears once in §2 and is referenced (not duplicated) from §8 — single source of truth.
   - JE shape (§6) calls out both `use_hrms=0` and `use_hrms=1` paths for both period-bundle and per-cell modes — matches the §4 popover note about SC cell-post being refused in HRMS mode.
3. **Scope check:** Focused on one feature. Single plan implementable in 1-2 sessions.

### Phase 2 — copy-paste test (walk each code block as if running it)
1. **Override rescale snippet in §2** — `upstream_rate = pakd_override_map.get(line.component) or template_rate(line.component)`. Verified `pakd.commission_overrides` is a child table; needs to be projected to `{component → override_rate}` dict inside `_sync_commission_lines`. Will note in plan task as a step. Confirmed engine.py's existing pattern is identical (`overrides.get(name)`).
2. **API `post_pakd_commission_period` synthetic PE** — `SimpleNamespace(name="", posting_date=today())` passed into `_post_pakd_commission_lines`. Function uses `pe_doc.posting_date` and `pe_doc.name`. Verified both attrs are read, not method calls — SimpleNamespace works.
3. **API `set_pakd_commission_line_override`** — sequence: `frappe.db.set_value` line.override_rate → `pakd_doc = frappe.get_doc(...)` → `pakd_doc.save()` → fetch line back via `get_value` to return new amount. Validated against existing `_sync_commission_lines` flow.
4. **API `reopen_pakd_commission_line`** — for Cancelled lines, `line.journal_entry` may be `None` (per existing `_cancel_commission_line` which deletes draft JEs). Guard with `if line.journal_entry: ...` before docstatus check.
5. **Patch `add_commission_line_skipped_state.py`** — only needs `frappe.reload_doc` for the new Select option + new Percent/Check/Small Text fields. No SQL ALTER, no data migration; existing rows keep `state='Pending'` and new columns default-blank. Confirmed.
6. **JE remark format** — `f"PAKD commission CELL {component} {payroll_month} | PAKD {pakd_doc.name} | line {line.name}"`. No spaces or quote issues. JE.remark column is Long Text, no length limit concern.
7. **Sticky CSS** — using `position: sticky` with `left: 0`/`right: 0` on first/last `<td>` inside an `<table>` works in all modern browsers. Frappe form's `.form-section` does not impose `overflow:hidden` on its body — verified by inspecting `summary_card` field which uses similar wrapper layout in the same form.

No outstanding ambiguities found. Spec ready for writing-plans.
