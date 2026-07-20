export default `
  <div v-if="auditLogOpen" class="crm-audit-overlay" @click.self="closeAuditLog" @keydown.esc="closeAuditLog">
    <section class="crm-audit-dialog" role="dialog" aria-modal="true" aria-labelledby="crm-audit-title" tabindex="-1">
      <header class="crm-audit-header">
        <div class="crm-audit-heading">
          <span class="crm-audit-heading-icon"><CRMIcon name="history" /></span>
          <div>
            <h2 id="crm-audit-title">Nhật ký</h2>
            <p>{{ auditLogData?.doctype_label || auditLogData?.doctype }}<template v-if="auditLogData?.name"> · {{ auditLogData.name }}</template></p>
          </div>
        </div>
        <div class="crm-audit-header-actions">
          <button class="icon-button" type="button" data-tooltip="Làm mới nhật ký" aria-label="Làm mới nhật ký" @click="refreshAuditLog" :disabled="auditLogLoading"><CRMIcon name="refresh" /></button>
          <button class="icon-button" type="button" data-tooltip="Đóng" aria-label="Đóng nhật ký" @click="closeAuditLog"><CRMIcon name="close" /></button>
        </div>
      </header>

      <div class="crm-audit-body">
        <div v-if="auditLogLoading" class="crm-audit-state">
          <span class="crm-audit-spinner"></span><strong>Đang tải nhật ký...</strong>
        </div>
        <div v-else-if="auditLogError" class="crm-audit-state crm-audit-state--error">
          <CRMIcon name="alert" /><strong>{{ auditLogError }}</strong>
          <button class="crm-button" type="button" @click="refreshAuditLog">Thử lại</button>
        </div>
        <div v-else-if="!auditLogEntries.length" class="crm-audit-state">
          <CRMIcon name="history" /><strong>Chưa có thay đổi nào</strong>
        </div>
        <ol v-else class="crm-audit-timeline">
          <li v-for="entry in auditLogEntries" :key="entry.name" class="crm-audit-entry">
            <span class="crm-audit-dot" :class="{ 'is-created': entry.kind === 'created', 'is-cancelled': entry.kind === 'activity_cancelled' }"><CRMIcon :name="entry.kind === 'created' ? 'plus' : entry.kind === 'commented' ? 'contact' : entry.kind === 'activity_cancelled' ? 'close' : entry.kind === 'activity_created' ? 'task' : 'history'" /></span>
            <article class="crm-audit-card">
              <div class="crm-audit-meta">
                <div class="crm-audit-actor-avatar">{{ (entry.actor_name || entry.actor || 'H').charAt(0).toUpperCase() }}</div>
                <div>
                  <strong>{{ entry.actor_name || entry.actor || 'Hệ thống' }}</strong>
                  <span>{{ entry.kind === 'created' ? 'đã tạo dữ liệu' : entry.kind === 'commented' ? 'đã ghi chú' : entry.kind === 'activity_cancelled' ? 'đã hủy hoạt động' : entry.kind === 'activity_created' ? 'đã tạo hoạt động' : 'đã cập nhật dữ liệu' }}</span>
                </div>
                <time>{{ formatAuditDate(entry.creation) }}</time>
              </div>
              <p v-if="entry.summary" class="crm-audit-summary">{{ entry.summary }}</p>
              <div v-if="entry.changes?.length" class="crm-audit-changes">
                <div v-for="(change, index) in entry.changes" :key="change.field + '-' + index" class="crm-audit-change">
                  <strong>{{ change.label }}</strong>
                  <div v-if="change.action === 'changed'" class="crm-audit-values">
                    <span class="is-old">{{ formatAuditValue(change.old_value) }}</span>
                    <span class="crm-audit-arrow">→</span>
                    <span class="is-new">{{ formatAuditValue(change.new_value) }}</span>
                  </div>
                  <span v-else class="crm-audit-row-action">{{ change.action === 'removed' ? 'Đã xóa một dòng' : change.action === 'added' ? 'Đã thêm một dòng' : 'Đã thay đổi dữ liệu dòng' }}</span>
                </div>
              </div>
            </article>
          </li>
        </ol>
      </div>
    </section>
  </div>
`;
