<template>
  <div class="declaration-card" :class="statusClass" @click="$emit('view')">
    <!-- Header -->
    <div class="card-header">
      <div class="type-badge">{{ declaration.declaration_type }}</div>
      <div class="status-badge" :class="statusClass">
        <span class="status-dot"></span>
        {{ declaration.status }}
      </div>
    </div>

    <!-- Period Info -->
    <div class="card-period">
      <div class="period-label">{{ periodLabel }}</div>
      <div class="period-value">{{ declaration.year }}</div>
    </div>

    <!-- Company -->
    <div class="card-company">
      <span class="company-icon">🏢</span>
      {{ declaration.company_name || declaration.company }}
    </div>

    <!-- Dates -->
    <div class="card-dates">
      <div class="date-item">
        <span class="date-label">Từ:</span>
        <span class="date-value">{{ formatDate(declaration.from_date) }}</span>
      </div>
      <div class="date-item">
        <span class="date-label">Đến:</span>
        <span class="date-value">{{ formatDate(declaration.to_date) }}</span>
      </div>
    </div>

    <!-- Footer -->
    <div class="card-footer">
      <div class="card-meta">
        <span v-if="declaration.generated_at" class="meta-item exported">
          📤 {{ formatDateTime(declaration.generated_at) }}
        </span>
        <span v-else class="meta-item">
          ⏰ {{ formatDateTime(declaration.creation) }}
        </span>
      </div>

      <div class="card-actions" @click.stop>
        <button
          class="action-btn view"
          @click="$emit('view')"
          title="Xem chi tiết"
        >
          👁️
        </button>
        <button
          v-if="declaration.generated_xml"
          class="action-btn download"
          @click="downloadXml"
          title="Tải XML"
        >
          📥
        </button>
        <button
          v-if="declaration.status === 'Nháp'"
          class="action-btn delete"
          @click="$emit('delete')"
          title="Xóa"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  declaration: {
    type: Object,
    required: true
  }
});

defineEmits(['view', 'delete']);

const statusClass = computed(() => {
  const status = props.declaration.status;
  if (status === 'Nháp') return 'draft';
  if (status === 'Chờ duyệt') return 'pending';
  if (status === 'Đã xuất') return 'exported';
  if (status === 'Đã nộp') return 'submitted';
  return '';
});

const periodLabel = computed(() => {
  const d = props.declaration;
  if (d.period_type === 'Tháng') return `Tháng ${d.period}`;
  if (d.period_type === 'Quý') return `Quý ${d.period}`;
  return 'Năm';
});

const formatDate = (dateStr) => {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return date.toLocaleDateString('vi-VN');
};

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return date.toLocaleDateString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const downloadXml = () => {
  if (props.declaration.generated_xml) {
    window.open(props.declaration.generated_xml, '_blank');
  }
};
</script>

<style scoped>
.declaration-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.declaration-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  transition: all 0.2s ease;
}

.declaration-card.draft::before { background: #64748b; }
.declaration-card.pending::before { background: #f59e0b; }
.declaration-card.exported::before { background: #0ea5e9; }
.declaration-card.submitted::before { background: #10b981; }

.declaration-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.15);
  border-color: transparent;
}

.declaration-card:hover::before {
  width: 6px;
}

/* Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.type-badge {
  background: linear-gradient(135deg, #1a237e, #283593);
  color: white;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-badge.draft {
  background: #f1f5f9;
  color: #64748b;
}
.status-badge.draft .status-dot { background: #64748b; }

.status-badge.pending {
  background: #fef3c7;
  color: #d97706;
}
.status-badge.pending .status-dot { background: #f59e0b; }

.status-badge.exported {
  background: #e0f2fe;
  color: #0284c7;
}
.status-badge.exported .status-dot { background: #0ea5e9; }

.status-badge.submitted {
  background: #d1fae5;
  color: #059669;
}
.status-badge.submitted .status-dot { background: #10b981; }

/* Period */
.card-period {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 12px;
}

.period-label {
  font-size: 24px;
  font-weight: 800;
  color: var(--text);
}

.period-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-muted);
}

/* Company */
.card-company {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}

.company-icon {
  font-size: 16px;
}

/* Dates */
.card-dates {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 16px;
}

.date-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.date-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.date-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

/* Footer */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.card-meta {
  font-size: 11px;
  color: var(--text-muted);
}

.meta-item.exported {
  color: #0ea5e9;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-btn.view:hover {
  background: #eef2ff;
  border-color: #c7d2fe;
}

.action-btn.download:hover {
  background: #e0f2fe;
  border-color: #bae6fd;
}

.action-btn.delete:hover {
  background: #fef2f2;
  border-color: #fecaca;
}
</style>
