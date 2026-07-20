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
