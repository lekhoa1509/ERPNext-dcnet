"""v2 scaffold — webhook receiver for banks that push transaction notifications."""
import frappe


@frappe.whitelist(allow_guest=True)
def receive_bank_push():
    raise NotImplementedError(
        "v2: verify signature via Bank Account.api_credentials, parse payload, "
        "call vn_banking.api.reconcile.trigger_import with source_type=bank_api_<key>."
    )
