"""Open PAKD Approval Workflow Draft + Rejected states for any role with
DocType write permission.

Originally Draft.allow_edit = "PAKD Sales Rep" — System Manager and
Accounts Manager were silently blocked from editing draft PAKDs even
though they had DocType write permission, because Frappe Workflow's
allow_edit overrides DocType perms when set.

In Frappe v16 ``allow_edit`` is a single Link → Role (comma-separated
strings fail link validation, and ``is_read_only`` doesn't split them
at runtime). The magic role "All" delegates the actual gate to DocType
permissions, which is what we want for Draft/Rejected.
"""

import frappe

NEW_ALLOW_EDIT = "All"
TARGET_STATES = {"Draft", "Rejected"}


def execute():
	if not frappe.db.exists("Workflow", "PAKD Approval"):
		return

	wf = frappe.get_doc("Workflow", "PAKD Approval")
	changed = False
	for state in wf.states:
		if state.state in TARGET_STATES and state.allow_edit != NEW_ALLOW_EDIT:
			state.allow_edit = NEW_ALLOW_EDIT
			changed = True
	if changed:
		wf.save(ignore_permissions=True)
		frappe.db.commit()
