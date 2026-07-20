# DCNET Permission Manager

## Overview

Added a new Frappe app `dcnet_permission` with a Desk page for department-scoped user and role management.

## Requirements

- Source: `docs/feature/FEATURE_SPECIFICATION.md` Section 12 Role & Permission.
- Supporting analysis: `docs/erpnext-flows/ROLES_AND_PERMISSIONS_ANALYSIS.md` Section 7.2 Department to Roles Mapping.
- Managers can create and update users only within configured department scopes.
- Managers can maintain a curated per-user permission matrix for business DocTypes and reports inside their department scope.
- Users created from this manager receive default password `123456` and must change it on first login.

## Implementation

- App: `dcnet-permission/`
- Page: `/desk/dcnet-permission-manager`
- Workspace: `DCNET Permission`
- Workspace Sidebar: `DCNET Permission`
- Desktop Icon: `DCNET Permission`
- Config DocType: `DCNET Permission Scope`
- Child DocType: `DCNET Permission Scope Role`
- Child DocType: `DCNET Permission Scope Profile`
- API: `dcnet_permission.api`
- UI assets:
  - `dcnet_permission/public/js/dcnet_permission_manager.js`
  - `dcnet_permission/public/css/dcnet_permission_manager.css`
  - `dcnet_permission/dcnet_permission/page/dcnet_permission_manager/`
  - `dcnet_permission/dcnet_permission/workspace/dcnet_permission/`
  - `dcnet_permission/workspace_sidebar/dcnet_permission.json`
  - `dcnet_permission/desktop_icon/dcnet_permission.json`

## Technical Notes

- Department boundary uses standard Frappe `User Permission` with `allow = Department`.
- The department list shown in the manager is loaded from the standard ERPNext `Department` master (`is_group = 0`, not disabled). `DCNET Permission Scope` is only the role-delegation configuration layered on top of that master data.
- Permission admins also see users inferred from scope roles when those users do not yet have a Department user permission or linked Employee department. Delegated managers still depend on explicit department scope.
- Dashboard API accepts GET and POST because Desk `frappe.call()` sends POST by default.
- User-specific permission updates create one hidden custom Role per user, remove delegated broad roles for that user, then use Frappe `Custom DocPerm` for DocTypes and `Custom Role` for reports.
- The app now seeds a safe `Accounts User` baseline for accounting setup screens: chart of accounts, cost centers, company, payment terms are read-only; ERPNext/VN accounting settings are not exposed to `Accounts User`. This prevents a sidebar/workspace warning from being bypassed by closing the modal.
- A server-side `has_permission` guard enforces the personal permission matrix for delegated users, so broad ERPNext roles cannot silently re-grant write/create/delete after a user has custom permissions.
- Permission matrix is department-profile aware: Accounting, HR, Sales, Buying, Stock, Support, and Projects scopes each show their own curated business catalog. It does not expose System Settings, User, Role, DocType, or other administrator surfaces.
- `DCNET Permission Scope.extra_permission_profiles` lets a `System Manager` / `DCNET Permission Admin` open cross-department catalogs intentionally. Example: add `HR / Nhân sự - Chấm công` to the Accounting scope so the accounting manager can grant Attendance/Leave access to selected accounting users.
- Delegated managers cannot assign protected roles: `System Manager`, `Administrator`.
- Existing roles outside the manager's allowed role list are preserved on update.
- New users are inserted with default password `123456`; the app disables welcome reset email for this flow and sets `last_password_reset_date` far enough in the past for Frappe's native password-expiry login flow to redirect them to `/update-password` immediately.
- If System Settings does not already enforce password expiry, the app sets `force_user_to_reset_password` to `36500` days so only intentionally backdated users are forced to change their password.
- Forced password-change redirects use a relative `/update-password` URL via `dcnet_permission.user.DCNETPermissionUserMixin`, avoiding login loops when developers open the site through `localhost`, `127.0.0.1`, or a LAN IP.
- The `DCNET Permission` workspace/sidebar intentionally do not set `module`; otherwise Frappe filters them out for department managers whose roles do not have module-level access to the custom app. Server APIs still enforce department scope.
- The Desk Page title includes `DCNET Permission` so Awesomebar/search can find it by the app name as well as by the Vietnamese title.
- The desktop icon opens the manager page directly at `/desk/dcnet-permission-manager`; the first sidebar link is also the page. This avoids Frappe routing the Vietnamese workspace title to a non-existent page like `phân-quyền-dcnet`.
- The Desk Page, Workspace, Desktop Icon, app tile, and all whitelisted APIs are restricted to `Administrator`, `System Manager`, `DCNET Permission Admin`, active scope `manager_role`s, or direct `manager_user`s synced through `DCNET Permission Manager`. Users outside those scopes cannot see the page in sidebar/search and cannot open it by URL.
- The app seeds only the accounting scope by default. HR or other departments should be added intentionally in `DCNET Permission Scope` when the customer confirms that delegation path. If both a short department (`Kế toán`) and a full department (`PHÒNG KẾ TOÁN`) exist, seeded scopes prefer the full `PHÒNG...` department.
- Frappe v16 Desk Page loading requires the physical `page/dcnet_permission_manager/` directory; the page CSS shim lives there and imports the public stylesheet.

## Deployment

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && ln -sfn /workspace/dcnet-permission apps/dcnet_permission"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && grep -qxF dcnet_permission sites/apps.txt || printf '\ndcnet_permission\n' >> sites/apps.txt"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && ./env/bin/pip install -e /workspace/dcnet-permission --no-deps"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local install-app dcnet_permission"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench build --app dcnet_permission"
```

## Future Updates

- Clarify whether the same flow should create linked `Employee` records.
- Confirm the production department-to-role matrix with the customer before go-live.

## Troubleshooting

- If a manager sees no departments, check `DCNET Permission Scope`.
- If a user is missing from the list, check their `User Permission` for `Department`.
- If a role is unavailable, check the scope's allowed role table and whether the Role is disabled.
- If the permission matrix shows the wrong business area, check `DCNET Permission Scope.department` and the scope's allowed roles. The matrix is resolved from department keywords and role names.
- If a department needs functions from another area, add that area in `DCNET Permission Scope > Extra Permission Profiles`, then reload the manager page.
- If a VN Accounting report is still unavailable, check both the report role and the `report` permission on its reference DocType.
- If first login does not show the password-change screen, check `System Settings.force_user_to_reset_password` and the user's `last_password_reset_date`.
- If the page should show for a manager but does not show in Desk search/sidebar, check `DCNET Permission Scope.manager_role` or `manager_user`, then run `dcnet_permission.install.setup()` to resync Page/Workspace/Desktop Icon roles.

## Verification Checklist

- Scope created for Accounting and HR where matching master data exists.
- Department manager cannot select a department outside their scope.
- Department manager cannot assign roles outside their scope.
- User receives default Department user permission after save.
- Newly created user can log in with `123456` and is redirected to change password before entering Desk.
- Desk sidebar/search shows `DCNET Permission` and links to `dcnet-permission-manager`.
- Normal users outside all permission scopes cannot see `DCNET Permission`, cannot load `dcnet-permission-manager`, and receive `PermissionError` from the dashboard API.
- Department manager can update read/create/write/delete/submit/cancel/report/export/print only for curated permission items and users inside their scope.
