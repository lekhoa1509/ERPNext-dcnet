# UI Implementation: Fitting Module

> **Module:** Fitting Session Management
> **UI Approach:** Frappe Desk
> **Analysis Date:** 2026-01-24

---

## UI Approach Decision

### Selected Approach: Frappe Desk

| Criteria | Frappe Desk | Frappe UI |
|----------|-------------|-----------|
| **Development Speed** | ✅ Fast | Slower |
| **Workflow Actions** | ✅ Native support | Custom build |
| **Calendar View** | ✅ Built-in | Custom component |
| **ERPNext Integration** | ✅ Native (Sales Order) | API bridge |
| **Reports** | ✅ Query Report | Custom charts |

**Rationale:**
- Fitting Session là custom DocType cần tích hợp sâu với ERPNext (Sales Order, Customer)
- 8-state workflow cần native Workflow Actions (buttons tự động theo trạng thái)
- Calendar View có sẵn trong Frappe, chỉ cần config
- Reports dùng Query Report pattern có sẵn
- Gap Analysis recommend: "Option A First - Frappe Standard trước"

**Skill Reference:** `frappe` (Form API, List API, Workflow, Calendar View)

---

## Screen Inventory

| # | Screen | Type | Priority | Complexity | UC Coverage |
|---|--------|------|----------|------------|-------------|
| 1 | Fitting Session List | List View | High | Medium | UC-02 |
| 2 | Fitting Session Form | Form View | High | High | UC-01,03,04,05,06,07,08,10 |
| 3 | Fitting Calendar | Calendar View | High | Low | UC-13 |
| 4 | Create Sales Order Dialog | Dialog | High | Medium | UC-09 |
| 5 | Fitting Reports | Script Reports | Medium | Medium | UC-11 |

---

## Frappe Desk Implementation

### 1. List View Customization

**File:** `dcnet_apps/dcnet_apps/fitting/doctype/fitting_session/fitting_session_list.js`

```javascript
frappe.listview_settings['Fitting Session'] = {
    add_fields: ['status', 'party_type', 'party_name', 'scheduled_datetime',
                 'assigned_fitter', 'company', 'total_amount'],

    get_indicator(doc) {
        const status_map = {
            'new': ['New', 'blue'],
            'confirmed': ['Confirmed', 'cyan'],
            'in_progress': ['In Progress', 'orange'],
            'completed': ['Completed', 'green'],
            'has_order': ['Has Order', 'purple'],
            'follow_up': ['Follow Up', 'yellow'],
            'no_show': ['No Show', 'grey'],
            'cancelled': ['Cancelled', 'red']
        };
        const [label, color] = status_map[doc.status] || ['Unknown', 'grey'];
        return [__(label), color, `status,=,${doc.status}`];
    },

    filters: [['status', 'not in', ['cancelled', 'no_show']]],

    onload(listview) {
        // Quick filter buttons
        listview.page.add_inner_button(__('Today'), () => {
            const today = frappe.datetime.get_today();
            listview.filter_area.clear();
            listview.filter_area.add([
                [listview.doctype, 'scheduled_datetime', 'like', `${today}%`]
            ]);
        });

        listview.page.add_inner_button(__('This Week'), () => {
            const start = frappe.datetime.week_start();
            const end = frappe.datetime.week_end();
            listview.filter_area.clear();
            listview.filter_area.add([
                [listview.doctype, 'scheduled_datetime', 'between', [start, end]]
            ]);
        });

        listview.page.add_inner_button(__('My Sessions'), () => {
            listview.filter_area.add([
                [listview.doctype, 'assigned_fitter', '=', frappe.session.user]
            ]);
        });

        // Calendar view shortcut
        listview.page.add_inner_button(__('Calendar View'), () => {
            frappe.set_route('List', 'Fitting Session', 'Calendar');
        }, __('View'));
    },

    formatters: {
        scheduled_datetime(value) {
            if (!value) return '';
            const datetime = frappe.datetime.str_to_obj(value);
            const today = frappe.datetime.get_today();
            const dateStr = frappe.datetime.obj_to_str(datetime).split(' ')[0];

            if (dateStr === today) {
                return `<span class="text-primary font-weight-bold">Today ${frappe.datetime.get_time(value)}</span>`;
            }
            return frappe.datetime.prettyDate(value);
        },

        total_amount(value) {
            if (!value) return '';
            return frappe.format(value, { fieldtype: 'Currency' });
        }
    }
};
```

**Effort:** 1 day

---

### 2. Form Customization

**File:** `dcnet_apps/dcnet_apps/fitting/doctype/fitting_session/fitting_session.js`

```javascript
frappe.ui.form.on('Fitting Session', {
    setup(frm) {
        // Party type filter
        frm.set_query('party', () => {
            if (frm.doc.party_type === 'Lead') {
                return { filters: { status: ['not in', ['Converted', 'Do Not Contact']] } };
            }
            return { filters: { disabled: 0 } };
        });

        // Fitter filter - only fitting staff
        frm.set_query('assigned_fitter', () => ({
            filters: {
                enabled: 1,
                user_type: 'System User',
                // Có thể thêm role filter nếu có role "Fitter"
            }
        }));

        // Item filter for services
        frm.set_query('item', 'services', () => ({
            filters: {
                item_group: ['in', ['Grip', 'Shaft', 'Golf Club', 'Fitting Service']],
                disabled: 0
            }
        }));
    },

    refresh(frm) {
        // === WORKFLOW ACTION BUTTONS ===
        // Buttons tự động hiển thị theo status nhờ Workflow

        if (frm.is_new()) return;

        // Dashboard indicators
        frm.dashboard.add_indicator(
            __('Services: {0}', [frm.doc.services?.length || 0]),
            frm.doc.services?.length > 0 ? 'green' : 'grey'
        );

        if (frm.doc.total_amount) {
            frm.dashboard.add_indicator(
                format_currency(frm.doc.total_amount),
                'blue'
            );
        }

        // === CUSTOM BUTTONS (ngoài workflow) ===

        // Create Sales Order - chỉ khi completed và chưa có SO
        if (frm.doc.status === 'completed' && !frm.doc.sales_order && frm.doc.services?.length > 0) {
            frm.add_custom_button(__('Create Sales Order'), () => {
                create_sales_order(frm);
            }).addClass('btn-primary');
        }

        // View linked Sales Order
        if (frm.doc.sales_order) {
            frm.add_custom_button(__('View Sales Order'), () => {
                frappe.set_route('Form', 'Sales Order', frm.doc.sales_order);
            }, __('Links'));
        }

        // View in Calendar
        frm.add_custom_button(__('View in Calendar'), () => {
            frappe.set_route('List', 'Fitting Session', 'Calendar', {
                scheduled_datetime: frm.doc.scheduled_datetime
            });
        }, __('View'));

        // Quick measurement entry
        if (['confirmed', 'in_progress'].includes(frm.doc.status)) {
            frm.add_custom_button(__('Quick Measurement'), () => {
                show_measurement_dialog(frm);
            }, __('Actions'));
        }

        // Add service
        if (['in_progress', 'completed'].includes(frm.doc.status)) {
            frm.add_custom_button(__('Add Service'), () => {
                show_add_service_dialog(frm);
            }, __('Actions'));
        }

        // Status intro messages
        set_status_intro(frm);
    },

    party_type(frm) {
        frm.set_value('party', '');
        frm.set_value('party_name', '');
    },

    party(frm) {
        if (frm.doc.party && frm.doc.party_type) {
            frappe.db.get_value(frm.doc.party_type, frm.doc.party,
                ['customer_name', 'lead_name', 'phone', 'email_id', 'mobile_no'],
                (r) => {
                    if (r) {
                        frm.set_value('party_name', r.customer_name || r.lead_name || '');
                        frm.set_value('phone', r.phone || r.mobile_no || '');
                        frm.set_value('email', r.email_id || '');
                    }
                }
            );
        }
    },

    validate(frm) {
        // Validate scheduled datetime is in future for new sessions
        if (frm.doc.status === 'new' && frm.doc.scheduled_datetime) {
            if (frappe.datetime.get_diff(frm.doc.scheduled_datetime, frappe.datetime.now_datetime()) < 0) {
                frappe.msgprint(__('Scheduled datetime should be in the future'));
            }
        }

        // Calculate total amount
        calculate_total(frm);
    }
});

// === Child Table: Fitting Service ===
frappe.ui.form.on('Fitting Service', {
    item(frm, cdt, cdn) {
        const row = frappe.get_doc(cdt, cdn);
        if (row.item) {
            frappe.db.get_value('Item', row.item, ['item_name', 'standard_rate'], (r) => {
                if (r) {
                    frappe.model.set_value(cdt, cdn, 'item_name', r.item_name);
                    frappe.model.set_value(cdt, cdn, 'rate', r.standard_rate || 0);
                }
            });
        }
    },

    quantity(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },

    rate(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },

    services_remove(frm) {
        calculate_total(frm);
    }
});

// === Helper Functions ===

function calculate_row_amount(frm, cdt, cdn) {
    const row = frappe.get_doc(cdt, cdn);
    const amount = (row.quantity || 0) * (row.rate || 0);
    frappe.model.set_value(cdt, cdn, 'amount', amount);
    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    (frm.doc.services || []).forEach(row => {
        total += row.amount || 0;
    });
    frm.set_value('total_amount', total);
}

function set_status_intro(frm) {
    const intros = {
        'new': { msg: __('New fitting request - Please confirm the appointment'), color: 'blue' },
        'confirmed': { msg: __('Appointment confirmed - Ready for fitting session'), color: 'green' },
        'in_progress': { msg: __('Fitting in progress - Enter measurements and services'), color: 'orange' },
        'completed': { msg: __('Fitting completed - Create Sales Order if needed'), color: 'green' },
        'follow_up': { msg: __('Follow up required - Contact customer'), color: 'yellow' },
        'no_show': { msg: __('Customer did not show up'), color: 'grey' },
        'cancelled': { msg: __('Session was cancelled'), color: 'red' }
    };

    const intro = intros[frm.doc.status];
    if (intro) {
        frm.set_intro(intro.msg, intro.color);
    }
}

function show_measurement_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __('Quick Measurement Entry'),
        size: 'large',
        fields: [
            { fieldtype: 'Column Break' },
            { fieldname: 'height', fieldtype: 'Int', label: __('Height (cm)'), default: frm.doc.height },
            { fieldname: 'weight', fieldtype: 'Float', label: __('Weight (kg)'), default: frm.doc.weight },
            { fieldname: 'hand_size', fieldtype: 'Select', label: __('Hand Size'),
              options: '\nS\nM\nL\nXL', default: frm.doc.hand_size },
            { fieldname: 'skill_level', fieldtype: 'Select', label: __('Skill Level'),
              options: '\nBeginner\nIntermediate\nAdvanced', default: frm.doc.skill_level },
            { fieldtype: 'Column Break' },
            { fieldname: 'club_head_speed', fieldtype: 'Float', label: __('Club Head Speed'), default: frm.doc.club_head_speed },
            { fieldname: 'ball_speed', fieldtype: 'Float', label: __('Ball Speed'), default: frm.doc.ball_speed },
            { fieldname: 'ball_flight', fieldtype: 'Select', label: __('Ball Flight'),
              options: '\nLow\nMid\nHigh', default: frm.doc.ball_flight },
            { fieldtype: 'Section Break' },
            { fieldname: 'upgrade_recommendations', fieldtype: 'Text', label: __('Upgrade Recommendations'),
              default: frm.doc.upgrade_recommendations }
        ],
        primary_action_label: __('Save'),
        primary_action(values) {
            Object.keys(values).forEach(key => {
                if (values[key] !== undefined) {
                    frm.set_value(key, values[key]);
                }
            });
            frm.dirty();
            d.hide();
            frappe.show_alert({ message: __('Measurements updated'), indicator: 'green' });
        }
    });
    d.show();
}

function show_add_service_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __('Add Service'),
        fields: [
            { fieldname: 'service_type', fieldtype: 'Select', label: __('Service Type'),
              options: 'Grip Replacement\nShaft Replacement\nCustom Club\nCombo Package\nOther', reqd: 1 },
            { fieldname: 'item', fieldtype: 'Link', label: __('Item'), options: 'Item',
              get_query: () => ({
                  filters: { item_group: ['in', ['Grip', 'Shaft', 'Golf Club', 'Fitting Service']] }
              })
            },
            { fieldname: 'quantity', fieldtype: 'Int', label: __('Quantity'), default: 1 },
            { fieldname: 'rate', fieldtype: 'Currency', label: __('Rate') },
            { fieldname: 'specs_note', fieldtype: 'Small Text', label: __('Specifications') }
        ],
        primary_action_label: __('Add'),
        primary_action(values) {
            const row = frm.add_child('services', {
                service_type: values.service_type,
                item: values.item,
                quantity: values.quantity || 1,
                rate: values.rate || 0,
                amount: (values.quantity || 1) * (values.rate || 0),
                specs_note: values.specs_note
            });
            frm.refresh_field('services');
            calculate_total(frm);
            frm.dirty();
            d.hide();
            frappe.show_alert({ message: __('Service added'), indicator: 'green' });
        }
    });

    // Auto-fill rate when item selected
    d.fields_dict.item.$input.on('change', () => {
        const item = d.get_value('item');
        if (item) {
            frappe.db.get_value('Item', item, ['item_name', 'standard_rate'], (r) => {
                if (r) {
                    d.set_value('rate', r.standard_rate || 0);
                }
            });
        }
    });

    d.show();
}

function create_sales_order(frm) {
    frappe.confirm(
        __('Create Sales Order from this Fitting Session?'),
        () => {
            frappe.call({
                method: 'dcnet_apps.fitting.api.fitting_session.create_sales_order',
                args: { fitting_session: frm.doc.name },
                freeze: true,
                freeze_message: __('Creating Sales Order...'),
                callback: (r) => {
                    if (r.message) {
                        frm.reload_doc();
                        frappe.set_route('Form', 'Sales Order', r.message);
                    }
                }
            });
        }
    );
}
```

**Effort:** 3 days

---

### 3. Calendar View Configuration

**File:** `dcnet_apps/dcnet_apps/fitting/doctype/fitting_session/fitting_session_calendar.js`

```javascript
frappe.views.calendar['Fitting Session'] = {
    field_map: {
        start: 'scheduled_datetime',
        end: 'scheduled_datetime',
        id: 'name',
        title: 'party_name',
        allDay: 0
    },

    gantt: false,

    filters: [
        {
            fieldtype: 'Link',
            fieldname: 'assigned_fitter',
            options: 'User',
            label: __('Fitter')
        },
        {
            fieldtype: 'Link',
            fieldname: 'company',
            options: 'Company',
            label: __('Company')
        },
        {
            fieldtype: 'Select',
            fieldname: 'status',
            options: '\nnew\nconfirmed\nin_progress\ncompleted',
            label: __('Status')
        }
    ],

    get_events_method: 'dcnet_apps.fitting.api.fitting_session.get_calendar_events',

    get_css_class(data) {
        const status_colors = {
            'new': 'info',
            'confirmed': 'success',
            'in_progress': 'warning',
            'completed': 'primary',
            'no_show': 'secondary',
            'cancelled': 'danger'
        };
        return status_colors[data.status] || 'secondary';
    }
};
```

**Effort:** 0.5 day

---

### 4. Dashboard Configuration

**File:** `dcnet_apps/dcnet_apps/fitting/doctype/fitting_session/fitting_session_dashboard.py`

```python
from frappe import _

def get_data():
    return {
        'heatmap': True,
        'heatmap_message': _('Fitting sessions over time'),
        'fieldname': 'fitting_session',
        'non_standard_fieldnames': {
            'Sales Order': 'custom_fitting_session'
        },
        'transactions': [
            {
                'label': _('Sales'),
                'items': ['Sales Order', 'Sales Invoice']
            },
            {
                'label': _('Related'),
                'items': ['Event']
            }
        ],
        'reports': [
            {
                'label': _('Reports'),
                'items': ['Fitting Revenue Report', 'Fitting Staff Performance']
            }
        ]
    }
```

**Effort:** 0.5 day

---

### 5. Workflow Configuration

**File:** `dcnet_apps/dcnet_apps/fitting/fixtures/workflow.json`

Workflow tự động hiển thị action buttons trên form dựa trên trạng thái:

| Current Status | Actions Available | Next Status |
|----------------|-------------------|-------------|
| new | Confirm, Cancel | confirmed, cancelled |
| confirmed | Start Session, No Show, Cancel | in_progress, no_show, cancelled |
| in_progress | Complete, Cancel | completed, cancelled |
| completed | Create Order, Follow Up | has_order, follow_up |
| follow_up | Create Order, Close | has_order, completed |

**Effort:** 1 day (included in backend)

---

## Implementation Tasks Summary

| Task | File | Effort | Priority |
|------|------|--------|----------|
| List View Script | `fitting_session_list.js` | 1 day | High |
| Form Script | `fitting_session.js` | 3 days | High |
| Calendar View | `fitting_session_calendar.js` | 0.5 day | High |
| Dashboard Config | `fitting_session_dashboard.py` | 0.5 day | Medium |
| Measurement Dialog | (in form script) | - | High |
| Add Service Dialog | (in form script) | - | High |
| Create SO Dialog | (in form script) | - | High |

**Total UI Effort:** 5 days

---

## Form Layout Design

### Section 1: Customer Information
```
[party_type] [party] [party_name]
[phone]      [email]
```

### Section 2: Appointment
```
[scheduled_datetime] [company]  [source]
[assigned_fitter]    [assigned_sale]
```

### Section 3: Status (read-only timestamps)
```
[status]       [confirmed_at]
[started_at]   [completed_at]
```

### Section 4: Measurements (Tab)
```
[height]  [weight]  [hand_size]  [skill_level]
[club_head_speed]   [ball_speed] [ball_flight]
[current_club_condition]
[special_requirements]
[upgrade_recommendations]
```

### Section 5: Services (Tab - Child Table)
```
[services table: service_type | item | quantity | rate | amount | specs_note]
[total_amount]
```

### Section 6: Notes (Tab)
```
[notes]
[internal_notes]
```

### Section 7: Links (Tab)
```
[sales_order] [calendar_event]
```

---

## Notes

- **Workflow Actions:** Frappe tự động render buttons theo workflow state - không cần code thêm
- **Calendar:** Sử dụng Frappe Calendar View có sẵn, chỉ config field mapping
- **Reports:** Dùng Query Report pattern - không cần custom UI
- **Future:** Nếu cần dashboard analytics phức tạp, có thể thêm Frappe UI page sau

---

**Next Steps:**
1. Update Fitting Session DocType với đầy đủ fields
2. Create Fitting Measurement fields (inline, không cần child table)
3. Create Fitting Service child DocType
4. Implement Workflow fixture
5. Implement form script với dialogs
6. Configure Calendar View
7. Test workflow transitions
