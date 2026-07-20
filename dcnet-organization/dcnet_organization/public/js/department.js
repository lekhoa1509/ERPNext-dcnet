// Department: chọn chi nhánh (tuỳ chọn), lọc theo công ty của phòng ban.
frappe.ui.form.on("Department", {
	refresh(frm) {
		// Danh sách Branch chỉ hiện chi nhánh thuộc công ty đã chọn.
		frm.set_query("branch", () => {
			if (frm.doc.company) {
				return { filters: { company: frm.doc.company } };
			}
			return {};
		});
	},

	company(frm) {
		// Đổi công ty -> nếu chi nhánh cũ không còn thuộc công ty này thì xoá.
		if (frm.doc.branch && frm.doc.company) {
			frappe.db.get_value("Branch", frm.doc.branch, "company").then((r) => {
				const branch_company = r.message && r.message.company;
				if (branch_company && branch_company !== frm.doc.company) {
					frm.set_value("branch", null);
				}
			});
		}
	},

	branch(frm) {
		// Chọn chi nhánh trước khi có công ty -> tự điền công ty từ chi nhánh.
		if (frm.doc.branch && !frm.doc.company) {
			frappe.db.get_value("Branch", frm.doc.branch, "company").then((r) => {
				const branch_company = r.message && r.message.company;
				if (branch_company) {
					frm.set_value("company", branch_company);
				}
			});
		}
	},
});
