"""Parse a Misa Migration Batch's files into Misa Migration Row records.

Spec §8.2 — openpyxl read_only + iter_rows streaming, 200-row buffer with
bulk insert, frappe.publish_realtime progress per batch chunk. Memory bound
~50MB regardless of file size.

Entry points:
  parse_batch(batch_name)  — enqueued by api/parse.start_parse
  parse_file(batch_name, file_row_name)  — single-file convenience
"""

from __future__ import annotations

import json
import os
import time
from typing import Iterator

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st

BUFFER_SIZE = 500
PROGRESS_EVENT = "misa_migration:parse_progress"


# PERF (Tier 1.6): Misa Migration Row.voucher_no is search_index=1 in the
# DocType, but it was never populated on insert — orchestrator UPDATE-by-
# voucher then had to JSON_UNQUOTE+JSON_EXTRACT raw_payload in WHERE,
# which forces a full table scan (322k rows) and locks every row for
# every voucher update. Two parallel shards = guaranteed lock-wait
# timeouts. Populating voucher_no here unlocks an index-driven UPDATE
# downstream (see phase_4_orchestrator._update_nkc_row_status_by_voucher).
_VOUCHER_NO_KEYS_NKC = ("Số chứng từ", "voucher_no", "số chứng từ")
_VOUCHER_NO_KEYS_SCT = ("voucher_no", "Số chứng từ", "Số c.từ")


def _extract_voucher_no(payload: dict, file_type: str) -> str | None:
    """Best-effort voucher_no extraction for the indexed column.

    NKC payloads carry the Vietnamese header verbatim. SCT lines come
    out of sct_parser as a normalised dict with ``voucher_no`` already
    populated. Fallback chain handles both.
    """
    if not isinstance(payload, dict):
        return None
    keys = _VOUCHER_NO_KEYS_SCT if file_type == "SCT" else _VOUCHER_NO_KEYS_NKC
    for k in keys:
        v = payload.get(k)
        if v not in (None, ""):
            return str(v)[:140]
    return None

# file_type → Misa Migration Row.entity_type
FILE_TYPE_TO_ENTITY = {
    "UOM": "UOM",
    "Bank": "Bank",
    "Department": "Department",
    "Warehouse": "Warehouse",
    "Item Group": "Item Group",
    "Customer Group": "Customer Group",
    "Supplier Group": "Supplier Group",
    "Cost Center": "Cost Center",
    "Project": "Project",
    "Asset Category": "Asset Category",
    "CCDC Category": "CCDC Category",
    "Account": "Account",
    # Phase 2 — derived defaults / closing rules. These don't insert
    # business documents — they configure Company defaults + VN Settings.
    "Misa Default Account": "Default Account",
    "Misa Closing Rule": "Closing Rule",
    "Item": "Item",
    "Customer": "Customer",
    "Supplier": "Supplier",
    "Employee": "Employee",
    "Bank Account": "Bank Account",
    "NKC": "Voucher",
    "Bang ke BR": "Voucher",
    "Bang ke MV": "Voucher",
    # SCT (Sổ chi tiết vật tư hàng hóa) — each Misa Migration Row holds
    # ONE item-line keyed by voucher_no (the section-marker scanner
    # in sct_parser.parse_sct_rows resolves the marker chain).
    "SCT": "Voucher Line",
}


# --------------------------------------------------------------------- helpers

def _resolve_file_path(file_url: str) -> str:
    """Convert /files/... or /private/files/... to absolute filesystem path."""
    site_path = frappe.utils.get_site_path()
    if file_url.startswith("/files/"):
        return os.path.join(site_path, "public", file_url.lstrip("/"))
    if file_url.startswith("/private/files/"):
        return os.path.join(site_path, file_url.lstrip("/"))
    # absolute path passthrough (for local testing)
    return file_url


def _find_header_row(rows: Iterator[tuple]) -> tuple[list[str], int]:
    """Return (header_list, n_skipped) — skip title + blank rows until 'STT' marker.

    Misa convention: row 0 = title, row 1 = blank, row 2 = headers starting with 'STT'.
    If no STT marker found within first 10 rows, treat first non-blank row as header.
    """
    candidates = []
    for idx, row in enumerate(rows):
        if idx > 15:
            break
        candidates.append(row)
    # Prefer STT marker
    for idx, row in enumerate(candidates):
        first = row[0] if row else None
        if isinstance(first, str) and first.strip().upper() == "STT":
            return [str(c).strip() if c is not None else f"_col_{i}" for i, c in enumerate(row)], idx + 1
    # Fallback: first row with ≥2 non-None cells
    for idx, row in enumerate(candidates):
        non_null = sum(1 for c in row if c is not None and str(c).strip())
        if non_null >= 2:
            return [str(c).strip() if c is not None else f"_col_{i}" for i, c in enumerate(row)], idx + 1
    return [], 0


def _row_to_dict(row: tuple, headers: list[str]) -> dict:
    """Build a Misa source dict from row + header list. Drop None values."""
    out = {}
    for i, val in enumerate(row):
        if i >= len(headers):
            break
        if val is None:
            continue
        # Coerce datetime to ISO string for JSON safety
        if hasattr(val, "isoformat"):
            val = val.isoformat()
        out[headers[i]] = val
    return out


def _publish(batch_name: str, payload: dict) -> None:
    """Realtime progress to subscribers (Vue ParseStep listens)."""
    payload.setdefault("batch", batch_name)
    payload.setdefault("ts", int(time.time()))
    try:
        frappe.publish_realtime(PROGRESS_EVENT, payload, after_commit=False)
    except Exception:
        pass  # realtime is best-effort; never fail parse because of it


_INSERT_COLS = (
    "name", "creation", "modified", "owner", "modified_by",
    "docstatus", "idx",
    "batch", "file_type", "entity_type", "row_index", "status",
    "voucher_no", "raw_payload",
)


def _bulk_insert_rows(rows: list[dict]) -> int:
    """Bulk-INSERT N Misa Migration Row records in a single multi-VALUES statement.

    Misa Migration Row is staging-only (no business hooks, controller is `pass`,
    track_changes=0 on the DocType). Frappe ORM lifecycle (autoname, validate,
    db_insert, audit) adds ~10ms/row and no value here. Raw multi-row INSERT
    cuts the insert phase 10-50x.
    """
    if not rows:
        return 0
    user = frappe.session.user or "Administrator"
    now = frappe.utils.now()
    placeholder = "(" + ",".join(["%s"] * len(_INSERT_COLS)) + ")"
    sql = (
        f"INSERT INTO `tabMisa Migration Row` "
        f"({', '.join('`' + c + '`' for c in _INSERT_COLS)}) VALUES "
        + ", ".join([placeholder] * len(rows))
    )
    flat: list = []
    for r in rows:
        flat.extend([
            frappe.generate_hash(length=10), now, now, user, user,
            0, 0,
            r.get("batch"), r.get("file_type"), r.get("entity_type"),
            r.get("row_index", 0), r.get("status", "New"),
            r.get("voucher_no"), r.get("raw_payload"),
        ])
    frappe.db.sql(sql, flat)
    return len(rows)


def _update_file_row(file_row_name: str, **fields) -> None:
    """Single SQL UPDATE on a Misa Migration File row, bumps modified=NOW().

    Replaces `file_row.X = Y; batch.save()` to avoid the child-row race
    when multiple parse_file jobs run in parallel against the same batch:
    each `batch.save()` writes the WHOLE batch doc including its `files`
    child table, so the second saver clobbers the first's in-flight
    child-row changes. Per-row SQL UPDATE has no race.
    """
    if not fields:
        return
    set_clause = ", ".join(f"`{c}`=%s" for c in fields.keys()) + ", `modified`=NOW()"
    frappe.db.sql(
        f"UPDATE `tabMisa Migration File` SET {set_clause} WHERE name=%s",
        list(fields.values()) + [file_row_name],
    )
    frappe.db.commit()


# Queue routing for parallel file parsing. Big files → `long` queue so they
# don't block the small-master pipeline on `short`. parse_batch orchestrator
# runs on `default` and just polls, so it never starves the per-file workers.
_QUEUE_BY_FILE_TYPE = {
    "NKC": "long",
    "SCT": "long",
    "Bang ke BR": "long",
    "Bang ke MV": "long",
}


def _queue_for_file_type(file_type: str) -> str:
    return _QUEUE_BY_FILE_TYPE.get(file_type, "short")


# ----------------------------------------------------------------- entry points

def parse_file(batch_name: str, file_row_name: str) -> dict:
    """Parse a single file row's xlsx into Misa Migration Row records.

    Updates Misa Migration File.parse_status + row_count + column_count.
    Returns summary dict.
    """
    from openpyxl import load_workbook

    batch = frappe.get_doc("Misa Migration Batch", batch_name)
    file_row = next((f for f in batch.files if f.name == file_row_name), None)
    if not file_row:
        frappe.throw(_("File row {0} không thuộc batch {1}").format(file_row_name, batch_name))

    file_path = _resolve_file_path(file_row.file_url)
    if not os.path.isfile(file_path):
        err = f"File không tồn tại trên disk: {file_path}"
        _update_file_row(file_row_name, parse_status="Failed", parse_error=err)
        _publish(batch_name, {"file": file_row_name, "status": "failed", "error": err})
        return {"file": file_row_name, "status": "failed", "rows": 0}

    # Pre-compute total rows estimate so UI can show "parsed / total" fraction.
    # openpyxl read_only mode populates max_row from the dimensions tag in the
    # XML — present in all Misa exports. ~1-2s for 6 MB files. We subtract
    # an approximate header offset (Misa always has 2 metadata rows + 1 header
    # row before data, so n_skipped=3 typically; we use 0 here to err on the
    # side of overestimating — better than promising fewer rows than delivered).
    estimated_total = 0
    try:
        if file_row.file_type != "SCT":  # SCT has sectioned layout, max_row inaccurate
            from openpyxl import load_workbook as _lw
            _wb = _lw(file_path, read_only=True, data_only=True)
            _ws = _wb.active
            estimated_total = max((_ws.max_row or 0) - 3, 0)  # -3 for typical Misa header offset
            _wb.close()
    except Exception:
        estimated_total = 0
    _update_file_row(
        file_row_name,
        parse_status="Parsing",
        total_rows_expected=estimated_total,
        row_count=0,  # reset stale row_count from a prior aborted run
        parse_error=None,
    )
    _publish(batch_name, {
        "file": file_row_name, "status": "parsing",
        "filename": file_row.original_filename,
        "total_rows_expected": estimated_total,
    })

    entity_type = FILE_TYPE_TO_ENTITY.get(file_row.file_type, "")
    buffer: list[dict] = []
    total = 0
    cols = 0
    try:
        # SCT has a sectioned layout (warehouse + voucher_no markers
        # interleaved with data rows) that the generic flat-header
        # parser below can't decode — duplicate sub-headers under
        # Nhập/Xuất/Tồn collide in _row_to_dict's header→value dict.
        # Use the dedicated sct_parser which walks section markers and
        # emits one normalised item-line dict per transaction row.
        if file_row.file_type == "SCT":
            from vn_accounting.misa_migration.parsers.sct_parser import (
                parse_sct_xlsx,
            )
            cols = 67  # SCT canonical width
            row_index = 0
            for line in parse_sct_xlsx(file_path):
                row_index += 1
                buffer.append({
                    "batch": batch_name,
                    "file_type": file_row.file_type,
                    "entity_type": entity_type,
                    "row_index": row_index,
                    "status": "New",
                    # PERF (Tier 1.6): denormalise voucher_no into the
                    # indexed column so orchestrator UPDATE-by-voucher
                    # uses the index instead of JSON-extract full scan.
                    "voucher_no": _extract_voucher_no(line, file_row.file_type),
                    "raw_payload": json.dumps(line, ensure_ascii=False, default=str),
                })
                total += 1
                if len(buffer) >= BUFFER_SIZE:
                    _bulk_insert_rows(buffer)
                    buffer.clear()
                    # Push row_count update so the UI shows the file's count
                    # growing — large files (6 MB NKC, 90k+ rows) otherwise
                    # show "0 rows" for the entire parse window.
                    frappe.db.sql(
                        "UPDATE `tabMisa Migration File` SET row_count=%s, modified=NOW() WHERE name=%s",
                        (total, file_row_name),
                    )
                    frappe.db.commit()
                    _publish(batch_name, {
                        "file": file_row_name, "status": "parsing",
                        "filename": file_row.original_filename,
                        "done": total, "row_count": total,
                    })
            if buffer:
                _bulk_insert_rows(buffer)
                buffer.clear()
                frappe.db.sql(
                    "UPDATE `tabMisa Migration File` SET row_count=%s, modified=NOW() WHERE name=%s",
                    (total, file_row_name),
                )
                frappe.db.commit()
        else:
            wb = load_workbook(file_path, read_only=True, data_only=True)
            ws = wb.active
            row_iter = ws.iter_rows(values_only=True)

            # peek first ~15 rows to find header
            first_chunk = []
            for idx, row in enumerate(row_iter):
                first_chunk.append(row)
                if idx >= 15:
                    break
            headers, n_skipped = _find_header_row(iter(first_chunk))
            cols = len(headers)
            if not headers:
                raise ValueError("Không xác định được header")

            # remaining unprocessed rows from first_chunk
            data_rows_from_peek = first_chunk[n_skipped:]

            def _emit_row(data_row: tuple, row_index: int) -> None:
                nonlocal total
                payload = _row_to_dict(data_row, headers)
                if not payload:
                    return  # skip fully-blank rows
                buffer.append({
                    "batch": batch_name,
                    "file_type": file_row.file_type,
                    "entity_type": entity_type,
                    "row_index": row_index,
                    "status": "New",
                    # PERF (Tier 1.6): see SCT branch above.
                    "voucher_no": _extract_voucher_no(payload, file_row.file_type),
                    "raw_payload": json.dumps(payload, ensure_ascii=False, default=str),
                })
                total += 1
                if len(buffer) >= BUFFER_SIZE:
                    _bulk_insert_rows(buffer)
                    buffer.clear()
                    frappe.db.sql(
                        "UPDATE `tabMisa Migration File` SET row_count=%s, modified=NOW() WHERE name=%s",
                        (total, file_row_name),
                    )
                    frappe.db.commit()
                    _publish(batch_name, {
                        "file": file_row_name, "status": "parsing",
                        "filename": file_row.original_filename,
                        "done": total, "row_count": total,
                    })

            # process peeked data + stream the rest
            for i, r in enumerate(data_rows_from_peek):
                _emit_row(r, n_skipped + i + 1)
            for j, r in enumerate(row_iter):
                _emit_row(r, n_skipped + len(data_rows_from_peek) + j + 1)

            if buffer:
                _bulk_insert_rows(buffer)
                buffer.clear()
                frappe.db.sql(
                    "UPDATE `tabMisa Migration File` SET row_count=%s, modified=NOW() WHERE name=%s",
                    (total, file_row_name),
                )
                frappe.db.commit()
            wb.close()
    except Exception as exc:
        # rollback partial inserts? — too expensive on 7k+ rows. Mark failed instead.
        err = f"{type(exc).__name__}: {exc}"
        _update_file_row(
            file_row_name, parse_status="Failed", parse_error=err[:1000],
        )
        _publish(batch_name, {"file": file_row_name, "status": "failed", "error": err})
        frappe.log_error(title=f"Misa parse_file failed: {file_row.original_filename}", message=err)
        return {"file": file_row_name, "status": "failed", "rows": total, "error": err}

    # update file row stats
    _update_file_row(
        file_row_name,
        parse_status="Parsed",
        row_count=total,
        column_count=cols,
        parse_error=None,
    )
    _publish(batch_name, {"file": file_row_name, "status": "parsed", "rows": total})
    return {"file": file_row_name, "status": "parsed", "rows": total, "columns": cols}


def _parse_files_parallel(batch_name: str, files_to_parse: list[tuple[str, str]]) -> None:
    """Enqueue per-file parse_file jobs across short/long queues + poll.

    files_to_parse: list of (file_row_name, file_type). Each is dispatched
    to the queue selected by _queue_for_file_type — big files (NKC/SCT/
    Bang ke) → `long`, small masters → `short`. The orchestrator that
    calls this stays on the `default` queue and just polls, so we get
    real parallelism across the bench's 3 workers without starvation.

    Per multi-session.md #18 / frappe-doctype-perms.md: commits MariaDB
    snapshot before each poll so parse_status / row_count updates from
    the per-file workers become visible.
    """
    import time as _t

    for fname, ftype in files_to_parse:
        frappe.enqueue(
            "vn_accounting.misa_migration.jobs.parse_job.parse_file",
            batch_name=batch_name,
            file_row_name=fname,
            queue=_queue_for_file_type(ftype),
            timeout=14400,
        )

    file_names = [fn for fn, _ftype in files_to_parse]
    placeholders = ",".join(["%s"] * len(file_names))
    deadline = _t.time() + 4 * 3600
    while _t.time() < deadline:
        frappe.db.commit()
        pending = frappe.db.sql(
            f"SELECT COUNT(*) FROM `tabMisa Migration File` "
            f"WHERE name IN ({placeholders}) "
            f"AND parse_status NOT IN ('Parsed', 'Failed')",
            file_names,
        )[0][0]
        if pending == 0:
            return
        _t.sleep(2)
    frappe.throw(_("parse_batch timeout: files still pending after 4h"))


def parse_batch(batch_name: str, parallel: bool = False) -> dict:
    """Parse all files in a batch + transition UPLOADED → PARSED.

    parallel=True: dispatch per-file jobs across short/long queues and poll
    for completion (5x wall-clock improvement on real-data batches).

    parallel=False (default + sync mode + tests): iterate files in-process.

    Acquires lock_for_batch around the state transition so a concurrent
    parse on the same batch raises cleanly.
    """
    batch = frappe.get_doc("Misa Migration Batch", batch_name)
    if batch.status not in ("UPLOADED",):
        frappe.throw(
            _("Không thể parse ở trạng thái {0} — phải là UPLOADED.").format(batch.status)
        )

    # Filter Fix #1 skips first — never re-parse files already Parsed.
    # Without this, re-clicking "Bắt đầu phân tích" after a worker crash
    # re-parses big files from scratch (NKC ~6MB, 15+ min).
    summaries: list[dict] = []
    total_rows = 0
    files_to_parse: list[tuple[str, str]] = []
    for f in (batch.files or []):
        if f.parse_status == "Parsed" and (f.row_count or 0) > 0:
            summaries.append({
                "file": f.name, "status": "parsed",
                "rows": f.row_count or 0, "skipped": True,
            })
            total_rows += (f.row_count or 0)
            _publish(batch_name, {
                "file": f.name, "status": "parsed",
                "rows": f.row_count or 0, "skipped": True,
            })
            continue
        files_to_parse.append((f.name, f.file_type))

    if files_to_parse:
        if parallel:
            _parse_files_parallel(batch_name, files_to_parse)
            placeholders = ",".join(["%s"] * len(files_to_parse))
            file_names = [fn for fn, _ in files_to_parse]
            results = frappe.db.sql(
                f"SELECT name, parse_status, row_count, parse_error "
                f"FROM `tabMisa Migration File` "
                f"WHERE name IN ({placeholders})",
                file_names, as_dict=True,
            )
            for r in results:
                summaries.append({
                    "file": r["name"],
                    "status": "parsed" if r["parse_status"] == "Parsed" else "failed",
                    "rows": r["row_count"] or 0,
                    "error": r["parse_error"],
                })
                total_rows += (r["row_count"] or 0)
        else:
            for fname, _ftype in files_to_parse:
                s = parse_file(batch_name, fname)
                summaries.append(s)
                total_rows += s.get("rows", 0)

    # After raw parse, classify each row via importer.preview_row so the
    # Review tab can show counts immediately. Phase B owns this; Phase D
    # (transactions) will replace with a richer classifier.
    from vn_accounting.misa_migration.importers.orchestrator import run_preview
    try:
        preview_summary = run_preview(batch_name)
    except Exception as exc:
        preview_summary = {"_error": str(exc)}
        frappe.log_error(title="Misa preview during parse_batch failed", message=str(exc))

    # Transition under lock — re-read batch in case parse_file saved updates
    with st.lock_for_batch(batch):
        batch = frappe.get_doc("Misa Migration Batch", batch_name)
        batch.total_rows = total_rows
        any_failed = any(s.get("status") == "failed" for s in summaries)
        if not any_failed:
            st.transition(batch, st.PARSED, reason=f"parsed {total_rows} rows across {len(summaries)} files")
        else:
            st.transition(batch, st.STUCK, reason="parse failed on at least 1 file")
        batch.save(ignore_permissions=True)
        frappe.db.commit()

    _publish(batch_name, {"status": batch.status, "total_rows": total_rows,
                          "files": summaries, "preview": preview_summary})
    return {"batch": batch_name, "status": batch.status, "total_rows": total_rows,
            "files": summaries, "preview": preview_summary}
