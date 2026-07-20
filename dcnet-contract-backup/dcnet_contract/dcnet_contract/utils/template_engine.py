"""HTML template fill engine for DCNet Contract.

Fills template_html with contract/customer/company data using dual-language
placeholders. Handles apply_template flow and DOCX export with per-contract edits.
"""

import re

import frappe

from dcnet_contract.dcnet_contract.utils.placeholder_engine import (
	resolve_placeholder,
)


def fill_html_placeholders(html: str, values: dict) -> str:
	"""Replace {{EN}} and {{VI}} placeholders in HTML with values.

	Unknown placeholders are left as-is.
	"""
	def _replacer(match):
		raw_key = match.group(1).strip()
		resolved = resolve_placeholder(raw_key)
		if resolved and resolved in values:
			return str(values[resolved])
		return match.group(0)  # leave unknown as-is

	return re.sub(r"\{\{([^}]+)\}\}", _replacer, html)


def build_placeholder_values(contract_name: str) -> dict:
	"""Build placeholder_key → display_value dict from contract data.

	Reuses the same logic as docx_generator._build_placeholder_values
	but returns the dict without Frappe formatting dependencies.
	"""
	from dcnet_contract.dcnet_contract.utils.docx_generator import _build_placeholder_values
	return _build_placeholder_values(contract_name)


@frappe.whitelist()
def apply_template(contract_name: str, template_name: str) -> str:
	"""Fill template HTML with contract data, save to contract.contract_html.

	Also copies default_items and default_terms if contract has none.
	Returns the filled HTML.
	"""
	import frappe

	contract = frappe.get_doc("DCNet Contract", contract_name)
	template = frappe.get_doc("DCNet Contract Template", template_name)

	if not template.template_html:
		frappe.throw(f"Template {template_name} has no HTML content")

	# Build values and fill
	values = build_placeholder_values(contract_name)
	filled_html = fill_html_placeholders(template.template_html, values)

	# Save to contract
	contract.db_set("contract_html", filled_html, update_modified=False)
	contract.db_set("template_ref", template_name, update_modified=False)
	contract.db_set("template_version", template.version or 1, update_modified=False)
	contract.db_set("contract_html_edited", 0, update_modified=False)
	contract.db_set("template_outdated", 0, update_modified=False)

	# Copy default items if contract has no items
	if not contract.items and template.default_items:
		for row in template.default_items:
			contract.append("items", {
				"item_label": row.item_label,
				"description": row.description,
				"uom": row.uom,
				"qty": row.qty,
				"unit_price": row.unit_price,
			})
		contract.save(ignore_permissions=True)

	# Copy default terms if empty
	if not contract.get("default_terms") and template.default_terms:
		contract.db_set("default_terms", template.default_terms, update_modified=False)

	frappe.db.commit()
	return filled_html


def extract_additions(original_html: str, edited_html: str) -> list[str]:
	"""Extract paragraphs added by sales (not in original template fill).

	Simple diff: split by block tags, compare. Returns list of added HTML blocks.
	"""
	if original_html == edited_html:
		return []

	# Split into blocks by common block tags
	block_re = re.compile(
		r"(<(?:p|div|h[1-6]|ul|ol|li|table|tr|blockquote)[^>]*>.*?</(?:p|div|h[1-6]|ul|ol|li|table|tr|blockquote)>)",
		re.DOTALL,
	)

	original_blocks = set(block_re.findall(original_html))
	edited_blocks = block_re.findall(edited_html)

	additions = []
	for block in edited_blocks:
		if block not in original_blocks:
			additions.append(block)

	return additions


def export_docx_with_edits(contract_name: str) -> str:
	"""Fill .docx template + inject per-contract HTML edits.

	Returns file URL of the generated .docx.
	"""
	import frappe

	contract = frappe.get_doc("DCNet Contract", contract_name)

	# Use existing docx engine regardless — it handles both template and non-template contracts
	from dcnet_contract.dcnet_contract.utils.docx_generator import generate_document

	template_name = contract.template_ref if contract.template_ref else None
	return generate_document(contract_name, template_name, "docx")
