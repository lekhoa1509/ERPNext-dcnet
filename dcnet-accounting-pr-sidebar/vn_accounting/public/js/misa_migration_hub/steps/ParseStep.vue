<template>
	<div class="parse-step">
		<div class="card">
			<div class="header-row">
				<div>
					<h3>{{ __("Phân tích file") }}</h3>
					<p class="muted">
						{{ __("Đọc nội dung từng file, tách hàng, phân loại tự động theo dedupe + auto-detect.") }}
					</p>
				</div>
				<div>
					<button
						v-if="store.status === 'UPLOADED'"
						class="btn btn-primary"
						:disabled="busy"
						@click="onStart"
					>
						<template v-if="busy">{{ __("Đang phân tích...") }}</template>
						<template v-else-if="isStaleUploaded">{{ __("Hoàn tất chuyển bước (đã phân tích xong) →") }}</template>
						<template v-else>{{ __("Bắt đầu phân tích") }}</template>
					</button>
					<button
						v-else-if="store.status === 'PARSED' || store.status === 'REVIEWED'"
						class="btn btn-primary"
						@click="$emit('next')"
					>
						{{ __("Sang bước Duyệt →") }}
					</button>
				</div>
			</div>

			<div v-if="error" class="error">{{ error }}</div>

			<div v-if="isStaleUploaded" class="stale-uploaded-banner">
				<strong>⚠ {{ __("Trạng thái batch chưa cập nhật") }}</strong>
				<p>
					{{ __("Tất cả file đã được phân tích thành công nhưng trạng thái batch vẫn là UPLOADED — thường do worker bị restart trong lúc chuyển trạng thái cuối. Bấm nút bên phải để hoàn tất chuyển trạng thái sang PARSED (không phân tích lại file).") }}
				</p>
			</div>

			<!-- Educational panel: what "Parsing" actually does (collapsible, default open while UPLOADED). -->
			<details class="parse-explainer" :open="store.status === 'UPLOADED' || isParsing">
				<summary>
					{{ __("🔍 Bước này làm gì? Bấm để xem chi tiết") }}
				</summary>
				<div class="parse-explainer-body">
					<p>
						{{ __("Phân tích = đọc nội dung từng file Excel của Misa, bóc tách dữ liệu thô thành các bản ghi chuẩn hóa để ERPNext hiểu được. Đây là bước \"đọc hiểu\" — chưa ghi gì vào sổ cái, chưa tạo doc nào trong ERPNext, có thể chạy lại nhiều lần an toàn.") }}
					</p>
					<div class="parse-explainer-tasks">
						<div class="task-item">
							<strong>📋 1. Đọc Excel (openpyxl streaming)</strong>
							<p>{{ __("Mở từng file .xlsx ở chế độ read-only, lướt qua từng sheet/hàng/ô. File NKC 2025 (~6 MB) có ~90.000 dòng → mất 3-6 phút. Streaming = không nạp cả file vào RAM nên không bị OOM ngay cả khi file > 100 MB.") }}</p>
						</div>
						<div class="task-item">
							<strong>🧭 2. Tìm dòng tiêu đề</strong>
							<p>{{ __("Misa xuất file có 1-3 dòng metadata trên đầu (logo, tiêu đề, công ty) trước khi đến header thật. Hệ thống quét tối đa 15 dòng đầu để tìm cột \"STT\" hoặc dòng có ≥2 ô không rỗng, rồi mới bắt đầu đọc data thực.") }}</p>
						</div>
						<div class="task-item">
							<strong>🏷️ 3. Phân loại từng file</strong>
							<p>{{ __("Dựa vào tên file + header pattern, hệ thống auto-detect 44+ loại file Misa: NKC, Bảng kê BR/MV, SCT, OB Account Balance, OB Inventory, Customer/Supplier, Item, Account, Cost Center... Sai loại = sai pipeline.") }}</p>
						</div>
						<div class="task-item">
							<strong>🔑 4. Trích voucher_no</strong>
							<p>{{ __("Mỗi dòng NKC/SCT/Bảng kê được denormalize cột số chứng từ ra một cột riêng (voucher_no) có index — sau này khi UPDATE-by-voucher (rất nhiều) sẽ dùng index thay vì full table scan, tăng tốc Phase 4 lên 10-50x.") }}</p>
						</div>
						<div class="task-item">
							<strong>📦 5. Bulk insert vào Misa Migration Row</strong>
							<p>{{ __("Mỗi 200 dòng được commit 1 lần (không phải mỗi dòng) — nhanh hơn ~50x. Cột raw_payload lưu nguyên bản JSON gốc để Phase D-E sau này có thể re-process mà không cần đọc lại Excel.") }}</p>
						</div>
						<div class="task-item">
							<strong>⚡ 6. Classify (preview)</strong>
							<p>{{ __("Sau khi parse xong toàn batch, hệ thống chạy preview_row trên từng dòng → đánh dấu New/Conflict/Exists/Invalid để bước Duyệt hiển thị thống kê tức thì. Khoảng 100k+ dòng được phân loại trong < 30s.") }}</p>
						</div>
					</div>
					<div class="parse-explainer-storage">
						<strong>📍 Dữ liệu Parse được lưu ở đâu?</strong>
						<p>
							{{ __("Mỗi dòng dữ liệu thô từ file Misa được lưu vào bảng") }}
							<code>tabMisa Migration Row</code>
							{{ __("dưới dạng JSON nguyên bản (cột raw_payload). Bảng này là một DocType ERPNext bình thường — bạn có thể truy cập trực tiếp tại") }}
							<a href="/app/misa-migration-row" target="_blank">/app/misa-migration-row</a>
							{{ __("nếu cần debug hoặc kiểm tra từng dòng. Mỗi dòng có trường") }}
							<code>status</code>
							{{ __("(New / Conflict / Exists / Invalid / Ready / Posted / Failed / Reversed) phản ánh vòng đời của nó qua các bước tiếp theo.") }}
						</p>
					</div>

					<div class="parse-explainer-next">
						<strong>🚦 Sau khi Parse xong, dữ liệu sẽ đi đâu?</strong>
						<div class="next-flow">
							<div class="flow-step done">
								<div class="flow-step-num">1</div>
								<div class="flow-step-body">
									<strong>{{ __("Bước hiện tại — Parse") }}</strong>
									<p>{{ __("Đọc + chuẩn hóa → Misa Migration Row (status=New). Chưa ghi gì vào ERPNext.") }}</p>
								</div>
							</div>
							<div class="flow-arrow">→</div>
							<div class="flow-step">
								<div class="flow-step-num">2</div>
								<div class="flow-step-body">
									<strong>{{ __("Bước Duyệt") }}</strong>
									<p>{{ __("Hệ thống dedupe + phân loại từng dòng → cập nhật status thành Exists (đã có trong ERPNext) / Conflict (cần resolve) / Ready (sẵn sàng tạo) / Invalid (thiếu trường bắt buộc). Bạn xem trước, chỉnh sửa, skip những dòng không muốn.") }}</p>
								</div>
							</div>
							<div class="flow-arrow">→</div>
							<div class="flow-step">
								<div class="flow-step-num">3</div>
								<div class="flow-step-body">
									<strong>{{ __("Bước Tạo") }}</strong>
									<p>{{ __("Pre-flight kiểm tra 8 ràng buộc (bút toán cân, kỳ chưa khóa, master đã import, v.v.) → enqueue background job xử lý theo thứ tự Phase 1 → 2 → 3 → 0 → 4a → 4b. Mỗi dòng Ready được biến thành 1 doc ERPNext thực sự (Customer, Supplier, Item, Sales Invoice, Payment Entry...) ghi vào sổ cái.") }}</p>
								</div>
							</div>
						</div>
					</div>

					<p class="parse-explainer-footnote">
						{{ __("💡 Toàn bộ quy trình có thể HOÀN TÁC bằng nút \"Hoàn tác (Undo)\" sau khi tạo — hệ thống lưu mapping target_doctype + target_name trên mỗi Misa Migration Row để cancel + delete chính xác doc đã tạo. Phase 0 (OB) được bảo vệ riêng, không bị hoàn tác chung với Phase 4.") }}
					</p>
				</div>
			</details>

			<div class="status-banner" :class="store.status.toLowerCase()">
				{{ __("Trạng thái batch:") }} <strong>{{ store.status }}</strong>
				· {{ __("Tổng số dòng:") }} <strong>{{ store.total_rows.toLocaleString() }}</strong>
				<span v-if="isParsing || elapsedLabel" class="muted">
					· {{ __("Thời gian:") }} <strong>{{ elapsedLabel }}</strong>
				</span>
			</div>

			<!-- Overall + per-file progress: shown while parsing OR right after to keep the final state visible. -->
			<div v-if="isParsing || (filesProcessed > 0 && store.status === 'UPLOADED')" class="overall-progress">
				<div class="overall-progress-header">
					<strong>{{ overallPct }}%</strong>
					<span class="overall-progress-stats">
						<span class="muted">{{ __("File") }}:</span>
						<strong>{{ filesProcessed }}/{{ totalFiles }}</strong>
						<span class="muted"> · {{ __("Dòng") }}:</span>
						<strong>{{ rowsDone.toLocaleString() }}</strong>
						<span class="muted">/ {{ rowsExpected.toLocaleString() }}</span>
					</span>
				</div>
				<div class="overall-progress-bar">
					<span :style="{ width: overallPct + '%' }"></span>
				</div>

				<!-- Currently-parsing files list (parallel mode → multiple at once) -->
				<div v-if="parsingFiles.length" class="parsing-live-list">
					<div v-for="f in parsingFiles" :key="f.name" class="parsing-live-row">
						<span class="row-spinner">⟳</span>
						<span class="parsing-live-name">{{ f.original_filename }}</span>
						<span class="parsing-live-progress">
							<template v-if="f.total_rows_expected">
								<strong>{{ (f.row_count || 0).toLocaleString() }}</strong>
								<span class="muted">/ {{ f.total_rows_expected.toLocaleString() }} ({{ _pctOf(f.row_count, f.total_rows_expected) }}%)</span>
							</template>
							<template v-else>
								<strong>{{ (f.row_count || 0).toLocaleString() }}</strong>
								<span class="muted">{{ __("dòng") }}</span>
							</template>
						</span>
					</div>
				</div>
			</div>

			<table v-if="files.length" class="file-table">
				<thead>
					<tr>
						<th>{{ __("File") }}</th>
						<th>{{ __("Loại") }}</th>
						<th>{{ __("Trạng thái") }}</th>
						<th class="num">{{ __("Số dòng") }}</th>
						<th>{{ __("Lỗi") }}</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="f in files" :key="f.name">
						<td>{{ f.original_filename || f.file_url }}</td>
						<td>{{ f.file_type }}</td>
						<td>
							<span class="badge" :class="(f.parse_status || 'pending').toLowerCase()">
								<template v-if="f.parse_status === 'Parsing'">
									<span class="row-spinner">⟳</span> {{ f.parse_status }}
								</template>
								<template v-else>{{ f.parse_status || 'Pending' }}</template>
							</span>
						</td>
						<td class="num">
							<template v-if="f.parse_status === 'Parsing' && f.total_rows_expected">
								<strong>{{ (f.row_count || 0).toLocaleString() }}</strong>
								<span class="muted"> / {{ f.total_rows_expected.toLocaleString() }}</span>
								<div class="row-mini-bar">
									<span :style="{ width: _pctOf(f.row_count, f.total_rows_expected) + '%' }"></span>
								</div>
							</template>
							<template v-else>
								{{ (f.row_count || 0).toLocaleString() }}
							</template>
						</td>
						<td class="error-cell">{{ (f.parse_error || '').slice(0, 80) }}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from "vue";
import { useMisaStore } from "../store.js";

defineEmits(["next"]);

const store = useMisaStore();
const busy = ref(false);
const error = ref(null);
const files = computed(() => store.files);

const isParsing = computed(() => (store.files || []).some(f => f.parse_status === "Parsing"));
const parsingFile = computed(() => (store.files || []).find(f => f.parse_status === "Parsing"));
const parsingFileLabel = computed(() => parsingFile.value?.original_filename || "");
const parsingFileRows = computed(() => parsingFile.value?.row_count || 0);
const parsingFileTotal = computed(() => parsingFile.value?.total_rows_expected || 0);

// All files currently in Parsing state — parallel mode flips 2-3 at once.
const parsingFiles = computed(() => (store.files || []).filter(f => f.parse_status === "Parsing"));

// Aggregate row counts across the batch for the overall progress bar.
// rowsDone counts everything inserted so far (Parsed final + Parsing live).
// rowsExpected uses total_rows_expected when known (per-file estimated by
// openpyxl max_row at parse start), falls back to row_count for Parsed files
// (where final count is known authoritatively) so the bar never overshoots.
const totalFiles = computed(() => (store.files || []).length);
const filesProcessed = computed(() => (store.files || []).filter(f => f.parse_status === "Parsed" || f.parse_status === "Failed").length);
const rowsDone = computed(() => (store.files || []).reduce((sum, f) => sum + (f.row_count || 0), 0));
const rowsExpected = computed(() => (store.files || []).reduce((sum, f) => {
	if (f.parse_status === "Parsed" || f.parse_status === "Failed") {
		return sum + (f.row_count || 0);
	}
	return sum + Math.max(f.total_rows_expected || 0, f.row_count || 0);
}, 0));
const overallPct = computed(() => {
	// Blend file-level and row-level progress so the bar moves while NKC chugs
	// even though file count stays the same. 50% file weight + 50% row weight.
	const filePct = totalFiles.value ? (filesProcessed.value / totalFiles.value) * 100 : 0;
	const rowPct = rowsExpected.value ? (rowsDone.value / rowsExpected.value) * 100 : 0;
	return Math.min(100, Math.round((filePct + rowPct) / 2));
});

// Live elapsed timer — starts when isParsing flips true, freezes after parse ends.
const elapsedMs = ref(0);
const parseStartTs = ref(null);
const parseEndTs = ref(null);
let elapsedTickHandle = null;
function _fmtElapsed(ms) {
	if (!ms || ms < 0) return "";
	const s = Math.floor(ms / 1000);
	const m = Math.floor(s / 60);
	const remS = s % 60;
	if (m > 0) return `${m}m ${remS}s`;
	return `${remS}s`;
}
const elapsedLabel = computed(() => _fmtElapsed(elapsedMs.value));

// Stale-UPLOADED detection: batch state did not transition to PARSED
// (typically because the worker crashed during the final state transition),
// but every file in the batch has parse_status='Parsed' with row_count > 0.
// Re-clicking the primary button is now idempotent (parse_job skips already-
// Parsed files), so the operator can recover without losing parse progress.
const isStaleUploaded = computed(() => {
	if (store.status !== "UPLOADED") return false;
	const files = store.files || [];
	if (!files.length) return false;
	return files.every(f => f.parse_status === "Parsed" && (f.row_count || 0) > 0);
});

function _pctOf(n, total) {
	if (!total || total <= 0) return 0;
	return Math.min(100, Math.round((n || 0) * 100 / total));
}

function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

let realtimeOff = null;
let pollTimer = null;

function _hasParsingFile() {
	return (store.files || []).some(f => f.parse_status === "Parsing");
}

function _tickElapsed() {
	if (parseStartTs.value && !parseEndTs.value) {
		elapsedMs.value = Date.now() - parseStartTs.value;
	} else if (parseStartTs.value && parseEndTs.value) {
		// Frozen — show the final duration after parse ends.
		elapsedMs.value = parseEndTs.value - parseStartTs.value;
	}
}

onMounted(() => {
	// Subscribe to realtime progress (push)
	if (window.frappe && frappe.realtime && typeof frappe.realtime.on === "function") {
		const handler = (payload) => {
			if (payload?.batch && payload.batch !== store.batch_name) return;
			// payload may include {file, done, status, total_rows, ...}
			store.refreshBatch().catch(() => {});
		};
		frappe.realtime.on("misa_migration:parse_progress", handler);
		realtimeOff = () => frappe.realtime.off?.("misa_migration:parse_progress", handler);
	}
	// Poll fallback every 2s while a file is in 'Parsing' state — realtime
	// can drop messages, and for large files (90k+ rows over ~6 min) the
	// UI otherwise appears stuck. Polling stops automatically when no file
	// is currently parsing.
	pollTimer = setInterval(() => {
		if (_hasParsingFile() || store.status === "UPLOADED") {
			store.refreshBatch().catch(() => {});
		}
		// Detect parse start/end transitions to drive the elapsed timer.
		if (_hasParsingFile() && !parseStartTs.value) {
			parseStartTs.value = Date.now();
			parseEndTs.value = null;
		}
		if (!_hasParsingFile() && parseStartTs.value && !parseEndTs.value) {
			parseEndTs.value = Date.now();
		}
	}, 2000);
	// Tighter elapsed update so the timer looks live (500ms).
	elapsedTickHandle = setInterval(_tickElapsed, 500);
});

onBeforeUnmount(() => {
	if (realtimeOff) realtimeOff();
	if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }
	if (elapsedTickHandle) { clearInterval(elapsedTickHandle); elapsedTickHandle = null; }
});

async function onStart() {
	error.value = null;
	busy.value = true;
	// Reset elapsed timer for this run (re-clicks should restart at 0).
	parseStartTs.value = null;
	parseEndTs.value = null;
	elapsedMs.value = 0;
	try {
		// sync=false → enqueue background job. Polling not needed beyond realtime.
		await store.startParse(false);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}
</script>

<style scoped>
.parse-step .card {
	background: var(--card-bg, #fff);
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 8px;
	padding: 20px;
}

.header-row {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	gap: 16px;
	margin-bottom: 16px;
}

.muted { color: var(--text-muted, #888); font-size: 13px; margin: 4px 0 0; }
.error {
	margin: 12px 0;
	padding: 8px 12px;
	background: #fef2f2;
	color: #991b1b;
	border-radius: 4px;
	font-size: 13px;
}

.stale-uploaded-banner {
	margin: 12px 0;
	padding: 10px 14px;
	background: #fffbeb;
	border: 1px solid #fcd34d;
	border-left: 4px solid #f59e0b;
	border-radius: 4px;
	font-size: 13px;
	color: #78350f;
}
.stale-uploaded-banner strong { display: block; margin-bottom: 4px; }
.stale-uploaded-banner p { margin: 0; line-height: 1.5; }

.status-banner {
	padding: 10px 14px;
	background: var(--bg-light-gray, #f3f4f6);
	border-radius: 6px;
	font-size: 13px;
	margin: 12px 0;
}
.status-banner.posted { background: #ecfdf5; }
.status-banner.reversed { background: #fff7ed; }
.status-banner.stuck { background: #fef2f2; }
.parsing-live-hint { margin-left: 6px; color: #78350f; }
.row-spinner { display: inline-block; animation: spin 1.4s linear infinite; color: #f59e0b; font-weight: 700; }
@keyframes spin { from { transform: rotate(0); } to { transform: rotate(360deg); } }

/* Overall progress card — shown during + right after parse */
.overall-progress {
	margin: 12px 0;
	padding: 12px 14px;
	background: #f9fafb;
	border: 1px solid #e5e7eb;
	border-radius: 6px;
	font-size: 13px;
}
.overall-progress-header {
	display: flex;
	align-items: baseline;
	justify-content: space-between;
	gap: 12px;
	margin-bottom: 8px;
}
.overall-progress-header > strong:first-child {
	font-size: 18px;
	color: #1e3a8a;
	min-width: 4ch;
}
.overall-progress-stats { color: #374151; }
.overall-progress-stats strong { color: #111827; }
.overall-progress-bar {
	height: 10px;
	background: #e5e7eb;
	border-radius: 5px;
	overflow: hidden;
	position: relative;
}
.overall-progress-bar > span {
	display: block;
	height: 100%;
	background: linear-gradient(90deg, #3b82f6, #2563eb);
	transition: width 0.3s ease;
}

/* Currently-parsing files (parallel mode → multiple at once) */
.parsing-live-list {
	margin-top: 10px;
	display: flex;
	flex-direction: column;
	gap: 4px;
}
.parsing-live-row {
	display: flex;
	align-items: baseline;
	gap: 8px;
	padding: 4px 8px;
	background: white;
	border-radius: 3px;
	border-left: 3px solid #f59e0b;
	font-size: 12px;
}
.parsing-live-name {
	flex: 1 1 auto;
	min-width: 0;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	color: #1f2937;
	font-weight: 500;
}
.parsing-live-progress { flex: 0 0 auto; color: #374151; }

/* Educational explainer: what Parsing actually does */
.parse-explainer {
	margin: 12px 0 14px;
	padding: 10px 14px;
	background: #eff6ff;
	border: 1px solid #bfdbfe;
	border-radius: 6px;
	font-size: 13px;
}
.parse-explainer summary {
	cursor: pointer;
	font-weight: 500;
	color: #1e3a8a;
	padding: 2px 0;
}
.parse-explainer summary:hover { color: #0c1f6b; }
.parse-explainer-body {
	margin-top: 10px;
	padding-top: 10px;
	border-top: 1px solid #bfdbfe;
}
.parse-explainer-body > p {
	margin: 0 0 12px;
	line-height: 1.55;
	color: #1f2937;
}
.parse-explainer-tasks {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 10px 14px;
}
@media (max-width: 820px) {
	.parse-explainer-tasks { grid-template-columns: 1fr; }
}
.task-item {
	background: white;
	padding: 8px 10px;
	border-radius: 4px;
	border-left: 3px solid #3b82f6;
}
.task-item strong {
	display: block;
	color: #1e3a8a;
	font-size: 12px;
	margin-bottom: 4px;
}
.task-item p {
	margin: 0;
	font-size: 12px;
	line-height: 1.5;
	color: #4b5563;
}
.parse-explainer-footnote {
	margin: 12px 0 0;
	padding: 8px 10px;
	background: #fffbeb;
	border-left: 3px solid #f59e0b;
	border-radius: 3px;
	font-size: 12px;
	color: #78350f;
	line-height: 1.5;
}

/* Storage + next-step flow */
.parse-explainer-storage {
	margin-top: 12px;
	padding: 10px 12px;
	background: white;
	border: 1px solid #bfdbfe;
	border-radius: 4px;
}
.parse-explainer-storage > strong { color: #1e3a8a; font-size: 13px; }
.parse-explainer-storage p {
	margin: 6px 0 0;
	font-size: 12px;
	line-height: 1.55;
	color: #4b5563;
}
.parse-explainer-storage code {
	background: #eef2ff;
	color: #312e81;
	padding: 1px 4px;
	border-radius: 2px;
	font-size: 11px;
}
.parse-explainer-storage a {
	color: #2563eb;
	text-decoration: underline dotted;
}

.parse-explainer-next {
	margin-top: 12px;
	padding: 10px 12px;
	background: white;
	border: 1px solid #bfdbfe;
	border-radius: 4px;
}
.parse-explainer-next > strong { color: #1e3a8a; font-size: 13px; }
.next-flow {
	display: flex; align-items: stretch; gap: 6px;
	margin-top: 8px;
	overflow-x: auto;
}
.flow-step {
	flex: 1 1 0;
	min-width: 180px;
	padding: 8px 10px;
	background: #f9fafb;
	border-radius: 4px;
	border: 1px solid #e5e7eb;
	display: flex; align-items: flex-start; gap: 8px;
}
.flow-step.done { background: #ecfdf5; border-color: #a7f3d0; }
.flow-step-num {
	flex: 0 0 22px; height: 22px;
	border-radius: 50%;
	background: #3b82f6; color: white;
	font-weight: 700; font-size: 11px;
	display: inline-flex; align-items: center; justify-content: center;
}
.flow-step.done .flow-step-num { background: #10b981; }
.flow-step-body strong {
	display: block; font-size: 12px; color: #1e3a8a; margin-bottom: 3px;
}
.flow-step.done .flow-step-body strong { color: #065f46; }
.flow-step-body p {
	margin: 0; font-size: 11px; line-height: 1.45;
	color: #4b5563;
}
.flow-arrow {
	display: flex; align-items: center;
	color: #9ca3af; font-size: 18px; padding: 0 2px;
}
@media (max-width: 820px) {
	.next-flow { flex-direction: column; }
	.flow-arrow { transform: rotate(90deg); padding: 4px 0; }
}

/* Mini progress bar inside the Số dòng cell during parsing */
.row-mini-bar {
	margin-top: 3px;
	height: 4px;
	background: #e5e7eb;
	border-radius: 2px;
	overflow: hidden;
}
.row-mini-bar > span {
	display: block;
	height: 100%;
	background: #3b82f6;
	transition: width 0.4s ease;
}

.file-table {
	width: 100%;
	border-collapse: collapse;
	margin-top: 12px;
}
.file-table th, .file-table td {
	padding: 8px;
	border-bottom: 1px solid var(--border-color, #e5e7eb);
	text-align: left;
	font-size: 13px;
}
.file-table th { background: var(--bg-light-gray, #f9fafb); font-weight: 500; }
.file-table .num { text-align: right; }
.error-cell { color: #991b1b; font-size: 11px; max-width: 240px; }

.badge {
	display: inline-block;
	padding: 2px 8px;
	border-radius: 10px;
	font-size: 11px;
	background: var(--gray-200, #e5e7eb);
}
.badge.parsing { background: #dbeafe; color: #1e40af; }
.badge.parsed { background: #d1fae5; color: #065f46; }
.badge.failed { background: #fee2e2; color: #991b1b; }
</style>
