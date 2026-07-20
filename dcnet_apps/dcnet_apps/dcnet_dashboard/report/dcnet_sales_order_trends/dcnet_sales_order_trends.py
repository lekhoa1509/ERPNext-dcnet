# Copyright (c) 2026, DCNET Cloud and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta


def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)

    return columns, data, None, chart


# ---------------------
# COLUMNS
# ---------------------

def get_columns():
    return [
        {
            "label": "Period",
            "fieldname": "label",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Total Sales",
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 150
        }
    ]


# ---------------------
# DATE RANGE
# ---------------------

def get_date_range(filters):

    if filters.get("from_date") and filters.get("to_date"):
        return filters["from_date"], filters["to_date"]

    if filters.get("fiscal_year"):
        fy = frappe.get_doc("Fiscal Year", filters["fiscal_year"])
        return fy.year_start_date, fy.year_end_date

    return None, None


# ---------------------
# CONDITIONS
# ---------------------

def get_conditions(filters):

    conditions = ["so.docstatus = 1"]

    if filters.get("company"):
        conditions.append("so.company = %(company)s")

    from_date, to_date = get_date_range(filters)

    if from_date:
        filters["from_date"] = from_date
        conditions.append("so.transaction_date >= %(from_date)s")

    if to_date:
        filters["to_date"] = to_date
        conditions.append("so.transaction_date <= %(to_date)s")

    if filters.get("customer_group"):
        conditions.append("c.customer_group = %(customer_group)s")

    if not filters.get("include_closed_orders"):
        conditions.append("so.status != 'Closed'")

    return " AND ".join(conditions)


# ---------------------
# SQL LABEL
# ---------------------

def get_label_clause(period):

    if period == "Daily":
        return "DATE_FORMAT(so.transaction_date, '%%Y-%%m-%%d')"

    if period == "Weekly":
        return "DATE_FORMAT(so.transaction_date, '%%x-W%%v')"

    if period == "Monthly":
        return "DATE_FORMAT(so.transaction_date, '%%Y-%%m')"

    if period == "Quarterly":
        return "CONCAT(YEAR(so.transaction_date), '-Q', QUARTER(so.transaction_date))"
    
    if period == "Half-Yearly":
        return """
        CONCAT(
            YEAR(so.transaction_date),
            '-H',
            IF(MONTH(so.transaction_date) <= 6, 1, 2)
        )
        """

    if period == "Yearly":
        return "YEAR(so.transaction_date)"

    return "DATE_FORMAT(so.transaction_date, '%%Y-%%m')"


# ---------------------
# SQL GROUP BY
# ---------------------

def get_group_by_clause(period):

    if period == "Daily":
        return "DATE(so.transaction_date)"

    if period == "Weekly":
        return "YEAR(so.transaction_date), WEEK(so.transaction_date,1)"

    if period == "Monthly":
        return "YEAR(so.transaction_date), MONTH(so.transaction_date)"

    if period == "Quarterly":
        return "YEAR(so.transaction_date), QUARTER(so.transaction_date)"
    
    if period == "Half-Yearly":
        return "YEAR(so.transaction_date), IF(MONTH(so.transaction_date)<=6,1,2)"

    if period == "Yearly":
        return "YEAR(so.transaction_date)"

    return "YEAR(so.transaction_date), MONTH(so.transaction_date)"


# ---------------------
# RAW DATA QUERY
# ---------------------

def get_raw_data(filters):

    period = filters.get("period", "Monthly")

    label = get_label_clause(period)
    group_by = get_group_by_clause(period)
    conditions = get_conditions(filters)

    query = f"""
        SELECT
            {label} as label,
            COALESCE(SUM(so.base_grand_total),0) as total
        FROM `tabSales Order` so
        LEFT JOIN `tabCustomer` c
            ON c.name = so.customer
        WHERE {conditions}
        GROUP BY {group_by}
        ORDER BY MIN(so.transaction_date)
    """

    return frappe.db.sql(query, filters, as_dict=True)


# ---------------------
# GENERATE FULL PERIOD RANGE
# ---------------------

def generate_period_range(period):

    today = datetime.today()
    labels = []

    if period == "Daily":

        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            labels.append(d.strftime("%Y-%m-%d"))

    elif period == "Weekly":

        for i in range(7, -1, -1):
            d = today - timedelta(weeks=i)
            labels.append(d.strftime("%G-W%V"))

    elif period == "Monthly":

        year = today.year
        month = today.month

        for i in range(11, -1, -1):

            m = month - i
            y = year

            while m <= 0:
                m += 12
                y -= 1

            labels.append(f"{y}-{m:02d}")

    elif period == "Quarterly":

        year = today.year
        current_q = (today.month - 1) // 3 + 1

        for i in range(3, -1, -1):

            q = current_q - i
            y = year

            while q <= 0:
                q += 4
                y -= 1

            labels.append(f"{y}-Q{q}")
    
    elif period == "Half-Yearly":

        year = today.year

        for i in range(2, -1, -1):

            y = year - i

            labels.append(f"{y}-H1")
            labels.append(f"{y}-H2")

    elif period == "Yearly":

        for i in range(4, -1, -1):
            labels.append(str(today.year - i))

    return labels


# ---------------------
# MERGE RAW DATA + TIMELINE
# ---------------------

def get_data(filters):

    period = filters.get("period", "Monthly")

    raw_data = get_raw_data(filters)

    data_map = {}

    for d in raw_data:

        key = str(d.get("label"))

        try:
            val = float(d.get("total") or 0)
        except:
            val = 0

        data_map[key] = val

    labels = generate_period_range(period)

    result = []

    for label in labels:

        result.append({
            "label": label,
            "total": data_map.get(label, 0)
        })

    return result


# ---------------------
# CHART DATA
# ---------------------

def get_chart_data(data):

    labels = []
    values = []

    for d in data:
        labels.append(d["label"])
        values.append(float(d["total"]))

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Sales Order",
                    "values": values
                }
            ]
        },
        "type": "line",
        "colors": ["#7cd6fd"]
    }