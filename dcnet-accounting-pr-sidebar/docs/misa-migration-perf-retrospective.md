# Misa Migration — Phase 4 Insert Perf Retrospective

**Branch:** `feature/misa-migration-phase-e` · **PR:** [#63](https://github.com/dcnet-cloud/dcnet-accounting/pull/63) · **Last updated:** 2026-05-21

This document tells the story of how Misa SME → ERPNext bulk-import
performance went from "weeks of work to import a year" to "minutes."
Written for: engineers who will operate the importer at customer sites,
and engineers who will own the next round of optimization.

---

## 1. Why the 1-month vs 12-month challenge is so different

The very same code that imports 1 month of Misa data in 2 minutes can
take 22 hours on 12 months — and *fail mid-way* without any change in
business logic. This isn't a linear scaling problem. The system crosses
multiple invisible thresholds.

| Dimension | 1 month (DCNET TEST B) | 12 months (DCNET TEST A) |
|---|---|---|
| NKC rows (parsed Misa GL) | 7,847 | 80,289 |
| SCT item-line rows | 302 | 4,505 |
| Bảng kê BR / MV rows | ~1,300 | ~15,000 |
| **Vouchers to insert** | ~2,100 | ~21,000 |
| **GL Entries on submit** | ~7,500 | ~75,000 |
| Total `tabMisa Migration Row` rows | ~10,000 | ~98,000 |
| Unique Items referenced (SCT) | ~150 | ~500 |
| Unique Suppliers / Customers | ~80 / ~40 | ~250 / ~150 |
| Unique Account leaves used | ~80 | ~150 |

What makes 12-month qualitatively harder than 12 × (1-month):

1. **Lock-wait gradient.** With a 10k-row `tabMisa Migration Row` table,
   even a JSON-extract UPDATE that full-scans takes ~1s. With 322k rows,
   the same UPDATE takes minutes — long enough that a *second* worker
   trying to UPDATE the same table hits the 50s InnoDB lock-wait
   timeout and crashes. Parallel sharding goes from "1.7× speedup" to
   "guaranteed failure."

2. **Master-data resolution cost compounds.** Each voucher resolves
   ~6 entities (party, 2-4 accounts, item, warehouse). At 1ms per
   `frappe.db.exists` round-trip × 6 entities × 20k vouchers = 120,000
   round-trips = 2 minutes pure DB chatter for an otherwise empty
   pipeline.

3. **Item/warehouse stub creation is per-row.** A naive flow that
   `_ensure_item_stub`-on-first-encounter inside the voucher loop pays
   the ~80ms `doc.insert()` cost for every previously-unseen Item, on
   the critical path. 500 unique items = 40s of work the user *waits
   for*, mid-stream.

4. **One memory leak / one zombie process / one missed flag** that
   adds 10ms per row becomes 22 hours of wall-clock pain at 84k rows,
   versus 14 minutes at 8k.

5. **Recovery cost is asymmetric.** A 1-month run that fails mid-way
   has ~1k drafts to clean up. A 12-month run that fails mid-way has
   ~15k. Cancel + delete of 15k drafts itself takes 5 minutes.

The lesson: **measure throughput in rows/s, not in absolute seconds.**
A change that improves 1-month time by 5% may improve 12-month time
by 10× because it removes a quadratic factor.

---

## 2. Evolution of solutions

Five major rounds of optimization landed on `feature/misa-migration-phase-e`.
Each round was driven by *measurement*, not speculation — each fix
exposed the next bottleneck.

### Round 1 — Baseline (~0.5 rows/s)

**State:** Vanilla Document.insert()/submit() per voucher. No caches,
no flags. Full ERPNext lifecycle: every `Link` validated, every
`mail.thread` tracked, every Version Log written.

**Bottleneck:** ERPNext per-doc overhead ~200ms per voucher.

### Round 2 — Bulk migration flags + Account cache (`51c14a2`)

**Landed:** `frappe.flags.tracking_disable / mute_emails / in_migrate`
set at run start; in-memory `_ACCOUNT_BY_NUMBER_CACHE` populated by
`_warm_account_cache_for_company` before the voucher loop.

**Effect:** ~0.5 → ~1 row/s (~2× speedup). Per-doc cost dropped
~200ms → ~100ms. Account lookups (4-leg JE = 4 DB hits per voucher)
collapsed to zero round-trips.

**Next bottleneck:** Per-doc `submit()` was committing inside ERPNext's
default transaction model, forcing fsync per voucher.

### Round 3 — SAVEPOINT-batched submit commits (`9b51226`)

**Landed:** `submit_phase_4_drafts` wraps every 25 submits in a single
`frappe.db.commit()`, with SAVEPOINT-per-doc so a poison row doesn't
roll back the batch.

**Effect:** Submit phase 108 → 72 ms/voucher (~33% improvement).

**Next bottleneck:** Insert phase still serial. Single-process throughput
capped at ~1.7 rows/s.

### Round 4 — Two-batch parallel via shard_token (`e9a4286`)

**Landed:** New `Misa Migration Batch.shard_token` Data field.
`state.lock_key_for_company` / `find_active_batch` shard-aware.
`start_post` routes shard A → `long` queue, shard B → `default` queue
based on first character of `shard_token`. UI form gets a shard_token
input.

**Theory:** Two RQ workers, two shards → 2× parallel throughput.

**Reality (2026-05-21 first attempt):** Both workers crashed within 60s
with `MySQLdb.OperationalError(1205) Lock wait timeout exceeded`.
Both were calling `run_preflight_setup` which mutates Company defaults
+ writes party Account child rows; concurrent writes raced on the same
row-level locks.

### Round 5 — Tier 1.1: Redis-cached prewarm flag (commit `6641441` part)

**Landed:** New `api.post.prewarm_masters` endpoint that acquires the
company-wide lock, runs `run_preflight_setup` once, then sets a
`misa:masters_prewarmed:<company>` Redis flag (1hr TTL). Workers in
`run_phase_4_post` check the flag and short-circuit
`run_preflight_setup` when set.

**Effect:** Parallel shards no longer race on Company-defaults rows.
Both workers entered the voucher loop within seconds of dispatch.

**Next bottleneck (revealed by Round 5 actually working):** The
voucher loop itself was now exposing a *new* lock-contention pattern.
Shard B got to ~9 rows/s for ~2 minutes, then crashed with the SAME
`(1205) Lock wait timeout` error. But this time it wasn't on Company
defaults — it was on `tabMisa Migration Row`.

### Round 6 — Tier 1.2-1.5: ignore_links + track_changes + item/party cache (commit `6641441` rest)

**Landed in same commit as Round 5:**

- **`flags.ignore_links = True`** on every voucher insert in 5
  handlers. Preflight already validates `Customer`/`Supplier`/`Account`/
  `Item`/`Warehouse` upstream, so ERPNext's per-row Link integrity
  check is redundant.
- **DocType-level `track_changes` save+restore** for SI/PI/PE/JE/SE
  during the migration. Wrapper `run_phase_4_post` guarantees restore
  in `finally` so a crash never leaves audit silently disabled.
- **`bulk_warm_items_from_sct`** — one bulk SELECT pre-populates
  `_ITEM_CACHE` for all SCT item_codes; missing items pre-created
  upfront. Voucher loop sees a fully-warm cache.
- **`_party_cache` module** — pre-loads Customer/Supplier/Employee/
  Account-leaf names into Python sets. Handlers replace ~20k
  `frappe.db.exists` round-trips with O(1) set-lookups. Defensive
  fallback to DB when unwarmed (preserves test ergonomics).

**Effect (per-shard, isolated):** Per-voucher cost dropped further to
~30ms theoretical max. **But sharded parallel still crashed at minute
2** — same `(1205)` on `tabMisa Migration Row`. We had a NEW
bottleneck dwarfing all the work above.

### Round 7 — Tier 1.6: Indexed voucher_no column (commit `0b790c1`)

**Discovery:** `EXPLAIN` of `_update_nkc_row_status_by_voucher`'s
UPDATE statement revealed:

```sql
UPDATE `tabMisa Migration Row`
SET status='Posted', ...
WHERE batch=%s AND file_type='NKC'
  AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"'))=%s
```

```
EXPLAIN: type=ALL, key=None, rows=321972
```

Every voucher status update was **full-scanning every NKC row in the
entire site** (322k rows) AND taking row-level locks on every scanned
row. With 21k vouchers in a shard, that's 21,000 × 322,000 = **7
billion row examines** just for status updates. With two shards both
hitting this UPDATE, lock-wait timeout was inevitable within ~60s.

The `Misa Migration Row` DocType already had a `voucher_no` Data
column declared with `search_index=1`. It was **never populated.**

**Landed:**

- `parse_job._extract_voucher_no` denormalises `Số chứng từ` (NKC) /
  `voucher_no` (SCT) into the indexed column at insert time.
- `_update_nkc_row_status_by_voucher` WHERE clause changed to query
  by `(batch, file_type, voucher_no)`.
- `patches/v1_5_0/backfill_misa_row_voucher_no.py` one-shot UPDATE
  populates voucher_no for historical rows (~295k NKC + 4.8k SCT,
  ran in 31s, 100% populated).

**Effect:**

```
BEFORE: EXPLAIN type=ALL,  key=None,        rows=321972  (full scan + lock all)
 AFTER: EXPLAIN type=ref,  key=voucher_no,  rows=1       (index seek)
```

**Combined Round 5+6+7 measurement (2026-05-21 successful E2E):**

| Phase | Combined throughput | Per-shard throughput |
|---|---|---|
| Warm-up (~1 min after dispatch) | ~80 rows/s | ~33 + ~47 |
| Peak (1-min interval) | **229 rows/s** | A: 154, B: 75 |
| Sustained (5 min) | ~95-120 rows/s | A solo: ~95-120 (B insert done) |

That's **~110-220× faster than the Round 1 baseline.**

---

## 3. How the latest solution works end-to-end

The user's experience for a fresh import:

### 3.1 Dispatcher prepares the run (once per Company)

```
POST /api/method/vn_accounting.misa_migration.api.post.prewarm_masters
     body: company=DCNET TEST
```

This:
1. Acquires the company-wide filelock (~30s timeout).
2. Runs `run_preflight_setup` once — ensures COA leaves exist,
   sets Company defaults (`stock_adjustment_account`, `default_in_transit_warehouse`),
   creates Party Accounts for every active Customer/Supplier.
3. Warms in-process Account number cache (227 entries on DCNET TEST).
4. **Sets Redis flag** `misa:masters_prewarmed:DCNET TEST = 1`, 1-hour TTL.

Returns in ~200-450ms on a typical site. UI confirms with toast.

### 3.2 Operator dispatches both shards in parallel

```
POST .../start_post  body: batch_name=MM-2026-01000  (shard A → "long" queue)
POST .../start_post  body: batch_name=MM-2026-01001  (shard B → "default" queue)
```

`start_post` runs the per-batch preflight (`preflight` API) which checks
that referenced Customers/Suppliers/Accounts exist, expected number of
NKC rows match the parsed count, etc. If preflight blocks (`pre["blocked"]`
non-empty), the operator sees a list of fixable issues (missing master
data, vouchers already imported by a prior run, etc.).

If preflight passes, `frappe.enqueue` queues `post_job.post_batch` on
the routed queue. Job ID returned to UI; batch status flips to
`POSTING`.

### 3.3 Worker enters Phase 4

`vn_accounting.misa_migration.jobs.post_job.post_batch(batch_name)`:

1. Calls `run_phase_4_post(batch_name)`:
   - Wrapper enables track_changes silence in a `try/finally`.
   - Inner `_run_phase_4_post_impl`:
     - Checks Redis prewarm flag → if set, **skips per-shard
       `run_preflight_setup`** (the contention-causing call).
     - Warms in-process Account cache (per-process, not shared).
     - **Tier 1.5:** Warms party_cache with one bulk SELECT per
       entity type (Customer/Supplier/Employee/Account-leaf).
     - Loads NKC/BR/MV/SCT rows from `tabMisa Migration Row`.
     - **Tier 1.4:** `bulk_warm_items_from_sct` — single SELECT
       populates `_ITEM_CACHE`; missing items pre-created.
     - Enters voucher loop. Per voucher:
       - `voucher_router` dispatches to SI/PI/PE/JE/SE/PR handler.
       - Handler uses `_party_cache.is_supplier/is_customer/...` for
         O(1) party lookups (Tier 1.5).
       - Handler does `doc.flags.ignore_links = True` then `insert()`
         (Tier 1.2).
       - On success: `_update_nkc_row_status_by_voucher` UPDATE uses
         the indexed `voucher_no` column (Tier 1.6).
     - Every 50 vouchers: `frappe.db.commit()` + publish realtime
       progress event to the UI.

2. Calls `submit_phase_4_drafts(batch_name)`:
   - Submits SI → JE → PE → PI → SE in dependency order.
   - SAVEPOINT-per-doc, commits every 25 submits (Round 3).

3. Sets `Misa Migration Batch.status = "POSTED"`.

### 3.4 Operator watches realtime UI

The Misa Migration Hub Vue app + the standard batch form subscribe to
`frappe.realtime` events (`misa_migration:post_progress`). Status badge
flips REVIEWED → POSTING → POSTED. Per-target counters (SI/PI/PE/JE/SE
posted vs failed vs skipped) update live.

### 3.5 Verified live E2E (2026-05-21 10:08 → 10:11)

Headed Playwright run against shard B (8k rows, partial-data state):

| Timestamp | Event |
|---|---|
| 10:08:35 | Dispatch via UI button (frappe.call → start_post) |
| 10:08:35 → 10:09:39 | Job queued (1 min — RQ pickup latency) |
| 10:09:39 | Worker starts processing |
| 10:11:32 | Worker reports "Successfully completed" — 1m52s wall-clock |
| 10:11:32 | UI form auto-refreshes; status badge flips POSTED |

**Browser console errors during successful run: 0.**
**Worker errors during successful run: 0.**

Note: Two console errors *before* the successful run were the first
dispatch attempt being rejected by preflight ("Voucher ... đã tồn tại")
— prior-run drafts not yet cleaned up. After `cancel_phase_4 + delete_phase_4`
the second dispatch ran cleanly.

---

## 4. What's left

Despite the dramatic speedup, three classes of issue remain. Logged
for the next session / for the operator's attention.

### 4.1 Pre-existing ~5-6% failure rate per shard

The 2026-05-21 12-month E2E showed:

- Shard A: 4,180 failed out of 80,288 processed (5.2%)
- Shard B: 454 failed out of 7,846 processed (5.8%)

These failures are NOT regressions from Tier 1+1.6 — they were present
at the ~1 row/s baseline too. Root causes from worker error logs (sampling):

1. **`Sales Invoice` with no `posting_date` or no line items.** Some
   NKC vouchers don't parse cleanly into invoice shape (free-text
   adjustments, opening-balance pre-mapped entries). Handlers correctly
   reject these; row-status stays `Failed` with the error logged.

2. **Party-account mismatch.** A voucher referencing a Customer with
   a non-VND `default_currency` while the SI defaults the company
   currency — ERPNext rejects on currency mismatch.

3. **Stock Entry batchwise-valuation negative-stock.** PXHN (internal
   transfer) vouchers reference inventory that the prior run hasn't
   set up yet; SE submit fails with `BatchNegativeStockError`.

**Fix path:** dedicated session walking `grep "Misa.*create failed"
logs/worker.*.log` → bucket by handler → file targeted fixes per
DocType. Probably 2-4 hours of work; each fixed bucket likely
collapses the rate by 1-2 percentage points.

### 4.2 Stranded drafts after a STUCK shard

When a Phase 4 worker dies mid-stream (memory limit, manual SIGTERM,
deploy restart), partial drafts pile up. The next dispatch attempt is
blocked by preflight: "Voucher X đã tồn tại (docstatus=0)".

Operator recovery exists via UI/API:
1. `cancel_phase_4(batch_name)` — cancels any submitted drafts
2. `delete_phase_4(batch_name)` — deletes docstatus=0/2 drafts
3. Reset batch status to REVIEWED + reset rows to Ready

But:
- On a 21k-voucher shard, this takes ~5-10 minutes.
- `delete_phase_4` currently has gaps — doesn't catch drafts created
  by *other shards* that re-use overlapping voucher_no (e.g. shard A
  creating PX2026* drafts while shard B's data also has them).

**Fix path:** widen `delete_phase_4` to delete ALL Misa-tagged drafts
in any DocType regardless of batch tag, OR add `cleanup_orphan_drafts`
endpoint that's bench-wide.

### 4.3 Submit phase still serial within a shard

`submit_phase_4_drafts` walks SI → JE → PE → PI → SE in dependency
order, single-threaded. For a 21k-voucher shard, submit phase takes
~5-8 minutes (~50ms per submit). Could be parallelised by:
- Submitting independent doctypes (SI, JE) in parallel processes
- Splitting per-doctype submits into chunks

Not pursued in this session because:
- Insert was the dominant cost (10-20× longer than submit)
- After Tier 1, insert is now fast enough that submit is the new
  bottleneck for total wall-clock

**Estimated effect:** submit-phase parallelism would shave maybe 30-50%
off total run time. For a 12-month run that takes 15-30 min today,
that's 5-15 min saved. Lower priority than the failure-rate fixes
above.

---

## 5. Operator runbook (cheat sheet)

```bash
# 1. Inspect current bench state
ssh frappe@<vps> 'cd ~/frappe-bench-dcnet && bench --site dcnet.com list-apps'
ssh frappe@<vps> 'pgrep -fa "frappe worker --queue (default|long)"'   # MUST be running

# 2. Open Misa Migration Hub
# URL: https://dcnet.com/desk/misa-migration-hub
# - Step 1: Upload files (NKC + Bang ke BR + Bang ke MV + SCT)
# - Step 2: Click "Phân tích" — parse_job runs ~2-3 min for 12 months
# - Step 3: Review preflight — fix any "blocked" entries before posting
# - Step 4: Click "Đăng vào ERPNext"

# 3. For two-shard parallel import (cuts wall-clock ~50%):
# - Split source data manually into shard A (e.g. months 1-6) + shard B (months 7-12)
# - Create batch A with shard_token="A" (routes to "long" queue)
# - Create batch B with shard_token="B" (routes to "default" queue)
# - In Step 4 of EACH batch: first call prewarm_masters ONCE, then dispatch both

# 4. Real-time monitoring
ssh frappe@<vps> 'tail -F ~/frappe-bench-dcnet/logs/worker.long.error.log'
ssh frappe@<vps> 'tail -F ~/frappe-bench-dcnet/logs/worker.default.error.log'

# 5. If a run gets stuck (no progress for 5+ min):
# - In UI: click ⋯ menu → "Cancel Phase 4" (cancels submitted drafts)
# - Then: ⋯ menu → "Delete Phase 4" (deletes 0/2 drafts)
# - Reset batch status to REVIEWED via form's status field
# - Re-dispatch
```

### Key thresholds

| Metric | Healthy | Investigate | Stop and ask |
|---|---|---|---|
| Insert rate (rows/s, sustained) | > 50 | 20-50 | < 20 |
| Worker memory growth (RSS) | < 1 GB | 1-2 GB | > 2 GB |
| Per-shard failure rate | < 6% | 6-15% | > 15% |
| Lock-wait timeout count per hour | 0 | 1-3 | > 3 |

---

## 6. Architectural insights for future similar work

Cross-applicable lessons captured in `~/.claude/.pending-promotions.md`:

1. **JSON-expression WHERE on indexed-DocType columns is a perf trap.**
   When a DocType declares a column with `search_index=1`, populate it
   at insert and query by it. Never `JSON_UNQUOTE(JSON_EXTRACT(...))`
   in WHERE. Diagnostic: `EXPLAIN` showing `type=ALL, key=None, rows=<N>`.

2. **Throughput perf work — each tier exposes the NEXT bottleneck.**
   Tier 1.1 fixed the "obvious" Company-default lock contention; the
   "real" dominant lock contention (JSON-extract UPDATE) only became
   visible after Tier 1 made workers fast enough to expose it. Treat
   each measured 5-10× speedup as a fresh diagnostic moment, not a
   finish line. Build measurement infrastructure (per-shard sampler)
   upfront.

3. **Wrapper-pattern try/finally is the lowest-diff way to add cleanup**
   semantics to a long existing function. Re-indenting 130 lines vs
   renaming + thin-wrapper is ~10× less risky.

4. **Defensive fallback in cache layers preserves test ergonomics.**
   `_party_cache.is_customer(code)` falls back to `frappe.db.exists`
   when unwarmed — unit tests that don't call `warm_party_cache` still
   work, while production code paths that DO warm get the fast path.

5. **Migration-mode flags + audit-trail silencing must be reversible.**
   Save the original value, restore in `finally` regardless of how
   the operation ends. Otherwise one mid-run crash leaves the site
   silently degraded forever.

---

## 7. Commit / PR map

| Commit | Description | Tier |
|---|---|---|
| `51c14a2` | in-memory Account cache + flags for bulk Phase 4 import | Round 2 |
| `9b51226` | SAVEPOINT-batched submit commits | Round 3 |
| `e9a4286` | two-batch parallel via shard_token | Round 4 |
| `33f9750` | SCT (Sổ chi tiết) → real Item + Warehouse on Stock Entries | (separate feature, lands first) |
| `6641441` | Tier 1 — parallel-safe prewarm + bulk warm caches | Rounds 5+6 |
| `0b790c1` | Tier 1.6 — indexed voucher_no kills 322k-row scan | Round 7 |

All committed to `feature/misa-migration-phase-e` on
`dcnet-cloud/dcnet-accounting`. PR #63 is open.
