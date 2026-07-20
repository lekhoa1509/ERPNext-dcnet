import frappe
from frappe import _

# ============================================
# EXECUTE
# ============================================
def execute(filters=None):

    columns = get_columns()
    data = get_data(filters)

    chart = get_price_chart(filters)
    summary = get_summary(filters)

    return columns, data, None, chart, summary


# ============================================
# COLUMNS
# ============================================
def get_columns():

    return [

        {"label": _("Mã Sản Phẩm"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 140},
        {"label": _("Tên Sản Phẩm"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": _("Nhóm Sản Phẩm"), "fieldname": "item_group", "fieldtype": "Data", "width": 160},
        {"label": _("Mô Tả"), "fieldname": "description", "fieldtype": "Data", "width": 80},

        {"label": _("Số Lượng"), "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": _("ĐVT"), "fieldname": "uom", "fieldtype": "Data", "width": 90},

        {"label": _("Đơn Giá"), "fieldname": "rate", "fieldtype": "Currency", "width": 160},
        {"label": _("Giá Cao Nhất"), "fieldname": "max_price", "fieldtype": "Currency", "width": 160},
        {"label": _("Giá Thấp Nhất"), "fieldname": "min_price", "fieldtype": "Currency", "width": 160},
        {"label": _("Giá Trung Bình"), "fieldname": "avg_price", "fieldtype": "Currency", "width": 160},
        {"label": _("Số Tiền"), "fieldname": "amount", "fieldtype": "Currency", "width": 160},

        {"label": _("Đơn Mua Hàng"), "fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order", "width": 180},
        {"label": _("Ngày Giao"), "fieldname": "schedule_date", "fieldtype": "Date", "width": 130},

        {"label": _("Nhà Cung Cấp"), "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 150},
        {"label": _("Tên NCC"), "fieldname": "supplier_name", "fieldtype": "Data", "width": 200},
        {"label": _("Nhóm NCC"), "fieldname": "supplier_group", "fieldtype": "Data", "width": 150},
    ]


# ============================================
# CONDITIONS
# ============================================
def get_conditions(filters):

    conditions = " WHERE po.docstatus = 1 "

    if filters.get("company"):
        conditions += " AND po.company = %(company)s "

    if filters.get("from_date"):
        conditions += " AND po.transaction_date >= %(from_date)s "

    if filters.get("to_date"):
        conditions += " AND po.transaction_date <= %(to_date)s "

    if filters.get("item_group"):
        conditions += " AND item.item_group = %(item_group)s "

    if filters.get("item"):
        conditions += " AND poi.item_code = %(item)s "

    if filters.get("supplier"):
        conditions += " AND po.supplier = %(supplier)s "

    return conditions


# ============================================
# TABLE DATA
# ============================================
def get_data(filters):

    conditions = get_conditions(filters)

    query = f"""
        SELECT

            poi.item_code,
            poi.item_name,
            item.item_group,
            poi.description,

            poi.qty,
            poi.uom,
            poi.rate,

            MAX(poi.rate) OVER(PARTITION BY poi.item_code) AS max_price,
            MIN(poi.rate) OVER(PARTITION BY poi.item_code) AS min_price,
            AVG(poi.rate) OVER(PARTITION BY poi.item_code) AS avg_price,

            poi.amount,

            po.name AS purchase_order,
            po.schedule_date,
            po.supplier,

            sup.supplier_name,
            sup.supplier_group

        FROM `tabPurchase Order Item` poi

        INNER JOIN `tabPurchase Order` po
            ON poi.parent = po.name

        LEFT JOIN `tabItem` item
            ON item.name = poi.item_code

        LEFT JOIN `tabSupplier` sup
            ON sup.name = po.supplier

        {conditions}

        ORDER BY poi.item_name ASC, po.transaction_date DESC
    """

    return frappe.db.sql(query, filters, as_dict=True)


# ============================================
# CHART 1
# PRICE COMPARISON
# ============================================
def get_price_chart(filters):

    conditions = get_conditions(filters)

    query = f"""
        SELECT

            poi.item_name,

            MAX(poi.rate) AS max_price,
            MIN(poi.rate) AS min_price,
            AVG(poi.rate) AS avg_price

        FROM `tabPurchase Order Item` poi

        INNER JOIN `tabPurchase Order` po
            ON poi.parent = po.name

        LEFT JOIN `tabItem` item
            ON item.name = poi.item_code

        {conditions}

        GROUP BY poi.item_name
        ORDER BY poi.item_name ASC
    """

    result = frappe.db.sql(query, filters, as_dict=True)

    labels = [r.item_name for r in result]
    max_values = [r.max_price for r in result]
    min_values = [r.min_price for r in result]
    avg_values = [r.avg_price for r in result]

    return {

        "data": {

            "labels": labels,

            "datasets": [

                {"name": "Giá Cao Nhất", "values": max_values},
                {"name": "Giá Thấp Nhất", "values": min_values},
                {"name": "Giá Trung Bình", "values": avg_values},
            ],
        },

        "type": "bar",

        "colors": [
            "#ff6b6b",
            "#4dabf7",
            "#ffd43b"
        ],
    }


# ============================================
# SUMMARY DASHBOARD
# ============================================
def get_summary(filters):

    conditions = get_conditions(filters)

    query = f"""
        SELECT

            SUM(poi.amount) AS total_purchase,
            SUM(poi.qty) AS total_qty

        FROM `tabPurchase Order Item` poi

        INNER JOIN `tabPurchase Order` po
            ON poi.parent = po.name

        {conditions}
    """

    r = frappe.db.sql(query, filters, as_dict=True)[0]

    return [

        {
            "label": "Tổng Giá Trị Mua Hàng",
            "value": r.total_purchase,
            "datatype": "Currency",
        },

        {
            "label": "Tổng Số lượng",
            "value": r.total_qty,
            "datatype": "Float",
        }
    ]