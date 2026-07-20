frappe.ui.form.on("VN Accounting Branch Menu Access", {
	async refresh(frm) {
		updateIntro(frm);
		frm.add_custom_button(__("Đồng bộ menu chuẩn"), async () => {
			await syncSidebarItems(frm);
		});

		if (!frm.__initialSidebarSyncDone && frm.doc.branch && !hasMenuItems(frm)) {
			frm.__initialSidebarSyncDone = true;
			await syncSidebarItems(frm);
		}
	},

	async branch(frm) {
		if (frm.doc.branch && !hasMenuItems(frm)) {
			await syncSidebarItems(frm);
		}
	},

	restrict_sidebar_items(frm) {
		updateIntro(frm);
	},
});

function hasMenuItems(frm) {
	return Boolean(frm.doc.menu_items && frm.doc.menu_items.length);
}

async function syncSidebarItems(frm) {
	await frm.call("sync_sidebar_items");
	frm.refresh_field("menu_items");
}

function updateIntro(frm) {
	if (frm.doc.restrict_sidebar_items) {
		frm.set_intro(
			__(
				"Chỉ các menu được đánh dấu trong bảng bên dưới mới hiển thị cho user thuộc chi nhánh này trong module Kế Toán VN."
			),
			"orange"
		);
		return;
	}

	frm.set_intro(
		__(
			"Nếu chưa bật giới hạn menu, chi nhánh sẽ thấy toàn bộ menu Kế Toán VN mà role hiện tại cho phép."
		),
		"blue"
	);
}
