import frappe, json
from frappe.model.document import Document


class AssetHandover(Document):
    def validate(self):
        self._check_scope_consistency()
        self._calc_total_value()
        self._check_threshold()

    def _check_scope_consistency(self):
        doctype_map = {"TSCĐ": "Asset", "CCDC": "CCDC Item"}
        expected = doctype_map.get(self.scope)
        if not expected:
            return
        for item in self.handover_items or []:
            if item.target_doctype and item.target_doctype != expected:
                frappe.throw(f"Scope {self.scope} only allows {expected} items, found {item.target_doctype}")

    def _calc_total_value(self):
        self.total_asset_value = sum(r.book_value or 0 for r in self.handover_items or [])

    def _check_threshold(self):
        settings = frappe.get_single("VN Accounting Settings")
        if not getattr(settings, "enable_value_thresholds", None):
            return
        threshold = getattr(settings, "handover_threshold", None) or 100000000
        if (self.total_asset_value or 0) >= threshold and not self.co_signer_employee:
            frappe.throw(
                f"Giá trị tài sản {self.total_asset_value:,.0f} ≥ ngưỡng {threshold:,.0f}. Cần người ký duyệt (co_signer)."
            )

    def on_submit(self):
        self._snapshot_before()
        if self.scope == "TSCĐ":
            self._create_asset_movement()  # must run before _update_targets so source_location != target
        self._update_targets()

    def _snapshot_before(self):
        snapshot = {}
        for item in self.handover_items or []:
            if not item.target_name or not item.target_doctype:
                continue
            doc = frappe.get_doc(item.target_doctype, item.target_name)
            snapshot[item.target_name] = {"location": doc.get("location"), "custodian": doc.get("custodian")}
        self.db_set("before_handover_snapshot", json.dumps(snapshot))

    def _update_targets(self):
        for item in self.handover_items or []:
            if not item.target_name or not item.target_doctype:
                continue
            frappe.db.set_value(item.target_doctype, item.target_name, {
                "location": self.to_location,
                "custodian": self.to_employee,
            })

    def _create_asset_movement(self):
        company = self.company or frappe.defaults.get_defaults().get("company")
        for item in self.handover_items or []:
            if item.target_doctype != "Asset" or not item.target_name:
                continue
            mov = frappe.new_doc("Asset Movement")
            mov.purpose = "Transfer"
            mov.transaction_date = self.posting_date
            mov.company = company
            mov.append("assets", {
                "asset": item.target_name,
                "from_employee": self.from_employee,
                "to_employee": self.to_employee,
                "target_location": self.to_location or "",
            })
            mov.insert(ignore_permissions=True)
            mov.submit()

    def on_cancel(self):
        snapshot = json.loads(self.before_handover_snapshot or "{}")
        for item in self.handover_items or []:
            if not item.target_name or item.target_name not in snapshot:
                continue
            prev = snapshot[item.target_name]
            frappe.db.set_value(item.target_doctype, item.target_name, {
                "location": prev.get("location"),
                "custodian": prev.get("custodian"),
            })
