"""Unit tests for markup_calc.calculate_price.

5 of 6 methods are fully pure (no DB) and tested directly. Contract methods
patch _resolve_contract_value to avoid DB dependency.
"""
from __future__ import annotations

import unittest
from unittest.mock import patch

from vn_accounting.project_costing.services.markup_calc import calculate_price


class TestMarkupCalcCoefficient(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(calculate_price(method="Coefficient", markup_value=1.5, cost_pinned=100), 150.0)

    def test_zero_markup(self):
        self.assertEqual(calculate_price(method="Coefficient", markup_value=0, cost_pinned=100), 0.0)

    def test_zero_cost(self):
        self.assertEqual(calculate_price(method="Coefficient", markup_value=1.5, cost_pinned=0), 0.0)

    def test_below_cost_coefficient(self):
        # Allow markup < 1 (sell at loss). No raise per BL R5.3 (warn but allow).
        self.assertEqual(calculate_price(method="Coefficient", markup_value=0.8, cost_pinned=100_000_000), 80_000_000.0)


class TestMarkupCalcPercentOnCost(unittest.TestCase):
    def test_plus_30_percent(self):
        self.assertEqual(calculate_price(method="Percent on Cost", markup_value=30, cost_pinned=100), 130.0)

    def test_zero_percent(self):
        self.assertEqual(calculate_price(method="Percent on Cost", markup_value=0, cost_pinned=100), 100.0)

    def test_negative_percent(self):
        self.assertEqual(calculate_price(method="Percent on Cost", markup_value=-10, cost_pinned=100), 90.0)


class TestMarkupCalcFixedAmount(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(calculate_price(method="Fixed Amount", markup_value=150_000_000), 150_000_000.0)

    def test_cost_ignored(self):
        # Fixed amount doesn't depend on cost
        self.assertEqual(calculate_price(method="Fixed Amount", markup_value=200, cost_pinned=99999), 200.0)

    def test_zero_value(self):
        self.assertEqual(calculate_price(method="Fixed Amount", markup_value=0), 0.0)


class TestMarkupCalcFromContract(unittest.TestCase):
    def test_basic(self):
        # From Contract uses markup_value directly (KTT đọc từ phụ lục)
        self.assertEqual(calculate_price(method="From Contract", markup_value=85_000_000), 85_000_000.0)


class TestMarkupCalcPercentOfContract(unittest.TestCase):
    @patch("vn_accounting.project_costing.services.markup_calc._resolve_contract_value")
    def test_basic(self, mock_resolve):
        mock_resolve.return_value = 300_000_000
        # 30% of 300tr contract = 90tr (tạm ứng đầu)
        self.assertEqual(
            calculate_price(method="Percent of Contract", markup_value=30, parent_costing="PROJ-X"),
            90_000_000.0,
        )

    @patch("vn_accounting.project_costing.services.markup_calc._resolve_contract_value")
    def test_no_contract(self, mock_resolve):
        mock_resolve.return_value = 0
        self.assertEqual(
            calculate_price(method="Percent of Contract", markup_value=30, parent_costing="PROJ-X"),
            0.0,
        )

    def test_no_parent_costing(self):
        # No parent_costing → no contract lookup → 0
        self.assertEqual(
            calculate_price(method="Percent of Contract", markup_value=30, parent_costing=None),
            0.0,
        )


class TestMarkupCalcCostToDateUplift(unittest.TestCase):
    def test_basic(self):
        # Nghiệm thu giữa: 25% uplift trên cost đã phát sinh
        self.assertEqual(
            calculate_price(method="Cost-to-Date Uplift", markup_value=25, cost_pinned=40_000_000),
            50_000_000.0,
        )

    def test_zero_uplift(self):
        # Cost-only (no profit margin)
        self.assertEqual(
            calculate_price(method="Cost-to-Date Uplift", markup_value=0, cost_pinned=40_000_000),
            40_000_000.0,
        )


class TestMarkupCalcEdgeCases(unittest.TestCase):
    def test_unknown_method(self):
        # Bad method → 0 (no raise per pure-function contract)
        self.assertEqual(calculate_price(method="BadMethod", markup_value=1.5, cost_pinned=100), 0.0)

    def test_empty_method(self):
        self.assertEqual(calculate_price(method="", markup_value=1.5, cost_pinned=100), 0.0)

    def test_none_markup_value(self):
        self.assertEqual(calculate_price(method="Coefficient", markup_value=None, cost_pinned=100), 0.0)

    def test_none_cost(self):
        self.assertEqual(calculate_price(method="Coefficient", markup_value=1.5, cost_pinned=None), 0.0)


if __name__ == "__main__":
    unittest.main()
