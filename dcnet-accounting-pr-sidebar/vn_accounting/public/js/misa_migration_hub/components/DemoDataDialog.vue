<template>
	<div v-if="open" class="demo-dialog-overlay" @click.self="$emit('close')">
		<div class="demo-dialog">
			<header>
				<h3>{{ __("Phát hiện dữ liệu mẫu (dcnet_sample)") }}</h3>
				<button class="close" @click="$emit('close')">×</button>
			</header>

			<div class="body">
				<div v-if="data" class="summary">
					<p>
						{{ __("Site này đang có dữ liệu mẫu cho company") }}
						<strong>{{ data.company }}</strong>:
						<strong>{{ data.total.toLocaleString() }}</strong>
						{{ __("bản ghi") }}.
					</p>
					<details class="counts-detail">
						<summary>{{ __("Chi tiết theo DocType") }}</summary>
						<table>
							<tr v-for="(n, dt) in data.counts" :key="dt">
								<td>{{ dt }}</td>
								<td class="num">{{ n.toLocaleString() }}</td>
							</tr>
						</table>
					</details>
				</div>

				<p class="muted">
					{{ __("Trước khi import Misa, chọn 1 trong 3 phương án:") }}
				</p>

				<div class="options">
					<label
						v-for="opt in OPTIONS"
						:key="opt.key"
						:class="['option', { active: choice === opt.key }]"
					>
						<input
							type="radio"
							name="demo-choice"
							:value="opt.key"
							v-model="choice"
						/>
						<div class="opt-text">
							<div class="opt-title">
								{{ opt.title }}
								<span v-if="opt.recommended" class="rec-badge">
									{{ __("Khuyến nghị") }}
								</span>
							</div>
							<div class="opt-desc">{{ opt.desc }}</div>
						</div>
					</label>
				</div>

				<div v-if="error" class="error">{{ error }}</div>
				<div v-if="message" class="success">{{ message }}</div>

				<div v-if="choice === 'wipe' && !wiped" class="warn-banner">
					⚠ {{ __("Sẽ xóa") }}
					<strong>{{ data?.total?.toLocaleString() || "?" }}</strong>
					{{ __("bản ghi demo. Thao tác không thể hoàn tác. Gõ chuỗi xác nhận:") }}
					<input
						type="text"
						v-model="confirmInput"
						placeholder="WIPE-DEMO-DATA"
						class="confirm-input"
					/>
				</div>
			</div>

			<footer>
				<button class="btn btn-link" :disabled="busy" @click="$emit('close')">
					{{ __("Hủy") }}
				</button>
				<button
					v-if="choice === 'wipe' && !wiped"
					class="btn btn-danger"
					:disabled="busy || confirmInput !== 'WIPE-DEMO-DATA'"
					@click="onWipe"
				>
					{{ busy ? __("Đang xóa...") : __("Xóa dữ liệu mẫu") }}
				</button>
				<button
					v-else-if="choice === 'coexist'"
					class="btn btn-primary"
					@click="onContinue"
				>
					{{ __("Giữ demo, tiếp tục import (rủi ro tên trùng)") }}
				</button>
				<button
					v-else-if="choice === 'new-company'"
					class="btn btn-primary"
					@click="onContinue"
				>
					{{ __("Đã hiểu — sẽ tạo Company mới") }}
				</button>
				<button
					v-else-if="wiped"
					class="btn btn-primary"
					@click="$emit('proceed')"
				>
					{{ __("Tiếp tục Review →") }}
				</button>
			</footer>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { useMisaStore } from "../store.js";

function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

const props = defineProps({
	open: { type: Boolean, default: false },
	data: { type: Object, default: null },
});
const emit = defineEmits(["close", "proceed"]);

const store = useMisaStore();
const choice = ref("wipe");
const confirmInput = ref("");
const busy = ref(false);
const error = ref(null);
const message = ref(null);
const wiped = ref(false);

const OPTIONS = [
	{
		key: "wipe",
		recommended: true,
		title: __("Xóa demo, import Misa thay thế"),
		desc: __("Gọi dcnet_sample.setup.teardown_all xóa toàn bộ dữ liệu mẫu (~30-120s). Phương án sạch nhất — dữ liệu Misa sẽ không bị trùng tên với demo."),
	},
	{
		key: "coexist",
		title: __("Giữ demo + Misa cùng tồn tại"),
		desc: __("Rủi ro: Customer/Supplier có thể trùng Mã (ví dụ VIETTEL). Phù hợp khi chỉ test pipeline trên 1 voucher."),
	},
	{
		key: "new-company",
		title: __("Tạo Company mới"),
		desc: __("Bạn cần tự tạo Company mới (ví dụ DCNET REAL) trước, set làm default, rồi quay lại đây import vào company đó."),
	},
];

async function onWipe() {
	error.value = null;
	message.value = null;
	busy.value = true;
	try {
		const r = await store.wipeDemoData();
		wiped.value = true;
		message.value = r.message || __("Đã xóa dữ liệu mẫu.");
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}

function onContinue() {
	emit("proceed");
}
</script>

<style scoped>
.demo-dialog-overlay {
	position: fixed; inset: 0;
	background: rgba(0,0,0,0.45);
	display: flex; align-items: center; justify-content: center;
	z-index: 999;
}
.demo-dialog {
	background: white;
	border-radius: 10px;
	width: min(640px, 92vw);
	max-height: 88vh;
	display: flex; flex-direction: column;
	box-shadow: 0 24px 60px rgba(0,0,0,0.2);
	overflow: hidden;
}
header {
	padding: 14px 18px;
	border-bottom: 1px solid #e5e7eb;
	display: flex; justify-content: space-between; align-items: center;
	background: #fff7ed;
}
header h3 { margin: 0; font-size: 16px; color: #92400e; }
.close { background: none; border: none; font-size: 26px; line-height: 1; cursor: pointer; color: #6b7280; }
.body { padding: 16px 18px; overflow-y: auto; flex: 1; font-size: 13px; }
.summary p { margin: 0 0 8px; }
.counts-detail { margin: 8px 0 14px; }
.counts-detail summary { cursor: pointer; color: #6b7280; font-size: 12px; }
.counts-detail table { width: 100%; margin-top: 6px; font-size: 12px; }
.counts-detail td { padding: 2px 6px; border-bottom: 1px solid #f3f4f6; }
.counts-detail td.num { text-align: right; font-variant-numeric: tabular-nums; }
.muted { color: #6b7280; font-size: 12px; margin: 12px 0 8px; }
.options {
	display: flex; flex-direction: column; gap: 8px;
	margin: 6px 0 16px;
}
.option {
	display: flex; gap: 10px; align-items: flex-start;
	padding: 10px 12px;
	border: 1px solid #e5e7eb;
	border-radius: 6px;
	cursor: pointer;
}
.option:hover { background: #f9fafb; }
.option.active { background: #eff6ff; border-color: #2563eb; }
.option input[type=radio] { margin-top: 3px; }
.opt-text { flex: 1; }
.opt-title { font-weight: 500; }
.opt-desc { color: #6b7280; font-size: 12px; margin-top: 3px; }
.rec-badge {
	background: #10b981; color: white;
	font-size: 10px; padding: 2px 6px; border-radius: 4px;
	margin-left: 6px;
	text-transform: uppercase;
	font-weight: 600;
}
.warn-banner {
	padding: 10px 12px;
	background: #fef2f2; color: #991b1b;
	border-radius: 6px;
	font-size: 12px;
	margin-bottom: 8px;
}
.confirm-input {
	margin-top: 6px; padding: 4px 8px;
	font-family: ui-monospace, "SF Mono", monospace;
	border: 1px solid #fecaca;
	border-radius: 4px;
	width: 200px;
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
.btn-danger { background: #dc2626; color: white; }
.btn-link { background: transparent; color: #6b7280; }
</style>
