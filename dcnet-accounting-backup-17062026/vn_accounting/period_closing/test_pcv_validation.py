"""Unit tests for Period Closing Voucher VN validation hooks."""
import unittest
from unittest.mock import MagicMock, patch


class TestPcvValidateVnRequirements(unittest.TestCase):
    """Tests for pcv_validate_vn_requirements hook."""

    def _make_doc(self, reason=""):
        doc = MagicMock()
        doc.get = lambda field, default=None: reason if field == "vn_lock_unlock_reason" else default
        return doc

    @patch("vn_accounting.period_closing.pcv_hooks._", lambda x, **kw: x)
    @patch("vn_accounting.period_closing.pcv_hooks.frappe")
    def test_empty_reason_raises(self, mock_frappe):
        from vn_accounting.period_closing.pcv_hooks import pcv_validate_vn_requirements

        mock_frappe.throw.side_effect = Exception("thrown")
        mock_frappe.has_role.return_value = True

        doc = self._make_doc(reason="")
        with self.assertRaises(Exception):
            pcv_validate_vn_requirements(doc, "validate")

        mock_frappe.throw.assert_called_once()
        call_msg = str(mock_frappe.throw.call_args[0][0])
        self.assertIn("Lý do", call_msg)

    @patch("vn_accounting.period_closing.pcv_hooks._", lambda x, **kw: x)
    @patch("vn_accounting.period_closing.pcv_hooks.frappe")
    def test_non_manager_role_raises(self, mock_frappe):
        from vn_accounting.period_closing.pcv_hooks import pcv_validate_vn_requirements

        mock_frappe.throw.side_effect = Exception("thrown")
        mock_frappe.has_role.return_value = False  # not Accounts Manager, not System Manager

        doc = self._make_doc(reason="Khóa sổ tháng 4/2026")
        with self.assertRaises(Exception):
            pcv_validate_vn_requirements(doc, "validate")

        mock_frappe.throw.assert_called_once()
        call_msg = str(mock_frappe.throw.call_args[0][0])
        self.assertIn("Accounts Manager", call_msg)

    @patch("vn_accounting.period_closing.pcv_hooks.frappe")
    def test_valid_state_no_exception(self, mock_frappe):
        from vn_accounting.period_closing.pcv_hooks import pcv_validate_vn_requirements

        mock_frappe.throw.side_effect = Exception("should not be called")
        mock_frappe.has_role.return_value = True

        doc = self._make_doc(reason="Khóa sổ tháng 4/2026 sau đối chiếu xong")
        # Should complete without raising
        pcv_validate_vn_requirements(doc, "validate")
        mock_frappe.throw.assert_not_called()

    @patch("vn_accounting.period_closing.pcv_hooks.frappe")
    def test_system_manager_allowed(self, mock_frappe):
        from vn_accounting.period_closing.pcv_hooks import pcv_validate_vn_requirements

        mock_frappe.throw.side_effect = Exception("should not be called")

        def has_role_side_effect(role):
            return role == "System Manager"  # only System Manager, not Accounts Manager

        mock_frappe.has_role.side_effect = has_role_side_effect

        doc = self._make_doc(reason="Mở khóa do kiểm toán yêu cầu")
        pcv_validate_vn_requirements(doc, "validate")
        mock_frappe.throw.assert_not_called()


class TestPcvAuditLog(unittest.TestCase):
    """Tests for pcv_on_submit and pcv_on_cancel audit log writing."""

    def _make_doc(self, reason="Test reason"):
        doc = MagicMock()
        doc.doctype = "Period Closing Voucher"
        doc.name = "PCV-2026-001"
        doc.get = lambda field, default=None: reason if field == "vn_lock_unlock_reason" else default
        return doc

    @patch("vn_accounting.period_closing.pcv_hooks.frappe")
    def test_on_submit_creates_comment(self, mock_frappe):
        from vn_accounting.period_closing.pcv_hooks import pcv_on_submit

        comment_doc = MagicMock()
        mock_frappe.get_doc.return_value = comment_doc
        mock_frappe.session.user = "admin@example.com"

        doc = self._make_doc(reason="Khóa sổ tháng 4")
        pcv_on_submit(doc, "on_submit")

        mock_frappe.get_doc.assert_called_once()
        call_kwargs = mock_frappe.get_doc.call_args[0][0]
        self.assertEqual(call_kwargs["doctype"], "Comment")
        self.assertEqual(call_kwargs["reference_doctype"], "Period Closing Voucher")
        self.assertIn("Khóa sổ", call_kwargs["content"])
        comment_doc.insert.assert_called_once()

    @patch("vn_accounting.period_closing.pcv_hooks.frappe")
    def test_on_cancel_creates_comment(self, mock_frappe):
        from vn_accounting.period_closing.pcv_hooks import pcv_on_cancel

        comment_doc = MagicMock()
        mock_frappe.get_doc.return_value = comment_doc
        mock_frappe.session.user = "ktt@example.com"

        doc = self._make_doc(reason="Mở khóa do kiểm toán")
        pcv_on_cancel(doc, "on_cancel")

        call_kwargs = mock_frappe.get_doc.call_args[0][0]
        self.assertIn("Mở khóa", call_kwargs["content"])
        comment_doc.insert.assert_called_once()

    @patch("vn_accounting.period_closing.pcv_hooks.frappe")
    def test_submit_includes_user_in_log(self, mock_frappe):
        from vn_accounting.period_closing.pcv_hooks import pcv_on_submit

        comment_doc = MagicMock()
        mock_frappe.get_doc.return_value = comment_doc
        mock_frappe.session.user = "ktt@dcnet.vn"

        doc = self._make_doc()
        pcv_on_submit(doc, "on_submit")

        content = mock_frappe.get_doc.call_args[0][0]["content"]
        self.assertIn("ktt@dcnet.vn", content)


if __name__ == "__main__":
    unittest.main()
