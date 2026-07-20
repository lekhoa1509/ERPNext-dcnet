<template>
	<div v-if="store.status === 'STUCK'" class="resume-banner">
		<div class="resume-row">
			<div class="resume-icon">⚠</div>
			<div class="resume-text">
				<strong>{{ __("Batch đang ở trạng thái STUCK") }}</strong>
				<div class="reason" v-if="lastStuckLine">
					{{ lastStuckLine }}
				</div>
				<div class="muted">
					{{ __("Worker bị kill hoặc watchdog đánh dấu treo. Handlers idempotent — nhấn Tiếp tục để chạy lại từ chỗ dở dang.") }}
				</div>
			</div>
			<button
				class="btn btn-warning"
				:disabled="busy"
				@click="onResume"
			>
				{{ busy ? __("Đang tiếp tục...") : __("Tiếp tục Post") }}
			</button>
		</div>
		<div v-if="error" class="resume-error">{{ error }}</div>
	</div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useMisaStore } from "../store.js";

function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

const store = useMisaStore();
const busy = ref(false);
const error = ref(null);

// state.transition appends "[ts] current → STUCK (reason)" lines to
// batch.notes. Show the most recent STUCK line in the banner.
const lastStuckLine = computed(() => {
	const notes = store.notes || "";
	const lines = notes.split("\n").reverse();
	return lines.find(l => l.includes("→ STUCK")) || null;
});

async function onResume() {
	const userOK = await new Promise(resolve => {
		frappe.confirm(
			__("Tiếp tục đăng từ chỗ dở? Hệ thống sẽ bỏ qua các chứng từ đã tạo thành công lần trước."),
			() => resolve(true), () => resolve(false),
		);
	});
	if (!userOK) return;
	busy.value = true;
	error.value = null;
	try {
		await store.resumePost(false);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}
</script>

<style scoped>
.resume-banner {
	padding: 12px 16px;
	background: #fef2f2; color: #7f1d1d;
	border: 1px solid #fca5a5;
	border-radius: 6px;
	margin: 8px 0 12px;
	font-size: 13px;
}
.resume-row { display: flex; align-items: center; gap: 12px; }
.resume-error {
	margin-top: 10px; padding: 8px 12px;
	background: white; color: #991b1b;
	border: 1px solid #fca5a5; border-radius: 4px;
	font-size: 12px;
}
.resume-icon { font-size: 22px; }
.resume-text { flex: 1; }
.resume-text strong { display: block; margin-bottom: 2px; }
.reason {
	font-family: ui-monospace, "SF Mono", monospace;
	font-size: 11px;
	color: #991b1b;
	margin: 2px 0;
}
.muted { color: #b91c1c; font-size: 12px; }
.btn-warning {
	background: #dc2626; color: white; border: none;
	padding: 6px 14px; border-radius: 4px;
	cursor: pointer; font-size: 13px;
}
.btn-warning:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-warning:hover:not(:disabled) { background: #b91c1c; }
</style>
