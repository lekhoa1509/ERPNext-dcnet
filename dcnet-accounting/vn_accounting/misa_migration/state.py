"""Misa Migration state machine + per-company locking.

Spec §8.6: 8-state lifecycle plus STUCK side-state. Transitions are
strictly directional, guarded by ALLOWED_TRANSITIONS. Each transition
acquires a per-company lock (frappe.db.get_lock) to enforce "1 active
batch per company".

Usage:

    from vn_accounting.misa_migration.state import transition, lock_for_batch

    doc = frappe.get_doc("Misa Migration Batch", batch_name)
    transition(doc, "PARSED", reason="parser_job_finished")  # raises if illegal

    with lock_for_batch(doc):
        # mutate doc safely; lock released on exit
        ...
"""

from __future__ import annotations

import contextlib
from typing import Iterator

import frappe
from frappe import _
from frappe.utils.file_lock import LockTimeoutError
from frappe.utils.synchronization import filelock

# ----------------------------------------------------------------- constants

DRAFT = "DRAFT"
UPLOADED = "UPLOADED"
PARSED = "PARSED"
REVIEWED = "REVIEWED"
POSTING = "POSTING"
POSTED = "POSTED"
REVERSING = "REVERSING"
REVERSED = "REVERSED"
STUCK = "STUCK"

ALL_STATUSES = (DRAFT, UPLOADED, PARSED, REVIEWED, POSTING, POSTED, REVERSING, REVERSED, STUCK)

# Edges of the state graph.  Format: {from_status: set_of_allowed_to_statuses}.
# STUCK is reachable from any in-progress state via watchdog.  Recovery from
# STUCK is back to the prior state (encoded as STUCK → DRAFT/UPLOADED/PARSED/
# REVIEWED so user can choose resume target after fixing root cause).
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    DRAFT:     {UPLOADED, STUCK},
    UPLOADED:  {DRAFT, PARSED, STUCK},          # DRAFT = user removes last file
    PARSED:    {REVIEWED, STUCK},
    REVIEWED:  {POSTING, PARSED, STUCK},        # PARSED = user wants to re-review
    POSTING:   {POSTED, STUCK},                  # POSTED on success; STUCK on watchdog
    POSTED:    {REVERSING},
    REVERSING: {REVERSED, STUCK},
    REVERSED:  set(),                            # terminal
    STUCK:     {DRAFT, UPLOADED, PARSED, REVIEWED},
}

# Statuses where the batch is "alive" — counted by _check_active_batch.
# Used to enforce "1 active batch per company".
ACTIVE_STATUSES = (DRAFT, UPLOADED, PARSED, REVIEWED, POSTING, REVERSING)

# Statuses where status field implies a long-running job is in flight.
# Watchdog monitors these for idle.
RUNNING_STATUSES = (POSTING, REVERSING)


# ------------------------------------------------------------------ helpers

def lock_key_for_company(company: str, shard_token: str | None = None) -> str:
    """File-safe lock name (filelock writes <site>/locks/<name>.lock).

    When ``shard_token`` is empty / None, the lock name is the legacy
    ``misa_migration_<company>`` — only one such batch can hold the lock
    per Company. When ``shard_token`` is non-empty, the lock name becomes
    ``misa_migration_<company>__shard_<token>`` so different shards on the
    same Company can run concurrently without blocking each other.
    """
    safe = frappe.scrub(company)
    if shard_token:
        safe_token = frappe.scrub(str(shard_token))
        return f"misa_migration_{safe}__shard_{safe_token}"
    return f"misa_migration_{safe}"


@contextlib.contextmanager
def lock_for_company(
    company: str, timeout: int = 5, shard_token: str | None = None,
) -> Iterator[None]:
    """Acquire per-(company, shard_token) file lock.

    Uses frappe.utils.synchronization.filelock (filelock package backed).
    Lock file at sites/<site>/locks/misa_migration_<company>[__shard_<t>].lock.

    Args:
        company: Company name.
        timeout: Seconds to wait before raising.
        shard_token: Optional shard label. Empty / None = legacy single-batch
            lock (one active batch per company). Non-empty = per-shard lock
            (multiple shards on same company can run concurrently).

    Raises:
        frappe.ValidationError if lock cannot be acquired within timeout.
    """
    name = lock_key_for_company(company, shard_token=shard_token)
    try:
        with filelock(name, timeout=timeout):
            yield
    except LockTimeoutError:
        if shard_token:
            frappe.throw(
                _("Đang có thao tác khác chạy trên Company {0} (shard {1}). Thử lại sau.").format(
                    company, shard_token,
                )
            )
        else:
            frappe.throw(
                _("Đang có thao tác khác chạy trên Company {0}. Thử lại sau.").format(company)
            )


@contextlib.contextmanager
def lock_for_batch(doc, timeout: int = 5) -> Iterator[None]:
    """Convenience wrapper — locks by doc.company + doc.shard_token.

    If the doc has no ``shard_token`` field or it's empty, falls back to
    the legacy per-company lock so existing batches keep their exclusive
    semantics.
    """
    shard_token = (getattr(doc, "shard_token", "") or "").strip() or None
    with lock_for_company(doc.company, timeout=timeout, shard_token=shard_token):
        yield


def transition(doc, to_status: str, reason: str | None = None, audit_user_remark: bool = True) -> None:
    """Validate + apply a state transition on a Misa Migration Batch.

    Args:
        doc: Misa Migration Batch document (in-memory).
        to_status: Target status (must be in ALL_STATUSES).
        reason: Free-text reason added to notes / audit log.
        audit_user_remark: Whether to append to doc.notes for human audit.

    Raises:
        frappe.ValidationError if (from, to) not in ALLOWED_TRANSITIONS.

    NOTE: Caller is responsible for doc.save() / frappe.db.commit().  This
    function only mutates the in-memory doc + adds timestamp fields.
    """
    if to_status not in ALL_STATUSES:
        frappe.throw(_("Trạng thái không hợp lệ: {0}").format(to_status))

    current = doc.status or DRAFT
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if to_status not in allowed:
        frappe.throw(
            _("Không thể chuyển từ {0} sang {1}. Các trạng thái cho phép: {2}").format(
                current, to_status, ", ".join(sorted(allowed)) or "(không có — đây là trạng thái kết thúc)"
            )
        )

    doc.status = to_status
    now = frappe.utils.now_datetime()
    if to_status == UPLOADED and not doc.started_on:
        doc.started_on = now
    elif to_status == PARSED:
        doc.parsed_on = now
    elif to_status == POSTED:
        doc.posted_on = now
    elif to_status == REVERSED:
        doc.reversed_on = now
    elif to_status == STUCK:
        doc.stuck_at = now

    if audit_user_remark:
        stamp = frappe.utils.now_datetime().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{stamp}] {current} → {to_status}"
        if reason:
            line += f" ({reason})"
        doc.notes = ((doc.notes or "") + "\n" + line).strip()


def can_transition(from_status: str, to_status: str) -> bool:
    """Pure check used by UI to enable/disable buttons before round-trip."""
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set())


def find_active_batch(
    company: str, shard_token: str | None = None,
) -> str | None:
    """Return the active batch name for a (company, shard_token) slot, or None.

    Two-batch parallel semantics:
    - ``shard_token=None`` (or empty): look for any active batch with EMPTY
      shard_token. Used by the legacy single-batch lock path — finding one
      means a non-sharded batch is in progress and a new non-sharded batch
      should be rejected.
    - ``shard_token="<value>"``: look for an active batch with that exact
      shard_token. Two batches with different non-empty shard_tokens for
      the same Company do NOT collide — each occupies its own shard slot.

    NOTE: this is used as an admission check at batch-creation time. The
    actual run-time concurrency guard is the per-(company, shard_token)
    file lock acquired via ``lock_for_batch`` / ``lock_for_company``.
    """
    filters: dict = {"company": company, "status": ["in", ACTIVE_STATUSES]}
    if shard_token:
        filters["shard_token"] = shard_token
    else:
        # Empty shard_token: must look for OTHER empty-shard active batches.
        # MariaDB stores empty Data fields as empty string "" (NOT NULL).
        filters["shard_token"] = ["in", ["", None]]
    return frappe.db.get_value("Misa Migration Batch", filters, "name")


def find_all_active_batches(company: str) -> list[dict]:
    """List ALL active batches for a company (any shard slot). UI display.

    Returns list of {"name": ..., "shard_token": ..., "status": ...} for
    every batch in ACTIVE_STATUSES on this company. Used to surface the
    full active-batch picture (e.g. "Batch A — shard '2025' POSTING +
    Batch B — shard '01-2026' POSTING") rather than the legacy 1:1 view.
    """
    return frappe.db.get_all(
        "Misa Migration Batch",
        filters={"company": company, "status": ["in", ACTIVE_STATUSES]},
        fields=["name", "shard_token", "status"],
        order_by="creation desc",
    )
