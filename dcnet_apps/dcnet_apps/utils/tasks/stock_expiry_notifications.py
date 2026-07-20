import frappe
from frappe import _
from frappe.utils import flt, cint, getdate, add_days, today
from dcnet_apps.utils.notification_helper import (
    get_report_subscribers,
    send_alert_notification,
)
from frappe.utils import escape_html

# bench execute dcnet_apps.utils.tasks.stock_expiry_notifications.send_low_stock_summary_notification
def send_low_stock_summary_notification():
    """
    Task: Scan all items where actual_qty <= safety_stock and notify Admin.
    Optimized to run in a single query where possible.
    """
    try:
        item = frappe.qb.DocType("Item")
        bin = frappe.qb.DocType("Bin")

        # Join Item and Bin to find items across all warehouses that are low on stock
        low_stock_items = (
            frappe.qb.from_(item)
            .inner_join(bin).on(item.item_code == bin.item_code)
            .select(
                item.item_code,
                item.item_name,
                bin.warehouse,
                bin.actual_qty,
                item.safety_stock,
                item.stock_uom
            )
            .where(
                (item.disabled == 0)
                & (item.safety_stock > 0)
                & (bin.actual_qty <= item.safety_stock)
            )
            .run(as_dict=True)
        )

        if not low_stock_items:
            return

        count = len(low_stock_items)
        subject = _("Today, there are {0} items with low stock").format(count)
        
        rows = ""
        for d in low_stock_items:
            rows += f"""
            <tr>
                <td>{escape_html(d.item_code)}</td>
                <td>{escape_html(d.item_name)}</td>
                <td>{escape_html(d.warehouse)}</td>
                <td style="color: red; font-weight: bold;">{flt(d.actual_qty)}</td>
                <td>{flt(d.safety_stock)}</td>
                <td>{escape_html(d.stock_uom)}</td>
            </tr>"""

        message = f"""
        <p>{_("The following {0} items are currently at or below their safety stock levels").format(count)}:</p>
        <table class="table table-bordered" style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f8f9fa;">
                    <th>{_("Item Code")}</th>
                    <th>{_("Item Name")}</th>
                    <th>{_("Warehouse")}</th>
                    <th>{_("Actual Qty")}</th>
                    <th>{_("Safety Stock")}</th>
                    <th>{_("UOM")}</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        <p style="margin-top: 10px;">{_("Please review and create Material Requests as needed.")}</p>
        """

        # Link to the new 'Low Stock Alert' report
        report_link = "/app/query-report/Low Stock Alert"

        # Filter recipients based on Report roles
        recipients = get_report_subscribers("Low Stock Alert")
        if not recipients:
            recipients = ["Administrator"] # Standard Frappe fallback (username)

        send_alert_notification(
            recipients=recipients,
            subject=subject,
            message=message,
            link=report_link
        )
        frappe.db.commit() # CRITICAL for bench execute to save to database
    except Exception:
        frappe.log_error(frappe.get_traceback(), _("Low Stock Summary Notification Error"))

# bench execute dcnet_apps.utils.tasks.stock_expiry_notifications.send_item_expiry_summary_notification
def send_item_expiry_summary_notification():
    """
    Task: Scan all batches expiring within X days and notify Admin.
    Logic: Today <= Expiry Date <= (Today + X Days)
    """
    try:
        expiry_threshold_days = 7
        limit_date = add_days(today(), expiry_threshold_days)
        
        batch = frappe.qb.DocType("Batch")
        
        expiring_batches = (
            frappe.qb.from_(batch)
            .select(
                batch.name,
                batch.item,
                batch.item_name,
                batch.expiry_date,
                batch.batch_qty,
                batch.stock_uom
            )
            .where(
                (batch.disabled == 0)
                & (batch.batch_qty > 0)
                & (batch.expiry_date <= limit_date)
                & (batch.expiry_date >= today())
            )
            .orderby(batch.expiry_date)
            .run(as_dict=True)
        )

        if not expiring_batches:
            return

        count = len(expiring_batches)
        subject = _("{0} Items Near Expiry Warning ({1} Days)").format(count, expiry_threshold_days)
        
        rows = ""
        for d in expiring_batches:
            days_left = (getdate(d.expiry_date) - getdate(today())).days
            rows += f"""
            <tr>
                <td>{escape_html(d.item)}</td>
                <td>{escape_html(d.item_name)}</td>
                <td>{escape_html(d.name)}</td>
                <td>{d.expiry_date}</td>
                <td style="font-weight: bold;">{days_left}</td>
                <td>{flt(d.batch_qty)} {escape_html(d.stock_uom)}</td>
            </tr>"""

        message = f"""
        <p>{_("The following {0} batches are expiring within the next {1} days").format(count, expiry_threshold_days)}:</p>
        <table class="table table-bordered" style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f8f9fa;">
                    <th>{_("Item")}</th>
                    <th>{_("Item Name")}</th>
                    <th>{_("Batch")}</th>
                    <th>{_("Expiry Date")}</th>
                    <th>{_("Days Left")}</th>
                    <th>{_("Qty")}</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        <p style="margin-top: 10px;">{_("Please consider prioritizing these items or applying discounts.")}</p>
        """

        # Link to the custom report with the threshold parameter
        report_link = f"/app/query-report/Batch Near Expiry Status?near_expiry_days={expiry_threshold_days}"

        # Filter recipients based on Report roles
        recipients = get_report_subscribers("Batch Near Expiry Status")
        if not recipients:
            recipients = ["Administrator"]

        send_alert_notification(
            recipients=recipients,
            subject=subject,
            message=message,
            link=report_link
        )
        frappe.db.commit() # CRITICAL for bench execute to save to database
    except Exception:
        frappe.log_error(frappe.get_traceback(), _("Item Expiry Summary Notification Error"))
