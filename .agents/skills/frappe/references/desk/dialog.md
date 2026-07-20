# Frappe Desk Dialog API

JavaScript API for creating dialogs and popups in Frappe Desk.

## Table of Contents

- [frappe.ui.Dialog](#frappeuidialog)
- [frappe.prompt](#frappeprompt)
- [frappe.confirm](#frappeconfirm)
- [frappe.msgprint](#frappemsgprint)
- [frappe.throw](#frappethrow)
- [frappe.warn](#frappewarn)
- [frappe.show_alert](#frappeshow_alert)
- [frappe.show_progress](#frappeshow_progress)
- [frappe.new_doc](#frappnew_doc)
- [MultiSelectDialog](#multiselectdialog)
- [Field Types](#field-types)

---

## frappe.ui.Dialog

Primary method for creating modal dialogs.

### Basic Usage

```javascript
let d = new frappe.ui.Dialog({
    title: 'Enter Details',
    fields: [
        {
            label: 'First Name',
            fieldname: 'first_name',
            fieldtype: 'Data',
            reqd: 1
        },
        {
            label: 'Email',
            fieldname: 'email',
            fieldtype: 'Data',
            options: 'Email'
        },
        {
            label: 'Status',
            fieldname: 'status',
            fieldtype: 'Select',
            options: 'Open\nClosed\nPending'
        }
    ],
    size: 'small', // 'small', 'large', 'extra-large'
    primary_action_label: 'Submit',
    primary_action(values) {
        console.log(values);
        d.hide();
    },
    secondary_action_label: 'Cancel',
    secondary_action() {
        d.hide();
    }
});

d.show();
```

### Options

| Option | Type | Description |
|--------|------|-------------|
| `title` | `string` | Dialog title |
| `fields` | `array` | Form field definitions |
| `size` | `string` | `'small'`, `'large'`, `'extra-large'` |
| `primary_action_label` | `string` | Primary button text |
| `primary_action` | `function` | Primary button callback |
| `secondary_action_label` | `string` | Secondary button text |
| `secondary_action` | `function` | Secondary button callback |
| `minimizable` | `boolean` | Allow minimize |
| `static` | `boolean` | Prevent close on backdrop click |

### Methods

| Method | Description |
|--------|-------------|
| `d.show()` | Show dialog |
| `d.hide()` | Hide dialog |
| `d.get_value(fieldname)` | Get field value |
| `d.get_values()` | Get all values |
| `d.set_value(fieldname, value)` | Set field value |
| `d.set_values(values)` | Set multiple values |
| `d.set_df_property(fieldname, prop, value)` | Set field property |
| `d.get_field(fieldname)` | Get field object |
| `d.enable_primary_action()` | Enable primary button |
| `d.disable_primary_action()` | Disable primary button |
| `d.set_primary_action(label, callback)` | Update primary action |

### Examples

#### Dialog with Multiple Sections

```javascript
let d = new frappe.ui.Dialog({
    title: 'Create Lead',
    fields: [
        {
            fieldtype: 'Section Break',
            label: 'Basic Info'
        },
        {
            label: 'Lead Name',
            fieldname: 'lead_name',
            fieldtype: 'Data',
            reqd: 1
        },
        {
            label: 'Email',
            fieldname: 'email',
            fieldtype: 'Data',
            options: 'Email'
        },
        {
            fieldtype: 'Column Break'
        },
        {
            label: 'Phone',
            fieldname: 'phone',
            fieldtype: 'Data',
            options: 'Phone'
        },
        {
            label: 'Company',
            fieldname: 'company',
            fieldtype: 'Data'
        },
        {
            fieldtype: 'Section Break',
            label: 'Additional Info'
        },
        {
            label: 'Notes',
            fieldname: 'notes',
            fieldtype: 'Text'
        }
    ],
    primary_action_label: 'Create',
    primary_action(values) {
        frappe.call({
            method: 'frappe.client.insert',
            args: {
                doc: {
                    doctype: 'Lead',
                    ...values
                }
            },
            callback: (r) => {
                if (r.message) {
                    frappe.show_alert({
                        message: 'Lead created',
                        indicator: 'green'
                    });
                    d.hide();
                }
            }
        });
    }
});
d.show();
```

#### Dialog with Link Field

```javascript
let d = new frappe.ui.Dialog({
    title: 'Select Customer',
    fields: [
        {
            label: 'Customer',
            fieldname: 'customer',
            fieldtype: 'Link',
            options: 'Customer',
            reqd: 1,
            get_query: () => {
                return {
                    filters: { disabled: 0 }
                };
            }
        },
        {
            label: 'Contact',
            fieldname: 'contact',
            fieldtype: 'Link',
            options: 'Contact',
            get_query: () => {
                let customer = d.get_value('customer');
                return {
                    filters: { link_name: customer }
                };
            },
            depends_on: 'eval:doc.customer'
        }
    ],
    primary_action_label: 'Select',
    primary_action(values) {
        // handle selection
    }
});
d.show();
```

#### Dialog with Table (Child Table)

```javascript
let d = new frappe.ui.Dialog({
    title: 'Add Items',
    fields: [
        {
            label: 'Items',
            fieldname: 'items',
            fieldtype: 'Table',
            cannot_add_rows: false,
            in_place_edit: true,
            data: [],
            fields: [
                {
                    fieldname: 'item',
                    fieldtype: 'Link',
                    options: 'Item',
                    label: 'Item',
                    in_list_view: 1
                },
                {
                    fieldname: 'qty',
                    fieldtype: 'Int',
                    label: 'Qty',
                    in_list_view: 1
                },
                {
                    fieldname: 'rate',
                    fieldtype: 'Currency',
                    label: 'Rate',
                    in_list_view: 1
                }
            ]
        }
    ],
    primary_action_label: 'Add',
    primary_action(values) {
        console.log(values.items);
        d.hide();
    }
});
d.show();
```

---

## frappe.prompt

Quick dialog for collecting single or multiple values.

### Single Field

```javascript
frappe.prompt(
    {
        label: 'Reason',
        fieldname: 'reason',
        fieldtype: 'Small Text',
        reqd: 1
    },
    (values) => {
        console.log(values.reason);
    },
    'Enter Reason',
    'Submit'
);
```

### Multiple Fields

```javascript
frappe.prompt(
    [
        {
            label: 'From Date',
            fieldname: 'from_date',
            fieldtype: 'Date',
            reqd: 1
        },
        {
            label: 'To Date',
            fieldname: 'to_date',
            fieldtype: 'Date',
            reqd: 1
        }
    ],
    (values) => {
        console.log(values.from_date, values.to_date);
    },
    'Select Date Range',
    'Apply'
);
```

---

## frappe.confirm

Binary yes/no confirmation dialog.

```javascript
frappe.confirm(
    'Are you sure you want to delete this item?',
    () => {
        // Yes callback
        deleteItem();
    },
    () => {
        // No callback (optional)
        console.log('Cancelled');
    }
);
```

### With Custom Labels

```javascript
frappe.confirm(
    'Proceed with this action?',
    () => { /* yes */ },
    () => { /* no */ }
).set_primary_action('Proceed', () => {
    // custom action
});
```

---

## frappe.msgprint

Display messages and alerts.

### Basic Message

```javascript
frappe.msgprint('Operation completed successfully');
```

### With Title

```javascript
frappe.msgprint({
    title: 'Success',
    message: 'Document has been saved',
    indicator: 'green'
});
```

### With Action

```javascript
frappe.msgprint({
    title: 'Warning',
    message: 'Some items are out of stock',
    indicator: 'orange',
    primary_action: {
        label: 'View Items',
        action: () => {
            frappe.set_route('List', 'Item', { stock_qty: ['<', 10] });
        }
    }
});
```

### Indicators

- `green` - Success
- `blue` - Info
- `orange` - Warning
- `red` - Error

---

## frappe.show_alert

Toast-style notifications (auto-dismiss).

```javascript
// Simple
frappe.show_alert('Saved');

// With indicator
frappe.show_alert({
    message: 'Document updated',
    indicator: 'green'
}, 5); // duration in seconds

// With action
frappe.show_alert({
    message: 'Item deleted',
    indicator: 'blue',
    action: {
        label: 'Undo',
        action: () => {
            // undo logic
        }
    }
});
```

---

## frappe.throw

Show error message and throw exception.

```javascript
// Simple error
frappe.throw('Invalid input');

// With title
frappe.throw({
    title: 'Validation Error',
    message: 'Please fill all required fields'
});

// Translated message
frappe.throw(__('This field is required'));
```

---

## frappe.warn

Warning dialog with minimize support.

```javascript
frappe.warn(
    'Warning Title',
    'This action may have consequences. Do you want to proceed?',
    () => {
        // Proceed callback
        performAction();
    },
    'Proceed',  // Primary action label
    true        // Show "Don't show again" checkbox
);
```

---

## frappe.show_progress

Display progress bar dialog.

```javascript
// Basic progress
frappe.show_progress('Processing...', 50, 100);  // 50 of 100

// With description
frappe.show_progress('Importing Records', 25, 100, 'Processing row 25 of 100');

// Hide when done
frappe.hide_progress();
```

### In Loop

```javascript
let items = [...];
for (let i = 0; i < items.length; i++) {
    frappe.show_progress('Processing...', i + 1, items.length, `Item ${i + 1}`);
    await processItem(items[i]);
}
frappe.hide_progress();
```

---

## frappe.new_doc

Open new document form with pre-filled values.

```javascript
// Basic - open new Lead form
frappe.new_doc('Lead');

// With pre-filled values
frappe.new_doc('Lead', {
    lead_name: 'John Doe',
    email_id: 'john@example.com',
    source: 'Website'
});

// Using route_options (alternative)
frappe.route_options = {
    customer: 'CUST-001',
    delivery_date: frappe.datetime.add_days(frappe.datetime.get_today(), 7)
};
frappe.new_doc('Sales Order');
```

---

## MultiSelectDialog

Select multiple records from a DocType.

```javascript
new frappe.ui.form.MultiSelectDialog({
    doctype: 'Item',
    target: cur_frm,
    setters: {
        item_group: null,
        brand: null
    },
    get_query: () => ({
        filters: { is_sales_item: 1 }
    }),
    action: (selections) => {
        // selections = array of selected names
        console.log(selections);
    },
    primary_action_label: 'Select Items'
});
```

### With Date Range

```javascript
new frappe.ui.form.MultiSelectDialog({
    doctype: 'Sales Invoice',
    target: cur_frm,
    setters: {
        customer: cur_frm.doc.customer
    },
    date_field: 'posting_date',
    get_query: () => ({
        filters: {
            docstatus: 1,
            outstanding_amount: ['>', 0]
        }
    }),
    action: (selections) => {
        // Process selected invoices
    }
});
```

---

## Field Types

Available field types for dialogs:

### Input Fields

| Fieldtype | Description | Options |
|-----------|-------------|---------|
| `Data` | Text input | `Email`, `Name`, `Phone`, `URL` |
| `Int` | Integer | - |
| `Float` | Decimal | - |
| `Currency` | Money | - |
| `Password` | Masked input | - |
| `Small Text` | Multi-line (3 rows) | - |
| `Text` | Multi-line (5 rows) | - |
| `Long Text` | Large text area | - |
| `Text Editor` | Rich text | - |
| `Code` | Code editor | Language name |
| `HTML Editor` | HTML editor | - |

### Selection Fields

| Fieldtype | Description | Options |
|-----------|-------------|---------|
| `Select` | Dropdown | Newline-separated options |
| `Link` | DocType reference | DocType name |
| `Dynamic Link` | Dynamic reference | Field containing doctype |
| `MultiSelect` | Multiple selection | - |
| `Autocomplete` | Filtered input | - |

### Date/Time

| Fieldtype | Description |
|-----------|-------------|
| `Date` | Date picker |
| `Datetime` | Date + time |
| `Time` | Time only |
| `Duration` | Time duration |

### Special

| Fieldtype | Description |
|-----------|-------------|
| `Check` | Checkbox |
| `Attach` | File upload |
| `Attach Image` | Image upload |
| `Color` | Color picker |
| `Rating` | Star rating |
| `Signature` | Signature pad |
| `Table` | Child table |
| `HTML` | Static HTML content |
| `Button` | Action button |

### Layout

| Fieldtype | Description |
|-----------|-------------|
| `Section Break` | New section |
| `Column Break` | New column |
| `Tab Break` | New tab |

### Field Properties

```javascript
{
    label: 'Field Label',
    fieldname: 'field_name',
    fieldtype: 'Data',
    reqd: 1,                    // Required
    default: 'Default Value',
    read_only: 0,
    hidden: 0,
    depends_on: 'eval:doc.other_field=="value"',
    mandatory_depends_on: 'eval:doc.status=="Active"',
    description: 'Help text',
    placeholder: 'Enter value...',
    options: 'Option1\nOption2',  // For Select
    get_query: () => ({ filters: {} }),  // For Link
    onchange: () => { /* handler */ }
}
```
