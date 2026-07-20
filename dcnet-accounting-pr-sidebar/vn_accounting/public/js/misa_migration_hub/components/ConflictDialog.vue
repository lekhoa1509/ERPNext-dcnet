<template>
	<div v-if="open" class="dialog-backdrop" @click.self="onCancel">
		<div class="dialog">
			<header>
				<h3>{{ __("Xử lý xung đột") }}</h3>
				<button class="close-btn" @click="onCancel">×</button>
			</header>

			<div class="body">
				<div v-if="row" class="row-info">
					<div class="row-info-label">{{ __("File:") }}</div>
					<div>{{ row.file_type }} · {{ __("dòng") }} {{ row.row_index }}</div>
					<div class="row-info-label">{{ __("Lỗi:") }}</div>
					<div class="error-msg">{{ row.error_message || __("(không có thông tin)") }}</div>
					<div v-if="row.target_name" class="row-info-label">
						{{ __("ERPNext hiện có:") }}
					</div>
					<div v-if="row.target_name">{{ row.target_doctype }} / <code>{{ row.target_name }}</code></div>
				</div>

				<div class="actions">
					<label class="action-option">
						<input type="radio" v-model="action" value="skip" />
						<div>
							<strong>{{ __("Bỏ qua dòng này") }}</strong>
							<p class="muted">{{ __("Status → Skipped. Không tạo ERPNext doc, không sửa existing.") }}</p>
						</div>
					</label>

					<label class="action-option" :class="{ disabled: !row?.target_name }">
						<input type="radio" v-model="action" value="use_existing" :disabled="!row?.target_name" />
						<div>
							<strong>{{ __("Dùng existing ERPNext") }}</strong>
							<p class="muted">{{ __("Status → Exists. Mapping Misa→ERPNext giữ nguyên record hiện có.") }}</p>
						</div>
					</label>

					<label class="action-option">
						<input type="radio" v-model="action" value="rename" />
						<div>
							<strong>{{ __("Tạo mới với hậu tố") }}</strong>
							<p class="muted">{{ __("Status → Ready. Mã Misa sẽ được nối thêm hậu tố để không trùng.") }}</p>
							<input
								v-if="action === 'rename'"
								v-model="suffix"
								class="suffix-input"
								type="text"
								placeholder="-MIGRATED"
							/>
						</div>
					</label>

					<label class="action-option">
						<input type="radio" v-model="action" value="overwrite" />
						<div>
							<strong>{{ __("Ghi đè existing (cẩn thận)") }}</strong>
							<p class="muted">{{ __("Phase B v1: tương đương Rename. True overwrite sẽ ship ở Phase E.") }}</p>
						</div>
					</label>
				</div>

				<div v-if="error" class="error">{{ error }}</div>
			</div>

			<footer>
				<button class="btn btn-link" @click="onCancel">{{ __("Hủy") }}</button>
				<button class="btn btn-primary" :disabled="!action || busy" @click="onConfirm">
					{{ busy ? __("Đang xử lý...") : __("Xác nhận") }}
				</button>
			</footer>
		</div>
	</div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useMisaStore } from "../store.js";

const props = defineProps({
	open: { type: Boolean, default: false },
	row: { type: Object, default: null },
});
const emit = defineEmits(["close", "resolved"]);

const store = useMisaStore();
const action = ref("");
const suffix = ref("-MIGRATED");
const busy = ref(false);
const error = ref(null);

function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

watch(() => props.open, (v) => {
	if (v) {
		action.value = "";
		suffix.value = "-MIGRATED";
		error.value = null;
		busy.value = false;
	}
});

function onCancel() {
	emit("close");
}

async function onConfirm() {
	if (!props.row || !action.value) return;
	error.value = null;
	busy.value = true;
	try {
		const sfx = action.value === "rename" ? (suffix.value || "-MIGRATED") : null;
		const result = await store.resolveRow(props.row.name, action.value, sfx);
		emit("resolved", { row: props.row.name, new_status: result.new_status });
		emit("close");
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}
</script>

<style scoped>
.dialog-backdrop {
	position: fixed;
	inset: 0;
	background: rgba(0, 0, 0, 0.4);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 9999;
}
.dialog {
	background: white;
	border-radius: 10px;
	width: 520px;
	max-width: 92vw;
	max-height: 88vh;
	overflow: auto;
	box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}
.dialog header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 14px 18px;
	border-bottom: 1px solid var(--border-color, #e5e7eb);
}
.dialog header h3 { margin: 0; font-size: 16px; }
.close-btn {
	background: none;
	border: none;
	font-size: 24px;
	cursor: pointer;
	color: var(--text-muted, #888);
	line-height: 1;
}
.body { padding: 16px 18px; }
.row-info {
	display: grid;
	grid-template-columns: 110px 1fr;
	gap: 6px 12px;
	padding: 10px;
	background: var(--bg-light-gray, #f9fafb);
	border-radius: 6px;
	font-size: 13px;
	margin-bottom: 14px;
}
.row-info-label { color: var(--text-muted, #888); }
.error-msg { color: #991b1b; }
.actions { display: flex; flex-direction: column; gap: 8px; }
.action-option {
	display: flex;
	gap: 10px;
	padding: 10px 12px;
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 6px;
	cursor: pointer;
}
.action-option:hover { background: var(--bg-light-gray, #f9fafb); }
.action-option.disabled { opacity: 0.5; cursor: not-allowed; }
.action-option p {
	margin: 2px 0 0;
	color: var(--text-muted, #888);
	font-size: 12px;
}
.suffix-input {
	margin-top: 6px;
	padding: 4px 8px;
	border: 1px solid var(--border-color, #d1d5db);
	border-radius: 4px;
	font-size: 13px;
	width: 200px;
}
.error {
	margin-top: 12px;
	padding: 8px 12px;
	background: #fef2f2;
	color: #991b1b;
	border-radius: 4px;
	font-size: 13px;
}
.dialog footer {
	display: flex;
	justify-content: flex-end;
	gap: 8px;
	padding: 12px 18px;
	border-top: 1px solid var(--border-color, #e5e7eb);
}
</style>
