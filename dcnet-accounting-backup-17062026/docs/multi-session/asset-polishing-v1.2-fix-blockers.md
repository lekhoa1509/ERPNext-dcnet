# Task: Asset Polishing v1.2 — Fix 7 P0 Blockers + 16 P1 Findings

## Context

Design QA review (commit `b083c0b`) phát hiện **49 findings** (29 PM + 20 KTV), score 4.5/10. Branch `feat/asset-polishing` v1.1 KHÔNG ship được vì có 7 unique P0 blockers + 16 P1 issues. Task này fix tất cả P0 + P1, batch-fix P2 nếu thời gian cho phép.

**Source of findings:** `docs/design-qa-proposals/asset-polishing-personas-review.md` — read FIRST every session để map fix → finding ID.

## Scope

- Project: `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing` (worktree)
- Branch: `feat/asset-polishing` — **TIẾP TỤC trên branch hiện tại** (KHÔNG tạo branch mới, KHÔNG merge v1.1 broken state vào main)
- Starting SHA: `b083c0b` (worktree HEAD); apps/vn_accounting đã sync về SHA này
- Bench root: `/home/long/long/frappe-bench-dcnet`
- Test site: `dcnet.localhost`
- Test URL: `http://dcnet.localhost:8001`

### Worktree dance (BẮT BUỘC mỗi session)

Per `git-deploy.md` memory — apps/vn_accounting và worktree là 2 checkouts khác nhau:

```bash
# Verify ở đầu mỗi session
cd /home/long/long/frappe-bench-dcnet
worktree_sha=$(git -C .worktrees/vn_accounting-asset-polishing rev-parse HEAD)
apps_sha=$(git -C apps/vn_accounting rev-parse HEAD)
if [ "$worktree_sha" != "$apps_sha" ]; then
  git -C apps/vn_accounting checkout --detach feat/asset-polishing
fi

# Sau JSON change: bench --site dcnet.localhost migrate
# Sau Python change: bench restart (nếu serve đang chạy)
# Sau JS/CSS: bench build --app vn_accounting
# Sau vi.csv / fixture: bench --site dcnet.localhost clear-cache
```

### Related files

| File | P0/P1 fix |
|------|-----------|
| `vn_accounting/install.py` | Fix CCDC Category seed (PM-13) |
| `vn_accounting/vn_accounting/report/s21_dn_so_tscd/s21_dn_so_tscd.py` | Fix report crash (PM-29) |
| `vn_accounting/vn_accounting/doctype/asset_stocktake/asset_stocktake.json` + `.py` | Fix Jinja default leak (PM-24) |
| `vn_accounting/workspace_sidebar/vn_accounting.json` | Add 5 missing sidebar items (PM-04) |
| `vn_accounting/vn_accounting/doctype/asset_repair/` (CF/PS) | Fix workspace routing (PM-03) |
| `vn_accounting/vn_accounting/print_format/asset_handover_s22_dn/asset_handover_s22_dn.json` | Fix JSON leak + add signatures (PM-23, PM-27) |
| `vn_accounting/translations/vi.csv` | i18n cleanup ~25 entries (PM-02, 14, 15, 21, KTV-05,06,07,08,09) |
| `vn_accounting/vn_accounting/doctype/{ccdc_item,asset_handover,asset_stocktake,ccdc_writeoff}/*.json` | Naming/autoname (PM-05,09,10), list view columns (PM-07), status vocabulary (PM-08) |
| `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.{json,py}` | Settings UX + permission boundary (PM-11, KTV-11) |

## Requirements

### Phase 1 — P0 Blockers (7 fixes)

**Outcome:** Site usable end-to-end without crashes, sidebar complete, prints render correctly. Each fix references finding ID in commit message: `fix(asset-polishing): {desc} (fixes #PM-NN, #KTV-NN)`.

**P0-1 — CCDC Category fixture not seeded (PM-13/KTV-03)**

Symptom: `frappe.db.count("CCDC Category") == 0`. CCDC Item form Link field empty → cannot create CCDC Item → entire CCDC workflow blocked.

Steps:
1. Read `vn_accounting/install.py` — verify `_seed_ccdc_categories()` exists + called from `after_install` AND `after_migrate`
2. If function missing or not called: implement per design §7.5 (5 categories: Bàn ghế VP, Máy tính, Dụng cụ SX, Đồ bảo hộ, Khác)
3. Run `bench --site dcnet.localhost execute vn_accounting.install._seed_ccdc_categories` to backfill
4. Verify: `bench console` → `frappe.db.count("CCDC Category") >= 5`
5. Verify each category has correct account mapping (153 sub, 242, 627/641/642 expense)

**P0-2 — Sổ S21-DN report crash (PM-29/KTV-01)**

Symptom: report opens with error stack trace. Cannot view Sổ TSCĐ.

Steps:
1. Open report URL via Playwright → capture error stack
2. Read `s21_dn_so_tscd.py` `execute(filters)` function
3. Common causes: SQL syntax with f-string (security), missing required filter handling, ERPNext API call returning None, parameter unpack error
4. Fix root cause per `superpowers:systematic-debugging` skill (4-phase: investigate → analyze → hypothesize → implement)
5. Test with various filter combinations: company filter, date range, asset_category filter, no filter (default), submitted-only

**P0-3 — Asset Stocktake Jinja default value leak (PM-24/KTV-02)**

Symptom: new form `company` field shows literal text `{{ company }}` instead of evaluating to current company.

Steps:
1. Open `asset_stocktake.json` — find `company` field default value
2. Common bug: `default: "{{ frappe.defaults.get_user_default('company') }}"` — Jinja syntax in JSON default doesn't auto-eval
3. Fix: change default to `default: ""` and set value in `before_insert` controller hook OR use Frappe's native default mechanism (`fetch_from`/`default: User Default`)
4. Verify: open new form → company field auto-fills with current company name (not literal Jinja)

**P0-4 — Asset Repair workspace routing leak (PM-03)**

Symptom: clicking Asset Repair from sidebar jumps to ERPNext "Tài sản" workspace, sidebar context lost, "Getting Started" wizard popup appears.

Steps:
1. Read Asset Repair DocType JSON for `workspace_link` or related field
2. ERPNext Asset Repair belongs to "Asset" module workspace by default. Override:
   - Option a) Custom Field on Asset Repair: `vn_accounting_workspace_link` to redirect
   - Option b) Add Asset Repair to vn_accounting workspace_sidebar with explicit route_options
   - Option c) Property Setter overriding `Asset Repair.workspace` (if such field exists)
3. Add Asset Repair link to `workspace_sidebar/vn_accounting.json` under TSCĐ section as DocType link
4. Verify: from Kế Toán VN sidebar → click "Sửa chữa" → form opens with sidebar=Kế Toán VN (not ERPNext Tài sản)

**P0-5 — Sidebar missing 5 items (PM-04)**

Per design §5.1, sidebar should have 13 items total (7 TSCĐ + 6 CCDC). Currently missing:
- Sửa chữa (Asset Repair, route to scope=N/A — single DocType for both)
- Bàn giao TSCĐ (Asset Handover, route_options scope=TSCĐ)
- Bàn giao CCDC (Asset Handover, route_options scope=CCDC)
- Kiểm kê TSCĐ (Asset Stocktake, route_options scope=TSCĐ)
- Kiểm kê CCDC (Asset Stocktake, route_options scope=CCDC)
- Ghi giảm CCDC (CCDC Writeoff)

Steps:
1. Read current `workspace_sidebar/vn_accounting.json`
2. Add 6 missing items in correct position (per §5.1 layout: TSCĐ section then CCDC)
3. Set route_options where applicable
4. After save: bench migrate + clear-cache + verify in browser (login fresh — sidebar boots once)

**P0-6 — Print S22-DN raw JSON leak (PM-23)**

Symptom: print preview shows raw JSON output (likely Jinja error or wrong template field). 

Steps:
1. Open print format JSON → check `html` field
2. Common bug: orphan `{{ doc.something_that_doesnt_exist }}` causing Jinja to print fallback or syntax leak
3. Verify Jinja syntax: all `{% ... %}` and `{{ ... }}` properly closed; field names match DocType
4. Fix template; test with submitted Asset Handover doc

**P0-7 — Print S22-DN no signature blocks (PM-27)**

Symptom: print format missing 3-sign blocks (Bên giao / Bên nhận / Kế toán + co_signer if present).

Steps:
1. Add signature block HTML at end of print format `html` field (use Asset Disposal print format pattern)
2. Format: 3 (or 4) cells side-by-side, each with role label, blank space for signature, name + date
3. Conditional render: `{% if doc.co_signer_employee %}` for 4th block

### Phase 2 — i18n Cleanup (~9 P1 i18n items)

**Outcome:** Zero English label residual on Asset/CCDC/Handover/Stocktake/Repair/Disposal/Writeoff forms. vi.csv complete.

Findings to fix (1 commit per finding or grouped per file):

- **PM-02** Asset new form — list missing labels, add to vi.csv
- **PM-14** Asset Disposal — i18n residual
- **PM-15** Asset Repair new form — i18n
- **PM-21** Asset Handover — 6 English labels (legal document — high priority)
- **KTV-05** Asset Handover — same as PM-21 (cross-cutting, fix once)
- **KTV-06** Asset Disposal — i18n
- **KTV-07** CCDC Writeoff — i18n
- **KTV-08** CCDC Item — i18n
- **KTV-09** Asset — i18n (extends PM-02)

Procedure per finding:
1. Open form in browser, screenshot (capture all visible English labels)
2. For each English label: find source (DocType JSON `label` field OR ERPNext native label needing translation)
3. Native labels → add to `vn_accounting/translations/vi.csv` (2-col: source,translated)
4. Custom DocType labels → edit JSON `label` field directly (Vietnamese)
5. Bench cycle (migrate if JSON, clear-cache always)
6. Re-screenshot to verify
7. Commit: `fix(asset-polishing): i18n {DocType name} {N} labels (fixes #PM-NN, #KTV-NN)`

### Phase 3 — UX Consistency (~7 P1 items)

**Outcome:** Naming, list views, status vocabulary, navigation consistent across new DocTypes.

- **PM-05** CCDC Item naming convention (use sequential CCDC-YYYY-NNNNN like Asset)
- **PM-07** CCDC Allocation/Writeoff list views — add missing columns (e.g., ccdc_item.cost summary)
- **PM-08** CCDC Item status vocabulary — verify Vietnamese consistency
- **PM-09** Asset Disposal naming — verify still works after fixes
- **PM-11** Settings UX improvements — based on finding details
- **PM-22** Asset Handover submitted — navigation/print buttons (#7 from v1.1 design QA já fixed; verify)
- **KTV-04** Asset Handover submitted — same as PM-22 cross-cut
- **KTV-10** Asset Handover/Stocktake/CCDC Item/CCDC Writeoff lists — UX/naming
- **KTV-11** VN Accounting Settings — permission boundary (only Accounts Manager edit?)

Procedure: read each finding's recommendation in report, apply, test, commit referencing finding ID.

### Phase 4 — P2 Batch + Final QA

**Outcome:** P2 items batch-fixed where simple text/style change; defer complex ones to v1.3 (log into report Update section).

Steps:
1. Re-read all P2 findings (PM-01, 06, 10, 12, 16-20, 25, 28; KTV-12-20)
2. Group by file → batch fix simple text/label/order
3. Skip P2 needing data model change (defer)
4. Run final smoke test: navigate sidebar 13 items → verify each opens correctly
5. Try full lifecycle: create CCDC → submit → allocate → writeoff. Create TSCĐ → bàn giao → kiểm kê → thanh lý. Confirm no crashes.
6. Update `docs/design-qa-proposals/asset-polishing-personas-review.md`:
   - Add `## Session 2026-04-29 v1.2 Fix Pass` header
   - Below each fixed finding: append `→ Fixed in v1.2 ({commit-sha}) on {date}`
   - List remaining deferred items (P2 not fixed) under "## Deferred to v1.3"
7. Bump VERSION 1.1.0 → 1.2.0
8. Final commit: `feat(asset-polishing): v1.2 ship — fix 7 P0 + 16 P1 findings, score upgraded`

## Acceptance Criteria

### Phase 1 P0
- [ ] `frappe.db.count("CCDC Category") >= 5` (verify via console)
- [ ] Sổ S21-DN opens without error in browser; renders rows for at least 1 test asset
- [ ] Asset Stocktake new form: company field auto-filled with company name (not Jinja string)
- [ ] Asset Repair from Kế Toán VN sidebar opens with sidebar=Kế Toán VN (not ERPNext Tài sản)
- [ ] Sidebar has ≥13 link items in TSCĐ + CCDC sections combined (verify via JSON parse)
- [ ] Print S22-DN preview: NO raw JSON visible
- [ ] Print S22-DN: ≥3 signature blocks visible (regex check on rendered HTML or visual screenshot)

### Phase 2 i18n
- [ ] vi.csv has ≥25 new entries since b083c0b (verify line count diff)
- [ ] Asset Handover form: 0 English labels visible (Playwright DOM check or manual screenshot review)
- [ ] Each i18n fix commit references at least 1 finding ID

### Phase 3 UX
- [ ] CCDC Item naming follows pattern `CCDC-YYYY-NNNNN` (verify via SQL: pattern match on tabCCDC Item.name)
- [ ] CCDC Allocation Schedule list view shows ≥4 columns including progress
- [ ] Each UX fix commit references finding ID

### Phase 4 Final
- [ ] Sidebar full smoke test: each of 13 items opens correctly (Playwright snapshot)
- [ ] Full lifecycle: CCDC create→submit→allocate→writeoff WITHOUT errors
- [ ] Full lifecycle: TSCĐ create→bàn giao→kiểm kê→thanh lý WITHOUT errors
- [ ] Report file updated with `## Session 2026-04-29 v1.2 Fix Pass` section
- [ ] VERSION bumped to 1.2.0
- [ ] Final commit "v1.2 ship" exists on feat/asset-polishing

### Standard
- [ ] All Phase 1 and 2 commits reference finding IDs (`grep -E "fixes #(PM|KTV)-"` count ≥ 16)
- [ ] `bench migrate` succeeds after all changes
- [ ] `bench build --app vn_accounting` succeeds
- [ ] No new files outside `vn_accounting/`, `docs/`, `qa-screenshots/`
- [ ] `apps/vn_accounting` SHA == worktree HEAD at end of each session (verify dance)

## Constraints

- Branch: KEEP on `feat/asset-polishing`. KHÔNG tạo branch mới. KHÔNG merge to main đến khi v1.2 ship clean.
- Commit format: mỗi P0/P1 fix là 1 atomic commit, message reference finding ID(s)
- KHÔNG bỏ qua P0 — tất cả 7 phải fix Phase 1
- P1 phải fix hết Phase 2-3 (cap 16, có thể defer 1-2 nếu cần data model change lớn)
- P2 nice-to-have — defer to v1.3 nếu cần
- KHÔNG modify ERPNext core (`apps/erpnext/`)
- Worktree dance enforced — verify SHA match đầu mỗi session
- Use `superpowers:systematic-debugging` cho mỗi P0 (4-phase, max 3 attempts then document)
- Use `superpowers:verification-before-completion` trước khi mark criterion `[x]`

## Verification Commands

test -f docs/design-qa-proposals/asset-polishing-personas-review.md
sh -c 'wt_sha=$(git rev-parse HEAD); apps_sha=$(git -C /home/long/long/frappe-bench-dcnet/apps/vn_accounting rev-parse HEAD); test "$wt_sha" = "$apps_sha"'
sh -c 'count=$(git log feat/asset-polishing --pretty=format:"%s" | grep -cE "fixes #(PM|KTV)-" 2>/dev/null || echo 0); test "$count" -ge 16'
grep -qE "## Session 2026-04-29 v1\.2 Fix Pass" docs/design-qa-proposals/asset-polishing-personas-review.md
grep -qE '__version__\s*=\s*"1\.2\.' vn_accounting/__init__.py
sh -c 'sidebar_count=$(python3 -c "import json; d=json.load(open(\"vn_accounting/workspace_sidebar/vn_accounting.json\")); print(len([i for i in d[\"items\"] if i.get(\"child\")==1 and i.get(\"label\","").strip() in [\"Sửa chữa\",\"Bàn giao TSCĐ\",\"Bàn giao CCDC\",\"Kiểm kê TSCĐ\",\"Kiểm kê CCDC\",\"Ghi giảm CCDC\"]]))"); test "$sidebar_count" -ge 5'
git log feat/asset-polishing -1 | grep -qE "v1\.2 ship"
test -d qa-screenshots/v1.2-fixes
sh -c 'count=$(find qa-screenshots/v1.2-fixes -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 10'

## Live Testing Procedure

### Setup verification (đầu mỗi session)

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing
# Verify worktree is on feat/asset-polishing
git status -sb | grep -q "## feat/asset-polishing" || { echo "ERROR: not on feat/asset-polishing"; exit 1; }
# Verify apps/ matches
wt=$(git rev-parse HEAD)
apps=$(git -C /home/long/long/frappe-bench-dcnet/apps/vn_accounting rev-parse HEAD)
[ "$wt" = "$apps" ] || { cd /home/long/long/frappe-bench-dcnet && git -C apps/vn_accounting checkout --detach feat/asset-polishing; }
# Read findings file
cat docs/design-qa-proposals/asset-polishing-personas-review.md | head -200
```

### Per-fix workflow

1. Read finding in report (line range from grep)
2. Apply systematic-debugging skill if it's a crash/bug
3. Make fix in worktree
4. Bench cycle (migrate / build / clear-cache as appropriate)
5. Verify in browser via Playwright MCP
6. Screenshot to `qa-screenshots/v1.2-fixes/{finding-id}.png`
7. Commit atomic with message referencing finding ID

### End-of-session verification

1. Run all Verification Commands manually before declaring complete
2. Update session-last.md with: which findings fixed, which still pending
3. NEVER write `ALL_TASKS_COMPLETE` unless ALL acceptance criteria pass

## Agent Persona

Senior Frappe/ERPNext developer doing P0 bug-fix sprint. Familiar with:
- Worktree ↔ apps/ deployment dance (per `git-deploy.md` memory)
- Frappe Property Setter / Custom Field for ERPNext overrides
- Frappe Jinja default value evaluation rules (User Default vs literal vs server hook)
- Print format Jinja syntax + signature block patterns (Asset Disposal pattern reference)
- ERPNext Asset Repair workspace assignment internals
- Script Report query debugging
- VN i18n CSV pattern (vn_accounting/translations/vi.csv)

Always:
- Read finding in report BEFORE attempting fix (extract exact symptom + recommendation from agent's predecessor)
- Use systematic-debugging for P0 (don't shortcut to "looks fixed")
- Reference finding ID(s) in commit message per format `fix(asset-polishing): {desc} (fixes #PM-NN, #KTV-NN)`
- Verify worktree dance correct at session start
- Verify in browser (not just code change verified) — Playwright MCP screenshot after fix
- Update session-last.md với specific findings fixed this session

NEVER:
- Skip verification because "it looks right"
- Mark criterion `[x]` without browser test
- Make multi-finding commits (1 atomic per finding)
- Touch ERPNext core
- Push to main / create PR đến khi all P0+P1 verified

## Model

auto

## Time Budget

- Max hours: 22 (matches MEMORY.md estimate "v1.2 scope ~20.5h" + 1.5h buffer)
- Max sessions: 35 (P0 ~10, P1 ~15, P2 batch + QA ~10)
- Per-session minutes: 30

**Per-phase session estimate:**
- Phase 1 (7 P0): ~10 sessions (some P0 like S21-DN crash + workspace routing need debug investigation)
- Phase 2 (~9 i18n P1): ~6 sessions
- Phase 3 (~7 UX P1): ~5 sessions
- Phase 4 (P2 batch + final QA + docs): ~4 sessions
