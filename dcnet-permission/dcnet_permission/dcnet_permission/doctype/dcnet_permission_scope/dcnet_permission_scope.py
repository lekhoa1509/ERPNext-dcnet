import frappe
from frappe import _
from frappe.model.document import Document


PROTECTED_ROLES = {"Administrator", "System Manager"}


class DCNETPermissionScope(Document):
    def validate(self):
        self._validate_manager()
        self._validate_allowed_roles()
        self._validate_extra_permission_profiles()

    def on_update(self):
        self._sync_permission_manager_access()

    def after_delete(self):
        self._sync_permission_manager_access()

    def _validate_manager(self):
        if not self.manager_role and not self.manager_user:
            frappe.throw(_("Manager Role or Manager User is required."))

    def _validate_allowed_roles(self):
        seen = set()
        for row in self.allowed_roles:
            if row.role in seen:
                frappe.throw(_("Role {0} is duplicated.").format(frappe.bold(row.role)))
            seen.add(row.role)

            if row.role in PROTECTED_ROLES:
                frappe.throw(_("Role {0} cannot be delegated from this tool.").format(frappe.bold(row.role)))

            disabled = frappe.db.get_value("Role", row.role, "disabled")
            if disabled:
                frappe.throw(_("Role {0} is disabled.").format(frappe.bold(row.role)))

    def _validate_extra_permission_profiles(self):
        from dcnet_permission.permission_manager import (
            get_inherent_permission_profile_keys,
            get_permission_profile_keys,
            get_permission_profile_label,
            normalize_profile_key,
        )

        valid_profiles = set(get_permission_profile_keys())
        allowed_roles = [row.role for row in self.get("allowed_roles", []) if row.role]
        inherent_profiles = get_inherent_permission_profile_keys(self.department, allowed_roles)
        seen = set()
        for row in self.get("extra_permission_profiles", []):
            profile = normalize_profile_key(row.profile)
            if not profile:
                continue
            if profile not in valid_profiles:
                frappe.throw(_("Permission Profile {0} is not supported.").format(frappe.bold(row.profile)))
            if profile in inherent_profiles:
                frappe.throw(
                    _("Permission Profile {0} is already included by department {1} and cannot be added again.").format(
                        frappe.bold(get_permission_profile_label(profile)),
                        frappe.bold(self.department),
                    )
                )
            if profile in seen:
                frappe.throw(
                    _("Permission Profile {0} is duplicated.").format(
                        frappe.bold(get_permission_profile_label(profile))
                    )
                )
            seen.add(profile)

    def _sync_permission_manager_access(self):
        try:
            from dcnet_permission.install import ensure_navigation_access

            ensure_navigation_access()
        except Exception:
            frappe.log_error(
                title=_("DCNET Permission access sync failed"),
                message=frappe.get_traceback(),
            )
