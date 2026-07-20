import frappe


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Type", "fieldname": "type", "fieldtype": "Data", "width": 80},
        {"label": "Name", "fieldname": "name", "fieldtype": "Data", "width": 160},
        {"label": "Location", "fieldname": "location", "fieldtype": "Data", "width": 140},
        {"label": "Custodian", "fieldname": "custodian", "fieldtype": "Data", "width": 120},
        {"label": "Book Value", "fieldname": "book_value", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]

    data = []
    # TSCĐ rows
    asset_filters = {"docstatus": 1}
    if filters.get("location"):
        asset_filters["location"] = filters["location"]
    for a in frappe.get_all("Asset", filters=asset_filters,
                             fields=["name", "location", "custodian", "total_asset_cost", "status"]):
        data.append({"type": "TSCĐ", "name": a.name, "location": a.location,
                     "custodian": a.custodian, "book_value": a.total_asset_cost, "status": a.status})

    # CCDC rows (only if DocType exists). frappe.db.table_exists tự thêm tiền tố "tab"
    # → truyền "CCDC Item" (KHÔNG phải "tabCCDC Item", sẽ thành "tabtabCCDC Item" và luôn False).
    if frappe.db.table_exists("CCDC Item"):
        ccdc_filters = {"docstatus": 1}
        if filters.get("location"):
            ccdc_filters["location"] = filters["location"]
        for c in frappe.get_all("CCDC Item", filters=ccdc_filters,
                                 fields=["name", "location", "custodian", "cost", "status"]):
            data.append({"type": "CCDC", "name": c.name, "location": c.location,
                         "custodian": c.custodian, "book_value": c.cost, "status": c.status})

    return columns, data
