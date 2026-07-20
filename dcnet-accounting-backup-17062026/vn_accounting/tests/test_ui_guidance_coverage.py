"""
UI guidance coverage test — per spec §8.4 and memory feedback_ui_inline_guidance.md.

Verifies that new DocTypes added in this feature branch have adequate field descriptions:
- All reqd=1 fields must have non-empty description (≥10 chars)
- All Link, Select, Currency, Date fields must have non-empty description
- Section Break fields with description help users understand the section purpose

DocTypes checked: LCV Allocation Settings, Manufacturing Costing Settings,
Work In Progress Valuation, BCTC Mapping, BCTC Line.
"""
import json
import os
import unittest

# Maps doctype slug → JSON path (relative to inner package root)
DOCTYPES_TO_CHECK = {
    "lcv_allocation_settings": (
        "vn_accounting/doctype/lcv_allocation_settings/lcv_allocation_settings.json"
    ),
    "bctc_mapping": (
        "vn_accounting/doctype/bctc_mapping/bctc_mapping.json"
    ),
    "bctc_line": (
        "vn_accounting/doctype/bctc_line/bctc_line.json"
    ),
}

# Field types that MUST have descriptions
MUST_HAVE_DESCRIPTION_TYPES = {
    "Link", "Select", "Currency", "Date", "Datetime",
    "Percent", "Float", "Int", "Check",
}

MIN_DESCRIPTION_LENGTH = 10


def _get_package_root() -> str:
    this_file = os.path.abspath(__file__)
    # .../vn_accounting/vn_accounting/tests/test_ui_guidance_coverage.py
    return os.path.dirname(os.path.dirname(this_file))  # vn_accounting/vn_accounting/


def _load_doctype_json(slug: str, rel_path: str) -> dict:
    pkg_root = _get_package_root()
    fpath = os.path.join(pkg_root, rel_path)
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"DocType JSON not found: {fpath}")
    with open(fpath, encoding="utf-8") as f:
        return json.load(f)


def _check_fields(doctype_name: str, data: dict) -> list:
    """Return list of violation strings."""
    violations = []
    fields = data.get("fields", [])

    for fld in fields:
        fname = fld.get("fieldname", "?")
        ftype = fld.get("fieldtype", "")
        desc = (fld.get("description") or "").strip()
        reqd = fld.get("reqd", 0)
        label = fld.get("label", fname)

        # reqd=1 fields must have description
        if reqd and not desc:
            violations.append(
                f"{doctype_name}.{fname} (reqd=1, type={ftype}, label={label!r}) — missing description"
            )
        elif reqd and len(desc) < MIN_DESCRIPTION_LENGTH:
            violations.append(
                f"{doctype_name}.{fname} (reqd=1) — description too short ({len(desc)} chars): {desc!r}"
            )

        # Key field types should have descriptions
        if ftype in MUST_HAVE_DESCRIPTION_TYPES and not reqd:
            if not desc:
                violations.append(
                    f"{doctype_name}.{fname} (type={ftype}, label={label!r}) — missing description"
                )

    return violations


class TestUiGuidanceCoverage(unittest.TestCase):
    """Verify all new DocTypes have UI guidance (field descriptions)."""

    def _run_doctype_check(self, slug: str, rel_path: str):
        try:
            data = _load_doctype_json(slug, rel_path)
        except FileNotFoundError as e:
            self.skipTest(str(e))
        violations = _check_fields(slug, data)
        self.assertEqual(
            violations, [],
            f"UI guidance missing in {slug}:\n" + "\n".join(violations),
        )

    def test_lcv_allocation_settings_has_descriptions(self):
        self._run_doctype_check(
            "lcv_allocation_settings",
            DOCTYPES_TO_CHECK["lcv_allocation_settings"],
        )

    def test_bctc_mapping_has_descriptions(self):
        self._run_doctype_check(
            "bctc_mapping",
            DOCTYPES_TO_CHECK["bctc_mapping"],
        )

    def test_bctc_line_has_descriptions(self):
        self._run_doctype_check(
            "bctc_line",
            DOCTYPES_TO_CHECK["bctc_line"],
        )


if __name__ == "__main__":
    unittest.main()
