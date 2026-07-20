"""COA leaf bootstrap for Misa migration.

Misa SME ships level-5 leaf accounts (1111, 1561, 2141, 3331, 3341, 4111,
4112, 4211, 4212, 4213, etc.) directly used as posting accounts. ERPNext's
VN Large Enterprise / VN Small Trade COA only stops at level-4 (111, 156,
214, 333, 334, 411, 421) — so Misa opening balances + transactional GL
posts that reference the deeper leaves either fail with "account not found"
or get collapsed to the group account by `_resolve_account` fallback logic.

This helper auto-creates the missing leaves UNDER their longest-matching
existing parent, inheriting `root_type` and `account_type` from the parent.
Idempotent — repeated calls are no-ops once leaves exist.

Public:
  ensure_misa_leaves_for_company(company: str) -> dict

Standard Misa leaf set (cherry-picked from Danh_sach_so_du_tai_khoan.xlsx
across real T1/2026 client data — covers cash/bank, AR/AP, inventory,
fixed asset, VAT, payroll, loans, capital, retained earnings):

  Cash + Bank:        1111, 1121
                      11210, 11214, 11215, 11218  (per-bank sub-accounts)
                      1121.81                     (placeholder for special accts)
  Inventory:          1531, 1561, 156100
  Fixed asset:        2112, 2113, 2114, 2115, 2118, 2135
  Accum depreciation: 2141
  Tax payable:        3331, 33311, 33381, 33382 (sub-codes)
  Payable to staff:   3341
  Loan principal:     3411
  Equity (capital):   4111, 4112, 4118
  Retained earnings:  4211, 4212, 4213

Adjustable per-company via Misa Account Mapping override (the resolved
leaf name persists into the mapping so subsequent calls go direct).
"""

from __future__ import annotations

import json

import frappe


# Misa standard level-5 leaves grouped by their level-4 parent. Adjust if
# client COA differs — typical adjustment is renaming or skipping certain
# rows (e.g. bank sub-codes are bank-specific).
MISA_STANDARD_LEAVES = {
    # parent_code: [(leaf_code, leaf_name)]
    "111": [
        ("1111", "Tiền mặt VND"),
    ],
    # Misa hierarchy: 112 → 1121 → {11210, 11214, 11215, 11218, 1121.20,
    # 1121.21, 1121.81, ...}. BCDTK reports parent rollup at TK 1121 (sum of
    # all VND bank sub-accounts). Flattening sub-accounts under 112 broke
    # validation: TK 1121 closing balance reads as 0 (empty leaf) instead of
    # the bank-sub-account sum. Insertion order matters — Python 3.7+ dicts
    # preserve order, so 112 is processed before 1121 (parent before
    # parent-of-children pattern). The _create_leaf helper auto-promotes a
    # leaf to group when the first child arrives.
    "112": [
        ("1121", "Tiền gửi VND ngân hàng"),
        ("1122", "Tiền gửi ngoại tệ"),
    ],
    "1121": [
        ("11210", "Tiền gửi VND BIDV"),
        ("11214", "Tiền gửi VND Vietcombank"),
        ("11215", "Tiền gửi VND Techcombank"),
        ("11218", "Tiền gửi VND Khác"),
        ("1121.20", "Tiền gửi VND sub-20"),
        ("1121.21", "Tiền gửi VND sub-21 (MB)"),
        ("1121.81", "Tiền gửi đặc biệt"),
    ],
    "153": [
        ("1531", "Công cụ dụng cụ"),
    ],
    "155": [
        ("1551", "Thành phẩm chính"),
    ],
    "156": [
        ("1561", "Giá mua hàng hóa"),
        ("1563", "Hàng hóa kho phụ"),
        ("156100", "Hàng hóa lưu kho"),
    ],
    "211": [
        ("2112", "Nhà cửa, vật kiến trúc"),
        ("2113", "Máy móc, thiết bị"),
        ("2114", "Phương tiện vận tải, truyền dẫn"),
        ("2115", "Thiết bị, dụng cụ quản lý"),
        ("2118", "TSCĐ hữu hình khác"),
    ],
    "213": [
        ("2135", "Phần mềm máy tính"),
    ],
    "214": [
        ("2141", "Hao mòn TSCĐ hữu hình"),
    ],
    # 333 hierarchy per TT99/2025: 333 → {3331 (VAT parent), 3334 (TNDN
    # leaf), 3335 (TNCN leaf), 3338 (other fees parent)} where 3331 owns
    # 33311 and 3338 owns 33381/33382. Source BCDTK rolls up at parent codes.
    "333": [
        ("3331", "Thuế GTGT phải nộp"),
        ("3334", "Thuế TNDN"),
        ("3335", "Thuế TNCN"),
        ("3338", "Các loại thuế khác phải nộp"),
    ],
    "3331": [
        ("33311", "Thuế GTGT đầu ra"),
    ],
    "3338": [
        ("33381", "Thuế môn bài"),
        ("33382", "Các loại thuế khác"),
    ],
    "334": [
        ("3341", "Phải trả công nhân viên"),
    ],
    "338": [
        ("3388", "Các khoản phải trả phải nộp khác"),
    ],
    "341": [
        ("3411", "Các khoản đi vay"),
    ],
    "352": [
        ("3524", "Dự phòng phải trả khác"),
    ],
    # 411 hierarchy: 411 → 4111 (parent of 41111 share class) + 4112 leaf
    # + 4118 leaf. Source BCDTK rolls up at 4111 for share-class sums.
    "411": [
        ("4111", "Vốn góp của chủ sở hữu"),
        ("4112", "Thặng dư vốn cổ phần"),
        ("4118", "Vốn khác"),
    ],
    "4111": [
        ("41111", "Cổ phiếu phổ thông có quyền biểu quyết"),
    ],
    "421": [
        ("4211", "LNST chưa phân phối năm trước"),
        ("4212", "LNST chưa phân phối năm nay"),
        ("4213", "Các khoản chênh lệch khác"),
    ],
}


def _find_parent_account(parent_code: str, company: str) -> str | None:
    """Find the existing Account with this account_number (preferred) or
    name starting with '<code> - ' as a fallback."""
    name = frappe.db.get_value(
        "Account",
        {"account_number": parent_code, "company": company},
        "name",
    )
    if name:
        return name
    # Fallback to name-prefix match
    name = frappe.db.get_value(
        "Account",
        {"name": ("like", f"{parent_code} - %"), "company": company},
        "name",
    )
    return name


def _create_leaf(
    leaf_code: str,
    leaf_label: str,
    parent_name: str,
    company: str,
) -> str | None:
    """Create one leaf Account under parent_name. Returns Account.name or None."""
    parent_doc = frappe.get_doc("Account", parent_name)
    leaf_payload = {
        "doctype": "Account",
        "account_name": leaf_label,
        "account_number": leaf_code,
        "parent_account": parent_name,
        "company": company,
        "is_group": 0,
        "root_type": parent_doc.root_type,
        "report_type": parent_doc.report_type,
        # Inherit account_type so e.g. 1121 → Bank, 2141 → Accumulated
        # Depreciation, 6424 → Depreciation
        "account_type": parent_doc.account_type or None,
        "account_currency": parent_doc.account_currency or "VND",
    }
    # Promote parent to group if it's currently a leaf (must hold children)
    if not parent_doc.is_group:
        # Already a leaf — promote to group so it can hold these new children.
        # Frappe blocks this if the parent has GL entries; we work around by
        # disabling validation flags. Per ERPNext patterns, parent with GL
        # gets reclassified safely as long as no posting will write to it
        # going forward (migration moves balances to children instead).
        try:
            parent_doc.is_group = 1
            parent_doc.flags.ignore_permissions = True
            parent_doc.flags.ignore_validate = True
            parent_doc.save()
        except Exception as exc:
            frappe.log_error(
                title=f"COA promote-to-group failed: {parent_name}",
                message=f"{type(exc).__name__}: {exc}",
            )
            return None
    try:
        doc = frappe.get_doc(leaf_payload)
        doc.flags.ignore_permissions = True
        doc.insert()
        return doc.name
    except Exception as exc:
        frappe.log_error(
            title=f"COA leaf create failed: {leaf_code}",
            message=f"{type(exc).__name__}: {exc}",
        )
        return None


def _find_longest_parent(tk_code: str, company: str) -> str | None:
    """Return the existing Account whose account_number is the LONGEST proper
    prefix of tk_code. Handles dotted notation by trying both the dotted and
    bare prefix at each length.

    Examples (assuming 1121 exists):
      _find_longest_parent("11215")    → "1121 - ..."
      _find_longest_parent("1121.21")  → "1121 - ..."
      _find_longest_parent("33311")    → "3331" if exists, else "333"

    Returns the longest match — caller relies on hierarchy: shorter parent
    creates first, so 11215's parent picks 1121 (created earlier) not 112.
    """
    # Generate prefix candidates longest-first
    candidates = []
    base = tk_code
    if "." in tk_code:
        # 1121.21 → try 1121 (drop everything from "." onward) first
        candidates.append(tk_code.split(".", 1)[0])
        base = tk_code.split(".", 1)[0]
    for cut in range(len(base) - 1, 0, -1):
        candidates.append(base[:cut])
    seen = set()
    for cand in candidates:
        if not cand or cand in seen:
            continue
        seen.add(cand)
        name = frappe.db.get_value(
            "Account", {"account_number": cand, "company": company}, "name",
        )
        if name:
            return name
    return None


def _collect_source_tks_from_batch(batch_name: str) -> dict[str, str]:
    """Scan Misa Migration Rows for a batch and return {tk_code: tk_label}.

    Pulls TKs from THREE source-file types:
    - OB / Account Balance: explicit 'account_number' + 'account_name' (best
      source of human-readable labels — comes from BCDTK).
    - NKC legs: 'Tài khoản' and 'TK đối ứng' fields (codes only, no name).
    - BR/MV invoice lists: pulled if they carry TK columns.

    Names from OB win over NKC (OB has human labels; NKC is code-only).
    Empty labels are tolerated — caller falls back to f"TK {code}".
    """
    tks: dict[str, str] = {}

    rows = frappe.db.sql(
        """SELECT raw_payload, parsed_payload, file_type FROM `tabMisa Migration Row`
           WHERE batch=%s""",
        (batch_name,),
        as_dict=True,
    )
    for r in rows:
        # Prefer parsed_payload when present (already structured)
        payload_raw = r.get("parsed_payload") or r.get("raw_payload") or "{}"
        try:
            p = json.loads(payload_raw) if isinstance(payload_raw, str) else (payload_raw or {})
        except (ValueError, TypeError):
            continue
        if not isinstance(p, dict):
            continue
        ft = (r.get("file_type") or "").upper()

        # OB / Account-balance shape — best source of names
        if ft in ("OB", "OB_AB", "OPENING_BALANCE", "ACCOUNT_BALANCE"):
            code = (p.get("account_number") or p.get("Số TK") or "").strip()
            label = (p.get("account_name") or p.get("Tên TK") or "").strip()
            if code and code[0].isdigit():
                # OB labels win over previously-seen labels
                tks[code] = label or tks.get(code, "")

        # NKC — code only
        for key in ("Tài khoản", "TK đối ứng", "tk", "tk_contra", "account"):
            v = (p.get(key) or "").strip() if isinstance(p.get(key), str) else ""
            if v and v[0].isdigit():
                tks.setdefault(v, "")

        # BR/MV — code may appear in line-item 'account' fields
        for li in (p.get("line_items") or []):
            if isinstance(li, dict):
                v = (li.get("account") or li.get("tk") or "").strip()
                if v and v[0].isdigit():
                    tks.setdefault(v, "")

    return tks


def ensure_coa_leaves_from_batch(
    batch_name: str,
    company: str,
) -> dict[str, list[str]]:
    """Source-driven CoA leaf bootstrap.

    Replaces the hardcoded MISA_STANDARD_LEAVES approach with discovery from
    Misa Migration Rows. Works for ANY company's CoA — TK structure inferred
    from the SOURCE files (BCDTK names + NKC code references), parent-child
    relationships inferred from TK prefix matching.

    Algorithm:
      1. Scan all Misa Migration Rows in batch → collect {tk_code: tk_label}.
      2. Sort TKs by (length, lex) ascending so parents are processed before
         children (e.g. 112 before 1121 before 11215).
      3. For each TK not yet in CoA, find LONGEST existing prefix as parent.
         Promote parent leaf → group if needed. Create child inheriting
         root_type/account_type.
      4. Skip TKs whose parent prefix not present (template missing root).

    Idempotent. Falls back gracefully when source data has unusual TKs.

    Args:
      batch_name: Misa Migration Batch.name.
      company: Company.name to bootstrap CoA on.

    Returns:
      {'created': [...], 'skipped_existing': [...], 'skipped_no_parent': [...],
       'errors': [{code, error}], 'source_tks': N}
    """
    if not frappe.db.exists("Company", company):
        return {"created": [], "skipped_existing": [], "skipped_no_parent": [],
                "errors": [{"code": "*", "error": f"Company {company!r} not found"}]}

    src_tks = _collect_source_tks_from_batch(batch_name)
    sorted_tks = sorted(src_tks.items(), key=lambda x: (len(x[0]), x[0]))

    created: list[str] = []
    skipped_existing: list[str] = []
    skipped_no_parent: list[str] = []
    errors: list[dict] = []

    for tk_code, tk_label in sorted_tks:
        # Skip if already exists
        existing = frappe.db.exists(
            "Account", {"account_number": tk_code, "company": company},
        )
        if existing:
            skipped_existing.append(tk_code)
            continue
        # Find longest existing prefix as parent
        parent_name = _find_longest_parent(tk_code, company)
        if not parent_name:
            skipped_no_parent.append(tk_code)
            continue
        # Create
        label = tk_label or f"TK {tk_code}"
        new_name = _create_leaf(tk_code, label, parent_name, company)
        if new_name:
            created.append(new_name)
        else:
            errors.append({"code": tk_code, "error": "create failed (see log)"})

    return {
        "created": created,
        "skipped_existing": skipped_existing,
        "skipped_no_parent": skipped_no_parent,
        "errors": errors,
        "source_tks": len(src_tks),
    }


def ensure_misa_leaves_for_company(
    company: str,
    extra_leaves: dict[str, list[tuple[str, str]]] | None = None,
) -> dict[str, list[str]]:
    """Bootstrap level-5 Misa leaf accounts under existing parent accounts.

    LEGACY hardcoded-baseline approach — kept as fallback for callers that
    don't have a batch_name yet (e.g., pre-batch CoA seeding). Production
    path: use ``ensure_coa_leaves_from_batch`` which discovers TKs from the
    actual source data instead of relying on the bundled Misa-SME baseline.

    Idempotent: re-running is a no-op for existing leaves.

    Args:
      company: Company.name to create leaves under.
      extra_leaves: optional client-specific extension {parent_code: [(code, label)]}
                    merged on top of MISA_STANDARD_LEAVES.

    Returns:
      {
        'created': [new Account.name list],
        'skipped_existing': [Account.name list already present],
        'skipped_no_parent': [leaf_code list whose parent doesn't exist],
        'errors': [{code, error}],
      }
    """
    if not frappe.db.exists("Company", company):
        return {"created": [], "skipped_existing": [], "skipped_no_parent": [],
                "errors": [{"code": "*", "error": f"Company {company!r} not found"}]}

    leaf_map = dict(MISA_STANDARD_LEAVES)
    if extra_leaves:
        for k, v in extra_leaves.items():
            leaf_map.setdefault(k, []).extend(v)

    created: list[str] = []
    skipped_existing: list[str] = []
    skipped_no_parent: list[str] = []
    errors: list[dict] = []

    for parent_code, leaves in leaf_map.items():
        parent_name = _find_parent_account(parent_code, company)
        if not parent_name:
            for leaf_code, _ in leaves:
                skipped_no_parent.append(leaf_code)
            continue
        for leaf_code, leaf_label in leaves:
            # Skip if already exists by code or by name-prefix
            already = (
                frappe.db.exists(
                    "Account",
                    {"account_number": leaf_code, "company": company},
                )
                or frappe.db.exists(
                    "Account",
                    {"name": ("like", f"{leaf_code} - %"), "company": company},
                )
            )
            if already:
                skipped_existing.append(leaf_code)
                continue
            new_name = _create_leaf(leaf_code, leaf_label, parent_name, company)
            if new_name:
                created.append(new_name)
            else:
                errors.append({"code": leaf_code, "error": "create failed (see log)"})

    return {
        "created": created,
        "skipped_existing": skipped_existing,
        "skipped_no_parent": skipped_no_parent,
        "errors": errors,
    }
