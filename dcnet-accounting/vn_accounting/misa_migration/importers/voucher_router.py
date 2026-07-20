"""Voucher router — dispatch parsed NKC voucher dicts to per-prefix handlers.

Per spec §4 Phase 4 and §5: each Misa voucher prefix maps to ONE ERPNext
DocType handler. This module is a thin registry + dispatcher. Handlers
themselves live in importers/nkc_handlers/*.py and follow a common
signature:

    def create_<entity>_from_<prefix>(voucher_dict, invoice_dict=None) -> dict:
        '''Return {"status": "created"|"skipped"|"failed",
                   "target_doctype": str, "target_name": str|None,
                   "error": str|None}'''

The router is import-light: handler modules are imported lazily on first
dispatch so missing handlers don't block test collection or migration
init. Phase D commits 4-12 fill in the handler implementations.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any, Callable

# Prefix → (handler module relative to nkc_handlers, function name within it)
# Source: spec §2.2 voucher prefix → ERPNext mapping (17 prefixes)
PREFIX_HANDLERS: dict[str, tuple[str, str]] = {
    # Sales invoices
    "BH": ("sales_invoice", "create_si_from_bh"),

    # Purchase invoices
    "MDV": ("purchase_invoice", "create_pi_from_mdv"),
    "MH": ("purchase_invoice", "create_pi_from_mh"),

    # Purchase Receipt (PI + PR with update_stock=1)
    "PN": ("purchase_receipt", "create_pi_pr_from_pn"),

    # Stock entries
    "PNHN": ("stock_entry", "create_se_from_pnhn"),
    "PX": ("stock_entry", "create_se_from_px"),
    "PXHN": ("stock_entry", "create_se_from_pxhn"),

    # Payment entries
    "BC": ("payment_entry", "create_pe_from_bc"),
    "UNC": ("payment_entry", "create_pe_from_unc"),
    "PT": ("payment_entry", "create_pe_from_pt"),
    "PC": ("payment_entry", "create_pe_from_pc"),

    # Journal entries (1:1 leg mapping per spec §5)
    "CTNB": ("journal_entry", "create_je_from_ctnb"),
    "NVK": ("journal_entry", "create_je_from_nvk"),
    "PBDT": ("journal_entry", "create_je_from_pbdt"),
    "PBPTT": ("journal_entry", "create_je_from_pbptt"),
    "PBCC": ("journal_entry", "create_je_from_pbcc"),
    "KH": ("journal_entry", "create_je_from_kh"),
    "CK": ("journal_entry", "create_je_from_ck"),
}

# ERPNext target DocType per handler module — used for pre-flight + reporting
HANDLER_TARGET_DOCTYPE: dict[str, str] = {
    "sales_invoice": "Sales Invoice",
    "purchase_invoice": "Purchase Invoice",
    "purchase_receipt": "Purchase Invoice",  # + Purchase Receipt sibling
    "stock_entry": "Stock Entry",
    "payment_entry": "Payment Entry",
    "journal_entry": "Journal Entry",
}


def is_supported_prefix(prefix: str) -> bool:
    """True iff a handler is registered for this Misa prefix."""
    return prefix in PREFIX_HANDLERS


def get_handler_spec(prefix: str) -> tuple[str, str] | None:
    """Return (module, function) handler spec for a prefix; None if unsupported."""
    return PREFIX_HANDLERS.get(prefix)


def get_target_doctype(prefix: str) -> str | None:
    """Return the primary ERPNext target DocType for a prefix; None if unsupported."""
    spec = PREFIX_HANDLERS.get(prefix)
    if not spec:
        return None
    return HANDLER_TARGET_DOCTYPE.get(spec[0])


def _resolve_handler(module_name: str, func_name: str) -> Callable | None:
    """Import handler module + return the function. None on failure."""
    try:
        mod = import_module(
            f"vn_accounting.misa_migration.importers.nkc_handlers.{module_name}"
        )
    except ImportError:
        return None
    return getattr(mod, func_name, None)


def route_voucher(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Dispatch a parsed NKC voucher dict to its prefix handler.

    Args:
      voucher: output of nkc_parser.parse_nkc_rows() — must have 'prefix' +
               'voucher_no'.
      invoice: optional bảng kê BR/MV output dict for this voucher_no
               (handlers for BH/MDV/MH/PN consume line_items from it).
      dry_run: if True, only verify routing config without invoking handler.
               Useful for pre-flight checks before any commit happens.

    Returns:
      {
        "status": "created" | "skipped" | "failed" |
                  "unsupported_prefix" | "handler_missing" | "would_dispatch",
        "voucher_no": str,
        "prefix": str,
        "target_doctype": str | None,
        "target_name": str | None,
        "error": str | None,
      }
    """
    voucher_no = voucher.get("voucher_no", "")
    prefix = voucher.get("prefix") or ""

    base = {
        "voucher_no": voucher_no,
        "prefix": prefix,
        "target_doctype": get_target_doctype(prefix),
        "target_name": None,
        "error": None,
    }

    spec = PREFIX_HANDLERS.get(prefix)
    if not spec:
        return {**base, "status": "unsupported_prefix",
                "error": f"No handler registered for prefix {prefix!r}"}

    module_name, func_name = spec

    if dry_run:
        return {**base, "status": "would_dispatch",
                "handler": f"{module_name}.{func_name}"}

    fn = _resolve_handler(module_name, func_name)
    if fn is None:
        return {**base, "status": "handler_missing",
                "error": f"Cannot resolve {module_name}.{func_name} — module "
                         f"or function not yet implemented"}

    try:
        result = fn(voucher, invoice)
        if not isinstance(result, dict):
            result = {"status": "failed",
                      "error": f"Handler returned {type(result).__name__}, expected dict"}
    except Exception as exc:
        result = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}

    # Fallback: a voucher the specialised handler can't shape (source data
    # quality — e.g. BH with the invoice number typed into the description,
    # MDV with no matching bảng kê line) must STILL reach the ledger or the
    # closing balance misses its legs (40 Failed rows ≈ 15 TK lệch on the
    # fresh-company E2E). Post it as a plain Journal Entry copying the NKC
    # legs 1:1 — đúng Nợ/Có, mất phân hệ (không SI/PI), được đánh dấu rõ.
    if result.get("status") == "failed" and prefix != "NVK":
        try:
            from vn_accounting.misa_migration.importers.nkc_handlers.journal_entry import (
                create_je_from_nvk,
            )
            fb = create_je_from_nvk(voucher, invoice)
            if isinstance(fb, dict) and fb.get("status") == "created":
                return {**base, **fb,
                        "target_doctype": "Journal Entry",
                        "error": (
                            "fallback JE (handler chuyên biệt lỗi: "
                            f"{(result.get('error') or '')[:120]})"
                        )}
        except Exception:
            pass  # keep the original failure below

    return {**base, **result}


def list_supported_prefixes() -> list[str]:
    """Return sorted list of all registered Misa prefixes."""
    return sorted(PREFIX_HANDLERS.keys())


def list_handler_modules() -> list[str]:
    """Return distinct handler module names (5 modules cover 17 prefixes)."""
    seen: set[str] = set()
    out: list[str] = []
    for mod, _ in PREFIX_HANDLERS.values():
        if mod not in seen:
            seen.add(mod)
            out.append(mod)
    return out
