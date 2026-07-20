<template>
	<div class="misa-hub">
		<header class="misa-hub-header">
			<h2>{{ __("Migration từ Misa SME") }}</h2>
			<p class="muted">{{ __("Quy trình 4 bước: Upload → Phân tích → Duyệt → Tạo") }}</p>
		</header>

		<nav class="misa-stepper">
			<div
				v-for="(s, idx) in steps"
				:key="s.key"
				class="misa-step"
				:class="{ active: idx === activeIdx, done: idx < activeIdx }"
			>
				<div class="misa-step-num">{{ idx + 1 }}</div>
				<div class="misa-step-label">{{ s.label }}</div>
			</div>
		</nav>

		<ResumeBanner />

		<section class="misa-step-body">
			<component :is="stepComponents[activeIdx]" />
		</section>
	</div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, watch } from "vue";
import { useMisaStore } from "./store.js";
import UploadStep from "./steps/UploadStep.vue";
import ParseStep from "./steps/ParseStep.vue";
import ReviewStep from "./steps/ReviewStep.vue";
import PostStep from "./steps/PostStep.vue";
import ResumeBanner from "./components/ResumeBanner.vue";

defineProps({
	page: { type: Object, required: true },
});

const stepComponents = [UploadStep, ParseStep, ReviewStep, PostStep];

// Translator shim — Frappe's __() is global on desk pages, but Vue scope
// may not pick it up via SetVueGlobals on older Frappe. Bind locally.
function __(text) {
	return typeof window.__ === "function" ? window.__(text) : text;
}

const steps = [
	{ key: "upload", label: __("1. Upload file") },
	{ key: "parse", label: __("2. Phân tích") },
	{ key: "review", label: __("3. Duyệt") },
	{ key: "post", label: __("4. Tạo vào ERPNext") },
];

const store = useMisaStore();
const activeIdx = computed(() => store.activeStepIdx);

// UX Gap 1: on mount, try to resume the last in-flight batch from
// localStorage; falls back to server-side find_active_batch when
// localStorage is empty (cleared, different browser, incognito).
onMounted(async () => {
	if (!store.batch_name) {
		await store.resumeFromStorage();
	}
	// Start the progress poller if the batch is in-flight. The poller
	// auto-stops on terminal state (POSTED / REVERSED).
	if (store.status && ["POSTING", "REVERSING"].includes(store.status)) {
		store.startProgressPoll();
	}
});

// Auto-start poller whenever status flips into an in-flight state
// (e.g., after user clicks Tạo vào ERPNext from PostStep).
watch(() => store.status, (newStatus) => {
	if (["POSTING", "REVERSING"].includes(newStatus)) {
		store.startProgressPoll();
	} else if (["POSTED", "REVERSED"].includes(newStatus)) {
		store.stopProgressPoll();
	}
});

onBeforeUnmount(() => {
	store.stopProgressPoll();
});
</script>

<style scoped>
.misa-hub {
	padding: 16px;
	max-width: 1100px;
	margin: 0 auto;
}

.misa-hub-header {
	margin-bottom: 20px;
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

.misa-stepper {
	display: flex;
	gap: 8px;
	margin-bottom: 24px;
	border-bottom: 1px solid var(--border-color, #e5e7eb);
	padding-bottom: 12px;
}

.misa-step {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 6px 12px;
	border-radius: 6px;
	opacity: 0.5;
	transition: opacity 120ms;
}

.misa-step.active {
	opacity: 1;
	background: var(--bg-light-gray, #f3f4f6);
	font-weight: 600;
}

.misa-step.done {
	opacity: 0.85;
}

.misa-step-num {
	width: 24px;
	height: 24px;
	border-radius: 50%;
	background: var(--gray-200, #e5e7eb);
	color: var(--text-color, #333);
	display: inline-flex;
	align-items: center;
	justify-content: center;
	font-size: 12px;
	font-weight: 600;
}

.misa-step.active .misa-step-num {
	background: var(--primary, #2563eb);
	color: white;
}

.misa-step-label {
	font-size: 13px;
}

.misa-step-body {
	min-height: 200px;
}

.misa-placeholder {
	border: 1px dashed var(--border-color, #d1d5db);
	border-radius: 8px;
	padding: 32px;
	text-align: center;
	color: var(--text-muted, #888);
}
</style>
