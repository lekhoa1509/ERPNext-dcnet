<template>
	<div class="review-step">
		<div class="card">
			<div class="header-row">
				<div>
					<h3>{{ __("Duyệt trước khi tạo") }}</h3>
					<p class="muted">{{ __("Kiểm tra từng entity. Sửa Conflict / Invalid trước khi chuyển sang Tạo.") }}</p>
				</div>
				<div class="header-actions">
					<button
						class="btn btn-default btn-sm"
						:disabled="busy || loadingRows"
						:title="__('Tải lại số liệu')"
						@click="refreshAll"
					>↻</button>
					<button
						v-if="store.status === 'PARSED'"
						class="btn btn-primary"
						:disabled="busy"
						@click="onMarkReviewed"
					>
						{{ __("Đánh dấu đã duyệt →") }}
					</button>
					<span v-else-if="store.status === 'REVIEWED' || store.status === 'POSTING' || store.status === 'POSTED'" class="badge badge-done">
						{{ __("Đã duyệt") }} ✓
					</span>
				</div>
			</div>

			<div v-if="error" class="error">{{ error }}</div>

			<!-- Demo data banner -->
			<div v-if="demoData?.has_demo_data && !demoDismissed" class="demo-banner">
				<span class="demo-icon">⚠</span>
				<div class="demo-text">
					<strong>{{ __("Site có dữ liệu mẫu dcnet_sample") }}</strong>
					({{ demoData.total.toLocaleString() }} {{ __("bản ghi") }})
					— {{ __("nên xử lý trước khi import Misa.") }}
				</div>
				<button class="btn btn-warning" @click="demoDialogOpen = true">
					{{ __("Xử lý") }}
				</button>
				<button class="btn btn-link" @click="demoDismissed = true">
					{{ __("Bỏ qua") }}
				</button>
			</div>

			<!-- Quick-action banner: skip-all when batch has blocking Invalid rows -->
			<div v-if="globalInvalidCount > 0 && store.status === 'PARSED'" class="invalid-banner">
				<span class="invalid-icon">⚠</span>
				<div class="invalid-text">
					<strong>{{ globalInvalidCount }} {{ __("dòng không hợp lệ") }}</strong>
					{{ __("đang chặn bước Tạo. Thường là header/footer artifact của Misa (như dòng \"Tổng\", dòng phụ đề). Bỏ qua nếu không cần.") }}
				</div>
				<button class="btn btn-warning" :disabled="busy" @click="onSkipAllInvalid">
					{{ busy ? __("Đang bỏ qua...") : __("🗑 Bỏ qua tất cả {0} dòng").replace("{0}", globalInvalidCount) }}
				</button>
			</div>

			<!-- Phase tabs -->
			<nav class="phase-tabs">
				<button
					v-for="p in phases"
					:key="p.key"
					:class="['phase-tab', { active: phase === p.key, disabled: p.disabled }]"
					:disabled="p.disabled"
					@click="phase = p.key"
				>
					{{ p.label }}
					<span v-if="phaseTotal(p) > 0" class="phase-count">{{ phaseTotal(p) }}</span>
				</button>
			</nav>

			<!-- File-type sub-tabs within current phase -->
			<nav v-if="fileTypesForPhase.length" class="ft-tabs">
				<button
					v-for="ft in fileTypesForPhase"
					:key="ft"
					:class="['ft-tab', { active: fileType === ft }]"
					@click="onSelectFt(ft)"
				>
					{{ ft }}
					<span class="ft-count">{{ totalFor(ft) }}</span>
				</button>
			</nav>

			<!-- Status filter chips -->
			<nav v-if="fileType" class="status-chips">
				<button
					v-for="s in STATUSES"
					:key="s.key"
					:class="['chip', s.color, { active: statusFilter === s.key }]"
					@click="onSelectStatus(s.key)"
				>
					{{ s.label }}
					<span class="chip-n">{{ countFor(fileType, s.key) }}</span>
				</button>
				<button v-if="statusFilter" class="chip clear" @click="onSelectStatus(null)">
					{{ __("Xóa lọc") }}
				</button>
			</nav>

			<!-- Row table -->
			<div v-if="fileType" class="row-section">
				<LoadingSkeleton v-if="loadingRows" :count="6" :cols="6" />
				<table v-else-if="rows.length" class="row-table">
					<thead>
						<tr>
							<th class="num">#</th>
							<th>{{ __("Trạng thái") }}</th>
							<th>{{ __("Dữ liệu Misa") }}</th>
							<th>{{ __("ERPNext target") }}</th>
							<th>{{ __("Lỗi") }}</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="r in rows" :key="r.name">
							<td class="num">{{ r.row_index }}</td>
							<td>
								<span class="badge" :class="r.status.toLowerCase()">{{ r.status }}</span>
							</td>
							<td class="payload" :title="r.raw_payload">{{ shortPayload(r.raw_payload) }}</td>
							<td>{{ r.target_name || '—' }}</td>
							<td class="error-cell" :title="r.error_message">{{ (r.error_message || '').slice(0, 60) }}</td>
							<td>
								<button
									v-if="r.status === 'Conflict' || r.status === 'Invalid'"
									class="btn btn-xs btn-link"
									@click="openConflictDialog(r)"
								>
									{{ __("Xử lý") }}
								</button>
							</td>
						</tr>
					</tbody>
				</table>
				<EmptyState
					v-else
					icon="🗂"
					:title="__('Không có dòng nào ở bộ lọc này')"
					:hint="__('Đổi tab trạng thái ở trên hoặc bỏ filter để xem tất cả.')"
				/>

				<div v-if="total > limit" class="pagination">
					<button :disabled="page <= 1" @click="page--; reloadRows()">‹</button>
					<span>{{ page }} / {{ Math.ceil(total / limit) }}</span>
					<button :disabled="page >= Math.ceil(total / limit)" @click="page++; reloadRows()">›</button>
				</div>
			</div>

			<EmptyState
				v-else-if="isMasterPhase"
				icon="⚙️"
				:title="__('Master tự động bóc tách ở bước Tạo')"
				:hint="__('Đơn vị tính, tài khoản, khách hàng, nhà cung cấp, vật tư... được hệ thống tự sinh từ file giao dịch và số dư khi bấm “Tạo vào ERPNext”. Không có dòng riêng để duyệt ở bước này — chuyển sang tab Phase 3.5 / Phase 4 để xem dữ liệu.')"
			/>
			<EmptyState
				v-else
				icon="📋"
				:title="__('Chưa có dữ liệu để duyệt')"
				:hint="__('Hoàn tất bước Phân tích trước, hoặc bấm ↻ để tải lại. Sau khi parser chạy xong, các dòng sẽ hiện ở đây.')"
			/>
		</div>

		<ConflictDialog
			:open="dialogOpen"
			:row="dialogRow"
			@close="dialogOpen = false"
			@resolved="onResolved"
		/>

		<DemoDataDialog
			:open="demoDialogOpen"
			:data="demoData"
			@close="demoDialogOpen = false"
			@proceed="onDemoProceed"
		/>
	</div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useMisaStore } from "../store.js";
import ConflictDialog from "../components/ConflictDialog.vue";
import DemoDataDialog from "../components/DemoDataDialog.vue";
import LoadingSkeleton from "../components/LoadingSkeleton.vue";
import EmptyState from "../components/EmptyState.vue";

const store = useMisaStore();
function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

const STATUSES = [
	{ key: "New", label: __("New"), color: "gray" },
	{ key: "Exists", label: __("Exists"), color: "blue" },
	{ key: "Conflict", label: __("Conflict"), color: "orange" },
	{ key: "Invalid", label: __("Invalid"), color: "red" },
	{ key: "Skipped", label: __("Skipped"), color: "gray" },
	{ key: "Ready", label: __("Ready"), color: "green" },
	{ key: "Posted", label: __("Posted"), color: "green-solid" },
	{ key: "Failed", label: __("Failed"), color: "red" },
	{ key: "Reversed", label: __("Reversed"), color: "gray" },
];

const PHASE_DEFS = {
	"Phase 1 — Reference": ["UOM", "Bank", "Department", "Warehouse", "Item Group",
		"Customer Group", "Supplier Group", "Cost Center", "Project",
		"Asset Category", "CCDC Category"],
	"Phase 2 — Accounts": ["Account"],
	"Phase 3 — Master": ["Item", "Customer", "Supplier", "Employee", "Bank Account"],
	"Phase 3.5 — Số dư đầu kỳ": [
		"OB Account Balance", "OB Bank Balance",
		"OB Customer AR", "OB Supplier AP", "OB Employee Advance",
		"OB Inventory", "OB Fixed Asset", "OB CCDC", "OB Prepaid Expense",
	],
	"Phase 4 — Transactions": ["NKC", "Bang ke BR", "Bang ke MV"],
};

const phases = computed(() => Object.keys(PHASE_DEFS).map((k) => ({
	key: k,
	label: __(k),
	disabled: false,  // C14: Phase 4 enabled
})));

const counts = ref({});  // {file_type: {status: n}}
const phase = ref("Phase 1 — Reference");
const fileType = ref("");
const statusFilter = ref(null);
const rows = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(50);
const loadingRows = ref(false);
const busy = ref(false);
const error = ref(null);
const dialogOpen = ref(false);
const dialogRow = ref(null);
const demoData = ref(null);
const demoDialogOpen = ref(false);
const demoDismissed = ref(false);

async function loadDemoData() {
	try { demoData.value = await store.detectDemoData(); }
	catch (e) { /* silent — feature optional */ }
}

async function onDemoProceed() {
	demoDialogOpen.value = false;
	demoDismissed.value = true;
	await loadDemoData();
}

const fileTypesForPhase = computed(() =>
	PHASE_DEFS[phase.value]?.filter((ft) => counts.value[ft]) || []
);

function countFor(ft, status) {
	return counts.value?.[ft]?.[status] || 0;
}
function totalFor(ft) {
	const m = counts.value?.[ft] || {};
	return Object.values(m).reduce((s, n) => s + n, 0);
}
function phaseTotal(p) {
	return (PHASE_DEFS[p.key] || []).reduce((s, ft) => s + totalFor(ft), 0);
}

// Phases 1-3 are MASTER doctypes (UOM, Account, Customer...) which are
// auto-extracted from the transaction/OB files at the Tạo step — they never
// have parsed rows here, so an empty tab is expected, not an error.
const MASTER_PHASES = ["Phase 1 — Reference", "Phase 2 — Accounts", "Phase 3 — Master"];
const isMasterPhase = computed(() => MASTER_PHASES.includes(phase.value));

function firstNonEmptyPhaseKey() {
	for (const k of Object.keys(PHASE_DEFS)) {
		if ((PHASE_DEFS[k] || []).reduce((s, ft) => s + totalFor(ft), 0) > 0) return k;
	}
	return null;
}

// Pull a human-readable message out of a JS Error or a Frappe xhr/jqXHR.
function _errMsg(e) {
	if (!e) return __("Lỗi không xác định");
	if (e.message) return e.message;
	try {
		const sm = e._server_messages && JSON.parse(e._server_messages);
		if (sm && sm.length) {
			const m = JSON.parse(sm[0]);
			return m.message || sm[0];
		}
	} catch (_) { /* not a server-messages payload */ }
	return String(e);
}

function shortPayload(j) {
	try {
		const parsed = JSON.parse(j || "{}");
		const entries = Object.entries(parsed)
			.filter(([k]) => !k.startsWith("STT"))
			.slice(0, 3);
		return entries.map(([k, v]) => `${k}: ${v}`).join(" · ");
	} catch (e) {
		return (j || "").slice(0, 80);
	}
}

async function loadCounts() {
	try {
		const r = await store.aggregateCounts();
		counts.value = r.counts || {};
		// Land on the first phase that actually has parsed rows. The default
		// (Phase 1) is a master phase with no rows, so without this the user
		// sees an empty review even when Phase 4 has thousands of rows.
		const curEmpty = (PHASE_DEFS[phase.value] || []).every((ft) => !counts.value[ft]);
		if (curEmpty) {
			const k = firstNonEmptyPhaseKey();
			if (k && k !== phase.value) phase.value = k;
		}
		// Auto-select first file_type in current phase if none
		if (!fileType.value) {
			const fts = PHASE_DEFS[phase.value]?.filter((ft) => counts.value[ft]) || [];
			if (fts.length) fileType.value = fts[0];
		}
	} catch (e) {
		error.value = __("Không tải được số liệu duyệt: ") + _errMsg(e);
	}
}

async function reloadRows() {
	if (!fileType.value) {
		rows.value = []; total.value = 0; return;
	}
	loadingRows.value = true;
	try {
		const r = await store.listRows({
			file_type: fileType.value,
			status: statusFilter.value || undefined,
			page: page.value,
			limit: limit.value,
		});
		rows.value = r.rows || [];
		total.value = r.total || 0;
	} catch (e) {
		error.value = __("Không tải được danh sách dòng: ") + _errMsg(e);
	} finally {
		loadingRows.value = false;
	}
}

// Manual + automatic refresh: parse finishes asynchronously, so counts may be
// empty if the user opened Review before the parser flipped status to PARSED.
async function refreshAll() {
	error.value = null;
	await loadCounts();
	await reloadRows();
}
watch(() => store.status, (s) => {
	if (s === "PARSED" || s === "REVIEWED") refreshAll();
});

function onSelectFt(ft) {
	fileType.value = ft;
	statusFilter.value = null;
	page.value = 1;
	reloadRows();
}

function onSelectStatus(s) {
	statusFilter.value = s;
	page.value = 1;
	reloadRows();
}

function openConflictDialog(row) {
	dialogRow.value = row;
	dialogOpen.value = true;
}

async function onResolved() {
	await Promise.all([loadCounts(), reloadRows()]);
}

async function onMarkReviewed() {
	busy.value = true;
	error.value = null;
	try {
		await store.markReviewed();
	} catch (e) {
		error.value = __("Không đánh dấu duyệt được: ") + _errMsg(e);
	} finally {
		busy.value = false;
	}
}

// Global Invalid count across all entity types — used for "Bỏ qua tất cả" quick action
const globalInvalidCount = computed(() => {
	const all = counts.value || {};
	let n = 0;
	for (const ft of Object.keys(all)) {
		n += (all[ft]?.Invalid || 0);
	}
	return n;
});

async function onSkipAllInvalid() {
	if (!confirm(__("Sẽ chuyển tất cả {0} dòng Invalid sang Skipped — bỏ qua trong bước Tạo. Tiếp tục?").replace("{0}", globalInvalidCount.value))) return;
	busy.value = true;
	error.value = null;
	try {
		await new Promise((resolve, reject) => {
			frappe.call({
				method: "vn_accounting.misa_migration.api.review.skip_all_invalid",
				args: { batch_name: store.batch_name },
				callback: r => resolve(r?.message),
				error: (xhr) => reject(new Error(_errMsg(xhr) || __("Bỏ qua thất bại"))),
			});
		});
		await loadCounts();
		await reloadRows();
	} catch (e) {
		error.value = __("Không bỏ qua được dòng Invalid: ") + _errMsg(e);
	} finally {
		busy.value = false;
	}
}

watch(phase, () => {
	fileType.value = "";
	statusFilter.value = null;
	page.value = 1;
	rows.value = [];
	const fts = PHASE_DEFS[phase.value]?.filter((ft) => counts.value[ft]) || [];
	if (fts.length) fileType.value = fts[0];
	reloadRows();
});

watch(fileType, () => { reloadRows(); });

onMounted(async () => {
	await Promise.all([loadCounts(), loadDemoData()]);
	await reloadRows();
});
</script>

<style scoped>
.review-step .card {
	background: var(--card-bg, #fff);
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 8px;
	padding: 16px;
}

.invalid-banner {
	display: flex; align-items: center; gap: 12px;
	margin: 12px 0;
	padding: 10px 14px;
	background: #fef2f2;
	border-left: 3px solid #dc2626;
	border-radius: 4px;
	font-size: 13px;
}
.invalid-icon { font-size: 18px; color: #dc2626; }
.invalid-text { flex: 1; color: #7f1d1d; line-height: 1.45; }
.invalid-text strong { color: #991b1b; }
.header-row {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	gap: 16px;
	margin-bottom: 12px;
}
.header-actions {
	display: flex;
	gap: 8px;
	align-items: center;
	flex: 0 0 auto;
}
h3 { margin: 0 0 4px; font-size: 16px; }
.muted { color: var(--text-muted, #888); font-size: 13px; margin: 0; }
.error {
	margin: 10px 0;
	padding: 8px 12px;
	background: #fef2f2;
	color: #991b1b;
	border-radius: 4px;
	font-size: 13px;
}
.phase-tabs {
	display: flex;
	gap: 4px;
	border-bottom: 2px solid var(--border-color, #e5e7eb);
	margin-bottom: 8px;
}
.phase-tab {
	padding: 8px 14px;
	border: none;
	background: none;
	cursor: pointer;
	border-bottom: 2px solid transparent;
	margin-bottom: -2px;
	font-size: 13px;
	display: flex;
	align-items: center;
	gap: 6px;
}
.phase-tab.active { border-bottom-color: var(--primary, #2563eb); font-weight: 600; }
.phase-tab.disabled { color: var(--text-muted, #aaa); cursor: not-allowed; }
.phase-count {
	background: var(--gray-200, #e5e7eb);
	padding: 1px 6px;
	border-radius: 8px;
	font-size: 11px;
}
.ft-tabs {
	display: flex;
	gap: 4px;
	flex-wrap: wrap;
	margin: 10px 0;
}
.ft-tab {
	padding: 4px 10px;
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 14px;
	background: white;
	cursor: pointer;
	font-size: 12px;
	display: inline-flex;
	gap: 6px;
	align-items: center;
}
.ft-tab.active { background: var(--primary, #2563eb); color: white; border-color: var(--primary, #2563eb); }
.ft-count {
	background: rgba(0, 0, 0, 0.1);
	padding: 1px 6px;
	border-radius: 8px;
	font-size: 10px;
}
.ft-tab.active .ft-count { background: rgba(255, 255, 255, 0.2); }
.status-chips {
	display: flex;
	gap: 6px;
	flex-wrap: wrap;
	margin: 8px 0 12px;
}
.chip {
	padding: 3px 10px;
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 12px;
	background: white;
	cursor: pointer;
	font-size: 12px;
}
.chip.active { background: var(--primary, #2563eb); color: white; border-color: var(--primary, #2563eb); }
.chip.gray { color: var(--text-muted, #888); }
.chip.blue { color: #1e40af; }
.chip.orange { color: #c2410c; }
.chip.red { color: #991b1b; }
.chip.green { color: #15803d; }
.chip.green-solid { color: #065f46; }
.chip-n {
	margin-left: 4px;
	padding: 0 4px;
	background: rgba(0, 0, 0, 0.06);
	border-radius: 6px;
	font-size: 10px;
}
.row-table {
	width: 100%;
	border-collapse: collapse;
}
.row-table th, .row-table td {
	padding: 6px 8px;
	border-bottom: 1px solid var(--border-color, #e5e7eb);
	text-align: left;
	font-size: 12px;
	vertical-align: top;
}
.row-table th { background: var(--bg-light-gray, #f9fafb); font-weight: 500; }
.row-table .num { text-align: right; width: 60px; }
.row-table .payload { max-width: 380px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.error-cell { color: #991b1b; font-size: 11px; max-width: 200px; }
.badge {
	display: inline-block;
	padding: 2px 6px;
	border-radius: 8px;
	font-size: 10px;
	background: var(--gray-200, #e5e7eb);
}
.badge.new { background: #f3f4f6; color: #4b5563; }
.badge.exists { background: #dbeafe; color: #1e40af; }
.badge.conflict { background: #fed7aa; color: #c2410c; }
.badge.invalid { background: #fecaca; color: #991b1b; }
.badge.skipped { background: #e5e7eb; color: #6b7280; }
.badge.ready { background: #d1fae5; color: #15803d; }
.badge.posted { background: #10b981; color: white; }
.badge.failed { background: #fecaca; color: #991b1b; }
.badge.reversed { background: #fde68a; color: #92400e; }
.badge-done {
	padding: 4px 12px;
	background: #d1fae5;
	color: #15803d;
	border-radius: 12px;
	font-size: 13px;
	font-weight: 600;
}
.loading, .empty {
	padding: 32px;
	text-align: center;
	color: var(--text-muted, #888);
	font-size: 13px;
}
.pagination {
	display: flex;
	justify-content: center;
	gap: 12px;
	align-items: center;
	margin-top: 12px;
	font-size: 13px;
}
.pagination button {
	padding: 4px 10px;
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 4px;
	background: white;
	cursor: pointer;
}

.demo-banner {
	display: flex; align-items: center; gap: 10px;
	padding: 10px 14px;
	background: #fff7ed; color: #92400e;
	border: 1px solid #fdba74; border-radius: 6px;
	margin: 8px 0 12px;
	font-size: 13px;
}
.demo-banner .demo-icon { font-size: 18px; }
.demo-banner .demo-text { flex: 1; }
.btn-warning {
	background: #f59e0b; color: white; border: none;
	padding: 6px 14px; border-radius: 4px;
	cursor: pointer; font-size: 13px;
}
.btn-warning:hover { background: #d97706; }
</style>
