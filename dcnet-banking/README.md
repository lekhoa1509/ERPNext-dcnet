# vn_banking

Vietnamese bank statement import and auto-match for ERPNext v16.

## Quickstart
1. Install: `bench --site <site> install-app vn_banking`
2. Open "Banking VN" workspace → "Bank Reconcile"
3. Pick Bank Account → Upload Statement → done

## Supported banks (v1)
BIDV, MB Bank, Sacombank, PG Bank — the 4 banks DCNet currently uses. Adding another bank = drop a new sample into `tests/fixtures/`, append an entry to `fixtures/bank_statement_format.json`, add a test — see `docs/accounting-requirements/banking/ANALYSIS.md` for the format analysis pattern.

## Architecture
See `docs/superpowers/specs/2026-04-10-vn-banking-v1-design.md` in the parent bench repo.

## Docs
- `docs/USAGE.md` — day-to-day accountant workflow
- `docs/SETTINGS.md` — matcher configuration reference
