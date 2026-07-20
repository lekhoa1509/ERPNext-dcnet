from __future__ import annotations

import json
import os

import frappe
from frappe.permissions import add_permission, update_permission_property


def after_install() -> None:
    """Chạy sau bench install-app: thiết lập workspace Desk icon và docs."""
    frappe.cache.delete_value("charts_for_country:Vietnam")
    _ensure_misa_migration_module()
    _sync_standard_docs()
    _sync_print_formats()
    _fix_workspace_labels()
    _sync_workspace_sidebar()
    _ensure_desktop_icon()
    _seed_treasury_settings()
    _seed_ccdc_categories()
    _ensure_branch_reference_permissions()
    _enforce_no_negative_stock()
    # Phase 1 (giathanh-tonghop-bctc) — new Settings seeds
    _seed_lcv_allocation_settings()
    _seed_period_closing_account_settings()
    _seed_bctc_mapping_templates()
    # role gate saves VN Accounting Settings — must run AFTER the seeds above
    # populate its reqd account fields, else fresh-site after_install hits MandatoryError
    _seed_workspace_role_gate()


def after_migrate() -> None:
    """Đảm bảo COA templates Việt Nam khả dụng sau migrate."""
    frappe.cache.delete_value("charts_for_country:Vietnam")
    _ensure_misa_migration_module()
    _sync_standard_docs()
    _sync_print_formats()
    _fix_workspace_labels()
    _sync_workspace_sidebar()
    _ensure_desktop_icon()
    _seed_treasury_settings()
    _seed_ccdc_categories()
    _disable_prepared_reports()
    _ensure_branch_reference_permissions()
    _backfill_ccdc_item_status()
    _set_default_workspace_for_accounts_users()
    _skip_asset_onboarding()
    _enforce_no_negative_stock()
    # Phase giathanh-tonghop-bctc: idempotent seeds for new Settings DocTypes
    _seed_lcv_allocation_settings()
    _seed_period_closing_account_settings()
    _seed_bctc_mapping_templates()
    _seed_project_costing_ux_flags()
    # MUST run last: re-applies admin-configured role gate AFTER fixture sync
    # would otherwise overwrite tabHas Role rows on Workspace VN Accounting.
    _seed_workspace_role_gate()
    _reapply_workspace_role_gate()


def _ensure_misa_migration_module() -> None:
    """Insert Module Def for Misa Migration if missing (post-install modules.txt additions)."""
    if not frappe.db.exists("Module Def", "Misa Migration"):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Misa Migration",
            "app_name": "vn_accounting",
            "custom": 0,
        }).insert(ignore_permissions=True)


def _sync_standard_docs() -> None:
    """Upsert Number Card and Dashboard Chart from JSON files (idempotent)."""
    app_path = os.path.dirname(__file__)
    for doctype, folder in [
        ("Number Card", "number_card"),
        ("Dashboard Chart", "dashboard_chart"),
    ]:
        folder_path = os.path.join(app_path, "vn_accounting", folder)
        if not os.path.isdir(folder_path):
            continue
        for subfolder in os.listdir(folder_path):
            json_path = os.path.join(folder_path, subfolder, f"{subfolder}.json")
            if not os.path.isfile(json_path):
                continue
            with open(json_path) as f:
                data = json.load(f)
            name = data.get("name")
            if not name:
                continue
            if frappe.db.exists(doctype, name):
                # Use db_set to bypass "Cannot edit Standard charts/cards" validation
                # Skip metadata fields and child tables (lists/dicts can't go through db_set)
                skip = {"doctype", "creation", "modified", "modified_by", "owner", "idx", "name"}
                updates = {
                    k: v for k, v in data.items()
                    if k not in skip and not isinstance(v, (list, dict))
                }
                for field, val in updates.items():
                    frappe.db.set_value(doctype, name, field, val, update_modified=False)
                print(f"  ↻ {doctype}: {name}")
            else:
                doc = frappe.get_doc(data)
                doc.flags.ignore_permissions = True
                doc.flags.ignore_links = True
                doc.flags.ignore_validate = True
                doc.insert()
                print(f"  ✓ {doctype}: {name}")
    frappe.db.commit()


def _sync_print_formats() -> None:
    """Sync Print Format HTML from fixture JSON into DB.

    Frappe fixture import (data_import=True) runs validate() which blocks
    updates to existing Print Formats. This bypasses that by writing HTML
    directly via db_set.
    """
    app_path = os.path.dirname(__file__)
    pf_dir = os.path.join(app_path, "vn_accounting", "print_format")
    if not os.path.isdir(pf_dir):
        return
    for subfolder in os.listdir(pf_dir):
        json_path = os.path.join(pf_dir, subfolder, f"{subfolder}.json")
        if not os.path.isfile(json_path):
            continue
        with open(json_path) as f:
            data = json.load(f)
        name = data.get("name")
        html = data.get("html")
        if not name or not html:
            continue
        if frappe.db.exists("Print Format", name):
            db_html = frappe.db.get_value("Print Format", name, "html")
            if db_html != html:
                frappe.db.set_value("Print Format", name, "html", html, update_modified=False)
                print(f"  ↻ Print Format: {name}")
        else:
            doc = frappe.get_doc(data)
            doc.flags.ignore_permissions = True
            doc.flags.ignore_validate = True
            doc.insert()
            print(f"  ✓ Print Format: {name}")
    frappe.db.commit()


def _sync_workspace_sidebar() -> None:
    """Re-sync Workspace Sidebar items từ JSON fixture (idempotent).

    Đảm bảo nút Home và tất cả items luôn đồng bộ với source JSON sau mỗi migrate.
    """
    app_path = os.path.dirname(__file__)
    sidebar_json = os.path.join(app_path, "workspace_sidebar", "vn_accounting.json")
    if not os.path.isfile(sidebar_json):
        return
    if not frappe.db.exists("Workspace Sidebar", "VN Accounting"):
        return

    with open(sidebar_json) as f:
        data = json.load(f)

    doc = frappe.get_doc("Workspace Sidebar", "VN Accounting")
    doc.set("items", data.get("items", []))
    doc.flags.ignore_permissions = True
    doc.flags.ignore_links = True
    doc.save()
    frappe.db.commit()
    print("  ✓ Workspace Sidebar: VN Accounting synced")


def _ensure_desktop_icon() -> None:
    """Create/update Desktop Icon for VN Accounting on Desk home (idempotent).

    Label MUST be ASCII 'VN Accounting' (not Vietnamese diacritics) because
    Frappe desktop.js looks up workspace_sidebar_item[label.toLowerCase()]
    and the key is 'ke toan vn' (ASCII). Diacritics in label causes KeyError
    and the icon is hidden.

    link_type MUST be 'Workspace' (not 'Workspace Sidebar') because Frappe
    desktop.js get_route() only handles 'External', 'Workspace', 'DocType'.
    """
    desired = {
        "label": "VN Accounting",
        "icon": "accounting",
        "link_type": "Workspace Sidebar",
        "link_to": "VN Accounting",
        "hidden": 0,
    }

    # Scan for known variants — Frappe auto-names Desktop Icon from label, so
    # the canonical row is named "VN Accounting"; older code mistakenly used
    # the Vietnamese-diacritic "Kế Toán VN" as the lookup key, which never
    # matched the auto-generated name and caused DuplicateEntryError on
    # subsequent migrates.
    for variant in ("VN Accounting", "Kế Toán VN", "Ke Toan VN"):
        if frappe.db.exists("Desktop Icon", variant):
            doc = frappe.get_doc("Desktop Icon", variant)
            changed = False
            for field, val in desired.items():
                if doc.get(field) != val:
                    doc.set(field, val)
                    changed = True
            if changed:
                doc.flags.ignore_permissions = True
                doc.save()
                frappe.db.commit()
                print(f"  ↻ Desktop Icon: {variant} updated")
            return

    doc = frappe.get_doc({
        "doctype": "Desktop Icon",
        "parent_icon": "",
        "idx": 1,
        **desired,
    })
    doc.flags.ignore_permissions = True
    doc.insert()
    frappe.db.commit()
    print("  ✓ Desktop Icon: VN Accounting")


def _seed_treasury_settings() -> None:
    """Seed VN Accounting Settings with default accounts from VN COA."""
    if not frappe.db.exists("DocType", "VN Accounting Settings"):
        return

    settings = frappe.get_doc("VN Accounting Settings")

    company = frappe.defaults.get_defaults().get("company")
    if not company:
        companies = frappe.get_all("Company", filters={"country": "Vietnam"}, limit=1)
        if not companies:
            return
        company = companies[0].name

    prefix_map = {
        "default_deposit_account": "1281",
        "default_interest_income_account": "515",
        "default_loan_account": "3411",
        "default_interest_expense_account": "635",
    }

    changed = False
    for field, prefix in prefix_map.items():
        if not settings.get(field):
            account = frappe.db.get_value(
                "Account",
                {"account_name": ["like", f"{prefix}%"], "company": company, "is_group": 0},
                "name",
            )
            if account:
                settings.set(field, account)
                changed = True

    if changed:
        settings.flags.ignore_permissions = True
        settings.save()
        frappe.db.commit()
        print("  \u2713 VN Accounting Settings: defaults seeded")


def _seed_ccdc_categories() -> None:
    """Seed 5 default CCDC Category records (idempotent).

    Spec §7.5: 5 categories required before CCDC Item can be created.
    """
    if not frappe.db.exists("DocType", "CCDC Category"):
        return

    company = frappe.defaults.get_defaults().get("company")
    if not company:
        companies = frappe.get_all("Company", filters={"country": "Vietnam"}, limit=1)
        if not companies:
            return
        company = companies[0].name

    def _acc(prefix: str) -> str | None:
        return frappe.db.get_value(
            "Account",
            {"account_name": ["like", f"{prefix}%"], "company": company, "is_group": 0},
            "name",
        )

    cost_153 = _acc("153")
    prepay_242 = _acc("242")
    expense_642 = _acc("642") or _acc("641") or _acc("627")

    categories = [
        {"category_name": "Bàn ghế văn phòng", "useful_period_default": 24},
        {"category_name": "Máy tính & thiết bị IT", "useful_period_default": 36},
        {"category_name": "Dụng cụ sản xuất", "useful_period_default": 24},
        {"category_name": "Đồ bảo hộ lao động", "useful_period_default": 12},
        {"category_name": "CCDC khác", "useful_period_default": 24},
    ]

    for cat in categories:
        if frappe.db.exists("CCDC Category", {"category_name": cat["category_name"]}):
            continue
        doc = frappe.get_doc({
            "doctype": "CCDC Category",
            "category_name": cat["category_name"],
            "parent_category_account": cost_153,
            "expense_account_default": expense_642,
            "useful_period_default": cat["useful_period_default"],
            "is_group": 0,
        })
        doc.flags.ignore_permissions = True
        doc.flags.ignore_mandatory = True
        doc.insert()
        print(f"  ✓ CCDC Category: {cat['category_name']}")
    frappe.db.commit()


def _disable_prepared_reports() -> None:
    """Disable prepared_report on ERPNext reports that need background workers.

    Dev benches without workers return empty results for prepared reports.
    This ensures all reports run directly on request.
    """
    updated = frappe.db.sql(
        """UPDATE `tabReport` SET prepared_report = 0
        WHERE prepared_report = 1"""
    )
    count = frappe.db.sql("SELECT ROW_COUNT()")[0][0]
    if count:
        frappe.db.commit()
        print(f"  ✓ Disabled prepared_report on {count} reports")

    # Reports that emit a manual total row from execute() must NOT have Frappe's
    # auto-total enabled — otherwise both totals overlay and meaningless sums
    # (Int month counts, Percent rates, snapshot balances) appear.
    # Frappe's report sync only seeds add_total_row on insert, never updates it,
    # so existing installs need this idempotent SQL alignment.
    frappe.db.sql(
        """UPDATE `tabReport` SET add_total_row = 0
        WHERE name IN ('Term Deposit Summary', 'Bank Loan Summary')
          AND add_total_row != 0"""
    )
    if frappe.db.sql("SELECT ROW_COUNT()")[0][0]:
        frappe.db.commit()
        print("  ✓ Aligned add_total_row=0 on treasury summary reports")


def _enforce_no_negative_stock() -> None:
    """Set Stock Settings.allow_negative_stock = 0 (chief accountant requirement).

    DCNet bán thiết bị + công trình → mọi giao dịch xuất kho phải có tồn dương.
    Nếu cần tạm cho phép âm cho 1 nghiệp vụ đặc biệt (gia công, tạm xuất tái
    nhập), kế toán có thể bật lại tay tại Stock Settings — hook chỉ enforce
    default, không lock cứng.

    Idempotent: chỉ ghi khi giá trị hiện tại != 0.
    """
    if not frappe.db.exists("DocType", "Stock Settings"):
        return
    current = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")
    if current != 0:
        frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 0)
        frappe.db.commit()
        print("  ✓ Stock Settings: allow_negative_stock = 0")


def _fix_workspace_labels() -> None:
    """Ensure workspace is visible on Desk with correct title and module.

    Frappe fixture import may reset title/label to Vietnamese (with diacritics),
    causing the Desk home card URL to be generated as 'kế-toán-vn' which 404s.
    Keep title and label ASCII so slug('VN Accounting') → 'ke-toan-vn' matches
    the workspace name. Vietnamese text shows in the sidebar title separately.
    """
    if frappe.db.exists("Workspace", "VN Accounting"):
        ws = frappe.get_doc("Workspace", "VN Accounting")
        ws.title = "VN Accounting"
        ws.label = "VN Accounting"
        ws.public = 1
        ws.is_hidden = 0
        ws.flags.ignore_permissions = True
        ws.flags.ignore_links = True
        ws.save()

    if frappe.db.exists("Workspace Sidebar", "VN Accounting"):
        sidebar = frappe.get_doc("Workspace Sidebar", "VN Accounting")
        sidebar.title = "VN Accounting"
        sidebar.module = "Accounts"
        sidebar.flags.ignore_permissions = True
        sidebar.flags.ignore_links = True
        sidebar.save()

    frappe.db.commit()


def _ensure_branch_reference_permissions() -> None:
    """Give accounting roles minimal read access to Branch for Link/UI rendering.

    Without this, Branch link fields in branch cash forms and reports trigger
    "Insufficient Permission for Branch" for non-HR accounting users.
    """
    changed = False

    for role in ("Accounts User", "Accounts Manager"):
        if not frappe.db.get_value(
            "Custom DocPerm",
            {"parent": "Branch", "role": role, "permlevel": 0, "if_owner": 0},
            "name",
        ):
            add_permission("Branch", role, 0, "read")
            changed = True

        for ptype, value in (("read", 1), ("select", 1), ("report", 0)):
            update_permission_property(
                "Branch",
                role,
                0,
                ptype,
                value=value,
                validate=False,
            )
            changed = True

    if changed:
        frappe.clear_cache(doctype="Branch")
        frappe.db.commit()


def _backfill_ccdc_item_status() -> None:
    """Backfill status for CCDC Item records submitted before the state-machine code shipped.

    Reconciles 4-state machine (PM-08): submitted CCDC Items stuck on 'Mới mua'
    are bumped to the correct state derived from allocation/writeoff history:
      - Has CCDC Writeoff submitted → 'Đã ghi giảm'
      - All allocation entries posted → 'Hết phân bổ'
      - Otherwise → 'Đang sử dụng'
    """
    stuck = frappe.db.sql(
        "SELECT name FROM `tabCCDC Item` WHERE docstatus = 1 AND status = 'Mới mua'",
        as_dict=True,
    )
    if not stuck:
        return

    for row in stuck:
        item = row["name"]
        has_writeoff = frappe.db.exists(
            "CCDC Writeoff", {"ccdc_item": item, "docstatus": 1}
        )
        if has_writeoff:
            new_status = "Đã ghi giảm"
        else:
            pending = frappe.db.sql(
                """
                SELECT COUNT(*) FROM `tabCCDC Allocation Entry` ae
                JOIN `tabCCDC Allocation Schedule` s ON ae.parent = s.name
                WHERE s.ccdc_item = %s AND ae.status = 'Pending'
                """,
                item,
            )[0][0]
            total = frappe.db.sql(
                """
                SELECT COUNT(*) FROM `tabCCDC Allocation Entry` ae
                JOIN `tabCCDC Allocation Schedule` s ON ae.parent = s.name
                WHERE s.ccdc_item = %s
                """,
                item,
            )[0][0]
            if total > 0 and pending == 0:
                new_status = "Hết phân bổ"
            else:
                new_status = "Đang sử dụng"
        frappe.db.set_value(
            "CCDC Item", item, "status", new_status, update_modified=False
        )
    frappe.db.commit()


def _set_default_workspace_for_accounts_users() -> None:
    """Set default_workspace = 'VN Accounting' for Accounts User role users who have none set.

    Idempotent: only updates users whose default_workspace is empty so existing
    personal preferences are not overwritten.
    """
    users_with_role = frappe.get_all(
        "Has Role",
        filters={"role": "Accounts User", "parenttype": "User"},
        pluck="parent",
    )
    if not users_with_role:
        return
    for user in users_with_role:
        if not frappe.db.get_value("User", user, "default_workspace"):
            frappe.db.set_value(
                "User", user, "default_workspace", "VN Accounting", update_modified=False
            )


def _skip_asset_onboarding() -> None:
    """Mark all ERPNext Asset Onboarding steps as skipped.

    The English-language Getting Started wizard is irrelevant for Vietnamese accounting users.
    Suppressing it on install/migrate prevents it from interrupting KTV (Kế Toán Viên) workflow
    when they open Asset Repair or other asset forms.
    """
    if not frappe.db.exists("Module Onboarding", "Asset Onboarding"):
        return
    frappe.db.set_value(
        "Module Onboarding", "Asset Onboarding", "is_complete", 1, update_modified=False
    )
    # Onboarding Step doesn't have a direct module_onboarding link field;
    # steps are listed in Module Onboarding's child table "steps".
    step_names = frappe.db.get_all(
        "Onboarding Step Map",
        filters={"parent": "Asset Onboarding", "parenttype": "Module Onboarding"},
        pluck="step",
    )
    for step in step_names:
        frappe.db.set_value("Onboarding Step", step, "is_skipped", 1, update_modified=False)


def _seed_lcv_allocation_settings() -> None:
    if not frappe.db.exists("DocType", "LCV Allocation Settings"):
        return
    from vn_accounting.landed_cost.seed import (
        seed_lcv_allocation_settings,
        resolve_default_accounts,
    )
    seed_lcv_allocation_settings()
    # Auto-resolve default accounts from COA per Company (idempotent, no-overwrite)
    try:
        resolve_default_accounts(overwrite=False)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "LCV resolve_default_accounts")


def _seed_period_closing_account_settings() -> None:
    if not frappe.db.exists("DocType", "VN Accounting Settings"):
        return
    from vn_accounting.period_closing.seed import seed_period_closing_account_settings
    seed_period_closing_account_settings()


def _seed_bctc_mapping_templates() -> None:
    if not frappe.db.exists("DocType", "BCTC Mapping Template"):
        return
    from vn_accounting.financial_reporting.bctc_template_seed import seed_bctc_mapping_templates
    seed_bctc_mapping_templates()


def _seed_project_costing_ux_flags() -> None:
    """Default auto_show_stage_picker_on_source_docs = 1 on existing sites.

    JSON `default: "1"` only applies on first doc creation; existing Single
    docs keep NULL for newly-added fields. Backfill so KTT sees the stage
    picker by default after upgrade.
    """
    if not frappe.db.exists("DocType", "VN Accounting Settings"):
        return
    meta = frappe.get_meta("VN Accounting Settings")
    if not meta.has_field("auto_show_stage_picker_on_source_docs"):
        return
    cur = frappe.db.get_single_value(
        "VN Accounting Settings", "auto_show_stage_picker_on_source_docs"
    )
    if cur is None or cur == "":
        frappe.db.set_single_value(
            "VN Accounting Settings", "auto_show_stage_picker_on_source_docs", 1
        )


def _seed_workspace_role_gate() -> None:
    """Seed default allowed_workspace_roles in VN Accounting Settings if empty.

    Default: Accounts User, Accounts Manager, Auditor — matches ERPNext convention.
    Idempotent: only seeds when the table is empty (preserves admin customization).
    """
    if not frappe.db.exists("DocType", "VN Accounting Settings"):
        return  # DocType not yet migrated
    settings = frappe.get_single("VN Accounting Settings")
    if settings.get("allowed_workspace_roles"):
        return  # admin already configured
    for role in ("Accounts User", "Accounts Manager", "Auditor"):
        # Skip roles that don't exist in the system
        if not frappe.db.exists("Role", role):
            continue
        settings.append("allowed_workspace_roles", {"role": role})
    if not settings.get("enforce_workspace_role_gate"):
        settings.enforce_workspace_role_gate = 1
    settings.flags.ignore_mandatory = True
    settings.save(ignore_permissions=True)


def _reapply_workspace_role_gate() -> None:
    """Re-sync workspace.roles from settings AFTER fixture import overwrites.

    Runs as the LAST step of after_migrate. The fixture sync earlier in migrate
    would otherwise wipe admin-configured roles back to fixture defaults. By
    re-running the on_update hook logic here, we restore the admin's intent.
    """
    if not frappe.db.exists("DocType", "VN Accounting Settings"):
        return
    if not frappe.db.exists("Workspace", "VN Accounting"):
        return
    from vn_accounting.vn_accounting.doctype.vn_accounting_settings.vn_accounting_settings import (
        _sync_workspace_role_gate,
    )
    settings = frappe.get_single("VN Accounting Settings")
    _sync_workspace_role_gate(settings)
