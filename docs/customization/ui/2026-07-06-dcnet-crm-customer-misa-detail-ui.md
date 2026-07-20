# DCNET CRM Customer MISA Detail UI

## Overview

Customize the DCNET CRM customer detail page to follow the MISA AMIS CRM customer layout: left customer profile rail, top detail tabs, nested sub-tabs for sales/support/marketing/notes, dense related tables, and expanded customer information sections.

## Requirements

- Match the provided MISA customer detail screenshots for customer profile, tab structure, sales subtabs, support subtabs, marketing subtabs, notes/attachments, and conversation.
- Keep implementation inside `dcnet-crm` customer detail UI.
- Reuse existing ERPNext Customer, Contact, Address, Sales Order, Quotation, Sales Invoice, Opportunity, File, and ToDo data.

## Implementation

- Added Customer custom fields to the detail API response and update allowlist.
- Added customer detail state for support, marketing, and notes nested tabs.
- Expanded customer detail sections: common info, billing, shipping, additional info, purchasing statistics, description, system info, and portal info.
- Converted sales related content into MISA-like tables with stable footer pagination.
- Added support, marketing, notes/attachments, and conversation panels.
- Kept the activity panel on the Customer list read-only: it displays related
  activities but does not provide an inline note composer. Notes remain an
  explicit action in Customer detail.

## Technical Notes

- Main frontend files:
  - `dcnet-crm/frontend/src/features/customers/template.js`
  - `dcnet-crm/frontend/src/features/customers/composable.js`
  - `dcnet-crm/frontend/src/styles.css`
- Backend API:
  - `dcnet-crm/dcnet_crm/api.py`

## Deployment

Run:

```bash
cd dcnet-crm
npm run build
docker exec -u frappe devcontainer-frappe-1 bash -lc 'cd /workspace/development/frappe-bench && bench build --app dcnet_crm && bench --site flow.local clear-cache && bench --site flow.local clear-website-cache'
```

## Future Updates

- Wire real data for Support cards, Marketing campaigns/promotions, and customer portal access once their DocTypes/specs are finalized.
- Add create/select dialogs for currently placeholder actions.

## Troubleshooting

- If the old layout is still visible, hard refresh the browser after cache clear.
- If purchased item type is empty, confirm the submitted Sales Invoice Item rows have `item_group`.

## Verification Checklist

- `npm run build`
- `python3 -m py_compile dcnet_crm/api.py`
- `bench --site flow.local execute dcnet_crm.api.get_customer_workspace --kwargs '{"name":"DCNET-CRM-TEST Customer 10"}'`
- `bench build --app dcnet_crm`
