import frappe
from frappe.tests.utils import FrappeTestCase


class TestReconcileAPI(FrappeTestCase):
    def test_module_importable(self):
        from vn_banking.api import reconcile
        self.assertTrue(hasattr(reconcile, "trigger_import"))
        self.assertTrue(hasattr(reconcile, "get_import_transactions"))
        self.assertTrue(hasattr(reconcile, "create_payment_entry"))
        self.assertTrue(hasattr(reconcile, "bulk_create_pe"))
        self.assertTrue(hasattr(reconcile, "trigger_rematch"))
