<template>
	<div class="post-step">
		<div class="card">
			<div class="header-row">
				<div>
					<h3>{{ __("Tạo vào ERPNext") }}</h3>
					<p class="muted">{{ __("Tạo các DocType ERPNext từ các dòng Ready. Sau khi tạo có thể Undo.") }}</p>
				</div>
				<div>
					<span class="status-badge" :class="store.status.toLowerCase()">{{ store.status }}</span>
				</div>
			</div>

			<div v-if="error" class="error">{{ error }}</div>

			<!-- Algorithm explainer: how the post pipeline handles 100k+ rows with FK dependencies -->
			<details class="post-explainer" :open="['REVIEWED', 'POSTING'].includes(store.status)">
				<summary>
					{{ __("⚙️ Bước này làm gì? Kỹ thuật & thuật toán xử lý big data — bấm để xem") }}
				</summary>
				<div class="post-explainer-body">
					<p>
						{{ __("Tạo = biến mỗi Misa Migration Row đã sẵn sàng thành 1 doc ERPNext thực (Customer, Item, Sales Invoice, Payment Entry...) và đẩy vào sổ cái (GL Entry). Với 100k+ dòng + phụ thuộc phức tạp (PE phải tham chiếu SI đã submit, SI phải có Item đã tồn tại, Item phải có UOM/Item Group...) hệ thống dùng các kỹ thuật sau để đảm bảo vừa đúng vừa nhanh:") }}
					</p>
					<div class="post-explainer-tasks">
						<div class="task-item">
							<strong>🔢 1. Phase ordering — chia dependency-DAG thành 6 phase tuần tự</strong>
							<p>{{ __("Phase 1 (UOM, Bank, Department, Item Group, Cost Center, Project...) → Phase 2 (Chart of Accounts) → Phase 3 (Customer, Supplier, Item, Employee, Bank Account) → Phase 0 (Opening Balance) → Phase 4a (NKC + Bảng kê + SCT insert as docstatus=0) → Phase 4b (submit SE → JE → SI → PI → PE). Mỗi phase chỉ chạy sau khi phase trước hoàn tất, không có race condition giữa master và transaction.") }}</p>
						</div>
						<div class="task-item">
							<strong>🌳 2. Account nested-set ordering</strong>
							<p>{{ __("Hệ thống tài khoản (COA) có cấu trúc cây: 111 (Tiền mặt) là cha của 1111, 1112. Khi import, parent phải tồn tại với is_group=1 TRƯỚC khi child arrive. Sort theo CHAR_LENGTH(_tk) ASC trong SQL để parent (mã ngắn) luôn xử lý trước child (mã dài).") }}</p>
						</div>
						<div class="task-item">
							<strong>⚡ 3. Indexed voucher_no lookup</strong>
							<p>{{ __("Lúc parse, voucher_no được tách ra cột riêng (có index). Khi NKC handler cần lookup line items từ Bảng kê BR/MV theo voucher_no, dùng index B-tree thay vì JSON_EXTRACT full-table-scan — tăng tốc Phase 4 từ ~50ms/row xuống ~3ms/row (15-50x).") }}</p>
						</div>
						<div class="task-item">
							<strong>🔁 4. Idempotency — re-run safe</strong>
							<p>{{ __("Mỗi Misa Migration Row có status (Ready/Posted/Failed/Exists/Reversed) + target_doctype/target_name. Nếu post bị gián đoạn giữa chừng (worker crash, timeout), re-enqueue chỉ xử lý Ready rows, không tạo trùng. lookup_existing chạy 2 lần (preview + post) để guard double-create.") }}</p>
						</div>
						<div class="task-item">
							<strong>📦 5. Two-phase submit (4a: insert docstatus=0, 4b: submit)</strong>
							<p>{{ __("Insert + Submit chia 2 pass: Phase 4a tạo TẤT CẢ vouchers ở docstatus=0 (draft) trước. Phase 4b submit theo dependency order: Stock Entry → Journal Entry → Sales Invoice → Purchase Invoice → Payment Entry. Tại sao? PE.references chỉ accept SI/PI đã docstatus=1; nếu submit PE trước SI, ERPNext throw 'reference not allowed'. Tách 2 pass giúp Phase 4a chạy nhanh (không qua validate submit), Phase 4b xử lý FK constraint đúng thứ tự.") }}</p>
						</div>
						<div class="task-item">
							<strong>🔗 6. PE backfill — cancel + amend</strong>
							<p>{{ __("Misa NKC voucher PE có thể đề cập SI/PI sẽ tạo SAU nó. Ta không thể link lúc insert (SI chưa có). Sau khi tất cả SI/PI submitted, _backfill_pe_references_for_batch lấy từng PE đã submit → cancel → frappe.copy_doc tạo bản amended có references đầy đủ → submit lại. Pattern này cần thiết vì ERPNext cấm sửa PE.references sau submit.") }}</p>
						</div>
						<div class="task-item">
							<strong>🪵 7. Stock-account temporary unblock</strong>
							<p>{{ __("ERPNext mặc định cấm Journal Entry có legs vào tài khoản account_type='Stock' (chống bypass Stock Ledger). Misa NKC lại có nghiệp vụ hợp lệ tác động vào TK kho. Pipeline temp-clear account_type='Stock' trên mọi Account của Company TRƯỚC khi submit, restore lại sau khi xong — chỉ JE mới (Misa-tagged) được lợi, JE thực tế của user vẫn được bảo vệ.") }}</p>
						</div>
						<div class="task-item">
							<strong>💾 8. Chunked commit + per-doc transaction isolation</strong>
							<p>{{ __("Mỗi doc INSERT/SUBMIT commit độc lập (per-doc try/except). Nếu doc#1234 fail không rollback doc#1-1233. Bulk parse insert chunk 200 rows/commit (50x nhanh hơn 1 row/commit). frappe.flags.mute_messages = True trong giai đoạn cancel để tránh flood UI 22k+ popup 'Payment items not linked'.") }}</p>
						</div>
						<div class="task-item">
							<strong>👻 9. Background queue + RQ (Redis Queue)</strong>
							<p>{{ __("Post pipeline enqueue vào queue 'long' (timeout 14400s = 4h). Worker chạy độc lập với HTTP — user có thể đóng tab, refresh, log out; pipeline vẫn tiếp tục. UI poll real-time qua frappe.publish_realtime + setInterval fallback để hiện progress.") }}</p>
						</div>
						<div class="task-item">
							<strong>🛡️ 10. Pre-flight 8-check gating</strong>
							<p>{{ __("Trước khi enqueue post: kiểm tra bút toán cân Dr=Cr, kỳ kế toán chưa khóa, master Customer/Supplier đã import, Company currency = VND, không bị duplicate voucher từ batch trước, v.v. Block-level fail ngăn enqueue; warn-level chỉ cảnh báo. Tránh chạy 1-2 giờ rồi mới crash.") }}</p>
						</div>
					</div>
					<div class="post-explainer-perf">
						<strong>📊 Performance khi import full 2025 + Jan 2026 (~116,782 dòng)</strong>
						<ul>
							<li>{{ __("Phase 1+2+3 master: 156 Ready rows + 4,027 Exists — ~5s") }}</li>
							<li>{{ __("Phase 0 OB: 1,614 rows + 16 SE + 1 OB JE — ~15s") }}</li>
							<li>{{ __("Phase 4a inserts: 88,136 NKC + 7,215 BR + 9,175 MV + 4,807 SCT line items — ~15-20 phút") }}</li>
							<li>{{ __("Phase 4b submit: ~16k vouchers (SE → JE → SI → PI → PE) — ~10-15 phút") }}</li>
							<li>{{ __("Tổng: ~25-35 phút trên dev bench, có thể nhanh hơn 2-3x trên prod với SSD + nhiều worker") }}</li>
						</ul>
					</div>
				</div>
			</details>

			<!-- Preflight summary -->
			<div v-if="preflightData" class="preflight">
				<div class="metrics">
					<div class="metric ready">
						<div class="metric-n">{{ preflightData.n_ready }}</div>
						<div class="metric-label">{{ __("Ready") }}</div>
					</div>
					<div class="metric conflict">
						<div class="metric-n">{{ preflightData.n_conflict }}</div>
						<div class="metric-label">{{ __("Conflict") }}</div>
					</div>
					<div class="metric invalid">
						<div class="metric-n">{{ preflightData.n_invalid }}</div>
						<div class="metric-label">{{ __("Invalid") }}</div>
					</div>
				</div>

				<div v-if="preflightData.blocked.length" class="blocked-list">
					<strong>{{ __("Bị chặn:") }}</strong>
					<ul>
						<li v-for="(b, i) in preflightData.blocked" :key="i">{{ b }}</li>
					</ul>
				</div>
				<div v-if="preflightData.warnings.length" class="warning-list">
					<strong>{{ __("Cảnh báo:") }}</strong>
					<ul>
						<li v-for="(w, i) in preflightData.warnings" :key="i">{{ w }}</li>
					</ul>
				</div>

				<!-- UX Gap 7: Phase 0 prerequisite check panel -->
				<div
					v-if="preflightData.phase_0_checks?.length"
					class="phase-0-panel"
					:class="'panel-' + (preflightData.phase_0_status || 'ok')"
				>
					<strong>{{ __("Phase 0 — kiểm tra phụ thuộc master:") }}</strong>
					<table class="phase-0-table">
						<thead>
							<tr>
								<th>{{ __("OB file") }}</th>
								<th>{{ __("Kiểm tra") }}</th>
								<th>{{ __("Có / Cần") }}</th>
								<th>{{ __("Mức") }}</th>
								<th>{{ __("Gợi ý sửa") }}</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(c, i) in preflightData.phase_0_checks" :key="i"
								:class="{
									'phase-0-pass': c.passed,
									'phase-0-block': !c.passed && c.level === 'block',
									'phase-0-warn': !c.passed && c.level === 'warn',
								}">
								<td>{{ c.file_type }}</td>
								<td>{{ c.label }}</td>
								<td>{{ c.found }} / {{ c.expected }}</td>
								<td>
									<span class="level-badge" :class="'lvl-' + c.level">
										{{ c.passed ? '✓' : (c.level === 'block' ? '❌' : '⚠') }}
									</span>
								</td>
								<td class="hint-cell">{{ c.passed ? '—' : c.hint }}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<!-- Live activity ticker during POSTING/REVERSING — shows what step is in flight -->
			<div v-if="liveActivity" class="live-activity">
				<span class="live-dot">⚡</span>
				<span class="live-text">{{ liveActivity }}</span>
			</div>

			<!-- Phase-grouped progress (rows ordered to match orchestrator import order) -->
			<div v-if="orderedPhases.length" class="phase-progress-stack">
				<div v-for="phase in orderedPhases" :key="phase.id" class="phase-block">
					<div class="phase-header">
						<span class="phase-title">{{ phase.title }}</span>
						<span class="phase-subtitle">{{ phase.subtitle }}</span>
						<span class="phase-summary">{{ phase.summary }}</span>
					</div>
					<div class="entity-progress">
						<div
							v-for="row in phase.rows"
							:key="row.ft"
							class="entity-row"
							:class="{ 'subsidiary': row.subsidiary, 'in-flight': row.inFlight, 'done': row.done }"
						>
							<div class="entity-row-head">
								<span class="entity-name">
									<span v-if="row.inFlight" class="row-spinner">⟳</span>
									<span v-else-if="row.done" class="row-check">✓</span>
									<span v-else-if="row.queued" class="row-queue">·</span>
									{{ row.label }}
									<span v-if="row.subsidiary" class="badge-ref">
										{{ __("Tham chiếu (line items)") }}
									</span>
								</span>
								<span class="entity-fraction">
									<template v-if="row.subsidiary">
										<span class="muted">{{ row.total.toLocaleString() }}</span>
										{{ __("dòng đã đọc — không tạo doc riêng") }}
									</template>
									<template v-else>
										{{ row.processed.toLocaleString() }} / {{ row.total.toLocaleString() }}
										<span v-if="row.failed > 0" class="failed-n">(✗{{ row.failed }})</span>
										<span v-if="row.exists > 0" class="exists-n">({{ row.exists.toLocaleString() }} {{ __("đã có") }})</span>
									</template>
								</span>
							</div>
							<div v-if="!row.subsidiary" class="entity-bar">
								<span class="entity-bar-posted" :style="{ width: row.pctPosted + '%' }"></span>
								<span class="entity-bar-failed" :style="{ width: row.pctFailed + '%' }"></span>
							</div>
							<div v-else class="subsidiary-hint">
								{{ __("File này cung cấp line items cho voucher cha (NKC). Tham khảo bảng dưới để xem chi tiết.") }}
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Phase 4 SUBMIT progress (docstatus 0→1) — separate, in submit order SE → JE → SI → PI → PE -->
			<div v-if="orderedVoucherDoctypes.length" class="voucher-submit-progress">
				<div class="phase-header">
					<span class="phase-title">{{ __("Phase 4b — Đẩy chứng từ lên sổ (docstatus 0 → 1)") }}</span>
					<span class="phase-subtitle">
						{{ __("Thứ tự submit: Phiếu kho → Phiếu kế toán → Hóa đơn bán → Hóa đơn mua → Phiếu thanh toán") }}
					</span>
					<span class="phase-summary">{{ voucherSummary }}</span>
				</div>
				<div class="entity-progress">
					<div
						v-for="d in orderedVoucherDoctypes"
						:key="d.doctype"
						class="entity-row"
						:class="{ 'in-flight': d.inFlight, 'done': d.done }"
					>
						<div class="entity-row-head">
							<span class="entity-name">
								<span v-if="d.inFlight" class="row-spinner">⟳</span>
								<span v-else-if="d.done" class="row-check">✓</span>
								<span v-else-if="d.queued" class="row-queue">·</span>
								{{ d.label }}
							</span>
							<span class="entity-fraction">
								{{ d.submitted }} / {{ d.total }}
								<span class="muted">({{ d.pct }}%)</span>
							</span>
						</div>
						<div class="entity-bar">
							<span class="entity-bar-posted" :style="{ width: d.pct + '%' }"></span>
						</div>
					</div>
				</div>
			</div>

			<!-- Detail counts table (collapsible — same data, full breakdown).
			     Click the Failed number to open a tooltip with grouped error reasons + suggested actions. -->
			<details v-if="progressData?.counts && Object.keys(progressData.counts).length" class="counts-table-collapse">
				<summary>{{ __("Chi tiết theo trạng thái") }}</summary>
				<table class="post-progress-table">
					<thead>
						<tr>
							<th>{{ __("Entity") }}</th>
							<th class="num">{{ __("Posted") }}</th>
							<th class="num">{{ __("Failed") }}</th>
							<th class="num">{{ __("Ready còn lại") }}</th>
							<th class="num">{{ __("Reversed") }}</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(c, ft) in progressData.counts" :key="ft">
							<td>{{ ft }}</td>
							<td class="num posted-n">{{ c.Posted || 0 }}</td>
							<td class="num failed-n">
								<template v-if="(c.Failed || 0) > 0">
									<a href="#" class="failed-link" @click.prevent="openFailedTooltip($event, ft)">
										{{ c.Failed }}
										<span class="failed-link-icon">ℹ</span>
									</a>
								</template>
								<template v-else>0</template>
							</td>
							<td class="num">{{ c.Ready || 0 }}</td>
							<td class="num">{{ c.Reversed || 0 }}</td>
						</tr>
					</tbody>
				</table>
			</details>

			<!-- Failed-rows tooltip popover (anchored, dismissable) -->
			<div
				v-if="failedTooltip.open"
				class="failed-tooltip"
				:style="{ top: failedTooltip.top + 'px', left: failedTooltip.left + 'px' }"
				@click.stop
			>
				<div class="ft-head">
					<strong>{{ failedTooltip.entity }}</strong>
					<span class="muted">{{ failedTooltip.total }} {{ __("dòng thất bại") }}</span>
					<button class="ft-close" @click="failedTooltip.open = false">×</button>
				</div>
				<div v-if="failedTooltip.loading" class="ft-loading">{{ __("Đang tải lý do...") }}</div>
				<div v-else-if="failedTooltip.groups.length === 0" class="ft-empty">{{ __("Không có chi tiết lỗi.") }}</div>
				<ol v-else class="ft-list">
					<li v-for="(g, i) in failedTooltip.groups" :key="i">
						<div class="ft-err-head">
							<span class="ft-err-n">×{{ g.count }}</span>
							<span class="ft-err-text">{{ g.error }}</span>
						</div>
						<div v-if="g.action" class="ft-action">
							<strong>{{ __("Hành động:") }}</strong> {{ g.action }}
						</div>
						<div v-if="g.sample.length" class="ft-samples">
							<span class="muted">{{ __("Ví dụ:") }}</span>
							<code v-for="(s, j) in g.sample" :key="j">{{ s }}</code>
						</div>
					</li>
				</ol>
				<div class="ft-actions">
					<button v-if="failedTooltip.total > 0" class="btn btn-link" @click="openFullFailedModal">
						{{ __("Mở Failed Rows Modal (đầy đủ + Retry)") }}
					</button>
				</div>
			</div>

			<!-- Action buttons -->
			<div class="actions">
				<button
					v-if="store.status === 'REVIEWED'"
					class="btn btn-link"
					:disabled="installingCoa"
					:title="__('Chạy Misa Phase 2 (Account import) trước khi tạo — bridge giữa CoA TT99/2025 do vn_accounting cài và sub-accounts Misa cấp 5 đang chờ trong Migration Rows. Idempotent.')"
					@click="onInstallMisaCoa"
				>
					{{ installingCoa ? __("Đang cài CoA Misa...") : __("Cài đặt CoA Misa") }}
					<span v-if="coaInstallResult" class="dot ok">✓</span>
				</button>

				<button
					v-if="store.status === 'REVIEWED'"
					class="btn btn-link"
					:disabled="derivingMasters"
					:title="__('Tự động trích xuất master từ nội dung NKC/BR/MV: Tài khoản (TK), Kho, Mặt hàng, Khách hàng, Nhà cung cấp. Misa export không có file master riêng — phải derive từ transactional content. Idempotent.')"
					@click="onDeriveMasters"
				>
					{{ derivingMasters ? __("Đang trích xuất master...") : __("Trích xuất master từ batch") }}
					<span v-if="deriveResult" class="dot ok">✓</span>
				</button>

				<button
					v-if="store.status === 'REVIEWED' && (preflightData?.checks?.length || 0) > 0"
					class="btn btn-link"
					@click="showPreflightDialog = true"
				>
					{{ __("Xem chi tiết pre-flight") }}
					<span v-if="preflightData.phase_d_status === 'block'" class="dot block">●</span>
					<span v-else-if="preflightData.phase_d_status === 'warn'" class="dot warn">●</span>
					<span v-else class="dot ok">●</span>
				</button>

				<button
					v-if="store.status === 'REVIEWED'"
					class="btn btn-primary"
					:disabled="busy || (preflightData?.blocked?.length > 0) || (preflightData?.n_ready === 0)"
					@click="onPost"
				>
					{{ busy ? __("Đang tạo...") : __("Tạo vào ERPNext") }}
				</button>

				<button
					v-if="store.status === 'REVIEWED'"
					class="btn btn-default"
					:disabled="busy || (preflightData?.blocked?.length > 0) || (preflightData?.n_ready === 0)"
					:title="__('Tạo nhanh bằng SQL bulk-INSERT — ~140x nhanh hơn chế độ ORM mặc định. Bỏ qua validate/hooks của ERPNext; chỉ dùng cho batch lịch sử nguồn dữ liệu đã sạch. Khuyến nghị: chạy thử trên batch nhỏ trước.')"
					@click="onPostBulkFull"
				>
					{{ busy ? __("Đang tạo...") : __("⚡ Tạo chế độ nhanh (SQL)") }}
				</button>

				<button
					v-if="store.status === 'POSTED' && totalFailed > 0"
					class="btn btn-warning"
					@click="showFailedModal = true"
				>
					{{ __("Xem & Retry") }} ({{ totalFailed }} {{ __("dòng Failed") }})
				</button>

				<button
					v-if="store.status === 'POSTED'"
					class="btn btn-danger"
					:disabled="busy"
					@click="onUndo"
				>
					{{ busy ? __("Đang hoàn tác...") : __("Hoàn tác (Undo)") }}
				</button>

				<button
					v-if="store.status === 'POSTING' || store.status === 'REVERSING'"
					class="btn btn-link"
					:disabled="true"
				>
					<span class="spinner">⟳</span> {{ __("Đang chạy background...") }}
				</button>

				<div v-if="store.status === 'REVERSED'" class="done-msg">
					✓ {{ __("Batch đã được hoàn tác. Tạo batch mới hoặc đóng tab.") }}
				</div>

				<button
					v-if="store.status === 'POSTED' || store.status === 'REVERSED'"
					class="btn btn-link"
					@click="refresh"
				>
					{{ __("Cập nhật trạng thái") }}
				</button>
			</div>

			<!-- Post-Migration Health Check card — appears after POSTED -->
			<div
				v-if="['POSTED', 'STUCK'].includes(store.status)"
				class="health-check-card"
			>
				<div class="hc-head">
					<h4>{{ __("📊 Kiểm tra cân đối sau import") }}</h4>
					<button v-if="!healthData" class="btn btn-link" :disabled="hcBusy" @click="runHealthCheck">
						{{ hcBusy ? __("Đang phân tích...") : __("Chạy kiểm tra") }}
					</button>
					<button v-else class="btn btn-link" :disabled="hcBusy" @click="runHealthCheck">
						{{ __("Chạy lại") }}
					</button>
				</div>
				<p class="muted hc-intro">
					{{ __("Phân tích Balance Sheet sau khi tạo — tự động phát hiện tài khoản lệch dấu (TS có Cr, Nợ phải trả có Dr), thiếu OB, mismatch SE/JE/AR/AP. KHÔNG sửa dữ liệu, chỉ báo cáo + đề xuất hành động.") }}
				</p>

				<div v-if="healthData" class="hc-body">
					<!-- Balance summary -->
					<div class="hc-balance">
						<div class="bal-row"><span>{{ __("Tài sản") }}</span><strong>{{ formatVND(healthData.bs_summary.assets) }}</strong></div>
						<div class="bal-row"><span>{{ __("Nợ phải trả") }}</span><strong>{{ formatVND(healthData.bs_summary.liabilities) }}</strong></div>
						<div class="bal-row"><span>{{ __("Vốn chủ sở hữu") }}</span><strong>{{ formatVND(healthData.bs_summary.equity) }}</strong></div>
						<div class="bal-row"><span>{{ __("Lợi nhuận tạm") }}</span><strong>{{ formatVND(healthData.bs_summary.pnl) }}</strong></div>
						<div class="bal-row total">
							<span>
								<template v-if="healthData.balance_sheet_balanced">✓ {{ __("Cân (Dr = Cr)") }}</template>
								<template v-else>⚠ {{ __("Lệch") }} {{ formatVND(Math.abs(healthData.imbalance)) }}</template>
							</span>
							<strong :class="{ 'balanced': healthData.balance_sheet_balanced, 'imbalanced': !healthData.balance_sheet_balanced }">
								{{ healthData.balance_sheet_balanced ? '✓' : '✗' }}
							</strong>
						</div>
					</div>

					<!-- Anomalies list -->
					<div v-if="healthData.n_anomalies === 0" class="hc-ok">
						✅ {{ __("Không phát hiện bất thường — tất cả tài khoản đều có số dư đúng chiều kỳ vọng.") }}
					</div>
					<div v-else class="hc-anomalies">
						<div class="hc-summary-bar">
							<strong>{{ healthData.n_anomalies }} {{ __("tài khoản bất thường") }}</strong>
							<span class="muted">{{ __("Click từng dòng để xem lý do + đề xuất sửa") }}</span>
						</div>
						<details
							v-for="a in healthData.anomalies"
							:key="a.account"
							class="anomaly-row"
							:class="'sev-' + (a.findings[0]?.severity || 'info')"
						>
							<summary>
								<span class="anom-name">{{ a.account_name }}</span>
								<span class="anom-net">
									{{ formatVND(a.net) }}
									<span class="muted">({{ __("kỳ vọng") }} {{ a.expected_sign }})</span>
								</span>
							</summary>
							<div class="anom-body">
								<div class="anom-section">
									<strong>{{ __("Lý do phát hiện được:") }}</strong>
									<ul>
										<li v-for="(f, i) in a.findings" :key="i" :class="'sev-' + f.severity">
											<span class="sev-badge">{{ f.severity }}</span>
											{{ f.msg }}
										</li>
									</ul>
								</div>
								<div v-if="a.actions.length" class="anom-section">
									<strong>{{ __("Hành động đề xuất:") }}</strong>
									<ul>
										<li v-for="(action, i) in a.actions" :key="i">{{ action }}</li>
									</ul>
								</div>
							</div>
						</details>
					</div>
				</div>
				<div v-else-if="hcError" class="error">{{ hcError }}</div>
			</div>

			<!-- Pipeline recovery (Item 2) — advanced operator tools -->
			<details
				v-if="store.status === 'POSTED' || store.status === 'POSTING' || store.status === 'REVERSED'"
				class="recovery-collapse"
			>
				<summary>{{ __("Khôi phục pipeline (nâng cao)") }}</summary>
				<p class="muted recovery-help">
					{{ __("Hai thao tác này chạy ở mức pipeline (toàn bộ doc Phase 4 đã import bởi batch này), khác với 'Hoàn tác' ở trên (chạy ở mức batch).") }}
				</p>
				<div class="recovery-actions">
					<button
						class="btn btn-warning"
						:disabled="busy"
						@click="onCancelPhase4"
					>
						{{ __("Hủy Phase 4 (REVERSE: PE → PI → SI → JE → SE)") }}
					</button>
					<button
						class="btn btn-danger"
						:disabled="busy"
						@click="onDeletePhase4"
					>
						{{ __("Xóa nháp Phase 4 (docstatus 0 + 2)") }}
					</button>
				</div>
				<div v-if="recoveryResult" class="recovery-result">
					<strong>{{ recoveryResultLabel }}:</strong>
					<pre>{{ JSON.stringify(recoveryResult, null, 2) }}</pre>
				</div>
			</details>
		</div>

		<PreflightDialog
			:open="showPreflightDialog"
			:data="preflightData"
			@close="showPreflightDialog = false"
			@confirm="onConfirmFromDialog"
		/>

		<FailedRowsModal
			:open="showFailedModal"
			@close="showFailedModal = false"
			@retried="onRetried"
		/>
	</div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useMisaStore } from "../store.js";
import PreflightDialog from "../components/PreflightDialog.vue";
import FailedRowsModal from "../components/FailedRowsModal.vue";

const store = useMisaStore();
function __(t) { return typeof window.__ === "function" ? window.__(t) : t; }

const preflightData = ref(null);
const progressData = ref(null);
const voucherProgress = ref(null);
const busy = ref(false);
const error = ref(null);
const showPreflightDialog = ref(false);
const showFailedModal = ref(false);
const recoveryResult = ref(null);
const recoveryResultLabel = ref("");
const installingCoa = ref(false);
const coaInstallResult = ref(null);
const derivingMasters = ref(false);
const deriveResult = ref(null);
let realtimeOff = null;
let voucherProgressTimer = null;

async function onInstallMisaCoa() {
	error.value = null;
	installingCoa.value = true;
	try {
		const r = await store.installMisaCoa();
		coaInstallResult.value = r;
		// Detect non-VN CoA: install_misa_coa bootstraps via bootstrap_coa which
		// returns 'non_vn_coa_detected' when Company has Standard CoA (Frappe
		// auto-create on Company.insert with country=Vietnam). Offer force overwrite.
		const inner = r?.bootstrap_coa || r;
		if (inner?.action === "non_vn_coa_detected") {
			const msg = inner.message
				|| __("Company có CoA chuẩn (không phải VN VAS). Ghi đè bằng CoA VN VAS TT99/2025? Chỉ chạy khi chưa có giao dịch.");
			const ok = await new Promise(resolve =>
				frappe.confirm(msg, () => resolve(true), () => resolve(false)));
			if (ok) {
				const force = await store.bootstrapCoaForce();
				coaInstallResult.value = { ...r, force_install: force };
				frappe.show_alert({
					message: __("Đã ghi đè CoA VN: {0} tài khoản",
						[force?.total_accounts || force?.accounts_created || 0]),
					indicator: "green",
				}, 5);
				// Re-run install_misa_coa now that VN CoA exists — Phase 1/2 Misa
				// rows can now insert Account refs that match.
				await store.installMisaCoa();
			}
		}
		setTimeout(refresh, 400);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		installingCoa.value = false;
	}
}

async function onDeriveMasters() {
	error.value = null;
	derivingMasters.value = true;
	try {
		const r = await store.deriveMastersFromBatch();
		deriveResult.value = r;
		const acc = r?.Account?.created || 0;
		const wh = r?.Warehouse?.created || 0;
		const it = r?.Item?.created || 0;
		const cust = r?.Parties?.Customer?.created || 0;
		const supp = r?.Parties?.Supplier?.created || 0;
		frappe.show_alert({
			message: __("Đã trích xuất: {0} TK, {1} kho, {2} mặt hàng, {3} khách, {4} nhà cung cấp",
				[acc, wh, it, cust, supp]),
			indicator: "green",
		}, 6);
		// derive_masters có thể tạo sub-account (vd 1111) → promote 111 thành group
		// → Company.default_cash_account orphan. Auto-fix ngay.
		try { await store.refreshCompanyDefaultAccounts(); } catch (_) { /* best-effort */ }
		setTimeout(refresh, 400);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		derivingMasters.value = false;
	}
}

// Post-migration health check
const healthData = ref(null);
const hcBusy = ref(false);
const hcError = ref(null);

async function runHealthCheck() {
	hcBusy.value = true;
	hcError.value = null;
	try {
		const data = await new Promise((resolve, reject) => {
			frappe.call({
				method: "vn_accounting.misa_migration.api.health_check.run_health_check",
				args: { batch_name: store.batch_name },
				callback: r => resolve(r?.message),
				error: () => reject(),
			});
		});
		healthData.value = data;
	} catch (e) {
		hcError.value = e?.message || String(e);
	} finally {
		hcBusy.value = false;
	}
}

function formatVND(n) {
	if (n === null || n === undefined) return "—";
	const v = Math.round(Number(n) || 0);
	return v.toLocaleString("vi-VN");
}

// Failed-rows tooltip (clicking a Failed number)
const failedTooltip = ref({
	open: false, entity: "", total: 0, top: 0, left: 0,
	loading: false, groups: [],
});

// Suggested action per error pattern. Matched against error_message substring.
// Order matters — first match wins.
const FAILED_ACTION_RULES = [
	{
		match: /thiếu line items|missing line items|bảng kê.*invoice not provided/i,
		action: "Voucher cha (NKC) tham chiếu mã hóa đơn nhưng file Bảng kê BR/MV không có dòng tương ứng. Kiểm tra Misa, bổ sung file Bảng kê chứa các mã này, parse lại rồi retry.",
	},
	{
		match: /missing party_code|thiếu mã đối tượng|thiếu party/i,
		action: "Voucher không có 'Mã đối tượng' (cột J trong Misa). Mở file Misa, điền Mã đối tượng cho dòng tương ứng, parse lại rồi retry.",
	},
	{
		match: /DuplicateEntryError.*Item/i,
		action: "Item code đã tồn tại trong ERPNext nhưng có khác biệt nhỏ (case-sensitive / khoảng trắng). An toàn để bỏ qua — Item bản gốc trong ERPNext đã sẵn sàng để các giao dịch sau tham chiếu.",
	},
	{
		match: /DuplicateEntryError|Duplicate entry/i,
		action: "Bản ghi đã tồn tại (có thể do lần import trước). Mở Misa Migration Row, mark Skipped để bỏ qua.",
	},
	{
		match: /Account.*does not exist|Tài khoản.*không tồn tại/i,
		action: "Tài khoản chưa có trong COA. Quay lại Phase 2 (Hệ thống tài khoản), kiểm tra file đã upload + parse, hoặc tạo tài khoản thủ công.",
	},
	{
		match: /Cost Center.*does not exist|Trung tâm chi phí.*không tồn tại/i,
		action: "Trung tâm chi phí chưa có. Phase 1 (Doi_tuong_tap_hop_chi_phi.xlsx) chưa import đủ — kiểm tra + parse lại.",
	},
	{
		match: /Customer.*does not exist|Khách hàng.*không tồn tại/i,
		action: "Khách hàng chưa có trong master. Phase 3 (Danh_sach_khach_hang.xlsx) chưa import — kiểm tra + import trước.",
	},
	{
		match: /Supplier.*does not exist|Nhà cung cấp.*không tồn tại/i,
		action: "Nhà cung cấp chưa có trong master. Phase 3 (Danh_sach_nha_cung_cap.xlsx) chưa import — kiểm tra + import trước.",
	},
	{
		match: /negative stock|tồn kho âm/i,
		action: "Giao dịch xuất kho làm tồn kho âm. Bật allow_negative_stock=1 trong Stock Settings (đã tự bật khi import nhưng có thể bị tắt lại). Hoặc kiểm tra OB Inventory đã import đủ.",
	},
	{
		match: /Period.*closed|Kỳ.*đã khóa|posting_date.*closed/i,
		action: "Kỳ kế toán đã khóa (Period Closing Voucher đã chốt). Mở khóa kỳ trong ERPNext, post lại, sau đó chốt lại kỳ.",
	},
	{
		match: /timeout|TimeoutError/i,
		action: "Worker bị timeout giữa chừng (doc quá lớn). Retry lại bằng FailedRows Modal.",
	},
	{
		match: /MandatoryError|reqd|required/i,
		action: "Thiếu trường bắt buộc. Xem error message để biết field nào — sửa source data trong Misa hoặc dùng Customize Form để gỡ required.",
	},
];

function _suggestAction(error) {
	for (const rule of FAILED_ACTION_RULES) {
		if (rule.match.test(error || "")) return rule.action;
	}
	return null;
}

async function openFailedTooltip(ev, ft) {
	const r = ev.currentTarget.getBoundingClientRect();
	failedTooltip.value = {
		open: true,
		entity: ft,
		total: (progressData.value?.counts || {})[ft]?.Failed || 0,
		top: r.bottom + window.scrollY + 4,
		left: Math.max(8, r.left + window.scrollX - 280),
		loading: true,
		groups: [],
	};
	try {
		const data = await new Promise((resolve, reject) => {
			frappe.call({
				method: "vn_accounting.misa_migration.api.upload.get_failed_rows_grouped",
				args: { batch_name: store.batch_name, entity_type: ft },
				callback: r => resolve(r?.message),
				error: () => reject(),
			});
		});
		const groups = (data?.groups || []).map(g => ({
			error: g.error,
			count: g.count,
			sample: g.sample || [],
			action: _suggestAction(g.error),
		}));
		failedTooltip.value = { ...failedTooltip.value, loading: false, groups };
	} catch (e) {
		failedTooltip.value = { ...failedTooltip.value, loading: false, groups: [] };
	}
}

function openFullFailedModal() {
	failedTooltip.value.open = false;
	showFailedModal.value = true;
}

function _onDocumentClick(e) {
	// Click outside tooltip closes it
	if (!failedTooltip.value.open) return;
	const tooltip = document.querySelector(".failed-tooltip");
	if (tooltip && !tooltip.contains(e.target) && !e.target.closest(".failed-link")) {
		failedTooltip.value.open = false;
	}
}

const API = "vn_accounting.misa_migration.api.upload";

// Exponential backoff state shared with the setInterval tick. Each
// failure doubles the next interval (cap 30s) so a transient bench
// restart doesn't spam dozens of net::ERR_* lines in the console.
let _voucher_poll_interval = 5000;
const _VOUCHER_POLL_MAX = 30000;
async function fetchVoucherProgress() {
	if (!store.batch_name) return false;
	try {
		const data = await new Promise((resolve, reject) => {
			frappe.call({
				method: `${API}.get_voucher_submit_progress`,
				args: { batch_name: store.batch_name },
				callback: r => resolve(r?.message),
				error: () => reject(),
			});
		});
		if (data) voucherProgress.value = data;
		return true;
	} catch (e) { return false; }
}

const totalFailed = computed(() => {
	const counts = progressData.value?.counts || {};
	return Object.values(counts).reduce((s, c) => s + (c.Failed || 0), 0);
});

async function onRetried() {
	// Refresh state after retry enqueues a re-post
	setTimeout(refresh, 1200);
}

function totalForFt(c) {
	return (c.Ready || 0) + (c.Posted || 0) + (c.Failed || 0) + (c.Reversed || 0);
}

// Subsidiary file types are LOOKUP DATA consumed by NKC voucher handlers
// (they don't create their own ERPNext doc → row.target_doctype stays NULL
// → Posted count stays 0). Showing them as "0/N" in a progress bar is
// confusing — operator thinks nothing happened. Instead, render a
// "Tham chiếu" badge + show how many lines were read.
const SUBSIDIARY_FILE_TYPES = new Set([
	"Bang ke BR", "Bang ke MV", "SCT",
	"Misa Default Account", "Misa Closing Rule",
]);
function isSubsidiary(ft) {
	return SUBSIDIARY_FILE_TYPES.has(ft);
}
function pctPosted(c) {
	const t = totalForFt(c);
	return t > 0 ? Math.round((c.Posted || 0) * 100 / t) : 0;
}
function pctFailed(c) {
	const t = totalForFt(c);
	return t > 0 ? Math.round((c.Failed || 0) * 100 / t) : 0;
}

// --- Phase ordering — must mirror orchestrator (phase_4_orchestrator + run_phase_X)
// User-visible labels are Vietnamese; technical entity_type stays English.
const PHASE_LAYOUT = [
	{
		id: "phase_1",
		title: "Phase 1 — Master tham chiếu",
		subtitle: "Đơn vị tính, Phòng ban, Kho, Nhóm khách hàng/NCC, Nhóm hàng hóa, TT chi phí, Dự án, Phân loại TSCĐ/CCDC, Ngân hàng",
		entities: [
			["UOM", "Đơn vị tính (UOM)"],
			["Department", "Phòng ban"],
			["Warehouse", "Kho"],
			["Item Group", "Nhóm hàng hóa/dịch vụ"],
			["Customer Group", "Nhóm khách hàng"],
			["Supplier Group", "Nhóm nhà cung cấp"],
			["Cost Center", "Trung tâm chi phí"],
			["Project", "Công trình / Dự án"],
			["Asset Category", "Phân loại TSCĐ"],
			["CCDC Category", "Phân loại CCDC"],
			["Bank", "Ngân hàng"],
		],
	},
	{
		id: "phase_2",
		title: "Phase 2 — Hệ thống tài khoản",
		subtitle: "Chart of Accounts + tài khoản ngầm định + tài khoản kết chuyển",
		entities: [
			["Account", "Hệ thống tài khoản (COA)"],
			["Misa Default Account", "Tài khoản ngầm định Misa"],
			["Misa Closing Rule", "Quy tắc kết chuyển Misa"],
		],
	},
	{
		id: "phase_3",
		title: "Phase 3 — Master nghiệp vụ",
		subtitle: "Khách hàng, Nhà cung cấp, Hàng hóa, Nhân viên, Tài khoản ngân hàng",
		entities: [
			["Customer", "Khách hàng"],
			["Supplier", "Nhà cung cấp"],
			["Item", "Hàng hóa / Dịch vụ"],
			["Employee", "Nhân viên"],
			["Bank Account", "Tài khoản ngân hàng"],
		],
	},
	{
		id: "phase_0",
		title: "Phase 0 — Số dư đầu kỳ",
		subtitle: "Toàn bộ 9 nhóm OB từ Misa (số dư TK, kho, công nợ, TSCĐ, CCDC, chi phí trả trước)",
		entities: [
			["OB Account Balance", "Số dư đầu kỳ tài khoản (TK 1xx-9xx)"],
			["OB Bank Balance", "Số dư đầu kỳ ngân hàng"],
			["OB Customer AR", "Công nợ khách hàng đầu kỳ"],
			["OB Supplier AP", "Công nợ nhà cung cấp đầu kỳ"],
			["OB Employee Advance", "Tạm ứng nhân viên đầu kỳ"],
			["OB Inventory", "Tồn kho đầu kỳ"],
			["OB Fixed Asset", "TSCĐ đầu kỳ"],
			["OB CCDC", "CCDC đầu kỳ"],
			["OB Prepaid Expense", "Chi phí trả trước đầu kỳ"],
		],
	},
	{
		id: "phase_4",
		title: "Phase 4a — Giao dịch trong kỳ (insert)",
		subtitle: "Nhật ký chung + Bảng kê bán ra/mua vào + Sổ chi tiết VTHH (chèn ở docstatus=0)",
		entities: [
			["NKC", "Nhật ký chung (NKC)"],
			["Bang ke BR", "Bảng kê hóa đơn bán ra"],
			["Bang ke MV", "Bảng kê hóa đơn mua vào"],
			["SCT", "Sổ chi tiết VTHH"],
		],
	},
];

// Phase 4 submit order (mirrors phase_4_orchestrator.submit_phase_4_drafts) —
// docstatus 0 → 1 in this order: SE creates stock movement first, then JE for
// adjustments, then SI/PI bill the customer/vendor, finally PE settles cash.
const SUBMIT_ORDER = [
	["Stock Entry", "Phiếu xuất / nhập kho (Stock Entry)"],
	["Journal Entry", "Phiếu kế toán (Journal Entry)"],
	["Sales Invoice", "Hóa đơn bán hàng (Sales Invoice)"],
	["Purchase Invoice", "Hóa đơn mua hàng (Purchase Invoice)"],
	["Payment Entry", "Phiếu thanh toán (Payment Entry)"],
];

function _buildEntityRow(ft, label, counts) {
	const c = counts[ft] || {};
	const exists = c.Exists || 0;
	const skipped = c.Skipped || 0;
	const conflict = c.Conflict || 0;
	const subsidiary = SUBSIDIARY_FILE_TYPES.has(ft);
	const posted = c.Posted || 0;
	const failed = c.Failed || 0;
	const reversed = c.Reversed || 0;
	const ready = c.Ready || 0;
	// `total` = ALL rows seen for this entity. Includes Exists (already in
	// ERPNext, no insert needed but COUNTS as processed), Skipped, Conflict,
	// posted, failed, ready, reversed. Without Exists, Phase 1+2+3 master
	// entities show as "0 / few doc" while actually 100% processed.
	const total = ready + posted + failed + reversed + exists + skipped + conflict;
	// `processed` = anything in a terminal state (already complete).
	const processed = posted + failed + reversed + exists + skipped;
	const done = !subsidiary && total > 0 && ready === 0;
	const inFlight = !subsidiary && posted > 0 && ready > 0;
	const queued = !subsidiary && posted === 0 && ready > 0;
	const pctP = subsidiary ? 0 : (total > 0 ? Math.round(processed * 100 / total) : 0);
	const pctF = subsidiary ? 0 : (total > 0 ? Math.round(failed * 100 / total) : 0);
	return {
		ft, label, subsidiary,
		total, posted, failed, reversed, ready, exists, skipped, conflict,
		processed,
		pctPosted: pctP, pctFailed: pctF,
		inFlight, queued, done,
	};
}

const orderedPhases = computed(() => {
	const counts = progressData.value?.counts || {};
	const out = [];
	for (const phase of PHASE_LAYOUT) {
		const rows = [];
		let phaseTotal = 0, phaseProcessed = 0, phaseFailed = 0, phaseExists = 0, phaseSubsidiaryLines = 0;
		for (const [ft, label] of phase.entities) {
			if (!(ft in counts)) continue;  // omit rows the batch didn't include
			const row = _buildEntityRow(ft, label, counts);
			rows.push(row);
			if (row.subsidiary) {
				phaseSubsidiaryLines += row.total;
			} else {
				phaseTotal += row.total;
				phaseProcessed += row.processed;
				phaseFailed += row.failed;
				phaseExists += row.exists;
			}
		}
		if (rows.length === 0) continue;
		const existsSuffix = phaseExists > 0 ? ` · ${phaseExists.toLocaleString()} đã có sẵn` : "";
		const summary = phaseTotal > 0
			? `${phaseProcessed.toLocaleString()} / ${phaseTotal.toLocaleString()} doc` + (phaseFailed > 0 ? ` (✗${phaseFailed})` : "")
			  + existsSuffix
			  + (phaseSubsidiaryLines > 0 ? ` · ${phaseSubsidiaryLines.toLocaleString()} dòng line items` : "")
			: (phaseSubsidiaryLines > 0 ? `${phaseSubsidiaryLines.toLocaleString()} dòng line items` : "—");
		out.push({ ...phase, rows, summary });
	}
	return out;
});

const orderedVoucherDoctypes = computed(() => {
	const list = voucherProgress.value?.doctypes || [];
	const byName = Object.fromEntries(list.map(d => [d.doctype, d]));
	const out = [];
	for (const [dt, label] of SUBMIT_ORDER) {
		if (!byName[dt]) continue;
		const d = byName[dt];
		const submitted = d.submitted || 0;
		const total = d.total || 0;
		const pct = d.pct || 0;
		const done = total > 0 && submitted === total;
		const inFlight = submitted > 0 && submitted < total;
		const queued = submitted === 0 && total > 0;
		out.push({ ...d, label, done, inFlight, queued });
	}
	return out;
});

const voucherSummary = computed(() => {
	const list = orderedVoucherDoctypes.value;
	if (!list.length) return "—";
	const submitted = list.reduce((s, d) => s + (d.submitted || 0), 0);
	const total = list.reduce((s, d) => s + (d.total || 0), 0);
	return `${submitted} / ${total} chứng từ đã submit`;
});

// liveActivity: 1-line "what's happening right now" message during POSTING/REVERSING.
// Resolves to the first in-flight phase row OR the first in-flight voucher submit row.
const liveActivity = computed(() => {
	if (!["POSTING", "REVERSING"].includes(store.status)) return null;
	// Phase 4b voucher submit takes priority (it's the slowest, latest phase)
	const inflightVoucher = orderedVoucherDoctypes.value.find(d => d.inFlight);
	if (inflightVoucher) {
		const verb = store.status === "REVERSING" ? "Đang hủy" : "Đang submit";
		return `${verb} ${inflightVoucher.label} — ${inflightVoucher.submitted} / ${inflightVoucher.total} (${inflightVoucher.pct}%)`;
	}
	// Otherwise find first in-flight Phase 1-4a row
	for (const phase of orderedPhases.value) {
		const inflight = phase.rows.find(r => r.inFlight);
		if (inflight) {
			return `${phase.title}: đang xử lý ${inflight.label} — ${inflight.posted + inflight.failed} / ${inflight.total}`;
		}
		const queued = phase.rows.find(r => r.queued && !r.subsidiary);
		if (queued) {
			return `${phase.title}: chờ xử lý ${queued.label} (${queued.total} dòng)`;
		}
	}
	if (store.status === "POSTING") return "Đang khởi tạo pipeline — chờ worker bắt đầu...";
	return null;
});
async function onConfirmFromDialog() {
	showPreflightDialog.value = false;
	await onPost();
}

async function refresh() {
	error.value = null;
	await store.refreshBatch().catch(() => {});
	if (store.status === "REVIEWED") {
		try { preflightData.value = await store.preflight(); } catch (e) { error.value = e.message; }
	}
	try { progressData.value = await store.getPostProgress(); } catch (e) { /* swallow */ }
}

async function onPost() {
	error.value = null; busy.value = true;
	try {
		await store.startPost(false);
		setTimeout(refresh, 800);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}

async function onPostBulkFull() {
	const msg = __(
		"<b>Đăng nhanh bằng SQL bulk-INSERT</b> bỏ qua validate/hooks của ERPNext.<br><br>"
		+ "Chỉ chạy chế độ này nếu:<br>"
		+ "• Đợt nhập là dữ liệu lịch sử nguồn đã sạch (Misa, kế toán đã chốt)<br>"
		+ "• Đã chạy kiểm tra trước (preflight) + duyệt xong<br>"
		+ "• Chấp nhận không có chi tiết lịch sử per-chứng-từ<br><br>"
		+ "Tiếp tục đăng?"
	);
	// frappe.confirm: in-DOM modal — testable + consistent với UX khác (window.confirm
	// native dialog không auto-accept được trong Playwright/automation test)
	const userOK = await new Promise(resolve => {
		frappe.confirm(msg, () => resolve(true), () => resolve(false));
	});
	if (!userOK) return;
	error.value = null; busy.value = true;
	try {
		const r = await store.startPostBulkFull();
		const elapsed = r && r.elapsed_seconds ? r.elapsed_seconds : "?";
		const n = r && r.voucher_count ? r.voucher_count : "?";
		frappe.show_alert({
			message: __("SQL pump xong trong {0}s ({1} vouchers)", [elapsed, n]),
			indicator: "green",
		}, 6);
		setTimeout(refresh, 800);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}

async function onUndo() {
	const userOK = await new Promise(resolve => {
		frappe.confirm(
			__("Hoàn tác toàn bộ đợt nhập? Mọi chứng từ do đợt này tạo sẽ bị cancel + xoá."),
			() => resolve(true), () => resolve(false),
		);
	});
	if (!userOK) return;
	error.value = null; busy.value = true;
	try {
		await store.startUndo(false, false);
		setTimeout(refresh, 800);
	} catch (e) {
		const msg = e.message || String(e);
		error.value = msg;
		// If the error mentions force=true, offer the bypass
		if (/force\s*=\s*true/i.test(msg)) {
			if (confirm(__("Undo bị chặn do có bản ghi ngoài batch tham chiếu. Bỏ qua bằng force=true? Các bản ghi ngoài có thể trỏ tới doc đã hủy."))) {
				try {
					await store.startUndo(false, true);
					error.value = null;
					setTimeout(refresh, 800);
				} catch (e2) {
					error.value = e2.message || String(e2);
				}
			}
		}
	} finally {
		busy.value = false;
	}
}

// Item 2 — pipeline recovery: typed-confirm dialogs
function _confirmThenCall({ title, intro, action_label, danger, run, label }) {
	const batch = store.batch_name;
	if (!batch) return;
	const Dialog = window.frappe?.ui?.Dialog;
	if (!Dialog) {
		// Fallback to native prompt if frappe.ui.Dialog isn't available
		const typed = window.prompt(`${intro}\n\n${__("Gõ chính xác mã batch")}: ${batch}`);
		if (typed === batch) { _runRecovery(run, label, typed); }
		return;
	}
	const d = new Dialog({
		title: __(title),
		fields: [
			{ fieldtype: "HTML", options:
				`<p style="margin-bottom:8px">${intro}</p>
				 <p style="margin:0;font-size:12px;color:#6b7280">${__("Gõ chính xác mã batch để xác nhận:")} <code style="background:#f3f4f6;padding:2px 6px;border-radius:3px">${batch}</code></p>` },
			{ fieldtype: "Data", fieldname: "confirm_token", reqd: 1,
			  description: __("Phải gõ chính xác, không thừa khoảng trắng.") },
		],
		primary_action_label: __(action_label),
		primary_action: (values) => {
			if (values.confirm_token !== batch) {
				frappe.msgprint({
					title: __("Mã không khớp"),
					message: __("Vui lòng gõ chính xác mã batch ({0}).").replace("{0}", batch),
					indicator: "red",
				});
				return;
			}
			d.hide();
			_runRecovery(run, label, values.confirm_token);
		},
	});
	// Apply danger styling to the primary button after render
	if (danger) {
		setTimeout(() => {
			d.get_primary_btn?.()?.removeClass("btn-primary").addClass("btn-danger");
		}, 50);
	}
	d.show();
}

async function _runRecovery(run, label, confirm_token) {
	error.value = null;
	recoveryResult.value = null;
	recoveryResultLabel.value = label;
	busy.value = true;
	try {
		const r = await run(confirm_token);
		recoveryResult.value = r;
		setTimeout(refresh, 800);
	} catch (e) {
		error.value = e.message || String(e);
	} finally {
		busy.value = false;
	}
}

function onCancelPhase4() {
	_confirmThenCall({
		title: "Hủy Phase 4 — chạy reverse pipeline",
		intro: __("Sẽ cancel mọi doc Misa-imported đã submit (PE → PI → SI → JE → SE). " +
				  "Doc đã hủy ở trạng thái docstatus=2; có thể xóa tiếp bằng nút Xóa nháp Phase 4. " +
				  "Phase 0 (OB JE / Asset / Inventory) KHÔNG bị ảnh hưởng."),
		action_label: "Hủy Phase 4",
		danger: true,
		label: __("Kết quả hủy Phase 4"),
		run: (t) => store.cancelPhase4(t),
	});
}

function onDeletePhase4() {
	_confirmThenCall({
		title: "Xóa nháp Phase 4 — dọn dẹp",
		intro: __("Sẽ xóa mọi doc Misa-imported có docstatus=0 (nháp) HOẶC docstatus=2 (đã hủy). " +
				  "Doc đã submit (docstatus=1) sẽ được BỎ QUA — phải Hủy trước. " +
				  "Phase 0 KHÔNG bị ảnh hưởng."),
		action_label: "Xóa nháp",
		danger: true,
		label: __("Kết quả xóa nháp Phase 4"),
		run: (t) => store.deletePhase4(t),
	});
}

onMounted(() => {
	refresh();
	fetchVoucherProgress();
	document.addEventListener("click", _onDocumentClick);
	// Voucher submit progress polls every 5s — only signal during long
	// PI/PE submit phase when row.status is frozen. Backoff on failure
	// to 30s so a bench restart doesn't spam console errors.
	const scheduleNext = () => {
		if (voucherProgressTimer) clearTimeout(voucherProgressTimer);
		voucherProgressTimer = setTimeout(async () => {
			if (["POSTING", "REVERSING", "POSTED"].includes(store.status)) {
				const ok = await fetchVoucherProgress();
				_voucher_poll_interval = ok ? 5000 : Math.min(_VOUCHER_POLL_MAX, _voucher_poll_interval * 2);
			}
			scheduleNext();
		}, _voucher_poll_interval);
	};
	scheduleNext();
	// Subscribe to post/undo progress
	if (window.frappe?.realtime?.on) {
		const handler = (payload) => {
			if (payload?.batch && payload.batch !== store.batch_name) return;
			refresh();
			fetchVoucherProgress();
		};
		frappe.realtime.on("misa_migration:post_progress", handler);
		frappe.realtime.on("misa_migration:undo_progress", handler);
		realtimeOff = () => {
			frappe.realtime.off?.("misa_migration:post_progress", handler);
			frappe.realtime.off?.("misa_migration:undo_progress", handler);
		};
	}
});

onBeforeUnmount(() => {
	if (realtimeOff) realtimeOff();
	if (voucherProgressTimer) { clearTimeout(voucherProgressTimer); voucherProgressTimer = null; }
	document.removeEventListener("click", _onDocumentClick);
});

watch(() => store.status, () => { refresh(); });
</script>

<style scoped>
.post-step .card {
	background: var(--card-bg, #fff);
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 8px;
	padding: 20px;
}
.header-row { display: flex; justify-content: space-between; align-items: flex-start; }
h3 { margin: 0 0 4px; font-size: 16px; }
.muted { color: var(--text-muted, #888); font-size: 13px; margin: 0; }
.error {
	margin: 12px 0; padding: 8px 12px;
	background: #fef2f2; color: #991b1b;
	border-radius: 4px; font-size: 13px;
}

.status-badge {
	display: inline-block;
	padding: 4px 12px;
	border-radius: 12px;
	font-size: 12px;
	font-weight: 600;
	background: var(--gray-200, #e5e7eb);
}
.status-badge.reviewed { background: #dbeafe; color: #1e40af; }
.status-badge.posting { background: #fde68a; color: #92400e; }
.status-badge.posted { background: #10b981; color: white; }
.status-badge.reversing { background: #fde68a; color: #92400e; }
.status-badge.reversed { background: #fed7aa; color: #c2410c; }

.preflight { margin: 16px 0; }
.metrics { display: flex; gap: 12px; margin-bottom: 12px; }
.metric {
	flex: 1; padding: 16px; border-radius: 8px; text-align: center;
}
.metric-n { font-size: 28px; font-weight: 600; }
.metric-label { font-size: 12px; color: var(--text-muted, #888); margin-top: 4px; }
.metric.ready { background: #ecfdf5; color: #065f46; }
.metric.conflict { background: #fff7ed; color: #c2410c; }
.metric.invalid { background: #fef2f2; color: #991b1b; }

.blocked-list, .warning-list {
	padding: 10px 14px;
	border-radius: 6px;
	font-size: 13px;
	margin: 8px 0;
}
.blocked-list { background: #fef2f2; color: #991b1b; }
.warning-list { background: #fffbeb; color: #92400e; }
.blocked-list ul, .warning-list ul { margin: 4px 0 0; padding-left: 18px; }

.post-progress-table {
	width: 100%; border-collapse: collapse; margin: 16px 0;
}
.post-progress-table th, .post-progress-table td {
	padding: 6px 8px; border-bottom: 1px solid var(--border-color, #e5e7eb);
	text-align: left; font-size: 12px;
}
.post-progress-table th { background: var(--bg-light-gray, #f9fafb); font-weight: 500; }
.post-progress-table .num { text-align: right; }
.posted-n { color: #065f46; font-weight: 600; }
.failed-n { color: #991b1b; font-weight: 600; }

.actions { margin-top: 16px; display: flex; gap: 10px; align-items: center; }
.btn-danger {
	background: #dc2626; color: white; padding: 6px 14px;
	border: none; border-radius: 4px; cursor: pointer;
}
.btn-danger:disabled { opacity: 0.5; cursor: not-allowed; }
.spinner { display: inline-block; animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0); } to { transform: rotate(360deg); } }
.done-msg {
	padding: 10px 14px;
	background: #ecfdf5;
	color: #065f46;
	border-radius: 6px;
	font-size: 13px;
}

/* Per-entity progress bars (C14) */
.entity-progress {
	margin: 14px 0;
	display: flex; flex-direction: column; gap: 8px;
}
.entity-row { display: flex; flex-direction: column; gap: 3px; }
.entity-row-head {
	display: flex; justify-content: space-between;
	font-size: 12px; color: var(--text-muted, #6b7280);
}
.entity-name { font-weight: 500; color: #111827; }
.entity-fraction { color: #4b5563; }
.entity-fraction .failed-n { color: #991b1b; margin-left: 4px; }
.entity-fraction .exists-n { color: #6b7280; margin-left: 4px; font-size: 11px; }

/* Algorithm explainer panel */
.post-explainer {
	margin: 12px 0 14px;
	padding: 10px 14px;
	background: #f5f3ff;
	border: 1px solid #ddd6fe;
	border-radius: 6px;
	font-size: 13px;
}
.post-explainer summary {
	cursor: pointer;
	font-weight: 500;
	color: #5b21b6;
	padding: 2px 0;
}
.post-explainer summary:hover { color: #4c1d95; }
.post-explainer-body {
	margin-top: 10px;
	padding-top: 10px;
	border-top: 1px solid #ddd6fe;
}
.post-explainer-body > p {
	margin: 0 0 12px;
	line-height: 1.55;
	color: #1f2937;
}
.post-explainer-tasks {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 10px 14px;
}
@media (max-width: 1100px) {
	.post-explainer-tasks { grid-template-columns: 1fr; }
}
.post-explainer-tasks .task-item {
	background: white;
	padding: 8px 10px;
	border-radius: 4px;
	border-left: 3px solid #8b5cf6;
}
.post-explainer-tasks .task-item strong {
	display: block;
	color: #5b21b6;
	font-size: 12px;
	margin-bottom: 4px;
}
.post-explainer-tasks .task-item p {
	margin: 0;
	font-size: 11.5px;
	line-height: 1.5;
	color: #4b5563;
}
.post-explainer-perf {
	margin-top: 12px;
	padding: 10px 12px;
	background: #ecfdf5;
	border: 1px solid #a7f3d0;
	border-radius: 4px;
	font-size: 12px;
}
.post-explainer-perf > strong { color: #065f46; font-size: 13px; }
.post-explainer-perf ul {
	margin: 6px 0 0;
	padding-left: 18px;
	line-height: 1.6;
	color: #065f46;
}
.post-explainer-perf li { margin-bottom: 2px; }

/* Post-Migration Health Check card */
.health-check-card {
	margin-top: 18px;
	padding: 14px 16px;
	background: #f0fdf4;
	border: 1px solid #86efac;
	border-radius: 8px;
}
.hc-head {
	display: flex; align-items: center; justify-content: space-between;
	margin-bottom: 8px;
}
.hc-head h4 { margin: 0; color: #14532d; font-size: 15px; }
.hc-intro {
	margin: 0 0 12px;
	font-size: 12px;
	color: #4b5563;
	line-height: 1.5;
}

.hc-balance {
	background: white;
	border: 1px solid #d1fae5;
	border-radius: 6px;
	padding: 10px 14px;
	margin-bottom: 12px;
	font-variant-numeric: tabular-nums;
}
.bal-row {
	display: flex; justify-content: space-between;
	padding: 4px 0;
	font-size: 13px;
	border-bottom: 1px dotted #e5e7eb;
}
.bal-row:last-child { border-bottom: none; }
.bal-row.total { font-size: 14px; padding-top: 8px; margin-top: 4px; border-top: 1px solid #d1fae5; }
.bal-row .balanced { color: #047857; font-weight: 700; font-size: 18px; }
.bal-row .imbalanced { color: #dc2626; font-weight: 700; font-size: 18px; }

.hc-ok {
	padding: 12px;
	background: white;
	border: 1px solid #d1fae5;
	border-radius: 4px;
	color: #047857;
	font-size: 13px;
	text-align: center;
}

.hc-anomalies { background: white; border-radius: 4px; }
.hc-summary-bar {
	padding: 8px 12px;
	background: #fef2f2;
	border: 1px solid #fecaca;
	border-radius: 4px 4px 0 0;
	display: flex; justify-content: space-between; align-items: baseline;
	font-size: 13px;
	color: #991b1b;
}

.anomaly-row {
	border: 1px solid #e5e7eb;
	border-top: none;
	font-size: 12.5px;
}
.anomaly-row[open] { background: #fffbeb; }
.anomaly-row.sev-high[open] { background: #fef2f2; }
.anomaly-row summary {
	padding: 8px 12px;
	cursor: pointer;
	display: flex; justify-content: space-between; align-items: baseline;
	gap: 12px;
}
.anomaly-row summary:hover { background: #f9fafb; }
.anom-name { font-weight: 500; color: #111827; }
.anom-net { font-variant-numeric: tabular-nums; color: #dc2626; }

.anom-body { padding: 8px 14px 12px; border-top: 1px dashed #e5e7eb; }
.anom-section { margin-bottom: 8px; }
.anom-section strong { color: #374151; font-size: 12px; }
.anom-section ul { margin: 4px 0 0; padding-left: 18px; line-height: 1.5; color: #4b5563; }
.anom-section li { margin-bottom: 3px; }
.anom-section li.sev-high::marker { color: #dc2626; }
.sev-badge {
	display: inline-block;
	min-width: 50px;
	padding: 1px 5px;
	font-size: 10px;
	font-weight: 600;
	text-transform: uppercase;
	text-align: center;
	border-radius: 3px;
	margin-right: 6px;
}
li.sev-high .sev-badge { background: #fef2f2; color: #991b1b; }
li.sev-medium .sev-badge { background: #fffbeb; color: #92400e; }
li.sev-info .sev-badge { background: #eff6ff; color: #1e40af; }
.entity-bar {
	position: relative;
	height: 8px;
	background: #e5e7eb;
	border-radius: 4px;
	overflow: hidden;
}
.entity-bar > span {
	display: block;
	position: absolute;
	top: 0; bottom: 0;
	transition: width 0.3s ease;
}
.entity-bar-posted { left: 0; background: #10b981; }
.entity-bar-failed { right: 0; background: #ef4444; }

.counts-table-collapse { margin-top: 8px; font-size: 12px; }
.counts-table-collapse summary {
	cursor: pointer; padding: 4px 0;
	color: var(--text-muted, #6b7280);
}
.counts-table-collapse summary:hover { color: #111827; }

.dot { font-size: 14px; line-height: 1; vertical-align: middle; margin-left: 4px; }
.dot.block { color: #991b1b; }
.dot.warn  { color: #c2410c; }
.dot.ok    { color: #10b981; }

.recovery-collapse {
	margin-top: 16px;
	padding: 12px 14px;
	background: #fafbfc;
	border: 1px dashed var(--border-color, #e5e7eb);
	border-radius: 6px;
	font-size: 13px;
}
.recovery-collapse summary {
	cursor: pointer;
	font-weight: 500;
	color: #4b5563;
}
.recovery-collapse summary:hover { color: #111827; }
.recovery-help { margin: 8px 0 10px; font-size: 12px; }
.recovery-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.btn-warning {
	background: #f59e0b; color: white; padding: 6px 14px;
	border: none; border-radius: 4px; cursor: pointer;
}
.btn-warning:disabled { opacity: 0.5; cursor: not-allowed; }
.recovery-result {
	margin-top: 10px;
	padding: 8px 10px;
	background: #f3f4f6;
	border-radius: 4px;
	font-size: 12px;
}
.recovery-result pre {
	margin: 4px 0 0;
	font-size: 11px;
	max-height: 220px;
	overflow: auto;
	background: white;
	padding: 6px;
	border-radius: 4px;
}

/* UX Gap 7 — Phase 0 prerequisite check panel */
.phase-0-panel {
	margin: 12px 0;
	padding: 10px 12px;
	border-radius: 6px;
	border: 1px solid var(--border-color, #e5e7eb);
}
.phase-0-panel.panel-ok      { background: #ecfdf5; border-color: #a7f3d0; }
.phase-0-panel.panel-warn    { background: #fffbeb; border-color: #fde68a; }
.phase-0-panel.panel-block   { background: #fef2f2; border-color: #fecaca; }
.phase-0-table {
	width: 100%;
	margin-top: 8px;
	border-collapse: collapse;
	font-size: 12px;
}
.phase-0-table th, .phase-0-table td {
	padding: 5px 8px;
	border-bottom: 1px solid var(--border-color, #e5e7eb);
	text-align: left;
	vertical-align: top;
}
.phase-0-table th { font-weight: 500; background: rgba(0,0,0,0.03); }
.phase-0-pass { color: #065f46; }
.phase-0-block td { color: #991b1b; }
.phase-0-warn td { color: #92400e; }
.level-badge {
	display: inline-block;
	min-width: 18px;
	text-align: center;
	font-weight: 600;
}
.level-badge.lvl-block { color: #991b1b; }
.level-badge.lvl-warn  { color: #c2410c; }
.hint-cell {
	max-width: 380px;
	white-space: normal;
	font-size: 11px;
	line-height: 1.4;
	color: var(--text-muted, #6b7280);
}

/* Phase-grouped progress stack — adds a header per phase to make the import order
   readable. Live activity ticker sits above. */
.live-activity {
	margin: 12px 0;
	padding: 8px 12px;
	background: #fffbeb;
	border-left: 3px solid #f59e0b;
	border-radius: 4px;
	font-size: 13px;
	color: #78350f;
	display: flex; align-items: center; gap: 8px;
}
.live-dot { font-size: 14px; }
.live-text { font-weight: 500; }

.phase-progress-stack { margin: 16px 0; display: flex; flex-direction: column; gap: 14px; }
.phase-block {
	padding: 10px 12px;
	background: var(--bg-light-gray, #fafbfc);
	border: 1px solid var(--border-color, #e5e7eb);
	border-radius: 6px;
}
.phase-header {
	display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;
	gap: 6px; margin-bottom: 8px;
	padding-bottom: 6px; border-bottom: 1px solid var(--border-color, #e5e7eb);
}
.phase-title { font-weight: 600; color: #111827; font-size: 13px; }
.phase-subtitle { font-size: 11px; color: var(--text-muted, #6b7280); flex-basis: 100%; }
.phase-summary { font-size: 12px; color: #374151; font-variant-numeric: tabular-nums; }

/* Per-row state markers — spinner / check / queue dot in front of the label */
.row-spinner { display: inline-block; animation: spin 1.4s linear infinite; color: #f59e0b; font-weight: 700; margin-right: 4px; }
.row-check { color: #10b981; font-weight: 700; margin-right: 4px; }
.row-queue { color: #9ca3af; margin-right: 4px; }
.entity-row.in-flight .entity-name { color: #78350f; }
.entity-row.done .entity-name { color: #047857; }

.voucher-submit-progress {
	margin: 16px 0;
	padding: 10px 12px;
	background: #eff6ff;
	border: 1px solid #bfdbfe;
	border-radius: 6px;
}
.voucher-submit-progress .phase-header { border-bottom-color: #bfdbfe; }
.voucher-submit-progress .phase-title { color: #1e3a8a; }

/* Failed-link in detail table — click to open tooltip */
.failed-link {
	color: #991b1b !important;
	text-decoration: underline dotted;
	cursor: pointer;
	font-weight: 600;
}
.failed-link:hover { color: #7f1d1d !important; text-decoration: underline; }
.failed-link-icon { font-size: 10px; margin-left: 2px; opacity: 0.7; }

.failed-tooltip {
	position: absolute;
	width: 480px;
	max-height: 520px;
	overflow-y: auto;
	background: white;
	border: 1px solid var(--border-color, #d1d5db);
	border-radius: 6px;
	box-shadow: 0 8px 24px rgba(0,0,0,0.15);
	padding: 12px 14px;
	z-index: 1000;
	font-size: 12px;
}
.failed-tooltip .ft-head {
	display: flex; align-items: center; gap: 8px;
	padding-bottom: 8px;
	border-bottom: 1px solid #e5e7eb;
	margin-bottom: 8px;
}
.failed-tooltip .ft-close {
	margin-left: auto;
	background: transparent;
	border: none;
	cursor: pointer;
	font-size: 18px;
	color: #6b7280;
	padding: 0 4px;
	line-height: 1;
}
.failed-tooltip .ft-close:hover { color: #111827; }
.failed-tooltip .ft-loading,
.failed-tooltip .ft-empty {
	padding: 16px;
	text-align: center;
	color: var(--text-muted, #6b7280);
}
.failed-tooltip .ft-list {
	margin: 0; padding-left: 18px;
	display: flex; flex-direction: column; gap: 10px;
}
.failed-tooltip .ft-list > li {
	border-bottom: 1px dashed #e5e7eb;
	padding-bottom: 8px;
}
.failed-tooltip .ft-list > li:last-child { border-bottom: none; }
.ft-err-head {
	display: flex; align-items: baseline; gap: 6px;
	margin-bottom: 4px;
}
.ft-err-n {
	display: inline-block;
	min-width: 38px;
	padding: 1px 6px;
	background: #fef2f2;
	color: #991b1b;
	border-radius: 3px;
	font-weight: 700;
	font-size: 11px;
	text-align: center;
}
.ft-err-text {
	font-family: ui-monospace, monospace;
	font-size: 11px;
	line-height: 1.4;
	color: #4b5563;
	word-break: break-word;
}
.ft-action {
	margin: 4px 0 4px 44px;
	padding: 6px 8px;
	background: #ecfeff;
	border-left: 2px solid #06b6d4;
	border-radius: 2px;
	font-size: 11px;
	line-height: 1.4;
}
.ft-action strong { color: #155e75; }
.ft-samples {
	margin: 4px 0 0 44px;
	display: flex; flex-wrap: wrap; gap: 4px;
	font-size: 10px;
}
.ft-samples code {
	background: #f3f4f6;
	padding: 1px 4px;
	border-radius: 2px;
	color: #374151;
}
.ft-actions {
	margin-top: 8px;
	padding-top: 8px;
	border-top: 1px solid #e5e7eb;
	display: flex; justify-content: flex-end;
}
</style>
