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
