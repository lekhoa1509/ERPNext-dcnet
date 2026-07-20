<template>
	<div v-if="open" class="failed-modal-overlay" @click.self="$emit('close')">
		<div class="failed-modal">
			<header>
				<h3>{{ __("Các dòng Failed") }}</h3>
				<button class="close" @click="$emit('close')">×</button>
			</header>

			<div class="body">
				<LoadingSkeleton v-if="loading" :count="5" :cols="4" />

				<EmptyState
					v-else-if="data?.total === 0"
					icon="✓"
					:title="__('Không còn dòng Failed nào')"
					:hint="__('Tất cả đã được retry hoặc resolved.')"
				/>

				<template v-else-if="data">
					<div class="summary">
						<strong>{{ data.total }}</strong>
						{{ __("dòng Failed") }}
						<span v-if="data.rows.length < data.total" class="muted">
							({{ __("hiển thị") }} {{ data.rows.length }})
						</span>
					</div>

					<table class="failed-table">
						<thead>
							<tr>
								<th>{{ __("File type") }}</th>
								<th class="num">{{ __("Row #") }}</th>
								<th>{{ __("Target") }}</th>
								<th>{{ __("Lỗi") }}</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="row in data.rows" :key="row.name">
								<td>{{ row.file_type }}</td>
								<td class="num">{{ row.row_index }}</td>
								<td>{{ row.target_doctype || '—' }}</td>
								<td class="err-cell" :title="row.error_message">
									{{ truncate(row.error_message) }}
								</td>
							</tr>
						</tbody>
					</table>
				</template>

				<div v-if="error" class="error">{{ error }}</div>
				<div v-if="message" class="success">{{ message }}</div>
			</div>

			<footer>
				<button class="btn btn-link" :disabled="busy" @click="$emit('close')">
					{{ __("Đóng") }}
				</button>
				<button
					v-if="data?.total > 0"
					class="btn btn-primary"
					:disabled="busy"
					@click="onRetryAll"
				>
					{{ busy ? __("Đang retry...") : __(`Retry tất cả ${data.total} dòng`) }}
				</button>
			</footer>
		</div>
	</div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useMisaStore } from "../store.js";
import LoadingSkeleton from "./LoadingSkeleton.vue";
import EmptyState from "./EmptyState.vue";

function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

const props = defineProps({
	open: { type: Boolean, default: false },
});
const emit = defineEmits(["close", "retried"]);

const store = useMisaStore();
const data = ref(null);
const loading = ref(false);
const busy = ref(false);
const error = ref(null);
const message = ref(null);

watch(() => props.open, async (v) => {
	if (v) await load();
});

async function load() {
	loading.value = true; error.value = null; message.value = null;
	try { data.value = await store.getFailedRows(100); }
	catch (e) { error.value = e.message || String(e); }
	finally { loading.value = false; }
}

async function onRetryAll() {
	if (!confirm(__(`Retry ${data.value.total} dòng Failed? Batch sẽ chuyển về REVIEWED và re-post.`))) {
		return;
	}
	busy.value = true; error.value = null; message.value = null;
	try {
		const r = await store.retryFailed(false);
		message.value = __(`Đã enqueue retry cho ${r.retried_count || data.value.total} dòng. Batch đang post lại.`);
		emit("retried", r);
		setTimeout(load, 1500);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}

function truncate(s, n = 80) {
	if (!s) return "";
	return s.length > n ? s.slice(0, n) + "…" : s;
}
</script>

<style scoped>
.failed-modal-overlay {
	position: fixed; inset: 0;
	background: rgba(0,0,0,0.45);
	display: flex; align-items: center; justify-content: center;
	z-index: 999;
}
.failed-modal {
	background: white;
	border-radius: 10px;
	width: min(880px, 94vw);
	max-height: 86vh;
	display: flex; flex-direction: column;
	box-shadow: 0 24px 60px rgba(0,0,0,0.2);
	overflow: hidden;
}
header {
	padding: 14px 18px;
	border-bottom: 1px solid #e5e7eb;
	display: flex; justify-content: space-between; align-items: center;
	background: #fef2f2;
}
header h3 { margin: 0; font-size: 16px; color: #991b1b; }
.close { background: none; border: none; font-size: 26px; line-height: 1; cursor: pointer; color: #6b7280; }
.body { padding: 14px 18px; overflow-y: auto; flex: 1; }
.loading, .empty { padding: 24px; text-align: center; color: #6b7280; }
.summary { margin-bottom: 10px; font-size: 13px; }
.summary .muted { color: #6b7280; margin-left: 6px; }
.failed-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.failed-table th, .failed-table td {
	padding: 6px 8px; border-bottom: 1px solid #f3f4f6;
	text-align: left; vertical-align: top;
}
.failed-table th { background: #fef2f2; color: #7f1d1d; font-weight: 500; }
.failed-table .num { text-align: right; font-variant-numeric: tabular-nums; }
.err-cell {
	color: #991b1b;
	font-family: ui-monospace, "SF Mono", monospace;
	font-size: 11px;
	max-width: 380px;
	word-break: break-all;
}
.error {
	padding: 8px 12px; background: #fef2f2; color: #991b1b;
	border-radius: 4px; font-size: 12px; margin: 8px 0;
}
.success {
	padding: 8px 12px; background: #ecfdf5; color: #065f46;
	border-radius: 4px; font-size: 12px; margin: 8px 0;
}
footer {
	padding: 12px 18px;
	border-top: 1px solid #e5e7eb;
	display: flex; justify-content: flex-end; gap: 10px;
}
.btn { padding: 6px 14px; border-radius: 4px; cursor: pointer; border: none; font-size: 13px; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary { background: #2563eb; color: white; }
.btn-link { background: transparent; color: #6b7280; }
</style>
