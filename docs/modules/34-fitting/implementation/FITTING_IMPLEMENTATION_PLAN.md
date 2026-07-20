# Fitting Module - Implementation Plan

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1, 5.2.2, 5.4, 5.5, 14.2
**Ngày tạo:** 2026-01-24
**Trạng thái:** Draft

---

## 1. Implementation Overview

### 1.1 Scope
Triển khai đầy đủ module Fitting với 13 Use Cases theo spec khách hàng.

### 1.2 Approach
- **Backend:** Extend existing Fitting Session DocType + Create child tables
- **Frontend Option A:** Frappe Standard (List, Form, Calendar, Report)
- **Frontend Option B:** frappe-ui Vue 3 SPA (Custom pages)

### 1.3 Dependencies
- ERPNext Lead module (party linking)
- ERPNext Customer module (party linking)
- ERPNext Sales Order (order creation)
- ERPNext Item (service items)
- Frappe Event (calendar sync)

---

## 2. Implementation Tasks

### Phase 1: Core DocTypes (Days 1-4)

#### Task 1.1: Fitting Measurement DocType
**Path:** `dcnet_apps/fitting/doctype/fitting_measurement/`
**Effort:** 1 day

```json
{
  "doctype": "DocType",
  "name": "Fitting Measurement",
  "module": "Fitting",
  "istable": 1,
  "fields": [
    {"fieldname": "height", "fieldtype": "Int", "label": "Chiều cao (cm)"},
    {"fieldname": "weight", "fieldtype": "Float", "label": "Cân nặng (kg)"},
    {"fieldname": "hand_size", "fieldtype": "Select", "label": "Size tay",
     "options": "\nS\nM\nL\nXL"},
    {"fieldname": "skill_level", "fieldtype": "Select", "label": "Trình độ",
     "options": "\nNgười mới\nNgười đã chơi"},
    {"fieldname": "column_break_1", "fieldtype": "Column Break"},
    {"fieldname": "club_head_speed", "fieldtype": "Float", "label": "Tốc độ đầu gậy (mph)"},
    {"fieldname": "ball_speed", "fieldtype": "Float", "label": "Tốc độ bóng (mph)"},
    {"fieldname": "swing_shape", "fieldtype": "Small Text", "label": "Hình swing"},
    {"fieldname": "ball_flight", "fieldtype": "Select", "label": "Đường bóng",
     "options": "\nLow\nMid\nHigh"},
    {"fieldname": "ball_trajectory", "fieldtype": "Select", "label": "Đường cao bóng",
     "options": "\nStraight\nDraw\nFade\nSlice\nHook"},
    {"fieldname": "section_break_distance", "fieldtype": "Section Break", "label": "Khoảng cách"},
    {"fieldname": "iron_distance", "fieldtype": "Int", "label": "Khoảng cách sắt 7 (yards)"},
    {"fieldname": "driver_distance", "fieldtype": "Int", "label": "Khoảng cách driver (yards)"},
    {"fieldname": "section_break_notes", "fieldtype": "Section Break", "label": "Ghi chú"},
    {"fieldname": "current_club_condition", "fieldtype": "Small Text", "label": "Tình trạng bộ gậy"},
    {"fieldname": "special_requirements", "fieldtype": "Small Text", "label": "Nhu cầu riêng"},
    {"fieldname": "upgrade_recommendations", "fieldtype": "Small Text", "label": "Đề xuất nâng cấp"}
  ]
}
```

#### Task 1.2: Fitting Service DocType
**Path:** `dcnet_apps/fitting/doctype/fitting_service/`
**Effort:** 1 day

```json
{
  "doctype": "DocType",
  "name": "Fitting Service",
  "module": "Fitting",
  "istable": 1,
  "fields": [
    {"fieldname": "service_type", "fieldtype": "Select", "label": "Loại dịch vụ",
     "options": "Grip\nShaft\nCustom Club\nCombo", "reqd": 1, "in_list_view": 1},
    {"fieldname": "item", "fieldtype": "Link", "label": "Sản phẩm",
     "options": "Item", "in_list_view": 1},
    {"fieldname": "item_name", "fieldtype": "Data", "label": "Tên sản phẩm",
     "fetch_from": "item.item_name", "read_only": 1},
    {"fieldname": "quantity", "fieldtype": "Int", "label": "Số lượng",
     "default": 1, "reqd": 1, "in_list_view": 1},
    {"fieldname": "rate", "fieldtype": "Currency", "label": "Đơn giá", "in_list_view": 1},
    {"fieldname": "amount", "fieldtype": "Currency", "label": "Thành tiền",
     "read_only": 1, "in_list_view": 1},
    {"fieldname": "specs_note", "fieldtype": "Small Text", "label": "Thông số đặc biệt"}
  ]
}
```

#### Task 1.3: Update Fitting Session DocType
**Path:** `dcnet_apps/fitting/doctype/fitting_session/fitting_session.json`
**Effort:** 2 days

**New Field Order:**
```python
field_order = [
    # Section 1: Thông tin chung
    "naming_series",
    "party_type",
    "party",
    "customer_name",
    "column_break_1",
    "phone",
    "email",

    # Section 2: Lịch hẹn
    "section_break_schedule",
    "scheduled_datetime",
    "company",
    "column_break_2",
    "source",

    # Section 3: Phân công
    "section_break_assignment",
    "assigned_fitter",
    "assigned_sale",

    # Section 4: Trạng thái
    "section_break_status",
    "status",
    "column_break_3",
    "confirmed_at",
    "started_at",
    "completed_at",
    "cancelled_at",
    "cancel_reason",

    # Section 5: Thông số kỹ thuật
    "section_break_measurements",
    "measurements",

    # Section 6: Dịch vụ phát sinh
    "section_break_services",
    "services",
    "total_amount",

    # Section 7: Tích hợp
    "section_break_integration",
    "calendar_event",
    "sales_order",

    # Section 8: Notes
    "section_break_notes",
    "notes",
    "internal_notes",

    "amended_from"
]
```

**New Fields Definition:**
```json
[
  {"fieldname": "party_type", "fieldtype": "Link", "label": "Loại khách",
   "options": "DocType", "reqd": 1,
   "get_query": "return {filters: {name: ['in', ['Lead', 'Customer']]}}"},
  {"fieldname": "party", "fieldtype": "Dynamic Link", "label": "Khách hàng",
   "options": "party_type", "reqd": 1, "in_list_view": 1},
  {"fieldname": "phone", "fieldtype": "Data", "label": "SĐT", "options": "Phone"},
  {"fieldname": "email", "fieldtype": "Data", "label": "Email", "options": "Email"},

  {"fieldname": "section_break_schedule", "fieldtype": "Section Break", "label": "Lịch hẹn"},
  {"fieldname": "scheduled_datetime", "fieldtype": "Datetime", "label": "Ngày giờ hẹn",
   "reqd": 1, "in_list_view": 1},
  {"fieldname": "company", "fieldtype": "Link", "label": "Chi nhánh",
   "options": "Company", "reqd": 1},
  {"fieldname": "source", "fieldtype": "Select", "label": "Nguồn",
   "options": "\nwebsite\nphone\nwalk_in\nfacebook\nzalo"},

  {"fieldname": "section_break_assignment", "fieldtype": "Section Break", "label": "Phân công"},
  {"fieldname": "assigned_fitter", "fieldtype": "Link", "label": "NV Fitting", "options": "User"},
  {"fieldname": "assigned_sale", "fieldtype": "Link", "label": "NV Sale", "options": "User"},

  {"fieldname": "section_break_status", "fieldtype": "Section Break", "label": "Trạng thái"},
  {"fieldname": "confirmed_at", "fieldtype": "Datetime", "label": "Xác nhận lúc", "read_only": 1},
  {"fieldname": "started_at", "fieldtype": "Datetime", "label": "Bắt đầu lúc", "read_only": 1},
  {"fieldname": "completed_at", "fieldtype": "Datetime", "label": "Hoàn thành lúc", "read_only": 1},
  {"fieldname": "cancelled_at", "fieldtype": "Datetime", "label": "Hủy lúc", "read_only": 1},
  {"fieldname": "cancel_reason", "fieldtype": "Small Text", "label": "Lý do hủy"},

  {"fieldname": "section_break_services", "fieldtype": "Section Break", "label": "Dịch vụ phát sinh"},
  {"fieldname": "services", "fieldtype": "Table", "label": "Dịch vụ", "options": "Fitting Service"},
  {"fieldname": "total_amount", "fieldtype": "Currency", "label": "Tổng tiền", "read_only": 1},

  {"fieldname": "section_break_integration", "fieldtype": "Section Break",
   "label": "Tích hợp", "collapsible": 1},
  {"fieldname": "calendar_event", "fieldtype": "Link", "label": "Event",
   "options": "Event", "read_only": 1},
  {"fieldname": "sales_order", "fieldtype": "Link", "label": "Đơn hàng",
   "options": "Sales Order", "read_only": 1},

  {"fieldname": "internal_notes", "fieldtype": "Text Editor", "label": "Ghi chú nội bộ"}
]
```

**Updated Status Options:**
```
new
confirmed
in_progress
completed
has_order
follow_up
no_show
cancelled
```

---

### Phase 2: Controller & Workflow (Days 5-6)

#### Task 2.1: Fitting Session Controller
**Path:** `dcnet_apps/fitting/doctype/fitting_session/fitting_session.py`
**Effort:** 1.5 days

```python
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime

class FittingSession(Document):
    def validate(self):
        self.validate_party()
        self.set_party_info()
        self.calculate_total()
        self.validate_status_transition()

    def on_update(self):
        self.set_timestamps()
        self.sync_calendar_event()

    def on_submit(self):
        if self.status not in ["completed", "has_order", "follow_up"]:
            frappe.throw(_("Chỉ submit khi đã hoàn thành fitting"))

    def on_cancel(self):
        self.db_set("status", "cancelled")
        self.db_set("cancelled_at", now_datetime())

    def validate_party(self):
        if self.party_type not in ["Lead", "Customer"]:
            frappe.throw(_("Loại khách phải là Lead hoặc Customer"))

    def set_party_info(self):
        if not self.party:
            return

        if self.party_type == "Lead":
            lead = frappe.get_doc("Lead", self.party)
            self.customer_name = lead.lead_name
            self.phone = lead.mobile_no or lead.phone
            self.email = lead.email_id
        elif self.party_type == "Customer":
            customer = frappe.get_doc("Customer", self.party)
            self.customer_name = customer.customer_name
            # Get from primary contact
            contact = frappe.db.get_value("Dynamic Link",
                {"link_doctype": "Customer", "link_name": self.party, "parenttype": "Contact"},
                "parent")
            if contact:
                contact_doc = frappe.get_doc("Contact", contact)
                self.phone = contact_doc.mobile_no or contact_doc.phone
                self.email = contact_doc.email_id

    def calculate_total(self):
        self.total_amount = sum(s.amount or 0 for s in self.services)

    def validate_status_transition(self):
        if self.is_new():
            return

        old_status = frappe.db.get_value("Fitting Session", self.name, "status")
        if not old_status or old_status == self.status:
            return

        valid_transitions = {
            "new": ["confirmed", "cancelled"],
            "confirmed": ["in_progress", "no_show", "cancelled"],
            "in_progress": ["completed", "cancelled"],
            "completed": ["has_order", "follow_up"],
            "has_order": [],
            "follow_up": ["has_order"],
            "no_show": [],
            "cancelled": []
        }

        if self.status not in valid_transitions.get(old_status, []):
            frappe.throw(_(f"Không thể chuyển từ {old_status} sang {self.status}"))

    def set_timestamps(self):
        if self.is_new():
            return

        old_status = frappe.db.get_value("Fitting Session", self.name, "status")
        if old_status == self.status:
            return

        now = now_datetime()
        if self.status == "confirmed" and not self.confirmed_at:
            self.db_set("confirmed_at", now)
        elif self.status == "in_progress" and not self.started_at:
            self.db_set("started_at", now)
        elif self.status == "completed" and not self.completed_at:
            self.db_set("completed_at", now)

    def sync_calendar_event(self):
        if not self.scheduled_datetime:
            return

        if self.calendar_event:
            # Update existing event
            event = frappe.get_doc("Event", self.calendar_event)
            event.starts_on = self.scheduled_datetime
            event.subject = f"Fitting: {self.customer_name}"
            event.save(ignore_permissions=True)
        else:
            # Create new event
            event = frappe.new_doc("Event")
            event.subject = f"Fitting: {self.customer_name}"
            event.starts_on = self.scheduled_datetime
            event.event_type = "Public"
            event.all_day = 0
            event.insert(ignore_permissions=True)
            self.db_set("calendar_event", event.name)
```

#### Task 2.2: Fitting Service Controller
**Path:** `dcnet_apps/fitting/doctype/fitting_service/fitting_service.py`
**Effort:** 0.5 day

```python
import frappe
from frappe.model.document import Document

class FittingService(Document):
    def validate(self):
        self.calculate_amount()
        self.fetch_item_rate()

    def calculate_amount(self):
        self.amount = (self.quantity or 0) * (self.rate or 0)

    def fetch_item_rate(self):
        if self.item and not self.rate:
            self.rate = frappe.db.get_value("Item Price",
                {"item_code": self.item, "selling": 1}, "price_list_rate") or 0
```

#### Task 2.3: Workflow Fixture
**Path:** `dcnet_apps/fitting/fixtures/fitting_workflow.json`
**Effort:** 0.5 day

```json
[
  {
    "doctype": "Workflow",
    "name": "Fitting Session Workflow",
    "document_type": "Fitting Session",
    "is_active": 1,
    "workflow_state_field": "status",
    "send_email_alert": 0
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "new",
    "style": "Primary"
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "confirmed",
    "style": "Info"
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "in_progress",
    "style": "Warning"
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "completed",
    "style": "Success"
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "has_order",
    "style": "Success"
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "follow_up",
    "style": "Warning"
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "no_show",
    "style": "Danger"
  },
  {
    "doctype": "Workflow State",
    "workflow_state_name": "cancelled",
    "style": "Danger"
  }
]
```

---

### Phase 3: Client Scripts & UI (Days 7-8)

#### Task 3.1: Fitting Session Client Script
**Path:** `dcnet_apps/fitting/doctype/fitting_session/fitting_session.js`
**Effort:** 1 day

```javascript
frappe.ui.form.on('Fitting Session', {
    refresh(frm) {
        frm.set_query('party_type', () => {
            return {
                filters: { name: ['in', ['Lead', 'Customer']] }
            };
        });

        // Status action buttons
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            if (frm.doc.status === 'new') {
                frm.add_custom_button(__('Xác nhận lịch'), () => {
                    frm.set_value('status', 'confirmed');
                    frm.save();
                }, __('Hành động'));

                frm.add_custom_button(__('Hủy'), () => {
                    frappe.prompt({
                        fieldname: 'reason',
                        fieldtype: 'Small Text',
                        label: 'Lý do hủy'
                    }, (values) => {
                        frm.set_value('status', 'cancelled');
                        frm.set_value('cancel_reason', values.reason);
                        frm.save();
                    }, __('Hủy đơn Fitting'));
                }, __('Hành động'));
            }

            if (frm.doc.status === 'confirmed') {
                frm.add_custom_button(__('Bắt đầu Fitting'), () => {
                    frm.set_value('status', 'in_progress');
                    frm.save();
                }, __('Hành động'));

                frm.add_custom_button(__('Vắng mặt'), () => {
                    frm.set_value('status', 'no_show');
                    frm.save();
                }, __('Hành động'));
            }

            if (frm.doc.status === 'in_progress') {
                frm.add_custom_button(__('Hoàn thành'), () => {
                    frm.set_value('status', 'completed');
                    frm.save();
                }, __('Hành động'));
            }
        }

        // Create Sales Order button
        if (frm.doc.docstatus === 1 &&
            ['completed', 'follow_up'].includes(frm.doc.status) &&
            frm.doc.services && frm.doc.services.length > 0 &&
            !frm.doc.sales_order) {
            frm.add_custom_button(__('Tạo đơn hàng'), () => {
                frappe.call({
                    method: 'dcnet_apps.fitting.api.create_sales_order',
                    args: { fitting_name: frm.doc.name },
                    callback: (r) => {
                        if (r.message) {
                            frappe.set_route('Form', 'Sales Order', r.message);
                        }
                    }
                });
            }, __('Tạo'));
        }

        // Status indicator colors
        const status_colors = {
            'new': 'blue',
            'confirmed': 'purple',
            'in_progress': 'yellow',
            'completed': 'green',
            'has_order': 'cyan',
            'follow_up': 'orange',
            'no_show': 'gray',
            'cancelled': 'red'
        };
        frm.page.set_indicator(__(frm.doc.status), status_colors[frm.doc.status] || 'gray');
    },

    party_type(frm) {
        frm.set_value('party', '');
        frm.set_value('customer_name', '');
        frm.set_value('phone', '');
        frm.set_value('email', '');
    },

    party(frm) {
        if (frm.doc.party && frm.doc.party_type) {
            frappe.call({
                method: 'dcnet_apps.fitting.api.get_party_details',
                args: {
                    party_type: frm.doc.party_type,
                    party: frm.doc.party
                },
                callback: (r) => {
                    if (r.message) {
                        frm.set_value('customer_name', r.message.name);
                        frm.set_value('phone', r.message.phone);
                        frm.set_value('email', r.message.email);
                    }
                }
            });
        }
    }
});

frappe.ui.form.on('Fitting Service', {
    item(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item) {
            frappe.db.get_value('Item Price',
                {item_code: row.item, selling: 1}, 'price_list_rate')
                .then(r => {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, 'rate', r.message.price_list_rate);
                    }
                });
        }
    },

    quantity(frm, cdt, cdn) {
        calculate_service_amount(frm, cdt, cdn);
    },

    rate(frm, cdt, cdn) {
        calculate_service_amount(frm, cdt, cdn);
    },

    services_remove(frm) {
        calculate_total(frm);
    }
});

function calculate_service_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, 'amount', (row.quantity || 0) * (row.rate || 0));
    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    (frm.doc.services || []).forEach(s => {
        total += s.amount || 0;
    });
    frm.set_value('total_amount', total);
}
```

#### Task 3.2: Calendar View Configuration
**Path:** `dcnet_apps/fitting/fitting_calendar.js`
**Effort:** 0.5 day

```javascript
frappe.views.calendar['Fitting Session'] = {
    field_map: {
        start: 'scheduled_datetime',
        end: 'scheduled_datetime',
        id: 'name',
        title: 'customer_name',
        allDay: 0
    },
    gantt: false,
    order_by: 'scheduled_datetime',
    get_events_method: 'dcnet_apps.fitting.api.get_fitting_calendar_events',
    filters: [
        {
            fieldtype: 'Link',
            fieldname: 'company',
            options: 'Company',
            label: __('Chi nhánh')
        },
        {
            fieldtype: 'Link',
            fieldname: 'assigned_fitter',
            options: 'User',
            label: __('NV Fitting')
        },
        {
            fieldtype: 'Select',
            fieldname: 'status',
            options: '\nnew\nconfirmed\nin_progress\ncompleted\nhas_order\nfollow_up\nno_show\ncancelled',
            label: __('Trạng thái')
        }
    ],
    get_css_class: function(data) {
        const classes = {
            'new': 'info',
            'confirmed': 'primary',
            'in_progress': 'warning',
            'completed': 'success',
            'has_order': 'success',
            'follow_up': 'warning',
            'no_show': 'danger',
            'cancelled': 'danger'
        };
        return classes[data.status] || '';
    }
};
```

#### Task 3.3: List View Configuration
**Path:** `dcnet_apps/fitting/doctype/fitting_session/fitting_session_list.js`
**Effort:** 0.5 day

```javascript
frappe.listview_settings['Fitting Session'] = {
    add_fields: ['status', 'scheduled_datetime', 'customer_name', 'company'],

    get_indicator: function(doc) {
        const indicators = {
            'new': [__('Mới'), 'blue', 'status,=,new'],
            'confirmed': [__('Đã xác nhận'), 'purple', 'status,=,confirmed'],
            'in_progress': [__('Đang fitting'), 'yellow', 'status,=,in_progress'],
            'completed': [__('Hoàn thành'), 'green', 'status,=,completed'],
            'has_order': [__('Có đơn hàng'), 'cyan', 'status,=,has_order'],
            'follow_up': [__('Chờ follow-up'), 'orange', 'status,=,follow_up'],
            'no_show': [__('Vắng mặt'), 'gray', 'status,=,no_show'],
            'cancelled': [__('Hủy'), 'red', 'status,=,cancelled']
        };
        return indicators[doc.status];
    },

    formatters: {
        scheduled_datetime: function(value) {
            return frappe.datetime.str_to_user(value);
        }
    },

    onload: function(listview) {
        listview.page.add_inner_button(__('Calendar'), () => {
            frappe.set_route('fitting-session', 'calendar');
        });
    }
};
```

---

### Phase 4: API Endpoints (Days 9-10)

#### Task 4.1: API Module
**Path:** `dcnet_apps/fitting/api.py`
**Effort:** 2 days

```python
import frappe
from frappe import _
from frappe.utils import now_datetime, getdate, add_days

@frappe.whitelist()
def get_party_details(party_type, party):
    """UC-01, UC-03: Get Lead/Customer details"""
    if party_type == "Lead":
        doc = frappe.get_doc("Lead", party)
        return {
            "name": doc.lead_name,
            "phone": doc.mobile_no or doc.phone,
            "email": doc.email_id
        }
    elif party_type == "Customer":
        doc = frappe.get_doc("Customer", party)
        contact = frappe.db.get_value("Dynamic Link",
            {"link_doctype": "Customer", "link_name": party, "parenttype": "Contact"},
            "parent")
        phone, email = "", ""
        if contact:
            contact_doc = frappe.get_doc("Contact", contact)
            phone = contact_doc.mobile_no or contact_doc.phone
            email = contact_doc.email_id
        return {
            "name": doc.customer_name,
            "phone": phone,
            "email": email
        }
    return {}

@frappe.whitelist()
def create_sales_order(fitting_name):
    """UC-09: Create Sales Order from Fitting Session"""
    fitting = frappe.get_doc("Fitting Session", fitting_name)

    if fitting.sales_order:
        frappe.throw(_("Đơn hàng đã được tạo: {0}").format(fitting.sales_order))

    if not fitting.services:
        frappe.throw(_("Không có dịch vụ để tạo đơn hàng"))

    # Get or create customer from Lead
    if fitting.party_type == "Lead":
        customer = convert_lead_to_customer(fitting.party)
    else:
        customer = fitting.party

    # Create Sales Order
    so = frappe.new_doc("Sales Order")
    so.customer = customer
    so.company = fitting.company
    so.delivery_date = getdate(fitting.scheduled_datetime) if fitting.scheduled_datetime else getdate()
    so.fitting_session = fitting_name  # Custom link field

    for service in fitting.services:
        so.append("items", {
            "item_code": service.item,
            "item_name": service.item_name,
            "qty": service.quantity,
            "rate": service.rate
        })

    so.insert()
    so.submit()

    # Update Fitting Session
    fitting.db_set("status", "has_order")
    fitting.db_set("sales_order", so.name)

    frappe.msgprint(_("Đã tạo đơn hàng {0}").format(so.name))
    return so.name

def convert_lead_to_customer(lead_name):
    """Convert Lead to Customer if not exists"""
    lead = frappe.get_doc("Lead", lead_name)

    # Check if already converted
    if lead.customer:
        return lead.customer

    # Check by email
    existing = frappe.db.get_value("Customer", {"email_id": lead.email_id})
    if existing:
        lead.db_set("customer", existing)
        return existing

    # Create new Customer
    customer = frappe.new_doc("Customer")
    customer.customer_name = lead.lead_name
    customer.customer_type = "Individual"
    customer.territory = lead.territory or "Vietnam"
    customer.insert()

    # Create Contact
    contact = frappe.new_doc("Contact")
    contact.first_name = lead.first_name or lead.lead_name
    contact.last_name = lead.last_name or ""
    contact.mobile_no = lead.mobile_no
    contact.phone = lead.phone
    contact.email_id = lead.email_id
    contact.append("links", {
        "link_doctype": "Customer",
        "link_name": customer.name
    })
    contact.insert()

    # Update Lead
    lead.db_set("customer", customer.name)

    return customer.name

@frappe.whitelist(allow_guest=True)
def receive_website_registration(data):
    """UC-12: Receive fitting registration from website"""
    data = frappe.parse_json(data)

    # Validate required fields
    required = ["name", "phone", "scheduled_datetime"]
    for field in required:
        if not data.get(field):
            frappe.throw(_("Thiếu thông tin: {0}").format(field))

    # Find or create Lead
    lead = None
    if data.get("email"):
        lead = frappe.db.get_value("Lead", {"email_id": data.get("email")})
    if not lead and data.get("phone"):
        lead = frappe.db.get_value("Lead", {"mobile_no": data.get("phone")})

    if not lead:
        new_lead = frappe.new_doc("Lead")
        new_lead.first_name = data.get("name")
        new_lead.lead_name = data.get("name")
        new_lead.email_id = data.get("email")
        new_lead.mobile_no = data.get("phone")
        new_lead.source = "Website"
        new_lead.insert(ignore_permissions=True)
        lead = new_lead.name

    # Create Fitting Session
    fitting = frappe.new_doc("Fitting Session")
    fitting.party_type = "Lead"
    fitting.party = lead
    fitting.scheduled_datetime = data.get("scheduled_datetime")
    fitting.source = "website"
    fitting.status = "new"
    fitting.company = frappe.defaults.get_user_default("Company") or \
                      frappe.db.get_single_value("Global Defaults", "default_company")
    fitting.notes = data.get("notes", "")
    fitting.insert(ignore_permissions=True)

    # Notify sales team
    notify_sales_team(fitting)

    return {"success": True, "fitting": fitting.name}

def notify_sales_team(fitting):
    """Send notification to sales team"""
    sales_users = frappe.get_all("Has Role",
        filters={"role": "Sales User", "parenttype": "User"},
        pluck="parent")

    for user in sales_users:
        frappe.publish_realtime("fitting_new", {
            "fitting": fitting.name,
            "customer": fitting.customer_name,
            "datetime": str(fitting.scheduled_datetime)
        }, user=user)

@frappe.whitelist()
def get_fitting_calendar_events(start, end, filters=None):
    """UC-13: Get calendar events for Fitting Sessions"""
    conditions = ["scheduled_datetime BETWEEN %s AND %s", "docstatus < 2"]
    values = [start, end]

    if filters:
        filters = frappe.parse_json(filters)
        if filters.get("company"):
            conditions.append("company = %s")
            values.append(filters["company"])
        if filters.get("assigned_fitter"):
            conditions.append("assigned_fitter = %s")
            values.append(filters["assigned_fitter"])
        if filters.get("status"):
            conditions.append("status = %s")
            values.append(filters["status"])

    events = frappe.db.sql("""
        SELECT
            name,
            customer_name as title,
            scheduled_datetime as start,
            DATE_ADD(scheduled_datetime, INTERVAL 1 HOUR) as end,
            status,
            assigned_fitter,
            company
        FROM `tabFitting Session`
        WHERE {conditions}
    """.format(conditions=" AND ".join(conditions)), values, as_dict=1)

    return events

@frappe.whitelist()
def get_dashboard_stats():
    """Dashboard statistics"""
    from frappe.utils import get_first_day, get_last_day, nowdate

    first_day = get_first_day(nowdate())
    last_day = get_last_day(nowdate())

    # Total sessions this month
    total_sessions = frappe.db.count("Fitting Session", {
        "scheduled_datetime": ["between", [first_day, last_day]],
        "docstatus": ["<", 2]
    })

    # Revenue from fitting
    revenue = frappe.db.sql("""
        SELECT SUM(total_amount) as revenue
        FROM `tabFitting Session`
        WHERE scheduled_datetime BETWEEN %s AND %s
        AND status IN ('completed', 'has_order')
    """, (first_day, last_day))[0][0] or 0

    # Conversion rate
    completed = frappe.db.count("Fitting Session", {
        "scheduled_datetime": ["between", [first_day, last_day]],
        "status": ["in", ["completed", "has_order"]]
    })
    conversion_rate = round((completed / total_sessions * 100) if total_sessions else 0, 1)

    # Pending count
    pending_count = frappe.db.count("Fitting Session", {
        "status": "new"
    })

    return {
        "total_sessions": total_sessions,
        "revenue": revenue,
        "conversion_rate": conversion_rate,
        "pending_count": pending_count
    }
```

---

### Phase 5: Reports (Days 11-13)

#### Task 5.1: Fitting Revenue Report
**Path:** `dcnet_apps/fitting/report/fitting_revenue/`
**Effort:** 0.5 day

```python
# fitting_revenue.py
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"fieldname": "date", "label": _("Ngày"), "fieldtype": "Date", "width": 120},
        {"fieldname": "fitting_count", "label": _("Số buổi"), "fieldtype": "Int", "width": 100},
        {"fieldname": "service_revenue", "label": _("Dịch vụ"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "order_count", "label": _("Đơn hàng"), "fieldtype": "Int", "width": 100},
        {"fieldname": "order_revenue", "label": _("Doanh thu ĐH"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "total", "label": _("Tổng"), "fieldtype": "Currency", "width": 140}
    ]

def get_data(filters):
    return frappe.db.sql("""
        SELECT
            DATE(fs.scheduled_datetime) as date,
            COUNT(DISTINCT fs.name) as fitting_count,
            SUM(fs.total_amount) as service_revenue,
            COUNT(DISTINCT fs.sales_order) as order_count,
            SUM(CASE WHEN so.name IS NOT NULL THEN so.grand_total ELSE 0 END) as order_revenue,
            SUM(fs.total_amount) + SUM(CASE WHEN so.name IS NOT NULL THEN so.grand_total ELSE 0 END) as total
        FROM `tabFitting Session` fs
        LEFT JOIN `tabSales Order` so ON fs.sales_order = so.name
        WHERE fs.status IN ('completed', 'has_order')
        AND fs.scheduled_datetime BETWEEN %(from_date)s AND %(to_date)s
        {company_filter}
        GROUP BY DATE(fs.scheduled_datetime)
        ORDER BY date
    """.format(
        company_filter="AND fs.company = %(company)s" if filters.get("company") else ""
    ), filters, as_dict=1)

def get_chart(data):
    return {
        "data": {
            "labels": [d.date.strftime("%d/%m") for d in data],
            "datasets": [
                {"name": _("Dịch vụ"), "values": [d.service_revenue or 0 for d in data]},
                {"name": _("Đơn hàng"), "values": [d.order_revenue or 0 for d in data]}
            ]
        },
        "type": "bar"
    }
```

#### Task 5.2: Other Reports
**Effort:** 2.5 days for remaining 4 reports

1. `fitting_sessions_monthly` - Số buổi fitting theo tháng
2. `fitting_customer_count` - Số khách đến fitting
3. `fitting_accessories_usage` - Linh kiện sử dụng (grip, shaft)
4. `fitting_staff_performance` - Hiệu suất NV fitting

---

### Phase 6: Roles & Permissions (Day 14)

#### Task 6.1: Custom Roles
**Path:** `dcnet_apps/fitting/fixtures/custom_role.json`

```json
[
    {
        "doctype": "Role",
        "role_name": "Fitting User",
        "desk_access": 1,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "role_name": "Fitting Manager",
        "desk_access": 1,
        "is_custom": 1
    }
]
```

#### Task 6.2: DocType Permissions
**Update:** `fitting_session.json` permissions

```json
{
    "permissions": [
        {"role": "Fitting User", "read": 1, "write": 1, "create": 1, "if_owner": 1},
        {"role": "Fitting Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
        {"role": "Sales User", "read": 1, "write": 1, "create": 1, "submit": 1},
        {"role": "Sales Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
        {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1}
    ]
}
```

---

### Phase 7: Option B - frappe-ui Pages (Days 15-19)

#### Task 7.1: Setup Vue Project
**Effort:** 1 day

```bash
# package.json
{
    "name": "fitting-ui",
    "private": true,
    "scripts": {
        "dev": "vite",
        "build": "vite build"
    },
    "dependencies": {
        "vue": "^3.4.0",
        "vue-router": "^4.2.0",
        "frappe-ui": "^0.1.0"
    },
    "devDependencies": {
        "@vitejs/plugin-vue": "^5.0.0",
        "vite": "^5.0.0",
        "tailwindcss": "^3.4.0",
        "autoprefixer": "^10.4.0"
    }
}
```

#### Task 7.2: Vue Components
**Effort:** 4 days

| Component | Description | Effort |
|-----------|-------------|--------|
| FittingListView.vue | Danh sách + filters | 1 day |
| FittingDetailView.vue | Chi tiết với tabs | 1 day |
| FittingCalendar.vue | Calendar view | 1 day |
| FittingDashboard.vue | Dashboard + charts | 1 day |

---

### Phase 8: Testing & QA (Days 20-22)

#### Task 8.1: Unit Tests
**Path:** `dcnet_apps/fitting/doctype/fitting_session/test_fitting_session.py`

```python
import frappe
import unittest

class TestFittingSession(unittest.TestCase):
    def setUp(self):
        self.lead = make_test_lead()

    def test_create_fitting_with_lead(self):
        fitting = create_fitting_session(party_type="Lead", party=self.lead.name)
        self.assertEqual(fitting.party_type, "Lead")
        self.assertEqual(fitting.customer_name, self.lead.lead_name)

    def test_status_transition(self):
        fitting = create_fitting_session()
        fitting.status = "confirmed"
        fitting.save()
        self.assertEqual(fitting.status, "confirmed")
        self.assertIsNotNone(fitting.confirmed_at)

    def test_invalid_status_transition(self):
        fitting = create_fitting_session()
        fitting.status = "completed"  # Skip confirmed, in_progress
        self.assertRaises(frappe.ValidationError, fitting.save)

    def test_create_sales_order(self):
        fitting = create_fitting_with_services()
        fitting.status = "completed"
        fitting.save()
        fitting.submit()

        so_name = create_sales_order(fitting.name)
        self.assertIsNotNone(so_name)

        fitting.reload()
        self.assertEqual(fitting.status, "has_order")
        self.assertEqual(fitting.sales_order, so_name)
```

---

## 3. File Structure Summary

```
dcnet_apps/dcnet_apps/fitting/
├── __init__.py
├── api.py                              # Whitelist methods
├── hooks.py                            # Module hooks
├── fitting_calendar.js                 # Calendar view config
│
├── doctype/
│   ├── fitting_session/
│   │   ├── fitting_session.json        # Updated DocType
│   │   ├── fitting_session.py          # Controller
│   │   ├── fitting_session.js          # Client script
│   │   ├── fitting_session_list.js     # List view config
│   │   └── test_fitting_session.py     # Unit tests
│   ├── fitting_measurement/
│   │   ├── fitting_measurement.json    # NEW child table
│   │   └── fitting_measurement.py
│   └── fitting_service/
│       ├── fitting_service.json        # NEW child table
│       └── fitting_service.py
│
├── report/
│   ├── fitting_revenue/
│   │   ├── fitting_revenue.json
│   │   └── fitting_revenue.py
│   ├── fitting_sessions_monthly/
│   ├── fitting_customer_count/
│   ├── fitting_accessories_usage/
│   └── fitting_staff_performance/
│
├── fixtures/
│   ├── fitting_workflow.json
│   └── custom_role.json
│
├── www/                                # Option B: frappe-ui
│   └── fitting.html
│
├── src/                                # Option B: Vue source
│   ├── main.js
│   ├── router.js
│   ├── App.vue
│   └── views/
│       ├── FittingListView.vue
│       ├── FittingDetailView.vue
│       ├── FittingCalendar.vue
│       └── FittingDashboard.vue
│
├── package.json
└── vite.config.js
```

---

## 4. Critical Dependencies

| Dependency | Required For | Priority |
|------------|--------------|----------|
| ERPNext Lead | Party linking | Critical |
| ERPNext Customer | Party linking | Critical |
| ERPNext Sales Order | Order creation | Critical |
| ERPNext Item | Service items | High |
| Frappe Event | Calendar sync | Medium |
| frappe-ui | Option B UI | Optional |

---

## 5. Verification Checklist

### Pre-Implementation
- [ ] ERPNext Lead module available
- [ ] ERPNext Sales Order module available
- [ ] frappe-ui installed (for Option B)

### Post-Implementation
- [ ] All 13 Use Cases functional
- [ ] 8 status transitions working
- [ ] Calendar view displaying correctly
- [ ] Sales Order creation working
- [ ] Website API accepting registrations
- [ ] 5 reports generating data
- [ ] Permissions enforced correctly

---

**Next:** [FITTING_TIMELINE.md](./FITTING_TIMELINE.md)
