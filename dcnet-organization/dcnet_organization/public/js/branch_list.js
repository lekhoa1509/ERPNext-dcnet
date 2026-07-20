// List view của Branch dựa vào realtime socket ("list_update") để tự thêm
// dòng mới sau khi lưu qua Quick Entry — nếu socket không kết nối được
// (proxy chặn, shield trình duyệt chặn cổng socket.io...) thì dòng mới chỉ
// hiện ra sau khi F5. Ghi đè nút "+ Add" để tự refresh list ngay sau khi
// insert thành công, không phụ thuộc realtime.
frappe.listview_settings["Branch"] = {
	onload(listview) {
		listview.settings.primary_action = () => {
			frappe.ui.form.make_quick_entry(listview.doctype, () => listview.refresh());
		};
	},
};
