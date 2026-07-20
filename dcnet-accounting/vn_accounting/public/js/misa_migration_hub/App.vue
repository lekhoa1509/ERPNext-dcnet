<template>
	<div class="misa-hub">
		<header class="misa-hub-header">
			<div class="misa-hub-header-text">
				<h2>{{ __("Chuyển số liệu từ Misa SME") }}</h2>
				<p class="muted">
					{{ __("Chọn công ty, thả toàn bộ file Excel xuất từ Misa, bấm một nút — hệ thống tự chạy đến khi ra bảng cân đối.") }}
					<span v-if="store.batch_name" class="batch-chip">
						· {{ store.batch_title || store.batch_name }}
					</span>
				</p>
			</div>
			<div class="header-actions">
				<button
					v-if="store.canDiscard"
					class="btn btn-default btn-sm"
					:disabled="store.loading"
					:title="__('Xóa đợt hiện tại (chưa tạo chứng từ nào) và bắt đầu lại')"
					@click="discardCurrent"
				>
					{{ __("Bỏ đợt này / Bắt đầu lại") }}
				</button>
			</div>
		</header>

		<AutoFlow @discard="discardCurrent" />
	</div>
</template>

<script setup>
import { onMounted } from "vue";
import { useMisaStore } from "./store.js";
import AutoFlow from "./AutoFlow.vue";

defineProps({
	page: { type: Object, required: true },
});

function __(text) {
	return typeof window.__ === "function" ? window.__(text) : text;
}

const store = useMisaStore();

// Escape hatch: abandon a never-posted batch so the operator isn't stuck
// with an old/parked batch. Server re-validates nothing was posted.
async function discardCurrent() {
	const label = store.batch_title || store.batch_name;
	const ok = await new Promise((resolve) => {
		frappe.confirm(
			__("Bỏ đợt \"{0}\"? Dữ liệu đã phân tích của đợt này sẽ bị xóa (chưa có chứng từ nào được tạo vào ERPNext). Không thể hoàn tác.").replace("{0}", label),
			() => resolve(true),
			() => resolve(false),
		);
	});
	if (!ok) return;
	try {
		await store.discardBatch();
		store.pipeline = null;
		store.row_counts = {};
		frappe.show_alert({ message: __("Đã bỏ. Có thể bắt đầu đợt mới."), indicator: "green" });
	} catch (e) {
		frappe.msgprint({
			title: __("Không bỏ được"),
			message: (e && e.message) || String(e),
			indicator: "red",
		});
	}
}

// Resume the last in-flight batch (localStorage → server discovery).
onMounted(async () => {
	if (!store.batch_name) {
		await store.resumeFromStorage();
	}
});
</script>

<style scoped>
.misa-hub {
	padding: 16px;
	max-width: 1100px;
	margin: 0 auto;
}

.misa-hub-header {
	margin-bottom: 16px;
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	gap: 16px;
}

.misa-hub-header-text {
	min-width: 0;
}

.batch-chip {
	color: var(--text-muted, #888);
}

.header-actions {
	flex: 0 0 auto;
	display: flex;
	gap: 8px;
}

.misa-hub-header h2 {
	margin: 0 0 4px;
	font-size: 22px;
}

.misa-hub-header .muted {
	color: var(--text-muted, #888);
	margin: 0;
	font-size: 13px;
}
</style>
