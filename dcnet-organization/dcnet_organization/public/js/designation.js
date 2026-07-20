// Designation: chọn phòng ban (tuỳ chọn) — hiện mọi phòng ban chưa bị vô hiệu hoá.
// Dùng ["!=", 1] thay vì {disabled: 0} để không loại nhầm phòng ban có disabled = NULL
// (tạo qua API/import hoặc trước khi có field). Server vẫn chặn phòng ban đã disable khi lưu.
frappe.ui.form.on("Designation", {
	refresh(frm) {
		frm.set_query("department", () => ({
			filters: { disabled: ["!=", 1] },
		}));
	},
});
