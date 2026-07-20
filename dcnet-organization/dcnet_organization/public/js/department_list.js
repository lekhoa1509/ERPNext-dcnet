// Xem giải thích ở branch_list.js — refresh list ngay sau khi thêm mới,
// không phụ thuộc realtime socket ("list_update").
frappe.listview_settings["Department"] = {
	onload(listview) {
		listview.settings.primary_action = () => {
			frappe.ui.form.make_quick_entry(listview.doctype, () => listview.refresh());
		};
	},
};
