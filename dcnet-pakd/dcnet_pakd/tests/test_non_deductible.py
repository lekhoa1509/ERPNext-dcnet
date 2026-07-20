"""Unit tests for the non-deductible auto-set heuristic.

The function under test is pure (no Frappe dependency) — drives off duck-typed
beneficiary line attributes. Run via:
    cd <bench-root>/sites
    ../env/bin/python -m unittest dcnet_pakd.dcnet_pakd.tests.test_non_deductible -v
"""
from __future__ import annotations

import unittest
from types import SimpleNamespace


class TestIsNonDeductibleBeneficiary(unittest.TestCase):
	def setUp(self):
		# Lazy import — the module patches Frappe at top, so we import per-test
		from dcnet_pakd.dcnet_pakd.integrations.accounting import (
			_is_non_deductible_beneficiary,
		)
		self._fn = _is_non_deductible_beneficiary

	def _line(self, **kwargs):
		defaults = {
			"invoice_no": None,
			"recipient_name": None,
			"recipient_tax_pct": 0,
			"kind": "Manager Services",
		}
		defaults.update(kwargs)
		return SimpleNamespace(**defaults)

	def test_has_invoice_is_deductible(self):
		"""Any line with invoice_no → deductible (chỉ exception)."""
		line = self._line(invoice_no="HD2026-001", recipient_name="Nguyễn Văn A")
		flag, reason = self._fn(line)
		self.assertFalse(flag)
		self.assertEqual(reason, "")

	def test_recipient_with_tncn_no_invoice_is_non_deductible(self):
		"""Per TT78/2014: PIT withholding ≠ CIT deductibility.

		Khoản chi cho cá nhân không có HĐ hợp pháp, dù có khấu trừ TNCN,
		KHÔNG được trừ TNDN. PIT chỉ giải quyết phía thu nhập cá nhân,
		không tự động hợp thức hóa chi phí bên doanh nghiệp.
		"""
		line = self._line(recipient_name="Nguyễn Văn A", recipient_tax_pct=10)
		flag, reason = self._fn(line)
		self.assertTrue(flag)
		self.assertEqual(reason, "Không HĐ hợp lệ")

	def test_recipient_no_tncn_no_invoice_is_non_deductible(self):
		"""Named individual + no TNCN + no invoice → flag."""
		line = self._line(recipient_name="Nguyễn Văn A", recipient_tax_pct=0)
		flag, reason = self._fn(line)
		self.assertTrue(flag)
		self.assertEqual(reason, "Không HĐ hợp lệ")

	def test_no_recipient_no_invoice_is_non_deductible(self):
		"""Internal allocation (no recipient) cũng non-deductible — không có proof gì cả."""
		line = self._line(recipient_name=None, recipient_tax_pct=0)
		flag, reason = self._fn(line)
		self.assertTrue(flag)
		self.assertEqual(reason, "Không HĐ hợp lệ")

	def test_empty_invoice_string_treated_as_none(self):
		"""Whitespace invoice_no should NOT bypass the flag."""
		line = self._line(invoice_no="   ", recipient_name="Nguyễn Văn A")
		flag, _reason = self._fn(line)
		self.assertTrue(flag)

	def test_override_true_forces_flag(self):
		"""override=True từ popup → force flag bất kể heuristic."""
		line = self._line(invoice_no="HD2026-001", recipient_name="Nguyễn Văn A")
		flag, reason = self._fn(line, override=True)
		self.assertTrue(flag)
		self.assertEqual(reason, "Không HĐ hợp lệ")

	def test_override_false_unflags_even_without_invoice(self):
		"""override=False → user xác nhận có HĐ → unflag dù heuristic default flag."""
		line = self._line(recipient_name="Nguyễn Văn A", recipient_tax_pct=0)
		flag, reason = self._fn(line, override=False)
		self.assertFalse(flag)
		self.assertEqual(reason, "")

	def test_override_none_uses_default_heuristic(self):
		"""override=None → fall back vào heuristic mặc định."""
		line = self._line(invoice_no="HD2026-001")
		flag_with_inv, _ = self._fn(line, override=None)
		self.assertFalse(flag_with_inv)
		line2 = self._line()
		flag_no_inv, _ = self._fn(line2, override=None)
		self.assertTrue(flag_no_inv)


class TestHelperRoundTrip(unittest.TestCase):
	def test_mark_and_read_back(self):
		from vn_accounting.non_deductible.helper import (
			mark_non_deductible,
			is_marked,
			get_reason,
			REASON_PENALTY,
		)
		row = SimpleNamespace(is_non_deductible=0, non_deductible_reason="")
		mark_non_deductible(row, REASON_PENALTY)
		self.assertTrue(is_marked(row))
		self.assertEqual(get_reason(row), REASON_PENALTY)

	def test_invalid_reason_raises(self):
		from vn_accounting.non_deductible.helper import mark_non_deductible
		row = SimpleNamespace(is_non_deductible=0, non_deductible_reason="")
		with self.assertRaises(ValueError):
			mark_non_deductible(row, "Bịa lý do nào đó")

	def test_unflagged_row_helpers(self):
		from vn_accounting.non_deductible.helper import is_marked, get_reason
		row = SimpleNamespace()  # no attrs at all
		self.assertFalse(is_marked(row))
		self.assertEqual(get_reason(row), "")


if __name__ == "__main__":
	unittest.main()
