"""Auto pipeline — one-shot migration: upload xong là chạy tới cùng.

Chains the existing stage machinery into ONE background job so the
operator never clicks through wizard steps:

    Phân tích file  →  Cài tài khoản & danh mục  →  Kiểm tra dữ liệu
    →  Tạo & ghi sổ chứng từ  →  Đối chiếu số liệu

Per-stage progress lives in ``Misa Migration Batch.pipeline_json``::

    {
      "stages": [
        {"key": "parse", "label": "...", "status": "done",
         "detail": "41 file, 80.290 dòng", "started": iso, "ended": iso},
        ...
      ],
      "current": "post",
      "activity": "Đang tạo Payment Entry 1.200/2.300",
      "error": null,
      "blockers": [...],          # set when preflight pauses the run
      "result": {...},            # validation summary, set by validate stage
    }

The job auto-resolves what it can (auto-skip Invalid rows with a count,
auto-derive OB posting date from data) and pauses ONLY on preflight
blockers — surfaced to the hub UI with resume support.

Watchdog note: every _save_pipeline() write bumps ``batch.modified`` so
the stuck-batch watchdog never false-positives a long post phase.
"""

from __future__ import annotations

import datetime
import json
from typing import Any

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st

PIPELINE_EVENT = "misa_migration:pipeline"

STAGES: list[tuple[str, str]] = [
    ("parse",     "Phân tích file"),
    ("masters",   "Cài đặt tài khoản & danh mục"),
    ("preflight", "Kiểm tra dữ liệu"),
    ("post",      "Tạo & ghi sổ chứng từ"),
    ("reconcile", "Tinh chỉnh sổ cái theo nguồn"),
    ("validate",  "Đối chiếu số liệu"),
]

_STAGE_LABELS = dict(STAGES)


# ------------------------------------------------------------ pipeline state

def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def _load_pipeline(batch_name: str) -> dict[str, Any]:
    raw = frappe.db.get_value("Misa Migration Batch", batch_name, "pipeline_json")
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            pass
    return {
        "stages": [
            {"key": k, "label": lbl, "status": "pending",
             "detail": "", "started": None, "ended": None}
            for k, lbl in STAGES
        ],
        "current": None,
        "activity": "",
        "error": None,
        "blockers": [],
        "result": None,
    }


def _save_pipeline(batch_name: str, pl: dict[str, Any]) -> None:
    """Persist + publish. Direct SQL so we don't reload/save the whole doc
    mid-job; explicitly bumps modified for the idle-watchdog."""
    frappe.db.sql(
        """UPDATE `tabMisa Migration Batch`
           SET pipeline_json=%s, modified=NOW(6) WHERE name=%s""",
        (json.dumps(pl, ensure_ascii=False), batch_name),
    )
    frappe.db.commit()
    try:
        frappe.publish_realtime(
            PIPELINE_EVENT,
            {"batch": batch_name, "pipeline": pl},
            after_commit=False,
        )
    except Exception:
        pass


def _stage(pl: dict[str, Any], key: str) -> dict[str, Any]:
    for s in pl["stages"]:
        if s["key"] == key:
            return s
    raise KeyError(key)


def _begin(batch_name: str, pl: dict[str, Any], key: str, activity: str = "") -> None:
    s = _stage(pl, key)
    s["status"] = "running"
    s["started"] = _now()
    pl["current"] = key
    pl["activity"] = activity or s["label"]
    _save_pipeline(batch_name, pl)


def _done(batch_name: str, pl: dict[str, Any], key: str, detail: str = "") -> None:
    s = _stage(pl, key)
    s["status"] = "done"
    s["ended"] = _now()
    if detail:
        s["detail"] = detail
    _save_pipeline(batch_name, pl)


def _fail(batch_name: str, pl: dict[str, Any], key: str, err: str) -> None:
    s = _stage(pl, key)
    s["status"] = "failed"
    s["ended"] = _now()
    s["detail"] = err[:300]
    pl["error"] = err[:1000]
    pl["activity"] = ""
    _save_pipeline(batch_name, pl)


def set_activity(batch_name: str, text: str) -> None:
    """Lightweight live-activity update other modules may call."""
    pl = _load_pipeline(batch_name)
    pl["activity"] = text
    _save_pipeline(batch_name, pl)


# ------------------------------------------------------------------- stages

def _derive_ob_posting_date(batch_name: str) -> str | None:
    """OB posting date = day before the earliest NKC posting date.

    Saves the operator from picking it manually — the convention for a
    full-period Misa import (e.g. data starts 2025-01-01 → OB on
    2024-12-31)."""
    # NB: rows store source data in raw_payload (parsed_payload is NULL on
    # the bulk path) — read Misa's "Ngày hạch toán" key directly. REGEXP
    # guard: footer rows carry text ("Tổng cộng") in that key.
    row = frappe.db.sql(
        """SELECT MIN(JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Ngày hạch toán"')))
           FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
             AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Ngày hạch toán"'))
                 REGEXP '^[0-9]{4}-'""",
        (batch_name,),
    )
    min_date = row[0][0] if row else None
    if not min_date or str(min_date) in ("null", "None"):
        return None
    try:
        d = datetime.date.fromisoformat(str(min_date)[:10])
    except ValueError:
        return None
    return (d - datetime.timedelta(days=1)).isoformat()


def _stage_parse(batch_name: str, pl: dict[str, Any]) -> None:
    from vn_accounting.misa_migration.jobs.parse_job import parse_batch

    n_files = frappe.db.count("Misa Migration File", {"parent": batch_name})
    pl["activity"] = _("Đang phân tích {0} file…").format(n_files)
    _save_pipeline(batch_name, pl)

    summary = parse_batch(batch_name, parallel=True)
    if summary.get("status") == st.STUCK:
        bad = [f for f in summary.get("files") or [] if f.get("status") == "failed"]
        raise frappe.ValidationError(
            _("Phân tích lỗi ở {0} file: {1}").format(
                len(bad), "; ".join((f.get("error") or "?")[:80] for f in bad[:3])
            )
        )
    total = summary.get("total_rows") or 0

    # Auto-derive OB posting date when the operator didn't set one.
    if not frappe.db.get_value("Misa Migration Batch", batch_name, "ob_posting_date"):
        ob = _derive_ob_posting_date(batch_name)
        if ob:
            frappe.db.set_value("Misa Migration Batch", batch_name,
                                "ob_posting_date", ob, update_modified=False)
            frappe.db.commit()

    _done(batch_name, pl, "parse",
          _("{0} file · {1} dòng").format(n_files, f"{total:,}".replace(",", ".")))


def _stage_masters(batch_name: str, pl: dict[str, Any]) -> None:
    from vn_accounting.misa_migration.api.post import install_misa_coa

    pl["activity"] = _("Đang cài hệ thống tài khoản + danh mục (khách hàng, NCC, vật tư…)")
    _save_pipeline(batch_name, pl)

    res = install_misa_coa(batch_name)
    if res.get("skipped_reason") == "non_vn_coa_detected":
        raise frappe.ValidationError(
            _("Công ty đang dùng hệ thống tài khoản không phải VN (TT99). "
              "Tạo công ty mới với tiền tệ VND hoặc xóa CoA hiện tại trước.")
        )
    ph = res.get("phase_2_summary") or {}
    posted = sum(
        v.get("posted", 0) for v in ph.values() if isinstance(v, dict)
    )
    n_acc = frappe.db.count("Account", {
        "company": frappe.db.get_value("Misa Migration Batch", batch_name, "company"),
    })
    _done(batch_name, pl, "masters",
          _("{0} tài khoản trên công ty · {1} dòng danh mục").format(n_acc, posted))


def _stage_preflight(batch_name: str, pl: dict[str, Any], skip_warnings: bool) -> bool:
    """Returns True to continue, False when paused on blockers."""
    from vn_accounting.misa_migration.api.post import preflight
    from vn_accounting.misa_migration.api.review import (
        mark_reviewed, skip_all_invalid,
    )

    pl["activity"] = _("Đang kiểm tra dữ liệu trước khi tạo chứng từ…")
    _save_pipeline(batch_name, pl)

    # Auto-policy: Invalid rows (parser couldn't classify) are skipped with
    # a visible count instead of blocking the whole run.
    n_invalid = frappe.db.count(
        "Misa Migration Row", {"batch": batch_name, "status": "Invalid"})
    skipped_note = ""
    if n_invalid:
        skip_all_invalid(batch_name)
        skipped_note = _(" · bỏ qua {0} dòng không hợp lệ").format(n_invalid)

    pf = preflight(batch_name) or {}
    # preflight() aggregates Phase B counts + Phase D 10-check + Phase 0
    # prerequisites into flat string lists `blocked` / `warnings`.
    blockers = list(pf.get("blocked") or [])
    warnings = list(pf.get("warnings") or [])

    if blockers:
        s = _stage(pl, "preflight")
        s["status"] = "blocked"
        s["detail"] = _("{0} lỗi chặn").format(len(blockers))
        pl["blockers"] = [{"level": "block", "message": b} for b in blockers] + [
            {"level": "warn", "message": w} for w in warnings
        ]
        pl["activity"] = ""
        pl["current"] = "preflight"
        _save_pipeline(batch_name, pl)
        return False

    if frappe.db.get_value("Misa Migration Batch", batch_name, "status") == st.PARSED:
        mark_reviewed(batch_name)

    n_warn = len(warnings)
    detail = _("Đạt") + (
        _(" · {0} cảnh báo (tiếp tục)").format(n_warn) if n_warn else ""
    ) + skipped_note
    # keep warnings visible in the result panel
    pl["blockers"] = [{"level": "warn", "message": w} for w in warnings]
    _done(batch_name, pl, "preflight", detail)
    return True


def _stage_post(batch_name: str, pl: dict[str, Any]) -> None:
    """Ghi sổ bằng đường bulk SQL (~140× nhanh hơn ORM).

    Toàn bộ doc + chi tiết + GL + SLE được PRE-COMPUTE trong RAM từ NKC/
    bảng kê rồi executemany — đúng chuẩn migration lưu trữ từ nguồn tin
    cậy. Liên kết PE↔hóa đơn, Bin, Payment Ledger được rebuild ngay trong
    run_bulk_pump_full (post_derive); stage reconcile + validate phía sau
    là lưới an toàn."""
    from vn_accounting.misa_migration import state as _st
    from vn_accounting.misa_migration.bulk_pump.orchestrator import (
        run_bulk_pump_full,
    )

    pl["activity"] = _("Đang tạo & ghi sổ chứng từ (bulk)…")
    _save_pipeline(batch_name, pl)

    batch = frappe.get_doc("Misa Migration Batch", batch_name)
    company = batch.company

    # Incremental guard (đối ứng với run_phase_0_post): công ty đã có sổ
    # từ đợt migrate trước → file "đầu kỳ" của batch này mô tả số dư ĐÃ
    # nằm trên sổ — bỏ qua Phase 0 để không ghi trùng.
    include_opening = not bool(frappe.db.sql(
        """SELECT 1 FROM `tabGL Entry`
           WHERE company=%s AND is_cancelled=0
             AND voucher_no NOT LIKE %s
           LIMIT 1""",
        (company, f"{batch_name}-OB%"),
    ))

    with _st.lock_for_batch(batch):
        batch = frappe.get_doc("Misa Migration Batch", batch_name)
        _st.transition(batch, _st.POSTING, reason="auto_pipeline bulk post")
        batch.save(ignore_permissions=True)
        frappe.db.commit()

    try:
        res = run_bulk_pump_full(batch_name, company,
                                 include_opening=include_opening)
    except Exception:
        with _st.lock_for_batch(batch):
            batch = frappe.get_doc("Misa Migration Batch", batch_name)
            _st.transition(batch, _st.STUCK, reason="bulk post fatal")
            batch.save(ignore_permissions=True)
            frappe.db.commit()
        raise

    posted = res.get("voucher_count") or 0
    skipped = res.get("skipped_count") or 0
    with _st.lock_for_batch(batch):
        batch = frappe.get_doc("Misa Migration Batch", batch_name)
        batch.posted_docs_count = posted
        _st.transition(batch, _st.POSTED,
                       reason=f"bulk posted {posted}, skipped {skipped}")
        batch.save(ignore_permissions=True)
        frappe.db.commit()

    detail = _("{0} chứng từ đã ghi sổ (bulk, {1} giây)").format(
        f"{posted:,}".replace(",", "."),
        int(res.get("elapsed_seconds") or 0),
    )
    if not include_opening:
        detail += _(" · bỏ qua số dư đầu kỳ (đã có từ đợt trước)")
    if skipped:
        detail += _(" · {0} bỏ qua").format(skipped)
    _done(batch_name, pl, "post", detail)


def _gl_balance_check(company: str) -> dict[str, Any]:
    """ΣNợ phải bằng ΣCó trên toàn bộ GL của công ty (định khoản kép)."""
    row = frappe.db.sql(
        """SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0)
           FROM `tabGL Entry`
           WHERE company=%s AND is_cancelled=0""",
        (company,),
    )[0]
    dr, cr = float(row[0]), float(row[1])
    return {
        "total_debit": dr,
        "total_credit": cr,
        "diff": dr - cr,
        "balanced": abs(dr - cr) < 1.0,
    }


def _find_attached_path(batch_name: str, *needles: str) -> str | None:
    """Find an uploaded batch file whose original name contains all
    needles (case-insensitive, '_'→' '); returns absolute path."""
    import os
    files = frappe.db.sql(
        """SELECT file_url, original_filename
           FROM `tabMisa Migration File` WHERE parent=%s""",
        (batch_name,), as_dict=True,
    )
    for r in files:
        base = os.path.basename(
            r.get("original_filename") or r.get("file_url") or ""
        ).lower().replace("_", " ")
        if all(n in base for n in needles):
            from vn_accounting.misa_migration.jobs.parse_job import _resolve_file_path
            try:
                return _resolve_file_path(r["file_url"])
            except Exception:
                continue
    return None


def _stage_reconcile(batch_name: str, pl: dict[str, Any]) -> None:
    """Re-derive GL legs from the NKC source for every migrated voucher.

    The ORM handlers build documents from Bảng kê/SCT registers (gross
    prices, VAT back-division, default accounts) — close but not equal to
    the source's per-leg TK routing. The repost scripts rewrite each
    voucher's GL to MATCH the NKC legs exactly; they took the May-2026
    DCNET TEST migration from 62% to 100% per-TK accuracy and are
    idempotent (delete-then-insert per voucher)."""
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")

    from vn_accounting.misa_migration.scripts.repost_si_gl_from_nkc import (
        repost_si_gl_from_nkc,
    )
    from vn_accounting.misa_migration.scripts.repost_pe_gl_from_nkc import (
        repost_pe_gl_from_nkc,
    )
    from vn_accounting.misa_migration.scripts.repost_pi_gl_from_nkc import (
        repost_pi_gl_from_nkc,
    )
    from vn_accounting.misa_migration.scripts.repost_pn_stock_to_payable import (
        repost_se_gl_from_nkc,
    )

    counts: dict[str, int] = {}
    steps = [
        ("SI", _("hóa đơn bán"), lambda: repost_si_gl_from_nkc(company, batch_name)),
        ("PI", _("hóa đơn mua"), lambda: repost_pi_gl_from_nkc(company, batch_name)),
        ("PE", _("phiếu thu/chi"), lambda: repost_pe_gl_from_nkc(company, batch_name)),
        ("SE", _("phiếu kho"), lambda: repost_se_gl_from_nkc(company, batch_name)),
    ]
    for key, label, fn in steps:
        pl["activity"] = _("Đang tinh chỉnh sổ cái: {0}…").format(label)
        _save_pipeline(batch_name, pl)
        try:
            r = fn() or {}
            counts[key] = int(
                r.get("reposted") or r.get("vouchers_processed") or 0
            )
        except Exception as exc:
            counts[key] = -1
            frappe.log_error(
                title=f"Misa reconcile {key} failed",
                message=str(exc),
            )
        frappe.db.commit()

    # P&L residual close — NOW that GL matches the NKC source, close any
    # remaining Income/Expense residual into TK 4212. Idempotent (fixed
    # voucher name, delete-first). Running it earlier (inside bulk post)
    # closed stale pre-reconcile balances → 5,9 tỷ lệch 4212/6321.
    try:
        frappe.db.sql(
            "DELETE FROM `tabGL Entry` WHERE voucher_no LIKE %s AND company=%s",
            ("%PL-CLOSE-RESIDUAL%", company),
        )
        frappe.db.sql(
            """DELETE a FROM `tabJournal Entry Account` a
               JOIN `tabJournal Entry` j ON j.name = a.parent
               WHERE j.name LIKE %s AND j.company=%s""",
            ("%PL-CLOSE-RESIDUAL%", company),
        )
        frappe.db.sql(
            "DELETE FROM `tabJournal Entry` WHERE name LIKE %s AND company=%s",
            ("%PL-CLOSE-RESIDUAL%", company),
        )
        frappe.db.commit()
        from vn_accounting.misa_migration.bulk_pump.backfill_audit_fixes import (
            post_pl_residual_close,
        )
        pl_close = post_pl_residual_close(company)
        counts["PL"] = int(pl_close.get("leg_count") or 0)
        frappe.db.commit()
    except Exception as exc:
        frappe.log_error(title="Misa reconcile PL residual close failed",
                         message=str(exc))

    # ERPNext's background Repost Item Valuation rebuilds stock-voucher GL
    # from SLE valuation — silently OVERWRITING the NKC-derived legs hours
    # later (357 RIV jobs wiped 2,25 tỷ Cr 1561 on the mixed-path E2E).
    # Migration GL is source-of-truth here: park any pending repost.
    frappe.db.sql(
        """UPDATE `tabRepost Item Valuation`
           SET status='Skipped',
               modified=NOW()
           WHERE company=%s AND status IN ('Queued', 'In Progress', 'Failed')""",
        (company,),
    )
    frappe.db.commit()

    detail = " · ".join(
        f"{k}: {v:,}".replace(",", ".") if v >= 0 else f"{k}: lỗi"
        for k, v in counts.items()
    )
    _done(batch_name, pl, "reconcile", detail)


_REFERENCE_FILE_TYPES = ("SCT", "Bang ke BR", "Bang ke MV")


def _stage_validate(batch_name: str, pl: dict[str, Any]) -> None:
    pl["activity"] = _("Đang đối chiếu số liệu (cân đối Nợ/Có, số dư cuối kỳ)…")
    _save_pipeline(batch_name, pl)

    # Bảng kê BR/MV + Sổ chi tiết rows are REFERENCE registers — they feed
    # invoice-line matching inside the NKC handlers and never become docs
    # themselves. Left at "Ready" they read as "19k dòng chưa xử lý" in the
    # result panel. Flip to Skipped with an explanatory note.
    for ft in _REFERENCE_FILE_TYPES:
        frappe.db.sql(
            """UPDATE `tabMisa Migration Row`
               SET status='Skipped',
                   error_message='Dòng tham chiếu (khớp hóa đơn) — không tạo chứng từ riêng'
               WHERE batch=%s AND file_type=%s AND status='Ready'""",
            (batch_name, ft),
        )
    frappe.db.commit()

    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    result: dict[str, Any] = {"gl_balance": _gl_balance_check(company)}

    # Per-doctype posted counts (the operator's "có gì được tạo")
    by_dt: dict[str, int] = {}
    for dt in ("Sales Invoice", "Purchase Invoice", "Payment Entry",
               "Journal Entry", "Stock Entry", "Purchase Receipt"):
        if frappe.db.has_column(dt, "misa_voucher_no"):
            by_dt[dt] = frappe.db.sql(
                f"""SELECT COUNT(*) FROM `tab{dt}`
                    WHERE company=%s AND docstatus=1
                      AND COALESCE(misa_voucher_no,'') != ''""",
                (company,),
            )[0][0]
    result["posted_by_doctype"] = by_dt

    # TB compare when the batch carries a Bảng cân đối tài khoản file —
    # its "Cuối kỳ" columns are the authoritative closing balance.
    tb_path = _find_attached_path(batch_name, "bang can doi tai khoan")
    if tb_path:
        try:
            from vn_accounting.misa_migration.scripts.validate_closing_balance import (
                _validate_accounts,
            )
            period_end = _max_posting_date(company) or datetime.date.today()
            result["tb_compare"] = _validate_accounts(tb_path, company, period_end)
        except Exception as exc:
            result["tb_compare"] = {"error": str(exc)[:300]}

    inv_path = _find_attached_path(batch_name, "tong hop ton kho")
    if inv_path:
        try:
            from vn_accounting.misa_migration.scripts.validate_closing_balance import (
                _validate_inventory,
            )
            result["inventory_compare"] = _validate_inventory(inv_path, company)
        except Exception as exc:
            result["inventory_compare"] = {"error": str(exc)[:300]}

    pl["result"] = result
    gl = result["gl_balance"]
    detail = (
        _("Sổ cái CÂN (Nợ = Có)") if gl["balanced"]
        else _("Sổ cái LỆCH {0} VND").format(f"{gl['diff']:,.0f}")
    )
    tb = result.get("tb_compare")
    if tb and not tb.get("error"):
        detail += _(" · Bảng cân đối khớp {0}/{1} TK").format(
            tb.get("matches", 0), tb.get("total_tks", 0))
    _done(batch_name, pl, "validate", detail)
    pl["activity"] = ""
    _save_pipeline(batch_name, pl)


def _max_posting_date(company: str) -> datetime.date | None:
    v = frappe.db.sql(
        "SELECT MAX(posting_date) FROM `tabGL Entry` WHERE company=%s AND is_cancelled=0",
        (company,),
    )[0][0]
    return v


# --------------------------------------------------------------- entrypoint

def run_auto_pipeline(batch_name: str, skip_warnings: bool = True) -> dict:
    """Run the migration end-to-end from wherever the batch currently is.

    Entry per status: UPLOADED → parse; PARSED → masters; REVIEWED → post.
    Pauses (no exception) when preflight finds blockers. Any stage
    exception → batch STUCK (existing semantics) + pipeline_json carries
    the error for the UI.
    """
    batch = frappe.get_doc("Misa Migration Batch", batch_name)
    status = batch.status

    if status not in (st.UPLOADED, st.PARSED, st.REVIEWED):
        frappe.throw(
            _("Không thể chạy pipeline ở trạng thái {0}.").format(status))

    pl = _load_pipeline(batch_name)
    pl["error"] = None

    # Mark stages already satisfied by current status as done (resume).
    def _mark_done_upto(*keys: str):
        for k in keys:
            s = _stage(pl, k)
            if s["status"] != "done":
                s["status"] = "done"
                s["detail"] = s["detail"] or _("Đã hoàn tất ở lần chạy trước")

    if status in (st.PARSED, st.REVIEWED):
        _mark_done_upto("parse")
    if status == st.REVIEWED:
        _mark_done_upto("masters", "preflight")

    try:
        if status == st.UPLOADED:
            _begin(batch_name, pl, "parse")
            _stage_parse(batch_name, pl)
            status = st.PARSED

        if status == st.PARSED:
            _begin(batch_name, pl, "masters")
            _stage_masters(batch_name, pl)

            _begin(batch_name, pl, "preflight")
            if not _stage_preflight(batch_name, pl, skip_warnings):
                return {"batch": batch_name, "paused": True,
                        "pipeline": pl}
            status = st.REVIEWED

        if status == st.REVIEWED:
            _begin(batch_name, pl, "post")
            _stage_post(batch_name, pl)

        _begin(batch_name, pl, "reconcile")
        _stage_reconcile(batch_name, pl)

        _begin(batch_name, pl, "validate")
        _stage_validate(batch_name, pl)

    except Exception as exc:
        cur = pl.get("current") or "parse"
        _fail(batch_name, pl, cur, str(exc))
        raise

    return {"batch": batch_name, "paused": False, "pipeline": pl}
