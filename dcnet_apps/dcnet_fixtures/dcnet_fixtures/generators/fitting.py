# Copyright (c) 2026, DCNET and contributors
# For license information, please see license.txt

"""
Fitting Module Sample Data Generator

Generates realistic Fitting Session data for DCNET Golf business.
Includes measurements, services, and various workflow states.

Usage:
    # From bench console
    from dcnet_fixtures.dcnet_fixtures.generators.fitting import generate_fitting_sessions
    generate_fitting_sessions(count=50)
    frappe.db.commit()

    # Or use full generator
    from dcnet_fixtures.dcnet_fixtures.generators.fitting import generate_full_fitting_data
    generate_full_fitting_data(session_count=50, submit=True)
"""

import frappe
import random
from datetime import datetime, timedelta
from frappe.utils import nowdate, add_days, now_datetime


# Vietnamese names for realistic data
FIRST_NAMES = [
    "Minh", "Hoàng", "Phúc", "Đức", "Tuấn", "Hải", "Long", "Nam", "Dũng", "Hùng",
    "Thành", "Quang", "Khang", "Bảo", "Vinh", "Trung", "Kiên", "Hiếu", "Nhật", "Tùng",
    "Thảo", "Linh", "Trang", "Hương", "Mai", "Lan", "Ngọc", "Phương", "Hà", "Chi"
]

LAST_NAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Vũ", "Võ", "Phan", "Trương",
    "Bùi", "Đặng", "Đỗ", "Ngô", "Dương", "Lý", "Hồ", "Đinh", "Lưu", "Cao"
]

# Service types with realistic pricing (VND)
SERVICE_TYPES = [
    {"type": "Grip", "item_name": "Thay Grip Golf", "rate": 150000, "description": "Thay grip mới cho gậy golf"},
    {"type": "Shaft", "item_name": "Lắp Shaft mới", "rate": 800000, "description": "Lắp đặt shaft phù hợp"},
    {"type": "Custom Club", "item_name": "Custom Driver", "rate": 15000000, "description": "Đặt driver theo thông số"},
    {"type": "Custom Club", "item_name": "Custom Iron Set", "rate": 25000000, "description": "Đặt bộ iron theo thông số"},
    {"type": "Combo", "item_name": "Fitting + Driver", "rate": 16500000, "description": "Gói fitting và driver"},
    {"type": "Combo", "item_name": "Fitting + Iron Set", "rate": 26500000, "description": "Gói fitting và bộ iron"},
    {"type": "Other", "item_name": "Lie/Loft Adjustment", "rate": 200000, "description": "Điều chỉnh góc lie/loft"},
    {"type": "Other", "item_name": "Swing Analysis Premium", "rate": 500000, "description": "Phân tích swing chuyên sâu"},
]

# Status distribution (weights for random selection)
STATUS_WEIGHTS = {
    "New": 10,
    "Confirmed": 20,
    "In Progress": 10,
    "Completed": 30,
    "Has Order": 16,
    "Follow Up": 6,
    "No Show": 4,
    "Cancelled": 4,
}

# Source distribution
SOURCE_WEIGHTS = {
    "Website": 30,
    "Walk-in": 25,
    "Phone": 15,
    "Facebook": 12,
    "Zalo": 10,
    "Referral": 5,
    "Other": 3,
}

# Skill levels with swing speed ranges (must match DocType options)
SKILL_LEVELS = {
    "Nguoi moi": {"weight": 40, "club_head_speed": (70, 85), "ball_speed_factor": (1.30, 1.35)},
    "Nguoi da choi": {"weight": 50, "club_head_speed": (85, 100), "ball_speed_factor": (1.35, 1.42)},
    "Nguoi choi chuyen nghiep": {"weight": 10, "club_head_speed": (100, 115), "ball_speed_factor": (1.42, 1.45)},
}


def weighted_choice(choices_dict):
    """Select item based on weights"""
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return random.choices(items, weights=weights, k=1)[0]


def generate_vietnamese_name():
    """Generate a realistic Vietnamese name"""
    return f"{random.choice(LAST_NAMES)} {random.choice(FIRST_NAMES)}"


def generate_phone():
    """Generate Vietnamese mobile number"""
    prefixes = ["090", "091", "093", "094", "096", "097", "098", "032", "033", "034", "035", "036", "037", "038", "039"]
    return f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"


def generate_email(name):
    """Generate email from name"""
    clean_name = name.lower().replace(" ", ".").replace("đ", "d")
    # Simple transliteration for Vietnamese
    for viet, eng in [("ă", "a"), ("â", "a"), ("ê", "e"), ("ô", "o"), ("ơ", "o"), ("ư", "u"), ("à", "a"), ("á", "a"), ("ả", "a"), ("ã", "a"), ("ạ", "a")]:
        clean_name = clean_name.replace(viet, eng)
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    return f"{clean_name}@{random.choice(domains)}"


def get_company():
    """Get default company or first available"""
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        company = frappe.db.get_value("Company", {}, "name")
    return company


def add_measurements(session, skill_level):
    """Add realistic measurements based on skill level"""
    skill_config = SKILL_LEVELS.get(skill_level, SKILL_LEVELS["Nguoi da choi"])

    # Club head speed
    min_speed, max_speed = skill_config["club_head_speed"]
    club_head_speed = round(random.uniform(min_speed, max_speed), 1)

    # Ball speed (factor of club head speed)
    min_factor, max_factor = skill_config["ball_speed_factor"]
    ball_speed = round(club_head_speed * random.uniform(min_factor, max_factor), 1)

    # Height and weight
    height = round(random.uniform(155, 185), 0)
    weight = round(random.uniform(55, 90), 1)

    # Distances based on skill
    if skill_level == "Nguoi moi":
        iron_distance = random.randint(110, 130)
        driver_distance = random.randint(180, 210)
    elif skill_level == "Nguoi choi chuyen nghiep":
        iron_distance = random.randint(160, 190)
        driver_distance = random.randint(250, 290)
    else:
        iron_distance = random.randint(130, 160)
        driver_distance = random.randint(210, 250)

    # Ball flight
    ball_flights = ["Straight", "Draw", "Fade", "Slice", "Hook"]
    ball_flight = random.choices(ball_flights, weights=[30, 25, 20, 15, 10], k=1)[0]

    # Ball trajectory
    trajectories = ["Low", "Mid-Low", "Mid", "Mid-High", "High"]
    trajectory = random.choice(trajectories)

    session.append("measurements", {
        "height": height,
        "weight": weight,
        "skill_level": skill_level,
        "hand_size": random.choice(["S", "M", "L", "XL"]),
        "club_head_speed": club_head_speed,
        "ball_speed": ball_speed,
        "iron_distance": iron_distance,
        "driver_distance": driver_distance,
        "ball_flight": ball_flight,
        "ball_trajectory": trajectory,
        "swing_description": f"Swing {ball_flight.lower()}, trajectory {trajectory.lower()}",
        "club_condition": random.choice(["Tot", "Trung binh", "Can nang cap"]),
        "special_requirements": random.choice(["", "", "", "Can gay nhe hon", "Can shaft mem hon", "Tay cam to hon"]),
        "upgrade_recommendations": f"Nen upgrade {random.choice(['driver', 'iron', 'wedge', 'putter'])} de cai thien ket qua",
    })


def add_services(session, num_services=None):
    """Add random services to session"""
    if num_services is None:
        num_services = random.randint(1, 3)

    # Select random services
    selected_services = random.sample(SERVICE_TYPES, min(num_services, len(SERVICE_TYPES)))

    total = 0
    for svc in selected_services:
        qty = 1
        if svc["type"] == "Grip":
            qty = random.randint(1, 14)  # Full set of grips

        amount = svc["rate"] * qty
        total += amount

        session.append("services", {
            "service_type": svc["type"],
            "item_name": svc["item_name"],
            "description": svc["description"],
            "quantity": qty,
            "rate": svc["rate"],
            "amount": amount,
        })

    return total


def create_linked_sales_order(fitting_session):
    """
    Create a Sales Order linked to Fitting Session.

    This demonstrates the 2-way link between Fitting Session and Sales Order:
    - Sales Order has custom field 'fitting_session' pointing to Fitting Session
    - Fitting Session shows linked Sales Orders in Links sidebar
    """
    try:
        company = get_company()

        # Get customer from fitting session
        customer = None
        if fitting_session.party_type == "Customer" and fitting_session.party:
            customer = fitting_session.party
        else:
            # Get first available customer
            customer = frappe.db.get_value("Customer", {}, "name")

        if not customer:
            return None

        # Get default warehouse
        warehouse = frappe.db.get_value("Warehouse", {"company": company, "is_group": 0}, "name")

        # Create Sales Order with items from fitting services
        so = frappe.new_doc("Sales Order")
        so.customer = customer
        so.company = company
        so.delivery_date = frappe.utils.add_days(frappe.utils.nowdate(), 7)
        so.fitting_session = fitting_session.name  # Link to Fitting Session!

        # Add items from services
        for service in fitting_session.services:
            # Try to find matching item or use generic service item
            item_code = frappe.db.get_value("Item", {"item_name": ["like", f"%{service.service_type}%"]}, "name")
            if not item_code:
                item_code = frappe.db.get_value("Item", {"is_stock_item": 0}, "name")
            if not item_code:
                item_code = frappe.db.get_value("Item", {}, "name")

            if item_code:
                so.append("items", {
                    "item_code": item_code,
                    "qty": service.quantity or 1,
                    "rate": service.rate or 100000,
                    "warehouse": warehouse,
                    "delivery_date": so.delivery_date,
                    "description": f"Từ Fitting: {service.item_name or service.service_type}"
                })

        # If no items from services, add a default item
        if not so.items:
            default_item = frappe.db.get_value("Item", {}, "name")
            if default_item:
                so.append("items", {
                    "item_code": default_item,
                    "qty": 1,
                    "rate": 500000,
                    "warehouse": warehouse,
                    "delivery_date": so.delivery_date,
                    "description": f"Dịch vụ Fitting - {fitting_session.name}"
                })

        so.flags.ignore_permissions = True
        so.flags.ignore_mandatory = True
        so.insert(ignore_permissions=True)

        # Update Fitting Session with Sales Order reference
        frappe.db.set_value("Fitting Session", fitting_session.name, "sales_order", so.name, update_modified=False)

        return so.name

    except Exception as e:
        # Silently skip - Sales Order creation is optional
        return None


def generate_fitting_sessions(count=50, submit=False):
    """
    Generate sample Fitting Sessions with measurements and services.

    Args:
        count (int): Number of sessions to generate (default 50)
        submit (bool): Whether to submit completed sessions

    Returns:
        list: List of created session names
    """
    print(f"🎯 Generating {count} Fitting Sessions...")

    # Get existing customers and leads
    customers = frappe.get_all("Customer", pluck="name", limit=40)
    leads = frappe.get_all("Lead", pluck="name", limit=20)

    if not customers and not leads:
        print("⚠️  No customers or leads found. Please install master/crm fixtures first.")
        return []

    company = get_company()
    created_sessions = []

    # Date range: 3 months ago to 2 weeks ahead
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now() + timedelta(days=14)

    for i in range(count):
        # Randomly choose Lead or Customer (70% Customer, 30% Lead)
        if customers and (not leads or random.random() < 0.7):
            party_type = "Customer"
            party = random.choice(customers)
            party_data = frappe.db.get_value("Customer", party, ["customer_name", "mobile_no", "email_id"], as_dict=True)
            customer_name = party_data.customer_name if party_data else generate_vietnamese_name()
            phone = party_data.mobile_no if party_data else generate_phone()
            email = party_data.email_id if party_data else generate_email(customer_name)
        else:
            party_type = "Lead"
            party = random.choice(leads) if leads else None
            if party:
                party_data = frappe.db.get_value("Lead", party, ["lead_name", "mobile_no", "email_id"], as_dict=True)
                customer_name = party_data.lead_name if party_data else generate_vietnamese_name()
                phone = party_data.mobile_no if party_data else generate_phone()
                email = party_data.email_id if party_data else generate_email(customer_name)
            else:
                customer_name = generate_vietnamese_name()
                phone = generate_phone()
                email = generate_email(customer_name)

        # Random datetime within range
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        # Round to hour
        scheduled_datetime = random_date.replace(minute=0, second=0, microsecond=0)

        # Select status and source
        status = weighted_choice(STATUS_WEIGHTS)
        source = weighted_choice(SOURCE_WEIGHTS)

        # Skill level for measurements
        skill_level = weighted_choice({k: v["weight"] for k, v in SKILL_LEVELS.items()})

        # Create session
        session = frappe.new_doc("Fitting Session")
        session.party_type = party_type
        session.party = party
        session.customer_name = customer_name
        session.phone = phone
        session.email = email
        session.scheduled_datetime = scheduled_datetime
        session.status = status
        session.source = source
        session.company = company
        session.notes = f"Session #{i+1} - {skill_level}"

        # 80% have measurements
        if random.random() < 0.8:
            add_measurements(session, skill_level)

        # 60% have services
        total_amount = 0
        if random.random() < 0.6:
            total_amount = add_services(session)

        session.total_amount = total_amount

        try:
            # Save desired status and create with "New" first
            desired_status = session.status
            session.status = "New"

            # Bypass workflow validation during import
            session.flags.ignore_permissions = True
            session.flags.ignore_links = True
            session.insert(ignore_permissions=True)

            # Update to desired status directly in DB (bypass workflow)
            if desired_status != "New":
                frappe.db.set_value("Fitting Session", session.name, "status", desired_status, update_modified=False)

            created_sessions.append(session.name)

            # Create linked Sales Order for "Has Order" status
            if desired_status == "Has Order" and session.services:
                create_linked_sales_order(session)

        except Exception as e:
            print(f"⚠️  Error creating session {i+1}: {str(e)}")
            continue

        # Progress indicator
        if (i + 1) % 10 == 0:
            print(f"   Created {i + 1}/{count} sessions...")

    frappe.db.commit()
    print(f"✅ Created {len(created_sessions)} Fitting Sessions")

    return created_sessions


def generate_full_fitting_data(session_count=50, submit=False):
    """
    Generate full fitting data with summary.

    Args:
        session_count (int): Number of sessions to create
        submit (bool): Whether to submit completed sessions

    Returns:
        dict: Summary of created data
    """
    print("\n" + "="*60)
    print("🏌️ DCNET Fitting Module - Sample Data Generator")
    print("="*60 + "\n")

    sessions = generate_fitting_sessions(count=session_count, submit=submit)

    # Get summary
    summary = {
        "total_sessions": len(sessions),
        "by_status": {},
        "by_party_type": {},
        "with_measurements": 0,
        "with_services": 0,
        "with_sales_order": 0,
        "total_revenue": 0,
    }

    for session_name in sessions:
        session = frappe.get_doc("Fitting Session", session_name)

        # Count by status
        summary["by_status"][session.status] = summary["by_status"].get(session.status, 0) + 1

        # Count by party type
        summary["by_party_type"][session.party_type] = summary["by_party_type"].get(session.party_type, 0) + 1

        # Count with measurements/services
        if session.measurements:
            summary["with_measurements"] += 1
        if session.services:
            summary["with_services"] += 1
            summary["total_revenue"] += session.total_amount or 0

    # Count Sales Orders linked to Fitting Sessions
    linked_so_count = frappe.db.count("Sales Order", {"fitting_session": ["is", "set"]})
    summary["with_sales_order"] = linked_so_count

    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    print(f"Total Sessions: {summary['total_sessions']}")
    print(f"With Measurements: {summary['with_measurements']}")
    print(f"With Services: {summary['with_services']}")
    print(f"With Sales Order: {summary['with_sales_order']} (linked)")
    print(f"Total Revenue: {summary['total_revenue']:,.0f} VND")
    print("\nBy Status:")
    for status, count in summary["by_status"].items():
        print(f"  - {status}: {count}")
    print("\nBy Party Type:")
    for party_type, count in summary["by_party_type"].items():
        print(f"  - {party_type}: {count}")
    print("="*60 + "\n")

    return summary


def clear_fitting_data():
    """Clear all Fitting Session data"""
    print("🗑️  Clearing Fitting Session data...")

    # Delete all Fitting Sessions
    frappe.db.sql("DELETE FROM `tabFitting Measurement`")
    frappe.db.sql("DELETE FROM `tabFitting Service`")
    frappe.db.sql("DELETE FROM `tabFitting Session`")

    frappe.db.commit()
    print("✅ Cleared all Fitting data")
