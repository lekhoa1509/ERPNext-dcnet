frappe.pages["excel-print-template-builder"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Trình soạn mẫu in Excel"),
        single_column: true,
    });
    new ExcelPrintTemplateBuilder(page, wrapper);
};

class ExcelPrintTemplateBuilder {
    constructor(page, wrapper) {
        this.page = page;
        this.wrapper = wrapper;
        this.state = null;
        this.activeSheet = 0;
        this.selectedCell = null;
        this.templateName = null;
        this.fields = [];
        this.templates = [];
        this.dirty = false;
        this.renderShell();
        this.bindEvents();
        this.loadBootstrap();
    }

    renderShell() {
        this.page.main.html(`
            <div class="xpt-builder">
                <div class="xpt-topbar">
                    <label class="sr-only" for="xpt-template-name">${__("Tên mẫu")}</label>
                    <input id="xpt-template-name" class="xpt-input" placeholder="${__("Tên mẫu in Excel...")}">
                    <label class="sr-only" for="xpt-doctype">${__("Loại chứng từ")}</label>
                    <select id="xpt-doctype" class="xpt-select"><option value="">${__("Chọn loại chứng từ")}</option></select>
                    <label class="xpt-status"><input id="xpt-default" type="checkbox"> ${__("Mẫu mặc định")}</label>
                    <span class="xpt-grow"></span>
                    <button class="xpt-btn" id="xpt-open" type="button">${this.icon("folder-open")} ${__("Mở mẫu")}</button>
                    <button class="xpt-btn" id="xpt-import" type="button">${this.icon("upload")} ${__("Load Excel mẫu")}</button>
                    <button class="xpt-btn" id="xpt-preview" type="button">${this.icon("eye")} ${__("Xem trước")}</button>
                    <button class="xpt-btn xpt-btn-primary" id="xpt-save" type="button">${this.icon("save")} ${__("Lưu mẫu")}</button>
                </div>
                <div class="xpt-toolbar" role="toolbar" aria-label="${__("Định dạng ô")}">
                    <button class="xpt-tool" data-format="bold" type="button" title="${__("In đậm")}"><strong>B</strong></button>
                    <button class="xpt-tool" data-format="italic" type="button" title="${__("In nghiêng")}"><em>I</em></button>
                    <button class="xpt-tool" data-format="underline" type="button" title="${__("Gạch chân")}"><u>U</u></button>
                    <span class="xpt-divider"></span>
                    <button class="xpt-tool" data-align="left" type="button" title="${__("Căn trái")}">${this.icon("align-left")}</button>
                    <button class="xpt-tool" data-align="center" type="button" title="${__("Căn giữa")}">${this.icon("align-center")}</button>
                    <button class="xpt-tool" data-align="right" type="button" title="${__("Căn phải")}">${this.icon("align-right")}</button>
                    <span class="xpt-divider"></span>
                    <select id="xpt-number-format" class="xpt-format-select" title="${__("Định dạng số")}">
                        <option value="General">${__("Tự động")}</option>
                        <option value="#0">1.234</option>
                        <option value="#0.00">1.234,00</option>
                        <option value="#,##0 [$₫-vi-VN]">1.234 ₫</option>
                        <option value="#,##0 [$đ-vi-VN]">1.234 đ</option>
                        <option value="0%">12%</option>
                        <option value="dd/mm/yyyy">31/12/2026</option>
                    </select>
                    <span class="xpt-divider"></span>
                    <button class="xpt-tool" id="xpt-merge" type="button" title="${__("Gộp với ô bên phải")}">${this.icon("merge")}</button>
                    <button class="xpt-tool" id="xpt-add-row" type="button" title="${__("Thêm dòng")}">${this.icon("rows")}</button>
                    <button class="xpt-tool" id="xpt-add-column" type="button" title="${__("Thêm cột")}">${this.icon("columns")}</button>
                    <span class="xpt-grow"></span>
                    <span id="xpt-cell-address" class="xpt-status">${__("Chưa chọn ô")}</span>
                </div>
                <div class="xpt-main">
                    <aside class="xpt-sidebar">
                        <div class="xpt-sidebar-head">
                            <input id="xpt-field-search" class="xpt-input xpt-search" placeholder="${__("Tìm trường...")}">
                        </div>
                        <div id="xpt-fields"></div>
                    </aside>
                    <section id="xpt-canvas" class="xpt-canvas"></section>
                </div>
                <div id="xpt-tabs" class="xpt-sheet-tabs"></div>
            </div>`);
        this.showEmpty();
    }

    bindEvents() {
        const root = this.page.main;
        root.on("change", "#xpt-doctype", () => this.changeDoctype());
        root.on("input", "#xpt-template-name", () => { this.dirty = true; });
        root.on("input", "#xpt-field-search", (event) => this.renderFields(event.target.value));
        root.on("click", "#xpt-import", () => this.openImportDialog());
        root.on("click", "#xpt-open", () => this.openTemplateDialog());
        root.on("click", "#xpt-save", () => this.save());
        root.on("click", "#xpt-preview", () => this.preview());
        root.on("click", ".xpt-field", (event) => this.insertToken(event.currentTarget.dataset.token));
        root.on("dragstart", ".xpt-field", (event) => event.originalEvent.dataTransfer.setData("text/plain", event.currentTarget.dataset.token));
        root.on("click", ".xpt-grid td[data-coordinate]", (event) => this.selectCell(event.currentTarget.dataset.coordinate));
        root.on("focus", ".xpt-grid td[data-coordinate]", (event) => this.selectCell(event.currentTarget.dataset.coordinate));
        root.on("input", ".xpt-grid td[data-coordinate]", (event) => this.updateCell(event.currentTarget));
        root.on("keydown", ".xpt-grid td[data-coordinate]", (event) => this.handleCellKeydown(event));
        root.on("dragover", ".xpt-grid td[data-coordinate]", (event) => event.preventDefault());
        root.on("drop", ".xpt-grid td[data-coordinate]", (event) => {
            event.preventDefault();
            this.selectCell(event.currentTarget.dataset.coordinate);
            this.insertToken(event.originalEvent.dataTransfer.getData("text/plain"));
        });
        root.on("click", ".xpt-tab", (event) => {
            this.activeSheet = Number(event.currentTarget.dataset.index);
            this.selectedCell = null;
            this.renderGrid();
        });
        root.on("click", "[data-format]", (event) => this.toggleFormat(event.currentTarget.dataset.format));
        root.on("click", "[data-align]", (event) => this.setAlignment(event.currentTarget.dataset.align));
        root.on("change", "#xpt-number-format", (event) => this.setNumberFormat(event.target.value));
        root.on("click", "#xpt-merge", () => this.mergeRight());
        root.on("click", "#xpt-add-row", () => this.addRow());
        root.on("click", "#xpt-add-column", () => this.addColumn());
        window.addEventListener("beforeunload", (event) => {
            if (!this.dirty) return;
            event.preventDefault();
            event.returnValue = "";
        });
    }

    async loadBootstrap(templateName = null) {
        const route = frappe.route_options || {};
        const query = frappe.utils.get_query_params ? frappe.utils.get_query_params() : {};
        templateName = templateName || route.template || query.template;
        const documentType = route.document_type || query.document_type;
        this.documentName = route.document_name || query.document_name || this.documentName;
        frappe.route_options = null;
        const response = await frappe.call({
            method: "vn_accounting.excel_printing.api.get_builder_bootstrap",
            type: "GET",
            args: { template_name: templateName || undefined, document_type: documentType || undefined },
            freeze: true,
            freeze_message: __("Đang tải trình soạn mẫu..."),
        });
        const data = response.message || {};
        this.templates = data.templates || [];
        this.populateDoctypes(data.supported_doctypes || []);
        if (data.template) {
            this.loadTemplatePayload(data.template, data.fields || []);
        } else if (documentType) {
            this.page.main.find("#xpt-doctype").val(documentType);
            this.fields = data.fields || [];
            this.renderFields();
        }
    }

    populateDoctypes(doctypes) {
        const select = this.page.main.find("#xpt-doctype");
        select.find("option:not(:first)").remove();
        doctypes.forEach((doctype) => select.append(new Option(__(doctype), doctype)));
    }

    async changeDoctype() {
        const documentType = this.getDoctype();
        this.templateName = null;
        if (!documentType) {
            this.fields = [];
            this.renderFields();
            return;
        }
        const response = await frappe.call({
            method: "vn_accounting.excel_printing.api.get_placeholder_fields",
            type: "GET",
            args: { document_type: documentType },
        });
        this.fields = response.message || [];
        this.renderFields();
        this.dirty = true;
    }

    renderFields(query = "") {
        const target = this.page.main.find("#xpt-fields");
        const needle = String(query || "").trim().toLowerCase();
        const filtered = this.fields.filter((field) => `${field.label} ${field.key}`.toLowerCase().includes(needle));
        const groups = {};
        filtered.forEach((field) => { (groups[field.group] ||= []).push(field); });
        target.html(Object.entries(groups).map(([group, fields]) => `
            <div class="xpt-field-group">
                <h6>${this.escape(group)}</h6>
                ${fields.map((field) => `
                    <button class="xpt-field" type="button" draggable="true" data-token="${this.escape(field.token)}" title="${this.escape(field.token)}">
                        <span class="xpt-field-label">${this.escape(field.label)}</span>
                        <span class="xpt-field-key">${this.escape(field.key)}</span>
                    </button>`).join("")}
            </div>`).join("") || `<div class="text-muted text-center p-4">${__("Không tìm thấy trường phù hợp.")}</div>`);
    }

    openImportDialog() {
        const documentType = this.getDoctype();
        if (!documentType) {
            frappe.msgprint({ message: __("Hãy chọn loại chứng từ trước khi load Excel mẫu."), indicator: "orange" });
            return;
        }
        const dialog = new frappe.ui.Dialog({
            title: __("Load Excel mẫu"),
            fields: [
                { fieldname: "mode", fieldtype: "Select", label: __("Chế độ ánh xạ"), options: [
                    { label: __("Thủ công — giữ nguyên nội dung"), value: "manual" },
                    { label: __("AI hỗ trợ — tự nhận diện và chèn trường"), value: "ai" },
                ], default: "manual", reqd: 1 },
                { fieldname: "hint", fieldtype: "HTML", options: `<div class="alert alert-info">${__("File .xlsx/.xlsm tối đa 20 MB. Hệ thống giữ merge, kích thước, font, màu nền, border, căn lề và định dạng số.")}</div>` },
            ],
            primary_action_label: __("Chọn file Excel"),
            primary_action: (values) => {
                dialog.hide();
                new frappe.ui.FileUploader({
                    allow_multiple: false,
                    restrictions: { allowed_file_types: [".xlsx", ".xlsm"] },
                    on_success: async (file) => {
                        const response = await frappe.call({
                            method: "vn_accounting.excel_printing.api.import_excel_template",
                            args: { file_url: file.file_url, document_type: documentType, mapping_mode: values.mode },
                            freeze: true,
                            freeze_message: __("Đang đọc cấu trúc Excel..."),
                        });
                        const result = response.message || {};
                        this.state = result.workbook_state;
                        this.sourceFile = file.file_url;
                        this.activeSheet = 0;
                        this.selectedCell = null;
                        this.dirty = true;
                        this.renderGrid();
                        const method = result.mapping_method === "ai" ? __("AI") : result.mapping_method === "heuristic" ? __("nhận diện nhãn") : __("thủ công");
                        frappe.show_alert({ message: result.mapped_count ? __("Đã chèn {0} trường bằng {1}.", [result.mapped_count, method]) : __("Đã load file Excel mẫu."), indicator: "green" });
                    },
                });
            },
        });
        dialog.show();
    }

    openTemplateDialog() {
        if (!this.templates.length) {
            frappe.msgprint(__("Chưa có mẫu in Excel nào được lưu."));
            return;
        }
        const dialog = new frappe.ui.Dialog({
            title: __("Mở mẫu in Excel"),
            fields: [{
                fieldname: "template", fieldtype: "Select", label: __("Mẫu"), reqd: 1,
                options: this.templates.map((item) => ({ label: `${item.template_name} — ${__(item.document_type)}`, value: item.name })),
            }],
            primary_action_label: __("Mở"),
            primary_action: (values) => { dialog.hide(); this.loadBootstrap(values.template); },
        });
        dialog.show();
    }

    loadTemplatePayload(template, fields) {
        this.templateName = template.name;
        this.state = template.workbook_state;
        this.sourceFile = template.source_file;
        this.fields = fields;
        this.activeSheet = Number(this.state.active_sheet || 0);
        this.selectedCell = null;
        this.page.main.find("#xpt-template-name").val(template.template_name);
        this.page.main.find("#xpt-doctype").val(template.document_type);
        this.page.main.find("#xpt-default").prop("checked", Boolean(template.is_default));
        this.renderFields();
        this.renderGrid();
        this.dirty = false;
    }

    showEmpty() {
        this.page.main.find("#xpt-canvas").html(`
            <div class="xpt-empty">
                <div>
                    ${this.icon("spreadsheet")}
                    <h4>${__("Bắt đầu từ file Excel hiện có")}</h4>
                    <p>${__("Chọn loại chứng từ, sau đó bấm “Load Excel mẫu” để giữ nguyên bố cục và định dạng.")}</p>
                </div>
            </div>`);
        this.page.main.find("#xpt-tabs").empty();
    }

    renderGrid() {
        if (!this.state?.sheets?.length) return this.showEmpty();
        const sheet = this.currentSheet();
        const rows = Math.max(Number(sheet.max_row || 1), 30);
        const columns = Math.max(Number(sheet.max_column || 1), 12);
        const merges = this.mergeMap(sheet.merged_cells || []);
        const columnHeaders = Array.from({ length: columns }, (_, index) => this.columnName(index + 1));
        const html = [`<div class="xpt-grid-wrap"><table class="xpt-grid"><colgroup><col style="width:38px">`];
        columnHeaders.forEach((column) => html.push(`<col style="width:${this.columnPixels(sheet.column_widths?.[column])}px">`));
        html.push(`</colgroup><thead><tr><th class="xpt-row-head"></th>`);
        columnHeaders.forEach((column) => html.push(`<th>${column}</th>`));
        html.push(`</tr></thead><tbody>`);
        for (let row = 1; row <= rows; row++) {
            html.push(`<tr style="height:${this.rowPixels(sheet.row_heights?.[String(row)])}px"><th class="xpt-row-head">${row}</th>`);
            for (let column = 1; column <= columns; column++) {
                const coordinate = `${this.columnName(column)}${row}`;
                if (merges.covered.has(coordinate)) continue;
                const cell = sheet.cells?.[coordinate] || {};
                const merge = merges.starts[coordinate];
                const style = this.cellStyle(cell.style || {});
                const value = this.rawCellValue(cell.value);
                const classes = [this.selectedCell === coordinate ? "is-selected" : "", String(value).includes("{{") ? "has-token" : ""].filter(Boolean).join(" ");
                const format = cell.style?.number_format || "General";
                html.push(`<td contenteditable="true" spellcheck="false" data-coordinate="${coordinate}" class="${classes}" title="${this.escape(`${coordinate} — ${format}`)}" style="${style}" ${merge ? `rowspan="${merge.rows}" colspan="${merge.columns}"` : ""}>${this.escape(value)}</td>`);
            }
            html.push(`</tr>`);
        }
        html.push(`</tbody></table></div>`);
        this.page.main.find("#xpt-canvas").html(html.join(""));
        this.renderTabs();
        this.refreshToolbar();
    }

    renderTabs() {
        this.page.main.find("#xpt-tabs").html(this.state.sheets.map((sheet, index) => `
            <button type="button" class="xpt-tab ${index === this.activeSheet ? "is-active" : ""}" data-index="${index}">${this.escape(sheet.title)}</button>`).join(""));
    }

    selectCell(coordinate) {
        this.selectedCell = coordinate;
        this.page.main.find(".xpt-grid td.is-selected").removeClass("is-selected");
        this.page.main.find(`.xpt-grid td[data-coordinate="${coordinate}"]`).addClass("is-selected");
        this.refreshToolbar();
    }

    updateCell(element) {
        const coordinate = element.dataset.coordinate;
        const cell = this.ensureCell(coordinate);
        cell.value = element.innerText.replace(/\r?\n/g, "\n");
        cell.data_type = String(cell.value).startsWith("=") ? "f" : "s";
        element.classList.toggle("has-token", String(cell.value).includes("{{"));
        this.dirty = true;
    }

    handleCellKeydown(event) {
        const coordinate = event.currentTarget.dataset.coordinate;
        const value = this.ensureCell(coordinate).value || "";
        if (["Backspace", "Delete"].includes(event.key) && /^{{[^{}]+}}$/.test(String(value))) {
            event.preventDefault();
            event.currentTarget.innerText = "";
            this.updateCell(event.currentTarget);
        }
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            const match = coordinate.match(/^([A-Z]+)(\d+)$/);
            this.selectCell(`${match[1]}${Number(match[2]) + 1}`);
            this.page.main.find(`td[data-coordinate="${match[1]}${Number(match[2]) + 1}"]`).focus();
        }
    }

    insertToken(token) {
        if (!token) return;
        if (!this.state) {
            frappe.msgprint(__("Hãy load file Excel mẫu trước."));
            return;
        }
        if (!this.selectedCell) {
            frappe.msgprint(__("Chọn một ô trước khi chèn trường."));
            return;
        }
        const cell = this.ensureCell(this.selectedCell);
        cell.value = token;
        cell.data_type = "s";
        this.currentSheet().max_row = Math.max(this.currentSheet().max_row, Number(this.selectedCell.match(/\d+/)[0]));
        this.dirty = true;
        this.renderGrid();
    }

    toggleFormat(format) {
        if (!this.selectedCell) return;
        const style = this.ensureStyle(this.selectedCell);
        style.font[format] = !style.font[format];
        this.dirty = true;
        this.renderGrid();
    }

    setAlignment(horizontal) {
        if (!this.selectedCell) return;
        this.ensureStyle(this.selectedCell).alignment.horizontal = horizontal;
        this.dirty = true;
        this.renderGrid();
    }

    setNumberFormat(format) {
        if (!this.selectedCell) return;
        this.ensureStyle(this.selectedCell).number_format = format;
        this.dirty = true;
        this.renderGrid();
    }

    mergeRight() {
        if (!this.selectedCell) return;
        const match = this.selectedCell.match(/^([A-Z]+)(\d+)$/);
        const next = `${this.columnName(this.columnIndex(match[1]) + 1)}${match[2]}`;
        const range = `${this.selectedCell}:${next}`;
        const merges = this.currentSheet().merged_cells ||= [];
        if (!merges.includes(range)) merges.push(range);
        this.dirty = true;
        this.renderGrid();
    }

    addRow() {
        if (!this.state) return;
        this.currentSheet().max_row = Math.min(Number(this.currentSheet().max_row || 1) + 1, 1000);
        this.dirty = true;
        this.renderGrid();
    }

    addColumn() {
        if (!this.state) return;
        this.currentSheet().max_column = Math.min(Number(this.currentSheet().max_column || 1) + 1, 80);
        this.dirty = true;
        this.renderGrid();
    }

    refreshToolbar() {
        this.page.main.find("#xpt-cell-address").text(this.selectedCell || __("Chưa chọn ô"));
        this.page.main.find("[data-format], [data-align]").removeClass("is-active");
        if (!this.selectedCell || !this.state) return;
        const style = this.ensureCell(this.selectedCell).style || {};
        ["bold", "italic", "underline"].forEach((name) => {
            if (style.font?.[name]) this.page.main.find(`[data-format="${name}"]`).addClass("is-active");
        });
        if (style.alignment?.horizontal) this.page.main.find(`[data-align="${style.alignment.horizontal}"]`).addClass("is-active");
        this.page.main.find("#xpt-number-format").val(style.number_format || "General");
    }

    async save() {
        if (!this.state) return frappe.msgprint(__("Chưa có nội dung Excel để lưu."));
        const templateName = String(this.page.main.find("#xpt-template-name").val() || "").trim();
        const documentType = this.getDoctype();
        if (!templateName || !documentType) return frappe.msgprint(__("Tên mẫu và loại chứng từ là bắt buộc."));
        const response = await frappe.call({
            method: "vn_accounting.excel_printing.api.save_template",
            args: {
                name: this.templateName || undefined,
                template_name: templateName,
                document_type: documentType,
                workbook_state: JSON.stringify(this.state),
                source_file: this.sourceFile || undefined,
                is_default: this.page.main.find("#xpt-default").is(":checked") ? 1 : 0,
            },
            freeze: true,
            freeze_message: __("Đang lưu mẫu..."),
        });
        this.templateName = response.message.name;
        this.dirty = false;
        frappe.show_alert({ message: __("Đã lưu mẫu: {0}", [templateName]), indicator: "green" });
        await this.loadBootstrap(this.templateName);
    }

    async preview() {
        if (!this.state) return frappe.msgprint(__("Chưa có nội dung để xem trước."));
        const response = await frappe.call({
            method: "vn_accounting.excel_printing.api.preview_excel_template_grid",
            args: {
                workbook_state: JSON.stringify(this.state),
                document_type: this.getDoctype(),
                document_name: this.documentName || undefined,
            },
            freeze: true,
            freeze_message: __("Đang dựng bản xem trước..."),
        });
        const dialog = new frappe.ui.Dialog({ title: __("Xem trước mẫu in Excel"), size: "extra-large" });
        dialog.$body.html(this.renderPrintPreview(response.message.workbook_state));
        dialog.set_primary_action(__("In"), () => window.print());
        dialog.show();
        this.makePreviewResizable(dialog);
    }

    renderPrintPreview(state) {
        return `<div class="xpt-print-shell">${state.sheets.map((sheet) => {
            const merges = this.mergeMap(sheet.merged_cells || []);
            const bounds = this.previewBounds(sheet);
            let table = `<div class="xpt-print-page"><h5>${this.escape(sheet.title)}</h5><table class="xpt-print-table"><colgroup>`;
            for (let column = bounds.min_column; column <= bounds.max_column; column++) table += `<col style="width:${this.columnPixels(sheet.column_widths?.[this.columnName(column)])}px">`;
            table += `</colgroup>`;
            for (let row = bounds.min_row; row <= bounds.max_row; row++) {
                table += `<tr style="height:${this.rowPixels(sheet.row_heights?.[String(row)])}px">`;
                for (let column = bounds.min_column; column <= bounds.max_column; column++) {
                    const coordinate = `${this.columnName(column)}${row}`;
                    if (merges.covered.has(coordinate)) continue;
                    const cell = sheet.cells?.[coordinate] || {};
                    const merge = merges.starts[coordinate];
                    const value = this.displayCellValue(cell);
                    table += `<td style="${this.cellStyle(cell.style || {}, true)}" ${merge ? `rowspan="${merge.rows}" colspan="${merge.columns}"` : ""}>${this.escape(value)}</td>`;
                }
                table += `</tr>`;
            }
            return table + `</table></div>`;
        }).join("")}</div>`;
    }

    currentSheet() { return this.state.sheets[this.activeSheet]; }
    getDoctype() { return this.page.main.find("#xpt-doctype").val(); }

    ensureCell(coordinate) {
        const sheet = this.currentSheet();
        sheet.cells ||= {};
        return sheet.cells[coordinate] ||= { value: "", data_type: "s", style: this.defaultStyle() };
    }

    ensureStyle(coordinate) {
        const cell = this.ensureCell(coordinate);
        cell.style ||= this.defaultStyle();
        cell.style.font ||= this.defaultStyle().font;
        cell.style.alignment ||= this.defaultStyle().alignment;
        return cell.style;
    }

    defaultStyle() {
        return {
            font: { name: "Arial", size: 10, bold: false, italic: false, underline: null, color: { type: "rgb", rgb: "FF0F172A" } },
            fill: { fill_type: null }, border: {},
            alignment: { horizontal: null, vertical: "center", wrap_text: false },
            number_format: "General", protection: { locked: true, hidden: false },
        };
    }

    cellStyle(style, printMode = false) {
        const font = style.font || {};
        const alignment = style.alignment || {};
        const fill = style.fill || {};
        const border = style.border || {};
        const parts = [
            `font-family:${this.cssValue(font.name || "Arial")}`,
            `font-size:${Number(font.size || 10)}pt`,
            `font-weight:${font.bold ? 700 : 400}`,
            `font-style:${font.italic ? "italic" : "normal"}`,
            `text-decoration:${font.underline ? "underline" : "none"}`,
            `color:${this.color(font.color, "#0f172a")}`,
            `background-color:${this.color(fill.fg_color, "#ffffff")}`,
            `text-align:${alignment.horizontal || "left"}`,
            `vertical-align:${alignment.vertical === "top" ? "top" : alignment.vertical === "bottom" ? "bottom" : "middle"}`,
            `white-space:${alignment.wrap_text ? "pre-wrap" : "nowrap"}`,
        ];
        ["top", "right", "bottom", "left"].forEach((side) => {
            if (border[side]?.style) parts.push(`border-${side}:1px ${this.borderStyle(border[side].style)} ${this.color(border[side].color, "#334155")}`);
            else if (!printMode) parts.push(`border-${side}:1px solid #d8dee6`);
        });
        return parts.join(";");
    }

    mergeMap(ranges) {
        const starts = {};
        const covered = new Set();
        ranges.forEach((range) => {
            const match = String(range).replace(/\$/g, "").match(/^([A-Z]+)(\d+):([A-Z]+)(\d+)$/);
            if (!match) return;
            const [, startColumn, startRow, endColumn, endRow] = match;
            starts[`${startColumn}${startRow}`] = { rows: Number(endRow) - Number(startRow) + 1, columns: this.columnIndex(endColumn) - this.columnIndex(startColumn) + 1 };
            for (let row = Number(startRow); row <= Number(endRow); row++) {
                for (let column = this.columnIndex(startColumn); column <= this.columnIndex(endColumn); column++) {
                    const coordinate = `${this.columnName(column)}${row}`;
                    if (coordinate !== `${startColumn}${startRow}`) covered.add(coordinate);
                }
            }
        });
        return { starts, covered };
    }

    color(value, fallback) {
        if (!value) return fallback;
        const rgb = value.rgb || "";
        if (value.type === "rgb" && /^[0-9A-F]{8}$/i.test(rgb)) return `#${rgb.slice(2)}`;
        if (value.type === "rgb" && /^[0-9A-F]{6}$/i.test(rgb)) return `#${rgb}`;
        return fallback;
    }

    rawCellValue(value) {
        if (value && typeof value === "object" && value.__type) return value.value || "";
        return value ?? "";
    }

    displayCellValue(cell) {
        const value = this.rawCellValue(cell.display_value ?? cell.value ?? "");
        const format = String(cell.style?.number_format || "");
        if (typeof value === "number" && /\[\$[đ₫]-vi-VN\]|[đ₫]/i.test(format)) {
            return `${new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 }).format(value)}${format.includes("₫") ? " ₫" : "đ"}`;
        }
        if (typeof value === "number" && format.includes("%")) return `${new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 }).format(value * 100)}%`;
        return value;
    }

    previewBounds(sheet) {
        return sheet.preview_bounds || { min_column: 1, min_row: 1, max_column: sheet.max_column, max_row: sheet.max_row };
    }

    makePreviewResizable(dialog) {
        const modal = dialog.$wrapper.find(".modal-dialog").css({ "max-width": "94vw", width: "94vw" });
        dialog.$wrapper.find(".modal-content").css({ resize: "both", overflow: "auto", "min-width": "720px", "min-height": "420px" });
        const button = $(`<button type="button" class="btn btn-xs btn-default" style="margin-left:auto" aria-label="${__("Phóng to/thu nhỏ")}">${this.icon("expand")}</button>`);
        let expanded = false;
        button.on("click", () => {
            expanded = !expanded;
            modal.css(expanded ? { width: "98vw", "max-width": "98vw", margin: "1vh auto" } : { width: "94vw", "max-width": "94vw", margin: "1.75rem auto" });
        });
        dialog.$wrapper.find(".modal-title").after(button);
    }

    borderStyle(value) { return ["dashed", "dotted", "double"].includes(value) ? value : "solid"; }
    rowPixels(value) { return Math.max(20, Math.round(Number(value || 18) * 1.34)); }
    columnPixels(value) { return Math.max(55, Math.min(360, Math.round(Number(value || 12) * 7))); }
    columnIndex(name) { return [...name].reduce((total, character) => total * 26 + character.charCodeAt(0) - 64, 0); }
    columnName(index) { let value = ""; while (index) { index--; value = String.fromCharCode(65 + (index % 26)) + value; index = Math.floor(index / 26); } return value; }
    escape(value) { return frappe.utils.escape_html(String(value ?? "")); }
    cssValue(value) { return `'${String(value).replace(/[^a-zA-Z0-9 _-]/g, "")}'`; }

    icon(name) {
        const paths = {
            "folder-open": '<path d="M3 6h6l2 2h10v10H3z"/><path d="M3 10h18l-2 8H5z"/>',
            upload: '<path d="M12 16V4m0 0L7 9m5-5 5 5"/><path d="M4 15v5h16v-5"/>',
            eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
            save: '<path d="M5 3h12l2 2v16H5z"/><path d="M8 3v6h8V3M8 21v-7h8v7"/>',
            "align-left": '<path d="M4 6h16M4 10h10M4 14h16M4 18h10"/>',
            "align-center": '<path d="M4 6h16M7 10h10M4 14h16M7 18h10"/>',
            "align-right": '<path d="M4 6h16M10 10h10M4 14h16M10 18h10"/>',
            merge: '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M8 12h8m-2-2 2 2-2 2M10 10l-2 2 2 2"/>',
            rows: '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M3 15h18"/>',
            columns: '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M9 4v16M15 4v16"/>',
            spreadsheet: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
            expand: '<path d="M8 3H3v5M16 3h5v5M8 21H3v-5M16 21h5v-5"/>',
        };
        return `<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${paths[name] || ""}</svg>`;
    }
}
