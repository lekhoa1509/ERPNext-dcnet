import frappe, json
frappe.set_user("Administrator")
from dcnet_crm.api import update_so_items
# submitted order
items=[{"item_code":"CC_GHEXOAY","item_name":"Ghe","qty":2,"uom":"Cái","rate":100000,"warehouse":"Stores - DCNET"}]
try:
    r=update_so_items("SAL-ORD-2026-00001", json.dumps(items))
    print("OK", r)
except Exception as e:
    print("ERRTYPE", type(e).__name__)
    print("ERR", str(e)[:300])
