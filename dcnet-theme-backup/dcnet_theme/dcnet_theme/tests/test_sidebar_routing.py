"""Integration tests for sidebar routing (merged from dcnet_sidebar_routing v0.3.0).

3 tests covering the entire surface:
  - get_allowed_modules: respects User.block_modules
  - get_allowed_modules: Administrator bypass
  - boot_session: emits expected sidebar bootinfo keys

Run via:
  bench --site <site> console
  >>> from dcnet_theme.dcnet_theme.tests.test_sidebar_routing import _run_all
  >>> _run_all()
"""

import unittest

import frappe

from dcnet_theme.dcnet_theme.boot import (
    boot_session,
    get_allowed_modules,
)


TEST_USER_PREFIX = "dcnet_theme_test_sidebar_"


def _create_test_user(suffix, roles, block_modules=None):
    email = f"{TEST_USER_PREFIX}{suffix}@example.com"
    if frappe.db.exists("User", email):
        frappe.delete_doc("User", email, force=True, ignore_permissions=True)

    user = frappe.new_doc("User")
    user.email = email
    user.first_name = f"Test {suffix}"
    user.send_welcome_email = 0
    user.enabled = 1
    user.user_type = "System User"
    for role in roles:
        user.append("roles", {"role": role})
    for mod in (block_modules or []):
        user.append("block_modules", {"module": mod})
    user.insert(ignore_permissions=True)
    frappe.db.commit()
    return email


def _all_modules():
    return [m.name for m in frappe.get_all("Module Def", fields=["name"])]


class TestSidebarRouting(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        for u in frappe.get_all("User", filters=[["email", "like", f"{TEST_USER_PREFIX}%"]]):
            frappe.delete_doc("User", u.name, force=True, ignore_permissions=True)
        frappe.db.commit()

    def setUp(self):
        frappe.set_user("Administrator")

    def test_allowed_modules_excludes_blocked(self):
        """User with block_modules → those modules not in allowed_modules."""
        user = _create_test_user(
            "blocked_modules",
            roles=["Accounts User", "Sales User"],
            block_modules=["Selling", "Stock"],
        )
        frappe.set_user(user)
        allowed = get_allowed_modules(user)
        self.assertNotIn("Selling", allowed)
        self.assertNotIn("Stock", allowed)
        self.assertIn("Accounts", allowed)

    def test_administrator_bypasses_block_modules(self):
        """Administrator returns all modules regardless."""
        allowed = get_allowed_modules("Administrator")
        all_mods = _all_modules()
        self.assertEqual(set(allowed), set(all_mods))

    def test_boot_session_emits_required_keys(self):
        """boot_session emits user_allowed_modules + workspace_sidebar_modules."""
        user = _create_test_user("boot_check", roles=["Accounts User"])
        frappe.set_user(user)
        bootinfo = {}
        boot_session(bootinfo)

        self.assertIn("user_allowed_modules", bootinfo)
        self.assertIsInstance(bootinfo["user_allowed_modules"], list)

        self.assertIn("workspace_sidebar_modules", bootinfo)
        self.assertIsInstance(bootinfo["workspace_sidebar_modules"], dict)

        # workspace_defaults should NOT be emitted (Layer A removed in v0.3.0)
        self.assertNotIn("workspace_defaults", bootinfo)


def _run_all():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSidebarRouting)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.failures or result.errors:
        raise SystemExit(1)
    return f"PASS: {result.testsRun} tests"
