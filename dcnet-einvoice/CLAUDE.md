# einvoice — Claude Code Instructions

App-specific instructions for the `einvoice` custom Frappe app. Parent bench instructions live at `/home/long/long/frappe-bench-hts/CLAUDE.md` — read both.

## Project Overview

- **App:** `einvoice` — Multi-provider E-Invoice integration for ERPNext v16
- **Stack:** Frappe v16 + ERPNext v16, Python ≥3.10
- **Pháp lý:** NĐ 123/2020, TT 78/2021 (Vietnam e-invoice regulation)
- **GitHub:** dcnet-cloud organization (Git Flow Guard CI active — see `~/.claude/rules/git-deploy.md`)
- **Branch convention:** `feature/<slug>`, NOT `feat/<slug>` (Git Flow Guard rejects short prefix)
- **Current branch:** `develop` (default)

## Inner package layout

```
apps/einvoice/                    ← repo root, this dir
├── einvoice/                     ← inner Python package (module path = einvoice.einvoice.X)
│   ├── hooks.py                  ← app metadata, scheduler_events, doctype_js
│   ├── patches.txt               ← patch order, namespace einvoice.patches.vX_Y_Z
│   ├── api.py                    ← whitelisted endpoints
│   ├── exceptions.py             ← EInvoiceError hierarchy
│   ├── doctype/
│   │   ├── einvoice_provider/         ← provider config per company
│   │   ├── einvoice_settings/         ← single doctype (defaults, frequency)
│   │   ├── einvoice_inward/           ← inbound invoice staging
│   │   ├── einvoice_inward_item/      ← child table (DSHHDVu line items)
│   │   ├── einvoice_issuance_log/     ← outbound issuance audit
│   │   └── einvoice_sync_log/         ← inbound sync audit
│   ├── providers/
│   │   ├── base.py                    ← BaseProvider abstract class + token cache
│   │   ├── matbao.py                  ← Mắt Bão (production, ~622 LOC)
│   │   ├── viettel.py                 ← stub
│   │   └── misa.py                    ← stub
│   ├── services/
│   │   ├── sync.py                    ← inward sync orchestration
│   │   └── issuance.py                ← outward issue/cancel orchestration
│   ├── tasks/                         ← scheduled jobs (sync_inward_invoices)
│   ├── public/js/                     ← form/list scripts (Sales Invoice, Provider, Inward list)
│   └── workspace/einvoice/            ← workspace fixture
├── patches/v0_X_Y/                    ← actually under inner pkg: einvoice/patches/v0_X_Y/
├── docs/
│   ├── BUSINESS_LOGIC.md              ← traceable rules, referenced by FEATURES.md (§N BL)
│   ├── CODEBASE.md / CODEBASE_DETAIL.md
│   ├── specs/YYYY-MM-DD-<slug>.md     ← design specs (canonical, source of truth)
│   └── plans/YYYY-MM-DD-<slug>/       ← implementation plans (derived from specs)
├── FEATURES.md                        ← Done/In-Progress/Planned matrix
└── .multi-session/                    ← multi-session task files + per-task session-last
```

## Provider System

Three providers via Registry pattern. `EInvoice Provider` DocType has `provider_type` field selecting class:

| Type | Class | Status | Auth |
|---|---|---|---|
| Mắt Bão | `MatbaoProvider` | Production (HTS uses this) | API token (purchase) + username/password (sales). Toggle `enable_inward` / `enable_outward` (separate auth per direction) |
| Viettel | `ViettelProvider` | Stub | TBD |
| MISA | `MisaProvider` | Stub | TBD |

`BaseProvider`:
- Token cache via Redis key `einvoice_token:{provider}:{type}`, TTL 58min (token TTL 1h)
- `_api_call()` with 30s timeout, raises `EInvoiceProviderError` on failure
- 401 mid-bulk → token refresh + retry once before failing the invoice

When adding/extending a provider, follow the existing matbao.py pattern: per-direction auth, response wrapper handling (`{Success, CustomData, Data, ErrorCode}`), field alias map for backward-compat.

## Active Specs / Plans

Currently in flight (as of 2026-05-07):
- **`docs/specs/2026-05-07-matbao-auto-attach-pdf-xml.md`** — auto download PDF+XML on inward sync, attach to EInvoice Inward record. Multi-session task at `.multi-session/tasks/matbao-attach-pdf-xml.md`. Background job + 3-tier retry. NOT YET IMPLEMENTED.
- `docs/specs/2026-05-06-matbao-api-spec-update.md` — parser update for v2 response shape. SHIPPED.
- `docs/specs/2026-03-31-einvoice-rewrite-design.md` — original architecture. REFERENCE.

Always read the most recent spec for the area you're editing before changing code.

## Hooks anchors (`einvoice/hooks.py`)

Important sections to know:
- `doctype_js` — DocType-specific form scripts. Add new entries here when creating `public/js/<doctype>.js`.
- `doctype_list_js` — list view scripts.
- `scheduler_events` — register each method in EXACTLY ONE bucket. Frappe's `sync_jobs` dedupes by `method` and keeps only one Scheduled Job Type per method, overwriting its frequency with whichever bucket is processed last — so the same method under multiple buckets silently collapses to the last one (weekly). `sync_inward` runs under the `*/15` cron only and self-gates cadence via `run_if_frequency_match` + `EInvoice Settings.sync_frequency`.
- `fixtures` — currently only Workspace. EInvoice Provider/Settings rows are NOT exported as fixtures (per-site config).
- `after_install` / `after_uninstall` — `einvoice.einvoice.install.after_install/after_uninstall`.

## Local Dev Workflow

Standard Frappe workflow. From bench root:

```bash
cd /home/long/long/frappe-bench-hts

# After Python edits in einvoice
bench --site hts.localhost migrate          # if DocType JSON changed
bench --site hts.localhost clear-cache      # if hooks.py changed
bench restart                                # if Python under einvoice/ changed (gunicorn cache)

# After JS edits
bench build --app einvoice
bench --site hts.localhost clear-cache

# Console for ad-hoc / test runs
bench --site hts.localhost console
```

**Tests:** Do NOT use `bench run-tests --app einvoice` on dev sites — ERPNext `BootStrapTestData` raises DuplicateEntryError before reaching custom tests. Run via bench console with `unittest.TestLoader().loadTestsFromTestCase(...)` instead. Documented in `~/.claude/rules/multi-session.md`.

**Compile sweep:** `find einvoice -name "*.py" -not -path "*/__pycache__/*" -print0 | xargs -0 python3 -m py_compile`

## Multi-session tasks

Tasks live at `.multi-session/tasks/<slug>.md`. Per-task session-last lives at `.multi-session/session-last-<slug>.md` (slug-scoped per `~/.claude/rules/multi-session.md` rule #9).

Currently configured tasks:
- `matbao-attach-pdf-xml.md` — 9 phases, 4h budget, 8 sessions, 30min/session

Launch: `bash ~/.claude/bin/multi-session.sh --task .multi-session/tasks/<slug>.md --project /home/long/long/frappe-bench-hts/apps/einvoice --hours <N> --session-minutes <N> --max-sessions <N>`

## Common Gotchas

- **Patches.txt order trap.** Patches run BEFORE schema sync. If a patch backfills a column added in the same PR, call `frappe.reload_doc("einvoice", "doctype", "einvoice_inward")` at the top of the patch first. See `~/.claude/rules/frappe.md` "Patches.txt order trap".
- **Vietnamese in DocType JSON.** `name`, `report_name`, fieldnames MUST be English ASCII. UI labels use English source + `translations/vi.csv`. Sidebar item labels are an exception (Vietnamese Unicode allowed). Currently NO `translations/vi.csv` shipped — labels in DocType JSON are mixed VN/EN.
- **Bearer token in error logs.** Never log raw `Authorization` header values to Sync Log / Issuance Log — token leak risk. Truncate / redact.
- **`bench run-tests` is broken on dev sites with sample data** (ERPNext bootstrap dup). Always run tests via bench console.
- **Provider response wrapper.** Mắt Bão wraps payload in `{Success, CustomData, Data, ErrorCode}`. Don't assume top-level fields — always check `Success` and `ErrorCode` first. See `parse_inward_invoice` for alias handling pattern.
- **`MatbaoProvider` size.** ~622 LOC, near 800-line hard cap (`~/.claude/rules/programming.md`). Don't bloat — extract new functionality to sibling files (`matbao_<area>.py`) and import.

## Do NOT

- **Do NOT branch as `feat/...`** — Git Flow Guard CI rejects. Use `feature/<slug>`, `fix/<slug>`, `refactor/<slug>`, `chore/<slug>`, etc.
- **Do NOT register a scheduler method in more than one `scheduler_events` bucket** — Frappe keeps only one Scheduled Job Type per method (last bucket wins). Pick one bucket (the `*/15` cron for sync) and let `run_if_frequency_match` gate the real cadence.
- **Do NOT log secrets** — API tokens, passwords, signed JWTs. Use Frappe Password fieldtype + redact in logs.
- **Do NOT remove `pdf_url` / `xml_url` Data fields** — backward-compat anchor for any existing record without local attachment.
- **Do NOT use bare `python` in Verification Commands** — use `python3` or full venv path (`/home/long/long/frappe-bench-hts/env/bin/python`). See `~/.claude/rules/multi-session.md` rule #24.
- **Do NOT auto-attach files to Purchase Invoice on auto-match** — out of scope, defer to a separate spec (file ownership + permission semantics need design).
- **Do NOT deploy directly to VPS from this dir** — local-only dev. Deploy via `git push` then SSH VPS pull (see parent CLAUDE.md).
