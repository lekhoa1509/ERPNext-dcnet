from frappe.tests import IntegrationTestCase

from dcnet_permission.permission_manager import (
    BUSINESS_PERMISSION_PROFILES,
    get_available_extra_permission_profiles,
    get_inherent_permission_profile_keys,
    get_permission_profiles,
    get_profile_doctype_specs,
    normalize_profile_key,
)


class TestPermissionProfiles(IntegrationTestCase):
    def test_profile_keys_and_labels_are_unique_and_normalizable(self):
        keys = [profile["key"] for profile in BUSINESS_PERMISSION_PROFILES]
        labels = [profile["label"] for profile in BUSINESS_PERMISSION_PROFILES]

        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(labels), len(set(labels)))
        for profile in BUSINESS_PERMISSION_PROFILES:
            self.assertEqual(normalize_profile_key(profile["label"]), profile["key"])

    def test_granular_accounting_profile_does_not_grant_full_accounting(self):
        profiles = get_permission_profiles(profile_keys=["Accounting - Cash & Banking"])
        doctypes = {spec["name"] for spec in get_profile_doctype_specs(profiles)}

        self.assertEqual(
            doctypes,
            {"Bank Account", "Bank Transaction", "Payment Entry"},
        )
        self.assertNotIn("Journal Entry", doctypes)
        self.assertNotIn("Sales Invoice", doctypes)

    def test_granular_sales_crm_profile_is_limited_to_crm_and_customer_data(self):
        profiles = get_permission_profiles(profile_keys=["Sales - CRM"])
        doctypes = {spec["name"] for spec in get_profile_doctype_specs(profiles)}

        self.assertEqual(
            doctypes,
            {"Lead", "Opportunity", "Campaign", "Customer", "Contact", "Address"},
        )
        self.assertNotIn("Sales Order", doctypes)
        self.assertNotIn("Sales Invoice", doctypes)

    def test_legacy_umbrella_profile_remains_supported(self):
        profiles = get_permission_profiles(profile_keys=["Accounting"])

        self.assertEqual([profile["key"] for profile in profiles], ["accounting"])

    def test_accounting_scope_only_offers_cross_department_profiles(self):
        inherent = get_inherent_permission_profile_keys(
            "Kế Toán - DCNET",
            ["Accounts User", "Accounts Manager"],
        )
        available = {
            profile["key"]
            for profile in get_available_extra_permission_profiles(
                "Kế Toán - DCNET",
                ["Accounts User", "Accounts Manager"],
            )
        }

        self.assertIn("accounting", inherent)
        self.assertIn("accounting_cash_banking", inherent)
        self.assertNotIn("accounting", available)
        self.assertNotIn("accounting_cash_banking", available)
        self.assertIn("hr_attendance", available)
        self.assertIn("sales_crm", available)

    def test_role_also_excludes_its_inherent_department_catalog(self):
        available = {
            profile["key"]
            for profile in get_available_extra_permission_profiles(
                "Phòng nghiệp vụ đặc biệt",
                ["Sales User"],
            )
        }

        self.assertNotIn("sales", available)
        self.assertNotIn("sales_orders", available)
        self.assertIn("accounting_cash_banking", available)
