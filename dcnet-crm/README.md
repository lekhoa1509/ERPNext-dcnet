# DCNET CRM

Independent Frappe v16 extension app for the standard ERPNext CRM documents.

## Continue development

Read [`HANDOFF.md`](HANDOFF.md) before making changes. It contains the current
architecture, non-negotiable rules, implemented customer profile tabs,
verification commands and pending work.

## Data ownership

- Lead: ERPNext `Lead`
- Opportunity: ERPNext `Opportunity`
- Customer: ERPNext `Customer`
- Contact: Frappe `Contact`
- Quotation: ERPNext `Quotation`
- Order: ERPNext `Sales Order`

The app does not copy or modify ERPNext source code and does not depend on
`dcnet_apps`. It adds a Vue workspace and permission-aware APIs on top of the
standard documents.

```bash
bench get-app /path/to/dcnet-crm
bench --site flow.local install-app dcnet_crm
bench --site flow.local migrate
bench build --app dcnet_crm
```
