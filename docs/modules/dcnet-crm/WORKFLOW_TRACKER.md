# Workflow Tracker: DCNET CRM

> Started: 2026-06-12 | Last updated: 2026-07-13
> Current phase: 6 - Documentation and release preparation

## Checklist

### Phase 0: Assessment
- [x] Read `docs/modules/PROGRESS.md`
- [x] Audit existing CRM code and documentation
- [x] Audit 10 source videos (Parts 1-4 and 6-11; Part 5 is absent)
- [x] Check remote CRM branches

### Phase 1: Clarify Requirements
- [x] Read `FEATURE_SPECIFICATION.md`
- [x] Separate official scope from competitor-only features
- [x] Record unresolved integrations in `SPEC_MAPPING.md`

### Phase 2: Documentation
- [x] Create spec-to-MISA-to-ERPNext mapping
- [x] Reuse approved design spec
- [x] Add module README, CLARIFY and CUSTOM_REQUIREMENTS
- [x] Correct DocType ownership for CRM Care Card and DCNET Service Account
- [x] Document dashboard bento UI and native sidebar routing
- [ ] Customer confirms integration and GPS scope

### Phase 3: Planning
- [x] Select separate Frappe app architecture
- [x] Select Vue SPA with permission-aware ERPNext APIs

### Phase 4: Implementation
- [x] Scaffold `dcnet-crm`
- [x] Implement CRM API layer
- [x] Implement Vue dashboard and tri-pane list views
- [x] Redesign dashboard with KPI cards, opportunity funnel and stage composition
- [x] Route `Bàn làm việc` to dashboard and remove duplicate `Tất cả` entry
- [x] Reuse ERPNext DocTypes
- [x] Build and runtime verification
- [x] Customer list and internal customer profile route
- [x] Inline Customer, primary Contact and Address editing
- [x] Contact table, create/edit and select existing Contact
- [x] Activity table for ToDo, meeting Event and call Event
- [x] Sales tab for orders, returns, opportunities, quotations, invoices and purchased items
- [x] Customer list preview uses related activities, quotations, orders, invoices and contacts
- [x] Customer saved-view menu without competitor AI prediction views
- [x] Customer column customization drawer with persisted selection
- [x] Opportunity tri-pane list with activity, customer, contact and item previews
- [x] Internal Opportunity create form with standard ERPNext fields and items
- [x] Fix Opportunity create form mount and initialization order
- [x] Align Opportunity create form with approved two-column UI
- [x] Auto-create and save Opportunity shipping/A-End/Z-End Custom Fields
- [x] Unconfirmed/incomplete features hidden by default in production
- [ ] Support, Marketing, Exchange and complete file-management tabs (requires approved spec)

### Phase 5: Review & Verify
- [x] Focused API checks pass with transaction rollback
- [x] Automated integration suite (9 tests) passes on `flow.local`
- [x] Frontend syntax, build and stored-XSS checks pass
- [x] Backend safety guard passes
- [x] Frontend build passes
- [x] Site migrate passes
- [x] HTTP asset and Desk route smoke test

### Phase 6: Ship & Document
- [x] Add `dcnet-crm/HANDOFF.md` for continuation
- [x] User guide at `docs/training/custom-apps/dcnet-crm/USER_GUIDE.md`
- [x] Module docs normalized under `docs/modules/dcnet-crm/`
- [ ] PR / merge
- [x] Production deployment/rollback runbook
