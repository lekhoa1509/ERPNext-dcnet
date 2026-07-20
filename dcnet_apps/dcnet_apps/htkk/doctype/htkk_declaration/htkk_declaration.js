// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("HTKK Declaration", {
	setup(frm) {
		// Dynamically load declaration types from API
		frappe.call({
			method: "dcnet_apps.htkk.api.get_supported_declarations",
			async: false,
			callback(r) {
				if (r.message) {
					const options = r.message.map(d => d.code).join("\n");
					frm.set_df_property("declaration_type", "options", options);
				}
			}
		});
	},

	calculate_btn(frm) {
		// Lưu trước để đảm bảo import_vat_account, manual fields đã được ghi
		frm.save().then(() => {
			return frm.call({
				method: "calculate",
				freeze: true,
				freeze_message: __("Đang tính toán từ chứng từ..."),
			});
		}).then(() => {
			frm.reload_doc();
		});
	},

	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Chỉnh sửa tờ khai"), () => {
				window.open(`/htkk?id=${frm.doc.name}`, "_blank");
			}, null, "success");

			frm.add_custom_button(__("Xem trước"), () => {
				frappe.call({
					method: "dcnet_apps.htkk.api.preview_declaration",
					args: { declaration_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Đang tính toán chỉ tiêu..."),
					callback(r) {
						if (r.message) {
							frm.events.show_preview_dialog(frm, r.message);
						}
					},
				});
			});

			frm.add_custom_button(
				__("Xuất XML"),
				() => {
					frappe.confirm(
						__("Xuất file XML cho tờ khai này? Trạng thái sẽ chuyển sang 'Đã xuất'."),
						() => {
							frappe.call({
								method: "dcnet_apps.htkk.api.export_declaration",
								args: { declaration_name: frm.doc.name },
								freeze: true,
								freeze_message: __("Đang tạo file XML..."),
								callback(r) {
									if (r.message) {
										frm.reload_doc();
										frappe.show_alert({
											message: r.message.message,
											indicator: "green",
										});
									}
								},
							});
						}
					);
				},
				null,
				"primary"
			);

			// Download button if already exported
			if (frm.doc.generated_xml) {
				frm.add_custom_button(__("Tải XML"), () => {
					window.open(
						`/api/method/dcnet_apps.htkk.api.download_declaration?declaration_name=${frm.doc.name}`
					);
				});
			}
		}
	},

	period_type(frm) {
		if (frm.doc.period_type === "Năm") {
			frm.set_value("period", 0);
		} else {
			frm.set_value("period", "");
		}
	},

	company(frm) {
		frm.events.fetch_carried_forward(frm);
	},

	period(frm) {
		frm.events.fetch_carried_forward(frm);
	},

	year(frm) {
		frm.events.fetch_carried_forward(frm);
	},

	fetch_carried_forward(frm) {
		if (
			frm.doc.declaration_type === "01/GTGT" &&
			frm.doc.company &&
			frm.doc.period_type &&
			frm.doc.period &&
			frm.doc.year
		) {
			frappe.call({
				method: "dcnet_apps.htkk.api.get_carried_forward_vat",
				args: {
					company: frm.doc.company,
					period_type: frm.doc.period_type,
					period: frm.doc.period,
					year: frm.doc.year,
				},
				callback(r) {
					if (r.message && r.message.vat_carried_forward) {
						frm.set_value(
							"vat_carried_forward",
							r.message.vat_carried_forward
						);
					}
				},
			});
		}
	},

	show_preview_dialog(frm, data) {
		let chi_tieu = data.chi_tieu || {};
		let phu_luc = data.phu_luc || {};

		// Build chi tiêu table
		let ct_html = `<table class="table table-bordered table-sm">
			<thead><tr>
				<th style="width:80px">Chỉ tiêu</th>
				<th>Giá trị</th>
			</tr></thead><tbody>`;

		const ct_labels = {
			ct21: "Không phát sinh hoạt động MHHDV",
			ct22: "Thuế GTGT còn khấu trừ kỳ trước",
			ct23: "Giá trị HHDV mua vào",
			ct24: "Thuế GTGT của HHDV mua vào",
			ct25: "Thuế GTGT được khấu trừ",
			ct26: "DT bán ra không chịu thuế",
			ct27: "Thuế GTGT KCT",
			ct29: "DT thuế suất 0%",
			ct30: "DT thuế suất 5%",
			ct31: "Thuế GTGT 5%",
			ct32: "DT thuế suất 8%",
			ct32a: "Thuế GTGT 8%",
			ct33: "DT thuế suất 10%",
			ct33a: "Thuế GTGT 10%",
			ct34: "Tổng DT HHDV bán ra",
			ct35: "Tổng thuế GTGT bán ra",
			ct36: "Tổng thuế GTGT được khấu trừ",
			ct37: "Điều chỉnh tăng",
			ct38: "Điều chỉnh giảm",
			ct39: "Thuế GTGT phải nộp trong kỳ",
			ct40: "Thuế GTGT chưa khấu trừ hết",
			ct41: "Thuế GTGT đề nghị hoàn",
			ct42: "Thuế GTGT còn khấu trừ chuyển kỳ sau",
			ct43: "Giá trị lưu (→ CT22 kỳ sau)",
		};

		const ct_order = [
			"ct21", "ct22", "ct23", "ct24", "ct25",
			"ct26", "ct27", "ct29",
			"ct30", "ct31", "ct32", "ct32a", "ct33", "ct33a",
			"ct34", "ct35", "ct36",
			"ct37", "ct38", "ct39", "ct40", "ct41", "ct42", "ct43",
		];

		const highlight = ["ct34", "ct35", "ct36", "ct39", "ct40", "ct42"];

		for (let key of ct_order) {
			if (chi_tieu[key] === undefined) continue;
			let val = chi_tieu[key];
			let label = ct_labels[key] || key;
			let formatted = typeof val === "number"
				? format_currency(val, frappe.boot.sysdefaults.currency)
				: val;
			let bold = highlight.includes(key) ? "font-weight:bold;" : "";

			ct_html += `<tr style="${bold}">
				<td>${key.toUpperCase()}</td>
				<td>${label}</td>
				<td class="text-right">${formatted}</td>
			</tr>`;
		}
		ct_html += "</tbody></table>";

		// Build phu luc summary
		let pl_html = "";
		for (let [pl_name, rows] of Object.entries(phu_luc)) {
			let label = pl_name.replace(/_/g, " ");
			pl_html += `<h6 class="mt-3">${label} (${rows.length} dòng)</h6>`;
			if (rows.length > 0) {
				pl_html += `<table class="table table-bordered table-sm">
					<thead><tr>
						<th>#</th><th>Số HĐ</th><th>Ngày</th>
						<th>Tên</th><th>MST</th>
						<th class="text-right">DT chưa thuế</th>
						<th>TS</th>
						<th class="text-right">Tiền thuế</th>
					</tr></thead><tbody>`;

				let max_show = Math.min(rows.length, 20);
				for (let i = 0; i < max_show; i++) {
					let r = rows[i];
					pl_html += `<tr>
						<td>${i + 1}</td>
						<td>${r.SHDon || ""}</td>
						<td>${r.NLap || ""}</td>
						<td>${r.NMua || r.NBan || ""}</td>
						<td>${r.MST || ""}</td>
						<td class="text-right">${format_currency(r.DThuaKCT || 0)}</td>
						<td>${r.TSuat || ""}</td>
						<td class="text-right">${format_currency(r.TienThue || 0)}</td>
					</tr>`;
				}
				if (rows.length > 20) {
					pl_html += `<tr><td colspan="8" class="text-muted text-center">
						... và ${rows.length - 20} dòng nữa
					</td></tr>`;
				}
				pl_html += "</tbody></table>";
			}
		}

		let dialog = new frappe.ui.Dialog({
			title: __("Xem trước tờ khai {0}", [frm.doc.declaration_type]),
			size: "extra-large",
			fields: [
				{
					fieldtype: "HTML",
					fieldname: "preview_content",
					options: `
						<h5>Chỉ tiêu tờ khai chính</h5>
						${ct_html}
						${pl_html ? "<h5 class='mt-4'>Phụ lục</h5>" + pl_html : ""}
					`,
				},
			],
		});
		dialog.show();
	},
});
