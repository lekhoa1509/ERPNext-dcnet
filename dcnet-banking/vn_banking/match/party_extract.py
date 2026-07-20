"""Fuzzy partner-name extraction from bank statement descriptions.

Pure functions — no Frappe imports. See test_party_extract.py for coverage.

FB-522 — when a bank statement description contains a customer/supplier
name like "CTY CMC TELECOM CHUYEN KHOAN ...", suggest the matching party
even if no outstanding invoice is found. Independent of invoice matching.
"""
from __future__ import annotations

import re
import unicodedata

# VN company prefixes/qualifiers that add noise to fuzzy matching.
# Order matters — longer phrases first so partial matches don't eat
# their substrings ("CONG TY CO PHAN" before "CONG TY").
_VN_PREFIXES = (
    "CONG TY CO PHAN",
    "CONG TY TNHH MTV",
    "CONG TY TNHH",
    "CONG TY",
    "CTY CP CONG TY",
    "CTY CP",
    "CTY TNHH MTV",
    "CTY TNHH",
    "CTY",
    "CTCP",
    "CO PHAN",
    "TNHH MTV",
    "TNHH",
    "MTV",
)


def normalize_vn_company_name(name: str | None) -> str:
    """Normalize a VN-style party name for fuzzy comparison.

    Steps: NFKD strip diacritics -> uppercase -> strip common prefixes
    (CTY, CONG TY, TNHH, CTCP, MTV, ...) -> collapse whitespace ->
    strip leading/trailing punctuation.
    """
    if not name:
        return ""
    # 1. NFKD then drop combining marks (đ/Đ need special handling — NFKD
    # leaves them as-is, so map manually).
    s = name.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    # 2. Uppercase + collapse whitespace
    s = s.upper()
    s = re.sub(r"\s+", " ", s).strip()
    # 3. Strip prefixes (iteratively; some inputs have nested forms)
    changed = True
    while changed:
        changed = False
        for p in _VN_PREFIXES:
            if s.startswith(p + " "):
                s = s[len(p) + 1:].strip()
                changed = True
                break
            if s == p:
                s = ""
                changed = True
                break
    # 4. Trim outer punctuation
    s = s.strip(" ,.;:-_/")
    return s


def find_party_in_description(
    description: str | None,
    candidates: list[str],
    threshold: int = 80,
) -> tuple[str, int] | None:
    """Find the best fuzzy-match party in `candidates` for `description`.

    Returns (party_name_original, ratio) or None if no match >= threshold.

    `party_name_original` is the candidate as supplied (preserving
    diacritics + prefixes) so the caller can look it up against the
    Customer/Supplier master without further normalization.

    Algorithm: normalize both sides, use rapidfuzz.partial_ratio. Short
    normalized candidate names (<3 chars after stripping prefixes) are
    skipped — too noisy.
    """
    if not description or not candidates:
        return None

    from rapidfuzz import fuzz

    norm_desc = normalize_vn_company_name(description)
    if not norm_desc:
        return None

    best: tuple[str, int] | None = None
    for cand in candidates:
        norm_cand = normalize_vn_company_name(cand)
        if len(norm_cand) < 3:
            continue
        ratio = int(fuzz.partial_ratio(norm_cand, norm_desc))
        if ratio < threshold:
            continue
        if best is None or ratio > best[1] or (
            ratio == best[1] and len(norm_cand) > len(normalize_vn_company_name(best[0]))
        ):
            best = (cand, ratio)
    return best
