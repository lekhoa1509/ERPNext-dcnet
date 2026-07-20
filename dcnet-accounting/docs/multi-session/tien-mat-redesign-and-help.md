# Task: "Tiền mặt" Sidebar Redesign + Native Frappe Help Page

## Context

The vn_accounting workspace section "Quỹ tiền mặt" (Cash Fund) has accumulated structural issues during incremental development: report items mixed with creation entries, missing docstatus filters on submittable DocTypes, an item ("Tạo bút toán tiền mặt") that opens a list view with stale localStorage filter instead of a new form, a duplicate "Dự báo dòng tiền" entry in two sections, and item labels that don't match Vietnamese accounting conventions (TT133/TT200/TT99).

A 102-item ANSD sidebar QA (results in `/home/long/long/dev-process/projects/vn-accounting-sidebar-qa/`) confirmed 10 UI bugs, several inside this section. The user has decided to redesign the section using Misa AMIS Kế Toán's Phân hệ Tiền mặt structure as inspiration: replace report-based items with creation entries (chứng từ), keep the section to actions + tools only, defer all reports to a future "Báo cáo tiền mặt" section. Additionally, build a native Frappe help page that mirrors Misa's helpact.misa.vn pattern — same Desk shell, native frappe-ui CSS, with one help article per sidebar feature.

Important Vietnamese accounting context: ERPNext's `Payment Entry` is **narrower** than VN "Phiếu thu/chi" — Payment Entry only handles invoice settlements, while VN Phiếu thu/chi covers ANY transaction touching account 111 (advance, settlement, internal transfer, payroll, tax, BHXH, etc.). The correct technical mechanism is `Journal Entry` with `voucher_type="Cash Entry"` and prefix-distinguished naming series (PT- for Phiếu thu, PC- for Phiếu chi).

## Scope

- Project: `/home/long/long/frappe-bench-dcnet/apps/vn_accounting`
- Bench root (for `bench` commands — `cd` from project): `/home/long/long/frappe-bench-dcnet`
- Branch: **`feat/tien-mat-redesign-and-help`** (already created from `main`, currently checked out)
- Site: `dcnet.localhost` on `http://dcnet.localhost:8001`
- Files to edit:
  - `vn_accounting/workspace_sidebar/vn_accounting.json` (1528 lines — only "Tiền mặt" section @ lines 19-138 + duplicate "Dự báo dòng tiền" @ line 89-99)
  - `vn_accounting/translations/vi.csv` (535 rows, 3-col: source,translated,context)
  - `vn_accounting/hooks.py` (add new bundle to `app_include_js`)
  - `vn_accounting/patches.txt` (append new patch entry)
- Files to create:
  - `vn_accounting/patches/v1_4_0/__init__.py`
  - `vn_accounting/patches/v1_4_0/add_je_naming_series_pt_pc.py` (Property Setter patch)
  - `vn_accounting/public/js/phieu_chi_subtype_dialog.bundle.js`
  - `vn_accounting/page/__init__.py`
  - `vn_accounting/page/vn_help/__init__.py`
  - `vn_accounting/page/vn_help/vn_help.json` (Frappe Page metadata)
  - `vn_accounting/page/vn_help/vn_help.py` (server-side stub)
  - `vn_accounting/page/vn_help/vn_help.js` (Page bundle — render layout + nav + content)
  - `vn_accounting/page/vn_help/vn_help.css` (component-scoped styles using frappe-ui CSS vars)
  - `vn_accounting/api/__init__.py` (if not exists)
  - `vn_accounting/api/help.py` (whitelisted `get_article(slug)` endpoint)
  - `vn_accounting/help/_index.json` (nav structure: array of {section, slug, title, summary})
  - `vn_accounting/help/tien-mat/index.md` (section overview)
  - `vn_accounting/help/tien-mat/phieu-thu.md`
  - `vn_accounting/help/tien-mat/phieu-chi.md`
  - `vn_accounting/help/tien-mat/rut-nop-tien.md`
  - `vn_accounting/help/tien-mat/kiem-ke-quy.md`
  - `vn_accounting/help/tien-mat/so-quy-chi-nhanh.md`
  - `vn_accounting/help/tien-mat/_images/<slug>-N.png` (screenshots, ≥1 per article)
  - `vn_accounting/tests/test_tien_mat_sidebar.py` (assert sidebar fixture state after redesign)
  - `docs/design-qa-proposals/tien-mat-redesign-verification.md` (final verification report)
  - `docs/design-qa-proposals/tien-mat-screenshots/*.png` (before/after sidebar + each new form + help page)
- Files to read (do NOT edit):
  - `vn_accounting/install.py` — `_sync_workspace_sidebar()` re-syncs JSON → DB after migrate
  - `docs/multi-session/kho-sidebar-fixes.md` — reference precedent for quality bar (5 commits, tests + screenshots + verification report)
  - `vn_accounting/tests/test_kho_sidebar.py` — template for new sidebar test
  - `/home/long/long/dev-process/projects/vn-accounting-sidebar-qa/findings-aggregate.json` — original QA findings for cross-ref

### Current "Quỹ tiền mặt" section (line 19-138 in fixture)

| Line | Label | link_type | link_to | route_options | Action |
|---|---|---|---|---|---|
| 28 | "Quỹ tiền mặt" (Section Break) | — | — | — | RENAME → "Tiền mặt" |
| 41 | "Thu tiền mặt" | Report | Cash Receipts | — | **REMOVE** (defer to future Báo cáo tiền mặt section) |
| 54 | "Chi tiền mặt" | Report | Cash Payments | — | **REMOVE** (defer) |
| 67 | "Sổ quỹ tiền mặt" | Report | Cash Book | — | **REMOVE** (defer) |
| 80 | "Kiểm kê quỹ" | DocType | Cash Count | — | KEEP (label as-is) |
| 93 | "Dự báo dòng tiền" | Page | cash-flow-forecast | — | **REMOVE** (duplicate; instance @ line 262 in Ngân hàng section is canonical) |
| 106 | "Phiếu quỹ chi nhánh" | DocType | Branch Cash Entry | null | KEEP + ADD docstatus=1 filter |
| 119 | "Sổ quỹ chi nhánh" | Report | So Noi Bo | — | KEEP (rename Report internal name in a future task — out of scope here) |
| 132 | "Tạo bút toán tiền mặt" | DocType | Journal Entry | — | **REMOVE** (replaced by 3 new URL items below) |

### Target "Tiền mặt" section (after redesign — 7 items)

**CRITICAL — Sidebar context preservation.** Frappe v16 auto-switches the sidebar when the user navigates to a DocType that the current workspace's sidebar does NOT contain (per `frappe-v16-ui.md` "Sidebar Persistence — Frappe Native Has TWO Modes, Not One"). Items 1-3 below all navigate to `Journal Entry` which is owned by ERPNext's "Accounts" workspace, NOT by VN Accounting. Without intervention, clicking these will teleport the user to the Accounts sidebar — losing context, breaking the task flow.

**Mitigation: append `&sidebar=VN%20Accounting` to every URL.** Frappe core has the extension hook `frappe.route_options.sidebar` (sidebar.js:302) which forces the named sidebar on the next navigation. URL slightly polluted but cross-browser stable, no monkey-patch needed. The exact value MUST match the Workspace Sidebar `name` field (verified at top of `vn_accounting/workspace_sidebar/vn_accounting.json` — `"name": "VN Accounting"` → URL-encoded as `VN%20Accounting`).

| # | Label | link_type | URL or link_to | route_options |
|---|---|---|---|---|
| 1 | "+ Phiếu thu" | URL | `/app/journal-entry/new?voucher_type=Cash%20Entry&naming_series=PT-.YYYY.-&sidebar=VN%20Accounting` | — |
| 2 | "+ Phiếu chi" | URL | `/app/journal-entry/new?voucher_type=Cash%20Entry&naming_series=PC-.YYYY.-&sidebar=VN%20Accounting` | — |
| 3 | "+ Rút/nộp tiền" | URL | `/app/journal-entry/new?voucher_type=Contra%20Entry&sidebar=VN%20Accounting` | — |
| 4 | "Kiểm kê quỹ" | DocType | Cash Count | `null` (custom DocType — already in VN Accounting sidebar via this same item; no `sidebar=` needed for DocType-type items) |
| 5 | "+ Tạo biên bản kiểm kê" | URL | `/app/cash-count/new?sidebar=VN%20Accounting` | — |
| 6 | "Phiếu quỹ chi nhánh" | DocType | Branch Cash Entry | `{"docstatus":["=",1]}` (Branch Cash Entry IS submittable; custom DocType — already in VN Accounting sidebar) |
| 7 | "Sổ quỹ chi nhánh" | Report | So Noi Bo | — |

For items 4, 6, 7 the DocType/Report is custom-owned by vn_accounting and already referenced in the VN Accounting sidebar fixture — Frappe Mode 2 ("same-tab navigation") preserves the sidebar in-memory across `frappe.set_route()`, so no URL param needed. The risk is only for cross-workspace-owned targets (Journal Entry → Accounts).

## Requirements

### Phase 1 — Sidebar JSON restructure

**Use `python3` + `json` module to load/edit/write the fixture.** Do NOT hand-edit raw JSON to avoid escaping bugs with Vietnamese diacritics. Preserve `ensure_ascii=False` if existing fixture uses Unicode escapes — verify by diffing one untouched section before/after.

1. Rename Section Break label `"Quỹ tiền mặt"` → `"Tiền mặt"` (line 28 in `items[]`).
2. Remove items by label match:
   - `"Thu tiền mặt"`, `"Chi tiền mặt"`, `"Sổ quỹ tiền mặt"`, `"Tạo bút toán tiền mặt"`
   - First occurrence of `"Dự báo dòng tiền"` (the one inside "Tiền mặt"/"Quỹ tiền mặt" section, NOT the one inside "Ngân hàng" section). Identify by index range — between Section Break "Tiền mặt" and next Section Break "Ngân hàng".
3. Add 4 new items inside the section (positions per target table above):
   - "+ Phiếu thu" — `link_type: "URL"`, `url: "/app/journal-entry/new?voucher_type=Cash%20Entry&naming_series=PT-.YYYY.-"`, `link_to: ""`
   - "+ Phiếu chi" — same shape, `naming_series=PC-.YYYY.-`
   - "+ Rút/nộp tiền" — `link_type: "URL"`, `url: "/app/journal-entry/new?voucher_type=Contra%20Entry"`
   - "+ Tạo biên bản kiểm kê" — `link_type: "URL"`, `url: "/app/cash-count/new"`
4. Update existing item "Phiếu quỹ chi nhánh": set `route_options` to JSON string `"{\"docstatus\":[\"=\",1]}"` (Frappe stores filter as JSON string inside this field — verify `json.loads(items[N]["route_options"])` returns dict after write).
5. Bump the top-level `"modified"` timestamp to current ISO datetime so Frappe re-imports on next migrate.

Each new item dict must include the same fields as existing items (`child`, `collapsible`, `icon`, `indent`, `keep_closed`, `label`, `link_to`, `link_type`, `show_arrow`, `type`, `url`) to avoid Frappe schema validation errors. Use an existing item as template, override fields. For URL-type items, `link_to` should be `""` and `url` carries the path.

### Phase 2 — Naming series Property Setter patch

ERPNext default Journal Entry `naming_series` options is just `ACC-JV-.YYYY.-`. Add `PT-.YYYY.-` and `PC-.YYYY.-` so the URL pre-fill resolves to a valid option.

Create `vn_accounting/patches/v1_4_0/__init__.py` (empty) and `vn_accounting/patches/v1_4_0/add_je_naming_series_pt_pc.py`:

```python
import frappe

def execute():
    name = "Journal Entry-naming_series-options"
    desired = "PT-.YYYY.-\nPC-.YYYY.-\nACC-JV-.YYYY.-"
    if frappe.db.exists("Property Setter", name):
        existing = frappe.db.get_value("Property Setter", name, "value") or ""
        if "PT-.YYYY.-" in existing and "PC-.YYYY.-" in existing:
            return
        # extend existing options preserving any user customization
        new_value = "PT-.YYYY.-\nPC-.YYYY.-\n" + existing.lstrip("\n")
        frappe.db.set_value("Property Setter", name, "value", new_value)
        return
    frappe.get_doc({
        "doctype": "Property Setter",
        "name": name,
        "doc_type": "Journal Entry",
        "field_name": "naming_series",
        "property": "options",
        "property_type": "Text",
        "value": desired,
        "doctype_or_field": "DocField",
    }).insert(ignore_permissions=True)
```

Append to `vn_accounting/patches.txt`:
```
vn_accounting.patches.v1_4_0.add_je_naming_series_pt_pc
```

### Phase 3 — Phiếu chi sub-type dialog (JS bundle)

Create `vn_accounting/public/js/phieu_chi_subtype_dialog.bundle.js`. The bundle attaches to Journal Entry form and shows a sub-type picker dialog when:
- `frappe.route_options.naming_series === "PC-.YYYY.-"` OR URL query has `naming_series=PC-.YYYY.-`
- AND form is brand new (`frm.is_new() === true`)
- AND `accounts` child table is empty

Sub-types and credit account mapping:

| Sub-type label | TK Nợ pre-fill (from Cash 1111) | TK Có pre-fill |
|---|---|---|
| "Trả NCC" | (user picks at row) | 331 |
| "Nộp thuế" | — | 3331 |
| "Đóng BHXH" | — | 338 |
| "Trả lương" | — | 334 |
| "Tạm ứng nhân viên" | — | 141 |
| "Khác" | — | (user picks freely) |

Logic flow:
1. Open `frappe.prompt` with field `subtype` (Select with the 6 options above + "Khác").
2. After user picks (not "Khác"):
   - Resolve company default cash account (TK 1111 prefix) via `frappe.db.get_value("Company", frm.doc.company || frappe.defaults.get_default("company"), "default_cash_account")`. Fallback: list of accounts with `account_number` starting with "1111" filtered by company → pick first.
   - Resolve TK đối ứng account name by querying `tabAccount` filtered by `account_number = <prefix>` AND `company = <current>`. If multiple, pick the first leaf account.
   - Add 2 rows to `frm.doc.accounts`: row1 `account = <TK đối ứng>`, `debit_in_account_currency = 0` (user fills); row2 `account = <cash account>`, `credit_in_account_currency = 0`. Use `frm.add_child("accounts", {...})` then `frm.refresh_field("accounts")`.
3. If user picks "Khác": skip autofill, just show the empty form.
4. Set `frm.doc.user_remark = "Phiếu chi: <subtype>"` for traceability.
5. Wrap entire logic in feature flag check — only run if URL has `naming_series=PC-.YYYY.-`.

Add bundle to `hooks.py`:
```python
app_include_js = [
    # ... existing entries
    "phieu_chi_subtype_dialog.bundle.js",
]
```

### Phase 4 — Frappe Page `vn-help` scaffold

Create directory tree:
```
vn_accounting/page/__init__.py        (empty)
vn_accounting/page/vn_help/__init__.py (empty)
vn_accounting/page/vn_help/vn_help.json
vn_accounting/page/vn_help/vn_help.py
vn_accounting/page/vn_help/vn_help.js
vn_accounting/page/vn_help/vn_help.css
```

`vn_help.json` (Page DocType fixture — use existing Frappe Page as template, e.g., `cash-flow-forecast` if available, otherwise minimal):
```json
{
 "doctype": "Page",
 "name": "vn-help",
 "title": "Trợ giúp VN Accounting",
 "module": "VN Accounting",
 "page_name": "vn-help",
 "standard": "Yes",
 "system_page": 0
}
```

`vn_help.py` (server-side hook stub):
```python
import frappe
@frappe.whitelist()
def get_index():
    """Return help index from disk, cached."""
    return frappe.cache.hget("vn_help_index", "all", lambda: _load_index())

def _load_index():
    import json, os
    path = os.path.join(frappe.get_app_path("vn_accounting"), "help", "_index.json")
    with open(path, "r") as f:
        return json.load(f)
```

`vn_help.js` — Page bundle. Use Frappe page wrapper API (`frappe.pages['vn-help'].on_page_load = function(wrapper) { ... }`). Render layout:
- Use `frappe.ui.make_app_page({parent: wrapper, title: "Trợ giúp VN Accounting", single_column: false})`
- Left column: nav rendered from `_index.json` (sections + collapsible articles). Click → render right column.
- Right column: article body. On load, parse `window.location.hash` (`#tien-mat/phieu-thu` form), call API `vn_accounting.api.help.get_article` with slug, render returned `body_html` into right pane.
- Listen to `hashchange` event; reload article when hash changes.

`vn_help.css` — minimal scoped styles using Frappe CSS variables (`var(--text-color)`, `var(--bg-color)`, `var(--border-color)`, etc.) so dark mode auto-matches:
- 2-pane flex layout, left 280px fixed, right `flex: 1`
- Section headers: bold, `var(--text-muted)`
- Article links: `padding: 8px 12px; border-radius: 6px; hover: background var(--bg-light-gray)`
- Active link: `background var(--primary-color)10`, `color var(--primary-color)`
- Article content: max-width 720px, line-height 1.7, headings via Frappe defaults

### Phase 5 — Whitelisted API endpoint

Create `vn_accounting/api/__init__.py` (empty if not exists) and `vn_accounting/api/help.py`:

```python
import frappe
import os
import json

@frappe.whitelist()
def get_article(slug: str) -> dict:
    """Read help article markdown from disk, render to HTML, return dict."""
    if not slug or "/" in slug.replace("/", "", 1) and slug.count("/") > 1:
        # allow exactly one "/" for section/article form
        frappe.throw("Invalid slug")
    safe_slug = slug.replace("..", "").strip("/")
    parts = safe_slug.split("/", 1)
    if len(parts) != 2:
        frappe.throw("Slug must be in 'section/article' form")
    section, article = parts
    base = os.path.join(frappe.get_app_path("vn_accounting"), "help", section)
    md_path = os.path.join(base, f"{article}.md")
    if not os.path.exists(md_path):
        frappe.throw(f"Article not found: {slug}")
    with open(md_path, "r", encoding="utf-8") as f:
        body_md = f.read()
    body_html = frappe.utils.markdown(body_md)
    title = body_md.split("\n", 1)[0].lstrip("# ").strip() if body_md.startswith("# ") else article
    return {
        "slug": slug,
        "section": section,
        "title": title,
        "body_html": body_html,
        "body_md": body_md,
    }

@frappe.whitelist()
def get_index() -> list:
    """Return help nav index from _index.json on disk."""
    path = os.path.join(frappe.get_app_path("vn_accounting"), "help", "_index.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
```

`_index.json` schema:
```json
[
  {
    "section": "tien-mat",
    "section_label": "Tiền mặt",
    "articles": [
      {"slug": "tien-mat/index", "title": "Tổng quan Tiền mặt", "summary": "..."},
      {"slug": "tien-mat/phieu-thu", "title": "Phiếu thu", "summary": "..."},
      ...
    ]
  }
]
```

### Phase 6 — Markdown content (6 articles for "Tiền mặt")

Each markdown file follows this schema (Vietnamese content, English code/identifiers):

```markdown
# <Article Title>

## Mục đích
<1-2 sentences: who is this for, what problem it solves>

## Khi nào dùng
<bullet list of triggering scenarios>

## Cách thực hiện
<numbered steps with screenshot references>

1. Bước 1...
   ![Screenshot of step 1](_images/<slug>-1.png)
2. Bước 2...

## Định khoản tự động
<table of TK Nợ / TK Có / Diễn giải>

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|

## Edge cases & cảnh báo
<bullet list>

## Báo cáo liên quan
<links to relevant reports — in vn_accounting workspace>

## FAQ
**Q:** ...
**A:** ...
```

Articles to write:
1. **`tien-mat/index.md`** — Section overview. Reference Misa Phân hệ Tiền mặt 4-group structure. List 7 sidebar items with 1-line descriptions. Include workflow narrative: "Khi có nghiệp vụ thu/chi tiền mặt → tạo Phiếu thu hoặc Phiếu chi → định khoản → ghi sổ → cuối ngày/tuần kiểm kê quỹ → định kỳ xem sổ quỹ chi nhánh nếu có". Cross-link to Báo cáo tiền mặt (note: future feature, mark as `[Sắp có]`).

2. **`tien-mat/phieu-thu.md`** — Mục đích: ghi nhận tiền vào quỹ tiền mặt cho mọi nguồn (KH thanh toán, hoàn tạm ứng, lãi NH chuyển vào quỹ, etc.). Cách thực hiện: click "+ Phiếu thu" → form mở với naming_series=PT-, voucher_type=Cash Entry; định khoản 2 dòng tối thiểu (TK 1111 Nợ, TK đối ứng Có); user_remark mô tả nội dung. Định khoản: Nợ 111 / Có 131 (KH), Có 141 (hoàn tạm ứng), Có 511 (doanh thu trực tiếp tiền mặt — hiếm), Có 711 (thu khác). Edge case: tỷ giá ngoại tệ, thu thuế GTGT.

3. **`tien-mat/phieu-chi.md`** — Mục đích: ghi nhận tiền ra khỏi quỹ tiền mặt. Cách thực hiện: click "+ Phiếu chi" → dialog hỏi sub-type (Trả NCC/Nộp thuế/Đóng BHXH/Trả lương/Tạm ứng/Khác) → form auto-fill TK đối ứng → user nhập amount + remark. Document the dialog with screenshot. Định khoản: Nợ 331 / Có 111 (trả NCC), Nợ 3331 / Có 111 (nộp thuế), Nợ 338 / Có 111 (BHXH), Nợ 334 / Có 111 (lương), Nợ 141 / Có 111 (tạm ứng).

4. **`tien-mat/rut-nop-tien.md`** — Mục đích: chuyển tiền giữa quỹ tiền mặt và tài khoản ngân hàng. voucher_type=Contra Entry. Định khoản: Nợ 111 / Có 112 (rút từ NH về quỹ); Nợ 112 / Có 111 (nộp từ quỹ vào NH).

5. **`tien-mat/kiem-ke-quy.md`** — Mục đích: biên bản kiểm kê thực tế quỹ tiền mặt định kỳ (cuối tháng/quý/năm). DocType `Cash Count` (NOT submittable — chỉ là biên bản, không tạo bút toán). Cách thực hiện: click "+ Tạo biên bản kiểm kê" → form Cash Count → nhập số dư thực tế theo mệnh giá → so sánh với sổ sách → ghi chú chênh lệch nếu có.

6. **`tien-mat/so-quy-chi-nhanh.md`** — Mục đích: sổ quỹ tiền mặt theo từng chi nhánh (cho doanh nghiệp đa chi nhánh). DocType `Branch Cash Entry` cho phiếu, Report `So Noi Bo` cho sổ tổng hợp. Cách thực hiện: tạo Phiếu quỹ chi nhánh → ghi sổ → xem Sổ quỹ chi nhánh. Edge case: chuyển tiền giữa chi nhánh và quỹ tổng (TK 111-NB ↔ TK 111-CN).

Screenshot ≥1 per article in `vn_accounting/help/_images/<slug>-N.png`. Capture via Playwright MCP during Phase 8 verification — see Live Testing Procedure.

### Phase 7 — Sidebar test file

Create `vn_accounting/tests/test_tien_mat_sidebar.py` mirroring `test_kho_sidebar.py` patterns:

- Setup: load JSON fixture, find "Tiền mặt" Section Break index, slice items between this and the next Section Break.
- `test_section_label_renamed`: assert section label is exactly "Tiền mặt" (not "Quỹ tiền mặt").
- `test_section_has_7_items`: assert `len(section_items) == 7`.
- `test_phieu_thu_url_correct`: assert item with label "+ Phiếu thu" exists, has `link_type=URL`, `url` contains `voucher_type=Cash%20Entry` and `naming_series=PT-.YYYY.-`.
- `test_phieu_chi_url_correct`: same pattern with `naming_series=PC-.YYYY.-`.
- `test_rut_nop_tien_url_correct`: same with `voucher_type=Contra%20Entry`.
- `test_kiem_ke_create_url_correct`: assert "+ Tạo biên bản kiểm kê" URL is `/app/cash-count/new`.
- `test_branch_cash_entry_has_docstatus_filter`: assert "Phiếu quỹ chi nhánh" `route_options` parses to `{"docstatus": ["=", 1]}`.
- `test_no_removed_items`: assert labels "Thu tiền mặt", "Chi tiền mặt", "Sổ quỹ tiền mặt", "Tạo bút toán tiền mặt" are NOT present in section.
- `test_no_duplicate_du_bao`: assert "Dự báo dòng tiền" appears at most ONCE in entire fixture (the Ngân hàng instance is canonical).

Use `unittest.TestCase` like the kho precedent. No frappe imports needed (load JSON directly). Run with: `cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting && python3 -m unittest vn_accounting.tests.test_tien_mat_sidebar -v`.

### Phase 8 — Live verification + Design QA

After implementation, run the bench operations (in Live Testing Procedure below) and:
- Walk every new sidebar item via Playwright MCP, screenshot to `docs/design-qa-proposals/tien-mat-screenshots/sidebar-<N>-<slug>.png`
- Open `/app/vn-help#tien-mat/index`, navigate through 6 articles, screenshot each to same dir
- Capture console errors per navigation; expected count = 0
- Take "before" screenshot from a separate browser session OR from git stash — IF infeasible, document the redesigned state only and reference the QA report `findings-aggregate.json` for what the section looked like before
- Apply Design QA exploratory pass on the new section + help page. Cosmetic fixes (spacing, label wording, missing tooltip) → fix autonomously and append fix list to verification report. Structural proposals (workflow changes, new fields, etc.) → log to `docs/design-qa-proposals/tien-mat-redesign-and-help.md` with `## Session YYYY-MM-DD HH:MM` header.

### Phase 9 — Verification report + final commit

Write `docs/design-qa-proposals/tien-mat-redesign-verification.md` covering:
1. **Summary** — what shipped (1 paragraph)
2. **Per-fix table** — original problem | fix applied | verification evidence (screenshot or grep)
3. **Sidebar before/after** — screenshots
4. **Help page screenshots** — at least the index + 1 article rendered
5. **Translation additions** — vi.csv new rows
6. **Out-of-scope reminder** — Báo cáo tiền mặt section deferred; rename `So Noi Bo` deferred; Q1=b dialog implemented for PC- only (PT- doesn't need sub-type)
7. **Final sign-off** — "ALL_TASKS_COMPLETE"

## Acceptance Criteria

Each criterion must be checkable. Mark `[x]` only after running the verification AND attaching evidence (commit SHA, screenshot path, or grep output).

- [ ] Branch `feat/tien-mat-redesign-and-help` has at least 4 atomic commits (sidebar, naming series patch, dialog JS, help page) — verified: `git log feat/tien-mat-redesign-and-help --oneline | wc -l` >= 4
- [ ] Section "Tiền mặt" in `vn_accounting/workspace_sidebar/vn_accounting.json` has exactly 7 child items with correct labels — verified: VC1 below
- [ ] Removed labels ("Thu tiền mặt", "Chi tiền mặt", "Sổ quỹ tiền mặt", "Tạo bút toán tiền mặt") absent from section — verified: VC2
- [ ] "Dự báo dòng tiền" appears exactly once in fixture (in Ngân hàng section) — verified: VC3
- [ ] New URL items have correct pre-fill query strings — verified: VC4-7
- [ ] All cross-workspace URL items (Phiếu thu / Phiếu chi / Rút-nộp tiền / Tạo biên bản kiểm kê) include `sidebar=VN%20Accounting` query param so Frappe v16 does NOT auto-switch sidebar to ERPNext Accounts module — verified: VC4b
- [ ] Live testing: after clicking each of items 1-3 (Phiếu thu/Phiếu chi/Rút-nộp), the sidebar still shows "Tiền mặt" section highlighted under "VN Accounting" workspace title (NOT "Accounts" / ERPNext sidebar). Capture screenshot showing sidebar context after each click. — verified: Live Testing step 4 captures sidebar context per click
- [ ] "Phiếu quỹ chi nhánh" `route_options` is JSON `{"docstatus": ["=", 1]}` — verified: VC8
- [ ] Patch file `vn_accounting/patches/v1_4_0/add_je_naming_series_pt_pc.py` compiles + listed in `patches.txt` — verified: VC9-10
- [ ] After running patch (in Live Testing), `tabProperty Setter` row `Journal Entry-naming_series-options` exists with PT- and PC- in value — verified: Live Testing step
- [ ] Bundle `phieu_chi_subtype_dialog.bundle.js` exists, syntactically valid (`node --check`), referenced in `hooks.py` `app_include_js` — verified: VC11-13
- [ ] Frappe Page `vn-help` files exist (`vn_help.json`, `.py`, `.js`, `.css`) and parse — verified: VC14-17
- [ ] API `vn_accounting/api/help.py` compiles and exports `get_article`, `get_index` — verified: VC18-19
- [ ] `vn_accounting/help/_index.json` parses as JSON, contains `tien-mat` section with 6 articles — verified: VC20
- [ ] All 6 markdown files exist with required H2 sections (`Mục đích`, `Khi nào dùng`, `Cách thực hiện`, `Định khoản tự động`, `Edge cases & cảnh báo`, `Báo cáo liên quan`, `FAQ`) — verified: VC21-26
- [ ] Test file `vn_accounting/tests/test_tien_mat_sidebar.py` exists with ≥9 test methods — verified: VC27-28
- [ ] Test suite passes (run inside Live Testing Procedure: `python3 -m unittest vn_accounting.tests.test_tien_mat_sidebar -v` exits 0 with all tests OK)
- [ ] vi.csv has new rows (e.g., "Cash Voucher Receipt", "Cash Voucher Payment", "Sub-type", "Internal Transfer") — verified: VC29
- [ ] Live testing: bench migrate runs cleanly (no orphan workspace warnings, patch executes), bench build succeeds for `vn_accounting` app — performed in Live Testing Procedure
- [ ] QA with Playwright MCP at http://dcnet.localhost:8001 (NOT headed — use Playwright server tools): walk through 7 sidebar items in "Tiền mặt" section; verify each opens correct page state (form/list/page). Capture screenshots to `docs/design-qa-proposals/tien-mat-screenshots/`. Console errors = 0 on every navigation.
- [ ] QA: open `/app/vn-help#tien-mat/index`, click each of 6 articles in left nav, verify content renders with markdown formatting (h1, h2, table, image). Screenshots to `docs/design-qa-proposals/tien-mat-screenshots/help-<slug>.png`. Console errors = 0.
- [ ] Design QA exploratory pass on sidebar + help page via Playwright MCP. Cosmetic fixes implemented autonomously and listed in verification report. Structural proposals (if any) appended to `docs/design-qa-proposals/tien-mat-redesign-and-help.md` with `## Session YYYY-MM-DD HH:MM` header. — verified: VC30 (proposals file exists if any, OR verification report has "no structural proposals" note)
- [ ] Verification report `docs/design-qa-proposals/tien-mat-redesign-verification.md` exists with all 7 required sections — verified: VC31-32
- [ ] Screenshots ≥10 PNGs in `docs/design-qa-proposals/tien-mat-screenshots/` — verified: VC33
- [ ] Help article inline screenshots ≥6 PNGs in `vn_accounting/help/tien-mat/_images/` — verified: VC34
- [ ] No edits outside allowed paths in scope — verified: `git diff main..HEAD --stat` shows only paths under `vn_accounting/workspace_sidebar/`, `vn_accounting/translations/`, `vn_accounting/hooks.py`, `vn_accounting/patches.txt`, `vn_accounting/patches/v1_4_0/`, `vn_accounting/public/js/phieu_chi_subtype_dialog.bundle.js`, `vn_accounting/page/vn_help/`, `vn_accounting/api/`, `vn_accounting/help/`, `vn_accounting/tests/`, `docs/design-qa-proposals/`, `docs/multi-session/`

## Constraints

- DO NOT modify any other sidebar section (Tổng quan, Ngân hàng, Mua hàng, Bán hàng, Kho, TSCĐ, CCDC, Tiền lương, Giá thành, Thuế, Tổng hợp, Báo cáo tài chính, Danh mục, Thiết lập). Verify with diff scoped to lines 28-138 of fixture.
- DO NOT rename or modify any DocType / Report file (Cash Receipts, Cash Payments, Cash Book, So Noi Bo). The "Sổ quỹ chi nhánh" rename is explicitly DEFERRED to a future task.
- DO NOT push the branch. User will review locally before merge.
- DO NOT modify ERPNext core or Frappe core (`apps/erpnext/`, `apps/frappe/`).
- DO NOT add new dependencies (pip / npm). Use only what's already in the bench env.
- Translation strings: only ADD rows to vi.csv, do NOT modify or delete existing rows.
- Branch `Cash Voucher` field on Journal Entry: do NOT add custom fields. Use existing `naming_series` differentiation only. PT- vs PC- prefix is the only signal needed.

## Verification Commands

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); items=d['items']; sec=next(i for i,it in enumerate(items) if it.get('type')=='Section Break' and it.get('label')=='Tiền mặt'); end=next((i for i,it in enumerate(items[sec+1:], sec+1) if it.get('type')=='Section Break'), len(items)); section=items[sec+1:end]; assert len(section)==7, f'expected 7 Tiền mặt items, got {len(section)}: {[it[\"label\"] for it in section]}'"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); labels=[it.get('label') for it in d['items']]; gone=['Thu tiền mặt','Chi tiền mặt','Sổ quỹ tiền mặt','Tạo bút toán tiền mặt']; missing=[l for l in gone if l in labels]; assert not missing, f'these should be removed: {missing}'"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); n=sum(1 for it in d['items'] if it.get('label')=='Dự báo dòng tiền'); assert n==1, f'Dự báo dòng tiền appears {n} times, expected 1'"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); items={it.get('label'):it for it in d['items']}; assert '+ Phiếu thu' in items, 'missing + Phiếu thu'; assert items['+ Phiếu thu']['link_type']=='URL'; assert 'voucher_type=Cash%20Entry' in items['+ Phiếu thu']['url']; assert 'naming_series=PT-.YYYY.-' in items['+ Phiếu thu']['url']"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); items={it.get('label'):it for it in d['items']}; assert '+ Phiếu chi' in items; assert items['+ Phiếu chi']['link_type']=='URL'; assert 'naming_series=PC-.YYYY.-' in items['+ Phiếu chi']['url']"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); items={it.get('label'):it for it in d['items']}; assert '+ Rút/nộp tiền' in items; assert items['+ Rút/nộp tiền']['link_type']=='URL'; assert 'voucher_type=Contra%20Entry' in items['+ Rút/nộp tiền']['url']"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); items={it.get('label'):it for it in d['items']}; cross=['+ Phiếu thu','+ Phiếu chi','+ Rút/nộp tiền','+ Tạo biên bản kiểm kê']; missing=[lbl for lbl in cross if lbl in items and 'sidebar=VN%20Accounting' not in items[lbl].get('url','')]; assert not missing, f'missing sidebar=VN%20Accounting param in: {missing}'"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); items={it.get('label'):it for it in d['items']}; assert '+ Tạo biên bản kiểm kê' in items; assert items['+ Tạo biên bản kiểm kê']['url'].startswith('/app/cash-count/new')"

python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); items={it.get('label'):it for it in d['items']}; ro=items['Phiếu quỹ chi nhánh'].get('route_options'); assert ro, 'no route_options'; parsed=json.loads(ro); assert parsed=={'docstatus':['=',1]}, parsed"

test -f vn_accounting/patches/v1_4_0/add_je_naming_series_pt_pc.py

python3 -m py_compile vn_accounting/patches/v1_4_0/add_je_naming_series_pt_pc.py

grep -q "vn_accounting.patches.v1_4_0.add_je_naming_series_pt_pc" vn_accounting/patches.txt

test -f vn_accounting/public/js/phieu_chi_subtype_dialog.bundle.js

node --check vn_accounting/public/js/phieu_chi_subtype_dialog.bundle.js

grep -q "phieu_chi_subtype_dialog.bundle.js" vn_accounting/hooks.py

test -f vn_accounting/page/vn_help/vn_help.json

test -f vn_accounting/page/vn_help/vn_help.js

test -f vn_accounting/page/vn_help/vn_help.py

python3 -m py_compile vn_accounting/page/vn_help/vn_help.py

test -f vn_accounting/api/help.py

python3 -m py_compile vn_accounting/api/help.py

python3 -c "import json; d=json.load(open('vn_accounting/help/_index.json')); secs=[s for s in d if s.get('section')=='tien-mat']; assert secs, 'no tien-mat section'; assert len(secs[0].get('articles',[]))==6, f\"expected 6 articles, got {len(secs[0].get('articles',[]))}\""

test -f vn_accounting/help/tien-mat/index.md

test -f vn_accounting/help/tien-mat/phieu-thu.md

test -f vn_accounting/help/tien-mat/phieu-chi.md

test -f vn_accounting/help/tien-mat/rut-nop-tien.md

test -f vn_accounting/help/tien-mat/kiem-ke-quy.md

test -f vn_accounting/help/tien-mat/so-quy-chi-nhanh.md

test -f vn_accounting/tests/test_tien_mat_sidebar.py

test $(grep -c '^    def test_' vn_accounting/tests/test_tien_mat_sidebar.py) -ge 9

grep -q '^Cash Voucher Receipt,' vn_accounting/translations/vi.csv

test -f docs/design-qa-proposals/tien-mat-redesign-verification.md

grep -q '## Summary' docs/design-qa-proposals/tien-mat-redesign-verification.md

test $(find docs/design-qa-proposals/tien-mat-screenshots/ -name '*.png' 2>/dev/null | wc -l) -ge 10

test $(find vn_accounting/help/tien-mat/_images/ -name '*.png' 2>/dev/null | wc -l) -ge 6

## Live Testing Procedure

The runner does NOT execute these — the agent runs them inside its session.

1. From bench root, apply DB-mutating ops:
   ```bash
   cd /home/long/long/frappe-bench-dcnet
   bench --site dcnet.localhost migrate
   bench --site dcnet.localhost clear-cache
   bench build --app vn_accounting
   ```

2. Verify Property Setter applied:
   ```bash
   bench --site dcnet.localhost mariadb -N -B -e "SELECT value FROM \`tabProperty Setter\` WHERE name='Journal Entry-naming_series-options'"
   # expect: contains PT-.YYYY.- and PC-.YYYY.-
   ```

3. Run sidebar test:
   ```bash
   cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
   python3 -m unittest vn_accounting.tests.test_tien_mat_sidebar -v
   # expect: all tests pass, "OK"
   ```

4. Use Playwright MCP browser tools to walk sidebar — **with explicit sidebar context preservation check after each click**:
   - `mcp__plugin_playwright_playwright__browser_navigate` to `http://dcnet.localhost:8001/app/vn-accounting`
   - Authenticate if needed (cookies from prior session)
   - Take a baseline screenshot showing the active workspace title + sidebar structure (expect "VN Accounting" title with sections including "Tiền mặt").
   - For each of the 7 items in section "Tiền mặt": click → verify URL → take browser_snapshot AND assert via JS evaluate that the active workspace sidebar header still reads "VN Accounting" (not "Accounts" / ERPNext / any other module). Use `browser_evaluate` with: `() => { const s=document.querySelector('.body-sidebar .standard-sidebar-section.indent[data-workspace-name]'); return {workspace: s?.dataset?.workspaceName, title: document.querySelector('.body-sidebar .sidebar-title')?.textContent?.trim()}; }` (adjust selector if Frappe v16 differs — the goal: capture which workspace owns the currently-shown sidebar). If sidebar switched away from "VN Accounting" → BLOCKER, root-cause the failure (likely missing `sidebar=VN%20Accounting` URL param OR Frappe Workspace name mismatch).
   - Screenshot to `docs/design-qa-proposals/tien-mat-screenshots/sidebar-N-<slug>.png` (showing both the loaded form/page AND the unchanged left sidebar context).
   - Check console errors via `browser_console_messages` (expect 0 errors per navigation).
   - For "+ Phiếu chi": after clicking, the sub-type dialog should open. Pick "Trả NCC" → verify accounts table has 2 rows pre-filled (TK 331 in row 1, TK 1111 in row 2). Screenshot dialog + filled form. Also verify sidebar still shows "VN Accounting" / "Tiền mặt" section highlighted.
   - For "+ Phiếu thu" / "+ Rút/nộp tiền" / "+ Tạo biên bản kiểm kê": same sidebar-preservation check after each.

   If the `sidebar=VN%20Accounting` URL approach fails (Frappe might require different value or the slug `vn-accounting`), debug:
   1. Try `sidebar=vn-accounting` (lowercase slug)
   2. Try `sidebar=VN+Accounting` (plus instead of %20)
   3. Inspect `frappe.boot.workspace_sidebar_item` keys via console to find the actual key the workspace registers under
   4. Document the working value in commit message AND in verification report
   5. Update VC4b grep to match the working value

5. Walk help page:
   - Navigate `http://dcnet.localhost:8001/app/vn-help`
   - Verify left nav lists "Tiền mặt" section with 6 articles
   - Click each article → verify right pane updates with rendered markdown
   - Screenshot each rendered article
   - Capture console errors per navigation

6. Design QA exploratory pass:
   - Use Playwright MCP to inspect the sidebar + help page like a first-time user
   - Note any visual inconsistencies, awkward spacing, label confusion
   - Apply cosmetic fixes (label wording, padding, font weight) directly with bench build + clear-cache between iterations
   - Log structural proposals (workflow changes, missing fields) to `docs/design-qa-proposals/tien-mat-redesign-and-help.md`

7. After all verification passes, write final verification report and create commit.

8. Rollback if needed (failure mid-run): `git checkout main` resets workspace; uncommitted changes preserved via `git stash`.

## Agent Persona

You are a senior Frappe v16 developer with deep Vietnamese accounting domain knowledge (TT133/TT200/TT99/2025). You read hooks.py and existing fixtures BEFORE editing. You use `frappe.get_doc()` and `frappe.db.set_value()` (not raw SQL) for DocType operations. You always run `bench clear-cache` after editing fixtures or hooks.py. You write Python with type hints and dict shape assertions. For JS bundle code, you use Frappe's existing utilities (`frappe.prompt`, `frappe.db.get_value`, `frm.add_child`) and AVOID monkey-patching prototypes when an extension hook exists. You read `~/.claude/rules/frappe.md` and `~/.claude/rules/frappe-v16-ui.md` for known pitfalls — especially the "Workspace Sidebar must have route_options as JSON string" gotcha and the "Custom app `.save()` on owned-by-other-module Workspace Sidebar leaks into other apps" rule.

## Model

auto

## Time Budget

- Session minutes: 30 (max per session)
- Max sessions: 12 (safety cap)
- Total hours: 6 (overall budget)
