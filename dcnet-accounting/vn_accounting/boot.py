"""Boot session for vn_accounting.

Two responsibilities:

1. `apply_branch_sidebar_item_access` — branch-level filtering of sidebar items
   (e.g., Branch Cash Entry items hidden when user is not assigned to a branch).
2. `_claim_workspace_ownership` — cross-workspace DocType ownership. Frappe's
   sidebar.js looks up `frappe.boot.workspace_sidebar_item[entity_name.lower()]`
   to decide which workspace's sidebar to show after navigation. We override
   the dict AFTER Frappe core builds it, claiming ERPNext-owned DocTypes that
   are conceptually VN Accounting territory (Phiếu kế toán = JE, Phiếu thanh
   toán = PE) so the sidebar context stays "VN Accounting" on drill-down.

Workspace sidebar routing + role gating live in dcnet_theme (merged from the
standalone dcnet_sidebar_routing app, which has been removed).

See: vn_accounting/branch_sidebar_access.py
"""

from vn_accounting.branch_sidebar_access import apply_branch_sidebar_item_access

# DocTypes that ERPNext owns but should preserve VN Accounting sidebar context
# when navigated to (drill-down from reports, "Create Payment" button, etc.).
# Add a DocType here when a VN-first site wants its drill-down to keep the
# VN Accounting sidebar instead of jumping to the ERPNext default workspace.
VN_OWNED_DOCTYPES = [
	"Journal Entry",
	"Payment Entry",
	# Mua hàng — claimed so sidebar stays "VN Accounting" on drill-down
	"Purchase Order",
	"Purchase Invoice",
	"Purchase Receipt",
	# Bán hàng — claimed so sidebar stays "VN Accounting" on drill-down
	"Quotation",
	"Sales Order",
	"Sales Invoice",
	# Kho — claimed so sidebar stays "VN Accounting" on drill-down
	"Stock Entry",
	"Stock Reconciliation",
	# TSCĐ — claimed so sidebar stays "VN Accounting" on drill-down
	"Asset",
	"Asset Depreciation Schedule",
	# Tiền lương — claimed so sidebar stays "VN Accounting" on drill-down
	"Payroll Entry",
	"Salary Slip",
	"Salary Structure",
	# Phase A — Quick wins
	"Account",        # F-DM-001
	"Delivery Note",  # F-BH-004
	# Phase C — Hợp đồng section
	"DCNet Contract",
	# Phase D — PAKD section
	"Phuong An Kinh Doanh",
]


def boot_session(bootinfo):
	apply_branch_sidebar_item_access(bootinfo)
	_claim_workspace_ownership(bootinfo)
	_inject_vn_accounting_settings(bootinfo)


def _inject_vn_accounting_settings(bootinfo):
	"""Expose a small subset of VN Accounting Settings to client JS via boot.

	Source-doc form hooks (PI/SE/DN/EC) read these flags to toggle field
	visibility without an extra round-trip.
	"""
	try:
		import frappe
		bootinfo.vn_accounting = bootinfo.get("vn_accounting") or {}
		bootinfo.vn_accounting["auto_show_stage_picker_on_source_docs"] = int(
			frappe.db.get_single_value(
				"VN Accounting Settings", "auto_show_stage_picker_on_source_docs"
			) or 0
		)
	except Exception:
		# Settings DocType missing column on fresh install before migrate; default off.
		bootinfo.vn_accounting = bootinfo.get("vn_accounting") or {}
		bootinfo.vn_accounting["auto_show_stage_picker_on_source_docs"] = 0


def _claim_workspace_ownership(bootinfo):
	"""Override `workspace_sidebar_item` dict to claim cross-workspace DocTypes.

	`bootinfo` is a `frappe._dict`. `workspace_sidebar_item` is a dict mapping
	`entity_name_lower` to a Workspace Sidebar object `{label, items, header_icon,
	module_onboarding, module, app}`. Frappe core populates it; we mutate after
	core is done so our writes win (vn_accounting loads after frappe + erpnext
	per apps.txt order).

	IMPORTANT — Frappe v16.17 dict-value shape: prior versions of this hook
	wrote a bare STRING ("VN Accounting") into the dict. Frappe v16's
	`desktop.js:get_route()` and other consumers call `.items.find(...)` on the
	value, expecting an object with an `.items` array. Writing a string crashes
	rendering for every Desktop Icon whose label happens to match a VN_OWNED
	entry — only one icon survives, the rest vanish. Fix: copy the existing
	"VN Accounting" workspace object reference so claimed entries point to the
	same shape Frappe expects.
	"""
	sidebar_map = bootinfo.get("workspace_sidebar_item")
	if not isinstance(sidebar_map, dict):
		return
	vn_workspace = sidebar_map.get("vn accounting")
	if not isinstance(vn_workspace, dict):
		# VN Accounting workspace not loaded for this user (perms or role gate);
		# skip override to avoid breaking the dict shape.
		return
	for dt in VN_OWNED_DOCTYPES:
		sidebar_map[dt.lower()] = vn_workspace
