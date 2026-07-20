# Task: Asset Polishing v1.1 — Apply Design QA Proposals

## Context

Asset Polishing v1.0 đã ship (commit `ce7f9bf`). Design QA exploratory để lại 10 structural proposals chưa apply (xem `docs/design-qa-proposals/asset-polishing.md`). User đã review và đồng ý apply tất cả. Task này thực hiện 10 polish items + light QA verify, ship v1.1.

## Scope

- Project: `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing` (worktree)
- Branch: `feat/asset-polishing` (continue trên branch hiện tại, không tạo branch mới)
- Bench root: `/home/long/long/frappe-bench-dcnet`
- Site test: `dcnet.localhost`
- Source proposals: `docs/design-qa-proposals/asset-polishing.md` — read this FIRST

### Related files

| File | Purpose | Items affected |
|------|---------|---------------|
| `docs/design-qa-proposals/asset-polishing.md` | Proposals source | Read for spec |
| `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json` | Settings DocType | #1 collapsible threshold section |
| `vn_accounting/vn_accounting/report/s21_dn_so_tscd/` | S21-DN report | #2 header rename |
| `vn_accounting/workspace_sidebar/vn_accounting.json` | Sidebar nav | #3 rename CCDC link |
| `vn_accounting/vn_accounting/doctype/ccdc_item/ccdc_item.js` | CCDC Item client script | #4 add button after submit |
| `vn_accounting/vn_accounting/doctype/ccdc_writeoff/ccdc_writeoff.json` + `.js` | CCDC Writeoff form | #5 remaining_242 read-only on insert |
| `vn_accounting/vn_accounting/doctype/ccdc_allocation_schedule/ccdc_allocation_schedule.json` | List view config | #6 status ratio column (custom field or formatter) |
| `vn_accounting/vn_accounting/doctype/asset_handover/asset_handover.js` | Handover client script | #7 preview button + #9 co_signer threshold highlight |
| `vn_accounting/vn_accounting/doctype/asset_stocktake/asset_stocktake.js` | Stocktake client script | #8 summary row footer |
| `vn_accounting/vn_accounting/print_format/asset_handover_s22_dn/` | Print format | #10 @media print CSS |

## Requirements

10 proposals, grouped by complexity. Items are independent — agent picks order based on dependencies (Settings/sidebar JSON before client scripts).

### #1 — Collapsible threshold section in Settings Permission tab

**Where:** `vn_accounting_settings.json` — group 3 fields (`disposal_threshold`, `handover_threshold`, `min_asset_threshold`) under a Section Break with `collapsible=1` and label "Ngưỡng giá trị".

**Implementation hint:** Use Frappe Section Break field with `collapsible: 1, collapsible_depends_on: 'eval:1'`. Reorder fields so the 3 thresholds sit consecutively under the new section.

### #2 — Rename S21-DN header

**Where:** `vn_accounting/vn_accounting/report/s21_dn_so_tscd/s21_dn_so_tscd.py` — find column with label `"GTKH luỹ kế"` → change to `"KH luỹ kế"`.

### #3 — Rename CCDC sidebar link

**Where:** `vn_accounting/workspace_sidebar/vn_accounting.json` — find item with `link_to: "CCDC Allocation Schedule"`, label "Phân bổ CCDC" → change to `"Lịch phân bổ CCDC"`. Also add to `vi.csv` if not yet translated.

### #4 — CCDC Item link button to Allocation Schedule

**Where:** `vn_accounting/vn_accounting/doctype/ccdc_item/ccdc_item.js`. After submit (`docstatus === 1`), add custom button:
```js
frm.add_custom_button(__('Lịch phân bổ'), () => {
    frappe.set_route('List', 'CCDC Allocation Schedule', { ccdc_item: frm.doc.name });
}, __('Mở'));
```

### #5 — CCDC Writeoff: read-only remaining_242 preview before submit

**Where:** `ccdc_writeoff.json` — set `remaining_242_amount` and `remaining_153_amount` `read_only: 1` (already likely so) BUT also add `in_preview: 1` or set up `js` `refresh()` hook to auto-fetch when `ccdc_item` changes via `@frappe.whitelist()` server method `get_writeoff_preview(ccdc_item)`. Show value in form before user clicks Submit.

**Implementation hint:** Add server method:
```python
@frappe.whitelist()
def get_writeoff_preview(ccdc_item):
    item = frappe.get_doc("CCDC Item", ccdc_item)
    # sum unposted allocation entries
    remaining_242 = ...
    remaining_153 = ...
    return {"remaining_242_amount": remaining_242, "remaining_153_amount": remaining_153}
```
Client script: on `ccdc_item` change → call method → set form values.

### #6 — Allocation Schedule list view: posted/pending ratio column

**Where:** `ccdc_allocation_schedule.json` — add a virtual field or use list_view_settings:
```python
# ccdc_allocation_schedule.py
@frappe.whitelist()
def get_progress(name):
    posted = frappe.db.count("CCDC Allocation Entry", {"parent": name, "status": "Posted"})
    total = frappe.db.count("CCDC Allocation Entry", {"parent": name})
    return f"{posted}/{total}"
```
Add field `progress_text: Data, read_only=1, in_list_view=1`, populated in `before_save()` or computed on `validate()`.

### #7 — Asset Handover: "Xem biên bản" preview button

**Where:** `asset_handover.js`. After submit, add button (next to existing print):
```js
frm.add_custom_button(__('Xem biên bản'), () => {
    frappe.utils.print(
        frm.doctype, frm.docname,
        frappe.get_meta(frm.doctype).default_print_format || 'Standard',
        frm.doc.letter_head
    );
}, __('In'));
```

### #8 — Asset Stocktake: summary row footer

**Where:** `asset_stocktake.js`. Compute counts in `refresh()` after items loaded. Inject HTML below `stocktake_items` table:
```js
function render_summary_row(frm) {
    const counts = { 'Còn nguyên': 0, 'Hỏng': 0, 'Mất': 0 };
    (frm.doc.stocktake_items || []).forEach(it => {
        if (counts[it.physical_status] !== undefined) counts[it.physical_status]++;
    });
    const summary_html = `<div style="margin-top:8px; padding:8px; background:#f5f5f5; border-radius:4px;">
        <strong>Tổng kết:</strong>
        Còn nguyên: ${counts['Còn nguyên']} ·
        Hỏng: ${counts['Hỏng']} ·
        Mất: ${counts['Mất']}
    </div>`;
    frm.fields_dict.stocktake_items.$wrapper.find('.stocktake-summary').remove();
    frm.fields_dict.stocktake_items.$wrapper.append(`<div class="stocktake-summary">${summary_html}</div>`);
}
// Call from refresh + on stocktake_items.physical_status change
```

### #9 — Asset Handover: co_signer threshold warning

**Where:** `asset_handover.js`. When `total_asset_value >= 80% of handover_threshold` from Settings (call server to fetch threshold), highlight `co_signer_employee` field with yellow background:
```js
frm.fields_dict.co_signer_employee.$wrapper.find('.control-input').css('background-color', '#fff8dc');
```
Add tooltip: "Sắp đạt ngưỡng yêu cầu KTT đồng ký".

### #10 — Print S22-DN: @media print CSS for page break

**Where:** `vn_accounting/vn_accounting/print_format/asset_handover_s22_dn/asset_handover_s22_dn.json` — find `html` field. Add at top of template:
```html
<style>
@media print {
    table.handover-items thead { display: table-header-group; }
    table.handover-items tbody tr { page-break-inside: avoid; }
    table.handover-items tfoot { display: table-footer-group; }
    .signature-block { page-break-inside: avoid; }
}
</style>
```
This keeps table headers repeating + prevents row split mid-page.

### Final QA + Commit

After all 10 items implemented:
1. **Bench cycle**: `cd /home/long/long/frappe-bench-dcnet && git -C apps/vn_accounting checkout --detach feat/asset-polishing && bench --site dcnet.localhost migrate && bench build --app vn_accounting && bench --site dcnet.localhost clear-cache`
2. **Browser smoke test (Playwright MCP, screenshots to `qa-screenshots/v1.1-polish/`)**:
   - Settings → verify "Ngưỡng giá trị" section collapsible
   - Sidebar → verify "Lịch phân bổ CCDC" label
   - Open submitted CCDC Item → verify "Lịch phân bổ" button works
   - Open CCDC Writeoff new form → select existing CCDC Item → verify remaining_242 auto-fills
   - Open Allocation Schedule list → verify progress column shows "X/Y"
   - Open submitted Asset Handover → verify "Xem biên bản" button + co_signer highlight when total ≥ 80% threshold
   - Open Asset Stocktake → verify summary row at bottom
   - Print Asset Handover S22-DN preview → verify table doesn't split mid-page
3. **Update proposals file**: in `docs/design-qa-proposals/asset-polishing.md`, mark each of 10 items as `✅ Applied YYYY-MM-DD` next to the proposal text.
4. **Bump version**: update `vn_accounting/__init__.py` `__version__` to next minor (e.g. 1.0.0 → 1.1.0)
5. **Final commit**: `feat(asset-polishing): v1.1 design polish — apply 10 design-QA proposals`

## Acceptance Criteria

- [ ] Settings DocType JSON has Section Break before `disposal_threshold` with `collapsible=1` and label "Ngưỡng giá trị" (verify via grep on JSON)
- [ ] S21-DN report column "GTKH luỹ kế" no longer present; "KH luỹ kế" exists (grep on report .py)
- [ ] Sidebar JSON has CCDC link with label "Lịch phân bổ CCDC" (grep)
- [ ] CCDC Item form (submitted) has button "Lịch phân bổ" in toolbar (Playwright snapshot to `qa-screenshots/v1.1-polish/ccdc-item-button.png`)
- [ ] CCDC Writeoff form: setting `ccdc_item` populates `remaining_242_amount` (Playwright: select an existing item, screenshot showing field value)
- [ ] Allocation Schedule list view shows progress column "X/Y" format (Playwright snapshot)
- [ ] Asset Handover (submitted) toolbar has "Xem biên bản" button (Playwright snapshot)
- [ ] Asset Handover with total ≥ 80% threshold: co_signer field has yellow background style (Playwright DOM check via `browser_evaluate`)
- [ ] Asset Stocktake form shows summary row "Còn nguyên: X · Hỏng: Y · Mất: Z" below items table (Playwright snapshot)
- [ ] Asset Handover S22-DN print preview: table headers repeat and rows don't split (visual inspection in Playwright print preview)
- [ ] All 10 items marked `✅ Applied 2026-04-29` in `docs/design-qa-proposals/asset-polishing.md`
- [ ] `__version__` in `vn_accounting/__init__.py` bumped to 1.1.0 (grep)
- [ ] Final commit message references "v1.1 design polish"
- [ ] `bench --site dcnet.localhost migrate` succeeds with 0 errors after all changes
- [ ] `bench build --app vn_accounting` succeeds with 0 errors

## Constraints

- Do NOT modify ERPNext core files
- Do NOT introduce new DocTypes — these are all polish items on existing DocTypes
- Do NOT change permission rules (avoid permission_matrix sync)
- All client script changes follow existing pattern in the file (don't restructure)
- Print format JSON: only modify `html` field; don't touch `name` or `doc_type`
- All Vietnamese labels: use exact diacritics, follow existing vi.csv convention
- File size: keep changes incremental; don't refactor unrelated parts

## Verification Commands

test -f docs/design-qa-proposals/asset-polishing.md
grep -q "Ngưỡng giá trị" vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json
grep -q '"collapsible": 1' vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json
grep -q "KH luỹ kế" vn_accounting/vn_accounting/report/s21_dn_so_tscd/s21_dn_so_tscd.py
grep -qv "GTKH luỹ kế" vn_accounting/vn_accounting/report/s21_dn_so_tscd/s21_dn_so_tscd.py
grep -q "Lịch phân bổ CCDC" vn_accounting/workspace_sidebar/vn_accounting.json
grep -q "Lịch phân bổ" vn_accounting/vn_accounting/doctype/ccdc_item/ccdc_item.js
grep -q "get_writeoff_preview" vn_accounting/vn_accounting/doctype/ccdc_writeoff/ccdc_writeoff.py
grep -qE "progress|posted_ratio" vn_accounting/vn_accounting/doctype/ccdc_allocation_schedule/ccdc_allocation_schedule.py
grep -q "Xem biên bản" vn_accounting/vn_accounting/doctype/asset_handover/asset_handover.js
grep -qE "co_signer_employee.*background|fff8dc" vn_accounting/vn_accounting/doctype/asset_handover/asset_handover.js
grep -qE "stocktake-summary|render_summary_row" vn_accounting/vn_accounting/doctype/asset_stocktake/asset_stocktake.js
grep -q "@media print" vn_accounting/vn_accounting/print_format/asset_handover_s22_dn/asset_handover_s22_dn.json
grep -qE 'Applied 2026-04-29' docs/design-qa-proposals/asset-polishing.md
sh -c 'count=$(grep -cE "Applied 2026-04-29" docs/design-qa-proposals/asset-polishing.md); test "$count" -ge 10'
grep -qE '__version__\s*=\s*"1\.1\.' vn_accounting/__init__.py
test -d qa-screenshots/v1.1-polish
sh -c 'count=$(find qa-screenshots/v1.1-polish -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 6'
git log --oneline feat/asset-polishing -1 | grep -q "v1.1 design polish"

## Live Testing Procedure

### Setup
1. cwd = `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing`
2. After ANY DocType JSON change: `cd /home/long/long/frappe-bench-dcnet && git -C apps/vn_accounting checkout --detach feat/asset-polishing && bench --site dcnet.localhost migrate`
3. After client script (.js) change: `bench build --app vn_accounting`
4. After any change: `bench --site dcnet.localhost clear-cache`

### Browser QA via Playwright MCP
1. `mcp__plugin_playwright_playwright__browser_navigate` to `http://dcnet.localhost:8001/app/<route>`
2. Test each item in golden path: open form → trigger interaction → screenshot to `qa-screenshots/v1.1-polish/<item>.png`
3. Check console: `mcp__plugin_playwright_playwright__browser_console_messages`
4. For DOM style check (#9 yellow highlight): use `browser_evaluate` with JS `getComputedStyle(...)`

### Worktree dance
Per `git-deploy.md` memory: always commit IN worktree first, THEN `git -C apps/vn_accounting checkout --detach feat/asset-polishing` to sync apps/. Stale apps/ checkout returns OLD code from disk even after server-side cache clear.

## Agent Persona

You are a senior Frappe/ERPNext developer doing UI/UX polish. You know:

- Frappe v16 client script patterns (`frm.add_custom_button`, `refresh()`, `setup()`, value cache fetch)
- DocType JSON conventions (Section Break collapsible, depends_on, in_list_view)
- Frappe `print_format.json` html field + `@media print` CSS
- ERPNext list view custom column patterns (in_list_view + computed field)
- Worktree dance per `git-deploy.md`

You always:
- Read `docs/design-qa-proposals/asset-polishing.md` FIRST
- Apply 10 items in order: JSON edits first (#1, #2, #3) → client scripts (#4-9) → print CSS (#10) → final QA + commit
- Commit each item atomically (10 small commits is OK; group related items if natural)
- Verify each item visually via Playwright before claiming complete
- Use existing patterns from the file (don't restructure)

You NEVER:
- Add new DocTypes
- Change permissions
- Modify ERPNext core
- Skip the worktree dance after JSON changes

## Model

auto

## Time Budget

- Max hours: 4
- Max sessions: 6
- Per-session minutes: 30
