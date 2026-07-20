# Task: Asset Polishing v1.2.1 + v1.2.2 — Cleanup remaining 11 findings

## Context

`feat/asset-polishing` đã FF-merge vào `main` (commit `4f440a1`). v1.2 ship clean với 38/49 design QA findings đã fix (commit `e7ebb81`). Còn lại **11 findings** đang đợi:

- **2 P1** (v1.2.1 priority): PM-08 CCDC state machine, PM-09 Asset Disposal terminology
- **9 P2** (v1.2.2 cosmetic): PM-01, 12, 16, 17, KTV-14, 15, 18, 19, 20

Task này gộp cả 2 milestone (P1 trước, P2 sau) trong 1 multi-session run, end with v1.2.2 ship + final merge to main.

Source of truth: `docs/design-qa-proposals/asset-polishing-personas-review.md` — read FIRST mỗi session.

## Scope

- Project: `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing`
- Branch: `feat/asset-polishing` (continue, KHÔNG tạo branch mới)
- Starting SHA: `4f440a1` (worktree HEAD == main HEAD)
- apps/vn_accounting: đã sync, no dirty
- Bench root: `/home/long/long/frappe-bench-dcnet`
- Test site: `dcnet.localhost`

### Worktree dance enforced (mỗi session)

```bash
cd /home/long/long/frappe-bench-dcnet
wt=$(git -C .worktrees/vn_accounting-asset-polishing rev-parse HEAD)
apps=$(git -C apps/vn_accounting rev-parse HEAD)
[ "$wt" != "$apps" ] && git -C apps/vn_accounting checkout --detach feat/asset-polishing
```

### Related files

| File | Findings touched |
|------|------------------|
| `vn_accounting/vn_accounting/doctype/ccdc_item/ccdc_item.{json,py,js}` | PM-08 state machine |
| `vn_accounting/vn_accounting/doctype/asset_disposal/asset_disposal.{json,py}` | PM-09 terminology |
| `vn_accounting/translations/vi.csv` | KTV-18, KTV-20, PM-17 i18n |
| `vn_accounting/workspace_sidebar/vn_accounting.json` + workspace JSON | PM-01 KPI bar, PM-12 logo, KTV-15 navigation |
| `vn_accounting/vn_accounting/doctype/asset_repair/` (CF/PS) | PM-16, PM-17, KTV-14 |
| `vn_accounting/vn_accounting/doctype/ccdc_writeoff/ccdc_writeoff.json` | KTV-19 list UX |

## Requirements

### Phase v1.2.1 — 2 P1 deep-dive fixes (~3h)

**Outcome:** PM-08 + PM-09 fixed with code-level rigor (cần investigation, không phải text-only). Each commit referenc finding ID + verifies via Playwright.

**PM-08 — CCDC Item state machine (4 states broken)**

Symptom (per report finding): CCDC Item.status có 4 options [Mới mua, Đang sử dụng, Hết phân bổ, Đã ghi giảm] nhưng transition giữa các state không nhất quán. State machine logic bị break.

Steps:
1. Read full PM-08 finding + recommendation in report
2. Use `superpowers:systematic-debugging` 4-phase
3. Verify state transitions:
   - Draft → submit → "Đang sử dụng" (set in on_submit)
   - "Đang sử dụng" → kỳ cuối allocation → "Hết phân bổ" (set in CCDC Allocation Schedule scheduler)
   - "Đang sử dụng"/"Hết phân bổ" → CCDC Writeoff submit → "Đã ghi giảm"
   - Status "Mới mua": chỉ ở Draft? Hay khi tạo từ PI auto?
4. Identify which transitions hiện tại có bug (state stuck, không update, hoặc revert sai)
5. Fix in CCDC Item controller + CCDC Allocation Schedule + CCDC Writeoff hooks
6. Test full lifecycle: PI → CCDC draft "Mới mua" → submit "Đang sử dụng" → 12 kỳ phân bổ → kỳ cuối "Hết phân bổ" → giả lập Writeoff giữa kỳ → "Đã ghi giảm"
7. Commit: `fix(asset-polishing): CCDC Item state machine 4-state transitions (fixes #PM-08)`

**PM-09 — Asset Disposal terminology unification**

Symptom: 3 different terms used cho cùng concept "thanh lý" (probably "Disposal", "Thanh lý", "Cancel Disposal" mixed).

Steps:
1. Read PM-09 finding + recommendation
2. Grep `vn_accounting/` cho all uses: "thanh lý", "Disposal", "disposal", "Cancel Disposal"
3. Map locations: DocType label, field label, button label, vi.csv entries, print format
4. Pick ONE canonical term per VAS convention (per recommendation in report)
5. Fix all locations (vi.csv + JSON + JS button labels) consistently
6. Verify in browser: Asset Disposal form → all UI text uses canonical term
7. Commit: `fix(asset-polishing): unify Asset Disposal terminology (fixes #PM-09)`

### Phase v1.2.2 — 9 P2 cosmetic fixes (~2.5h)

**Outcome:** All P2 items either fixed (cosmetic-safe) or explicitly deferred to v1.3 with reason. Group commits where natural (e.g., 2-3 i18n in 1 commit if same file).

For each P2:

**PM-01** Workspace KPI bar layout — adjustment to KPI cards layout/spacing per finding recommendation
**PM-12** Workspace top-left logo branding — replace if Frappe default still visible
**PM-16** Asset Repair new form navigation — small UX improvement
**PM-17** Asset Repair new form i18n — vi.csv entries
**KTV-14** Asset Repair list UX/onboarding — list_view config, perhaps add help block
**KTV-15** Workspace navigation — small navigation hint
**KTV-18** Asset Khấu hao tab i18n — vi.csv entries
**KTV-19** CCDC Writeoff list UX/naming — list_view config columns
**KTV-20** Asset new form i18n/UX — vi.csv entries

Procedure per finding:
1. Read finding in report
2. Apply if cosmetic-safe (vi.csv add, label rename, list_view column, simple style)
3. If complex / requires data model change → defer with note in Deferred section
4. Commit format: `fix(asset-polishing): {desc} (fixes #PM-NN, #KTV-NN)`. Group when same file (e.g., 1 commit cho 3 vi.csv entries của KTV-18+KTV-20+PM-17).

### Phase Final — Update report + ship + merge (~30min)

1. **Update `docs/design-qa-proposals/asset-polishing-personas-review.md`:**
   - Find `## Deferred to v1.3` section
   - Move PM-08, PM-09 ra khỏi (đã fix) — note commit SHA
   - Move ANY P2 đã fix ra khỏi
   - List còn lại CHÍNH XÁC những gì thực sự defer (none, or 1-2 if any)
   - Add sub-section `### v1.2.x Fix Pass (2026-04-29)` liệt kê 11 items với commit SHA mỗi item
2. **Bump VERSION** `1.2.0` → `1.2.2` (skip 1.2.1 vì gộp luôn) trong `vn_accounting/__init__.py`
3. **Update FEATURES.md**: nếu có mục liên quan, mark Done
4. **Final commit:** `feat(asset-polishing): v1.2.2 ship — fix 11 remaining P1/P2 findings, score upgraded`
5. **FF merge feat → main locally:**
   ```bash
   git fetch . feat/asset-polishing:main
   ```
6. **Verify apps/ sync** lần cuối
7. **Update PR #33 trên dcnet-cloud** (đã OPEN): push lên `dcnet/feature/asset-polishing` để PR pick up new commits — `git push dcnet feat/asset-polishing:feature/asset-polishing`

## Acceptance Criteria

### v1.2.1 P1
- [ ] CCDC Item lifecycle test (Draft → submit → kỳ cuối → writeoff giữa kỳ): mỗi step status đúng (verify SQL `tabCCDC Item.status`)
- [ ] grep -r `Asset Disposal\|Cancel Disposal\|Thanh lý` vn_accounting/ → consistent terminology (only 1 canonical term in user-facing strings)
- [ ] Both P1 commits exist with `fixes #PM-08` and `fixes #PM-09`

### v1.2.2 P2
- [ ] At least 6/9 P2 items fixed (some may legitimately defer if complex)
- [ ] Each fix commit references finding ID
- [ ] Deferred items listed explicitly in report Deferred section với reason

### Final
- [ ] VERSION bumped to 1.2.2
- [ ] Report updated: Deferred section accurate (no items already fixed listed there)
- [ ] Final commit "v1.2.2 ship" on feat/asset-polishing
- [ ] main FF-merged to feat tip (verify `git log --oneline main..feat/asset-polishing | wc -l == 0`)
- [ ] dcnet/feature/asset-polishing pushed up to date (verify `git log --oneline dcnet/feature/asset-polishing..feat/asset-polishing | wc -l == 0`)
- [ ] PR #33 picks up new commits (manual check via `gh pr view 33 -R dcnet-cloud/dcnet-accounting`)

### Standard
- [ ] `bench --site dcnet.localhost migrate` succeeds
- [ ] `bench build --app vn_accounting` succeeds
- [ ] apps/ SYNCED with worktree at end of each session
- [ ] No new files outside `vn_accounting/`, `docs/`, `qa-screenshots/`

## Constraints

- KHÔNG tạo DocType mới
- KHÔNG đổi data model / JE routing / permission rules
- KHÔNG modify ERPNext core
- 1 fix / 1 commit (atomic). Group nhiều findings cùng file OK nếu commit message liệt kê đủ ID
- KHÔNG skip P1 — PM-08 + PM-09 phải fix Phase v1.2.1
- P2 cap: defer max 3/9 nếu complex (need data model change). Phải log lý do trong Deferred section
- Worktree dance enforced
- Use `superpowers:systematic-debugging` cho PM-08 (state machine bug)
- Use `superpowers:verification-before-completion` trước khi mark `[x]`

## Verification Commands

test -f docs/design-qa-proposals/asset-polishing-personas-review.md
sh -c 'wt_sha=$(git rev-parse HEAD); apps_sha=$(git -C /home/long/long/frappe-bench-dcnet/apps/vn_accounting rev-parse HEAD); test "$wt_sha" = "$apps_sha"'
sh -c 'pm08_count=$(git log feat/asset-polishing --pretty=format:"%s" | grep -cE "fixes #PM-08" 2>/dev/null || echo 0); test "$pm08_count" -ge 1'
sh -c 'pm09_count=$(git log feat/asset-polishing --pretty=format:"%s" | grep -cE "fixes #PM-09" 2>/dev/null || echo 0); test "$pm09_count" -ge 1'
sh -c 'p2_fixes=$(git log feat/asset-polishing --pretty=format:"%s" | grep -cE "fixes #(PM-(01|12|16|17)|KTV-(14|15|18|19|20))" 2>/dev/null || echo 0); test "$p2_fixes" -ge 6'
grep -qE '__version__\s*=\s*"1\.2\.2' vn_accounting/__init__.py
grep -qE "v1\.2\.x Fix Pass" docs/design-qa-proposals/asset-polishing-personas-review.md
git log feat/asset-polishing -1 | grep -qE "v1\.2\.2 ship"
sh -c 'main_behind=$(git log --oneline main..feat/asset-polishing | wc -l); test "$main_behind" -eq 0'
test -d qa-screenshots/v1.2.x-cleanup
sh -c 'count=$(find qa-screenshots/v1.2.x-cleanup -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 6'

## Live Testing Procedure

### Setup verification (đầu mỗi session)

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing
git status -sb | grep -q "## feat/asset-polishing" || { echo "ERROR"; exit 1; }
wt=$(git rev-parse HEAD)
apps=$(git -C /home/long/long/frappe-bench-dcnet/apps/vn_accounting rev-parse HEAD)
[ "$wt" = "$apps" ] || { cd /home/long/long/frappe-bench-dcnet && git -C apps/vn_accounting checkout --detach feat/asset-polishing; }
# Read findings
sed -n '/^PM-08\|^PM-09\|^PM-01\|^PM-12\|^PM-16\|^PM-17\|^KTV-14\|^KTV-15\|^KTV-18\|^KTV-19\|^KTV-20/,/^$/p' docs/design-qa-proposals/asset-polishing-personas-review.md
```

### Per-fix workflow

1. Read finding (recommendation field)
2. systematic-debugging if it's a state machine / behavior bug (PM-08)
3. Make fix in worktree
4. Bench cycle (migrate / build / clear-cache as appropriate)
5. Browser verify via Playwright MCP, screenshot to `qa-screenshots/v1.2.x-cleanup/{finding-id}.png`
6. Commit atomic with finding ID

### Final ship

After all fixes done:
1. Run all Verification Commands manually
2. Update report Deferred section (be honest — only list ACTUAL deferred)
3. Bump VERSION
4. Final commit
5. FF main → feat tip (local)
6. Push to dcnet for PR #33 update
7. Verify gh pr checks 33 PASS

## Agent Persona

Senior Frappe developer doing P1/P2 cleanup sprint. Familiar with:
- CCDC state machine pattern (this branch's design)
- Frappe workflow / status field transitions in `on_submit`, scheduler hooks
- VN i18n patterns
- Asset Disposal pattern (already merged in v1.0)
- Workspace JSON structure
- Worktree dance per `git-deploy.md`

You always:
- Read finding BEFORE fixing
- For PM-08: use systematic-debugging — don't shortcut to "looks fixed"
- For PM-09: grep ALL files for inconsistent terminology, fix consistently
- Reference finding IDs in commits
- Update report Deferred section ACCURATELY at end (don't leave fixed items listed there — that's the v1.2 mistake we're correcting)
- Verify in browser before claiming complete

You NEVER:
- Skip P1 (PM-08, PM-09)
- Defer P2 without explicit reason in Deferred section
- Touch ERPNext core
- Mark criterion `[x]` without screenshot evidence
- Force-merge to main with broken state
- Push to main directly on dcnet remote

## Model

auto

## Time Budget

- Max hours: 6 (estimated 5-6h: 3h P1 + 2.5h P2 + 0.5h ship)
- Max sessions: 10 (P1 ~4-5, P2 ~3-4, Ship ~1-2)
- Per-session minutes: 30
