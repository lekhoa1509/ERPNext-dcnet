import frappe


# -------------------------------------------------
# PURCHASE RECEIPT EVENT
# -------------------------------------------------

def update_po_from_receipt(doc, method):

    for item in doc.items:

        if item.purchase_order:
            update_po_state(item.purchase_order)


# -------------------------------------------------
# PURCHASE INVOICE EVENT
# -------------------------------------------------

def update_po_from_invoice(doc, method):

    for item in doc.items:

        if item.purchase_order:
            update_po_state(item.purchase_order)


# -------------------------------------------------
# MAIN STATE UPDATE
# -------------------------------------------------

def update_po_state(doc, method=None):

    # handle both string and doc
    if isinstance(doc, str):
        po_name = doc
    else:
        po_name = doc.name

    po = frappe.get_doc("Purchase Order", po_name)

    # chỉ chạy khi PO đã submit
    if po.docstatus != 1:
        return


    # -------------------------------
    # GET TOTAL DATA
    # -------------------------------

    total_qty = frappe.db.sql("""
        SELECT SUM(qty)
        FROM `tabPurchase Order Item`
        WHERE parent=%s
    """, po_name)[0][0] or 0


    received_qty = frappe.db.sql("""
        SELECT SUM(received_qty)
        FROM `tabPurchase Order Item`
        WHERE parent=%s
    """, po_name)[0][0] or 0


    total_amt = frappe.db.sql("""
        SELECT SUM(amount)
        FROM `tabPurchase Order Item`
        WHERE parent=%s
    """, po_name)[0][0] or 0


    billed_amt = frappe.db.sql("""
        SELECT SUM(billed_amt)
        FROM `tabPurchase Order Item`
        WHERE parent=%s
    """, po_name)[0][0] or 0


    receipt_complete = received_qty >= total_qty
    invoice_complete = billed_amt >= total_amt


    # -------------------------------
    # STATE LOGIC
    # -------------------------------

    if receipt_complete and invoice_complete:

        new_state = "Completed"

    elif received_qty > 0 and not invoice_complete:

        new_state = "To Bill"

    elif billed_amt > 0 and not receipt_complete:

        new_state = "To Receive"

    else:

        new_state = "To Receive and Bill"


    if po.po_workflow_state != new_state:

        frappe.db.set_value(
            "Purchase Order",
            po_name,
            "po_workflow_state",
            new_state
        )
