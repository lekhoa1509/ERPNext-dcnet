# Implementation Plan: Lead Module

> **Module:** Lead Management
> **Based on:** LEAD_GAP_ANALYSIS.md
> **Target ERPNext Version:** v15.8.0
> **Estimated Duration:** 6 weeks
> **Team Size:** 2 developers (1 Backend, 1 Frontend)

---

## Implementation Strategy

### Approach Summary
- **ERPNext Standard Features:** 56%
- **Customization/Extension:** 31%
- **New Development:** 13%

### Architecture Decisions

| Decision Point | Options Considered | Selected | Rationale |
| --- | --- | --- | --- |
| Duplicate check method | 1. Python validation<br>2. Database unique constraint<br>3. Client-side JS only | Python validation | Better error messages, can check both phone AND email, flexible for future |
| Consultation history storage | 1. Child DocType<br>2. JSON field<br>3. Separate linked DocType | Child DocType | ERPNext best practice, easier queries, standard UI |
| Lead→Customer conversion | 1. Manual button<br>2. Auto on Sales Order submit<br>3. Workflow state | Auto on Sales Order submit | Matches spec requirement, reduces manual steps |
| Branch linking | 1. Custom field<br>2. Territory mapping<br>3. New Branch DocType | New Branch DocType | Clean separation, scalable for multiple branches |
| nhanh_vn integration | 1. Webhook<br>2. Scheduled sync<br>3. Manual import | Webhook | Real-time, matches spec requirement |

---

## Technical Implementation Breakdown

### Phase 1: Data Model Setup (Week 1-2)

#### Task 1.1: Create Branch DocType
**Category:** Backend - Data Model
**Effort:** 1 day
**Developer:** Backend Dev

**Deliverables:**
- `Branch` DocType
  - Fields: branch_code, branch_name, address, phone, manager (Link to User)
  - Permissions: System Manager (full access), Sales Manager (read)
  - Naming: Auto-increment (BRANCH-00001)

**Code Locations:**
```
flow_next/apps/flow_next/flow_next/
└── setup/
    └── doctype/
        └── branch/
            ├── branch.json
            ├── branch.py
            └── branch.js
```

**ERPNext Patterns to Follow:**
- Extend `Document` class
- Simple master data pattern
- Reference: `erpnext/setup/doctype/territory/territory.py`

**Acceptance Criteria:**
- [ ] Branch DocType created and migrated
- [ ] Can create/edit/delete branches
- [ ] Naming series works
- [ ] Permissions configured

---

#### Task 1.2: Add Custom Fields to Lead DocType
**Category:** Backend - Customization
**Effort:** 2 days
**Developer:** Backend Dev

**Custom Fields to Add:**

| Field Name | Type | Options | Insert After | Mandatory |
| --- | --- | --- | --- | --- |
| `custom_branch` | Link | Branch | territory | No |
| `custom_date_received` | Date | - | creation | No |
| `custom_last_contact` | Datetime | - | lead_owner | No |
| `custom_total_interactions` | Int | Default: 0 | custom_last_contact | No |
| `custom_birth_date` | Date | - | gender | No |
| `custom_price_list` | Link | Price List | territory | No |
| `custom_sales_person` | Link | Sales Person | lead_owner | No |
| `custom_age_group` | Select | 18-25, 26-35, 36-45, 46-55, 56+ | custom_birth_date | No |

**Code Locations:**
```
flow_next/apps/flow_next/flow_next/
└── fixtures/
    └── custom_field.json
```

**Implementation:**
```json
[
  {
    "doctype": "Custom Field",
    "dt": "Lead",
    "fieldname": "custom_branch",
    "fieldtype": "Link",
    "label": "Chi nhánh",
    "options": "Branch",
    "insert_after": "territory"
  },
  {
    "doctype": "Custom Field",
    "dt": "Lead",
    "fieldname": "custom_date_received",
    "fieldtype": "Date",
    "label": "Ngày nhận lead",
    "insert_after": "creation",
    "default": "Today"
  }
  // ... (remaining 6 fields)
]
```

**ERPNext Approach:**
- Use Fixtures for version control
- Avoid direct database changes
- Run `bench --site [site] migrate` to apply

**Acceptance Criteria:**
- [ ] All 8 custom fields added via fixture
- [ ] Fields appear in Lead form (correct positions)
- [ ] Field types and options correct
- [ ] Default values work (e.g., custom_date_received = Today)

---

#### Task 1.3: Create Lead Consultation Log Child DocType
**Category:** Backend - Data Model
**Effort:** 2 days
**Developer:** Backend Dev

**Deliverables:**
- `Lead Consultation Log` Child DocType
  - Fields: product (Link to Item), consultant (Link to User), consultation_date, content (Text)
  - Linked to: Lead (parent field)
  - Not standalone (istable = 1)

**Code Locations:**
```
flow_next/apps/flow_next/flow_next/
└── crm/
    └── doctype/
        └── lead_consultation_log/
            ├── lead_consultation_log.json
            ├── lead_consultation_log.py
            └── __init__.py
```

**Implementation:**
```python
# File: lead_consultation_log.py
from frappe.model.document import Document

class LeadConsultationLog(Document):
    pass  # Simple child table, no custom logic needed
```

**Child Table in Lead:**
Add custom field to Lead DocType:
```json
{
  "doctype": "Custom Field",
  "dt": "Lead",
  "fieldname": "custom_consultation_history",
  "fieldtype": "Table",
  "label": "Lịch sử tư vấn",
  "options": "Lead Consultation Log",
  "insert_after": "notes"
}
```

**ERPNext Patterns to Follow:**
- Child DocType pattern (istable = 1)
- Reference: `erpnext/crm/doctype/opportunity_item/opportunity_item.py`

**Acceptance Criteria:**
- [ ] Lead Consultation Log DocType created
- [ ] Child table appears in Lead form
- [ ] Can add/edit/delete consultation entries
- [ ] Fields validated (product, consultant required)

---

### Phase 2: Business Logic (Week 2-3)

#### Task 2.1: Duplicate Check Validation
**Category:** Backend - Business Logic
**Effort:** 1 day
**Developer:** Backend Dev

**Requirements (from SPEC):**
> Check trùng thông tin (khi tạo lead) - by phone/email

**Implementation:**
```python
# File: flow_next/crm/overrides/lead.py
import frappe
from frappe import _
from erpnext.crm.doctype.lead.lead import Lead as StandardLead

class Lead(StandardLead):
    def validate(self):
        super().validate()  # Call standard ERPNext validation

        # Custom: Check duplicate by phone
        if self.phone:
            self.check_duplicate_phone()

        # Custom: Check duplicate by email
        if self.email_id:
            self.check_duplicate_email()

    def check_duplicate_phone(self):
        """Check if lead with same phone already exists"""
        existing = frappe.db.exists("Lead", {
            "phone": self.phone,
            "name": ["!=", self.name],
            "status": ["!=", "Do Not Contact"]  # Ignore leads marked as DNC
        })

        if existing:
            existing_lead = frappe.get_doc("Lead", existing)
            frappe.throw(
                _("Lead với số điện thoại {0} đã tồn tại: {1}").format(
                    self.phone,
                    frappe.utils.get_link_to_form("Lead", existing_lead.name)
                )
            )

    def check_duplicate_email(self):
        """Check if lead with same email already exists"""
        existing = frappe.db.exists("Lead", {
            "email_id": self.email_id,
            "name": ["!=", self.name],
            "status": ["!=", "Do Not Contact"]
        })

        if existing:
            existing_lead = frappe.get_doc("Lead", existing)
            frappe.throw(
                _("Lead với email {0} đã tồn tại: {1}").format(
                    self.email_id,
                    frappe.utils.get_link_to_form("Lead", existing_lead.name)
                )
            )
```

**Hook Configuration:**
```python
# File: flow_next/apps/flow_next/flow_next/hooks.py

doc_events = {
    "Lead": {
        "validate": "flow_next.crm.overrides.lead.Lead.validate"
    }
}
```

**Testing:**
```python
# File: flow_next/crm/overrides/test_lead.py
import frappe
from frappe.tests.utils import FrappeTestCase

class TestLeadDuplicateCheck(FrappeTestCase):
    def test_duplicate_phone(self):
        # Create first lead
        lead1 = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": "Test Lead 1",
            "phone": "0901234567"
        })
        lead1.insert()

        # Try to create duplicate by phone
        lead2 = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": "Test Lead 2",
            "phone": "0901234567"
        })

        with self.assertRaises(frappe.ValidationError):
            lead2.insert()

    def test_duplicate_email(self):
        # Similar test for email
        pass
```

**Acceptance Criteria:**
- [ ] Duplicate check works for phone
- [ ] Duplicate check works for email
- [ ] Error message includes link to existing lead
- [ ] Unit tests pass
- [ ] Does not block if existing lead is "Do Not Contact"

---

#### Task 2.2: Auto Lead → Customer Conversion on Sales Order
**Category:** Backend - Workflow
**Effort:** 2 days
**Developer:** Backend Dev

**Requirements (from SPEC):**
> Khi tạo đơn hàng, Lead tự động chuyển thành Khách hàng

**Implementation:**
```python
# File: flow_next/selling/overrides/sales_order.py
import frappe
from frappe import _
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder as StandardSalesOrder

class SalesOrder(StandardSalesOrder):
    def on_submit(self):
        super().on_submit()  # Call ERPNext standard logic

        # Custom: Auto-convert Lead to Customer
        if self.party_type == "Lead":
            self.convert_lead_to_customer()

    def convert_lead_to_customer(self):
        """Convert Lead to Customer and update Sales Order"""
        lead_name = self.party_name

        # Get Lead document
        lead = frappe.get_doc("Lead", lead_name)

        # Use ERPNext standard conversion method
        customer = lead.make_customer()

        # Update Sales Order to reference new Customer
        self.db_set("party_type", "Customer")
        self.db_set("party_name", customer.name)
        self.db_set("customer_name", customer.customer_name)

        # Reload to reflect changes
        self.reload()

        # Log conversion
        frappe.msgprint(
            _("Lead {0} đã được chuyển đổi thành Khách hàng {1}").format(
                frappe.utils.get_link_to_form("Lead", lead_name),
                frappe.utils.get_link_to_form("Customer", customer.name)
            ),
            indicator="green",
            alert=True
        )

        # Update lead status
        lead.db_set("status", "Converted")
```

**Hook Configuration:**
```python
# File: flow_next/hooks.py

doc_events = {
    "Sales Order": {
        "on_submit": "flow_next.selling.overrides.sales_order.SalesOrder.on_submit"
    }
}
```

**Testing:**
```python
# File: flow_next/selling/overrides/test_sales_order.py

def test_lead_to_customer_conversion():
    # Create Lead
    lead = frappe.get_doc({
        "doctype": "Lead",
        "lead_name": "Test Lead",
        "phone": "0901234567"
    })
    lead.insert()

    # Create Sales Order from Lead
    so = frappe.get_doc({
        "doctype": "Sales Order",
        "party_type": "Lead",
        "party_name": lead.name,
        "delivery_date": frappe.utils.today(),
        "items": [{
            "item_code": "Test Item",
            "qty": 1,
            "rate": 100
        }]
    })
    so.insert()
    so.submit()

    # Verify conversion
    assert so.party_type == "Customer"
    assert frappe.db.exists("Customer", so.party_name)

    # Verify Lead status updated
    lead.reload()
    assert lead.status == "Converted"
```

**Dependencies:**
- ERPNext standard `Lead.make_customer()` method

**Acceptance Criteria:**
- [ ] Sales Order submission triggers conversion
- [ ] Customer created with correct data from Lead
- [ ] Sales Order updated to reference Customer
- [ ] Lead status changed to "Converted"
- [ ] User sees success message
- [ ] Integration test passes

---

#### Task 2.3: Auto-increment Total Interactions
**Category:** Backend - Business Logic
**Effort:** 0.5 day
**Developer:** Backend Dev

**Requirements:**
> Track "Tổng số tương tác" automatically

**Implementation:**
```python
# File: flow_next/crm/overrides/lead.py

class Lead(StandardLead):
    def after_save(self):
        super().after_save()
        self.update_interaction_count()

    def update_interaction_count(self):
        """Count all communications linked to this lead"""
        count = frappe.db.count("Communication", {
            "reference_doctype": "Lead",
            "reference_name": self.name
        })

        if count != self.custom_total_interactions:
            self.db_set("custom_total_interactions", count)
```

**Alternative: Use Communication hook**
```python
# File: flow_next/hooks.py

doc_events = {
    "Communication": {
        "after_insert": "flow_next.crm.utils.update_lead_interaction_count"
    }
}

# File: flow_next/crm/utils.py
def update_lead_interaction_count(doc, method):
    if doc.reference_doctype == "Lead":
        lead = frappe.get_doc("Lead", doc.reference_name)
        count = frappe.db.count("Communication", {
            "reference_doctype": "Lead",
            "reference_name": lead.name
        })
        lead.db_set("custom_total_interactions", count)
```

**Acceptance Criteria:**
- [ ] Interaction count updates when communication added
- [ ] Count includes: calls, emails, comments, notes
- [ ] No performance impact on Lead save

---

### Phase 3: Frontend/UI (Week 3-4)

#### Task 3.1: Custom Lead List View
**Category:** Frontend - UI
**Effort:** 2 days
**Developer:** Frontend Dev

**Requirements (from SPEC):**
> Display columns: Mã KH, Tên, ĐT, Trạng thái, Email, Tags, Thời gian tạo, Ngày nhận lead, Liên hệ lần cuối, Tổng số tương tác, Người tạo, Nguồn lead, Chi nhánh, Địa chỉ, Giới tính

**Implementation:**
```javascript
// File: flow_next/crm/doctype/lead/lead_list.js

frappe.listview_settings['Lead'] = {
    add_fields: [
        "lead_name", "phone", "email_id", "status", "custom_branch",
        "source", "gender", "creation", "custom_date_received",
        "custom_last_contact", "custom_total_interactions", "lead_owner"
    ],

    get_indicator: function(doc) {
        // Color-code by status
        const status_colors = {
            "Open": "orange",
            "Replied": "blue",
            "Interested": "green",
            "Quotation": "purple",
            "Converted": "green",
            "Do Not Contact": "red"
        };
        return [__(doc.status), status_colors[doc.status] || "gray", "status,=," + doc.status];
    },

    onload: function(listview) {
        // Add custom button: Import Leads
        listview.page.add_inner_button(__("Import Leads"), function() {
            frappe.route_options = {"reference_doctype": "Lead"};
            frappe.set_route("Form", "Data Import", "New Data Import");
        });

        // Add custom button: Export Leads
        listview.page.add_inner_button(__("Export Leads"), function() {
            frappe.utils.csvDownload(
                frappe.utils.get_query_params({
                    doctype: "Lead",
                    file_format: "Excel"
                })
            );
        });
    },

    // Custom filters
    filters: [
        ["status", "!=", "Do Not Contact"]
    ]
};
```

**Acceptance Criteria:**
- [ ] All required columns visible in list view
- [ ] Custom fields (branch, date_received, etc.) display correctly
- [ ] Status color indicators work
- [ ] Import/Export buttons functional
- [ ] Default filter excludes "Do Not Contact" leads

---

#### Task 3.2: Lead Form Custom Scripts
**Category:** Frontend - Form
**Effort:** 1 day
**Developer:** Frontend Dev

**Requirements:**
- Auto-calculate age group from birth_date
- Auto-set date_received to today on new lead
- Validate consultation log entries

**Implementation:**
```javascript
// File: flow_next/crm/doctype/lead/lead.js

frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        // Custom button: Convert to Customer (if not converted)
        if (frm.doc.status != "Converted" && !frm.is_new()) {
            frm.add_custom_button(__('Convert to Customer'), function() {
                frappe.call({
                    method: "erpnext.crm.doctype.lead.lead.make_customer",
                    args: {
                        source_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(__("Customer created: {0}", [r.message.name]));
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
    },

    onload_post_render: function(frm) {
        // Auto-set date_received for new leads
        if (frm.is_new() && !frm.doc.custom_date_received) {
            frm.set_value('custom_date_received', frappe.datetime.get_today());
        }
    },

    custom_birth_date: function(frm) {
        // Auto-calculate age group
        if (frm.doc.custom_birth_date) {
            let birth_year = new Date(frm.doc.custom_birth_date).getFullYear();
            let current_year = new Date().getFullYear();
            let age = current_year - birth_year;

            let age_group = '';
            if (age >= 18 && age <= 25) age_group = '18-25';
            else if (age >= 26 && age <= 35) age_group = '26-35';
            else if (age >= 36 && age <= 45) age_group = '36-45';
            else if (age >= 46 && age <= 55) age_group = '46-55';
            else if (age >= 56) age_group = '56+';

            frm.set_value('custom_age_group', age_group);
        }
    }
});

// Consultation Log validation
frappe.ui.form.on('Lead Consultation Log', {
    consultation_date: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        // Cannot set future date
        if (row.consultation_date > frappe.datetime.get_today()) {
            frappe.msgprint(__('Consultation date cannot be in the future'));
            frappe.model.set_value(cdt, cdn, 'consultation_date', '');
        }
    }
});
```

**Acceptance Criteria:**
- [ ] Date_received auto-fills on new lead
- [ ] Age group calculates automatically from birth_date
- [ ] Convert to Customer button works
- [ ] Consultation date validation works
- [ ] Form UI responsive and user-friendly

---

### Phase 4: Integration (Week 4-5)

#### Task 4.1: nhanh_vn Webhook Integration
**Category:** Integration - External API
**Effort:** 3 days
**Developer:** Backend Dev

**Requirements (from SPEC):**
> Tự động tạo lead mới từ nhanh_vn - Về với các nguồn đa kênh

**Implementation:**
```python
# File: flow_next/crm/api/webhooks.py

import frappe
from frappe import _
import hmac
import hashlib

@frappe.whitelist(allow_guest=True)
def nhanh_vn_lead_webhook():
    """
    Receive webhook from nhanh_vn and create Lead

    Expected payload:
    {
        "name": "Nguyen Van A",
        "phone": "0901234567",
        "email": "example@email.com",
        "channel": "Facebook",  // or "Zalo", "Website", etc.
        "message": "Quan tâm sản phẩm X"
    }
    """

    # Validate webhook signature
    if not validate_nhanh_signature():
        frappe.throw(_("Invalid webhook signature"), frappe.PermissionError)

    # Parse request data
    try:
        data = frappe.request.json
    except Exception:
        frappe.throw(_("Invalid JSON payload"))

    # Map nhanh_vn data to Lead fields
    lead_data = {
        "doctype": "Lead",
        "lead_name": data.get("name"),
        "phone": data.get("phone"),
        "email_id": data.get("email"),
        "source": "nhanh_vn",  # Custom source
        "custom_date_received": frappe.utils.now(),
        "status": "Open",
        "notes": data.get("message", "")
    }

    # Check for existing lead (duplicate check will run in validate)
    try:
        lead = frappe.get_doc(lead_data)
        lead.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "success": True,
            "lead_id": lead.name,
            "message": _("Lead created successfully")
        }

    except frappe.DuplicateEntryError:
        # Handle duplicate - update existing lead
        existing_lead = frappe.db.get_value("Lead", {"phone": lead_data["phone"]}, "name")

        if existing_lead:
            lead = frappe.get_doc("Lead", existing_lead)
            lead.add_comment("Comment", f"New inquiry from nhanh_vn: {data.get('message')}")

            return {
                "success": True,
                "lead_id": lead.name,
                "message": _("Lead updated (duplicate found)")
            }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "nhanh_vn webhook error")
        return {
            "success": False,
            "message": str(e)
        }

def validate_nhanh_signature():
    """
    Validate webhook signature using HMAC
    """
    signature = frappe.request.headers.get("X-Nhanh-Signature")
    if not signature:
        return False

    # Get secret key from settings
    secret = frappe.get_doc("Integration Settings").get_password("nhanh_vn_secret")

    # Calculate expected signature
    payload = frappe.request.data
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
```

**Configuration:**
- Webhook URL: `https://your-domain.com/api/method/flow_next.crm.api.webhooks.nhanh_vn_lead_webhook`
- Authentication: HMAC signature in header `X-Nhanh-Signature`
- Store secret key in Integration Settings

**Testing:**
```python
# File: flow_next/crm/api/test_webhooks.py

import json
import hmac
import hashlib

def test_nhanh_webhook_valid():
    payload = {
        "name": "Test Lead",
        "phone": "0901234567",
        "email": "test@example.com",
        "channel": "Facebook",
        "message": "Quan tâm sản phẩm"
    }

    # Calculate signature
    secret = "test_secret_key"
    signature = hmac.new(
        secret.encode(),
        json.dumps(payload).encode(),
        hashlib.sha256
    ).hexdigest()

    # Make request
    response = requests.post(
        "http://localhost:8000/api/method/flow_next.crm.api.webhooks.nhanh_vn_lead_webhook",
        json=payload,
        headers={"X-Nhanh-Signature": signature}
    )

    assert response.status_code == 200
    assert response.json()["success"] == True
```

**Acceptance Criteria:**
- [ ] Webhook endpoint receives POST requests
- [ ] Signature validation works
- [ ] Lead created from webhook data
- [ ] Duplicate handling works (updates existing)
- [ ] Error logging functional
- [ ] Integration test with nhanh_vn staging passes

---

#### Task 4.2: REST API Endpoints for Lead
**Category:** Integration - API
**Effort:** 1 day
**Developer:** Backend Dev

**Requirements (from SPEC):**
> Expose API tạo khách hàng từ hệ thống khác

**Implementation:**

ERPNext already provides REST API endpoints:
- GET `/api/resource/Lead` - List leads
- GET `/api/resource/Lead/{id}` - Get lead details
- POST `/api/resource/Lead` - Create lead
- PUT `/api/resource/Lead/{id}` - Update lead
- DELETE `/api/resource/Lead/{id}` - Delete lead

**Configuration:**
1. Create API User with Lead permissions
2. Generate API Key & Secret
3. Document API endpoints for external systems

**Custom API (if needed):**
```python
# File: flow_next/crm/api/lead_api.py

@frappe.whitelist()
def create_lead_from_external(lead_data):
    """
    Custom API for external systems to create leads
    with additional validation/processing
    """
    # Validate required fields
    required_fields = ["lead_name", "phone"]
    for field in required_fields:
        if not lead_data.get(field):
            frappe.throw(_(f"{field} is required"))

    # Create lead
    lead = frappe.get_doc({
        "doctype": "Lead",
        **lead_data,
        "source": "External API"
    })
    lead.insert()

    return {
        "success": True,
        "lead_id": lead.name
    }
```

**Acceptance Criteria:**
- [ ] API documentation complete
- [ ] API user created with correct permissions
- [ ] External system can create leads via API
- [ ] API key authentication works
- [ ] Rate limiting configured (if needed)

---

### Phase 5: Testing & QA (Week 5-6)

#### Task 5.1: Unit Testing
**Category:** Testing
**Effort:** 2 days
**Developer:** Backend Dev

**Test Coverage:**
- Lead CRUD operations
- Duplicate validation (phone & email)
- Lead → Customer conversion
- Consultation history
- Webhook integration
- Custom field validation

**Test Files:**
```
flow_next/apps/flow_next/flow_next/
└── crm/
    └── overrides/
        └── test_lead.py
```

**Test Cases:**
```python
class TestLead(FrappeTestCase):
    def test_create_lead(self):
        # Test basic lead creation
        pass

    def test_duplicate_phone(self):
        # Test duplicate validation
        pass

    def test_lead_to_customer(self):
        # Test auto-conversion on Sales Order
        pass

    def test_consultation_log(self):
        # Test adding consultation entries
        pass

    def test_age_group_calculation(self):
        # Test age group auto-calculation
        pass
```

**Acceptance Criteria:**
- [ ] Test coverage > 80%
- [ ] All critical paths tested
- [ ] Edge cases covered (empty fields, invalid data, etc.)
- [ ] All tests pass

---

#### Task 5.2: Integration Testing
**Category:** Testing
**Effort:** 2 days
**Developer:** QA

**Test Scenarios:**
1. **End-to-end Lead Lifecycle:**
  - Create Lead → Add consultation → Create Sales Order → Verify Customer created

2. **Import/Export:**
  - Import 100 leads from Excel → Verify all imported → Export → Compare data

3. **Webhook Integration:**
  - Trigger nhanh_vn webhook → Verify lead created → Check duplicate handling

4. **Multi-user Scenario:**
  - Admin creates lead → Assigns to sales person → Sales person updates → Create order → Verify permissions

**Acceptance Criteria:**
- [ ] All scenarios pass
- [ ] No data loss or corruption
- [ ] Permissions work correctly
- [ ] Performance acceptable (list view loads < 2s with 1000 leads)

---

### Phase 6: Documentation & Deployment (Week 6)

#### Task 6.1: Technical Documentation
**Category:** Documentation
**Effort:** 1 day
**Developer:** Tech Lead

**Deliverables:**
- API documentation (endpoints, authentication, examples)
- Custom field reference
- Deployment guide (migration steps)
- Troubleshooting guide

---

#### Task 6.2: User Documentation
**Category:** Documentation
**Effort:** 1 day
**Developer:** BA/Tech Writer

**Deliverables:**
- User manual (Vietnamese)
  - Tạo lead mới
  - Tìm kiếm và filter lead
  - Thêm lịch sử tư vấn
  - Chuyển lead thành khách hàng
  - Import/Export leads
- Quick start guide (PDF)
- Video tutorial (optional)

---

#### Task 6.3: Deployment to Staging
**Category:** DevOps
**Effort:** 0.5 day
**Developer:** DevOps

**Steps:**
1. Backup staging database
2. Deploy code to staging server
3. Run migrations: `bench --site [site] migrate`
4. Create test data (sample leads, branches)
5. QA smoke test

---

#### Task 6.4: Deployment to Production
**Category:** DevOps
**Effort:** 1 day
**Developer:** DevOps

**Steps:**
1. **Pre-deployment:**
  - Backup production database
  - Schedule maintenance window
  - Notify users

2. **Deployment:**
  - Deploy code: `git pull && bench update --patch`
  - Run migrations: `bench --site [site] migrate`
  - Clear cache: `bench --site [site] clear-cache`
  - Restart services: `sudo supervisorctl restart all`

3. **Post-deployment:**
  - Smoke test critical features
  - Monitor error logs (24 hours)
  - Rollback plan ready

**Rollback Plan:**
- Database backup location: `/home/frappe/backups/`
- Code rollback: `git checkout [previous-tag]`
- Restore database: `bench --site [site] restore [backup-file]`

**Acceptance Criteria:**
- [ ] Production deployment successful
- [ ] No critical errors in 24 hours
- [ ] User acceptance sign-off

---

## Code Structure

```
flow_next/
├── apps/
│   └── flow_next/
│       └── flow_next/
│           ├── crm/                          # CRM module
│           │   ├── overrides/
│           │   │   ├── lead.py              # Lead DocType override
│           │   │   └── test_lead.py         # Unit tests
│           │   ├── doctype/
│           │   │   └── lead_consultation_log/  # Child DocType
│           │   │       ├── lead_consultation_log.json
│           │   │       ├── lead_consultation_log.py
│           │   │       └── __init__.py
│           │   ├── api/
│           │   │   ├── webhooks.py          # nhanh_vn webhook
│           │   │   ├── lead_api.py          # Custom API endpoints
│           │   │   └── test_webhooks.py     # Integration tests
│           │   └── utils.py                 # Helper functions
│           │
│           ├── selling/
│           │   └── overrides/
│           │       └── sales_order.py       # Sales Order override (Lead conversion)
│           │
│           ├── setup/
│           │   └── doctype/
│           │       └── branch/              # Branch DocType
│           │           ├── branch.json
│           │           ├── branch.py
│           │           └── branch.js
│           │
│           ├── fixtures/
│           │   └── custom_field.json        # Custom fields for Lead
│           │
│           └── hooks.py                     # App hooks and overrides
```

---

## Technical Decisions Log

| Decision | Date | Context | Choice | Alternatives Rejected | Rationale |
| --- | --- | --- | --- | --- | --- |
| Duplicate check timing | 2026-01-12 | When to check duplicates | In `validate()` method | Database unique constraint, API-level check | Flexible, can customize logic, better error messages |
| Consultation storage | 2026-01-12 | How to store consultation history | Child DocType | JSON field, separate DocType | ERPNext best practice, easier to query and display |
| Lead conversion trigger | 2026-01-12 | When to convert Lead→Customer | On Sales Order submit | Manual button, Workflow | Matches spec requirement, automatic |
| Branch data model | 2026-01-12 | Where to store branch info | New Branch DocType | Use Territory, Custom field only | Scalable, clean separation |
| Webhook authentication | 2026-01-12 | How to secure nhanh_vn webhook | HMAC signature | API key, IP whitelist | Industry standard, secure |

---

## Migration Strategy

### Data Migration (if applicable)

**Source:** Legacy CRM system
**Target:** ERPNext Lead DocType

**Steps:**
1. Export data from legacy CRM to CSV
2. Map fields:
  - `legacy_customer_code` → `name` (Lead ID)
  - `legacy_phone` → `phone`
  - `legacy_branch_id` → `custom_branch` (after creating Branches)
3. Use ERPNext Data Import tool
4. Validate imported data (check duplicates, missing fields)
5. Run post-migration scripts (update interaction counts, etc.)

**Migration Scripts:**
```python
# File: flow_next/crm/migrations/migrate_leads.py

def execute():
    # Update old leads with new custom fields
    leads = frappe.get_all("Lead", fields=["name"])

    for lead in leads:
        doc = frappe.get_doc("Lead", lead.name)

        # Set default values for new custom fields
        if not doc.custom_date_received:
            doc.custom_date_received = doc.creation.date()

        if not doc.custom_total_interactions:
            doc.custom_total_interactions = 0

        doc.save()
```

---

## Rollback Plan

**Scenario:** Critical bug found post-deployment

**Steps:**
1. Stop application services: `sudo supervisorctl stop all`
2. Restore database backup: `bench --site [site] restore /path/to/backup.sql.gz`
3. Revert code to previous version: `git checkout [previous-tag] && bench update --patch`
4. Restart services: `sudo supervisorctl start all`
5. Verify system functionality
6. Notify users of rollback

**Backup Strategy:**
- Automated daily backups: `bench --site [site] backup --with-files`
- Retention: Keep 30 days
- Test restore quarterly

---

**Estimated Total Effort:** 24.5 days (1 developer) = **5 weeks**
**Estimated with Team:** 3-4 weeks (1 Backend + 1 Frontend developer)

**Confidence Level:** High (based on clear requirements and standard ERPNext patterns)
