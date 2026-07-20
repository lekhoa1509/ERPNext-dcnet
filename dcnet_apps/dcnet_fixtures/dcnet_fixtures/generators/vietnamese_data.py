"""
Vietnamese Data Generator for DCNET Fixtures

Generates realistic Vietnamese data with proper diacritics for:
- Leads
- Opportunities
- Customers (B2C and B2B)
- Suppliers
- Sales Orders
- Purchase Orders
- Fitting Sessions

Usage in bench console:
    from dcnet_fixtures.generators.vietnamese_data import generate_all_data
    generate_all_data()
    frappe.db.commit()
"""

import frappe
from frappe.utils import getdate, add_days, flt, nowdate
from random import randint, choice, sample, random, shuffle
from datetime import datetime, timedelta


# =============================================================================
# VIETNAMESE DATA - Names with diacritics
# =============================================================================

# Common Vietnamese family names (họ)
FAMILY_NAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ",
    "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đoàn", "Trương",
    "Đinh", "Lương", "Tạ", "Mai", "Cao", "Tô", "Lâm", "Châu", "Hà",
    "Thái", "Quách", "Tăng", "Diệp", "Triệu", "La", "Từ", "Kiều"
]

# Common Vietnamese middle names (tên đệm)
MIDDLE_NAMES = [
    "Văn", "Thị", "Hữu", "Đức", "Minh", "Ngọc", "Quốc", "Thanh", "Hoàng",
    "Thành", "Xuân", "Thu", "Hồng", "Bảo", "Kim", "Quang", "Anh", "Phương",
    "Tuấn", "Trung", "Công", "Tiến", "Đình", "Như", "Mỹ", "Hải", "Việt"
]

# Common Vietnamese given names (tên) - Male
MALE_NAMES = [
    "An", "Bình", "Cường", "Dũng", "Đạt", "Hùng", "Khoa", "Long", "Minh",
    "Nam", "Phong", "Quân", "Sơn", "Tâm", "Thắng", "Trung", "Tùng", "Vinh",
    "Hải", "Hoàng", "Kiên", "Lâm", "Nghĩa", "Phúc", "Quang", "Tài", "Thành",
    "Tuấn", "Việt", "Bách", "Đông", "Hiếu", "Khang", "Linh", "Nhật", "Phát",
    "Sang", "Thiện", "Toàn", "Trí", "Vũ", "Duy", "Hậu", "Khánh", "Luân"
]

# Common Vietnamese given names (tên) - Female
FEMALE_NAMES = [
    "Anh", "Bích", "Chi", "Diệu", "Dung", "Hà", "Hạnh", "Hiền", "Hoa",
    "Hương", "Lan", "Linh", "Loan", "Mai", "My", "Nga", "Ngân", "Ngọc",
    "Nhung", "Oanh", "Phương", "Quyên", "Thảo", "Thu", "Thủy", "Trang",
    "Trinh", "Tuyết", "Vân", "Yến", "Giang", "Hằng", "Huệ", "Kiều", "Ly",
    "Nhi", "Phượng", "Quỳnh", "Tâm", "Thanh", "Thúy", "Trâm", "Uyên", "Xuân"
]

# Vietnamese phone prefixes (mobile)
PHONE_PREFIXES = [
    "090", "091", "092", "093", "094", "096", "097", "098", "099",  # Viettel, Vinaphone, Mobifone
    "086", "083", "084", "085", "081", "082",  # Newer prefixes
    "070", "076", "077", "078", "079",  # Mobifone
    "032", "033", "034", "035", "036", "037", "038", "039"  # Viettel
]

# Vietnamese cities/provinces
CITIES = [
    "Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
    "Biên Hòa", "Nha Trang", "Huế", "Buôn Ma Thuột", "Quy Nhơn",
    "Vũng Tàu", "Thái Nguyên", "Nam Định", "Vinh", "Hạ Long",
    "Pleiku", "Phan Thiết", "Long Xuyên", "Mỹ Tho", "Bắc Ninh",
    "Thủ Dầu Một", "Biên Hòa", "Đồng Nai", "Bình Dương", "Long An"
]

# Districts in major cities
DISTRICTS = {
    "Hà Nội": ["Ba Đình", "Hoàn Kiếm", "Hai Bà Trưng", "Đống Đa", "Tây Hồ",
               "Cầu Giấy", "Thanh Xuân", "Hoàng Mai", "Long Biên", "Nam Từ Liêm"],
    "TP. Hồ Chí Minh": ["Quận 1", "Quận 3", "Quận 5", "Quận 7", "Quận 10",
                        "Bình Thạnh", "Phú Nhuận", "Tân Bình", "Gò Vấp", "Thủ Đức"],
    "Đà Nẵng": ["Hải Châu", "Thanh Khê", "Sơn Trà", "Ngũ Hành Sơn", "Liên Chiểu"]
}

# Golf courses in Vietnam
GOLF_COURSES = [
    "Sân Golf Long Thành", "Sân Golf Tân Sơn Nhất", "Sân Golf Thủ Đức",
    "Sân Golf Đồng Nai", "Sân Golf Vũng Tàu Paradise", "Sân Golf Đà Lạt Palace",
    "Sân Golf Kings Island", "Sân Golf Sky Lake", "Sân Golf Tam Đảo",
    "Sân Golf Vinpearl Hải Phòng", "Sân Golf Vinpearl Nha Trang",
    "Sân Golf BRG Legend Hill", "Sân Golf BRG Ruby Tree",
    "Sân Golf FLC Sầm Sơn", "Sân Golf FLC Hạ Long"
]

# Golf-related company names
GOLF_COMPANIES = [
    "Golf Shop", "Pro Shop", "Golf Center", "Golf Academy", "Golf Store",
    "Golf World", "Golf House", "Golf Paradise", "Golf Plus", "Golf Pro"
]

# Business types for B2B customers
B2B_TYPES = [
    "TNHH", "Cổ phần", "Tư nhân", "Liên doanh"
]

# Lead sources
LEAD_SOURCES = [
    "Website", "Facebook", "Zalo", "Phone", "Walk In", "Referral",
    "Google Ads", "TikTok", "Instagram", "Exhibition", "Partner"
]

# Lead statuses with weights (ERPNext standard values)
LEAD_STATUSES = [
    ("Lead", 15),
    ("Open", 30),
    ("Replied", 20),
    ("Interested", 20),
    ("Converted", 8),
    ("Do Not Contact", 4),
    ("Lost Quotation", 3)
]

# Opportunity stages with weights (ERPNext standard values)
OPPORTUNITY_STAGES = [
    ("Prospecting", 15),
    ("Qualification", 15),
    ("Needs Analysis", 20),
    ("Value Proposition", 10),
    ("Identifying Decision Makers", 10),
    ("Proposal/Price Quote", 15),
    ("Negotiation/Review", 15)
]

# Golf product interests (for notes)
GOLF_INTERESTS = [
    "Driver TaylorMade mới nhất",
    "Iron Set Callaway Paradym",
    "Putter Scotty Cameron",
    "Full set cho người mới",
    "Fitting service",
    "Coaching package",
    "Găng tay và phụ kiện",
    "Giày golf FootJoy",
    "Túi golf cao cấp",
    "Rangefinder Bushnell",
    "Trade-in gậy cũ",
    "Bóng golf Titleist Pro V1",
    "Wedge Vokey SM9",
    "Hybrid Ping G430",
    "Fairway wood Cobra"
]

# Supplier types (ERPNext standard values)
SUPPLIER_TYPES = [
    "Company",
    "Individual",
    "Partnership"
]

# Golf brands
GOLF_BRANDS = [
    "TaylorMade", "Callaway", "Titleist", "Ping", "Cobra",
    "Mizuno", "Srixon", "Cleveland", "Bridgestone", "Honma"
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_vietnamese_name(gender="male"):
    """Generate a random Vietnamese full name with diacritics"""
    family = choice(FAMILY_NAMES)
    middle = choice(MIDDLE_NAMES)

    if gender == "female":
        given = choice(FEMALE_NAMES)
        # Female often use "Thị" as middle name
        if random() < 0.4:
            middle = "Thị"
    else:
        given = choice(MALE_NAMES)
        # Male often use "Văn" as middle name
        if random() < 0.3:
            middle = "Văn"

    return {
        "first_name": family,
        "middle_name": middle,
        "last_name": given,
        "full_name": f"{family} {middle} {given}"
    }


def generate_phone():
    """Generate Vietnamese mobile phone number"""
    prefix = choice(PHONE_PREFIXES)
    suffix = "".join([str(randint(0, 9)) for _ in range(7)])
    return f"{prefix}{suffix}"


def generate_email(name):
    """Generate email from name"""
    # Remove diacritics for email
    import unicodedata

    # Vietnamese character replacements (đ -> d, Đ -> D)
    viet_map = {
        'đ': 'd', 'Đ': 'D',
        'ă': 'a', 'â': 'a', 'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'ê': 'e', 'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ô': 'o', 'ơ': 'o', 'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ư': 'u', 'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
    }

    # Replace Vietnamese special chars first
    ascii_name = name.lower()
    for viet_char, ascii_char in viet_map.items():
        ascii_name = ascii_name.replace(viet_char, ascii_char)

    # Then normalize and remove any remaining diacritics
    normalized = unicodedata.normalize('NFD', ascii_name)
    ascii_name = ''.join(c for c in normalized if not unicodedata.combining(c))
    ascii_name = ascii_name.replace(" ", "")

    # Only keep alphanumeric
    ascii_name = ''.join(c for c in ascii_name if c.isalnum())

    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    suffix = randint(1, 999) if random() < 0.5 else ""

    return f"{ascii_name}{suffix}@{choice(domains)}"


def generate_address():
    """Generate Vietnamese address"""
    city = choice(CITIES)

    # Get district if available
    if city in DISTRICTS:
        district = choice(DISTRICTS[city])
    else:
        district = f"Quận {randint(1, 12)}"

    street_num = randint(1, 500)
    street_names = [
        "Nguyễn Huệ", "Lê Lợi", "Trần Hưng Đạo", "Hai Bà Trưng",
        "Lý Thường Kiệt", "Điện Biên Phủ", "Võ Văn Tần", "Nguyễn Trãi",
        "Pasteur", "Nam Kỳ Khởi Nghĩa", "Cách Mạng Tháng 8"
    ]

    return {
        "address": f"{street_num} {choice(street_names)}",
        "district": district,
        "city": city
    }


def weighted_choice(choices_with_weights):
    """Choose from list of (item, weight) tuples"""
    total = sum(w for _, w in choices_with_weights)
    r = random() * total
    cumulative = 0
    for item, weight in choices_with_weights:
        cumulative += weight
        if r <= cumulative:
            return item
    return choices_with_weights[-1][0]


def get_company():
    """Get default company"""
    return frappe.db.get_single_value("Global Defaults", "default_company") or \
           frappe.db.get_value("Company", {}, "name")


def get_random_date(start_date, end_date):
    """Get random date between start and end"""
    if isinstance(start_date, str):
        start_date = getdate(start_date)
    if isinstance(end_date, str):
        end_date = getdate(end_date)

    delta = (end_date - start_date).days
    random_days = randint(0, max(0, delta))
    return add_days(start_date, random_days)


# =============================================================================
# LEAD GENERATOR
# =============================================================================

def generate_leads(count=150):
    """
    Generate Vietnamese leads with proper diacritics

    Args:
        count: Number of leads to generate

    Returns:
        List of created Lead names
    """
    print(f"\nGenerating {count} Leads...")
    created = []
    company = get_company()

    for i in range(count):
        # Random gender with slight male bias for golf
        gender = "male" if random() < 0.7 else "female"
        name_data = generate_vietnamese_name(gender)

        # Generate contact info
        phone = generate_phone()
        email = generate_email(name_data["full_name"])

        # Random status with weights
        status = weighted_choice(LEAD_STATUSES)

        # Random source
        source = choice(LEAD_SOURCES)

        # Generate golf-related notes
        interests = sample(GOLF_INTERESTS, randint(1, 3))
        notes = f"Quan tâm: {', '.join(interests)}"

        # Additional context based on status
        if status == "Interested":
            notes += ". Đã xem showroom, đang cân nhắc."
        elif status == "Replied":
            notes += ". Đã gửi báo giá, chờ phản hồi."
        elif status == "Converted":
            notes += ". Đã chuyển đổi thành khách hàng."
        elif status == "Lost":
            notes += ". Đã mua ở nơi khác."

        try:
            lead = frappe.get_doc({
                "doctype": "Lead",
                "first_name": name_data["first_name"],
                "last_name": f"{name_data['middle_name']} {name_data['last_name']}",
                "email_id": email,
                "mobile_no": phone,
                "status": status,
                "source": source,
                "company": company,
                "lead_owner": "Administrator"
            })
            lead.flags.ignore_permissions = True
            lead.flags.ignore_mandatory = True
            lead.insert()

            created.append(lead.name)

            if (i + 1) % 50 == 0:
                print(f"  Created {i + 1}/{count} leads...")
                frappe.db.commit()

        except Exception as e:
            print(f"  Error creating lead {i+1}: {str(e)}")
            continue

    frappe.db.commit()
    print(f"  Created {len(created)} leads successfully!")
    return created


# =============================================================================
# OPPORTUNITY GENERATOR
# =============================================================================

def generate_opportunities(count=100):
    """
    Generate opportunities from existing Leads and Customers

    Args:
        count: Number of opportunities to generate

    Returns:
        List of created Opportunity names
    """
    print(f"\nGenerating {count} Opportunities...")

    # Get existing leads and customers
    leads = frappe.get_all("Lead",
        filters={"status": ["not in", ["Converted", "Do Not Contact"]]},
        fields=["name", "lead_name"]
    )
    customers = frappe.get_all("Customer", fields=["name", "customer_name"])

    if not leads and not customers:
        print("  No leads or customers found. Please generate leads first.")
        return []

    created = []
    company = get_company()

    for i in range(count):
        # 70% from Lead, 30% from Customer
        if leads and (not customers or random() < 0.7):
            source = choice(leads)
            opportunity_from = "Lead"
            party_name = source.name
        else:
            source = choice(customers)
            opportunity_from = "Customer"
            party_name = source.name

        # Random stage
        stage = weighted_choice(OPPORTUNITY_STAGES)

        # Status - mostly Open, some Converted or Lost
        status_roll = random()
        if status_roll < 0.75:
            status = "Open"
        elif status_roll < 0.90:
            status = "Converted"
        else:
            status = "Lost"

        # Probability based on stage
        stage_probabilities = {
            "Prospecting": randint(10, 25),
            "Qualification": randint(20, 35),
            "Needs Analysis": randint(30, 50),
            "Value Proposition": randint(40, 55),
            "Identifying Decision Makers": randint(45, 60),
            "Proposal/Price Quote": randint(55, 75),
            "Negotiation/Review": randint(70, 90)
        }
        probability = stage_probabilities.get(stage, 50)

        # Amount based on customer type
        if opportunity_from == "Customer":
            # B2B usually larger deals
            amount = randint(50, 500) * 1000000  # 50M - 500M VND
        else:
            # B2C smaller deals
            amount = randint(5, 100) * 1000000  # 5M - 100M VND

        # Expected closing date
        base_date = getdate(nowdate())
        closing_date = add_days(base_date, randint(7, 90))

        # Notes based on amount and stage
        if amount > 200000000:
            notes = "Đơn hàng lớn - cần approval từ quản lý"
        elif amount > 50000000:
            notes = "Deal trung bình - follow up hàng tuần"
        else:
            notes = "Deal nhỏ - chốt nhanh trong tuần"

        if stage == "Negotiation/Review":
            notes += ". Đang thương lượng giá và điều khoản."

        try:
            opp = frappe.get_doc({
                "doctype": "Opportunity",
                "opportunity_from": opportunity_from,
                "party_name": party_name,
                "opportunity_type": "Sales",
                "status": status,
                "sales_stage": stage,
                "source": choice(LEAD_SOURCES),
                "expected_closing": closing_date,
                "opportunity_amount": amount,
                "probability": probability,
                "company": company
            })
            opp.flags.ignore_permissions = True
            opp.flags.ignore_mandatory = True
            opp.insert()

            created.append(opp.name)

            if (i + 1) % 25 == 0:
                print(f"  Created {i + 1}/{count} opportunities...")
                frappe.db.commit()

        except Exception as e:
            print(f"  Error creating opportunity {i+1}: {str(e)}")
            continue

    frappe.db.commit()
    print(f"  Created {len(created)} opportunities successfully!")
    return created


# =============================================================================
# CUSTOMER GENERATOR
# =============================================================================

def generate_customers(count=100, b2b_ratio=0.3):
    """
    Generate Vietnamese customers (both B2C individuals and B2B companies)

    Args:
        count: Total number of customers
        b2b_ratio: Ratio of B2B customers (default 30%)

    Returns:
        List of created Customer names
    """
    print(f"\nGenerating {count} Customers ({int(b2b_ratio*100)}% B2B)...")
    created = []

    # Get customer groups
    customer_groups = frappe.get_all("Customer Group",
        filters={"is_group": 0}, pluck="name")

    if not customer_groups:
        customer_groups = ["All Customer Groups"]

    # Get territory
    territory = frappe.db.get_single_value("Selling Settings", "territory") or \
                frappe.db.get_value("Territory", {"is_group": 0}, "name") or \
                "All Territories"

    b2b_count = int(count * b2b_ratio)
    b2c_count = count - b2b_count

    # Generate B2C customers (individuals)
    for i in range(b2c_count):
        gender = "male" if random() < 0.65 else "female"
        name_data = generate_vietnamese_name(gender)
        address = generate_address()

        customer_name = name_data["full_name"]

        # Check if exists
        if frappe.db.exists("Customer", {"customer_name": customer_name}):
            customer_name = f"{customer_name} ({randint(1, 999)})"

        try:
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": customer_name,
                "customer_type": "Individual",
                "customer_group": choice(customer_groups),
                "territory": territory,
                "mobile_no": generate_phone(),
                "email_id": generate_email(name_data["full_name"])
            })
            customer.flags.ignore_permissions = True
            customer.flags.ignore_mandatory = True
            customer.insert()

            created.append(customer.name)

            if (i + 1) % 50 == 0:
                print(f"  Created {i + 1}/{b2c_count} B2C customers...")
                frappe.db.commit()

        except Exception as e:
            print(f"  Error creating B2C customer {i+1}: {str(e)}")
            continue

    # Generate B2B customers (companies)
    for i in range(b2b_count):
        # Generate company name
        company_type = choice(B2B_TYPES)

        if random() < 0.4:
            # Golf-related business
            base_name = f"{choice(FAMILY_NAMES)} {choice(GOLF_COMPANIES)}"
        elif random() < 0.3:
            # Golf course pro shop
            base_name = choice(GOLF_COURSES).replace("Sân Golf ", "Pro Shop ")
        else:
            # Generic company
            name_data = generate_vietnamese_name()
            base_name = f"Công ty {company_type} {name_data['first_name']} {choice(['Sports', 'Trading', 'Commerce', 'Distribution'])}"

        customer_name = base_name

        # Check if exists
        if frappe.db.exists("Customer", {"customer_name": customer_name}):
            customer_name = f"{customer_name} ({randint(1, 999)})"

        address = generate_address()

        try:
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": customer_name,
                "customer_type": "Company",
                "customer_group": choice(customer_groups),
                "territory": territory,
                "mobile_no": generate_phone(),
                "email_id": generate_email(base_name.split()[0])
            })
            customer.flags.ignore_permissions = True
            customer.flags.ignore_mandatory = True
            customer.insert()

            created.append(customer.name)

            if (i + 1) % 20 == 0:
                print(f"  Created {i + 1}/{b2b_count} B2B customers...")
                frappe.db.commit()

        except Exception as e:
            print(f"  Error creating B2B customer {i+1}: {str(e)}")
            continue

    frappe.db.commit()
    print(f"  Created {len(created)} customers successfully!")
    return created


# =============================================================================
# SUPPLIER GENERATOR
# =============================================================================

def generate_suppliers(count=50):
    """
    Generate Vietnamese suppliers for golf equipment

    Args:
        count: Number of suppliers to generate

    Returns:
        List of created Supplier names
    """
    print(f"\nGenerating {count} Suppliers...")
    created = []

    # Get supplier groups
    supplier_groups = frappe.get_all("Supplier Group", pluck="name")
    if not supplier_groups:
        supplier_groups = ["All Supplier Groups"]

    for i in range(count):
        # Generate supplier name
        brand = choice(GOLF_BRANDS)
        supplier_type = choice(SUPPLIER_TYPES)
        city = choice(["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng"])

        name_patterns = [
            f"Công ty TNHH {brand} Việt Nam",
            f"Đại lý {brand} {city}",
            f"Công ty CP Thể thao {choice(FAMILY_NAMES)}",
            f"NPP {brand} chính hãng",
            f"Công ty TNHH TM {choice(FAMILY_NAMES)} Sports",
            f"Golf Equipment {choice(FAMILY_NAMES)}",
        ]

        supplier_name = choice(name_patterns)

        # Check if exists
        if frappe.db.exists("Supplier", {"supplier_name": supplier_name}):
            supplier_name = f"{supplier_name} ({randint(1, 999)})"

        try:
            supplier = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": supplier_name,
                "supplier_type": supplier_type,
                "supplier_group": choice(supplier_groups),
                "country": "Vietnam",
                "mobile_no": generate_phone(),
                "email_id": generate_email(supplier_name.split()[0])
            })
            supplier.flags.ignore_permissions = True
            supplier.flags.ignore_mandatory = True
            supplier.insert()

            created.append(supplier.name)

            if (i + 1) % 20 == 0:
                print(f"  Created {i + 1}/{count} suppliers...")
                frappe.db.commit()

        except Exception as e:
            print(f"  Error creating supplier {i+1}: {str(e)}")
            continue

    frappe.db.commit()
    print(f"  Created {len(created)} suppliers successfully!")
    return created


# =============================================================================
# SALES ORDER GENERATOR
# =============================================================================

def generate_sales_orders(count=150, start_date=None, end_date=None, submit=False):
    """
    Generate Sales Orders with Vietnamese customers

    Args:
        count: Number of Sales Orders
        start_date: Start date (default: 3 months ago)
        end_date: End date (default: today)
        submit: Whether to submit orders

    Returns:
        List of created Sales Order names
    """
    print(f"\nGenerating {count} Sales Orders...")

    if not start_date:
        start_date = add_days(nowdate(), -90)
    if not end_date:
        end_date = nowdate()

    # Get data
    customers = frappe.get_all("Customer", pluck="name")
    items = frappe.get_all("Item",
        filters={"is_sales_item": 1, "disabled": 0},
        fields=["item_code", "item_name", "standard_rate", "stock_uom"]
    )

    if not customers:
        print("  No customers found. Please generate customers first.")
        return []

    if not items:
        print("  No items found. Please install master data first.")
        return []

    # Get warehouse
    company = get_company()
    warehouse = frappe.db.get_value("Warehouse",
        {"company": company, "is_group": 0},
        "name"
    )

    created = []

    for i in range(count):
        transaction_date = get_random_date(start_date, end_date)
        delivery_date = add_days(transaction_date, randint(3, 14))

        customer = choice(customers)

        # Random items (1-5 per order)
        num_items = randint(1, min(5, len(items)))
        selected_items = sample(items, num_items)

        so_items = []
        for item in selected_items:
            qty = randint(1, 5)
            rate = flt(item.standard_rate) or randint(100000, 50000000)

            so_items.append({
                "item_code": item.item_code,
                "qty": qty,
                "rate": rate,
                "delivery_date": delivery_date,
                "warehouse": warehouse
            })

        try:
            so = frappe.get_doc({
                "doctype": "Sales Order",
                "customer": customer,
                "transaction_date": transaction_date,
                "delivery_date": delivery_date,
                "company": company,
                "items": so_items
            })
            so.flags.ignore_permissions = True
            so.flags.ignore_mandatory = True
            so.insert()

            if submit:
                so.submit()

            created.append(so.name)

            if (i + 1) % 50 == 0:
                print(f"  Created {i + 1}/{count} sales orders...")
                frappe.db.commit()

        except Exception as e:
            print(f"  Error creating SO {i+1}: {str(e)}")
            continue

    frappe.db.commit()
    print(f"  Created {len(created)} sales orders successfully!")
    return created


# =============================================================================
# PURCHASE ORDER GENERATOR
# =============================================================================

def generate_purchase_orders(count=100, start_date=None, end_date=None, submit=False):
    """
    Generate Purchase Orders with Vietnamese suppliers

    Args:
        count: Number of Purchase Orders
        start_date: Start date (default: 3 months ago)
        end_date: End date (default: today)
        submit: Whether to submit orders

    Returns:
        List of created Purchase Order names
    """
    print(f"\nGenerating {count} Purchase Orders...")

    if not start_date:
        start_date = add_days(nowdate(), -90)
    if not end_date:
        end_date = nowdate()

    # Get data
    suppliers = frappe.get_all("Supplier", pluck="name")
    items = frappe.get_all("Item",
        filters={"is_purchase_item": 1, "disabled": 0},
        fields=["item_code", "item_name", "standard_rate", "stock_uom"]
    )

    if not suppliers:
        print("  No suppliers found. Please generate suppliers first.")
        return []

    if not items:
        print("  No items found. Please install master data first.")
        return []

    # Get warehouse
    company = get_company()
    warehouse = frappe.db.get_value("Warehouse",
        {"company": company, "is_group": 0},
        "name"
    )

    created = []

    for i in range(count):
        transaction_date = get_random_date(start_date, end_date)
        schedule_date = add_days(transaction_date, randint(7, 30))

        supplier = choice(suppliers)

        # Random items (2-8 per order - POs usually larger)
        num_items = randint(2, min(8, len(items)))
        selected_items = sample(items, num_items)

        po_items = []
        for item in selected_items:
            qty = randint(5, 50)  # Larger quantities for PO
            rate = flt(item.standard_rate) * 0.6 or randint(50000, 30000000)  # Cost price ~60%

            po_items.append({
                "item_code": item.item_code,
                "qty": qty,
                "rate": rate,
                "schedule_date": schedule_date,
                "warehouse": warehouse
            })

        try:
            po = frappe.get_doc({
                "doctype": "Purchase Order",
                "supplier": supplier,
                "transaction_date": transaction_date,
                "schedule_date": schedule_date,
                "company": company,
                "items": po_items
            })
            po.flags.ignore_permissions = True
            po.flags.ignore_mandatory = True
            po.insert()

            if submit:
                po.submit()

            created.append(po.name)

            if (i + 1) % 50 == 0:
                print(f"  Created {i + 1}/{count} purchase orders...")
                frappe.db.commit()

        except Exception as e:
            print(f"  Error creating PO {i+1}: {str(e)}")
            continue

    frappe.db.commit()
    print(f"  Created {len(created)} purchase orders successfully!")
    return created


# =============================================================================
# FITTING SESSION GENERATOR (wrapper)
# =============================================================================

def generate_fitting_sessions(count=50, submit=False):
    """
    Generate Fitting Sessions with Vietnamese customers/leads

    Args:
        count: Number of Fitting Sessions (default 50)
        submit: Whether to submit sessions (not used, for API consistency)

    Returns:
        List of created Fitting Session names
    """
    try:
        from dcnet_fixtures.dcnet_fixtures.generators.fitting import generate_fitting_sessions as _generate_fitting
        return _generate_fitting(count=count, submit=submit)
    except ImportError as e:
        print(f"  ⚠️  Fitting generator not available: {e}")
        return []
    except Exception as e:
        # Check if DocType doesn't exist
        if "Fitting Session" in str(e):
            print(f"  ⚠️  Fitting Session DocType not found. Skipping...")
        else:
            print(f"  ⚠️  Error generating Fitting Sessions: {str(e)}")
        return []


# =============================================================================
# MAIN FUNCTION - GENERATE ALL DATA
# =============================================================================

def generate_all_data(
    leads=150,
    opportunities=100,
    customers=100,
    suppliers=50,
    sales_orders=150,
    purchase_orders=100,
    fitting_sessions=50,
    submit_orders=False
):
    """
    Generate all sample data with Vietnamese names and diacritics

    Args:
        leads: Number of leads (default 150)
        opportunities: Number of opportunities (default 100)
        customers: Number of customers (default 100)
        suppliers: Number of suppliers (default 50)
        sales_orders: Number of sales orders (default 150)
        purchase_orders: Number of purchase orders (default 100)
        fitting_sessions: Number of fitting sessions (default 50)
        submit_orders: Whether to submit orders (default False)

    Returns:
        Summary dict
    """
    print("\n" + "=" * 60)
    print("DCNET Vietnamese Data Generator")
    print("=" * 60)

    summary = {}

    # Step 1: Customers first (needed for opportunities and fitting)
    print("\n[1/7] Generating Customers...")
    summary["customers"] = generate_customers(customers)

    # Step 2: Suppliers
    print("\n[2/7] Generating Suppliers...")
    summary["suppliers"] = generate_suppliers(suppliers)

    # Step 3: Leads
    print("\n[3/7] Generating Leads...")
    summary["leads"] = generate_leads(leads)

    # Step 4: Opportunities (from leads and customers)
    print("\n[4/7] Generating Opportunities...")
    summary["opportunities"] = generate_opportunities(opportunities)

    # Step 5: Sales Orders
    print("\n[5/7] Generating Sales Orders...")
    summary["sales_orders"] = generate_sales_orders(sales_orders, submit=submit_orders)

    # Step 6: Purchase Orders
    print("\n[6/7] Generating Purchase Orders...")
    summary["purchase_orders"] = generate_purchase_orders(purchase_orders, submit=submit_orders)

    # Step 7: Fitting Sessions (requires customers/leads)
    print("\n[7/7] Generating Fitting Sessions...")
    summary["fitting_sessions"] = generate_fitting_sessions(fitting_sessions)

    frappe.db.commit()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Customers:         {len(summary.get('customers', []))}")
    print(f"  Suppliers:         {len(summary.get('suppliers', []))}")
    print(f"  Leads:             {len(summary.get('leads', []))}")
    print(f"  Opportunities:     {len(summary.get('opportunities', []))}")
    print(f"  Sales Orders:      {len(summary.get('sales_orders', []))}")
    print(f"  Purchase Orders:   {len(summary.get('purchase_orders', []))}")
    print(f"  Fitting Sessions:  {len(summary.get('fitting_sessions', []))}")
    print("=" * 60)

    return summary


# =============================================================================
# CLEAR GENERATED DATA
# =============================================================================

def clear_generated_data(confirm=False):
    """
    Clear all generated data (use with caution!)

    Args:
        confirm: Must be True to proceed
    """
    if not confirm:
        print("Pass confirm=True to clear all generated data")
        return

    print("\n" + "=" * 60)
    print("CLEARING GENERATED DATA")
    print("=" * 60)

    # Clear in reverse order of dependencies
    doctypes = [
        "Purchase Order",
        "Sales Order",
        "Opportunity",
        "Lead",
        "Customer",
        "Supplier"
    ]

    for doctype in doctypes:
        try:
            count = frappe.db.count(doctype)
            if count > 0:
                print(f"  Deleting {count} {doctype}s...")
                frappe.db.delete(doctype)
                frappe.db.commit()
        except Exception as e:
            print(f"  Error clearing {doctype}: {str(e)}")

    print("\nData cleared!")
