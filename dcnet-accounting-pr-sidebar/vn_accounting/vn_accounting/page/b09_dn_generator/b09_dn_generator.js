// B09-DN Generator — multi-sheet Excel for Thuyết minh BCTC
frappe.pages["b09-dn-generator"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Thuyết minh BCTC (B09-DN)"),
        single_column: true
    });

    const help_html = `
        <div class="alert alert-info" style="margin-bottom:16px;">
            <strong>${__("Hướng dẫn:")}</strong>
            ${__("Sinh khung Thuyết minh BCTC (B09-DN) theo Thông tư 99/2025/TT-BTC. App tự fill phần số liệu (sheet 5.x chi tiết). Kế toán trưởng điền văn xuôi vào sheet 1 (đặc điểm DN, chính sách kế toán) trước khi nộp. Ô nền xám: App đã điền, không xóa. Ô nền trắng: Kế toán cần điền thêm.")}
        </div>`;

    const form_html = `
        <div style="max-width:540px; margin: 16px auto; background:#fff; border:1px solid #d1d8dd; border-radius:8px; padding:24px;">
            <div id="b09-help-panel">${help_html}</div>
            <div class="form-group">
                <label class="control-label">${__("Công ty")}<span class="reqd"> *</span></label>
                <div id="field-company"></div>
                <p class="help-block">${__("Chọn công ty cần sinh B09-DN.")}</p>
            </div>
            <div class="form-group">
                <label class="control-label">${__("Năm tài chính")}<span class="reqd"> *</span></label>
                <div id="field-fiscal-year"></div>
                <p class="help-block">${__("Chọn năm tài chính. Dữ liệu sheet chi tiết sẽ tổng hợp theo niên độ này.")}</p>
            </div>
            <div style="margin-top:20px; display:flex; gap:12px;">
                <button class="btn btn-primary" id="btn-generate-b09">
                    ${__("Sinh file B09-DN")}
                </button>
                <span id="b09-spinner" style="display:none; align-self:center;">
                    <i class="fa fa-spinner fa-spin"></i> ${__("Đang tạo file...")}
                </span>
            </div>
            <div id="b09-result" style="margin-top:16px;"></div>
        </div>`;

    page.main.html(form_html);

    // Company field
    const company_field = frappe.ui.form.make_control({
        df: {
            fieldtype: "Link",
            fieldname: "company",
            options: "Company",
            placeholder: __("Chọn công ty..."),
            filters: { country: "Vietnam" }
        },
        parent: page.main.find("#field-company")[0],
        render_input: true
    });
    company_field.refresh();

    // Auto-set company from defaults
    const default_company = frappe.defaults.get_default("company");
    if (default_company) company_field.set_value(default_company);

    // Fiscal year field
    const fiscal_year_field = frappe.ui.form.make_control({
        df: {
            fieldtype: "Link",
            fieldname: "fiscal_year",
            options: "Fiscal Year",
            placeholder: __("Chọn năm tài chính..."),
        },
        parent: page.main.find("#field-fiscal-year")[0],
        render_input: true
    });
    fiscal_year_field.refresh();

    // Auto-set fiscal year
    frappe.call({
        method: "frappe.client.get_list",
        args: { doctype: "Fiscal Year", order_by: "year_start_date desc", limit: 1, fields: ["name"] },
        callback(r) {
            if (r.message && r.message[0]) {
                fiscal_year_field.set_value(r.message[0].name);
            }
        }
    });

    // Generate button
    page.main.find("#btn-generate-b09").on("click", function () {
        const company = company_field.get_value();
        const fiscal_year = fiscal_year_field.get_value();

        if (!company) {
            frappe.msgprint({ message: __("Vui lòng chọn công ty."), indicator: "red" });
            return;
        }
        if (!fiscal_year) {
            frappe.msgprint({ message: __("Vui lòng chọn năm tài chính."), indicator: "red" });
            return;
        }

        page.main.find("#btn-generate-b09").prop("disabled", true);
        page.main.find("#b09-spinner").show();
        page.main.find("#b09-result").html("");

        frappe.call({
            method: "vn_accounting.financial_reporting.b09_generator.generate_b09",
            args: { company, fiscal_year },
            callback(r) {
                page.main.find("#btn-generate-b09").prop("disabled", false);
                page.main.find("#b09-spinner").hide();

                if (r.exc || !r.message) {
                    page.main.find("#b09-result").html(
                        `<div class="alert alert-danger">${__("Có lỗi khi sinh file B09-DN. Kiểm tra lại dữ liệu hoặc liên hệ quản trị hệ thống.")}</div>`
                    );
                    return;
                }

                const { file_url, file_name, sheets_generated } = r.message;
                const sheet_list = sheets_generated.map(s => `<li>${s}</li>`).join("");
                page.main.find("#b09-result").html(`
                    <div class="alert alert-success">
                        <p><strong>${__("Tạo file thành công!")}</strong></p>
                        <p>${__("Các sheet đã tạo:")}</p>
                        <ul>${sheet_list}</ul>
                        <a href="${file_url}" class="btn btn-sm btn-success" download>
                            <i class="fa fa-download"></i> ${__("Tải file B09-DN")}
                        </a>
                    </div>`);
            }
        });
    });
};
