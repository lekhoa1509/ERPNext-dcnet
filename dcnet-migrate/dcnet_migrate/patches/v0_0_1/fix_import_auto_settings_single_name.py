import frappe


def execute():
    old_settings = "MISA AI Import Settings"
    new_settings = "Import Auto Settings"

    if not frappe.db.exists("DocType", new_settings):
        return

    frappe.db.sql(
        """
        update `tabSingles`
        set doctype = %s
        where doctype = %s
        """,
        (new_settings, old_settings),
    )
    frappe.db.sql(
        """
        update `tabSingles`
        set value = %s
        where doctype = %s
          and field = 'name'
          and value = %s
        """,
        (new_settings, new_settings, old_settings),
    )

    frappe.db.sql(
        """
        update `tabWorkspace Shortcut`
        set type = 'URL',
            link_to = null,
            url = '/desk/import-auto-settings',
            doc_view = null
        where parent = 'Import Auto Home'
          and label = 'Cài đặt Import AI'
        """
    )
    frappe.db.sql(
        """
        update `tabWorkspace Sidebar Item`
        set link_type = 'URL',
            link_to = null,
            url = '/desk/import-auto-settings'
        where parent in ('Import Auto', 'Import Auto Home')
          and label = 'Cài đặt Import AI'
        """
    )

    frappe.clear_cache(doctype=new_settings)
