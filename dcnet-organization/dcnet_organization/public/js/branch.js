// Branch: chi nhánh có thể (tuỳ chọn) thuộc một công ty
// (field `company` do dcnet_organization thêm vào Branch qua Custom Field).
// Không cần filter đặc biệt cho Company; giữ file để mở rộng UX sau này.
frappe.ui.form.on("Branch", {
	// placeholder cho tuỳ biến tương lai (vd: mặc định công ty theo user).
});
