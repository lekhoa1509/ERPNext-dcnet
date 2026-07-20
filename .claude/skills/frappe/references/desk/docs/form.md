# Frappe Desk Form API

JavaScript API for customizing DocType forms in Frappe Desk.

## Table of Contents

- [Form Events](#form-events)
- [Form Methods](#form-methods)
- [Field Manipulation](#field-manipulation)
- [Custom Buttons](#custom-buttons)
- [Server Calls](#server-calls)
- [Client Scripts](#client-scripts)

---

## Form Events

### Standard Form Script

Located in `{app}/{module}/doctype/{doctype}/{doctype}.js`:

```javascript
frappe.ui.form.on('Lead', {
    // Form lifecycle events
    setup(frm) {
        // Called once when form is created
    },

    onload(frm) {
        // Called when form loads
    },

    refresh(frm) {
        // Called on every refresh
    },

    validate(frm) {
        // Before save validation
        // Return false to prevent save
    },

    before_save(frm) {
        // Just before save
    },

    after_save(frm) {
        // After successful save
    },

    before_submit(frm) {
        // Before document submission
    },

    on_submit(frm) {
        // After submission
    },

    before_cancel(frm) {
        // Before cancellation
    },

    after_cancel(frm) {
        // After cancellation
    },

    // Field change events
    status(frm) {
        // When 'status' field changes
    },

    customer(frm) {
        // When 'customer' field changes
    }
});
```

### Child Table Events

```javascript
frappe.ui.form.on('Lead', {
    // Child table row added
    items_add(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        // Initialize row
    },

    // Child table row removed
    items_remove(frm, cdt, cdn) {
        // Recalculate totals
    },

    // Child table row moved
    items_move(frm, cdt, cdn) {
        // Handle reordering
    }
});

// Events on child table fields
frappe.ui.form.on('Lead Item', {
    item(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        // Handle item change
    },

    qty(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.amount = row.qty * row.rate;
        frm.refresh_field('items');
    }
});
```

---

## Form Methods

### Get/Set Values

```javascript
// Get field value
let status = frm.doc.status;
let value = frm.get_value('fieldname');

// Set field value
frm.set_value('status', 'Converted');

// Set multiple values
frm.set_value({
    status: 'Converted',
    converted_by: frappe.session.user
});

// For child tables
frm.doc.items[0].qty = 10;
frm.refresh_field('items');
```

### Form State

```javascript
// Check states
frm.is_new()        // New unsaved document
frm.is_dirty()      // Has unsaved changes
frm.doc.docstatus   // 0=Draft, 1=Submitted, 2=Cancelled

// Save document
frm.save();
frm.save('Submit');
frm.save('Cancel');
frm.save('Update');

// Reload from server
frm.reload_doc();
```

### Child Table Operations

```javascript
// Add row
let row = frm.add_child('items', {
    item: 'ITEM-001',
    qty: 1,
    rate: 100
});
frm.refresh_field('items');

// Clear table
frm.clear_table('items');
frm.refresh_field('items');

// Get rows
let items = frm.doc.items;
let row = frm.doc.items[0];

// Remove row (by index)
frm.doc.items.splice(0, 1);
frm.refresh_field('items');
```

---

## Field Manipulation

### Show/Hide Fields

```javascript
// Single field
frm.toggle_display('fieldname', true);  // show
frm.toggle_display('fieldname', false); // hide

// Multiple fields
frm.toggle_display(['field1', 'field2'], condition);

// Set hidden property
frm.set_df_property('fieldname', 'hidden', 1);
```

### Required Fields

```javascript
// Make required
frm.toggle_reqd('fieldname', true);
frm.toggle_reqd(['field1', 'field2'], true);

// Set reqd property
frm.set_df_property('fieldname', 'reqd', 1);
```

### Read-Only Fields

```javascript
// Make read-only
frm.toggle_enable('fieldname', false);

// Set read_only property
frm.set_df_property('fieldname', 'read_only', 1);
```

### Field Properties

```javascript
// Set any field property
frm.set_df_property('fieldname', 'label', 'New Label');
frm.set_df_property('fieldname', 'options', 'Option1\nOption2');
frm.set_df_property('fieldname', 'description', 'Help text');
frm.set_df_property('fieldname', 'placeholder', 'Enter value');

// Refresh field after property change
frm.refresh_field('fieldname');
```

### Link Field Filters

```javascript
// Set query filter for Link field
frm.set_query('customer', () => {
    return {
        filters: {
            disabled: 0,
            territory: frm.doc.territory
        }
    };
});

// For Link in child table
frm.set_query('item', 'items', () => {
    return {
        filters: {
            is_sales_item: 1
        }
    };
});

// With custom query
frm.set_query('customer', () => {
    return {
        query: 'erpnext.controllers.queries.customer_query',
        filters: { territory: frm.doc.territory }
    };
});
```

---

## Custom Buttons

### Primary Action

```javascript
frm.page.set_primary_action('Save & Submit', () => {
    frm.save('Submit');
});
```

### Custom Buttons

```javascript
// Add button to toolbar
frm.add_custom_button('Send Email', () => {
    // action
});

// Button in group
frm.add_custom_button('Create Invoice', () => {
    // action
}, 'Create');

frm.add_custom_button('Create Delivery', () => {
    // action
}, 'Create');

// Remove button
frm.remove_custom_button('Send Email');
frm.remove_custom_button('Create Invoice', 'Create');

// Change button type
frm.change_custom_button_type('Send Email', null, 'primary');
```

### Conditional Buttons

```javascript
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        // Only show for submitted documents
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button('Create Invoice', () => {
                frappe.model.open_mapped_doc({
                    method: 'erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice',
                    frm: frm
                });
            }, 'Create');
        }
    }
});
```

---

## Server Calls

### frappe.call

```javascript
frappe.call({
    method: 'frappe.client.get_value',
    args: {
        doctype: 'Customer',
        filters: { name: frm.doc.customer },
        fieldname: ['customer_name', 'territory']
    },
    callback: (r) => {
        if (r.message) {
            frm.set_value('customer_name', r.message.customer_name);
        }
    }
});
```

### frappe.db Methods

```javascript
// Get document
frappe.db.get_doc('Customer', 'CUST-001')
    .then(doc => console.log(doc));

// Get list
frappe.db.get_list('Customer', {
    fields: ['name', 'customer_name'],
    filters: { territory: 'Vietnam' },
    limit: 20
}).then(customers => console.log(customers));

// Get single value
frappe.db.get_value('Customer', 'CUST-001', 'customer_name')
    .then(r => console.log(r.message.customer_name));

// Set value
frappe.db.set_value('Customer', 'CUST-001', 'territory', 'Vietnam');

// Insert document
frappe.db.insert({
    doctype: 'Customer',
    customer_name: 'New Customer',
    territory: 'Vietnam'
}).then(doc => console.log(doc));

// Check exists
frappe.db.exists('Customer', 'CUST-001')
    .then(exists => console.log(exists));

// Count
frappe.db.count('Customer', { territory: 'Vietnam' })
    .then(count => console.log(count));
```

### Call DocType Method

```javascript
// Call whitelisted method on document
frm.call({
    method: 'custom_method',
    args: { param1: 'value' },
    callback: (r) => {
        console.log(r.message);
    }
});

// Or directly
frm.call('custom_method', { param1: 'value' })
    .then(r => console.log(r.message));
```

---

## Client Scripts

### Creating via UI

1. Go to **Home > Customization > Client Script**
2. Create new with:
   - **DocType**: Target DocType
   - **Script**: JavaScript code
   - **Enabled**: Check to activate

### Client Script Example

```javascript
// Client Script for Sales Order
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        // Add custom validations
        if (frm.doc.grand_total > 100000) {
            frm.dashboard.add_comment(
                'This is a high-value order',
                'yellow'
            );
        }
    },

    customer(frm) {
        // Fetch customer details
        if (frm.doc.customer) {
            frappe.db.get_value('Customer', frm.doc.customer, 'territory')
                .then(r => {
                    frm.set_value('territory', r.message.territory);
                });
        }
    },

    validate(frm) {
        // Custom validation
        if (frm.doc.delivery_date < frappe.datetime.get_today()) {
            frappe.throw('Delivery date cannot be in the past');
        }
    }
});
```

### Form Script in App

Create `{doctype}.js` alongside `{doctype}.py`:

```javascript
// lead.js
frappe.ui.form.on('Lead', {
    setup(frm) {
        frm.set_query('territory', () => ({
            filters: { is_group: 0 }
        }));
    },

    refresh(frm) {
        if (!frm.is_new() && frm.doc.status !== 'Converted') {
            frm.add_custom_button('Convert to Customer', () => {
                frappe.xcall('crm.api.lead.convert_to_customer', {
                    lead: frm.doc.name
                }).then(() => {
                    frm.reload_doc();
                });
            });
        }
    }
});
```

---

## Common Patterns

### Auto-Calculate Totals

```javascript
frappe.ui.form.on('Sales Order Item', {
    qty(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },
    rate(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    }
});

function calculate_row_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    row.amount = flt(row.qty) * flt(row.rate);
    frm.refresh_field('items');
    calculate_totals(frm);
}

function calculate_totals(frm) {
    let total = 0;
    frm.doc.items.forEach(item => {
        total += flt(item.amount);
    });
    frm.set_value('total', total);
}
```

### Dependent Fields

```javascript
frappe.ui.form.on('Lead', {
    lead_type(frm) {
        if (frm.doc.lead_type === 'Company') {
            frm.toggle_reqd('company_name', true);
            frm.toggle_display('company_name', true);
        } else {
            frm.toggle_reqd('company_name', false);
            frm.toggle_display('company_name', false);
        }
    }
});
```

### Confirm Before Action

```javascript
frm.add_custom_button('Delete All Items', () => {
    frappe.confirm(
        'Are you sure you want to delete all items?',
        () => {
            frm.clear_table('items');
            frm.refresh_field('items');
            frm.save();
        }
    );
});
```
