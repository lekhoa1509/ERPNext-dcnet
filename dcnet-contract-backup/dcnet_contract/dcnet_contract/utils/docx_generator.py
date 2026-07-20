"""Docx template engine for DCNet Contract.

Fills .docx templates with contract data, supports items table cloning,
Vietnamese number-to-words, and PDF conversion via LibreOffice.
"""

import copy
import os
import re
import subprocess
import tempfile

import frappe
from frappe.utils import cint, flt, getdate

# ---------------------------------------------------------------------------
# Placeholder map: key -> (mapped_field_description, human label)
# ---------------------------------------------------------------------------
PLACEHOLDER_MAP = {
    "contract_number": ("doc.name / contract_no_external", "So hop dong"),
    "contract_date": ("doc.contract_date", "Ngay ky hop dong"),
    "customer_name": ("doc.customer_name", "Ten Ben A"),
    "customer_address": ("customer primary address", "Dia chi Ben A"),
    "customer_phone": ("customer phone", "So dien thoai"),
    "customer_fax": ("customer fax", "So fax"),
    "customer_tax_id": ("customer tax_id", "Ma so thue"),
    "customer_representative": ("contact full_name", "Nguoi dai dien"),
    "customer_representative_title": ("contact designation", "Chuc vu nguoi dai dien"),
    "customer_id_number": ("CMND/CCCD", "So CMND/CCCD"),
    "customer_id_date": ("ngay cap CMND", "Ngay cap"),
    "customer_id_place": ("noi cap CMND", "Noi cap"),
    "customer_dob": ("ngay sinh", "Ngay sinh"),
    "customer_email": ("customer email", "Email"),
    "customer_bank_account": ("customer bank account", "Tai khoan ngan hang"),
    "service_type": ("doc.service_type", "Loai dich vu"),
    "package_name": ("doc.package_name", "Ten goi cuoc"),
    "installation_address": ("doc.installation_address", "Dia chi lap dat"),
    "setup_fee": ("doc.setup_fee", "Phi lap dat"),
    "setup_fee_vat": ("setup_fee * 10%", "VAT phi lap dat"),
    "setup_fee_total": ("setup_fee * 110%", "Tong phi lap dat"),
    "setup_fee_words": ("so tien bang chu", "Phi lap dat bang chu"),
    "monthly_fee": ("doc.unit_price_total", "Cuoc hang thang"),
    "monthly_fee_vat": ("monthly_fee * 10%", "VAT cuoc hang thang"),
    "monthly_fee_total": ("monthly_fee * 110%", "Tong cuoc hang thang"),
    "monthly_fee_words": ("so tien bang chu", "Cuoc hang thang bang chu"),
    "package_term": ("doc.package_term_months", "Thoi han hop dong"),
    "acceptance_date": ("doc.acceptance_date", "Ngay nghiem thu"),
    "end_date": ("doc.end_date", "Ngay ket thuc"),
    "bandwidth": ("bandwidth", "Bang thong"),
    "point_a": ("diem dau", "Diem dau"),
    "point_b": ("diem cuoi", "Diem cuoi"),
    "sla_restore_hours": ("thoi gian khac phuc", "SLA khac phuc su co"),
    # Party B (company) placeholders
    "company_name_b": ("company name", "Ten Ben B"),
    "company_address_b": ("company address", "Dia chi Ben B"),
    "company_phone_b": ("company phone", "Dien thoai Ben B"),
    "company_fax_b": ("company fax", "Fax Ben B"),
    "company_tax_id_b": ("company tax_id", "Ma so thue Ben B"),
    "company_representative_b": ("company representative", "Nguoi dai dien Ben B"),
    "company_representative_title_b": ("company rep title", "Chuc vu nguoi dai dien Ben B"),
    "company_bank_account_b": ("company bank account", "Tai khoan ngan hang Ben B"),
    "company_bank_b": ("company bank name", "Ngan hang Ben B"),
    # Items table placeholders
    "item_stt": ("row index", "STT"),
    "item_label": ("item.item_label", "Ten hang muc"),
    "item_qty": ("item.qty", "So luong"),
    "item_uom": ("item.uom", "Don vi"),
    "item_price": ("item.unit_price", "Don gia"),
    "item_amount": ("item.amount_per_period", "Thanh tien"),
}


# ---------------------------------------------------------------------------
# Vietnamese number-to-words
# ---------------------------------------------------------------------------
_ONES = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
_GROUPS = ["", "nghìn", "triệu", "tỷ"]


def _number_to_words_vi(amount: int) -> str:
    """Convert VND integer amount to Vietnamese words with diacritics.

    Examples:
        0 -> "Không đồng"
        550 -> "Năm trăm năm mươi đồng"
        3300000 -> "Ba triệu ba trăm nghìn đồng"
    """
    if amount == 0:
        return "Không đồng"
    if amount < 0:
        return "Âm " + _number_to_words_vi(-amount).replace(" đồng", "") + " đồng"

    # Split into groups of 3 digits from right
    groups = []
    n = amount
    while n > 0:
        groups.append(n % 1000)
        n //= 1000

    parts = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        group_words = _three_digits_to_words(g, needs_leading_zero=(i < len(groups) - 1 and g < 100))
        suffix = _GROUPS[i]
        parts.append(group_words + (" " + suffix if suffix else ""))

    result = " ".join(parts).strip()
    # Capitalize first letter
    result = result[0].upper() + result[1:] if result else ""
    return result + " đồng"


def _three_digits_to_words(n: int, needs_leading_zero: bool = False) -> str:
    """Convert a 3-digit number to Vietnamese words with diacritics."""
    hundreds = n // 100
    tens = (n % 100) // 10
    ones = n % 10

    parts = []

    if hundreds > 0:
        parts.append(_ONES[hundreds] + " trăm")
    elif needs_leading_zero and (tens > 0 or ones > 0):
        parts.append("không trăm")

    if tens > 1:
        parts.append(_ONES[tens] + " mươi")
        if ones == 1:
            parts.append("mốt")
        elif ones == 5:
            parts.append("lăm")
        elif ones == 4:
            parts.append("tư")
        elif ones > 0:
            parts.append(_ONES[ones])
    elif tens == 1:
        parts.append("mười")
        if ones == 5:
            parts.append("lăm")
        elif ones > 0:
            parts.append(_ONES[ones])
    elif ones > 0:
        if hundreds > 0 or needs_leading_zero:
            parts.append("lẻ")
        parts.append(_ONES[ones])

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Vietnamese date formatting
# ---------------------------------------------------------------------------
def _format_date_vi(d) -> str:
    """Format date as 'ngày DD tháng MM năm YYYY'."""
    if not d:
        return ""
    d = getdate(d)
    return f"ngày {d.day:02d} tháng {d.month:02d} năm {d.year}"


def _format_currency(amount) -> str:
    """Format number with comma separator: 3000000 -> '3,000,000'."""
    amount = cint(flt(amount))
    return f"{amount:,}"


# ---------------------------------------------------------------------------
# Placeholder value builder
# ---------------------------------------------------------------------------
def _build_placeholder_values(contract_name: str) -> dict:
    """Build dict of placeholder_key -> display_value from contract data.

    Customer info is read directly from contract fields (populated on form via auto-fill).
    Company info is looked up from the Company DocType (rarely changes).
    """
    doc = frappe.get_doc("DCNet Contract", contract_name)

    monthly = flt(doc.unit_price_total or 0)
    setup = flt(doc.setup_fee or 0)

    values = {
        # Contract info
        "contract_number": doc.get("contract_no_external") or doc.name,
        "contract_date": _format_date_vi(doc.contract_date) if doc.get("contract_date") else "",
        # Party A — read directly from contract fields
        "customer_name": doc.customer_name or "",
        "customer_address": doc.get("customer_address") or "",
        "customer_phone": doc.get("customer_phone") or "",
        "customer_fax": doc.get("customer_fax") or "",
        "customer_tax_id": doc.get("customer_tax_id") or "",
        "customer_representative": doc.get("customer_representative") or "",
        "customer_representative_title": doc.get("customer_representative_title") or "",
        "customer_id_number": doc.get("customer_id_number") or "",
        "customer_id_date": _format_date_vi(doc.get("customer_id_date")) if doc.get("customer_id_date") else "",
        "customer_id_place": doc.get("customer_id_place") or "",
        "customer_dob": _format_date_vi(doc.get("customer_dob")) if doc.get("customer_dob") else "",
        "customer_email": doc.get("customer_email") or "",
        "customer_bank_account": doc.get("customer_bank_account") or "",
        # Service & fees
        "service_type": doc.service_type or "",
        "package_name": doc.get("package_name") or "",
        "installation_address": doc.get("installation_address") or "",
        "setup_fee": _format_currency(setup),
        "setup_fee_vat": _format_currency(setup * 0.1),
        "setup_fee_total": _format_currency(setup * 1.1),
        "setup_fee_words": _number_to_words_vi(cint(setup * 1.1)),
        "monthly_fee": _format_currency(monthly),
        "monthly_fee_vat": _format_currency(monthly * 0.1),
        "monthly_fee_total": _format_currency(monthly * 1.1),
        "monthly_fee_words": _number_to_words_vi(cint(monthly * 1.1)),
        "package_term": str(doc.package_term_months or ""),
        "acceptance_date": _format_date_vi(doc.acceptance_date) if doc.acceptance_date else "",
        "end_date": _format_date_vi(doc.end_date) if doc.end_date else "",
        # Technical
        "bandwidth": doc.get("bandwidth") or "",
        "point_a": doc.get("point_a") or "",
        "point_b": doc.get("point_b") or "",
        "sla_restore_hours": str(doc.get("sla_restore_hours") or ""),
    }

    # Party B (company) info — looked up from Company (rarely changes)
    # Representative comes from contract fields first, then Company fallback
    if doc.company:
        company = frappe.get_doc("Company", doc.company)
        values["company_name_b"] = company.company_name or ""
        values["company_address_b"] = company.get("address") or ""
        values["company_phone_b"] = company.get("phone_no") or ""
        values["company_fax_b"] = company.get("fax") or ""
        values["company_tax_id_b"] = company.get("tax_id") or ""

        # Representative: contract field > Company field
        values["company_representative_b"] = (
            doc.get("company_representative") or company.get("representative") or ""
        )
        values["company_representative_title_b"] = (
            doc.get("company_representative_title") or company.get("representative_title") or ""
        )

        # Company bank account
        company_bank = frappe.db.get_value(
            "Bank Account",
            {"company": doc.company, "is_company_account": 1, "is_default": 1},
            ["bank_account_no", "bank"],
            as_dict=True,
        )
        if company_bank:
            values["company_bank_account_b"] = company_bank.bank_account_no or ""
            values["company_bank_b"] = company_bank.bank or ""
        else:
            values["company_bank_account_b"] = ""
            values["company_bank_b"] = ""
    else:
        for key in ["company_name_b", "company_address_b", "company_phone_b",
                     "company_fax_b", "company_tax_id_b", "company_representative_b",
                     "company_representative_title_b", "company_bank_account_b",
                     "company_bank_b"]:
            values[key] = ""

    # Ensure no None values
    return {k: (v if v is not None else "") for k, v in values.items()}


def _build_items_list(contract_name: str) -> list[dict]:
    """Build list of item dicts for table cloning."""
    doc = frappe.get_doc("DCNet Contract", contract_name)
    items = []
    for idx, row in enumerate(doc.items, 1):
        items.append({
            "item_stt": str(idx),
            "item_label": row.item_label or "",
            "item_qty": str(cint(row.qty)),
            "item_uom": row.uom or "",
            "item_price": _format_currency(row.unit_price),
            "item_amount": _format_currency((row.qty or 0) * (row.unit_price or 0)),
        })
    return items


# ---------------------------------------------------------------------------
# Docx fill engine — run merging + placeholder replacement
# ---------------------------------------------------------------------------
def _merge_runs_for_placeholders(paragraph):
    """Merge adjacent runs that together form a {{...}} pattern.

    Word often splits text across multiple XML runs, e.g.:
      run1.text = "{{place"
      run2.text = "holder}}"
    This function merges them so replacement works.
    """
    if not paragraph.runs:
        return

    # Join all run texts to find placeholders
    full_text = "".join(run.text for run in paragraph.runs)
    if "{{" not in full_text:
        return

    # Find placeholder positions in the joined text
    placeholders = list(re.finditer(r"\{\{[^}]+\}\}", full_text))
    if not placeholders:
        return

    # Build character-to-run mapping
    char_to_run = []
    for run_idx, run in enumerate(paragraph.runs):
        for _ in run.text:
            char_to_run.append(run_idx)

    # For each placeholder, check if it spans multiple runs
    runs_to_merge = set()
    for match in placeholders:
        start_run = char_to_run[match.start()]
        end_run = char_to_run[match.end() - 1]
        if start_run != end_run:
            for r in range(start_run, end_run + 1):
                runs_to_merge.add((start_run, r))

    if not runs_to_merge:
        return

    # Merge: collect text into first run of each group, clear others
    # Simple approach: rebuild paragraph runs
    merged_text = full_text
    # Clear all runs and set merged text on first run
    if paragraph.runs:
        paragraph.runs[0].text = merged_text
        for run in paragraph.runs[1:]:
            run.text = ""


def _replace_in_paragraph(paragraph, values: dict):
    """Replace {{key}} placeholders in a paragraph's runs."""
    _merge_runs_for_placeholders(paragraph)
    for run in paragraph.runs:
        if "{{" in run.text:
            for key, val in values.items():
                run.text = run.text.replace("{{" + key + "}}", str(val))


def _fill_docx(doc_path: str, values: dict, items: list[dict]) -> str:
    """Fill a .docx template with values and items. Returns path to filled file."""
    from docx import Document as DocxDocument

    doc = DocxDocument(doc_path)

    # Replace in all paragraphs
    for para in doc.paragraphs:
        _replace_in_paragraph(para, values)

    # Replace in all tables (non-item tables)
    item_table = None
    template_row_idx = None

    for table in doc.tables:
        for row_idx, row in enumerate(table.rows):
            row_text = "".join(cell.text for cell in row.cells)
            if "{{item_stt}}" in row_text:
                item_table = table
                template_row_idx = row_idx
                break

        if item_table:
            break

        # Regular table — just replace placeholders
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    _replace_in_paragraph(para, values)

    # Handle items table
    if item_table and template_row_idx is not None:
        _clone_item_rows(item_table, template_row_idx, items, values)

    # Replace in headers/footers
    for section in doc.sections:
        if section.header:
            for para in section.header.paragraphs:
                _replace_in_paragraph(para, values)
        if section.footer:
            for para in section.footer.paragraphs:
                _replace_in_paragraph(para, values)

    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    doc.save(tmp.name)
    tmp.close()
    return tmp.name


def _clone_item_rows(table, template_row_idx: int, items: list[dict], values: dict):
    """Clone template row for each item, then remove template row."""
    from docx.oxml.ns import qn
    from copy import deepcopy

    template_row = table.rows[template_row_idx]
    template_tr = template_row._tr

    # Insert cloned rows after template
    last_tr = template_tr
    for item in items:
        new_tr = deepcopy(template_tr)
        # Replace placeholders in cloned row
        for tc in new_tr.findall(qn("w:tc")):
            for p in tc.findall(qn("w:p")):
                _replace_in_xml_paragraph(p, item)
                _replace_in_xml_paragraph(p, values)
        last_tr.addnext(new_tr)
        last_tr = new_tr

    # Add total/VAT/grand total rows
    monthly_total = sum(
        (int(it.get("item_qty", "0") or 0) * _parse_currency(it.get("item_price", "0")))
        for it in items
    )
    summary_rows = [
        ("", "Tong cong", "", "", "", _format_currency(monthly_total)),
        ("", "VAT (10%)", "", "", "", _format_currency(monthly_total * 0.1)),
        ("", "Tong cong (da bao gom VAT)", "", "", "", _format_currency(monthly_total * 1.1)),
    ]
    for stt, label, qty, uom, price, amount in summary_rows:
        new_tr = deepcopy(template_tr)
        summary_values = {
            "item_stt": stt,
            "item_label": label,
            "item_qty": qty,
            "item_uom": uom,
            "item_price": price,
            "item_amount": amount,
        }
        for tc in new_tr.findall(qn("w:tc")):
            for p in tc.findall(qn("w:p")):
                _replace_in_xml_paragraph(p, summary_values)
                _replace_in_xml_paragraph(p, values)
        last_tr.addnext(new_tr)
        last_tr = new_tr

    # Remove template row
    template_tr.getparent().remove(template_tr)


def _replace_in_xml_paragraph(p_element, values: dict):
    """Replace {{key}} in XML paragraph element runs."""
    from docx.oxml.ns import qn

    runs = p_element.findall(qn("w:r"))
    for r in runs:
        t = r.find(qn("w:t"))
        if t is not None and t.text and "{{" in t.text:
            for key, val in values.items():
                t.text = t.text.replace("{{" + key + "}}", str(val))


def _parse_currency(s: str) -> int:
    """Parse formatted currency string back to int: '3,000,000' -> 3000000."""
    if not s:
        return 0
    return int(s.replace(",", "").replace(".", "").strip() or 0)


# ---------------------------------------------------------------------------
# PDF conversion
# ---------------------------------------------------------------------------
def _convert_to_pdf(docx_path: str) -> str:
    """Convert .docx to .pdf using LibreOffice headless."""
    outdir = os.path.dirname(docx_path)
    result = subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", outdir, docx_path],
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0:
        frappe.throw(f"PDF conversion failed: {result.stderr.decode()}")
    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    if not os.path.exists(pdf_path):
        frappe.throw("PDF conversion produced no output file")
    return pdf_path


# ---------------------------------------------------------------------------
# Placeholder discovery (for template upload)
# ---------------------------------------------------------------------------
def discover_placeholders(file_path: str) -> list[dict]:
    """Scan a .docx file for {{...}} markers. Returns list of dicts."""
    from docx import Document as DocxDocument

    doc = DocxDocument(file_path)
    found = set()

    def _scan_paragraphs(paragraphs):
        for para in paragraphs:
            text = "".join(run.text for run in para.runs)
            for match in re.finditer(r"\{\{(\w+)\}\}", text):
                found.add(match.group(1))

    _scan_paragraphs(doc.paragraphs)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                _scan_paragraphs(cell.paragraphs)

    for section in doc.sections:
        if section.header:
            _scan_paragraphs(section.header.paragraphs)
        if section.footer:
            _scan_paragraphs(section.footer.paragraphs)

    results = []
    for key in sorted(found):
        mapped, desc = PLACEHOLDER_MAP.get(key, ("", ""))
        results.append({
            "placeholder_key": key,
            "mapped_field": mapped,
            "description": desc,
        })
    return results


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def generate_document(contract_name: str, template_name: str | None = None,
                      output_format: str = "docx") -> str:
    """Generate filled contract document.

    Args:
        contract_name: DCNet Contract name
        template_name: DCNet Contract Template name (auto-detect from contract if None)
        output_format: "docx" or "pdf"

    Returns:
        File URL of generated document (attached to contract)
    """
    # Get template
    if not template_name:
        doc = frappe.get_doc("DCNet Contract", contract_name)
        template_name = doc.get("contract_template")
        if not template_name:
            frappe.throw("No template specified and no default template on contract")

    template = frappe.get_doc("DCNet Contract Template", template_name)
    if not template.template_file:
        frappe.throw(f"Template '{template_name}' has no .docx file attached")

    # Download template file
    file_doc = frappe.get_doc("File", {"file_url": template.template_file})
    template_path = file_doc.get_full_path()

    # Build values and items
    values = _build_placeholder_values(contract_name)
    items = _build_items_list(contract_name)

    # Fill template
    filled_path = _fill_docx(template_path, values, items)

    # Convert to PDF if needed
    if output_format == "pdf":
        final_path = _convert_to_pdf(filled_path)
        ext = "pdf"
    else:
        final_path = filled_path
        ext = "docx"

    # Attach to contract
    contract_doc = frappe.get_doc("DCNet Contract", contract_name)
    filename = f"{contract_doc.name}-{template.template_name}.{ext}"
    filename = re.sub(r"[^\w\-.]", "_", filename)

    with open(final_path, "rb") as f:
        file_content = f.read()

    attached = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "content": file_content,
        "attached_to_doctype": "DCNet Contract",
        "attached_to_name": contract_name,
        "is_private": 1,
    })
    attached.save(ignore_permissions=True)

    # Cleanup temp files
    try:
        os.unlink(filled_path)
        if output_format == "pdf" and filled_path != final_path:
            os.unlink(final_path)
    except OSError:
        pass

    return attached.file_url


# ---------------------------------------------------------------------------
# HTML generation for print format (single source of truth = DOCX template)
# ---------------------------------------------------------------------------
def generate_html_for_print(contract_name: str, template_name: str | None = None) -> str:
    """Generate filled HTML from DOCX template for use in Frappe print format.

    Uses mammoth to convert the filled .docx to clean HTML.
    Auto-detects template from contract's service_type if not specified.
    """
    import mammoth

    # Auto-detect template from service_type
    if not template_name:
        doc = frappe.get_doc("DCNet Contract", contract_name)
        matches = frappe.get_all(
            "DCNet Contract Template",
            filters={"template_file": ["is", "set"], "service_type": doc.service_type or ""},
            fields=["name"],
            limit=1,
        )
        if matches:
            template_name = matches[0].name
        else:
            # Fallback to generic template
            matches = frappe.get_all(
                "DCNet Contract Template",
                filters={"template_file": ["is", "set"]},
                fields=["name"],
                limit=1,
            )
            if matches:
                template_name = matches[0].name
            else:
                return "<p>Khong tim thay mau hop dong DOCX.</p>"

    template = frappe.get_doc("DCNet Contract Template", template_name)
    if not template.template_file:
        return f"<p>Mau '{template_name}' chua co file .docx dinh kem.</p>"

    file_doc = frappe.get_doc("File", {"file_url": template.template_file})
    template_path = file_doc.get_full_path()

    # Build values, fill template
    values = _build_placeholder_values(contract_name)
    items = _build_items_list(contract_name)
    filled_path = _fill_docx(template_path, values, items)

    # Convert to HTML via mammoth
    with open(filled_path, "rb") as f:
        result = mammoth.convert_to_html(f)

    # Cleanup temp file
    try:
        os.unlink(filled_path)
    except OSError:
        pass

    return result.value


def generate_appendix_html_for_print(contract_name: str) -> str:
    """Generate filled HTML from appendix DOCX template for print format.

    Auto-detects the appendix template (category=Phu luc) matching service_type.
    """
    doc = frappe.get_doc("DCNet Contract", contract_name)
    matches = frappe.get_all(
        "DCNet Contract Template",
        filters={
            "template_file": ["is", "set"],
            "service_type": doc.service_type or "",
            "template_category": "Phụ lục",
        },
        fields=["name"],
        limit=1,
    )
    if matches:
        return generate_html_for_print(contract_name, matches[0].name)

    # No appendix template for this service_type
    return "<p>Khong tim thay mau phu luc cho loai dich vu nay.</p>"
