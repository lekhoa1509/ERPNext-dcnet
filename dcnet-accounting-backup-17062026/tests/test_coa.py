import json
import os
import pytest

COA_DIR = os.path.join(os.path.dirname(__file__), "..", "vn_accounting", "chart_of_accounts")


def _collect_account_numbers(tree, numbers=None):
    if numbers is None:
        numbers = []
    for key, value in tree.items():
        if isinstance(value, dict):
            if "account_number" in value:
                numbers.append(value["account_number"])
            _collect_account_numbers(value, numbers)
    return numbers


@pytest.mark.parametrize("filename", ["vn_large_enterprise.json", "vn_small_enterprise.json"])
def test_coa_structure(filename):
    filepath = os.path.join(COA_DIR, filename)
    with open(filepath) as f:
        coa = json.load(f)

    assert "tree" in coa, "Thiếu key 'tree'"
    assert "country_code" in coa, "Thiếu key 'country_code'"
    assert coa["country_code"] == "vn"

    # Mọi node gốc phải có root_type
    for name, node in coa["tree"].items():
        assert "root_type" in node, f"Node gốc '{name}' thiếu root_type"
        assert node["root_type"] in ("Asset", "Liability", "Equity", "Income", "Expense")

    # account_number không được trùng
    numbers = _collect_account_numbers(coa["tree"])
    duplicates = [n for n in numbers if numbers.count(n) > 1]
    assert len(duplicates) == 0, f"Trùng account_number: {set(duplicates)}"


def test_large_has_more_accounts_than_small():
    with open(os.path.join(COA_DIR, "vn_large_enterprise.json")) as f:
        large = json.load(f)
    with open(os.path.join(COA_DIR, "vn_small_enterprise.json")) as f:
        small = json.load(f)

    large_nums = _collect_account_numbers(large["tree"])
    small_nums = _collect_account_numbers(small["tree"])
    assert len(large_nums) > len(small_nums), "DN lớn phải có nhiều TK hơn DN nhỏ"


def test_large_has_manufacturing_accounts():
    """DN lớn phải có TK 621, 622, 627 (chi phí sản xuất chi tiết)."""
    with open(os.path.join(COA_DIR, "vn_large_enterprise.json")) as f:
        coa = json.load(f)
    numbers = _collect_account_numbers(coa["tree"])
    for tk in ["621", "622", "627"]:
        assert tk in numbers, f"DN lớn thiếu TK {tk}"


def test_small_no_manufacturing_accounts():
    """DN nhỏ không có TK 621, 622, 627."""
    with open(os.path.join(COA_DIR, "vn_small_enterprise.json")) as f:
        coa = json.load(f)
    numbers = _collect_account_numbers(coa["tree"])
    for tk in ["621", "622", "627"]:
        assert tk not in numbers, f"DN nhỏ không nên có TK {tk}"
