---
name: dcnet-start
description: |
  Master orchestrator for DCNET Flow development workflow.
  Guides user through complete checklist from task start to done,
  coordinating DCNET custom skills and superpowers skills at each phase.

  Use when:
  - User says "/dcnet-start {STT}" or "/dcnet-start {feature name}"
  - User wants to start working on a module or feature end-to-end
  - User says "bat dau lam module X", "start module X", "lam chuc nang X"
  - User wants a guided workflow from requirements to completion
  - User asks "lam gi tiep", "buoc tiep theo", "next step"

  Triggers: "dcnet-start", "bat dau lam", "start module", "start feature",
  "workflow", "lam tu dau", "quy trinh", "checklist", "lam gi tiep"
---

# /dcnet-start — Master Workflow Orchestrator

> "Mot quy trinh, tu A den Z, khong bo sot buoc nao."

Orchestrate the full development lifecycle by coordinating DCNET custom skills
and superpowers skills. Each phase has a checklist — ask user to confirm
before moving to the next phase.

## Usage

```
/dcnet-start 07                    # Start by STT number
/dcnet-start kho-hang              # Start by slug
/dcnet-start 07 --resume           # Resume from last checkpoint
/dcnet-start 07 --phase code       # Jump to specific phase
/dcnet-start 07 --status           # Show current progress only
```

## Phase Router

```
Argument received
│
├─► Has STT or slug ──► Lookup in source-mapping (dcnet-module/references/source-mapping.md)
│   │
│   ├─► --status  ──► Show STATUS DASHBOARD only (no action)
│   ├─► --resume  ──► Read tracker file, resume from last incomplete phase
│   ├─► --phase X ──► Jump to phase X (validate prerequisites met)
│   └─► (default) ──► Start PHASE 0: Assessment
│
└─► No argument ──► Ask: "Ban muon lam module nao? (VD: /dcnet-start 07)"
```

## Tracker File

Create/update `docs/modules/{STT}-{slug}/WORKFLOW_TRACKER.md` to persist progress:

```markdown
# Workflow Tracker: {STT} - {Module Name}

> Started: {date} | Last updated: {date}
> Current phase: {phase_number} - {phase_name}

## Checklist

### Phase 0: Assessment
- [ ] Read PROGRESS.md
- [ ] Lookup source-mapping
- [ ] Check existing docs in docs/modules/{STT}-{slug}/
- [ ] Check existing code in dcnet_apps/

### Phase 1: Clarify Requirements
- [ ] Read spec files (FEATURE/ERP/IMPORT_SPECIFICATION)
- [ ] Identify unclear requirements
- [ ] Run /dcnet-interview if needed
- [ ] All requirements clear or documented in CLARIFY.md

### Phase 2: Documentation
- [ ] SPEC_MAPPING.md created (/dcnet-module)
- [ ] CLARIFY.md created (if needed)
- [ ] CUSTOM_REQUIREMENTS.md created (if EXT/NEW features)
- [ ] BA_ANALYSIS.md created (/dcnet-ba) — if complex module
- [ ] Mockup created (/dcnet-mockup) — if custom UI needed

### Phase 3: Planning
- [ ] Execution plan written (superpowers:writing-plans)
- [ ] Plan saved to docs/plans/ or docs/modules/{STT}-{slug}/
- [ ] Tasks broken down with dependencies identified
- [ ] Git branch created: feature/{STT}-{slug}

### Phase 4: Implementation
- [ ] Git worktree/branch ready (superpowers:using-git-worktrees)
- [ ] Tests written first (superpowers:test-driven-development)
- [ ] Code implemented (superpowers:executing-plans)
- [ ] dcnet_quality validation passed (auto-trigger)
- [ ] All tests passing in Docker container

### Phase 5: Review & Verify
- [ ] Code review passed (superpowers:requesting-code-review)
- [ ] Review feedback addressed (superpowers:receiving-code-review)
- [ ] Final verification (superpowers:verification-before-completion)
- [ ] Tests pass, no regressions

### Phase 6: Ship & Document
- [ ] Branch finished (superpowers:finishing-a-development-branch)
- [ ] PR created or merged
- [ ] User guide created (/dcnet-guide) — if needed
- [ ] PROGRESS.md updated
- [ ] WORKFLOW_TRACKER.md marked complete
```

---

## Phase 0: Assessment

**Goal:** Understand current state before doing anything.

**Steps:**

1. Read `docs/modules/PROGRESS.md` — check module status
2. Lookup STT in `dcnet-module/references/source-mapping.md` — get slug, source, milestone
3. Check existing docs: `docs/modules/{STT}-{slug}/`
4. Check existing code: `dcnet_apps/dcnet_apps/{module}/`
5. Check git branches: any existing `feature/{STT}-*` branch?
6. Read SPEC_MAPPING.md (if exists) → extract feature list with tags
7. Read README.md (if exists) → extract related modules

**Output to user — 3 sections:**

### Section 1: Module Info + State

```
╔══════════════════════════════════════════════════╗
║  DCNET START: {STT} - {Module Name}             ║
╠══════════════════════════════════════════════════╣
║  Milestone:  {T3/T4/T5/T6/T7/T8}               ║
║  Cong ty:    {TM + NM / TM only / NM only}      ║
║  Source:     {spec file} Section {X}             ║
║  Deadline:   {date}                              ║
╠══════════════════════════════════════════════════╣
║  CURRENT STATE:                                  ║
║  Docs:       {none / partial / done}             ║
║  Code:       {none / partial / done}             ║
║  Branch:     {none / feature/XX-slug}            ║
║  Tests:      {none / partial / passing}          ║
╠══════════════════════════════════════════════════╣
║  RECOMMENDED START: Phase {N} - {name}           ║
╚══════════════════════════════════════════════════╝
```

### Section 2: Feature List

Read SPEC_MAPPING.md and list ALL features with their tags. Also cross-reference
`docs/feature/ERPNEXT_COVERAGE_ANALYSIS.md` to add ERPNext coverage status.

```
## Danh sach chuc nang ({N} features)

| # | Spec | Chuc nang | Tag | ERPNext | Coverage | Effort |
|---|------|-----------|-----|---------|----------|--------|
| 1 | 3.1.1 | Uu dai NCC | CFG | Pricing Rule | ⚠️ Can build | 1d |
| 2 | 3.1.2 | Import hinh anh SP | EXT | File Attach + custom | ⚠️ Can build | 3d |
| 3 | 3.1.3 | Tao PO | EXT | Purchase Order | ✅ Co san | 1d |
| ... | ... | ... | ... | ... | ... | ... |

Tong: USE {n} | CFG {n} | EXT {n} | NEW {n} | REF {n}
ERPNext co san: {n} | Can build moi: {n}
Effort uoc tinh: ~{N} ngay
```

**Coverage column values:**
- `✅ Co san` — Feature listed in ERPNEXT_COVERAGE_ANALYSIS.md "ERPNext co san" section
- `⚠️ Can build` — Feature listed in "Can build moi" section (custom development needed)
- `—` — REF features (belong to another module)

**How to extract:**
1. Parse each `### X.X.X.` heading in SPEC_MAPPING.md → spec number, feature name, Tag, ERPNext, Effort
2. Read `docs/feature/ERPNEXT_COVERAGE_ANALYSIS.md` → find matching Spec ID (e.g., ERP-3.Feature 3)
3. If feature appears in "ERPNext co san" tables → `✅ Co san`
4. If feature appears in "Can build moi" tables (e.g., "Mua hang nang cao") → `⚠️ Can build`
5. Present as a compact table so user sees the full scope at a glance

### Section 3: Related Modules

Read README.md "Lien ket module" section AND cross-reference source-mapping.md
to show related modules with their current status from PROGRESS.md.

```
## Module lien quan

| STT | Module | Quan he | Status (docs/code) |
|-----|--------|---------|---------------------|
| 03 | San pham | Item master data | docs:done / code:none |
| 04 | NCC | Supplier master data | docs:done / code:none |
| 07 | Kho hang | Purchase Receipt -> Stock | docs:partial / code:none |
| 24 | KT Mua hang | Purchase Invoice -> GL | docs:none / code:none |
| 26 | KT Cong no | Accounts Payable | docs:none / code:none |
```

**How to extract:** Parse README.md table under "Lien ket module" or "Module lien quan".
For each related STT, look up its status in PROGRESS.md.
This helps user see dependencies and what needs to be done first.

---

**Ask:** "Thong tin dung khong? Bat dau Phase {N}?"

Create WORKFLOW_TRACKER.md and check off Phase 0 items.

---

## Phase 1: Clarify Requirements

**Goal:** Ensure all requirements are understood before writing docs or code.

**Steps:**

1. Read relevant spec files silently:
   - `docs/feature/FEATURE_SPECIFICATION.md`
   - `docs/feature/ERP_SPECIFICATION.md`
   - `docs/feature/IMPORT_PROCESS_SPECIFICATION.md`
2. Summarize features found for this module (list with spec numbers)
3. Identify unclear/ambiguous requirements
4. If unclear items exist → invoke `/dcnet-interview` (INTERVIEW mode)
5. If already clear → ask user to confirm and move on

**Ask:** "Day la {N} features trong spec. Co diem nao can clarify voi khach truoc khi lam khong?"

**Skip condition:** If SPEC_MAPPING.md already exists and is up-to-date → skip to Phase 2 check.

**Update tracker** when done.

---

## Phase 2: Documentation

**Goal:** Create all required docs for the module.

**Steps — execute sequentially, ask before each:**

1. **SPEC_MAPPING.md** — "Can tao SPEC_MAPPING? Chay /dcnet-module {STT}?"
   - If yes → invoke `/dcnet-module {STT}`
   - If exists → ask if need update: `/dcnet-module {STT} --update`

2. **BA Analysis** — "Module nay co phuc tap khong? Can phan tich BPMN/gap?"
   - Complex module (kho, ban hang, ke toan, trade-in) → invoke `/dcnet-ba {STT}`
   - Simple module (chi nhanh, nhan vien) → skip

3. **Mockup** — "Can tao UI mockup cho khach xem truoc?"
   - If module has custom UI (EXT/NEW features) → invoke `/dcnet-mockup {STT}`
   - If mostly ERPNext standard → skip

**Skip condition:** If all docs already exist → show checklist status, ask to proceed to Phase 3.

**Update tracker** after each sub-step.

---

## Phase 3: Planning

**Goal:** Create detailed execution plan before writing code.

**Steps:**

1. Read completed docs: SPEC_MAPPING, BA_ANALYSIS, CUSTOM_REQUIREMENTS
2. Invoke `superpowers:writing-plans`
   - Input: all docs created in Phase 2
   - Output: execution plan in `docs/plans/` or `docs/modules/{STT}-{slug}/`
3. After plan is written, ask: "Plan nay ok chua? Can dieu chinh gi?"
4. Create git branch:
   ```
   git checkout develop && git pull origin develop
   git checkout -b feature/{STT}-{slug}
   ```
   Or invoke `superpowers:using-git-worktrees` for isolated work.

**Ask before branching:** "Tao branch feature/{STT}-{slug} tu develop?"

**Update tracker** when done.

---

## Phase 4: Implementation

**Goal:** Write code following the plan with quality guardrails.

**Steps:**

1. Invoke `superpowers:test-driven-development`
   - Write tests FIRST based on plan and spec
   - `dcnet_quality` auto-triggers to validate test patterns

2. Invoke `superpowers:executing-plans`
   - Follow plan step by step
   - At each step, `dcnet_quality` 28 skills auto-validate:
     - syntax/* for correct patterns
     - core/* for DB, permissions, API
     - impl/* for workflow correctness
     - errors/* for error handling
   - If multiple independent tasks → `superpowers:dispatching-parallel-agents`

3. Run tests in Docker:
   ```
   docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app dcnet_apps --module {module} -v"
   ```

4. If tests fail → invoke `superpowers:systematic-debugging`

**Ask at each milestone:** "Step {N}/{total} xong. Ket qua: {summary}. Tiep tuc?"

**If stuck:** Suggest `/dcnet-interview` (UNSTUCK mode) with 5 lateral thinking personas.

**Update tracker** after each significant step.

---

## Phase 5: Review & Verify

**Goal:** Ensure code quality before shipping.

**Steps:**

1. Invoke `superpowers:requesting-code-review`
   - `dcnet_quality/agents/erpnext-code-validator` runs alongside
   - Report: CRITICAL / WARNING / SUGGESTION

2. If feedback received → invoke `superpowers:receiving-code-review`
   - Verify feedback technically before implementing
   - Do NOT blind-fix

3. Invoke `superpowers:verification-before-completion`
   - Run ALL tests in Docker
   - Run `bench migrate` to verify no schema issues
   - Confirm no regressions
   - Show evidence (test output) before claiming done

**Ask:** "Review xong. {N} issues found ({critical}/{warning}/{suggestion}). Fix truoc khi ship?"

**Update tracker** when all checks pass.

---

## Phase 6: Ship & Document

**Goal:** Merge code and create user documentation.

**Steps:**

1. Invoke `superpowers:finishing-a-development-branch`
   - Options: merge to develop / create PR / cleanup
   - Ask user which option

2. If PR → create with `gh pr create`:
   - Title: `feat({STT}): {module description}`
   - Reference spec sections and plan

3. Ask: "Can tao user guide tieng Viet cho module nay?"
   - If yes → invoke `/dcnet-guide {STT}`

4. Update `docs/modules/PROGRESS.md`:
   - Set Code = `done`
   - Set all doc columns to current status

5. Mark WORKFLOW_TRACKER.md as complete:
   ```
   > Status: COMPLETED
   > Completed: {date}
   ```

**Final output:**

```
╔══════════════════════════════════════════════════╗
║  DONE: {STT} - {Module Name}                    ║
╠══════════════════════════════════════════════════╣
║  Docs:    SPEC_MAPPING + BA + Mockup + Guide     ║
║  Code:    dcnet_apps/{module}/ ({N} files)        ║
║  Tests:   {N} tests passing                      ║
║  Branch:  feature/{STT}-{slug} → {merged/PR#N}   ║
║  Time:    Started {date} → Completed {date}      ║
╚══════════════════════════════════════════════════╝
```

---

## Status Dashboard (--status)

When called with `--status`, show overview without taking action.
Include ALL 3 sections: phase progress + feature list + related modules.

```
╔══════════════════════════════════════════════════════════════╗
║  DCNET START STATUS: {STT} - {Module Name}                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Phase 0: Assessment          [====] DONE                    ║
║  Phase 1: Clarify             [====] DONE                    ║
║  Phase 2: Documentation       [==  ] 3/5 items               ║
║    ✓ SPEC_MAPPING  ✓ CLARIFY  ✗ BA  ✗ Mockup  — CR          ║
║  Phase 3: Planning            [    ] NOT STARTED              ║
║  Phase 4: Implementation      [    ] NOT STARTED              ║
║  Phase 5: Review & Verify     [    ] NOT STARTED              ║
║  Phase 6: Ship & Document     [    ] NOT STARTED              ║
║                                                              ║
║  ► Next action: Phase 2 — Run /dcnet-ba {STT}                ║
╚══════════════════════════════════════════════════════════════╝
```

Then show Section 2 (Feature List) and Section 3 (Related Modules) as defined in Phase 0.

---

## Decision Rules

| Situation | Action |
|-----------|--------|
| Module docs exist, code = none | Start at Phase 3 (Planning) |
| Module docs = none | Start at Phase 1 (Clarify) |
| Code exists, tests failing | Start at Phase 4 (fix + debug) |
| Code exists, tests passing, no PR | Start at Phase 5 (Review) |
| PR exists, not merged | Start at Phase 6 (Ship) |
| Everything done | Show completion dashboard |
| User says "bi ket" / "stuck" | Trigger /dcnet-interview UNSTUCK mode |
| User says "lam gi tiep" | Read tracker, show next incomplete item |

## Important Rules

- **ALWAYS ask before invoking a skill** — never auto-run without user confirmation
- **Update WORKFLOW_TRACKER.md** after completing each phase/sub-step
- **Show progress** after each step: "Phase {N}, step {M}/{total}: {description}"
- **One phase at a time** — do not jump ahead or batch multiple phases
- **Respect existing work** — if docs/code exist, acknowledge and build on them
- **Follow CLAUDE.md rules** — no features outside specs, no assumptions
