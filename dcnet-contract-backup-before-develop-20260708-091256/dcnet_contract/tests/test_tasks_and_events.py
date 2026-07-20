"""Integration tests for auto-invoice, PE hook, overdue, and expire schedulers."""

from datetime import date, timedelta

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today

from dcnet_contract.dcnet_contract.tasks import (
    run_auto_invoice,
    run_expire_contracts,
    run_overdue_check,
)
from dcnet_contract.tests.helpers import (
    ensure_branch,
    ensure_cost_center_mapping,
    ensure_customer,
    ensure_employee,
    make_active_contract,
)


def _ensure_income_account(company):
    """Ensure the company has a default income account."""
    acc = frappe.db.get_value("Company", company, "default_income_account")
    if acc:
        return acc
    # Find any income-type leaf account
    acc = frappe.db.get_value(
        "Account",
        {"company": company, "root_type": "Income", "is_group": 0},
        "name",
    )
    if acc:
        frappe.db.set_value("Company", company, "default_income_account", acc)
    return acc


def _ensure_receivable_account(company):
    """Ensure the company has a default receivable account."""
    acc = frappe.db.get_value("Company", company, "default_receivable_account")
    if acc:
        return acc
    acc = frappe.db.get_value(
        "Account",
        {"company": company, "account_type": "Receivable", "is_group": 0},
        "name",
    )
    if acc:
        frappe.db.set_value("Company", company, "default_receivable_account", acc)
    return acc


def _get_company():
    return (
        frappe.db.get_single_value("Global Defaults", "default_company")
        or frappe.db.get_value("Company", {}, "name")
    )


class TestAutoInvoice(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = ensure_customer()
        cls.sales_person = ensure_employee()
        ensure_branch("HCM")
        ensure_cost_center_mapping("HCM")
        cls.company = _get_company()
        _ensure_income_account(cls.company)
        _ensure_receivable_account(cls.company)

    def test_auto_invoice_creates_si_for_due_rows(self):
        """Projected rows with due_date <= today get invoiced."""
        # Use dates far enough in the past so all 3 months' due_dates are <= today
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=3,
            payment_mode="Monthly",
        )
        self.assertEqual(len(contract.billing_schedule), 3)
        self.assertTrue(all(r.state == "Projected" for r in contract.billing_schedule))

        run_auto_invoice()

        contract.reload()
        invoiced = [r for r in contract.billing_schedule if r.state == "Invoiced"]
        self.assertEqual(len(invoiced), 3)
        # Each should have a SI link
        for r in invoiced:
            self.assertTrue(r.sales_invoice)
            si = frappe.get_doc("Sales Invoice", r.sales_invoice)
            self.assertEqual(si.docstatus, 1)
            self.assertEqual(si.customer, self.customer)

    def test_auto_invoice_skips_future_rows(self):
        """Rows with due_date in the future stay Projected."""
        future_date = add_days(today(), 60)
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date=future_date,
            package_term_months=3,
            payment_mode="Monthly",
        )

        run_auto_invoice()

        contract.reload()
        self.assertTrue(all(r.state == "Projected" for r in contract.billing_schedule))

    def test_auto_invoice_prepay_single_si(self):
        """Prepay contract: all schedule rows covered by one SI."""
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=12,
            payment_mode="Prepay",
        )
        # Prepay = 1 billing schedule row
        self.assertEqual(len(contract.billing_schedule), 1)

        run_auto_invoice()

        contract.reload()
        self.assertEqual(contract.billing_schedule[0].state, "Invoiced")
        self.assertTrue(contract.billing_schedule[0].sales_invoice)

    def test_auto_invoice_si_has_correct_amount(self):
        """SI amount matches billing schedule row amount."""
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=1,
            payment_mode="Monthly",
        )

        run_auto_invoice()

        contract.reload()
        row = contract.billing_schedule[0]
        si = frappe.get_doc("Sales Invoice", row.sales_invoice)
        self.assertEqual(si.grand_total, row.amount)


class TestPaymentEntryHook(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = ensure_customer()
        cls.sales_person = ensure_employee()
        ensure_branch("HCM")
        ensure_cost_center_mapping("HCM")
        cls.company = _get_company()
        _ensure_income_account(cls.company)
        _ensure_receivable_account(cls.company)

    def _make_invoiced_contract(self):
        """Helper: create contract + run auto_invoice to get an invoiced row with SI."""
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=1,
            payment_mode="Monthly",
        )
        run_auto_invoice()
        contract.reload()
        return contract

    def test_pe_submit_transitions_to_paid(self):
        """Submitting a PE for the full SI amount flips billing schedule to Paid."""
        contract = self._make_invoiced_contract()
        row = contract.billing_schedule[0]
        si = frappe.get_doc("Sales Invoice", row.sales_invoice)

        # Create PE using get_payment_entry
        from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

        pe = get_payment_entry("Sales Invoice", si.name)
        pe.mode_of_payment = "Cash"
        pe.reference_no = f"TEST-PE-{si.name}"
        pe.reference_date = today()
        pe.flags.ignore_permissions = True
        pe.insert()
        pe.submit()

        contract.reload()
        self.assertEqual(contract.billing_schedule[0].state, "Paid")
        self.assertEqual(contract.billing_schedule[0].payment_entry, pe.name)

    def test_partial_payment_stays_invoiced(self):
        """Partial PE (amount < outstanding) does NOT flip to Paid."""
        contract = self._make_invoiced_contract()
        row = contract.billing_schedule[0]
        si = frappe.get_doc("Sales Invoice", row.sales_invoice)

        from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

        pe = get_payment_entry("Sales Invoice", si.name)
        # Halve the payment amount
        pe.paid_amount = si.grand_total / 2
        pe.received_amount = si.grand_total / 2
        for ref in pe.references:
            if ref.reference_name == si.name:
                ref.allocated_amount = si.grand_total / 2
        pe.mode_of_payment = "Cash"
        pe.reference_no = f"TEST-PE-PARTIAL-{si.name}"
        pe.reference_date = today()
        pe.flags.ignore_permissions = True
        pe.insert()
        pe.submit()

        contract.reload()
        # Should remain Invoiced since SI has outstanding
        self.assertIn(contract.billing_schedule[0].state, ["Invoiced", "Overdue"])


class TestOverdueCheck(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = ensure_customer()
        cls.sales_person = ensure_employee()
        ensure_branch("HCM")
        ensure_cost_center_mapping("HCM")
        cls.company = _get_company()
        _ensure_income_account(cls.company)
        _ensure_receivable_account(cls.company)

    def test_overdue_after_grace_period(self):
        """Invoiced rows past due_date + grace_period become Overdue."""
        # Use a past date so due_date is well past grace period
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=1,
            payment_mode="Monthly",
        )

        run_auto_invoice()
        contract.reload()
        self.assertEqual(contract.billing_schedule[0].state, "Invoiced")

        run_overdue_check()
        contract.reload()
        self.assertEqual(contract.billing_schedule[0].state, "Overdue")


class TestExpireContracts(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = ensure_customer()
        cls.sales_person = ensure_employee()
        ensure_branch("HCM")

    def test_expire_past_end_date(self):
        """Active contracts with end_date < today get expired."""
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=1,
        )
        self.assertEqual(contract.status, "Active")
        # end_date should be 2025-01-31 — well in the past

        run_expire_contracts()

        contract.reload()
        self.assertEqual(contract.status, "Expired")

    def test_future_contract_not_expired(self):
        """Active contracts with future end_date stay Active."""
        future_date = add_days(today(), 60)
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date=future_date,
            package_term_months=12,
        )

        run_expire_contracts()

        contract.reload()
        self.assertEqual(contract.status, "Active")


class TestFullChain(FrappeTestCase):
    """End-to-end: Contract → auto-invoice → PE → Paid."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = ensure_customer()
        cls.sales_person = ensure_employee()
        ensure_branch("HCM")
        ensure_cost_center_mapping("HCM")
        cls.company = _get_company()
        _ensure_income_account(cls.company)
        _ensure_receivable_account(cls.company)

    def test_full_lifecycle(self):
        """Contract submit → auto-invoice → PE submit → Paid."""
        # 1. Create + submit contract
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=1,
            payment_mode="Monthly",
        )
        self.assertEqual(contract.status, "Active")
        self.assertEqual(len(contract.billing_schedule), 1)
        self.assertEqual(contract.billing_schedule[0].state, "Projected")

        # 2. Run auto-invoice
        run_auto_invoice()
        contract.reload()
        row = contract.billing_schedule[0]
        self.assertEqual(row.state, "Invoiced")
        self.assertTrue(row.sales_invoice)

        # 3. Create + submit PE for the SI
        si = frappe.get_doc("Sales Invoice", row.sales_invoice)
        from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

        pe = get_payment_entry("Sales Invoice", si.name)
        pe.mode_of_payment = "Cash"
        pe.reference_no = f"TEST-FULL-{si.name}"
        pe.reference_date = today()
        pe.flags.ignore_permissions = True
        pe.insert()
        pe.submit()

        # 4. Verify billing schedule is Paid
        contract.reload()
        self.assertEqual(contract.billing_schedule[0].state, "Paid")
        self.assertEqual(contract.billing_schedule[0].payment_entry, pe.name)


class TestSchedulerGuards(FrappeTestCase):
    """Tests for items 7-9: null income_account, null cost_center, deleted SI."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = ensure_customer()
        cls.sales_person = ensure_employee()
        ensure_branch("HCM")
        cls.company = _get_company()
        _ensure_income_account(cls.company)
        _ensure_receivable_account(cls.company)

    def test_auto_invoice_throws_on_missing_cost_center(self):
        """Auto-invoice with no branch→cost_center mapping throws."""
        # Create contract with a branch that has NO cost center mapping
        ensure_branch("TEST_NO_CC")
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=1,
            payment_mode="Monthly",
            branch="TEST_NO_CC",
        )
        with self.assertRaises(frappe.ValidationError) as ctx:
            run_auto_invoice()
        self.assertIn("Cost center", str(ctx.exception))

    def test_auto_invoice_throws_on_missing_income_account(self):
        """Auto-invoice with no default_income_account throws."""
        ensure_cost_center_mapping("HCM")
        contract = make_active_contract(
            self.customer,
            self.sales_person,
            acceptance_date="2026-01-01",
            package_term_months=1,
            payment_mode="Monthly",
        )
        # Temporarily remove default_income_account
        orig = frappe.db.get_value("Company", self.company, "default_income_account")
        frappe.db.set_value("Company", self.company, "default_income_account", None)
        try:
            with self.assertRaises(frappe.ValidationError) as ctx:
                run_auto_invoice()
            self.assertIn("Income account not configured", str(ctx.exception))
        finally:
            frappe.db.set_value("Company", self.company, "default_income_account", orig)

    def test_pe_hook_deleted_si_no_crash(self):
        """PE hook with a deleted SI → graceful skip, no crash."""
        from dcnet_contract.dcnet_contract.events import _process_si_payment
        # Call with a non-existent SI name — should not raise
        _process_si_payment("NON-EXISTENT-SI-12345", "PE-TEST-001")
