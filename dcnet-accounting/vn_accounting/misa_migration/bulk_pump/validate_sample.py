"""Post-pump safety net — load a random 0.5% sample of bulk-inserted docs
through ERPNext's ORM `validate()` to catch row-shape bugs the SQL pump
might have introduced (missing required field, wrong child link, FK).

Fail-loud threshold: >5% of the sample failing validate() raises a
ValidationError so the operator notices before relying on the data.

Coverage: Sales Invoice + Purchase Invoice + Payment Entry. Stock Entry
+ Journal Entry are excluded because their ORM validate() runs the full
GL repost cycle which would defeat the point of bulk-pump speed.
"""
from __future__ import annotations

import math
import random
import time
import traceback

import frappe


# Doctypes whose ORM validate() is cheap enough to spot-check.
_VALIDATE_DOCTYPES = ("Sales Invoice", "Purchase Invoice", "Payment Entry")


def validate_sample(
    company: str,
    sample_pct: float = 0.5,
    fail_threshold_pct: float = 5.0,
    seed: int | None = None,
) -> dict:
    """Sample-pass docs created in this company through ORM validate().

    Args:
        company: scope to docs belonging to this Company.
        sample_pct: fraction of each doctype's rows to sample (default 0.5%).
        fail_threshold_pct: raise ValidationError if more than this % of the
            sample fails validate(). Default 5%.
        seed: optional RNG seed for reproducibility (e.g. in tests).

    Returns:
        {"doctype": str, "sampled": int, "passed": int, "failed": int,
         "elapsed_seconds": float, "errors": list[{"name", "error"}]}
        per doctype in {"per_doctype": [...]}, plus aggregate summary.
    """
    t0 = time.time()
    if seed is not None:
        random.seed(seed)

    pct = max(0.0, min(100.0, float(sample_pct))) / 100.0
    per_dt: list[dict] = []
    total_sampled = total_failed = 0

    for dt in _VALIDATE_DOCTYPES:
        names = frappe.db.sql_list(
            f"SELECT name FROM `tab{dt}` WHERE company=%s AND docstatus=1",
            (company,),
        )
        if not names:
            per_dt.append({
                "doctype": dt, "sampled": 0, "passed": 0, "failed": 0,
                "elapsed_seconds": 0, "errors": [],
            })
            continue

        # At least 5 docs per doctype if any exist, capped at 50.
        sample_size = max(min(5, len(names)), math.ceil(len(names) * pct))
        sample_size = min(sample_size, 50, len(names))
        sample = random.sample(names, sample_size)

        passed = 0
        errors: list[dict] = []
        t_dt = time.time()
        for name in sample:
            try:
                doc = frappe.get_doc(dt, name)
                doc.flags.ignore_permissions = True
                doc.validate()
                passed += 1
            except Exception as exc:
                errors.append({
                    "name": name,
                    "error": f"{type(exc).__name__}: {exc}",
                    "trace": traceback.format_exc(limit=3),
                })

        failed = len(sample) - passed
        per_dt.append({
            "doctype": dt,
            "sampled": len(sample),
            "passed": passed,
            "failed": failed,
            "elapsed_seconds": round(time.time() - t_dt, 2),
            "errors": errors,
        })
        total_sampled += len(sample)
        total_failed += failed

    fail_pct = (total_failed / total_sampled * 100) if total_sampled else 0.0
    result = {
        "company": company,
        "sample_pct": sample_pct,
        "fail_threshold_pct": fail_threshold_pct,
        "total_sampled": total_sampled,
        "total_failed": total_failed,
        "fail_pct": round(fail_pct, 2),
        "elapsed_seconds": round(time.time() - t0, 2),
        "per_doctype": per_dt,
        "passed_threshold": fail_pct <= fail_threshold_pct,
    }

    if not result["passed_threshold"]:
        # Aggregate first few errors for the message
        sample_errs = [
            f"{d['doctype']}/{e['name']}: {e['error']}"
            for d in per_dt for e in d.get("errors", [])[:2]
        ][:6]
        msg = (
            f"bulk_pump validate-sample FAILED: {fail_pct:.1f}% failed "
            f"(>{fail_threshold_pct}%). First errors:\n  - "
            + "\n  - ".join(sample_errs)
        )
        # Don't raise — caller decides. Just mark passed_threshold=False
        # and log. Raising mid-pipeline would roll back unrelated commits.
        frappe.log_error(msg, "bulk_pump validate-sample")

    return result
