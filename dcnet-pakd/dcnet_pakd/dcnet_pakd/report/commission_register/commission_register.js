// Commission Register — sổ hoa hồng NVKD.
// only_payable mặc định BẬT → mở từ sidebar là thấy ngay worklist "Phải trả
// NVKD" (Pending + kỳ billing đã Paid). Bỏ tick để xem toàn sổ; khi đó filter
// "Trạng thái" + "Tháng lương" mới có tác dụng.
frappe.query_reports["Commission Register"] = {
	filters: [
		{
			fieldname: "only_payable",
			label: __("Chỉ khoản đã thu tiền KH"),
			fieldtype: "Check",
			default: 1,
		},
		{
			fieldname: "sales_person",
			label: __("NVKD"),
			fieldtype: "Link",
			options: "Employee",
		},
		{
			fieldname: "component",
			label: __("Khoản"),
			fieldtype: "Select",
			options: "\nSales Commission\nLicense Fee",
		},
		{
			fieldname: "pakd",
			label: __("PAKD"),
			fieldtype: "Link",
			options: "Phuong An Kinh Doanh",
		},
		{
			fieldname: "state",
			label: __("Trạng thái (chỉ khi bỏ tick 'cần thanh toán')"),
			fieldtype: "Select",
			options: "\nPending\nPosted\nCancelled\nSkipped",
		},
		{
			fieldname: "payroll_month",
			label: __("Tháng lương"),
			fieldtype: "Data",
			description: __("YYYY-MM"),
		},
	],
};
