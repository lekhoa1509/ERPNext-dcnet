<template>
	<div class="upload-step">
		<!-- UX Gap 7: migration-order guidance shown at hub entry -->
		<details class="order-guide" :open="!store.batch_name">
			<summary>
				📋 {{ __("Thứ tự migration khuyến nghị") }}
				<span class="muted">— {{ __("bấm để xem chi tiết") }}</span>
			</summary>
			<div class="order-guide-body">
				<p class="muted">
					{{ __("Để tránh import OB bị thiếu dữ liệu, làm theo thứ tự sau:") }}
				</p>
				<ol class="order-list">
					<li><strong>{{ __("Phase 1 — Master data tham chiếu") }}</strong>:
						{{ __("UOM, Bank, Department, Warehouse, Item Group, Customer/Supplier Group, Cost Center, Project, Asset Category, CCDC Category.") }}
						<em>{{ __("Yêu cầu cho:") }}</em> OB Inventory ({{ __("Warehouse") }}), OB Fixed Asset / CCDC ({{ __("Asset Category") }}).</li>
					<li><strong>{{ __("Phase 2 — Chart of Accounts") }}</strong>:
						{{ __("Hệ thống tài khoản; sau đó chạy COA leaves bootstrap nếu cần TK 1111/1121.XX/2141/3341/4211/...") }}
						<em>{{ __("Yêu cầu cho:") }}</em> {{ __("tất cả OB *.") }}</li>
					<li><strong>{{ __("Phase 3 — Master entities") }}</strong>:
						{{ __("Customer, Supplier, Item, Employee, Bank Account.") }}
						<em>{{ __("Yêu cầu cho:") }}</em> OB Customer AR, OB Supplier AP, OB Employee Advance,
						OB Inventory ({{ __("is_stock_item=1") }}), OB Fixed Asset / CCDC ({{ __("is_fixed_asset=1") }}).</li>
					<li><strong>{{ __("Phase 0 — Opening balances") }}</strong>:
						{{ __("9 file OB. Preflight sẽ phát hiện missing master + hiện cảnh báo block/warn cho từng nhóm.") }}</li>
					<li><strong>{{ __("Phase 4 — Transactions") }}</strong>:
						{{ __("NKC + Bảng kê BR/MV.") }}</li>
				</ol>
				<p class="hint">
					⚠ {{ __("Nếu chỉ import Phase 0 mà thiếu Phase 1+2+3, các handler sẽ silently drop balance hoặc fail giữa chừng. Preflight giúp catch những trường hợp này trước khi bấm Tạo.") }}
				</p>
			</div>
		</details>

		<!-- Step 1: create batch -->
		<div v-if="!store.batch_name" class="card">
			<h3>{{ __("Tạo batch migration mới") }}</h3>
			<p class="muted">
				{{ __("Mỗi batch là một phiên import từ Misa SME. Một Company chỉ có 1 batch đang chạy tại một thời điểm.") }}
			</p>
			<div class="form-row company-autocomplete">
				<label>{{ __("Company") }} <span class="reqd">*</span></label>
				<div class="company-picker">
					<input
						ref="companyInput"
						v-model="form.company"
						type="text"
						:placeholder="__('Gõ để tìm Company...')"
						@focus="onCompanyFocus"
						@input="onCompanyType"
						@blur="onCompanyBlur"
						autocomplete="off"
					/>
					<div v-if="showCompanyDropdown && companyOptions.length" class="company-dropdown">
						<div
							v-for="c in companyOptions"
							:key="c.name"
							class="company-option"
							:class="{ highlighted: c.name === form.company }"
							@mousedown.prevent="selectCompany(c.name)"
						>
							<div class="company-option-name">{{ c.name }}</div>
							<div class="company-option-meta">
								<span class="muted">{{ c.country }}</span>
								<span class="muted">·</span>
								<span class="muted">{{ c.default_currency }}</span>
							</div>
						</div>
					</div>
					<div v-if="showCompanyDropdown && !companyOptions.length && !companyLoading" class="company-empty">
						{{ __("Không tìm thấy Company.") }}
						<a :href="'/app/company/new?company_name=' + encodeURIComponent(form.company)" target="_blank">
							{{ __("Tạo mới") }}
						</a>
					</div>
				</div>
				<small v-if="form.company && !companyValidated" class="hint error-hint">
					⚠ {{ __("Company chưa tồn tại — chọn từ gợi ý hoặc tạo mới.") }}
				</small>
			</div>
			<div class="form-row">
				<label>{{ __("Tiêu đề batch") }}</label>
				<input v-model="form.batch_title" type="text" :placeholder="__('VD: Import Misa T1/2026')" />
			</div>
			<div class="form-row">
				<label>{{ __("Ngày OB (đầu kỳ)") }} <span class="reqd">*</span></label>
				<input v-model="form.ob_posting_date" type="date" />
				<small class="hint">
					{{ __("Misa file 'đầu kỳ' không có ngày. Bắt buộc nhập ngày bắt đầu kỳ kế toán.") }}<br>
					{{ __("Ví dụ: nếu OB là đầu kỳ 2025 → chọn 2024-12-31. Nếu OB là đầu kỳ 2026 → chọn 2025-12-31.") }}
				</small>
			</div>
			<!-- Shard token — hidden by default. Operators running 2 parallel batches per
			     Company can toggle this open via the "Tuỳ chọn nâng cao" disclosure
			     below. Hidden in normal flow to reduce form noise. Backend still
			     accepts shard_token; default empty = queue long, single-batch mode. -->
			<details class="advanced-options">
				<summary>{{ __("⚙️ Tuỳ chọn nâng cao") }}</summary>
				<div class="form-row">
					<label>{{ __("Shard token") }}</label>
					<input v-model="form.shard_token" type="text" maxlength="32" :placeholder="__('VD: A hoặc B (để trống nếu chạy đơn)')" />
					<small class="hint">
						{{ __("Chỉ điền khi muốn chạy song song 2 batch cùng Company.") }}<br>
						{{ __("Quy ước: 'A' / '1' / 'L' → queue long; 'B' / '2' / 'D' → queue default. Để trống = chế độ truyền thống (1 batch / Company).") }}
					</small>
				</div>
			</details>
			<div class="form-actions">
				<button class="btn btn-primary" :disabled="!form.company || !companyValidated || !form.ob_posting_date || creating" @click="onCreate">
					{{ creating ? __("Đang tạo...") : __("Tạo batch") }}
				</button>
			</div>
			<div v-if="error" class="error">{{ error }}</div>
		</div>

		<!-- Step 2: upload files into existing batch -->
		<div v-else class="card">
			<div class="batch-header">
				<div>
					<h3>{{ store.batch_title || store.batch_name }}</h3>
					<p class="muted">
						{{ __("Company:") }} <strong>{{ store.company }}</strong>
						· {{ __("Trạng thái:") }} <span class="status-badge">{{ store.status }}</span>
					</p>
				</div>
				<button class="btn btn-link" @click="onSwitchBatch">{{ __("Đổi batch khác") }}</button>
			</div>

			<div class="upload-zone" @dragover.prevent @drop.prevent="onDrop">
				<input
					ref="fileInput"
					type="file"
					accept=".xlsx,.xls"
					multiple
					style="display: none"
					@change="onFileInput"
				/>
				<div class="upload-zone-inner" @click="$refs.fileInput.click()">
					<div class="upload-icon">⬆</div>
					<div>{{ __("Kéo thả file Excel vào đây hoặc bấm để chọn") }}</div>
					<div class="muted">{{ __("Chấp nhận .xlsx / .xls (tối đa 100 MB / file)") }}</div>
				</div>
			</div>

			<div v-if="store.files.length" class="file-list">
				<table class="file-table">
					<thead>
						<tr>
							<th>{{ __("Tên file") }}</th>
							<th>{{ __("Loại") }}</th>
							<th>{{ __("Dung lượng") }}</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="f in store.files" :key="f.name">
							<td>{{ f.original_filename || f.file_url }}</td>
							<td>
								<select :value="f.file_type" @change="onChangeType(f, $event.target.value)">
									<option v-for="opt in FILE_TYPE_OPTIONS" :key="opt" :value="opt">{{ opt }}</option>
								</select>
							</td>
							<td>{{ formatBytes(f.size_bytes) }}</td>
							<td>
								<button class="btn btn-xs btn-link" @click="onRemoveFile(f)">×</button>
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<div v-if="error" class="error">{{ error }}</div>
		</div>
	</div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useMisaStore } from "../store.js";

const store = useMisaStore();

function __(t) {
	return typeof window.__ === "function" ? window.__(t) : t;
}

const FILE_TYPE_OPTIONS = [
	"Unknown",
	"NKC",
	"Bang ke BR",
	"Bang ke MV",
	"Account",
	"Item",
	"Item Group",
	"Customer",
	"Customer Group",
	"Supplier",
	"Supplier Group",
	"Employee",
	"UOM",
	"Bank",
	"Bank Account",
	"Warehouse",
	"Department",
	"Cost Center",
	"Project",
	"Asset Category",
	"CCDC Category",
];

const form = reactive({ company: "", batch_title: "", ob_posting_date: "", shard_token: "" });
const creating = ref(false);
const error = ref(null);
const fileInput = ref(null);

// Company autocomplete state
const companyInput = ref(null);
const companyOptions = ref([]);
const companyLoading = ref(false);
const showCompanyDropdown = ref(false);
const companyValidated = ref(false);
let companyDebounce = null;

async function fetchCompanies(query) {
	companyLoading.value = true;
	try {
		const data = await new Promise((resolve, reject) => {
			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Company",
					filters: query ? [["name", "like", `%${query}%`]] : [],
					fields: ["name", "country", "default_currency"],
					order_by: "name asc",
					limit_page_length: 20,
				},
				callback: r => resolve(r?.message || []),
				error: () => reject(),
			});
		});
		companyOptions.value = data;
	} catch (e) {
		companyOptions.value = [];
	} finally {
		companyLoading.value = false;
	}
}

function onCompanyFocus() {
	showCompanyDropdown.value = true;
	if (!companyOptions.value.length) {
		fetchCompanies(form.company);
	}
}

function onCompanyType() {
	companyValidated.value = false;
	showCompanyDropdown.value = true;
	if (companyDebounce) clearTimeout(companyDebounce);
	companyDebounce = setTimeout(() => fetchCompanies(form.company), 200);
}

function onCompanyBlur() {
	// Delay so mousedown on option fires first
	setTimeout(() => {
		showCompanyDropdown.value = false;
		// Validate that typed value matches a known company
		const matches = companyOptions.value.some(c => c.name === form.company);
		companyValidated.value = matches || form.company === "";
	}, 200);
}

function selectCompany(name) {
	form.company = name;
	companyValidated.value = true;
	showCompanyDropdown.value = false;
}

async function onCreate() {
	error.value = null;
	creating.value = true;
	try {
		await store.createBatch(
			form.company.trim(),
			form.batch_title.trim(),
			form.ob_posting_date,
			form.shard_token.trim(),
		);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		creating.value = false;
	}
}

function onSwitchBatch() {
	store.$reset();
}

async function onDrop(e) {
	const files = Array.from(e.dataTransfer.files || []);
	for (const file of files) {
		await tryUpload(file);
	}
}

async function onFileInput(e) {
	const files = Array.from(e.target.files || []);
	for (const file of files) {
		await tryUpload(file);
	}
	e.target.value = ""; // reset so re-selecting same file works
}

async function tryUpload(file) {
	error.value = null;
	try {
		await store.uploadFile(file, "Unknown");
	} catch (e) {
		error.value = (e.message || String(e)) + " — " + file.name;
	}
}

async function onChangeType(row, file_type) {
	error.value = null;
	try {
		await store.updateFileType(row.name, file_type);
	} catch (e) {
		error.value = e.message || String(e);
	}
}

async function onRemoveFile(row) {
	if (!confirm(__("Xóa file '") + (row.original_filename || row.name) + __("'?"))) return;
	try {
		await store.removeFile(row.name);
	} catch (e) {
		error.value = e.message || String(e);
	}
}

function formatBytes(n) {
	if (!n || n < 1024) return (n || 0) + " B";
	if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB";
	return (n / 1024 / 1024).toFixed(1) + " MB";
}
</script>

<style scoped>
.upload-step .card {
	background: var(--card-bg, #fff);
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 8px;
	padding: 20px;
}

.card h3 {
	margin: 0 0 6px;
	font-size: 16px;
}

.muted {
	color: var(--text-muted, #888);
	font-size: 13px;
	margin: 0 0 12px;
}

.form-row {
	display: flex;
	flex-direction: column;
	gap: 4px;
	margin-bottom: 12px;
}

.form-row label {
	font-size: 12px;
	font-weight: 500;
}

.form-row input {
	padding: 6px 10px;
	border: 1px solid var(--border-color, #d1d5db);
	border-radius: 4px;
	font-size: 13px;
}

.reqd {
	color: var(--red-500, #ef4444);
}

.form-actions {
	margin-top: 8px;
}

.advanced-options {
	margin: 8px 0 4px;
	font-size: 12.5px;
}
.advanced-options summary {
	cursor: pointer;
	color: var(--text-muted, #6b7280);
	user-select: none;
	padding: 4px 0;
}
.advanced-options summary:hover { color: #111827; }
.advanced-options[open] summary { color: #111827; font-weight: 500; }
/* Frappe's global CSS forces display:block on details children — override to honor browser default hide-when-closed */
.advanced-options:not([open]) > *:not(summary) { display: none !important; }
.advanced-options .form-row {
	margin-top: 6px;
	padding: 8px 10px;
	background: var(--bg-light-gray, #f9fafb);
	border-left: 2px solid var(--border-color, #e5e7eb);
	border-radius: 3px;
}

.error {
	margin-top: 12px;
	padding: 8px 12px;
	background: #fef2f2;
	color: #991b1b;
	border-radius: 4px;
	font-size: 13px;
}

.batch-header {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	margin-bottom: 16px;
}

.status-badge {
	background: var(--primary, #2563eb);
	color: white;
	padding: 2px 8px;
	border-radius: 10px;
	font-size: 11px;
	font-weight: 600;
}

.upload-zone {
	margin: 16px 0;
	border: 2px dashed var(--border-color, #d1d5db);
	border-radius: 8px;
	background: var(--bg-light-gray, #f9fafb);
}

.upload-zone-inner {
	padding: 32px 16px;
	text-align: center;
	cursor: pointer;
}

.upload-icon {
	font-size: 32px;
	margin-bottom: 8px;
}

.file-list {
	margin-top: 16px;
}

.file-table {
	width: 100%;
	border-collapse: collapse;
}

.file-table th,
.file-table td {
	padding: 8px;
	border-bottom: 1px solid var(--border-color, #e5e7eb);
	text-align: left;
	font-size: 13px;
}

.file-table th {
	background: var(--bg-light-gray, #f9fafb);
	font-weight: 500;
}

.file-table select {
	padding: 4px 6px;
	border: 1px solid var(--border-color, #d1d5db);
	border-radius: 4px;
	font-size: 12px;
}

/* UX Gap 7 — migration-order guidance banner */
.order-guide {
	margin-bottom: 16px;
	padding: 10px 14px;
	background: #f0f9ff;
	border: 1px solid #bae6fd;
	border-radius: 6px;
	font-size: 13px;
}
.order-guide summary {
	cursor: pointer;
	font-weight: 500;
	color: #075985;
}
.order-guide summary:hover { color: #0c4a6e; }
.order-guide-body { margin-top: 10px; }
.order-list { padding-left: 22px; margin: 8px 0; }
.order-list li { margin: 6px 0; line-height: 1.5; }
.order-list li em {
	color: #0369a1;
	font-style: normal;
	font-size: 12px;
	margin-left: 4px;
}
.order-guide .hint {
	margin: 10px 0 0;
	padding: 8px 12px;
	background: #fff7ed;
	color: #92400e;
	border-radius: 4px;
	font-size: 12px;
}
.company-autocomplete { position: relative; }
.company-picker { position: relative; }
.company-dropdown {
	position: absolute; top: 100%; left: 0; right: 0; z-index: 50;
	background: var(--card-bg, #fff);
	border: 1px solid var(--border-color, #d1d5db);
	border-radius: 6px;
	margin-top: 4px;
	max-height: 280px; overflow-y: auto;
	box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.company-option {
	padding: 8px 12px;
	cursor: pointer;
	border-bottom: 1px solid var(--bg-light-gray, #f3f4f6);
}
.company-option:last-child { border-bottom: 0; }
.company-option:hover, .company-option.highlighted {
	background: var(--bg-light-gray, #f3f4f6);
}
.company-option-name { font-weight: 600; font-size: 13px; }
.company-option-meta { font-size: 11px; margin-top: 2px; display: flex; gap: 6px; }
.company-empty {
	padding: 12px;
	font-size: 13px;
	color: var(--text-muted, #888);
	text-align: center;
}
.company-empty a { color: var(--primary, #2563eb); margin-left: 4px; }
.error-hint { color: #d97706; }
</style>
