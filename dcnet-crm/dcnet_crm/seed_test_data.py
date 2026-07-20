"""Seed DCNET CRM smoke-test data on a development site.

Run with:
    bench --site flow.local execute dcnet_crm.seed_test_data.run
"""

from __future__ import annotations

import json
import random

import frappe
from frappe.utils import add_days, cint, flt, today

from dcnet_crm import api as crm_api
from dcnet_crm.install import CRM_SALES_STAGES


PREFIX = "DCNET-CRM-TEST"
DEFAULT_COUNT = 10


def run(count: int = DEFAULT_COUNT) -> dict:
    """Create CRM test records and verify the main CRM APIs."""
    frappe.set_user("Administrator")
    count = cint(count) or DEFAULT_COUNT

    ensure_master_data()

    items = ensure_items(count)
    customers = ensure_customers(count)
    contacts = ensure_contacts(customers, count)
    leads = ensure_leads(count)
    opportunities = ensure_opportunities(customers, contacts, items, count)
    sync_opportunity_amounts(opportunities)
    quotations = ensure_quotations(customers, contacts, opportunities, items, count)
    sales_orders = ensure_sales_orders(customers, contacts, opportunities, items, count)
    service_accounts = ensure_service_accounts(customers, items, count)
    invoices, todos = ensure_sales_invoices_and_activities(sales_orders, count)
    care_cards = ensure_care_cards(customers, sales_orders, items, count)
    comments = ensure_comments(customers, contacts, opportunities, care_cards, count)

    verification = verify_crm_apis(
        leads=leads,
        customers=customers,
        contacts=contacts,
        opportunities=opportunities,
        quotations=quotations,
        sales_orders=sales_orders,
        service_accounts=service_accounts,
        todos=todos,
        care_cards=care_cards,
    )

    frappe.db.commit()
    return {
        "prefix": PREFIX,
        "target_per_group": count,
        "created_or_reused": {
            "Item": len(items),
            "Lead": len(leads),
            "Customer": len(customers),
            "Contact": len(contacts),
            "Opportunity": len(opportunities),
            "Quotation": len(quotations),
            "Sales Order": len(sales_orders),
            "Sales Invoice": len(invoices),
            "ToDo": len(todos),
            "DCNET Service Account": len(service_accounts),
            "CRM Care Card": len(care_cards),
            "Comment": len(comments),
        },
        "verification": verification,
    }


def run_existing_customers(count: int = DEFAULT_COUNT) -> dict:
    """Create CRM test records against existing customers only."""
    frappe.set_user("Administrator")
    count = cint(count) or DEFAULT_COUNT

    ensure_master_data()

    customers = ensure_existing_customers(count)
    items = ensure_items(count)
    contacts = ensure_contacts(customers, count, email_prefix="crm.existing.contact")
    leads = ensure_leads(count)
    opportunities = ensure_opportunities(customers, contacts, items, count)
    sync_opportunity_amounts(opportunities)
    quotations = ensure_quotations(customers, contacts, opportunities, items, count)
    sales_orders = ensure_sales_orders(customers, contacts, opportunities, items, count)
    service_accounts = ensure_service_accounts(customers, items, count)
    invoices, todos = ensure_sales_invoices_and_activities(sales_orders, count)
    care_cards = ensure_care_cards(customers, sales_orders, items, count)
    comments = ensure_comments(customers, contacts, opportunities, care_cards, count)

    verification = verify_existing_customer_seed(
        leads=leads,
        customers=customers,
        contacts=contacts,
        opportunities=opportunities,
        quotations=quotations,
        sales_orders=sales_orders,
        service_accounts=service_accounts,
        todos=todos,
        care_cards=care_cards,
    )

    frappe.db.commit()
    return {
        "prefix": PREFIX,
        "customer_source": "existing",
        "target_per_group": count,
        "existing_customers_used": customers,
        "created_or_reused": {
            "Item": len(items),
            "Lead": len(leads),
            "Customer": len(customers),
            "Contact": len(contacts),
            "Opportunity": len(opportunities),
            "Quotation": len(quotations),
            "Sales Order": len(sales_orders),
            "Sales Invoice": len(invoices),
            "ToDo": len(todos),
            "DCNET Service Account": len(service_accounts),
            "CRM Care Card": len(care_cards),
            "Comment": len(comments),
        },
        "verification": verification,
    }


def ensure_master_data() -> None:
    """Ensure minimal master data required by ERPNext selling documents."""
    _ensure_customer_group()
    _ensure_territory()
    _ensure_item_group()
    _ensure_selling_price_list()
    _ensure_uom()


def ensure_items(count: int) -> list[str]:
    """Create test service items."""
    item_group = _ensure_item_group()
    uom = _ensure_uom()
    names = []
    for idx in range(1, count + 1):
        item_code = f"{PREFIX}-ITEM-{idx:02d}"
        if not frappe.db.exists("Item", item_code):
            doc = frappe.new_doc("Item")
            doc.item_code = item_code
            doc.item_name = f"CRM Test Service {idx:02d}"
            doc.item_group = item_group
            doc.stock_uom = uom
            doc.is_stock_item = 0
            doc.is_sales_item = 1
            doc.is_purchase_item = 0
            doc.insert(ignore_permissions=True)
        names.append(item_code)
    return names


def ensure_existing_customers(count: int) -> list[str]:
    """Return random existing Company customers without creating Customers."""
    filters = {"customer_type": "Company"}
    if frappe.get_meta("Customer").has_field("disabled"):
        filters["disabled"] = 0

    names = frappe.get_all(
        "Customer",
        filters=filters,
        pluck="name",
        limit_page_length=0,
    )
    if len(names) < count:
        frappe.throw(
            f"Cần ít nhất {count} khách hàng công ty có sẵn, hiện chỉ có {len(names)}."
        )
    return random.SystemRandom().sample(names, count)


def ensure_customers(count: int) -> list[str]:
    """Create customers through the CRM create_customer API."""
    customer_group = _ensure_customer_group()
    territory = _ensure_territory()
    names = []
    for idx in range(1, count + 1):
        customer_name = f"{PREFIX} Customer {idx:02d}"
        existing = frappe.db.get_value("Customer", {"customer_name": customer_name}, "name")
        if existing:
            names.append(existing)
            continue

        result = crm_api.create_customer(
            customer=json.dumps(
                {
                    "customer_name": customer_name,
                    "customer_type": "Company",
                    "customer_group": customer_group,
                    "territory": territory,
                    "tax_id": f"0310001{idx:03d}",
                    "website": f"https://crm-test-{idx:02d}.example.com",
                    "customer_details": f"{PREFIX} generated customer {idx:02d}",
                }
            ),
            contact=json.dumps({}),
            billing_address=json.dumps(
                {
                    "address_title": customer_name,
                    "address_type": "Billing",
                    "address_line1": f"{idx:02d} Test Street",
                    "state": "Ho Chi Minh City",
                    "county": "Ward 1",
                    "country": "Vietnam",
                    "pincode": f"70{idx:04d}",
                    "phone": f"0289000{idx:04d}",
                }
            ),
            shipping_address=json.dumps(
                {
                    "address_title": f"{customer_name} Shipping",
                    "address_type": "Shipping",
                    "address_line1": f"{idx:02d} Shipping Street",
                    "state": "Ho Chi Minh City",
                    "county": "Ward 2",
                    "country": "Vietnam",
                    "pincode": f"71{idx:04d}",
                    "phone": f"0289100{idx:04d}",
                }
            ),
        )
        names.append(result["name"])
    return names


def ensure_contacts(customers: list[str], count: int, email_prefix: str = "crm.contact") -> list[str]:
    """Create one contact per customer through the CRM contact API."""
    names = []
    for idx in range(1, count + 1):
        email = f"{email_prefix}.{idx:02d}@example.com"
        existing = frappe.db.get_value("Contact", {"email_id": email}, "name")
        if existing:
            names.append(existing)
            continue

        result = crm_api.create_contact_standalone(
            json.dumps(
                {
                    "first_name": f"Contact {idx:02d}",
                    "last_name": "CRM Test",
                    "designation": "Test Buyer",
                    "department": "Sales",
                    "customer": customers[idx - 1],
                    "mobile_no": f"090100{idx:04d}",
                    "phone": f"0289200{idx:04d}",
                    "email_id": email,
                    "billing_address": {
                        "address_line1": f"{idx:02d} Contact Lane",
                        "state": "Ho Chi Minh City",
                        "county": "Ward 3",
                        "country": "Vietnam",
                        "pincode": f"72{idx:04d}",
                    },
                }
            )
        )
        names.append(result["name"])
    return names


def ensure_leads(count: int) -> list[str]:
    """Create leads through the CRM Lead API."""
    names = []
    for idx in range(1, count + 1):
        email = f"crm.lead.{idx:02d}@example.com"
        existing = frappe.db.get_value("Lead", {"email_id": email}, "name")
        if existing:
            cleanup_auto_lead_contacts(existing)
            names.append(existing)
            continue

        result = crm_api.save_lead(
            json.dumps(
                {
                    "first_name": f"Lead {idx:02d}",
                    "last_name": "CRM Test",
                    "company_name": f"{PREFIX} Lead Company {idx:02d}",
                    "email_id": email,
                    "mobile_no": f"091100{idx:04d}",
                    "phone": f"0289300{idx:04d}",
                    "status": "Lead",
                    "country": "Vietnam",
                    "state": "Ho Chi Minh City",
                    "city": "Ho Chi Minh City",
                    "address_line1": f"{idx:02d} Lead Street",
                    "notes": f"{PREFIX} generated lead {idx:02d}",
                    "custom_lead_type": "KH viễn thông",
                    "custom_is_shared": 1,
                }
            )
        )
        cleanup_auto_lead_contacts(result["name"])
        names.append(result["name"])
    return names


def cleanup_auto_lead_contacts(lead_name: str) -> list[str]:
    """Remove Contacts auto-created by ERPNext for a Lead."""
    contact_names = frappe.get_all(
        "Dynamic Link",
        filters={
            "parenttype": "Contact",
            "link_doctype": "Lead",
            "link_name": lead_name,
        },
        pluck="parent",
    )
    deleted = []
    for contact_name in contact_names:
        links = frappe.get_all(
            "Dynamic Link",
            filters={"parenttype": "Contact", "parent": contact_name},
            fields=["link_doctype", "link_name"],
        )
        if any(link.link_doctype != "Lead" or link.link_name != lead_name for link in links):
            continue
        frappe.delete_doc("Contact", contact_name, ignore_permissions=True, force=True)
        deleted.append(contact_name)
    return deleted


def cleanup_seed_lead_contacts() -> dict:
    """Delete the accidental test Contacts that were auto-created from seeded Leads."""
    frappe.set_user("Administrator")
    leads = frappe.get_all(
        "Lead",
        filters={"email_id": ["like", "crm.lead.%@example.com"]},
        pluck="name",
        limit_page_length=100,
    )
    deleted = []
    for lead_name in leads:
        deleted.extend(cleanup_auto_lead_contacts(lead_name))
    frappe.db.commit()
    return {"leads_checked": len(leads), "contacts_deleted": len(deleted), "deleted": deleted}


def ensure_opportunities(
    customers: list[str],
    contacts: list[str],
    items: list[str],
    count: int,
) -> list[str]:
    """Create opportunities through the CRM Opportunity API."""
    names = []
    company = _default_company()
    territory = _ensure_territory()
    uom = _ensure_uom()
    for idx in range(1, count + 1):
        title = f"{PREFIX} Opportunity {idx:02d}"
        existing = frappe.db.get_value("Opportunity", {"title": title}, "name")
        if existing:
            names.append(existing)
            continue

        result = crm_api.save_opportunity(
            json.dumps(
                {
                    "title": title,
                    "party_name": customers[idx - 1],
                    "contact_person": contacts[idx - 1],
                    "company": company,
                    "territory": territory,
                    "transaction_date": today(),
                    "expected_closing": add_days(today(), 15 + idx),
                    "sales_stage": CRM_SALES_STAGES[(idx - 1) % len(CRM_SALES_STAGES)],
                    "probability": min(90, 20 + idx * 5),
                    "notes": f"{PREFIX} generated opportunity {idx:02d}",
                    "custom_shipping_country": "Vietnam",
                    "custom_shipping_state": "Ho Chi Minh City",
                    "custom_shipping_county": "Ward 4",
                    "custom_shipping_address_line1": f"{idx:02d} Opportunity Site",
                    "custom_shipping_address": f"{idx:02d} Opportunity Site, Ward 4",
                    "custom_is_shared": 1,
                    "items": [
                        {
                            "item_code": items[idx - 1],
                            "item_name": f"CRM Test Service {idx:02d}",
                            "description": f"{PREFIX} opportunity item {idx:02d}",
                            "qty": 1 + (idx % 3),
                            "uom": uom,
                            "rate": 1000000 + idx * 100000,
                            "custom_installation_point_a_end": f"A-{idx:02d}",
                            "custom_installation_point_z_end": f"Z-{idx:02d}",
                        }
                    ],
                }
            )
        )
        names.append(result["name"])
    return names


def ensure_quotations(
    customers: list[str],
    contacts: list[str],
    opportunities: list[str],
    items: list[str],
    count: int,
) -> list[str]:
    """Create quotations through the CRM Quotation API."""
    names = []
    company = _default_company()
    currency = _company_currency(company)
    price_list = _ensure_selling_price_list()
    territory = _ensure_territory()
    uom = _ensure_uom()
    for idx in range(1, count + 1):
        title = f"{PREFIX} Quotation {idx:02d}"
        existing = frappe.db.get_value(
            "Quotation",
            {"opportunity": opportunities[idx - 1], "docstatus": ["<", 2]},
            "name",
        )
        if existing:
            names.append(existing)
            continue

        result = crm_api.create_quotation(
            {
                "customer": customers[idx - 1],
                "contact_person": contacts[idx - 1],
                "opportunity": opportunities[idx - 1],
                "company": company,
                "currency": currency,
                "selling_price_list": price_list,
                "territory": territory,
                "transaction_date": today(),
                "valid_till": add_days(today(), 30),
                "order_type": "Sales",
                "title": title,
                "note": f"{PREFIX} generated quotation {idx:02d}",
                "items": [
                    {
                        "item_code": items[idx - 1],
                        "item_name": f"CRM Test Service {idx:02d}",
                        "description": f"{PREFIX} quotation item {idx:02d}",
                        "qty": 1 + (idx % 3),
                        "uom": uom,
                        "price_list_rate": 1000000 + idx * 100000,
                        "rate": 1000000 + idx * 100000,
                        "discount_percentage": idx % 5,
                        "a_end": f"A-{idx:02d}",
                        "z_end": f"Z-{idx:02d}",
                    }
                ],
            }
        )
        names.append(result["name"])
    return names


def sync_opportunity_amounts(opportunities: list[str]) -> None:
    """Keep seeded Opportunity totals consistent with their item rows."""
    for name in opportunities:
        doc = frappe.get_doc("Opportunity", name)
        amount = sum(flt(row.amount) for row in doc.get("items", []))
        if flt(doc.opportunity_amount) != amount:
            doc.db_set("opportunity_amount", amount, update_modified=False)


def sync_seed_opportunity_amounts() -> dict:
    """Repair totals for the generated CRM smoke-test opportunities."""
    names = frappe.get_all(
        "Opportunity",
        filters={"title": ["like", f"{PREFIX}%"]},
        pluck="name",
        limit_page_length=0,
    )
    sync_opportunity_amounts(names)
    frappe.db.commit()
    return {"updated": len(names), "opportunities": names}


def run_read_only_smoke() -> dict:
    """Verify the installed CRM app using existing seed data without writes."""
    frappe.set_user("Administrator")

    lead = frappe.db.get_value("Lead", {"email_id": ["like", "crm.lead.%@example.com"]}, "name")
    contact = frappe.db.get_value("Contact", {"email_id": ["like", "crm.existing.contact.%"]}, "name")
    opportunity = frappe.db.get_value("Opportunity", {"title": ["like", f"{PREFIX}%"]}, "name")
    quotation = frappe.db.get_value(
        "Quotation", {"opportunity": opportunity, "docstatus": ["<", 2]}, "name"
    )
    sales_order = frappe.db.get_value(
        "Sales Order", {"custom_opportunity": opportunity, "docstatus": ["<", 2]}, "name"
    )
    care_card = frappe.db.get_value("CRM Care Card", {"description": ["like", f"{PREFIX}%"]}, "name")

    required = {
        "Lead": lead,
        "Contact": contact,
        "Opportunity": opportunity,
        "Quotation": quotation,
        "Sales Order": sales_order,
        "CRM Care Card": care_card,
    }
    missing = [doctype for doctype, name in required.items() if not name]
    if missing:
        frappe.throw(f"Thiếu dữ liệu smoke test: {', '.join(missing)}")

    opportunity_detail = crm_api.get_opportunity_detail(opportunity)
    return {
        "boot_resources": sorted(crm_api.get_boot()["resources"]),
        "lead": crm_api.get_lead_detail(lead)["document"]["name"],
        "contact": crm_api.get_contact_detail(contact)["name"],
        "opportunity": opportunity_detail["document"]["name"],
        "opportunity_items": len(opportunity_detail["items"]),
        "quotation_items": len(crm_api.get_quotation_items(quotation)),
        "sales_order": crm_api.get_so_detail(sales_order)["document"]["name"],
        "sales_order_items": len(crm_api.get_so_items(sales_order)),
        "care_card": crm_api.get_care_card_detail(care_card)["card"]["name"],
        "asset_route": "/assets/dcnet_crm/dist/crm.bundle.js",
    }


def ensure_sales_orders(
    customers: list[str],
    contacts: list[str],
    opportunities: list[str],
    items: list[str],
    count: int,
) -> list[str]:
    """Create sales orders through the CRM Sales Order API."""
    names = []
    company = _default_company()
    currency = _company_currency(company)
    price_list = _ensure_selling_price_list()
    territory = _ensure_territory()
    uom = _ensure_uom()
    for idx in range(1, count + 1):
        po_no = f"{PREFIX}-PO-{idx:02d}"
        existing = frappe.db.get_value("Sales Order", {"po_no": po_no}, "name")
        if existing:
            names.append(existing)
            continue

        result = crm_api.create_sales_order(
            {
                "customer": customers[idx - 1],
                "contact_person": contacts[idx - 1],
                "opportunity": opportunities[idx - 1],
                "company": company,
                "currency": currency,
                "selling_price_list": price_list,
                "territory": territory,
                "transaction_date": today(),
                "delivery_date": add_days(today(), 7 + idx),
                "order_type": "Sales",
                "po_no": po_no,
                "title": f"{PREFIX} Sales Order {idx:02d}",
                "note": f"{PREFIX} generated sales order {idx:02d}",
                "installation_zone": "Nam",
                "contract_duration": 12,
                "execution_status": "Chưa thực hiện",
                "items": [
                    {
                        "item_code": items[idx - 1],
                        "item_name": f"CRM Test Service {idx:02d}",
                        "description": f"{PREFIX} sales order item {idx:02d}",
                        "qty": 1 + (idx % 3),
                        "uom": uom,
                        "price_list_rate": 1000000 + idx * 100000,
                        "rate": 1000000 + idx * 100000,
                        "discount_percentage": idx % 5,
                        "a_end": f"A-{idx:02d}",
                        "z_end": f"Z-{idx:02d}",
                    }
                ],
            }
        )
        names.append(result["name"])
    return names


def ensure_service_accounts(customers: list[str], items: list[str], count: int) -> list[str]:
    """Ensure one service account per customer/item endpoint combo."""
    names = []
    for idx in range(1, count + 1):
        result = crm_api.get_or_create_service_account(
            customers[idx - 1],
            items[idx - 1],
            f"A-{idx:02d}",
            f"Z-{idx:02d}",
        )
        names.append(result.get("account_code") or result.get("name"))
    return names


def ensure_sales_invoices_and_activities(sales_orders: list[str], count: int) -> tuple[list[str], list[str]]:
    """Create request and activity tasks without bypassing ERPNext documents."""
    todos = []
    for idx, so_name in enumerate(sales_orders[:count], start=1):
        request_todo = frappe.db.get_value(
            "ToDo",
            {
                "reference_type": "Sales Order",
                "reference_name": so_name,
                "description": f"{PREFIX} Invoice request {idx:02d}",
            },
            "name",
        )
        if not request_todo:
            result = crm_api.create_so_action(
                so_name,
                "invoice",
                {
                    "title": f"{PREFIX} Invoice request {idx:02d}",
                    "task_type": "Đề nghị xuất hóa đơn",
                    "date": add_days(today(), idx),
                    "priority": "Medium",
                    "status": "Open",
                    "related_users": [],
                },
            )
            request_todo = result.get("todo_name")
        todos.append(request_todo)

        todo = frappe.db.get_value(
            "ToDo",
            {
                "reference_type": "Sales Order",
                "reference_name": so_name,
                "description": ["like", f"%{PREFIX} Activity {idx:02d}%"],
            },
            "name",
        )
        if not todo:
            result = crm_api.create_so_action(
                so_name,
                "activity",
                {
                    "title": f"{PREFIX} Activity {idx:02d}",
                    "task_type": "Chăm sóc khách hàng",
                    "date": add_days(today(), idx + 1),
                    "priority": "Medium",
                    "status": "Open",
                    "related_users": [],
                },
            )
            todo = result.get("todo_name")
        todos.append(todo)

    return [], [name for name in todos if name]


def ensure_care_cards(
    customers: list[str],
    sales_orders: list[str],
    items: list[str],
    count: int,
) -> list[str]:
    """Create CRM Care Cards through the CRM Care Card API."""
    names = []
    statuses = ["Chưa chăm sóc", "Đang chăm sóc", "Đã chăm sóc"]
    satisfaction = ["Rất hài lòng", "Hài lòng", "Bình thường", "Không hài lòng"]
    for idx in range(1, count + 1):
        existing = frappe.db.get_value("CRM Care Card", {"customer": customers[idx - 1]}, "name")
        if existing:
            names.append(existing)
            continue
        result = crm_api.save_care_card(
            data={
                "customer": customers[idx - 1],
                "province": "Ho Chi Minh City",
                "district": "District 1",
                "ward": "Ward 5",
                "country": "Vietnam",
                "address": f"{idx:02d} Care Street",
                "sales_order": sales_orders[idx - 1],
                "item": items[idx - 1],
                "item_type": "Service",
                "order_executor": "Administrator",
                "status": statuses[(idx - 1) % len(statuses)],
                "care_date": add_days(today(), idx),
                "satisfaction_level": satisfaction[(idx - 1) % len(satisfaction)],
                "dissatisfaction_reason": "Test reason" if idx % 4 == 0 else "",
                "description": f"{PREFIX} generated care card {idx:02d}",
                "department": "Sales",
                "layout": "Mẫu tiêu chuẩn",
                "related_users": json.dumps([{"name": "Administrator", "full_name": "Administrator"}]),
            }
        )
        names.append(result["name"])
    return names


def ensure_comments(
    customers: list[str],
    contacts: list[str],
    opportunities: list[str],
    care_cards: list[str],
    count: int,
) -> list[str]:
    """Create comments used by timeline/detail panels."""
    refs = []
    for idx in range(1, count + 1):
        refs.append(("Customer", customers[idx - 1], f"{PREFIX} Customer note {idx:02d}"))
        refs.append(("Contact", contacts[idx - 1], f"{PREFIX} Contact note {idx:02d}"))
        refs.append(("Opportunity", opportunities[idx - 1], f"{PREFIX} Opportunity note {idx:02d}"))
        refs.append(("CRM Care Card", care_cards[idx - 1], f"{PREFIX} Care note {idx:02d}"))

    names = []
    for doctype, docname, content in refs:
        existing = frappe.db.get_value(
            "Comment",
            {
                "reference_doctype": doctype,
                "reference_name": docname,
                "content": content,
            },
            "name",
        )
        if existing:
            names.append(existing)
            continue
        comment = frappe.get_doc(
            {
                "doctype": "Comment",
                "comment_type": "Comment",
                "reference_doctype": doctype,
                "reference_name": docname,
                "content": content,
            }
        )
        comment.insert(ignore_permissions=True)
        names.append(comment.name)
    return names


def verify_crm_apis(**records: list[str]) -> dict:
    """Call the main CRM APIs against seeded records."""
    checks = {}

    for resource in (
        "leads",
        "customers",
        "contacts",
        "opportunities",
        "quotations",
        "orders",
        "care_cards",
    ):
        result = crm_api.get_list(resource=resource, search=PREFIX, page=1, page_length=20)
        checks[f"list:{resource}"] = result["total"]
        if result["total"] < 1:
            frappe.throw(f"CRM list returned no rows for {resource}")

    checks["lead_detail"] = crm_api.get_lead_detail(records["leads"][0])["document"]["name"]
    checks["customer_workspace"] = crm_api.get_customer_workspace(records["customers"][0])["document"]["name"]
    checks["contact_detail"] = crm_api.get_contact_detail(records["contacts"][0])["name"]
    checks["opportunity_detail"] = crm_api.get_opportunity_detail(records["opportunities"][0])["document"]["name"]
    checks["quotation_items"] = len(crm_api.get_quotation_items(records["quotations"][0]))
    checks["sales_order_detail"] = crm_api.get_so_detail(records["sales_orders"][0])["document"]["name"]
    checks["sales_order_items"] = len(crm_api.get_so_items(records["sales_orders"][0]))
    checks["sales_order_stock_balance"] = len(crm_api.get_so_stock_balance(records["sales_orders"][0])["items"])

    activity_list = crm_api.get_activity_list(search=PREFIX, page=1, page_length=20)
    checks["activity_list"] = activity_list["total"]
    if records["todos"]:
        checks["activity_detail"] = crm_api.get_activity_detail(records["todos"][0])["name"]

    care_detail = crm_api.get_care_card_detail(records["care_cards"][0])
    checks["care_card_detail"] = care_detail["card"]["name"]
    checks["care_card_purchases"] = len(care_detail["purchases"])

    service_accounts = records["service_accounts"]
    checks["service_account_detail"] = crm_api.get_service_account_detail(service_accounts[0])["account_code"]
    checks["service_account_customer_suggestions"] = len(
        crm_api.get_customer_service_accounts(records["customers"][0])
    )

    return checks


def verify_existing_customer_seed(**records: list[str]) -> dict:
    """Verify CRM APIs for data generated around pre-existing customers."""
    checks = {}

    list_searches = {
        "leads": PREFIX,
        "contacts": "crm.existing.contact",
        "opportunities": PREFIX,
        "orders": PREFIX,
    }
    for resource, search in list_searches.items():
        result = crm_api.get_list(resource=resource, search=search, page=1, page_length=20)
        checks[f"list:{resource}"] = result["total"]
        if result["total"] < 1:
            frappe.throw(f"CRM list returned no rows for {resource}")

    quotation_list = crm_api.get_list(
        resource="quotations",
        search=records["customers"][0],
        page=1,
        page_length=20,
    )
    checks["list:quotations"] = quotation_list["total"]
    if quotation_list["total"] < 1:
        frappe.throw("CRM list returned no rows for quotations")

    care_card_list = crm_api.get_list(
        resource="care_cards",
        search=records["customers"][0],
        page=1,
        page_length=20,
    )
    checks["list:care_cards"] = care_card_list["total"]
    if care_card_list["total"] < 1:
        frappe.throw("CRM list returned no rows for care_cards")

    customer_list = crm_api.get_list(
        resource="customers",
        search=records["customers"][0],
        page=1,
        page_length=20,
    )
    checks["list:customers_existing"] = customer_list["total"]
    checks["existing_customers_used"] = len(records["customers"])

    checks["lead_detail"] = crm_api.get_lead_detail(records["leads"][0])["document"]["name"]
    checks["customer_workspace"] = crm_api.get_customer_workspace(records["customers"][0])["document"]["name"]
    checks["contact_detail"] = crm_api.get_contact_detail(records["contacts"][0])["name"]
    checks["opportunity_detail"] = crm_api.get_opportunity_detail(records["opportunities"][0])["document"]["name"]
    checks["quotation_items"] = len(crm_api.get_quotation_items(records["quotations"][0]))
    checks["sales_order_detail"] = crm_api.get_so_detail(records["sales_orders"][0])["document"]["name"]
    checks["sales_order_items"] = len(crm_api.get_so_items(records["sales_orders"][0]))
    checks["sales_order_stock_balance"] = len(crm_api.get_so_stock_balance(records["sales_orders"][0])["items"])

    activity_list = crm_api.get_activity_list(search=PREFIX, page=1, page_length=20)
    checks["activity_list"] = activity_list["total"]
    if records["todos"]:
        checks["activity_detail"] = crm_api.get_activity_detail(records["todos"][0])["name"]

    care_detail = crm_api.get_care_card_detail(records["care_cards"][0])
    checks["care_card_detail"] = care_detail["card"]["name"]
    checks["care_card_purchases"] = len(care_detail["purchases"])

    service_accounts = records["service_accounts"]
    checks["service_account_detail"] = crm_api.get_service_account_detail(service_accounts[0])["account_code"]
    checks["service_account_customer_suggestions"] = len(
        crm_api.get_customer_service_accounts(records["customers"][0])
    )

    return checks


def _default_company() -> str:
    company = frappe.defaults.get_user_default("Company") or frappe.db.get_value("Company", {}, "name")
    if not company:
        frappe.throw("No Company found. Complete ERPNext setup before seeding CRM data.")
    return company


def _company_currency(company: str) -> str:
    return frappe.db.get_value("Company", company, "default_currency") or "VND"


def _ensure_customer_group() -> str:
    name = f"{PREFIX} Customer Group"
    if not frappe.db.exists("Customer Group", name):
        parent = frappe.db.get_value("Customer Group", {"is_group": 1}, "name")
        doc = frappe.new_doc("Customer Group")
        doc.customer_group_name = name
        doc.parent_customer_group = parent
        doc.is_group = 0
        doc.insert(ignore_permissions=True)
    return name


def _ensure_territory() -> str:
    name = f"{PREFIX} Territory"
    if not frappe.db.exists("Territory", name):
        parent = frappe.db.get_value("Territory", {"is_group": 1}, "name")
        doc = frappe.new_doc("Territory")
        doc.territory_name = name
        doc.parent_territory = parent
        doc.is_group = 0
        doc.insert(ignore_permissions=True)
    return name


def _ensure_item_group() -> str:
    name = f"{PREFIX} Services"
    if not frappe.db.exists("Item Group", name):
        parent = frappe.db.get_value("Item Group", {"is_group": 1}, "name")
        doc = frappe.new_doc("Item Group")
        doc.item_group_name = name
        doc.parent_item_group = parent
        doc.is_group = 0
        doc.insert(ignore_permissions=True)
    return name


def _ensure_selling_price_list() -> str:
    existing = frappe.db.get_value("Price List", {"selling": 1, "enabled": 1}, "name")
    if existing:
        return existing
    name = f"{PREFIX} Selling"
    if not frappe.db.exists("Price List", name):
        doc = frappe.new_doc("Price List")
        doc.price_list_name = name
        doc.selling = 1
        doc.buying = 0
        doc.enabled = 1
        doc.currency = _company_currency(_default_company())
        doc.insert(ignore_permissions=True)
    return name


def _ensure_uom() -> str:
    for name in ("Nos", "Cái", "Unit"):
        if frappe.db.exists("UOM", name):
            return name
    doc = frappe.new_doc("UOM")
    doc.uom_name = "Unit"
    doc.insert(ignore_permissions=True)
    return "Unit"
