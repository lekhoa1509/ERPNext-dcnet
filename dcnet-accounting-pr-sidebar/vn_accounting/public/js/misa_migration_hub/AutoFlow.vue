<template>
	<div class="auto-flow">
		<!-- ════════ ZONE A — Setup: chọn công ty + thả file + 1 nút ════════ -->
		<div v-if="mode === 'setup'" class="card setup-card">
			<div class="setup-grid">
				<div class="form-row company-autocomplete">
					<label>{{ __("Công ty nhận dữ liệu") }} <span class="reqd">*</span></label>
					<div class="company-picker">
						<input
							v-model="form.company"
							type="text"
							:placeholder="__('Gõ để tìm công ty…')"
							autocomplete="off"
							@focus="onCompanyFocus"
							@input="onCompanyType"
							@blur="onCompanyBlur"
						/>
						<div v-if="showCompanyDropdown && companyOptions.length" class="company-dropdown">
							<div
								v-for="c in companyOptions"
								:key="c.name"
								class="company-option"
								@mousedown.prevent="selectCompany(c.name)"
							>
								<span class="company-option-name">{{ c.name }}</span>
								<span class="muted">{{ c.default_currency }}</span>
							</div>
						</div>
						<div v-if="showCompanyDropdown && !companyOptions.length && !companyLoading" class="company-empty">
							{{ __("Không tìm thấy.") }}
							<a :href="'/app/company/new?company_name=' + encodeURIComponent(form.company)" target="_blank">
								{{ __("Tạo công ty mới") }}
							</a>
						</div>
					</div>
					<small v-if="form.company && !companyValidated" class="hint error-hint">
						⚠ {{ __("Công ty chưa tồn tại — chọn từ gợi ý hoặc tạo mới (tiền tệ VND).") }}
					</small>
					<small v-else class="hint">
						{{ __("Công ty mới tạo (VND) sẽ được tự cài hệ thống tài khoản TT99/2025 + tài khoản từ file Misa.") }}
					</small>
				</div>
				<div class="form-row">
					<label>{{ __("Tên đợt migration") }}</label>
					<input v-model="form.batch_title" type="text" :placeholder="__('VD: Số liệu 2025')" />
				</div>
			</div>

			<div
				class="dropzone"
				:class="{ over: dragOver }"
				role="button"
				tabindex="0"
				@click="fileInput && fileInput.click()"
				@dragover.prevent="dragOver = true"
				@dragleave="dragOver = false"
				@drop.prevent="onDrop"
			>
				<input
					ref="fileInput"
					type="file"
					accept=".xlsx,.xls"
					multiple
					style="display: none"
					@click="$event.target.value = ''"
					@change="onFileInput"
				/>
				<div class="dz-icon">📂</div>
				<div class="dz-title">{{ __("Kéo thả TOÀN BỘ file Excel xuất từ Misa vào đây") }}</div>
				<div class="muted">{{ __("Hoặc bấm để chọn nhiều file (.xlsx / .xls). Hệ thống tự nhận diện loại từng file.") }}</div>
			</div>

			<div v-if="picked.length" class="picked-list">
				<table class="file-table">
					<thead>
						<tr>
							<th>{{ __("Tên file") }}</th>
							<th>{{ __("Loại đã nhận diện") }}</th>
							<th>{{ __("Dung lượng") }}</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(p, i) in picked" :key="p.file.name + i">
							<td class="fname">{{ p.file.name }}</td>
							<td>
								<select v-model="p.file_type" :class="{ unknown: p.file_type === 'Unknown' }">
									<option v-for="opt in FILE_TYPE_OPTIONS" :key="opt" :value="opt">{{ typeLabel(opt) }}</option>
								</select>
							</td>
							<td class="muted">{{ formatBytes(p.file.size) }}</td>
							<td><button class="btn btn-xs btn-link" :title="__('Bỏ file này')" @click="picked.splice(i, 1)">×</button></td>
						</tr>
					</tbody>
				</table>
				<small v-if="unknownCount" class="hint warn-hint">
					⚠ {{ __("{0} file chưa nhận diện được loại — chọn loại thủ công hoặc bỏ ra.").replace("{0}", unknownCount) }}
				</small>
				<small v-else-if="skipCount" class="hint">
					{{ __("{0} file ngoài phạm vi import sẽ được bỏ qua (đổi cột Loại nếu muốn import).").replace("{0}", skipCount) }}
				</small>
			</div>

			<details class="advanced">
				<summary>{{ __("Tùy chọn nâng cao") }}</summary>
				<div class="form-row">
					<label>{{ __("Ngày chốt số dư đầu kỳ") }}</label>
					<input v-model="form.ob_posting_date" type="date" />
					<small class="hint">{{ __("Để trống = tự xác định từ dữ liệu (ngày liền trước chứng từ sớm nhất). VD dữ liệu 2025 → 31/12/2024.") }}</small>
				</div>
			</details>

			<div class="start-bar">
				<button
					class="btn btn-primary btn-lg start-btn"
					:disabled="!canStart"
					@click="onStart"
				>
					🚀 {{ __("Bắt đầu migration") }}
				</button>
				<span class="muted">
					{{ __("Sau khi bấm, toàn bộ quy trình chạy tự động: phân tích → tài khoản & danh mục → kiểm tra → tạo chứng từ → đối chiếu.") }}
				</span>
			</div>
			<div v-if="error" class="error">{{ error }}</div>
		</div>

		<!-- ════════ ZONE B — Uploading files ════════ -->
		<div v-else-if="mode === 'uploading'" class="card progress-card">
			<h3>{{ __("Đang tải file lên…") }}</h3>
			<div class="bar"><div class="bar-fill" :style="{ width: uploadPct + '%' }"></div></div>
			<p class="activity">{{ __("Đã tải {0}/{1} file").replace("{0}", uploadedCount).replace("{1}", picked.length) }} — {{ currentUploadName }}</p>
		</div>

		<!-- ════════ ZONE C — Pipeline running / blocked / failed / done ════════ -->
		<div v-else class="card progress-card">
			<div class="run-header">
				<div>
					<h3>{{ store.batch_title || store.batch_name }}</h3>
					<p class="muted">
						{{ store.company }}
						<span v-if="obDateLabel"> · {{ __("Số dư đầu kỳ:") }} {{ obDateLabel }}</span>
						· {{ totalRowsLabel }}
					</p>
				</div>
				<div class="run-header-right">
					<span class="elapsed" v-if="elapsedLabel">⏱ {{ elapsedLabel }}</span>
				</div>
			</div>

			<div class="bar big">
				<div class="bar-fill" :class="{ danger: hasFailed, warn: isBlocked }" :style="{ width: overallPct + '%' }"></div>
			</div>

			<ul class="stage-list">
				<li v-for="s in stages" :key="s.key" class="stage" :class="s.status">
					<span class="stage-ico">
						<template v-if="s.status === 'done'">✅</template>
						<template v-else-if="s.status === 'running'"><span class="spinner"></span></template>
						<template v-else-if="s.status === 'failed'">❌</template>
						<template v-else-if="s.status === 'blocked'">⚠️</template>
						<template v-else>○</template>
					</span>
					<span class="stage-label">{{ s.label }}</span>
					<span class="stage-detail muted">{{ s.detail }}</span>
				</li>
			</ul>

			<p v-if="isRunning && activity" class="activity">
				<span class="spinner small"></span> {{ activity }}
			</p>
			<div v-if="isRunning" class="live-chips">
				<span v-if="rc.Posted" class="chip ok">{{ __("Đã tạo:") }} {{ fmtN(rc.Posted) }}</span>
				<span v-if="rc.Ready" class="chip">{{ __("Đang chờ:") }} {{ fmtN(rc.Ready) }}</span>
				<span v-if="rc.Failed" class="chip bad">{{ __("Lỗi:") }} {{ fmtN(rc.Failed) }}</span>
				<span v-if="rc.Skipped" class="chip">{{ __("Bỏ qua:") }} {{ fmtN(rc.Skipped) }}</span>
			</div>
			<p v-if="isRunning" class="hint bg-hint">
				💡 {{ __("Migration chạy nền trên máy chủ — có thể rời trang này, quay lại vẫn thấy tiến trình.") }}
			</p>

			<!-- Blocked: cần người dùng xử lý -->
			<div v-if="isBlocked" class="blocker-panel">
				<h4>⚠️ {{ __("Cần xử lý trước khi tiếp tục") }}</h4>
				<p class="muted">{{ __("Pipeline tạm dừng vì dữ liệu có vấn đề phải sửa. Sửa xong bấm “Chạy tiếp”.") }}</p>
				<ul class="blocker-list">
					<li v-for="(b, i) in blockers" :key="i" :class="b.level">
						<span class="chip" :class="b.level === 'block' ? 'bad' : 'warnc'">{{ b.level === "block" ? __("Chặn") : __("Cảnh báo") }}</span>
						{{ b.message }}
					</li>
				</ul>
				<div class="actions">
					<button class="btn btn-primary" :disabled="busy" @click="onResume">{{ __("Chạy tiếp") }}</button>
					<button class="btn btn-default" :disabled="busy" @click="$emit('discard')">{{ __("Bỏ đợt này") }}</button>
				</div>
			</div>

			<!-- Dead job: stage "đang chạy" nhưng server không ghi nhận tiến
			     triển nhiều phút (worker bị restart giữa chừng) -->
			<div v-if="isStale" class="blocker-panel">
				<h4>⏸ {{ __("Tiến trình có vẻ đã dừng") }}</h4>
				<p class="muted">{{ __("Máy chủ không ghi nhận tiến triển trong vài phút (có thể do khởi động lại). Bấm để chạy tiếp từ chỗ dừng — các phần đã xong sẽ không chạy lại.") }}</p>
				<div class="actions">
					<button class="btn btn-primary" :disabled="busy" @click="onResume">{{ __("Chạy tiếp") }}</button>
				</div>
			</div>

			<!-- Failed / STUCK -->
			<div v-if="hasFailed || store.status === 'STUCK'" class="blocker-panel">
				<h4>❌ {{ __("Migration gặp lỗi") }}</h4>
				<p class="error-text">{{ pipelineError || __("Xem chi tiết trong Error Log.") }}</p>
				<div class="actions">
					<button class="btn btn-primary" :disabled="busy" @click="onResumeStuck">{{ __("Chạy tiếp từ chỗ dừng") }}</button>
					<a class="btn btn-default" href="/app/error-log" target="_blank">{{ __("Xem nhật ký lỗi") }}</a>
				</div>
			</div>

			<!-- Done: kết quả + đối chiếu -->
			<div v-if="isDone" class="result-panel">
				<h4>🎉 {{ __("Hoàn tất!") }}</h4>

				<div class="result-row" :class="glBalanced ? 'good' : 'bad-row'">
					<span class="result-ico">{{ glBalanced ? "✅" : "❌" }}</span>
					<span v-if="glBalanced">{{ __("Bảng cân đối CÂN — tổng Nợ bằng tổng Có") }} ({{ fmtVnd(result.gl_balance.total_debit) }})</span>
					<span v-else>{{ __("Bảng cân đối LỆCH") }} {{ fmtVnd(result.gl_balance.diff) }} — {{ __("cần kiểm tra!") }}</span>
				</div>

				<div v-if="tb" class="result-row" :class="tbPerfect ? 'good' : 'warn-row'">
					<span class="result-ico">{{ tbPerfect ? "✅" : "⚠️" }}</span>
					<span>
						{{ __("Số dư cuối kỳ khớp file Misa:") }}
						<strong>{{ tb.matches }}/{{ tb.total_tks }} {{ __("tài khoản") }} ({{ tb.accuracy_pct }}%)</strong>
					</span>
				</div>
				<div v-if="inv" class="result-row" :class="invPerfect ? 'good' : 'warn-row'">
					<span class="result-ico">{{ invPerfect ? "✅" : "⚠️" }}</span>
					<span>
						{{ __("Tồn kho khớp file Misa:") }}
						<strong>{{ inv.matches }}/{{ inv.total_lines || inv.total_items || inv.total }} {{ __("dòng") }} ({{ inv.accuracy_pct }}%)</strong>
					</span>
				</div>

				<table v-if="postedRows.length" class="result-table">
					<thead><tr><th>{{ __("Loại chứng từ") }}</th><th class="num">{{ __("Đã ghi sổ") }}</th></tr></thead>
					<tbody>
						<tr v-for="r in postedRows" :key="r.dt">
							<td>{{ r.label }}</td>
							<td class="num">{{ fmtN(r.n) }}</td>
						</tr>
					</tbody>
				</table>

				<div v-if="rc.Failed" class="result-row warn-row">
					<span class="result-ico">⚠️</span>
					<span>
						{{ __("{0} dòng lỗi chưa vào sổ").replace("{0}", fmtN(rc.Failed)) }} —
						<a :href="failedRowsUrl" target="_blank">{{ __("xem danh sách") }}</a>
					</span>
				</div>

				<details v-if="warnings.length" class="advanced">
					<summary>{{ __("Cảnh báo trong quá trình chạy") }} ({{ warnings.length }})</summary>
					<ul class="blocker-list">
						<li v-for="(w, i) in warnings" :key="i">{{ w.message }}</li>
					</ul>
				</details>

				<div class="actions">
					<a class="btn btn-primary" :href="tbReportUrl" target="_blank">📊 {{ __("Mở Bảng cân đối số phát sinh") }}</a>
					<a class="btn btn-default" :href="'/app/misa-migration-batch/' + encodeURIComponent(store.batch_name)" target="_blank">{{ __("Chi tiết đợt migration") }}</a>
					<button class="btn btn-default" @click="onNewRun">{{ __("Migration đợt mới") }}</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import { useMisaStore } from "./store.js";

const emit = defineEmits(["discard"]);
const store = useMisaStore();

function __(t) {
	return typeof window.__ === "function" ? window.__(t) : t;
}

// VN-friendly labels for file types (shown in the picked-files table)
const TYPE_LABELS = {
	"Unknown": "❓ Chưa nhận diện",
	"NKC": "Sổ nhật ký chung",
	"Bang ke BR": "Bảng kê bán ra",
	"Bang ke MV": "Bảng kê mua vào",
	"SCT": "Sổ chi tiết vật tư",
	"Account": "Hệ thống tài khoản",
	"Misa Default Account": "TK ngầm định",
	"Misa Closing Rule": "TK kết chuyển",
	"OB Account Balance": "Số dư tài khoản đầu kỳ",
	"OB Bank Balance": "Số dư ngân hàng đầu kỳ",
	"OB Customer AR": "Công nợ khách hàng",
	"OB Supplier AP": "Công nợ nhà cung cấp",
	"OB Employee Advance": "Công nợ nhân viên",
	"OB Inventory": "Tồn kho đầu kỳ",
	"OB Fixed Asset": "Tài sản cố định đầu kỳ",
	"OB CCDC": "Công cụ dụng cụ đầu kỳ",
	"OB Prepaid Expense": "Chi phí trả trước đầu kỳ",
	"Customer": "Khách hàng",
	"Customer Group": "Nhóm KH/NCC",
	"Supplier": "Nhà cung cấp",
	"Supplier Group": "Nhóm nhà cung cấp",
	"Employee": "Nhân viên",
	"Item": "Hàng hóa dịch vụ",
	"Item Group": "Nhóm vật tư hàng hóa",
	"UOM": "Đơn vị tính",
	"Bank": "Ngân hàng",
	"Bank Account": "Tài khoản ngân hàng",
	"Warehouse": "Kho",
	"Department": "Cơ cấu tổ chức",
	"Cost Center": "Đối tượng tập hợp chi phí",
	"Project": "Công trình",
	"Asset Category": "Loại tài sản cố định",
	"CCDC Category": "Loại công cụ dụng cụ",
	"Skip": "⏭ Bỏ qua (không import)",
};
const FILE_TYPE_OPTIONS = Object.keys(TYPE_LABELS);

const DT_LABELS = {
	"Sales Invoice": "Hóa đơn bán hàng",
	"Purchase Invoice": "Hóa đơn mua hàng",
	"Payment Entry": "Phiếu thu / chi",
	"Journal Entry": "Phiếu kế toán",
	"Stock Entry": "Phiếu kho",
	"Purchase Receipt": "Phiếu nhập mua",
};

function typeLabel(t) {
	return TYPE_LABELS[t] || t;
}

// ---------------------------------------------------------------- mode
// setup → uploading → (pipeline zones driven by store.pipeline/status)
const phase = ref("setup"); // local: setup | uploading | run
const mode = computed(() => {
	if (phase.value === "uploading") return "uploading";
	if (phase.value === "run" || store.pipeline || ["UPLOADED", "PARSED", "REVIEWED", "POSTING", "POSTED", "STUCK", "REVERSING", "REVERSED"].includes(store.status) && store.batch_name) {
		return "run";
	}
	return "setup";
});

// ---------------------------------------------------------------- setup zone
const form = reactive({ company: "", batch_title: "", ob_posting_date: "" });
const picked = reactive([]);
const dragOver = ref(false);
const error = ref(null);
const busy = ref(false);
const fileInput = ref(null);

const companyOptions = ref([]);
const companyLoading = ref(false);
const showCompanyDropdown = ref(false);
const companyValidated = ref(false);
let companyDebounce = null;

async function fetchCompanies(q) {
	companyLoading.value = true;
	try {
		const data = await new Promise((resolve) => {
			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Company",
					filters: q ? [["name", "like", `%${q}%`]] : [],
					fields: ["name", "default_currency"],
					order_by: "creation desc",
					limit_page_length: 15,
				},
				callback: (r) => resolve(r?.message || []),
				error: () => resolve([]),
			});
		});
		companyOptions.value = data;
		companyValidated.value = data.some((c) => c.name === form.company);
	} finally {
		companyLoading.value = false;
	}
}
function onCompanyFocus() {
	showCompanyDropdown.value = true;
	fetchCompanies(form.company);
}
function onCompanyType() {
	companyValidated.value = false;
	clearTimeout(companyDebounce);
	companyDebounce = setTimeout(() => fetchCompanies(form.company), 250);
}
function onCompanyBlur() {
	setTimeout(() => (showCompanyDropdown.value = false), 180);
}
function selectCompany(name) {
	form.company = name;
	companyValidated.value = true;
	showCompanyDropdown.value = false;
}

async function addFiles(fileList) {
	const files = Array.from(fileList || []).filter((f) => /\.(xlsx|xls)$/i.test(f.name));
	if (!files.length) return;
	let detected = {};
	try {
		detected = await store.detectFileTypes(files.map((f) => f.name));
	} catch (e) { /* fallback Unknown */ }
	for (const f of files) {
		if (picked.some((p) => p.file.name === f.name && p.file.size === f.size)) continue;
		// Files the pipeline has no importer for (biểu thuế, ký hiệu chấm
		// công…) default to "Bỏ qua" — operator chỉnh lại được, nhưng không
		// bị chặn nút Start vì những file ngoài phạm vi.
		const t = detected[f.name];
		picked.push({ file: f, file_type: !t || t === "Unknown" ? "Skip" : t });
	}
}
function onDrop(e) {
	dragOver.value = false;
	addFiles(e.dataTransfer.files);
}
function onFileInput(e) {
	addFiles(e.target.files);
}

const unknownCount = computed(() => picked.filter((p) => p.file_type === "Unknown").length);
const skipCount = computed(() => picked.filter((p) => p.file_type === "Skip").length);
const canStart = computed(() =>
	companyValidated.value && picked.length > 0 && !busy.value && unknownCount.value === 0
);

// ---------------------------------------------------------------- start
const uploadedCount = ref(0);
const currentUploadName = ref("");
const uploadPct = computed(() =>
	picked.length ? Math.round((uploadedCount.value / picked.length) * 100) : 0
);

async function onStart() {
	error.value = null;
	busy.value = true;
	try {
		await store.createBatch(
			form.company,
			form.batch_title || __("Migration Misa {0}").replace("{0}", frappe.datetime.now_date()),
			form.ob_posting_date || "",
			"",
		);
		phase.value = "uploading";
		uploadedCount.value = 0;
		for (const p of picked) {
			if (p.file_type === "Skip") {
				uploadedCount.value += 1;
				continue;
			}
			currentUploadName.value = p.file.name;
			await store.uploadFile(p.file, p.file_type);
			uploadedCount.value += 1;
		}
		await store.startAutoPipeline();
		phase.value = "run";
		startTimer();
	} catch (e) {
		error.value = (e && e.message) || String(e);
		phase.value = "setup";
	} finally {
		busy.value = false;
	}
}

// ---------------------------------------------------------------- run zone
const stages = computed(() => store.pipeline?.stages || []);
const activity = computed(() => store.pipeline?.activity || "");
const blockers = computed(() =>
	(store.pipeline?.blockers || []).filter((b) => b.level === "block")
);
const warnings = computed(() =>
	(store.pipeline?.blockers || []).filter((b) => b.level !== "block")
);
const pipelineError = computed(() => store.pipeline?.error || "");
const result = computed(() => store.pipeline?.result || null);
const rc = computed(() => store.row_counts || {});

const hasFailed = computed(() => stages.value.some((s) => s.status === "failed"));
// Worker died mid-run: a stage still says "running" but the server hasn't
// written progress for 3+ phút AND the batch is in a resumable status.
const isStale = computed(() =>
	stages.value.some((s) => s.status === "running") &&
	(store.seconds_since_update ?? 0) > 180 &&
	["UPLOADED", "PARSED", "REVIEWED"].includes(store.status)
);
const isBlocked = computed(() => stages.value.some((s) => s.status === "blocked"));
const isDone = computed(
	() => stages.value.length > 0 && stages.value.every((s) => s.status === "done") && !!result.value
);
const isRunning = computed(
	() => !isDone.value && !hasFailed.value && !isBlocked.value && (stages.value.some((s) => s.status === "running") || store.status === "POSTING")
);

const overallPct = computed(() => {
	const ss = stages.value;
	if (!ss.length) return 4;
	const done = ss.filter((s) => s.status === "done").length;
	const running = ss.some((s) => s.status === "running") ? 0.5 : 0;
	return Math.min(100, Math.round(((done + running) / ss.length) * 100));
});

const glBalanced = computed(() => !!result.value?.gl_balance?.balanced);
const tb = computed(() => {
	const t = result.value?.tb_compare;
	return t && !t.error ? t : null;
});
const tbPerfect = computed(() => tb.value && tb.value.mismatches === 0 && (tb.value.missing_in_db || 0) === 0);
const inv = computed(() => {
	const t = result.value?.inventory_compare;
	return t && !t.error ? t : null;
});
const invPerfect = computed(() => inv.value && (inv.value.mismatches || 0) === 0);

const postedRows = computed(() => {
	const by = result.value?.posted_by_doctype || {};
	return Object.entries(by)
		.filter(([, n]) => n > 0)
		.map(([dt, n]) => ({ dt, label: DT_LABELS[dt] || dt, n }));
});

const failedRowsUrl = computed(() =>
	`/app/misa-migration-row?batch=${encodeURIComponent(store.batch_name || "")}&status=Failed`
);
const tbReportUrl = computed(() =>
	`/app/query-report/Bang Can Doi So Phat Sinh?company=${encodeURIComponent(store.company || "")}`
);
const totalRowsLabel = computed(() =>
	__("{0} dòng dữ liệu").replace("{0}", fmtN(store.total_rows || 0))
);
const obDateLabel = computed(() => {
	if (!store.ob_posting_date) return "";
	try {
		return window.frappe?.datetime?.str_to_user(store.ob_posting_date) || store.ob_posting_date;
	} catch (e) {
		return store.ob_posting_date;
	}
});

async function onResume() {
	busy.value = true;
	try {
		await store.startAutoPipeline();
	} catch (e) {
		frappe.msgprint({ title: __("Không chạy tiếp được"), message: (e && e.message) || String(e), indicator: "red" });
	} finally {
		busy.value = false;
	}
}
async function onResumeStuck() {
	busy.value = true;
	try {
		await store.resumeAfterStuck();
	} catch (e) {
		frappe.msgprint({ title: __("Không chạy tiếp được"), message: (e && e.message) || String(e), indicator: "red" });
	} finally {
		busy.value = false;
	}
}
function onNewRun() {
	store.stopPipelinePoll();
	store.setBatch(null);
	store.pipeline = null;
	store.row_counts = {};
	picked.splice(0);
	phase.value = "setup";
}

// ---------------------------------------------------------------- timer
const elapsedLabel = ref("");
let timerHandle = null;
let t0 = null;
function startTimer() {
	t0 = Date.now();
	stopTimer();
	timerHandle = setInterval(() => {
		const s = Math.floor((Date.now() - t0) / 1000);
		const m = Math.floor(s / 60);
		elapsedLabel.value = m ? `${m} phút ${s % 60} giây` : `${s} giây`;
		if (isDone.value || hasFailed.value) stopTimer();
	}, 1000);
}
function stopTimer() {
	if (timerHandle) {
		clearInterval(timerHandle);
		timerHandle = null;
	}
}

// ---------------------------------------------------------------- utils
function formatBytes(b) {
	if (!b) return "";
	if (b > 1048576) return (b / 1048576).toFixed(1) + " MB";
	if (b > 1024) return Math.round(b / 1024) + " KB";
	return b + " B";
}
function fmtN(n) {
	return Number(n || 0).toLocaleString("vi-VN");
}
function fmtVnd(n) {
	return Number(n || 0).toLocaleString("vi-VN") + " ₫";
}

// ---------------------------------------------------------------- lifecycle
async function hydrateFromBatch() {
	if (!store.batch_name || store.status === "DRAFT") return;
	phase.value = "run";
	await store.fetchPipeline();
	const running = ["UPLOADED", "PARSED", "REVIEWED", "POSTING", "REVERSING"].includes(store.status);
	if (running || stages.value.some((s) => s.status === "running")) {
		store.startPipelinePoll();
		startTimer();
	}
}

// App.vue resolves the resumed batch AFTER this child mounts (parent
// onMounted fires last) — watch for it so the run view hydrates instead
// of rendering an empty card.
watch(() => store.batch_name, () => {
	if (!store.pipeline) hydrateFromBatch();
});

onMounted(async () => {
	await hydrateFromBatch();
	// Realtime push between polls
	if (window.frappe?.realtime) {
		frappe.realtime.on("misa_migration:pipeline", (data) => {
			if (data?.batch === store.batch_name && data.pipeline) {
				store.pipeline = data.pipeline;
			}
		});
	}
});
onBeforeUnmount(() => {
	stopTimer();
	store.stopPipelinePoll();
	if (window.frappe?.realtime) {
		frappe.realtime.off("misa_migration:pipeline");
	}
});
</script>

<style scoped>
.auto-flow { max-width: 980px; }
.card {
	background: var(--card-bg, #fff);
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 10px;
	padding: 20px;
}
.setup-grid { display: flex; gap: 16px; flex-wrap: wrap; }
.setup-grid .form-row { flex: 1 1 280px; }
.form-row { margin-bottom: 12px; display: flex; flex-direction: column; gap: 4px; }
.form-row label { font-weight: 600; font-size: 13px; }
.form-row input, .form-row select {
	border: 1px solid var(--border-color, #d1d5db);
	border-radius: 6px; padding: 7px 10px; font-size: 13px;
	background: var(--control-bg, #fff); color: var(--text-color, #333);
}
.reqd { color: var(--red-500, #dc2626); }
.hint { color: var(--text-muted, #888); font-size: 12px; }
.error-hint { color: var(--red-600, #dc2626); }
.warn-hint { color: var(--orange-600, #d97706); }
.error { color: var(--red-600, #dc2626); margin-top: 10px; font-size: 13px; }
.error-text { color: var(--red-600, #dc2626); }

.company-picker { position: relative; }
.company-picker input { width: 100%; }
.company-dropdown {
	position: absolute; top: 100%; left: 0; right: 0; z-index: 30;
	background: var(--card-bg, #fff); border: 1px solid var(--border-color, #d1d5db);
	border-radius: 6px; max-height: 240px; overflow: auto; box-shadow: 0 4px 10px rgba(0,0,0,.08);
}
.company-option { display: flex; justify-content: space-between; padding: 8px 10px; cursor: pointer; font-size: 13px; }
.company-option:hover { background: var(--bg-light-gray, #f3f4f6); }
.company-empty { position: absolute; top: 100%; left: 0; right: 0; z-index: 30; background: var(--card-bg, #fff); border: 1px solid var(--border-color, #d1d5db); border-radius: 6px; padding: 10px; font-size: 13px; }

.dropzone {
	border: 2px dashed var(--border-color, #cbd5e1);
	border-radius: 10px; padding: 30px; text-align: center; cursor: pointer;
	transition: border-color .15s, background .15s; margin: 8px 0 12px;
}
.dropzone.over, .dropzone:hover { border-color: var(--primary, #2563eb); background: var(--bg-light-gray, #f8fafc); }
.dz-icon { font-size: 30px; }
.dz-title { font-weight: 600; margin: 6px 0 2px; }

.file-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.file-table th { text-align: left; color: var(--text-muted, #888); font-weight: 600; padding: 6px 8px; border-bottom: 1px solid var(--border-color, #e5e7eb); }
.file-table td { padding: 5px 8px; border-bottom: 1px solid var(--border-color, #f1f5f9); }
.file-table .fname { max-width: 380px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.file-table select.unknown { border-color: var(--orange-500, #f59e0b); background: var(--orange-50, #fffbeb); }
.file-table .num, .result-table .num { text-align: right; }

.advanced { margin: 10px 0; }
.advanced summary { cursor: pointer; font-size: 13px; color: var(--text-muted, #888); }

.start-bar { display: flex; align-items: center; gap: 14px; margin-top: 14px; flex-wrap: wrap; }
.start-btn { font-size: 15px; padding: 10px 22px; }

.progress-card h3 { margin: 0 0 6px; }
.run-header { display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }
.elapsed { font-size: 13px; color: var(--text-muted, #888); white-space: nowrap; }
.bar { height: 8px; border-radius: 6px; background: var(--gray-200, #e5e7eb); overflow: hidden; margin: 12px 0; }
.bar.big { height: 12px; }
.bar-fill { height: 100%; background: var(--primary, #2563eb); border-radius: 6px; transition: width .5s ease; }
.bar-fill.danger { background: var(--red-500, #dc2626); }
.bar-fill.warn { background: var(--orange-500, #f59e0b); }

.stage-list { list-style: none; margin: 8px 0 4px; padding: 0; }
.stage { display: flex; align-items: baseline; gap: 10px; padding: 7px 4px; font-size: 14px; }
.stage.pending { opacity: .45; }
.stage.running .stage-label { font-weight: 700; }
.stage-ico { width: 22px; text-align: center; flex: 0 0 22px; }
.stage-detail { font-size: 12.5px; }

.spinner {
	display: inline-block; width: 14px; height: 14px;
	border: 2px solid var(--gray-300, #d1d5db); border-top-color: var(--primary, #2563eb);
	border-radius: 50%; animation: spin .8s linear infinite; vertical-align: -2px;
}
.spinner.small { width: 11px; height: 11px; }
@keyframes spin { to { transform: rotate(360deg); } }

.activity { font-size: 13px; color: var(--text-color, #374151); margin: 6px 0; }
.live-chips { display: flex; gap: 8px; flex-wrap: wrap; margin: 6px 0; }
.chip {
	font-size: 12px; padding: 2px 10px; border-radius: 999px;
	background: var(--gray-100, #f3f4f6); color: var(--text-color, #374151);
}
.chip.ok { background: var(--green-50, #ecfdf5); color: var(--green-700, #047857); }
.chip.bad { background: var(--red-50, #fef2f2); color: var(--red-700, #b91c1c); }
.chip.warnc { background: var(--orange-50, #fffbeb); color: var(--orange-700, #b45309); }
.bg-hint { margin-top: 8px; }

.blocker-panel { border-top: 1px solid var(--border-color, #e5e7eb); margin-top: 14px; padding-top: 12px; }
.blocker-panel h4 { margin: 0 0 6px; }
.blocker-list { list-style: none; padding: 0; margin: 8px 0; max-height: 300px; overflow: auto; }
.blocker-list li { font-size: 13px; padding: 4px 0; display: flex; gap: 8px; align-items: baseline; }

.result-panel { border-top: 1px solid var(--border-color, #e5e7eb); margin-top: 14px; padding-top: 12px; }
.result-panel h4 { margin: 0 0 10px; }
.result-row { display: flex; gap: 8px; align-items: baseline; padding: 5px 0; font-size: 14px; }
.result-row.good { color: var(--green-700, #047857); }
.result-row.bad-row { color: var(--red-700, #b91c1c); font-weight: 600; }
.result-row.warn-row { color: var(--orange-700, #b45309); }
.result-table { border-collapse: collapse; font-size: 13px; margin: 10px 0; min-width: 320px; }
.result-table th, .result-table td { padding: 5px 12px; border-bottom: 1px solid var(--border-color, #f1f5f9); text-align: left; }
.actions { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.muted { color: var(--text-muted, #888); }
</style>
