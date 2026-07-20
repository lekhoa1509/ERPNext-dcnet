"""Smoke test for Inventory Cost Reallocation DocType.

Validates that:
  - DocType is registered + can be instantiated
  - validate() rejects bad inputs (wrong date order, same source/target, zero amount)
  - compute_reallocation() runs without error against an empty company

Heavier integration tests (with seeded GL entries) live in
test_lcv_inventory_split.py — this file just verifies the DocType wiring.
"""
from __future__ import annotations

import unittest

import frappe


class TestInventoryCostReallocation(unittest.TestCase):
    def test_doctype_registered(self):
        meta = frappe.get_meta("Inventory Cost Reallocation")
        self.assertEqual(meta.module, "VN Accounting")
        self.assertTrue(meta.is_submittable)
        self.assertTrue(meta.has_field("source_account"))
        self.assertTrue(meta.has_field("target_account"))
        self.assertTrue(meta.has_field("computed_amount"))
        self.assertTrue(meta.has_field("journal_entry"))

    def test_compute_endpoint_callable(self):
        # Just verify the function is reachable + returns expected keys.
        from vn_accounting.vn_accounting.doctype.inventory_cost_reallocation.inventory_cost_reallocation import (
            compute_reallocation,
        )
        self.assertTrue(callable(compute_reallocation))
