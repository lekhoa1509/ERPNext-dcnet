<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <!-- Header -->
      <div class="modal-header">
        <div class="header-icon">📝</div>
        <div class="header-content">
          <h2>Tạo tờ khai mới</h2>
          <p>Chọn loại tờ khai và kỳ kê khai</p>
        </div>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>

      <!-- Body -->
      <div class="modal-body">
        <!-- Company -->
        <div class="form-group">
          <label class="form-label">
            <span class="label-icon">🏢</span>
            Công ty
          </label>
          <select v-model="form.company" class="form-select" required>
            <option value="">Chọn công ty...</option>
            <option v-for="c in companies" :key="c.name" :value="c.name">
              {{ c.company_name }}
            </option>
          </select>
        </div>

        <!-- Declaration Type -->
        <div class="form-group">
          <label class="form-label">
            <span class="label-icon">📋</span>
            Loại tờ khai
          </label>
          <div class="type-grid">
            <button
              v-for="dt in declarationTypes"
              :key="dt.code"
              type="button"
              class="type-option"
              :class="{ active: form.declaration_type === dt.code }"
              @click="selectType(dt)"
            >
              <div class="type-code">{{ dt.code }}</div>
              <div class="type-name">{{ dt.name }}</div>
              <div class="type-period">{{ formatPeriod(dt.period) }}</div>
            </button>
          </div>
        </div>

        <!-- Period Type -->
        <div class="form-group" v-if="form.declaration_type">
          <label class="form-label">
            <span class="label-icon">📅</span>
            Kỳ kê khai
          </label>
          <div class="period-row">
            <select v-model="form.period_type" class="form-select period-type" @change="updatePeriodOptions">
              <option v-for="pt in periodTypes" :key="pt" :value="pt">{{ pt }}</option>
            </select>

            <select v-model="form.period" class="form-select period-value" v-if="form.period_type !== 'Năm'">
              <option v-for="p in periodOptions" :key="p.value" :value="p.value">
                {{ p.label }}
              </option>
            </select>

            <select v-model="form.year" class="form-select year-value">
              <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
            </select>
          </div>
        </div>

        <!-- Preview -->
        <div class="preview-card" v-if="isFormComplete">
          <div class="preview-title">Xem trước</div>
          <div class="preview-content">
            <div class="preview-item">
              <span class="preview-label">Tờ khai:</span>
              <span class="preview-value">{{ form.declaration_type }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">Kỳ:</span>
              <span class="preview-value">{{ previewPeriod }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">Công ty:</span>
              <span class="preview-value">{{ selectedCompanyName }}</span>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
          ⚠️ {{ errorMessage }}
        </div>
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button class="btn-cancel" @click="$emit('close')">Hủy</button>
        <button
          class="btn-create"
          :disabled="!isFormComplete || isCreating"
          @click="handleCreate"
        >
          <span v-if="isCreating" class="btn-spinner"></span>
          {{ isCreating ? 'Đang tạo...' : 'Tạo tờ khai' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

const emit = defineEmits(['close', 'created']);

// State
const companies = ref([]);
const declarationTypes = ref([]);
const isCreating = ref(false);
const errorMessage = ref('');

const form = ref({
  company: '',
  declaration_type: '',
  period_type: 'Quý',
  period: 1,
  year: new Date().getFullYear()
});

// Computed
const currentYear = new Date().getFullYear();
const years = Array.from({ length: 6 }, (_, i) => currentYear - i);

const periodTypes = computed(() => {
  const dt = declarationTypes.value.find(d => d.code === form.value.declaration_type);
  if (!dt) return ['Quý'];
  if (dt.period === 'monthly') return ['Tháng'];
  if (dt.period === 'quarterly') return ['Quý'];
  if (dt.period === 'yearly') return ['Năm'];
  return ['Tháng', 'Quý', 'Năm'];
});

const periodOptions = computed(() => {
  if (form.value.period_type === 'Tháng') {
    return Array.from({ length: 12 }, (_, i) => ({
      value: i + 1,
      label: `Tháng ${i + 1}`
    }));
  }
  if (form.value.period_type === 'Quý') {
    return [
      { value: 1, label: 'Quý 1 (T1-T3)' },
      { value: 2, label: 'Quý 2 (T4-T6)' },
      { value: 3, label: 'Quý 3 (T7-T9)' },
      { value: 4, label: 'Quý 4 (T10-T12)' }
    ];
  }
  return [];
});

const isFormComplete = computed(() => {
  return form.value.company &&
    form.value.declaration_type &&
    form.value.period_type &&
    form.value.year &&
    (form.value.period_type === 'Năm' || form.value.period);
});

const selectedCompanyName = computed(() => {
  const c = companies.value.find(c => c.name === form.value.company);
  return c?.company_name || form.value.company;
});

const previewPeriod = computed(() => {
  const f = form.value;
  if (f.period_type === 'Năm') return `Năm ${f.year}`;
  if (f.period_type === 'Quý') return `Quý ${f.period}/${f.year}`;
  return `Tháng ${f.period}/${f.year}`;
});

// Methods
const formatPeriod = (period) => {
  if (period === 'monthly') return 'Theo tháng';
  if (period === 'quarterly') return 'Theo quý';
  if (period === 'yearly') return 'Theo năm';
  return period;
};

const selectType = (dt) => {
  form.value.declaration_type = dt.code;
  // Auto-set period type based on declaration config
  if (dt.period === 'monthly') form.value.period_type = 'Tháng';
  else if (dt.period === 'quarterly') form.value.period_type = 'Quý';
  else if (dt.period === 'yearly') form.value.period_type = 'Năm';
};

const updatePeriodOptions = () => {
  form.value.period = form.value.period_type === 'Năm' ? 0 : 1;
};

const fetchCompanies = async () => {
  try {
    const response = await fetch(
      '/api/method/dcnet_apps.htkk.api.get_companies',
      { credentials: 'include' }
    );
    const data = await response.json();
    if (data.message) {
      companies.value = data.message;
      // Auto-select if only one company
      if (data.message.length === 1) {
        form.value.company = data.message[0].name;
      }
    }
  } catch (e) {
    console.error('Failed to fetch companies:', e);
  }
};

const fetchDeclarationTypes = async () => {
  try {
    const response = await fetch(
      '/api/method/dcnet_apps.htkk.api.get_supported_declarations',
      { credentials: 'include' }
    );
    const data = await response.json();
    if (data.message) {
      declarationTypes.value = data.message;
    }
  } catch (e) {
    console.error('Failed to fetch declaration types:', e);
  }
};

const handleCreate = async () => {
  if (!isFormComplete.value) return;

  isCreating.value = true;
  errorMessage.value = '';

  try {
    const response = await fetch(
      '/api/method/dcnet_apps.htkk.api.create_declaration',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          company: form.value.company,
          declaration_type: form.value.declaration_type,
          period_type: form.value.period_type,
          period: form.value.period_type === 'Năm' ? 0 : form.value.period,
          year: form.value.year
        })
      }
    );
    const data = await response.json();

    if (data.message?.status === 'success') {
      emit('created', data.message.name);
    } else if (data.message?.existing_name) {
      errorMessage.value = `${data.message.message} Mã: ${data.message.existing_name}`;
    } else {
      errorMessage.value = data.message?.message || 'Có lỗi xảy ra';
    }
  } catch (e) {
    console.error('Failed to create:', e);
    errorMessage.value = 'Lỗi kết nối server';
  } finally {
    isCreating.value = false;
  }
};

// Watch for period type changes
watch(() => form.value.declaration_type, () => {
  if (periodTypes.value.length === 1) {
    form.value.period_type = periodTypes.value[0];
  }
});

onMounted(async () => {
  await Promise.all([
    fetchCompanies(),
    fetchDeclarationTypes()
  ]);
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-container {
  background: white;
  width: 100%;
  max-width: 560px;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: modalPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modalPop {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Header */
.modal-header {
  padding: 24px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.header-icon {
  font-size: 32px;
}

.header-content h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.header-content p {
  margin: 4px 0 0;
  font-size: 13px;
  opacity: 0.8;
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Body */
.modal-body {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 10px;
}

.label-icon {
  font-size: 16px;
}

.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--border);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.form-select:hover {
  border-color: #c7d2fe;
}

.form-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* Type Grid */
.type-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.type-option {
  padding: 16px;
  border: 2px solid var(--border);
  border-radius: 12px;
  background: white;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}

.type-option:hover {
  border-color: #c7d2fe;
  background: #fafafa;
}

.type-option.active {
  border-color: #6366f1;
  background: #eef2ff;
}

.type-code {
  font-size: 16px;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 4px;
}

.type-name {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.type-period {
  font-size: 11px;
  font-weight: 600;
  color: #6366f1;
  background: #eef2ff;
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-block;
}

.type-option.active .type-period {
  background: white;
}

/* Period Row */
.period-row {
  display: grid;
  grid-template-columns: 1fr 1fr 100px;
  gap: 12px;
}

.period-type {
  grid-column: span 1;
}

/* Preview Card */
.preview-card {
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-top: 16px;
}

.preview-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.preview-item {
  display: flex;
  justify-content: space-between;
}

.preview-label {
  font-size: 13px;
  color: var(--text-muted);
}

.preview-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

/* Error Message */
.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 13px;
  margin-top: 16px;
}

/* Footer */
.modal-footer {
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-cancel {
  padding: 12px 24px;
  background: white;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f1f5f9;
}

.btn-create {
  padding: 12px 28px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-create:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.btn-create:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
