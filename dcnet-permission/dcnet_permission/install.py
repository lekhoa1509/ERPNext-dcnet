import json

import frappe


APP_ADMIN_ROLE = "DCNET Permission Admin"
APP_MANAGER_ROLE = "DCNET Permission Manager"
APP_NAME = "dcnet_permission"
MODULE_NAME = "DCNET Permission"
WORKSPACE_NAME = "DCNET Permission"
PAGE_NAME = "dcnet-permission-manager"
SCOPE_DOCTYPE = "DCNET Permission Scope"
SEED_NOTE = "Seeded by DCNET Permission. Review with customer before production use."


def before_install():
    ensure_access_roles()


def before_migrate():
    ensure_access_roles()


def after_install():
    setup()


def after_migrate():
    setup()


def setup():
    ensure_access_roles()
    normalize_permission_profile_values()
    cleanup_seeded_scopes()
    create_default_scopes()
    ensure_workspace_navigation()
    ensure_permission_baselines()


def ensure_access_roles():
    for role_name in [APP_ADMIN_ROLE, APP_MANAGER_ROLE]:
        ensure_role(role_name)


def ensure_role(role_name):
    if frappe.db.exists("Role", role_name):
        frappe.db.set_value("Role", role_name, "desk_access", 1, update_modified=False)
        return

    role = frappe.new_doc("Role")
    role.role_name = role_name
    role.desk_access = 1
    role.is_custom = 1
    role.insert(ignore_permissions=True)


def ensure_workspace_navigation():
    ensure_permission_page_title()
    ensure_permission_workspace()
    ensure_permission_sidebar()
    ensure_permission_desktop_icon()
    ensure_navigation_access()
    sync_manager_user_access()


def ensure_permission_page_title():
    if not frappe.db.exists("Page", PAGE_NAME):
        return

    frappe.db.set_value(
        "Page",
        PAGE_NAME,
        {
            "title": "DCNET Permission - Department Permissions",
            "module": MODULE_NAME,
        },
        update_modified=False,
    )


def ensure_permission_workspace():
    workspace = (
        frappe.get_doc("Workspace", WORKSPACE_NAME)
        if frappe.db.exists("Workspace", WORKSPACE_NAME)
        else frappe.new_doc("Workspace")
    )
    workspace.label = "DCNET Permission"
    workspace.title = "DCNET Permission"
    workspace.module = ""
    workspace.app = APP_NAME
    workspace.public = 1
    workspace.is_hidden = 0
    workspace.icon = "shield-check"
    workspace.type = "Workspace"
    workspace.sequence_id = 28
    workspace.content = json.dumps(
        [
            {
                "id": "dpm_header",
                "type": "header",
                "data": {"text": '<span class="h4"><b>Department Permissions</b></span>', "col": 12},
            },
            {
                "id": "dpm_shortcut",
                "type": "shortcut",
                "data": {"shortcut_name": "Permission Manager", "col": 4},
            },
            {
                "id": "dpm_card",
                "type": "card",
                "data": {"card_name": "Permission Admin", "col": 4},
            },
        ],
        ensure_ascii=False,
    )
    workspace.set("shortcuts", [])
    workspace.append(
        "shortcuts",
        {
            "label": "Permission Manager",
            "type": "Page",
            "link_to": PAGE_NAME,
            "color": "Blue",
        },
    )
    workspace.set("links", [])
    workspace.append(
        "links",
        {
            "type": "Card Break",
            "label": "Permission Admin",
            "link_count": 1,
        },
    )
    workspace.append(
        "links",
        {
            "type": "Link",
            "label": "Department Permission Manager",
            "link_type": "Page",
            "link_to": PAGE_NAME,
        },
    )

    if workspace.is_new():
        workspace.insert(ignore_permissions=True)
    else:
        workspace.save(ignore_permissions=True)


def ensure_permission_sidebar():
    sidebar = (
        frappe.get_doc("Workspace Sidebar", WORKSPACE_NAME)
        if frappe.db.exists("Workspace Sidebar", WORKSPACE_NAME)
        else frappe.new_doc("Workspace Sidebar")
    )
    sidebar.title = WORKSPACE_NAME
    sidebar.app = APP_NAME
    sidebar.module = ""
    sidebar.standard = 1
    sidebar.header_icon = "shield-check"
    sidebar.set("items", [])
    sidebar.append(
        "items",
        {
            "type": "Link",
            "label": "Overview",
            "link_type": "Workspace",
            "link_to": WORKSPACE_NAME,
            "icon": "home",
        },
    )
    sidebar.append(
        "items",
        {
            "type": "Link",
            "label": "Permission Manager",
            "link_type": "Page",
            "link_to": PAGE_NAME,
            "icon": "shield-check",
        },
    )
    sidebar.append(
        "items",
        {
            "type": "Link",
            "label": "Permission Scope",
            "link_type": "DocType",
            "link_to": SCOPE_DOCTYPE,
            "icon": "settings",
        },
    )

    if sidebar.is_new():
        sidebar.insert(ignore_permissions=True)
    else:
        sidebar.save(ignore_permissions=True)

    # Frappe auto-fills this from the first sidebar item. Keep it open so delegated
    # managers without the custom app module can still see the entry.
    frappe.db.set_value("Workspace Sidebar", WORKSPACE_NAME, "module", "", update_modified=False)


def ensure_permission_desktop_icon():
    icon = (
        frappe.get_doc("Desktop Icon", WORKSPACE_NAME)
        if frappe.db.exists("Desktop Icon", WORKSPACE_NAME)
        else frappe.new_doc("Desktop Icon")
    )
    if icon.is_new():
        icon.name = WORKSPACE_NAME
    icon.label = "DCNET Permission"
    icon.standard = 1
    icon.icon = "shield-check"
    icon.icon_type = "Link"
    icon.link_type = "Workspace Sidebar"
    icon.link_to = WORKSPACE_NAME
    icon.link = ""
    icon.sidebar = WORKSPACE_NAME
    icon.app = APP_NAME
    icon.hidden = 0
    icon.restrict_removal = 1

    if icon.is_new():
        icon.insert(ignore_permissions=True)
    else:
        icon.save(ignore_permissions=True)


def ensure_navigation_access():
    roles = get_navigation_access_roles()
    set_document_roles("Page", PAGE_NAME, roles)
    set_document_roles("Workspace", WORKSPACE_NAME, roles)
    set_document_roles("Desktop Icon", WORKSPACE_NAME, roles)
    frappe.clear_cache()


def get_navigation_access_roles():
    roles = {"System Manager", APP_ADMIN_ROLE, APP_MANAGER_ROLE}
    if frappe.db.table_exists("DCNET Permission Scope"):
        for role in frappe.get_all(
            "DCNET Permission Scope",
            filters={"enabled": 1, "manager_role": ["is", "set"]},
            pluck="manager_role",
        ):
            if role:
                roles.add(role)

    return sorted(role for role in roles if frappe.db.exists("Role", role))


def set_document_roles(doctype, name, roles):
    if not frappe.db.exists(doctype, name):
        return

    doc = frappe.get_doc(doctype, name)
    current_roles = [row.role for row in doc.get("roles", []) if row.role]
    if current_roles == roles:
        return

    doc.set("roles", [])
    for role in roles:
        doc.append("roles", {"role": role})
    doc.save(ignore_permissions=True)


def sync_manager_user_access():
    if not frappe.db.table_exists("DCNET Permission Scope"):
        return

    from dcnet_permission.permission_manager import get_enabled_scope_manager_roles

    manager_roles = set(get_enabled_scope_manager_roles())
    manager_users = {
        user
        for user in frappe.get_all(
            "DCNET Permission Scope",
            filters={"enabled": 1, "manager_user": ["is", "set"]},
            pluck="manager_user",
        )
        if user and frappe.db.exists("User", user)
    }
    if manager_roles:
        manager_users.update(
            {
                row.parent
                for row in frappe.get_all(
                    "Has Role",
                    filters={
                        "parenttype": "User",
                        "role": ["in", list(manager_roles)],
                    },
                    fields=["parent"],
                )
                if row.parent and frappe.db.exists("User", row.parent)
            }
        )
    users_with_manager_role = {
        row.parent
        for row in frappe.get_all(
            "Has Role",
            filters={"parenttype": "User", "role": APP_MANAGER_ROLE},
            fields=["parent"],
        )
    }

    for user in manager_users - users_with_manager_role:
        doc = frappe.get_doc("User", user)
        doc.append("roles", {"role": APP_MANAGER_ROLE})
        doc.flags.ignore_permlevel_for_fields = ["roles"]
        doc.save(ignore_permissions=True)
        frappe.clear_cache(user=user)

    for user in users_with_manager_role - manager_users:
        if not frappe.db.exists("User", user):
            continue

        doc = frappe.get_doc("User", user)
        kept_roles = sorted({row.role for row in doc.get("roles", []) if row.role and row.role != APP_MANAGER_ROLE})
        doc.set("roles", [])
        for role in kept_roles:
            doc.append("roles", {"role": role})
        doc.flags.ignore_permlevel_for_fields = ["roles"]
        doc.save(ignore_permissions=True)
        frappe.clear_cache(user=user)


def ensure_permission_baselines():
    from dcnet_permission.permission_manager import apply_default_permission_baselines

    apply_default_permission_baselines()


def normalize_permission_profile_values():
    if not frappe.db.table_exists("DCNET Permission Scope Profile"):
        return

    from dcnet_permission.permission_manager import get_permission_profile_label, normalize_profile_key

    rows = frappe.get_all("DCNET Permission Scope Profile", fields=["name", "profile"])
    for row in rows:
        key = normalize_profile_key(row.profile)
        canonical_label = get_permission_profile_label(key)
        if key and canonical_label and canonical_label != row.profile:
            frappe.db.set_value(
                "DCNET Permission Scope Profile",
                row.name,
                "profile",
                canonical_label,
                update_modified=False,
            )


def create_default_scopes():
    if not frappe.db.table_exists("DCNET Permission Scope"):
        return

    seed_specs = [
        {
            "department_keywords": ["Kế toán", "Phòng Kế toán", "Accounting"],
            "manager_role": "Accounts Manager",
            "allowed_roles": ["Accounts User", "Accounts Manager"],
        },
    ]

    for spec in seed_specs:
        if not frappe.db.exists("Role", spec["manager_role"]):
            continue

        allowed_roles = [role for role in spec["allowed_roles"] if frappe.db.exists("Role", role)]
        if not allowed_roles:
            continue

        for department in find_departments(spec["department_keywords"]):
            scope_name = f"{department} / {spec['manager_role']}"
            if frappe.db.exists("DCNET Permission Scope", scope_name):
                continue

            scope = frappe.new_doc("DCNET Permission Scope")
            scope.scope_name = scope_name
            scope.enabled = 1
            scope.department = department
            scope.manager_role = spec["manager_role"]
            scope.user_type = "System User"
            scope.notes = SEED_NOTE
            for role in allowed_roles:
                scope.append("allowed_roles", {"role": role, "is_default": role.endswith("User")})
            scope.insert(ignore_permissions=True)


def cleanup_seeded_scopes():
    if not frappe.db.table_exists("DCNET Permission Scope"):
        return

    valid_departments = set()
    for keywords in [
        ["Kế toán", "Phòng Kế toán", "Accounting"],
    ]:
        valid_departments.update(find_departments(keywords))

    seeded_scopes = frappe.get_all(
        "DCNET Permission Scope",
        filters={"notes": SEED_NOTE},
        fields=["name", "department"],
    )
    for scope in seeded_scopes:
        if scope.department not in valid_departments:
            frappe.delete_doc("DCNET Permission Scope", scope.name, force=True, ignore_permissions=True)


def find_departments(keywords):
    departments = frappe.get_all("Department", fields=["name", "department_name"], order_by="name asc")
    matches = []
    normalized_keywords = [normalize_text(keyword) for keyword in keywords]

    for department in departments:
        base_names = {
            normalize_text(department.department_name or ""),
            normalize_text(str(department.name or "").split(" - ")[0]),
        }
        if any(base in normalized_keywords for base in base_names if base):
            matches.append(department.name)

    return choose_preferred_departments(matches)


def choose_preferred_departments(departments):
    if not departments:
        return []

    return [
        sorted(
            departments,
            key=lambda name: (
                0 if normalize_text(str(name).split(" - ")[0]).startswith("phong ") else 1,
                0 if " - " in str(name) else 1,
                -len(str(name)),
                str(name),
            ),
        )[0]
    ]


def normalize_text(value):
    value = str(value or "").lower()
    replacements = {
        "á": "a",
        "à": "a",
        "ả": "a",
        "ã": "a",
        "ạ": "a",
        "ă": "a",
        "ắ": "a",
        "ằ": "a",
        "ẳ": "a",
        "ẵ": "a",
        "ặ": "a",
        "â": "a",
        "ấ": "a",
        "ầ": "a",
        "ẩ": "a",
        "ẫ": "a",
        "ậ": "a",
        "é": "e",
        "è": "e",
        "ẻ": "e",
        "ẽ": "e",
        "ẹ": "e",
        "ê": "e",
        "ế": "e",
        "ề": "e",
        "ể": "e",
        "ễ": "e",
        "ệ": "e",
        "í": "i",
        "ì": "i",
        "ỉ": "i",
        "ĩ": "i",
        "ị": "i",
        "ó": "o",
        "ò": "o",
        "ỏ": "o",
        "õ": "o",
        "ọ": "o",
        "ô": "o",
        "ố": "o",
        "ồ": "o",
        "ổ": "o",
        "ỗ": "o",
        "ộ": "o",
        "ơ": "o",
        "ớ": "o",
        "ờ": "o",
        "ở": "o",
        "ỡ": "o",
        "ợ": "o",
        "ú": "u",
        "ù": "u",
        "ủ": "u",
        "ũ": "u",
        "ụ": "u",
        "ư": "u",
        "ứ": "u",
        "ừ": "u",
        "ử": "u",
        "ữ": "u",
        "ự": "u",
        "ý": "y",
        "ỳ": "y",
        "ỷ": "y",
        "ỹ": "y",
        "ỵ": "y",
        "đ": "d",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    return value
