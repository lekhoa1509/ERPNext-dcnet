"""
Data fetcher for drill-down functionality.

Trả về danh sách chứng từ gốc đóng góp vào một chỉ tiêu cụ thể.
"""

import frappe


def get_source_documents(declaration_name, target_named_range):
    """
    Fetches original documents contributing to an indicator.

    Args:
        declaration_name: HTKK Declaration name
        target_named_range: Indicator code (ct23, ct24, ct29, etc.)

    Returns:
        List of source documents with standardized fields:
        - name: Document number
        - posting_date: Date
        - party: Customer/Supplier name
        - base_amount: Amount before tax
        - tax_amount: Tax amount
        - rate: Tax rate
    """
    if not frappe.db.exists("HTKK Declaration", declaration_name):
        return []

    doc = frappe.get_doc("HTKK Declaration", declaration_name)

    # Route to appropriate declaration handler
    if doc.declaration_type == "01/GTGT":
        return _get_vat_source_documents(doc, target_named_range)
    elif doc.declaration_type == "03/TNDN":
        return _get_cit_source_documents(doc, target_named_range)
    elif doc.declaration_type == "05/KK-TNCN":
        return _get_pit_source_documents(doc, target_named_range)

    return []


def _get_vat_source_documents(doc, target_named_range):
    """Get source documents for VAT declaration (01/GTGT)."""
    from dcnet_apps.htkk.declarations import vat_01gtgt

    # Mua vào (Purchases) - ct23, ct24, ct25
    if target_named_range in ["ct23", "ct24", "ct25"]:
        rows = vat_01gtgt.get_bang_ke_mua_vao(doc.company, doc.from_date, doc.to_date)
        return [
            {
                "name": r.get("SHDon") or "N/A",
                "posting_date": r.get("NLap"),
                "party": r.get("NBan"),
                "base_amount": r.get("DThuaKCT"),
                "tax_amount": r.get("TienThue"),
                "rate": r.get("TSuat")
            }
            for r in rows
        ]

    # Bán ra (Sales) - ct26, ct29, ct30, ct31, ct32, ct33
    sales_indicators = {
        "ct26": "KCT",  # Không chịu thuế
        "ct29": "0%",
        "ct30": "5%",
        "ct31": "5%",   # Tax amount for 5%
        "ct32": "10%",
        "ct33": "10%",  # Tax amount for 10%
    }

    if target_named_range in sales_indicators:
        target_rate = sales_indicators[target_named_range]
        rows = vat_01gtgt.get_bang_ke_ban_ra(doc.company, doc.from_date, doc.to_date)
        return [
            {
                "name": r.get("SHDon") or "N/A",
                "posting_date": r.get("NLap"),
                "party": r.get("NMua"),
                "base_amount": r.get("DThuaKCT"),
                "tax_amount": r.get("TienThue"),
                "rate": r.get("TSuat")
            }
            for r in rows
            if r.get("TSuat") == target_rate
        ]

    return []


def _get_cit_source_documents(doc, target_named_range):
    """Get source documents for CIT declaration (03/TNDN)."""
    # CIT typically uses P&L accounts, not individual invoices
    # Return empty for now - could be enhanced to show GL entries
    return []


def _get_pit_source_documents(doc, target_named_range):
    """Get source documents for PIT declaration (05/KK-TNCN)."""
    # Could return Salary Slips for ct21 (taxable income), ct29 (tax deducted)
    if target_named_range in ["ct21", "ct29"]:
        slips = frappe.get_all(
            "Salary Slip",
            filters={
                "company": doc.company,
                "posting_date": ["between", [doc.from_date, doc.to_date]],
                "docstatus": 1
            },
            fields=["name", "posting_date", "employee_name", "gross_pay", "income_tax_deducted"]
        )
        return [
            {
                "name": s.name,
                "posting_date": s.posting_date,
                "party": s.employee_name,
                "base_amount": s.gross_pay,
                "tax_amount": s.income_tax_deducted or 0,
                "rate": ""
            }
            for s in slips
        ]
    return []
