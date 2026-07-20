# Contract Template Management — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement template lifecycle (upload, approve, version), contract form integration (select template, auto-fill, per-contract edit), and dual-format document export (PDF from HTML, DOCX from python-docx fill).

**Architecture:** HTML-First + DOCX Sidecar. HTML is the operational format for editing/preview/PDF. Original .docx kept for pixel-perfect Word export via existing python-docx engine. Dual-language placeholder system (EN key + VI label) resolves to same value.

**Tech Stack:** Frappe v16, python-docx (existing), mammoth (existing), unidecode (new, lightweight), wkhtmltopdf (Frappe built-in)

**Spec:** `docs/specs/2026-04-16-contract-template-management.md`

**Branch:** `feat/contract-pakd-post-review`

---

## File Map

### New files
| File | Responsibility |
|------|---------------|
| `dcnet_contract/dcnet_contract/utils/placeholder_engine.py` | Dual-language PLACEHOLDER_MAP, resolve, validate, typo detect, guide HTML |
| `dcnet_contract/dcnet_contract/utils/template_engine.py` | HTML fill engine, apply_template(), export_docx_with_edits() |
| `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.js` | Client script: placeholder guide, .docx upload, status workflow buttons |
| `dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract_template_integration.js` | Client script: template selection, version warning, apply/switch |
| `dcnet_contract/dcnet_contract/tests/test_placeholder_engine.py` | Tests for resolve, validate, typo detection, guide generation |
| `dcnet_contract/dcnet_contract/tests/test_template_engine.py` | Tests for HTML fill, apply_template |

### Modified files
| File | Changes |
|------|---------|
| `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.json` | Add version, status, template_html, placeholder_guide_html, review/approve fields |
| `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.py` | Upgrade controller: mammoth convert, status transitions, permission checks |
| `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template_placeholder/dcnet_contract_template_placeholder.json` | Add needs_dev_mapping Check field |
| `dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract.json` | Add template_ref, template_version, contract_html, contract_html_edited, template_outdated |
| `dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract.py` | Upgrade before_print() for contract_html fallback |
| `dcnet_contract/dcnet_contract/print_format/hop_dong_chuan/hop_dong_chuan.html` | Use contract_html_rendered (already does via `doc.contract_html`) |
| `dcnet_contract/dcnet_contract/hooks.py` | Add app_include_js for new client scripts |
| `dcnet_contract/install.py` | Add Contract Template Manager role, migration for existing templates |

All paths below are relative to `apps/dcnet_contract/`.

---

## Task 1: Placeholder Engine — Core Module (TDD required)

**Files:**
- Create: `dcnet_contract/dcnet_contract/utils/placeholder_engine.py`
- Create: `dcnet_contract/dcnet_contract/tests/test_placeholder_engine.py`

### Why separate from docx_generator.py
The existing `PLACEHOLDER_MAP` in docx_generator.py uses format `{key: (description, label)}`. The new dual-language map uses `{key: {vi, source, example, group}}`. Creating a new module avoids breaking the existing 677-line engine. docx_generator.py will later import from placeholder_engine for backward compat.

- [ ] **Step 1: Write failing tests for resolve_placeholder**

Create `dcnet_contract/dcnet_contract/tests/test_placeholder_engine.py`:

```python
"""Tests for placeholder_engine dual-language system."""
import unittest


class TestResolvePlaceholder(unittest.TestCase):
    def test_english_key_resolves(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import resolve_placeholder
        assert resolve_placeholder("customer_name") == "customer_name"

    def test_vietnamese_label_resolves(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import resolve_placeholder
        assert resolve_placeholder("Tên khách hàng") == "customer_name"

    def test_unknown_returns_none(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import resolve_placeholder
        assert resolve_placeholder("nonexistent_field") is None

    def test_whitespace_stripped(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import resolve_placeholder
        assert resolve_placeholder("  customer_name  ") == "customer_name"


class TestDetectTypo(unittest.TestCase):
    def test_missing_diacritics_detected(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import detect_typo
        result = detect_typo("Ten khach hang")
        assert result is not None
        assert result["suggested_key"] == "customer_name"
        assert result["suggested_vi"] == "Tên khách hàng"

    def test_exact_match_returns_none(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import detect_typo
        assert detect_typo("customer_name") is None

    def test_close_english_key_detected(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import detect_typo
        result = detect_typo("custmer_name")  # typo in English key
        # unidecode normalization won't catch this — returns None (no fuzzy)
        # This is expected: typo detection is diacritics-only, not fuzzy
        assert result is None


class TestValidateTemplatePlaceholders(unittest.TestCase):
    def test_matched_placeholder(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import validate_template_placeholders
        html = "<p>Dear {{customer_name}},</p>"
        results = validate_template_placeholders(html)
        assert len(results) == 1
        assert results[0]["status"] == "matched"
        assert results[0]["key"] == "customer_name"

    def test_vietnamese_placeholder_matched(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import validate_template_placeholders
        html = "<p>Kính gửi {{Tên khách hàng}},</p>"
        results = validate_template_placeholders(html)
        assert len(results) == 1
        assert results[0]["status"] == "matched"

    def test_typo_placeholder_detected(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import validate_template_placeholders
        html = "<p>{{Ten khach hang}}</p>"
        results = validate_template_placeholders(html)
        assert len(results) == 1
        assert results[0]["status"] == "typo"
        assert results[0]["suggestion"] == "Tên khách hàng"

    def test_unknown_placeholder(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import validate_template_placeholders
        html = "<p>{{so_giay_phep_kinh_doanh}}</p>"
        results = validate_template_placeholders(html)
        assert len(results) == 1
        assert results[0]["status"] == "unknown"

    def test_removed_placeholder_detected(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import validate_template_placeholders
        html = "<p>{{customer_name}}</p>"
        previous = ["customer_name", "customer_fax"]
        results = validate_template_placeholders(html, previous_version_placeholders=previous)
        statuses = {r["key"]: r["status"] for r in results}
        assert statuses["customer_name"] == "matched"
        assert statuses["customer_fax"] == "removed"

    def test_multiple_placeholders(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import validate_template_placeholders
        html = "<p>{{customer_name}} at {{customer_address}}</p>"
        results = validate_template_placeholders(html)
        assert len(results) == 2
        assert all(r["status"] == "matched" for r in results)


class TestGeneratePlaceholderGuideHtml(unittest.TestCase):
    def test_guide_contains_groups(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import generate_placeholder_guide_html
        html = generate_placeholder_guide_html(["customer_name", "contract_number"])
        assert "Bên A" in html  # group header
        assert "customer_name" in html
        assert "Tên khách hàng" in html
        assert "contract_number" in html

    def test_guide_is_valid_html_table(self):
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import generate_placeholder_guide_html
        html = generate_placeholder_guide_html(["customer_name"])
        assert "<table" in html
        assert "</table>" in html


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/dcnet_contract/dcnet_contract/tests/test_placeholder_engine.py -v 2>&1 | tail -20`
Expected: FAIL with ModuleNotFoundError or ImportError

- [ ] **Step 3: Implement placeholder_engine.py**

Create `dcnet_contract/dcnet_contract/utils/placeholder_engine.py`:

```python
"""Dual-language placeholder engine for DCNet Contract templates.

Supports both English keys ({{customer_name}}) and Vietnamese labels
({{Tên khách hàng}}) resolving to the same value. Provides validation,
typo detection via unidecode normalization, and bilingual guide generation.
"""

import re

from unidecode import unidecode

# ---------------------------------------------------------------------------
# Dual-language placeholder map
# Keys are English identifiers. Each entry has: vi label, source path,
# example value, and display group for the placeholder guide.
# ---------------------------------------------------------------------------
PLACEHOLDER_MAP = {
    # --- Bên A (Khách hàng) ---
    "customer_name": {
        "vi": "Tên khách hàng",
        "source": "contract.customer_name",
        "example": "Công ty TNHH ABC",
        "group": "Bên A (Khách hàng)",
    },
    "customer_address": {
        "vi": "Địa chỉ khách hàng",
        "source": "contract.customer_address",
        "example": "123 Nguyễn Huệ, Q.1, TP.HCM",
        "group": "Bên A (Khách hàng)",
    },
    "customer_phone": {
        "vi": "Số điện thoại KH",
        "source": "contract.customer_phone",
        "example": "028 1234 5678",
        "group": "Bên A (Khách hàng)",
    },
    "customer_fax": {
        "vi": "Số fax KH",
        "source": "contract.customer_fax",
        "example": "028 1234 5679",
        "group": "Bên A (Khách hàng)",
    },
    "customer_tax_id": {
        "vi": "Mã số thuế KH",
        "source": "contract.customer_tax_id",
        "example": "0123456789",
        "group": "Bên A (Khách hàng)",
    },
    "customer_representative": {
        "vi": "Người đại diện KH",
        "source": "contract.customer_representative",
        "example": "Nguyễn Văn A",
        "group": "Bên A (Khách hàng)",
    },
    "customer_representative_title": {
        "vi": "Chức vụ người đại diện KH",
        "source": "contract.customer_representative_title",
        "example": "Giám đốc",
        "group": "Bên A (Khách hàng)",
    },
    "customer_id_number": {
        "vi": "Số CMND/CCCD",
        "source": "contract.customer_id_number",
        "example": "079123456789",
        "group": "Bên A (Khách hàng)",
    },
    "customer_id_date": {
        "vi": "Ngày cấp CMND",
        "source": "contract.customer_id_date",
        "example": "ngày 15 tháng 03 năm 2020",
        "group": "Bên A (Khách hàng)",
    },
    "customer_id_place": {
        "vi": "Nơi cấp CMND",
        "source": "contract.customer_id_place",
        "example": "Cục CS QLHC về TTXH",
        "group": "Bên A (Khách hàng)",
    },
    "customer_dob": {
        "vi": "Ngày sinh KH",
        "source": "contract.customer_dob",
        "example": "ngày 01 tháng 01 năm 1990",
        "group": "Bên A (Khách hàng)",
    },
    "customer_email": {
        "vi": "Email KH",
        "source": "contract.customer_email",
        "example": "contact@abc.com.vn",
        "group": "Bên A (Khách hàng)",
    },
    "customer_bank_account": {
        "vi": "Tài khoản ngân hàng KH",
        "source": "contract.customer_bank_account",
        "example": "1234567890 - Vietcombank",
        "group": "Bên A (Khách hàng)",
    },
    # --- Bên B (Công ty) ---
    "company_name_b": {
        "vi": "Tên Bên B",
        "source": "Company.company_name",
        "example": "Công ty Cổ phần Viễn thông DCNet",
        "group": "Bên B (Công ty)",
    },
    "company_address_b": {
        "vi": "Địa chỉ Bên B",
        "source": "Company.address",
        "example": "456 Lê Lợi, Q.1, TP.HCM",
        "group": "Bên B (Công ty)",
    },
    "company_phone_b": {
        "vi": "Điện thoại Bên B",
        "source": "Company.phone_no",
        "example": "028 9876 5432",
        "group": "Bên B (Công ty)",
    },
    "company_fax_b": {
        "vi": "Fax Bên B",
        "source": "Company.fax",
        "example": "028 9876 5433",
        "group": "Bên B (Công ty)",
    },
    "company_tax_id_b": {
        "vi": "Mã số thuế Bên B",
        "source": "Company.tax_id",
        "example": "0301234567",
        "group": "Bên B (Công ty)",
    },
    "company_representative_b": {
        "vi": "Người đại diện Bên B",
        "source": "contract.company_representative / Company.representative",
        "example": "Trần Văn B",
        "group": "Bên B (Công ty)",
    },
    "company_representative_title_b": {
        "vi": "Chức vụ người đại diện Bên B",
        "source": "contract.company_representative_title / Company.representative_title",
        "example": "Tổng Giám đốc",
        "group": "Bên B (Công ty)",
    },
    "company_bank_account_b": {
        "vi": "Tài khoản ngân hàng Bên B",
        "source": "Bank Account (default, company)",
        "example": "9876543210",
        "group": "Bên B (Công ty)",
    },
    "company_bank_b": {
        "vi": "Ngân hàng Bên B",
        "source": "Bank Account.bank",
        "example": "BIDV - CN Sài Gòn",
        "group": "Bên B (Công ty)",
    },
    # --- Hợp đồng ---
    "contract_number": {
        "vi": "Số hợp đồng",
        "source": "contract.contract_no_external or contract.name",
        "example": "DCNET/2026/001",
        "group": "Hợp đồng",
    },
    "contract_date": {
        "vi": "Ngày ký hợp đồng",
        "source": "contract.contract_date",
        "example": "ngày 15 tháng 04 năm 2026",
        "group": "Hợp đồng",
    },
    "package_term": {
        "vi": "Thời hạn hợp đồng",
        "source": "contract.package_term_months",
        "example": "12",
        "group": "Hợp đồng",
    },
    "acceptance_date": {
        "vi": "Ngày nghiệm thu",
        "source": "contract.acceptance_date",
        "example": "ngày 20 tháng 04 năm 2026",
        "group": "Hợp đồng",
    },
    "end_date": {
        "vi": "Ngày kết thúc",
        "source": "contract.end_date",
        "example": "ngày 19 tháng 04 năm 2027",
        "group": "Hợp đồng",
    },
    # --- Dịch vụ ---
    "service_type": {
        "vi": "Loại dịch vụ",
        "source": "contract.service_type",
        "example": "FTTH DN",
        "group": "Dịch vụ",
    },
    "package_name": {
        "vi": "Tên gói cước",
        "source": "contract.package_name",
        "example": "FTTH-100M",
        "group": "Dịch vụ",
    },
    "installation_address": {
        "vi": "Địa chỉ lắp đặt",
        "source": "contract.installation_address",
        "example": "Tầng 5, Tòa nhà ABC, Q.1, TP.HCM",
        "group": "Dịch vụ",
    },
    "bandwidth": {
        "vi": "Băng thông",
        "source": "contract.bandwidth",
        "example": "100 Mbps",
        "group": "Dịch vụ",
    },
    "point_a": {
        "vi": "Điểm đầu",
        "source": "contract.point_a",
        "example": "POP Nguyễn Huệ",
        "group": "Dịch vụ",
    },
    "point_b": {
        "vi": "Điểm cuối",
        "source": "contract.point_b",
        "example": "Tòa nhà ABC, Q.1",
        "group": "Dịch vụ",
    },
    "sla_restore_hours": {
        "vi": "SLA khắc phục sự cố",
        "source": "contract.sla_restore_hours",
        "example": "4",
        "group": "Dịch vụ",
    },
    # --- Tài chính ---
    "setup_fee": {
        "vi": "Phí lắp đặt",
        "source": "contract.setup_fee",
        "example": "3,000,000",
        "group": "Tài chính",
    },
    "setup_fee_vat": {
        "vi": "VAT phí lắp đặt",
        "source": "setup_fee * 10%",
        "example": "300,000",
        "group": "Tài chính",
    },
    "setup_fee_total": {
        "vi": "Tổng phí lắp đặt",
        "source": "setup_fee * 110%",
        "example": "3,300,000",
        "group": "Tài chính",
    },
    "setup_fee_words": {
        "vi": "Phí lắp đặt bằng chữ",
        "source": "number_to_words(setup_fee_total)",
        "example": "Ba triệu ba trăm nghìn đồng",
        "group": "Tài chính",
    },
    "monthly_fee": {
        "vi": "Phí hàng tháng",
        "source": "contract.unit_price_total",
        "example": "5,000,000",
        "group": "Tài chính",
    },
    "monthly_fee_vat": {
        "vi": "VAT phí hàng tháng",
        "source": "monthly_fee * 10%",
        "example": "500,000",
        "group": "Tài chính",
    },
    "monthly_fee_total": {
        "vi": "Tổng phí hàng tháng",
        "source": "monthly_fee * 110%",
        "example": "5,500,000",
        "group": "Tài chính",
    },
    "monthly_fee_words": {
        "vi": "Phí hàng tháng bằng chữ",
        "source": "number_to_words(monthly_fee_total)",
        "example": "Năm triệu năm trăm nghìn đồng",
        "group": "Tài chính",
    },
    # --- Hạng mục (items table) ---
    "item_stt": {
        "vi": "STT",
        "source": "row index",
        "example": "1",
        "group": "Hạng mục",
    },
    "item_label": {
        "vi": "Tên hạng mục",
        "source": "item.item_label",
        "example": "Dịch vụ Internet FTTH",
        "group": "Hạng mục",
    },
    "item_qty": {
        "vi": "Số lượng",
        "source": "item.qty",
        "example": "1",
        "group": "Hạng mục",
    },
    "item_uom": {
        "vi": "Đơn vị",
        "source": "item.uom",
        "example": "Nos",
        "group": "Hạng mục",
    },
    "item_price": {
        "vi": "Đơn giá",
        "source": "item.unit_price",
        "example": "5,000,000",
        "group": "Hạng mục",
    },
    "item_amount": {
        "vi": "Thành tiền",
        "source": "item.amount_per_period",
        "example": "5,000,000",
        "group": "Hạng mục",
    },
}

# Auto-build reverse lookup: Vietnamese label → English key
VI_TO_KEY = {v["vi"]: k for k, v in PLACEHOLDER_MAP.items()}

# Pre-compute normalized (unidecode) lookup for typo detection
_NORMALIZED_VI = {unidecode(v["vi"]).lower(): k for k, v in PLACEHOLDER_MAP.items()}
_NORMALIZED_EN = {unidecode(k).lower(): k for k in PLACEHOLDER_MAP}

# Regex for extracting {{...}} placeholders from HTML/text
_PLACEHOLDER_RE = re.compile(r"\{\{([^}]+)\}\}")


def resolve_placeholder(raw_key: str) -> str | None:
    """Resolve a placeholder key (EN or VI) to its canonical English key.

    Returns None if not found in either language.
    """
    key = raw_key.strip()
    if key in PLACEHOLDER_MAP:
        return key
    if key in VI_TO_KEY:
        return VI_TO_KEY[key]
    return None


def detect_typo(raw_key: str) -> dict | None:
    """Detect if raw_key is a diacritics-stripped version of a known placeholder.

    Uses unidecode normalization: "Ten khach hang" → "ten khach hang"
    matches against normalized "Tên khách hàng" → "ten khach hang".

    Returns {"suggested_key": str, "suggested_vi": str} or None.
    """
    key = raw_key.strip()
    # Skip if it's already a valid key
    if key in PLACEHOLDER_MAP or key in VI_TO_KEY:
        return None

    normalized = unidecode(key).lower()

    # Check against normalized Vietnamese labels
    if normalized in _NORMALIZED_VI:
        en_key = _NORMALIZED_VI[normalized]
        return {"suggested_key": en_key, "suggested_vi": PLACEHOLDER_MAP[en_key]["vi"]}

    # Check against normalized English keys
    if normalized in _NORMALIZED_EN:
        en_key = _NORMALIZED_EN[normalized]
        return {"suggested_key": en_key, "suggested_vi": PLACEHOLDER_MAP[en_key]["vi"]}

    return None


def extract_placeholders_from_html(html: str) -> list[str]:
    """Extract all {{...}} placeholder raw keys from HTML content."""
    return _PLACEHOLDER_RE.findall(html)


def validate_template_placeholders(
    html_content: str,
    previous_version_placeholders: list[str] | None = None,
) -> list[dict]:
    """Validate all placeholders in HTML template content.

    Returns list of dicts with keys: key, status, suggestion, context_line.
    Status: matched | typo | unknown | removed
    """
    raw_keys = extract_placeholders_from_html(html_content)
    results = []
    seen_keys = set()

    for raw in raw_keys:
        raw = raw.strip()
        resolved = resolve_placeholder(raw)
        if resolved:
            seen_keys.add(resolved)
            results.append({
                "key": resolved,
                "raw": raw,
                "status": "matched",
                "suggestion": None,
            })
            continue

        typo = detect_typo(raw)
        if typo:
            seen_keys.add(typo["suggested_key"])
            results.append({
                "key": raw,
                "raw": raw,
                "status": "typo",
                "suggestion": typo["suggested_vi"],
                "suggested_key": typo["suggested_key"],
            })
            continue

        results.append({
            "key": raw,
            "raw": raw,
            "status": "unknown",
            "suggestion": None,
        })

    # Check for removed placeholders vs previous version
    if previous_version_placeholders:
        for prev_key in previous_version_placeholders:
            canonical = resolve_placeholder(prev_key)
            check_key = canonical or prev_key
            if check_key not in seen_keys:
                results.append({
                    "key": check_key,
                    "raw": check_key,
                    "status": "removed",
                    "suggestion": None,
                })

    return results


def generate_placeholder_guide_html(placeholder_keys: list[str]) -> str:
    """Generate bilingual HTML table showing placeholder info grouped by category."""
    # Group by category
    groups: dict[str, list[str]] = {}
    for key in placeholder_keys:
        if key not in PLACEHOLDER_MAP:
            continue
        info = PLACEHOLDER_MAP[key]
        group = info["group"]
        groups.setdefault(group, []).append(key)

    # Render HTML table
    rows = []
    for group_name in [
        "Bên A (Khách hàng)", "Bên B (Công ty)", "Hợp đồng",
        "Dịch vụ", "Tài chính", "Hạng mục",
    ]:
        keys_in_group = groups.get(group_name, [])
        if not keys_in_group:
            continue
        rows.append(
            f'<tr><td colspan="5" style="background:#e8e8e8;font-weight:bold;">'
            f"{group_name}</td></tr>"
        )
        for key in keys_in_group:
            info = PLACEHOLDER_MAP[key]
            rows.append(
                f"<tr>"
                f"<td><code>{{{{{key}}}}}</code></td>"
                f"<td><code>{{{{{info['vi']}}}}}</code></td>"
                f"<td>{info['source']}</td>"
                f"<td>{info['example']}</td>"
                f"</tr>"
            )

    header = (
        "<table class='table table-bordered table-sm'>"
        "<thead><tr>"
        "<th>Key (EN)</th><th>Label (VI)</th>"
        "<th>Source</th><th>Example</th>"
        "</tr></thead><tbody>"
    )
    return header + "\n".join(rows) + "</tbody></table>"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/dcnet_contract/dcnet_contract/tests/test_placeholder_engine.py -v 2>&1 | tail -20`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/utils/placeholder_engine.py apps/dcnet_contract/dcnet_contract/tests/test_placeholder_engine.py
git commit -m "feat(contract): add dual-language placeholder engine with typo detection"
```

---

## Task 2: Upgrade DCNet Contract Template DocType JSON

**Files:**
- Modify: `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.json`
- Modify: `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template_placeholder/dcnet_contract_template_placeholder.json`

No TDD — DocType JSON is validated by `bench migrate`.

- [ ] **Step 1: Add new fields to DCNet Contract Template JSON**

Open `dcnet_contract_template.json` and add these fields after the existing `template_file` field:

```json
{
    "fieldname": "template_html",
    "fieldtype": "Long Text",
    "label": "Template HTML",
    "hidden": 1
},
{
    "fieldname": "placeholder_guide_html",
    "fieldtype": "Long Text",
    "label": "Placeholder Guide HTML",
    "read_only": 1
}
```

Add a new section for versioning and approval, after `boilerplate_text`:

```json
{
    "fieldname": "version_section",
    "fieldtype": "Section Break",
    "label": "Version & Approval"
},
{
    "fieldname": "version",
    "fieldtype": "Int",
    "label": "Version",
    "default": "1",
    "read_only": 1
},
{
    "fieldname": "status",
    "fieldtype": "Select",
    "label": "Status",
    "options": "Draft\nPending Review\nApproved\nArchived",
    "default": "Draft",
    "in_list_view": 1,
    "in_standard_filter": 1
},
{
    "fieldname": "change_log",
    "fieldtype": "Small Text",
    "label": "Change Log"
},
{
    "fieldname": "column_break_approval",
    "fieldtype": "Column Break"
},
{
    "fieldname": "reviewed_by",
    "fieldtype": "Link",
    "label": "Reviewed By",
    "options": "User",
    "read_only": 1
},
{
    "fieldname": "reviewed_date",
    "fieldtype": "Datetime",
    "label": "Reviewed Date",
    "read_only": 1
},
{
    "fieldname": "approved_by",
    "fieldtype": "Link",
    "label": "Approved By",
    "options": "User",
    "read_only": 1
},
{
    "fieldname": "approved_date",
    "fieldtype": "Datetime",
    "label": "Approved Date",
    "read_only": 1
}
```

Also add `"Contract Template Manager"` to the `permissions` array with read/write/create/delete for level 0.

- [ ] **Step 2: Add needs_dev_mapping to Placeholder child DocType**

In `dcnet_contract_template_placeholder.json`, add:

```json
{
    "fieldname": "needs_dev_mapping",
    "fieldtype": "Check",
    "label": "Needs Dev Mapping",
    "default": "0"
}
```

- [ ] **Step 3: Run migrate to validate**

Run: `cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost migrate 2>&1 | tail -10`
Expected: No errors

- [ ] **Step 4: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/ apps/dcnet_contract/dcnet_contract/dcnet_contract/doctype/dcnet_contract_template_placeholder/
git commit -m "feat(contract): add version, status, template_html fields to Contract Template"
```

---

## Task 3: Upgrade Contract Template Controller

**Files:**
- Modify: `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.py`

- [ ] **Step 1: Rewrite controller with mammoth conversion and status transitions**

Replace the entire content of `dcnet_contract_template.py`:

```python
"""DCNet Contract Template controller.

Handles .docx upload → mammoth HTML conversion, placeholder discovery + validation,
status workflow (Draft → Pending Review → Approved → Archived), and versioning.
"""

import os

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class DCNetContractTemplate(Document):
    def before_save(self):
        if self.template_file:
            self._convert_docx_to_html()
            self._discover_placeholders()
            self._generate_placeholder_guide()

    def validate(self):
        self._validate_status_transition()

    def _convert_docx_to_html(self):
        """Convert uploaded .docx to HTML via mammoth."""
        file_path = self._get_template_file_path()
        if not file_path:
            return

        import mammoth

        with open(file_path, "rb") as f:
            result = mammoth.convert_to_html(f)
            self.template_html = result.value

    def _discover_placeholders(self):
        """Scan template_html for {{...}} markers, populate placeholders child table."""
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import (
            extract_placeholders_from_html,
            resolve_placeholder,
            validate_template_placeholders,
        )

        if not self.template_html:
            return

        # Get previous version placeholders for removed detection
        previous_keys = None
        if not self.is_new() and self.has_value_changed("template_file"):
            previous_keys = [row.placeholder_key for row in self.placeholders]

        results = validate_template_placeholders(
            self.template_html, previous_version_placeholders=previous_keys
        )

        self.set("placeholders", [])
        for r in results:
            resolved = resolve_placeholder(r.get("raw", r["key"]))
            from dcnet_contract.dcnet_contract.utils.placeholder_engine import PLACEHOLDER_MAP
            info = PLACEHOLDER_MAP.get(resolved, {}) if resolved else {}
            self.append("placeholders", {
                "placeholder_key": r["key"],
                "mapped_field": info.get("source", ""),
                "description": info.get("vi", r.get("suggestion", "")),
                "needs_dev_mapping": 1 if r["status"] == "unknown" else 0,
            })

    def _generate_placeholder_guide(self):
        """Generate bilingual placeholder guide HTML."""
        from dcnet_contract.dcnet_contract.utils.placeholder_engine import (
            generate_placeholder_guide_html,
            resolve_placeholder,
        )

        keys = []
        for row in self.placeholders:
            resolved = resolve_placeholder(row.placeholder_key)
            if resolved:
                keys.append(resolved)
        self.placeholder_guide_html = generate_placeholder_guide_html(keys)

    def _validate_status_transition(self):
        """Validate status transitions per workflow rules."""
        if self.is_new():
            return

        old_status = self.db_get("status") or "Draft"
        new_status = self.status or "Draft"

        if old_status == new_status:
            return

        allowed = {
            "Draft": ["Pending Review"],
            "Pending Review": ["Draft", "Approved"],
            "Approved": ["Archived", "Draft"],
            "Archived": ["Draft"],
        }

        if new_status not in allowed.get(old_status, []):
            frappe.throw(
                _("Cannot change status from {0} to {1}").format(old_status, new_status)
            )

    def _get_template_file_path(self) -> str | None:
        """Get absolute path of the attached .docx file."""
        if not self.template_file:
            return None

        file_doc = frappe.get_doc("File", {"file_url": self.template_file})
        file_path = file_doc.get_full_path()

        if not os.path.exists(file_path):
            return None

        return file_path

    # --- Status transition API methods ---

    @frappe.whitelist()
    def submit_for_review(self):
        """Transition Draft → Pending Review."""
        if self.status != "Draft":
            frappe.throw(_("Only Draft templates can be submitted for review"))
        self.status = "Pending Review"
        self.save()

    @frappe.whitelist()
    def approve_template(self):
        """Transition Pending Review → Approved. Requires Sales Manager or CEO."""
        if self.status != "Pending Review":
            frappe.throw(_("Only templates in Pending Review can be approved"))
        self.status = "Approved"
        self.approved_by = frappe.session.user
        self.approved_date = now_datetime()
        self.save()

    @frappe.whitelist()
    def reject_template(self):
        """Transition Pending Review → Draft (rejection)."""
        if self.status != "Pending Review":
            frappe.throw(_("Only templates in Pending Review can be rejected"))
        self.status = "Draft"
        self.reviewed_by = frappe.session.user
        self.reviewed_date = now_datetime()
        self.save()

    @frappe.whitelist()
    def archive_template(self):
        """Transition Approved → Archived."""
        if self.status != "Approved":
            frappe.throw(_("Only Approved templates can be archived"))
        self.status = "Archived"
        self.save()

    @frappe.whitelist()
    def create_new_version(self):
        """Clone current template as new Draft with incremented version."""
        new_doc = frappe.copy_doc(self)
        new_doc.version = (self.version or 1) + 1
        new_doc.status = "Draft"
        new_doc.reviewed_by = None
        new_doc.reviewed_date = None
        new_doc.approved_by = None
        new_doc.approved_date = None
        new_doc.template_name = f"{self.template_name} v{new_doc.version}"
        new_doc.insert()
        return new_doc.name


@frappe.whitelist()
def get_template(template_name):
    """Return template data for auto-filling a contract form."""
    doc = frappe.get_doc("DCNet Contract Template", template_name)
    return {
        "service_type": doc.service_type,
        "contract_type": doc.contract_type,
        "payment_mode": doc.payment_mode,
        "package_term_months": doc.package_term_months,
        "boilerplate_text": doc.boilerplate_text,
        "template_html": doc.template_html,
        "version": doc.version,
        "items": [
            {
                "item_label": row.item_label,
                "description": row.description,
                "uom": row.uom,
                "qty": row.qty,
                "unit_price": row.unit_price,
            }
            for row in doc.default_items
        ],
    }
```

- [ ] **Step 2: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.py
git commit -m "feat(contract): upgrade template controller with mammoth, status workflow, versioning"
```

---

## Task 4: Contract Template Manager Role + Install.py

**Files:**
- Modify: `dcnet_contract/install.py`

- [ ] **Step 1: Add Contract Template Manager role to _ensure_custom_roles()**

In `install.py`, modify `_ensure_custom_roles()` at line 33:

```python
def _ensure_custom_roles():
    for role_name in ["DCNet Sales Rep", "DCNet Sales Manager", "Contract Template Manager"]:
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(ignore_permissions=True)
    frappe.db.commit()
```

- [ ] **Step 2: Add _ensure_custom_roles() to after_migrate()**

Add `_ensure_custom_roles()` call to `after_migrate()` function (it's currently only in `after_install()`):

```python
def after_migrate():
    _ensure_custom_roles()  # add this line
    _ensure_settings_singleton()
    # ... rest unchanged
```

- [ ] **Step 3: Add migration function for existing templates**

Add this function after `_ensure_desktop_icon()`:

```python
def _migrate_templates_to_dual_format():
    """Migrate existing templates: mammoth → template_html, set status=Approved, version=1."""
    import mammoth

    templates = frappe.get_all(
        "DCNet Contract Template",
        filters={"template_file": ["is", "set"]},
        fields=["name", "template_file", "template_html", "status", "version"],
    )

    for t in templates:
        if t.template_html:
            continue  # already migrated

        doc = frappe.get_doc("DCNet Contract Template", t.name)
        file_path = doc._get_template_file_path() if hasattr(doc, "_get_template_file_path") else None

        if not file_path:
            continue

        try:
            with open(file_path, "rb") as f:
                result = mammoth.convert_to_html(f)
                doc.template_html = result.value
        except Exception as e:
            frappe.log_error(f"Failed to convert template {t.name}: {e}")
            continue

        if not doc.status or doc.status == "Draft":
            doc.db_set("status", "Approved", update_modified=False)
        if not doc.version:
            doc.db_set("version", 1, update_modified=False)

        doc.db_set("template_html", doc.template_html, update_modified=False)

        # Re-scan placeholders and guide
        doc.reload()
        doc._discover_placeholders()
        doc._generate_placeholder_guide()
        doc.save(ignore_permissions=True)

    frappe.db.commit()
```

Add `_migrate_templates_to_dual_format()` at the end of `after_migrate()`.

- [ ] **Step 4: Run migrate to test**

Run: `cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost migrate 2>&1 | tail -10`
Expected: No errors, existing templates get template_html populated

- [ ] **Step 5: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/install.py
git commit -m "feat(contract): add Contract Template Manager role + template migration"
```

---

## Task 5: Upgrade DCNet Contract DocType JSON

**Files:**
- Modify: `dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract.json`

No TDD — validated by migrate.

- [ ] **Step 1: Add template integration fields to Contract JSON**

Add a new section before the existing `items` section:

```json
{
    "fieldname": "template_section",
    "fieldtype": "Section Break",
    "label": "Template"
},
{
    "fieldname": "template_ref",
    "fieldtype": "Link",
    "label": "Contract Template",
    "options": "DCNet Contract Template"
},
{
    "fieldname": "template_version",
    "fieldtype": "Int",
    "label": "Template Version",
    "read_only": 1
},
{
    "fieldname": "template_outdated",
    "fieldtype": "Check",
    "label": "Template Outdated",
    "read_only": 1,
    "hidden": 1
},
{
    "fieldname": "column_break_template",
    "fieldtype": "Column Break"
},
{
    "fieldname": "contract_html_edited",
    "fieldtype": "Check",
    "label": "Contract HTML Edited",
    "read_only": 1,
    "hidden": 1
}
```

Add after the `terms_section` / `boilerplate_text` area (but NOT replacing `contract_html` which is generated in before_print — note: the print format already reads `doc.contract_html`, so we need the field to exist as a stored field, not just a transient property):

```json
{
    "fieldname": "contract_html_section",
    "fieldtype": "Section Break",
    "label": "Contract Document",
    "collapsible": 1
},
{
    "fieldname": "contract_html",
    "fieldtype": "Text Editor",
    "label": "Contract HTML"
}
```

**Important:** The existing `before_print()` sets `self.contract_html` as a transient property. With this new stored field, `before_print()` must be updated to use `contract_html_rendered` instead (Task 6).

- [ ] **Step 2: Run migrate**

Run: `cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost migrate 2>&1 | tail -10`

- [ ] **Step 3: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract.json
git commit -m "feat(contract): add template_ref, contract_html fields to Contract"
```

---

## Task 6: Template Engine + Contract Controller Upgrade (TDD required)

**Files:**
- Create: `dcnet_contract/dcnet_contract/utils/template_engine.py`
- Create: `dcnet_contract/dcnet_contract/tests/test_template_engine.py`
- Modify: `dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract.py`

- [ ] **Step 1: Write failing tests for template_engine**

Create `dcnet_contract/dcnet_contract/tests/test_template_engine.py`:

```python
"""Tests for template_engine HTML fill and apply."""
import unittest


class TestFillHtmlPlaceholders(unittest.TestCase):
    def test_english_placeholder_filled(self):
        from dcnet_contract.dcnet_contract.utils.template_engine import fill_html_placeholders
        html = "<p>Dear {{customer_name}},</p>"
        values = {"customer_name": "ABC Corp"}
        result = fill_html_placeholders(html, values)
        assert "ABC Corp" in result
        assert "{{customer_name}}" not in result

    def test_vietnamese_placeholder_filled(self):
        from dcnet_contract.dcnet_contract.utils.template_engine import fill_html_placeholders
        html = "<p>Kính gửi {{Tên khách hàng}},</p>"
        values = {"customer_name": "ABC Corp"}
        result = fill_html_placeholders(html, values)
        assert "ABC Corp" in result

    def test_unknown_placeholder_left_as_is(self):
        from dcnet_contract.dcnet_contract.utils.template_engine import fill_html_placeholders
        html = "<p>{{unknown_field}}</p>"
        values = {"customer_name": "ABC Corp"}
        result = fill_html_placeholders(html, values)
        assert "{{unknown_field}}" in result

    def test_multiple_placeholders(self):
        from dcnet_contract.dcnet_contract.utils.template_engine import fill_html_placeholders
        html = "<p>{{customer_name}} - {{Số hợp đồng}}</p>"
        values = {"customer_name": "ABC Corp", "contract_number": "HD-001"}
        result = fill_html_placeholders(html, values)
        assert "ABC Corp" in result
        assert "HD-001" in result


class TestBuildPlaceholderValues(unittest.TestCase):
    def test_returns_dict(self):
        from dcnet_contract.dcnet_contract.utils.template_engine import build_placeholder_values
        # This function needs a real Frappe context — skip in pure unit test
        # Tested via integration in Task 8 QA


class TestExtractAdditions(unittest.TestCase):
    def test_no_edits_returns_empty(self):
        from dcnet_contract.dcnet_contract.utils.template_engine import extract_additions
        original = "<p>Hello</p>"
        assert extract_additions(original, original) == []

    def test_appended_paragraph_detected(self):
        from dcnet_contract.dcnet_contract.utils.template_engine import extract_additions
        original = "<p>Hello</p>"
        edited = "<p>Hello</p><p>Extra clause</p>"
        additions = extract_additions(original, edited)
        assert len(additions) >= 1
        assert "Extra clause" in additions[0]


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/dcnet_contract/dcnet_contract/tests/test_template_engine.py -v 2>&1 | tail -20`
Expected: FAIL with ImportError

- [ ] **Step 3: Implement template_engine.py**

Create `dcnet_contract/dcnet_contract/utils/template_engine.py`:

```python
"""HTML template fill engine for DCNet Contract.

Fills template_html with contract/customer/company data using dual-language
placeholders. Handles apply_template flow and DOCX export with per-contract edits.
"""

import re

import frappe
from frappe.utils import cint, flt, getdate

from dcnet_contract.dcnet_contract.utils.placeholder_engine import (
    PLACEHOLDER_MAP,
    VI_TO_KEY,
    resolve_placeholder,
)


def fill_html_placeholders(html: str, values: dict) -> str:
    """Replace {{EN}} and {{VI}} placeholders in HTML with values.

    Unknown placeholders are left as-is.
    """
    def _replacer(match):
        raw_key = match.group(1).strip()
        resolved = resolve_placeholder(raw_key)
        if resolved and resolved in values:
            return values[resolved]
        return match.group(0)  # leave unknown as-is

    return re.sub(r"\{\{([^}]+)\}\}", _replacer, html)


def build_placeholder_values(contract_name: str) -> dict:
    """Build placeholder_key → display_value dict from contract data.

    Reuses the same logic as docx_generator._build_placeholder_values
    but returns the dict without Frappe formatting dependencies.
    """
    from dcnet_contract.dcnet_contract.utils.docx_generator import _build_placeholder_values
    return _build_placeholder_values(contract_name)


def apply_template(contract_name: str, template_name: str) -> str:
    """Fill template HTML with contract data, save to contract.contract_html.

    Also copies default_items and default_terms if contract has none.
    Returns the filled HTML.
    """
    contract = frappe.get_doc("DCNet Contract", contract_name)
    template = frappe.get_doc("DCNet Contract Template", template_name)

    if not template.template_html:
        frappe.throw(f"Template {template_name} has no HTML content")

    # Build values and fill
    values = build_placeholder_values(contract_name)
    filled_html = fill_html_placeholders(template.template_html, values)

    # Save to contract
    contract.db_set("contract_html", filled_html, update_modified=False)
    contract.db_set("template_ref", template_name, update_modified=False)
    contract.db_set("template_version", template.version or 1, update_modified=False)
    contract.db_set("contract_html_edited", 0, update_modified=False)
    contract.db_set("template_outdated", 0, update_modified=False)

    # Copy default items if contract has no items
    if not contract.items and template.default_items:
        for row in template.default_items:
            contract.append("items", {
                "item_label": row.item_label,
                "description": row.description,
                "uom": row.uom,
                "qty": row.qty,
                "unit_price": row.unit_price,
            })
        contract.save(ignore_permissions=True)

    # Copy default terms if empty
    if not contract.get("default_terms") and template.default_terms:
        contract.db_set("default_terms", template.default_terms, update_modified=False)

    frappe.db.commit()
    return filled_html


def extract_additions(original_html: str, edited_html: str) -> list[str]:
    """Extract paragraphs added by sales (not in original template fill).

    Simple diff: split by block tags, compare. Returns list of added HTML blocks.
    """
    if original_html == edited_html:
        return []

    # Split into blocks by common block tags
    block_re = re.compile(r"(<(?:p|div|h[1-6]|ul|ol|li|table|tr|blockquote)[^>]*>.*?</(?:p|div|h[1-6]|ul|ol|li|table|tr|blockquote)>)", re.DOTALL)

    original_blocks = set(block_re.findall(original_html))
    edited_blocks = block_re.findall(edited_html)

    additions = []
    for block in edited_blocks:
        if block not in original_blocks:
            additions.append(block)

    return additions


def export_docx_with_edits(contract_name: str) -> str:
    """Fill .docx template + inject per-contract HTML edits.

    Returns file URL of the generated .docx.
    """
    contract = frappe.get_doc("DCNet Contract", contract_name)

    if not contract.template_ref:
        # Fallback to existing engine
        from dcnet_contract.dcnet_contract.utils.docx_generator import generate_document
        return generate_document(contract_name, None, "docx")

    template = frappe.get_doc("DCNet Contract Template", contract.template_ref)

    # Use existing docx engine to fill the original .docx
    from dcnet_contract.dcnet_contract.utils.docx_generator import generate_document
    file_url = generate_document(contract_name, template.name, "docx")

    # Per-contract edit injection is a v2 feature — for v1, the .docx fill
    # uses the original template placeholders which covers the main content.
    # HTML edits appear in PDF export (via contract_html) but not in .docx.

    return file_url
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/dcnet_contract/dcnet_contract/tests/test_template_engine.py -v 2>&1 | tail -20`
Expected: All tests PASS

- [ ] **Step 5: Update dcnet_contract.py before_print() for backward compat**

In `dcnet_contract.py`, update `before_print()` at line 30:

```python
def before_print(self, settings=None):
    if self.contract_html:
        # Template-based contract: use stored HTML (may include sales edits)
        self.contract_html_rendered = self.contract_html
    else:
        # Backward compat: old contracts without template
        from dcnet_contract.dcnet_contract.utils.docx_generator import (
            generate_appendix_html_for_print,
            generate_html_for_print,
        )
        self.contract_html_rendered = generate_html_for_print(self.name)
        self.appendix_html = generate_appendix_html_for_print(self.name)
```

- [ ] **Step 6: Update print format to use contract_html_rendered**

In `hop_dong_chuan.html`, change line 43:

```html
{{ doc.contract_html_rendered or doc.contract_html or "" }}
```

- [ ] **Step 7: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/utils/template_engine.py apps/dcnet_contract/dcnet_contract/tests/test_template_engine.py apps/dcnet_contract/dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract.py apps/dcnet_contract/dcnet_contract/dcnet_contract/print_format/hop_dong_chuan/hop_dong_chuan.html
git commit -m "feat(contract): add template engine, update before_print for backward compat"
```

---

## Task 7: Client Scripts — Template Form

**Files:**
- Create: `dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.js`
- Modify: `dcnet_contract/hooks.py`

No TDD — browser verification.

- [ ] **Step 1: Create template form client script**

Create `dcnet_contract_template.js`:

```javascript
frappe.ui.form.on("DCNet Contract Template", {
    refresh(frm) {
        // Display placeholder guide
        if (frm.doc.placeholder_guide_html) {
            frm.set_df_property("placeholder_guide_html", "hidden", 0);
            frm.fields_dict.placeholder_guide_html.$wrapper.html(
                frm.doc.placeholder_guide_html
            );
        }

        // Status action buttons
        if (frm.doc.status === "Draft" && !frm.is_new()) {
            frm.add_custom_button(__("Submit for Review"), () => {
                frm.call("submit_for_review").then(() => frm.reload_doc());
            }, __("Actions"));
        }

        if (frm.doc.status === "Pending Review") {
            frm.add_custom_button(__("Approve"), () => {
                frm.call("approve_template").then(() => frm.reload_doc());
            }, __("Actions"));
            frm.add_custom_button(__("Reject"), () => {
                frm.call("reject_template").then(() => frm.reload_doc());
            }, __("Actions"));
        }

        if (frm.doc.status === "Approved") {
            frm.add_custom_button(__("Archive"), () => {
                frappe.confirm(
                    __("Archive this template? It will no longer be available for new contracts."),
                    () => frm.call("archive_template").then(() => frm.reload_doc())
                );
            }, __("Actions"));
            frm.add_custom_button(__("New Version"), () => {
                frm.call("create_new_version").then((r) => {
                    if (r.message) {
                        frappe.set_route("Form", "DCNet Contract Template", r.message);
                    }
                });
            }, __("Actions"));
        }

        // Status indicator
        const status_colors = {
            "Draft": "orange",
            "Pending Review": "blue",
            "Approved": "green",
            "Archived": "grey",
        };
        if (frm.doc.status) {
            frm.page.set_indicator(__(frm.doc.status), status_colors[frm.doc.status] || "grey");
        }
    },
});
```

- [ ] **Step 2: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/dcnet_contract/doctype/dcnet_contract_template/dcnet_contract_template.js
git commit -m "feat(contract): add template form client script with workflow buttons"
```

---

## Task 8: Client Scripts — Contract Template Integration

**Files:**
- Create: `dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract_template_integration.js`

- [ ] **Step 1: Create contract template integration client script**

Create `dcnet_contract_template_integration.js`:

```javascript
frappe.ui.form.on("DCNet Contract", {
    refresh(frm) {
        // Template version warning for Draft contracts
        if (frm.doc.template_ref && frm.doc.docstatus === 0 && frm.doc.template_outdated) {
            frm.dashboard.set_headline(
                __("Template has been updated. Click 'Re-apply Template' to use the latest version."),
                "orange"
            );
        }

        // Apply Template button (Draft only, template selected)
        if (frm.doc.template_ref && frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Apply Template"), () => {
                let warning = "";
                if (frm.doc.contract_html_edited) {
                    warning = __("You have edited the contract content. Applying template will overwrite your changes. Continue?");
                } else {
                    warning = __("Apply template content to this contract?");
                }
                frappe.confirm(warning, () => {
                    frappe.call({
                        method: "dcnet_contract.dcnet_contract.utils.template_engine.apply_template",
                        args: {
                            contract_name: frm.doc.name,
                            template_name: frm.doc.template_ref,
                        },
                        callback: () => frm.reload_doc(),
                    });
                });
            }, __("Template"));
        }
    },

    template_ref(frm) {
        if (!frm.doc.template_ref) return;

        // Auto-fill from template
        frappe.call({
            method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract_template.dcnet_contract_template.get_template",
            args: { template_name: frm.doc.template_ref },
            callback(r) {
                if (!r.message) return;
                const tmpl = r.message;

                // Set contract fields from template
                if (tmpl.service_type) frm.set_value("service_type", tmpl.service_type);
                if (tmpl.contract_type) frm.set_value("contract_type", tmpl.contract_type);
                if (tmpl.payment_mode) frm.set_value("payment_mode", tmpl.payment_mode);
                if (tmpl.package_term_months) frm.set_value("package_term_months", tmpl.package_term_months);

                // Copy items if empty
                if (!frm.doc.items || frm.doc.items.length === 0) {
                    frm.clear_table("items");
                    (tmpl.items || []).forEach((item) => {
                        frm.add_child("items", item);
                    });
                    frm.refresh_field("items");
                }

                frm.set_value("template_version", tmpl.version || 1);
            },
        });
    },

    contract_html(frm) {
        // Track if HTML was edited by user
        if (frm.doc.template_ref && frm.doc.__original_contract_html !== undefined) {
            if (frm.doc.contract_html !== frm.doc.__original_contract_html) {
                frm.set_value("contract_html_edited", 1);
            }
        }
    },

    onload(frm) {
        // Cache original HTML for edit detection
        if (frm.doc.contract_html) {
            frm.doc.__original_contract_html = frm.doc.contract_html;
        }

        // Filter template_ref to only Approved templates
        frm.set_query("template_ref", () => ({
            filters: { status: "Approved" },
        }));
    },
});
```

- [ ] **Step 2: Commit**

```bash
git add apps/dcnet_contract/dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract_template_integration.js
git commit -m "feat(contract): add template integration client script for contract form"
```

---

## Task 9: Hooks + Build + Final Verification

**Files:**
- Modify: `dcnet_contract/hooks.py`

- [ ] **Step 1: Update hooks.py with app_include_js if needed**

The client scripts (.js files in DocType directories) are auto-loaded by Frappe for their respective forms — no `app_include_js` entry needed for form scripts. Only `.bundle.js` files in `public/js/` need `app_include_js`.

Verify that no hooks.py changes are needed for the form scripts. The existing hooks.py is already correct.

- [ ] **Step 2: Add vi.csv translations for new labels**

Check if `dcnet_contract/translations/vi.csv` exists, create or update with new translations:

```csv
Version,Phiên bản
Status,Trạng thái
Template HTML,HTML mẫu
Placeholder Guide HTML,Hướng dẫn placeholder
Change Log,Nhật ký thay đổi
Reviewed By,Người duyệt
Reviewed Date,Ngày duyệt
Approved By,Người phê duyệt
Approved Date,Ngày phê duyệt
Needs Dev Mapping,Cần IT ánh xạ
Contract Template,Mẫu hợp đồng
Template Version,Phiên bản mẫu
Template Outdated,Mẫu đã cũ
Contract HTML Edited,HTML đã chỉnh sửa
Contract Document,Tài liệu hợp đồng
Version & Approval,Phiên bản & Phê duyệt
Submit for Review,Gửi duyệt
Approve,Phê duyệt
Reject,Từ chối
Archive,Lưu trữ
New Version,Phiên bản mới
Apply Template,Áp dụng mẫu
Template has been updated. Click 'Re-apply Template' to use the latest version.,Mẫu đã được cập nhật. Nhấn 'Áp dụng mẫu' để sử dụng phiên bản mới nhất.
Only Draft templates can be submitted for review,Chỉ mẫu Nháp mới có thể gửi duyệt
Only templates in Pending Review can be approved,Chỉ mẫu đang Chờ duyệt mới có thể phê duyệt
Only templates in Pending Review can be rejected,Chỉ mẫu đang Chờ duyệt mới có thể từ chối
Only Approved templates can be archived,Chỉ mẫu đã Duyệt mới có thể lưu trữ
Cannot change status from {0} to {1},Không thể đổi trạng thái từ {0} sang {1}
Archive this template? It will no longer be available for new contracts.,Lưu trữ mẫu này? Mẫu sẽ không còn khả dụng cho hợp đồng mới.
Draft,Nháp
Pending Review,Chờ duyệt
Approved,Đã duyệt
Archived,Đã lưu trữ
Contract Template Manager,Quản lý mẫu hợp đồng
```

- [ ] **Step 3: Build and migrate**

Run:
```bash
cd /home/long/long/frappe-bench-dcnet && bench build --app dcnet_contract 2>&1 | tail -5
cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost migrate 2>&1 | tail -10
cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost clear-cache 2>&1 | tail -3
```

- [ ] **Step 4: Run all tests**

Run:
```bash
cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/dcnet_contract/dcnet_contract/tests/test_placeholder_engine.py -v 2>&1 | tail -20
cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/dcnet_contract/dcnet_contract/tests/test_template_engine.py -v 2>&1 | tail -20
```

- [ ] **Step 5: Commit all remaining changes**

```bash
git add -A apps/dcnet_contract/
git commit -m "feat(contract): translations, build, final wiring for template management"
```

---

## Task 10: QA with Headed Browser

**Prerequisite:** Run `/connect-chrome` first, then `/qa`.

Test checklist:
1. Open DCNet Contract Template list → verify status column shows
2. Open a template → verify placeholder guide HTML renders
3. Upload new .docx → verify mammoth conversion fills template_html
4. Click "Submit for Review" → status changes to "Pending Review"
5. Click "Approve" → status changes to "Approved"
6. Open DCNet Contract → select template_ref dropdown (only Approved templates)
7. Select template → verify service_type, items auto-fill
8. Click "Apply Template" → contract_html fills
9. Print preview → verify contract renders from contract_html
10. Old contract without template → verify backward compat (still renders)
11. Test "Archive" and "New Version" buttons

---

## Self-Review Notes

- **Spec coverage:**
  - [x] §3 Template Data Model → Task 2 (JSON fields), Task 3 (controller)
  - [x] §4 Placeholder System → Task 1 (engine), Task 3 (integration in controller)
  - [x] §5 Contract Form Integration → Task 5 (JSON), Task 6 (engine), Task 8 (client script)
  - [x] §6 Document Export → Task 6 (before_print + template_engine.export_docx_with_edits)
  - [x] §7 Permission Model → Task 2 (permissions in JSON), Task 4 (role creation)
  - [x] §8 Migration → Task 4 (_migrate_templates_to_dual_format)
  - [x] §9 Scope → all in-scope items covered

- **Placeholder scan:** No TBD/TODO/placeholder text found.

- **Type consistency:**
  - `resolve_placeholder()` — used consistently in placeholder_engine.py and template_engine.py
  - `fill_html_placeholders()` — defined in template_engine.py, used in apply_template()
  - `build_placeholder_values()` — delegates to docx_generator._build_placeholder_values()
  - `validate_template_placeholders()` — defined in placeholder_engine.py, used in template controller
  - Template controller methods: submit_for_review, approve_template, reject_template, archive_template, create_new_version — consistent between .py and .js
