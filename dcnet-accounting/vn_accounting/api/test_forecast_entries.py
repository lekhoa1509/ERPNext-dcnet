import unittest
from unittest.mock import patch
from vn_accounting.api.forecast import (
    _filter_entries, _compute_group_totals, CONFIDENCE_ORDER,
    get_forecast_entries,
)


class TestFilterEntries(unittest.TestCase):
    def _entry(self, **overrides):
        base = {
            "expected_date": "2026-05-15",
            "amount": 1000.0,
            "direction": "inflow",
            "category": "Sales Order",
            "confidence": "committed",
            "source_doctype": "Sales Order",
            "source_name": "SO-001",
            "description": "SO-001 customer ABC",
            "party": "Customer ABC",
        }
        base.update(overrides)
        return base

    def test_no_filter_returns_all(self):
        entries = [self._entry(), self._entry(amount=2000)]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="")
        self.assertEqual(len(out), 2)

    def test_period_key_monthly_match(self):
        entries = [
            self._entry(expected_date="2026-05-15"),
            self._entry(expected_date="2026-06-01"),
        ]
        out = _filter_entries(entries, period_key="2026-05", granularity="monthly",
                              confidences=None, sources=None, search="")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["expected_date"], "2026-05-15")

    def test_period_key_weekly_match(self):
        # 2026-05-04 is a Monday (ISO week 19 of 2026)
        entries = [
            self._entry(expected_date="2026-05-04"),  # ISO 2026-W19
            self._entry(expected_date="2026-05-11"),  # ISO 2026-W20
        ]
        out = _filter_entries(entries, period_key="2026-W19", granularity="weekly",
                              confidences=None, sources=None, search="")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["expected_date"], "2026-05-04")

    def test_confidence_filter(self):
        entries = [
            self._entry(confidence="committed"),
            self._entry(confidence="probable"),
            self._entry(confidence="possible"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=["committed", "probable"],
                              sources=None, search="")
        self.assertEqual(len(out), 2)
        self.assertEqual({e["confidence"] for e in out}, {"committed", "probable"})

    def test_source_filter(self):
        entries = [
            self._entry(source_doctype="Sales Order"),
            self._entry(source_doctype="Purchase Order"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=["Sales Order"], search="")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["source_doctype"], "Sales Order")

    def test_search_matches_description(self):
        # Override party to neutral values so search "abc" only matches description.
        entries = [
            self._entry(description="ABC Co. invoice", party="Neutral One"),
            self._entry(description="XYZ Ltd. payment", party="Neutral Two"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="abc")
        self.assertEqual(len(out), 1)

    def test_search_matches_party(self):
        entries = [
            self._entry(party="Customer ABC", description="x"),
            self._entry(party="Supplier XYZ", description="y"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="xyz")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["party"], "Supplier XYZ")

    def test_search_matches_source_name(self):
        entries = [
            self._entry(source_name="SO-001"),
            self._entry(source_name="PI-2026-099"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="2026-099")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["source_name"], "PI-2026-099")

    def test_combined_filters(self):
        entries = [
            self._entry(confidence="committed", source_doctype="Sales Order"),
            self._entry(confidence="committed", source_doctype="Purchase Order"),
            self._entry(confidence="probable",  source_doctype="Sales Order"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=["committed"],
                              sources=["Sales Order"], search="")
        self.assertEqual(len(out), 1)


class TestComputeGroupTotals(unittest.TestCase):
    def _entry(self, **overrides):
        base = {
            "expected_date": "2026-05-15", "amount": 1000.0, "direction": "inflow",
            "confidence": "committed", "source_doctype": "Sales Order",
            "source_name": "x", "category": "x",
        }
        base.update(overrides)
        return base

    def test_empty_entries_returns_zeroed_buckets(self):
        out = _compute_group_totals([])
        self.assertEqual(set(out.keys()),
                         {"overdue", "committed", "probable", "possible"})
        for v in out.values():
            self.assertEqual(v, {"inflow": 0.0, "outflow": 0.0, "count": 0})

    def test_inflow_summed_per_confidence(self):
        entries = [
            self._entry(confidence="committed", direction="inflow", amount=100),
            self._entry(confidence="committed", direction="inflow", amount=200),
            self._entry(confidence="probable",  direction="inflow", amount=50),
        ]
        out = _compute_group_totals(entries)
        self.assertEqual(out["committed"]["inflow"], 300)
        self.assertEqual(out["committed"]["count"], 2)
        self.assertEqual(out["probable"]["inflow"], 50)

    def test_outflow_separated_from_inflow(self):
        entries = [
            self._entry(confidence="committed", direction="inflow",  amount=100),
            self._entry(confidence="committed", direction="outflow", amount=80),
        ]
        out = _compute_group_totals(entries)
        self.assertEqual(out["committed"]["inflow"], 100)
        self.assertEqual(out["committed"]["outflow"], 80)
        self.assertEqual(out["committed"]["count"], 2)


class TestConfidenceOrder(unittest.TestCase):
    def test_order_priorities(self):
        self.assertEqual(CONFIDENCE_ORDER["overdue"], 0)
        self.assertEqual(CONFIDENCE_ORDER["committed"], 1)
        self.assertEqual(CONFIDENCE_ORDER["probable"], 2)
        self.assertEqual(CONFIDENCE_ORDER["possible"], 3)


class TestGetForecastEntries(unittest.TestCase):
    """End-to-end wrapper: mocks _load_entries_with_cache to avoid Redis."""

    def _entry(self, **overrides):
        base = {
            "expected_date": "2026-05-15", "amount": 1000.0, "direction": "inflow",
            "confidence": "committed", "source_doctype": "Sales Order",
            "source_name": "SO-001", "description": "x", "party": "Customer",
            "category": "Sales Order", "party_type": "Customer",
        }
        base.update(overrides)
        return base

    def _patch_loader(self, entries):
        return patch("vn_accounting.api.forecast._load_entries_with_cache",
                     return_value=entries)

    def test_pagination_first_page(self):
        entries = [self._entry(amount=i, expected_date=f"2026-05-{i:02d}")
                   for i in range(1, 26)]  # 25 entries
        with self._patch_loader(entries):
            r = get_forecast_entries("ACME", "2026-05-01", "2026-05-31",
                                     page=1, page_size=10)
        self.assertEqual(r["total"], 25)
        self.assertEqual(len(r["entries"]), 10)
        self.assertEqual(r["page"], 1)
        self.assertEqual(r["page_size"], 10)

    def test_pagination_second_page(self):
        entries = [self._entry(amount=i, expected_date=f"2026-05-{i:02d}")
                   for i in range(1, 26)]
        with self._patch_loader(entries):
            r = get_forecast_entries("ACME", "2026-05-01", "2026-05-31",
                                     page=2, page_size=10)
        self.assertEqual(len(r["entries"]), 10)
        self.assertEqual(r["entries"][0]["expected_date"], "2026-05-11")

    def test_pagination_last_partial_page(self):
        entries = [self._entry(amount=i, expected_date=f"2026-05-{i:02d}")
                   for i in range(1, 26)]
        with self._patch_loader(entries):
            r = get_forecast_entries("ACME", "2026-05-01", "2026-05-31",
                                     page=3, page_size=10)
        self.assertEqual(len(r["entries"]), 5)

    def test_group_totals_uses_full_filtered_set_not_page(self):
        # 25 entries committed, page_size 5 → group_totals should still see all 25.
        entries = [self._entry(amount=100, direction="inflow",
                               expected_date=f"2026-05-{i:02d}")
                   for i in range(1, 26)]
        with self._patch_loader(entries):
            r = get_forecast_entries("ACME", "2026-05-01", "2026-05-31",
                                     page=1, page_size=5)
        self.assertEqual(r["group_totals"]["committed"]["count"], 25)
        self.assertEqual(r["group_totals"]["committed"]["inflow"], 25 * 100)

    def test_sort_by_confidence_then_date(self):
        entries = [
            self._entry(confidence="possible",  expected_date="2026-05-10"),
            self._entry(confidence="overdue",   expected_date="2026-05-20"),
            self._entry(confidence="committed", expected_date="2026-05-05"),
            self._entry(confidence="probable",  expected_date="2026-05-15"),
        ]
        with self._patch_loader(entries):
            r = get_forecast_entries("ACME", "2026-05-01", "2026-05-31",
                                     page=1, page_size=10)
        order = [e["confidence"] for e in r["entries"]]
        self.assertEqual(order, ["overdue", "committed", "probable", "possible"])

    def test_string_confidences_parsed_as_json(self):
        # frappe.xcall sends list params as JSON-stringified.
        entries = [
            self._entry(confidence="committed"),
            self._entry(confidence="probable"),
            self._entry(confidence="possible"),
        ]
        with self._patch_loader(entries):
            r = get_forecast_entries("ACME", "2026-05-01", "2026-05-31",
                                     confidences='["committed","probable"]',
                                     page=1, page_size=10)
        self.assertEqual(r["total"], 2)
        confs = {e["confidence"] for e in r["entries"]}
        self.assertEqual(confs, {"committed", "probable"})

    def test_filters_apply_before_sort_and_pagination(self):
        entries = [
            self._entry(source_doctype="Sales Order"),
            self._entry(source_doctype="Purchase Order"),
            self._entry(source_doctype="Sales Order"),
        ]
        with self._patch_loader(entries):
            r = get_forecast_entries("ACME", "2026-05-01", "2026-05-31",
                                     sources=["Sales Order"],
                                     page=1, page_size=10)
        self.assertEqual(r["total"], 2)
        self.assertTrue(all(e["source_doctype"] == "Sales Order"
                            for e in r["entries"]))
