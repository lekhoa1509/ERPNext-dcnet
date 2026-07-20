// Auto Generated Docs Pending (display: "Tài liệu tự động chờ duyệt" via vi.csv) — filters + row navigation
frappe.query_reports["Auto Generated Docs Pending"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Công ty"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("Từ ngày"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(), -90),
		},
		{
			fieldname: "to_date",
			label: __("Đến ngày"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "doc_status",
			label: __("Trạng thái"),
			fieldtype: "MultiSelectList",
			default: ["Bản nháp"],
			get_data: () => [
				{ value: "Bản nháp", description: __("Đang chờ kế toán duyệt và ghi sổ") },
				{ value: "Đã ghi sổ", description: __("Đã ghi sổ — để biết và kiểm tra khi cần") },
				{ value: "Đã hủy", description: __("Đã hủy — cần kiểm tra lý do") },
			],
			description: __("Mặc định chỉ hiện Bản nháp. Mở rộng để xem toàn bộ vòng đời tài liệu."),
		},
		{
			fieldname: "loai",
			label: __("Loại tài liệu"),
			fieldtype: "MultiSelectList",
			get_data: () => frappe.call({
				method: "vn_accounting.auto_source.get_source_labels_for_filter",
				freeze: false,
			}).then(r => (r.message || []).map(v => ({ value: v, description: "" }))),
			description: __("Để trống nghĩa là chọn tất cả các loại"),
		},
		{
			fieldname: "only_overdue",
			label: __("Chỉ hiện quá hạn duyệt"),
			fieldtype: "Check",
			default: 0,
		},
		{
			fieldname: "overdue_days",
			label: __("Ngưỡng quá hạn (ngày)"),
			fieldtype: "Int",
			default: 7,
			depends_on: "eval:doc.only_overdue",
		},
	],

	formatter(value, row, column, data, default_formatter) {
		const v = default_formatter(value, row, column, data);
		if (column.fieldname === "days_waiting" && data && typeof data.days_waiting === "number") {
			// Only highlight days_waiting for drafts — for submitted/cancelled it's just informational.
			if (data.docstatus === 0) {
				if (data.days_waiting >= 30) {
					return `<span style="color:#d9534f; font-weight:600;">${data.days_waiting} ⚠⚠</span>`;
				}
				if (data.days_waiting >= 7) {
					return `<span style="color:#f0ad4e; font-weight:600;">${data.days_waiting} ⚠</span>`;
				}
			}
		}
		if (column.fieldname === "status_label" && data && data.status_label) {
			if (data.docstatus === 0) {
				return `<span style="background:#fffbea; color:#735c0f; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600;">${data.status_label}</span>`;
			}
			if (data.docstatus === 1) {
				return `<span style="background:#e6f6e6; color:#1a7f37; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600;">${data.status_label}</span>`;
			}
			if (data.docstatus === 2) {
				return `<span style="background:#ffebe9; color:#cf222e; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600;">${data.status_label}</span>`;
			}
		}
		if (column.fieldname === "action" && data && data.action) {
			if (data.docstatus === 0) {
				return `<span style="color:#0366d6; font-weight:500;">${data.action}</span>`;
			}
			if (data.docstatus === 2) {
				return `<span style="color:#cf222e;">${data.action}</span>`;
			}
			return `<span style="color:#586069;">${data.action}</span>`;
		}
		return v;
	},
};
