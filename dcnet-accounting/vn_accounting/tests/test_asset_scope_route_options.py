"""Tests for the TSCĐ / CCDC sidebar split (F-CCDC-003 + F-CCDC-004).

Asserts that the 4 sidebar items (Bàn giao TSCĐ, Kiểm kê TSCĐ, Bàn giao CCDC,
Kiểm kê CCDC) filter by the existing `scope` field on Asset Handover / Asset
Stocktake — the canonical source-of-truth field already used by controllers
and JS handlers. An earlier draft introduced a parallel `asset_category` field;
that was rolled back to avoid two-field drift (see sprint-abcd-report.md).

JSON fixture only — no Frappe DB required.
"""
import json
import os
import unittest


def _fixture_path(rel: str) -> str:
	here = os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(here, "..", rel))


def _load_sidebar() -> dict:
	with open(_fixture_path("workspace_sidebar/vn_accounting.json"), encoding="utf-8") as f:
		return json.load(f)


class TestSidebarScopeRouteOptions(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.items = _load_sidebar()["items"]

	def _find(self, label: str) -> dict:
		try:
			return next(it for it in self.items if it.get("label") == label)
		except StopIteration:
			self.fail(f"sidebar item not found: {label}")

	def _assert_route_options(self, label: str, expected_scope: str):
		it = self._find(label)
		ro = it.get("route_options") or ""
		self.assertTrue(ro, f"{label}: route_options is empty")
		parsed = json.loads(ro)
		self.assertEqual(
			parsed.get("scope"), expected_scope,
			f"{label}: expected scope={expected_scope!r}, got {parsed.get('scope')!r}",
		)
		self.assertIn("docstatus", parsed, f"{label}: missing docstatus filter")
		self.assertNotIn(
			"asset_category", parsed,
			f"{label}: stale asset_category key — should be scope only",
		)

	def test_ban_giao_tscd_filters_scope_tscd(self):
		self._assert_route_options("Bàn giao TSCĐ", "TSCĐ")

	def test_kiem_ke_tscd_filters_scope_tscd(self):
		self._assert_route_options("Kiểm kê TSCĐ", "TSCĐ")

	def test_ban_giao_ccdc_filters_scope_ccdc(self):
		self._assert_route_options("Bàn giao CCDC", "CCDC")

	def test_kiem_ke_ccdc_filters_scope_ccdc(self):
		self._assert_route_options("Kiểm kê CCDC", "CCDC")


if __name__ == "__main__":
	unittest.main()
