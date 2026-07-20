"""DCNet Contract Template controller.

Handles .docx upload → mammoth HTML conversion, placeholder discovery + validation,
status workflow (Draft → Pending Review → Approved → Archived), and versioning.
"""

import os

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class DCNetContractTemplate(Document):
	def before_save(self):
		file_changed = self.is_new() or self.has_value_changed("template_file")
		if self.template_file and file_changed:
			self._convert_docx_to_html()
		if self.template_html:
			self._discover_placeholders()
			self._generate_placeholder_guide()

	def validate(self):
		self._validate_status_transition()

	def _convert_docx_to_html(self):
		"""Convert uploaded .docx to HTML preserving paragraph alignment and run styles."""
		file_path = self._get_template_file_path()
		if not file_path:
			return

		from dcnet_contract.dcnet_contract.api import _docx_to_styled_html
		self.template_html = _docx_to_styled_html(file_path)

	def _discover_placeholders(self):
		"""Scan template_html for {{...}} markers, populate placeholders child table."""
		from dcnet_contract.dcnet_contract.utils.placeholder_engine import (
			PLACEHOLDER_MAP,
			extract_placeholders_from_html,
			resolve_placeholder,
			validate_template_placeholders,
		)

		if not self.template_html:
			return

		# Get previous version placeholders for removed detection
		previous_keys = None
		if not self.is_new() and self.has_value_changed("template_file"):
			previous_keys = [row.placeholder_key for row in self.placeholders]

		results = validate_template_placeholders(
			self.template_html, previous_version_placeholders=previous_keys
		)

		self.set("placeholders", [])
		for r in results:
			resolved = resolve_placeholder(r.get("raw", r["key"]))
			info = PLACEHOLDER_MAP.get(resolved, {}) if resolved else {}
			self.append("placeholders", {
				"placeholder_key": r["key"],
				"mapped_field": info.get("source", ""),
				"description": info.get("vi", r.get("suggestion", "")),
				"needs_dev_mapping": 1 if r["status"] == "unknown" else 0,
			})

	def _generate_placeholder_guide(self):
		"""Generate bilingual placeholder guide HTML."""
		from dcnet_contract.dcnet_contract.utils.placeholder_engine import (
			generate_placeholder_guide_html,
			resolve_placeholder,
		)

		keys = []
		for row in self.placeholders:
			resolved = resolve_placeholder(row.placeholder_key)
			if resolved:
				keys.append(resolved)
		self.placeholder_guide_html = generate_placeholder_guide_html(keys)

	def _validate_status_transition(self):
		"""Validate status transitions per workflow rules."""
		if self.is_new():
			return

		old_status = self.db_get("status") or "Draft"
		new_status = self.status or "Draft"

		if old_status == new_status:
			return

		allowed = {
			"Draft": ["Pending Review"],
			"Pending Review": ["Draft", "Approved"],
			"Approved": ["Archived", "Draft"],
			"Archived": ["Draft"],
		}

		if new_status not in allowed.get(old_status, []):
			frappe.throw(
				_("Cannot change status from {0} to {1}").format(old_status, new_status)
			)

	def _get_template_file_path(self):
		"""Get absolute path of the attached .docx file."""
		if not self.template_file:
			return None

		try:
			file_doc = frappe.get_doc("File", {"file_url": self.template_file})
			file_path = file_doc.get_full_path()
		except Exception:
			return None

		if not os.path.exists(file_path):
			return None

		return file_path

	# --- Status transition API methods ---

	@frappe.whitelist()
	def submit_for_review(self):
		"""Transition Draft → Pending Review."""
		if self.status != "Draft":
			frappe.throw(_("Only Draft templates can be submitted for review"))
		self.status = "Pending Review"
		self.save()

	@frappe.whitelist()
	def approve_template(self):
		"""Transition Pending Review → Approved. Requires Sales Manager or CEO."""
		if self.status != "Pending Review":
			frappe.throw(_("Only templates in Pending Review can be approved"))
		self.status = "Approved"
		self.approved_by = frappe.session.user
		self.approved_date = now_datetime()
		self.save()

	@frappe.whitelist()
	def reject_template(self):
		"""Transition Pending Review → Draft (rejection)."""
		if self.status != "Pending Review":
			frappe.throw(_("Only templates in Pending Review can be rejected"))
		self.status = "Draft"
		self.reviewed_by = frappe.session.user
		self.reviewed_date = now_datetime()
		self.save()

	@frappe.whitelist()
	def archive_template(self):
		"""Transition Approved → Archived."""
		if self.status != "Approved":
			frappe.throw(_("Only Approved templates can be archived"))
		self.status = "Archived"
		self.save()

	@frappe.whitelist()
	def create_new_version(self):
		"""Clone current template as new Draft with incremented version."""
		new_doc = frappe.copy_doc(self)
		new_doc.version = (self.version or 1) + 1
		new_doc.status = "Draft"
		new_doc.reviewed_by = None
		new_doc.reviewed_date = None
		new_doc.approved_by = None
		new_doc.approved_date = None
		new_doc.template_name = f"{self.template_name} v{new_doc.version}"
		new_doc.insert()
		return new_doc.name


@frappe.whitelist()
def get_template(template_name):
	"""Return template data for auto-filling a contract form."""
	doc = frappe.get_doc("DCNet Contract Template", template_name)
	return {
		"service_type": doc.service_type,
		"contract_type": doc.contract_type,
		"payment_mode": doc.payment_mode,
		"package_term_months": doc.package_term_months,
		"boilerplate_text": doc.boilerplate_text,
		"template_html": doc.template_html,
		"version": doc.version,
		"items": [
			{
				"item_label": row.item_label,
				"description": row.description,
				"uom": row.uom,
				"qty": row.qty,
				"unit_price": row.unit_price,
			}
			for row in doc.default_items
		],
	}
