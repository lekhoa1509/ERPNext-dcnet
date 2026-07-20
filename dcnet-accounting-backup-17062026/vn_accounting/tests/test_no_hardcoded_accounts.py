"""
Regression test: no hardcoded TK (account codes) in business logic Python files.

Rule: all TK must come from Settings DocTypes — never from string literals in
controller/helper code. Whitelist: lookup helpers with '# fallback default TT99/2025'
comment, test files themselves, fixture JSON files.

Scanned packages: landed_cost/, costing/, period_closing/, financial_reporting/
"""
import re
import os
import unittest


# Regex: 3-5 digit account code surrounded by quotes — e.g. "111", '6324', "15211"
ACCOUNT_CODE_RE = re.compile(r"""["']\b([1-9]\d{2,4})\b["']""")

# Directories to scan (relative to vn_accounting inner package root)
SCAN_DIRS = [
    "landed_cost",
    "costing",
    "period_closing",
    "financial_reporting",
]

# Patterns that indicate an allowed hardcoded code (lookup helper defaults)
WHITELIST_PATTERNS = [
    "# fallback default TT99/2025",
    "# default TT99/2025",
    "# default account",
    "# TT99 default",
    "# VN COA default",
    "TK label column",        # display-only column values in B09 generator
    "account_number",         # lookup filter — reads COA, not a GL posting
]

# Account codes that appear in translations, test fixtures, example strings — ignore
TRANSLATION_CONTEXTS = {
    "vi.csv",
    "test_",
    "_test",
    "fixtures/",
    ".json",
}


def _get_package_root() -> str:
    """Return the inner vn_accounting package root (where landed_cost/ etc live)."""
    this_file = os.path.abspath(__file__)
    # this_file: .../vn_accounting/vn_accounting/tests/test_no_hardcoded_accounts.py
    return os.path.dirname(os.path.dirname(this_file))  # up to vn_accounting/vn_accounting/


def _is_whitelisted_line(line: str) -> bool:
    """Return True if this line explicitly documents a TT99 default or is a comment."""
    stripped = line.strip()
    if stripped.startswith("#"):
        return True
    for pat in WHITELIST_PATTERNS:
        if pat in line:
            return True
    return False


def _scan_file(filepath: str) -> list:
    """Return list of (lineno, line) tuples with hardcoded account codes."""
    # Seed files ARE the TT99/2025 defaults — every TK in them is intentional
    basename = os.path.basename(filepath)
    if "seed" in basename or basename.endswith("_seed.py"):
        return []

    violations = []
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return violations

    for lineno, line in enumerate(lines, 1):
        if _is_whitelisted_line(line):
            continue
        # Only look at string literals, not identifiers or import paths
        if ACCOUNT_CODE_RE.search(line):
            violations.append((lineno, line.rstrip()))
    return violations


class TestNoHardcodedAccounts(unittest.TestCase):
    """Ensure no hardcoded account codes in business logic packages."""

    def test_no_hardcoded_tk_in_landed_cost(self):
        pkg_root = _get_package_root()
        violations = []
        scan_dir = os.path.join(pkg_root, "landed_cost")
        if not os.path.isdir(scan_dir):
            self.skipTest(f"landed_cost/ not found at {scan_dir}")
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "tests")]
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                if fname.startswith("test_"):
                    continue
                fpath = os.path.join(root, fname)
                found = _scan_file(fpath)
                for lineno, line in found:
                    rel = os.path.relpath(fpath, pkg_root)
                    violations.append(f"{rel}:{lineno}: {line}")
        self.assertEqual(
            violations, [],
            f"Hardcoded account codes found in landed_cost/:\n" + "\n".join(violations),
        )

    def test_no_hardcoded_tk_in_costing(self):
        pkg_root = _get_package_root()
        violations = []
        scan_dir = os.path.join(pkg_root, "costing")
        if not os.path.isdir(scan_dir):
            self.skipTest(f"costing/ not found at {scan_dir}")
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "tests")]
            for fname in files:
                if not fname.endswith(".py") or fname.startswith("test_"):
                    continue
                fpath = os.path.join(root, fname)
                found = _scan_file(fpath)
                for lineno, line in found:
                    rel = os.path.relpath(fpath, pkg_root)
                    violations.append(f"{rel}:{lineno}: {line}")
        self.assertEqual(
            violations, [],
            f"Hardcoded account codes found in costing/:\n" + "\n".join(violations),
        )

    def test_no_hardcoded_tk_in_period_closing(self):
        pkg_root = _get_package_root()
        violations = []
        scan_dir = os.path.join(pkg_root, "period_closing")
        if not os.path.isdir(scan_dir):
            self.skipTest(f"period_closing/ not found at {scan_dir}")
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "tests")]
            for fname in files:
                if not fname.endswith(".py") or fname.startswith("test_"):
                    continue
                fpath = os.path.join(root, fname)
                found = _scan_file(fpath)
                for lineno, line in found:
                    rel = os.path.relpath(fpath, pkg_root)
                    violations.append(f"{rel}:{lineno}: {line}")
        self.assertEqual(
            violations, [],
            f"Hardcoded account codes found in period_closing/:\n" + "\n".join(violations),
        )

    def test_no_hardcoded_tk_in_financial_reporting(self):
        pkg_root = _get_package_root()
        violations = []
        scan_dir = os.path.join(pkg_root, "financial_reporting")
        if not os.path.isdir(scan_dir):
            self.skipTest(f"financial_reporting/ not found at {scan_dir}")
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "tests")]
            for fname in files:
                if not fname.endswith(".py") or fname.startswith("test_"):
                    continue
                fpath = os.path.join(root, fname)
                found = _scan_file(fpath)
                for lineno, line in found:
                    rel = os.path.relpath(fpath, pkg_root)
                    violations.append(f"{rel}:{lineno}: {line}")
        self.assertEqual(
            violations, [],
            f"Hardcoded account codes found in financial_reporting/:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
