# DCNET CRM Production Readiness

> Verified: 13/07/2026  
> Code status: production-hardened locally  
> Release status: pending immutable Git release and production infrastructure

## Passed

- `npm test`: frontend syntax, stored-XSS guard and minified build pass.
- Backend static safety guard passes.
- 12 Frappe integration tests pass, including Guest denial, Sales User boot,
  Lead conversion, Service Account permissions and export-field validation.
- `bench --site flow.local migrate` passes for `dcnet_crm`.
- Scheduler enabled; three workers online.
- CRM asset returns HTTP 200 after migrate/cache clear.
- Whitelisted CRM actions no longer create invalid accounting/stock documents.
- Explicit transaction commits removed from CRM request methods.
- Unfinished controls are hidden unless
  `dcnet_crm_show_unready_features = 1` is explicitly configured.
- Lead conversion uses ERPNext mappings and creates permission-checked Customer
  and Opportunity documents.
- Lead, Customer, Opportunity and Sales Order lists export permission-filtered
  Excel workbooks.
- Custom `DCNET Service Account` is included in CRM boot and supports
  permission-aware list/search/detail/related orders/export.

## Release actions outside code

- Commit and review the current changes on `feature/sync-08-07-2026`; deploy an
  immutable commit/tag from the standalone `dcnet-crm` repository.
- Production secrets, HTTPS, Redis authentication, backups and monitoring must
  be configured by infrastructure according to `PRODUCTION_RUNBOOK.md`.
- Run UAT with named Sales User, Sales Manager and System Manager accounts.
- Warnings from other installed DCNET apps are outside the `dcnet_crm` release
  scope and do not block a CRM-only deployment on a clean Frappe + ERPNext site.

## Scope policy

Features not confirmed in the customer specification are not presented as
working production controls. They remain available only when the explicit
development feature flag is enabled.
