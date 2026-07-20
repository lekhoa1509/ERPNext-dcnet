<template>
  <div class="declaration-list">
    <!-- Stats Cards -->
    <div class="stats-row" v-if="stats">
      <div class="stat-card">
        <div class="stat-value">{{ stats.total }}</div>
        <div class="stat-label">Tổng tờ khai</div>
      </div>
      <div class="stat-card draft">
        <div class="stat-value">{{ stats.by_status?.['Nháp'] || 0 }}</div>
        <div class="stat-label">Nháp</div>
      </div>
      <div class="stat-card pending">
        <div class="stat-value">{{ stats.by_status?.['Chờ duyệt'] || 0 }}</div>
        <div class="stat-label">Chờ duyệt</div>
      </div>
      <div class="stat-card exported">
        <div class="stat-value">{{ stats.by_status?.['Đã xuất'] || 0 }}</div>
        <div class="stat-label">Đã xuất</div>
      </div>
      <div class="stat-card submitted">
        <div class="stat-value">{{ stats.by_status?.['Đã nộp'] || 0 }}</div>
        <div class="stat-label">Đã nộp</div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-group">
        <select v-model="filters.company" @change="fetchDeclarations" class="filter-select">
          <option value="">Tất cả công ty</option>
          <option v-for="c in companies" :key="c.name" :value="c.name">
            {{ c.company_name }}
          </option>
        </select>

        <select v-model="filters.declaration_type" @change="fetchDeclarations" class="filter-select">
          <option value="">Tất cả loại</option>
          <option v-for="dt in declarationTypes" :key="dt.code" :value="dt.code">
            {{ dt.code }} - {{ dt.name }}
          </option>
        </select>

        <select v-model="filters.year" @change="fetchDeclarations" class="filter-select">
          <option value="">Tất cả năm</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>

        <select v-model="filters.status" @change="fetchDeclarations" class="filter-select">
          <option value="">Tất cả trạng thái</option>
          <option value="Nháp">Nháp</option>
          <option value="Chờ duyệt">Chờ duyệt</option>
          <option value="Đã xuất">Đã xuất</option>
          <option value="Đã nộp">Đã nộp</option>
        </select>
      </div>

      <button class="btn-create" @click="$emit('create')">
        <span class="btn-icon">+</span>
        Tạo tờ khai mới
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <span>Đang tải danh sách...</span>
    </div>

    <!-- Empty State -->
    <div v-else-if="declarations.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <h3>Chưa có tờ khai nào</h3>
      <p>Nhấn "Tạo tờ khai mới" để bắt đầu</p>
    </div>

    <!-- Declaration Grid -->
    <div v-else class="declaration-grid">
      <DeclarationCard
        v-for="decl in declarations"
        :key="decl.name"
        :declaration="decl"
        @view="$emit('view', decl.name)"
        @delete="handleDelete(decl)"
      />
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
      >
        ←
      </button>

      <template v-for="p in paginationRange" :key="p">
        <span v-if="p === '...'" class="page-ellipsis">...</span>
        <button
          v-else
          class="page-btn"
          :class="{ active: p === currentPage }"
          @click="goToPage(p)"
        >
          {{ p }}
        </button>
      </template>

      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
      >
        →
      </button>

      <span class="page-info">
        {{ (currentPage - 1) * pageSize + 1 }}-{{ Math.min(currentPage * pageSize, total) }} / {{ total }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import DeclarationCard from './DeclarationCard.vue';

const emit = defineEmits(['view', 'create', 'refresh']);

// State
const isLoading = ref(true);
const declarations = ref([]);
const companies = ref([]);
const declarationTypes = ref([]);
const stats = ref(null);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(12);
const totalPages = ref(1);

const filters = ref({
  company: '',
  declaration_type: '',
  year: '',
  status: ''
});

// Generate years (current year and 5 years back)
const currentYear = new Date().getFullYear();
const years = Array.from({ length: 6 }, (_, i) => currentYear - i);

// Pagination range
const paginationRange = computed(() => {
  const range = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 7) {
    for (let i = 1; i <= total; i++) range.push(i);
  } else {
    if (current <= 3) {
      range.push(1, 2, 3, 4, '...', total);
    } else if (current >= total - 2) {
      range.push(1, '...', total - 3, total - 2, total - 1, total);
    } else {
      range.push(1, '...', current - 1, current, current + 1, '...', total);
    }
  }
  return range;
});

// Fetch functions
const fetchDeclarations = async () => {
  isLoading.value = true;
  try {
    const params = new URLSearchParams({
      filters: JSON.stringify(filters.value),
      page: currentPage.value,
      page_size: pageSize.value
    });
    const response = await fetch(
      `/api/method/dcnet_apps.htkk.api.get_declarations?${params}`,
      { credentials: 'include' }
    );
    const data = await response.json();
    if (data.message) {
      declarations.value = data.message.declarations;
      total.value = data.message.total;
      totalPages.value = data.message.total_pages;
    }
  } catch (e) {
    console.error('Failed to fetch declarations:', e);
  } finally {
    isLoading.value = false;
  }
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

const fetchStats = async () => {
  try {
    const params = new URLSearchParams();
    if (filters.value.company) params.append('company', filters.value.company);
    if (filters.value.year) params.append('year', filters.value.year);

    const response = await fetch(
      `/api/method/dcnet_apps.htkk.api.get_dashboard_stats?${params}`,
      { credentials: 'include' }
    );
    const data = await response.json();
    if (data.message) {
      stats.value = data.message;
    }
  } catch (e) {
    console.error('Failed to fetch stats:', e);
  }
};

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    fetchDeclarations();
  }
};

const handleDelete = async (decl) => {
  if (!confirm(`Bạn có chắc muốn xóa tờ khai "${decl.name}"?`)) return;

  try {
    const response = await fetch(
      '/api/method/dcnet_apps.htkk.api.delete_declaration',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ declaration_id: decl.name })
      }
    );
    const data = await response.json();
    if (data.message?.status === 'success') {
      fetchDeclarations();
      fetchStats();
    } else {
      alert(data.message?.message || 'Có lỗi xảy ra');
    }
  } catch (e) {
    console.error('Failed to delete:', e);
    alert('Lỗi kết nối server');
  }
};

// Expose refresh method
defineExpose({
  refresh: () => {
    fetchDeclarations();
    fetchStats();
  }
});

onMounted(async () => {
  await Promise.all([
    fetchCompanies(),
    fetchDeclarationTypes()
  ]);
  await fetchDeclarations();
  await fetchStats();
});
</script>

<style scoped>
.declaration-list {
  padding: 24px;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border);
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  color: var(--text);
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-card.draft { border-left: 4px solid #64748b; }
.stat-card.pending { border-left: 4px solid #f59e0b; }
.stat-card.exported { border-left: 4px solid #0ea5e9; }
.stat-card.submitted { border-left: 4px solid #10b981; }

.stat-card.draft .stat-value { color: #64748b; }
.stat-card.pending .stat-value { color: #f59e0b; }
.stat-card.exported .stat-value { color: #0ea5e9; }
.stat-card.submitted .stat-value { color: #10b981; }

/* Filter Bar */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 10px 16px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  cursor: pointer;
  min-width: 160px;
  transition: all 0.2s ease;
}

.filter-select:hover {
  border-color: var(--secondary);
}

.filter-select:focus {
  outline: none;
  border-color: var(--secondary);
  box-shadow: 0 0 0 3px rgba(2, 136, 209, 0.1);
}

.btn-create {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-create:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.btn-create:active {
  transform: scale(0.98);
}

.btn-icon {
  font-size: 18px;
  font-weight: bold;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
  color: var(--text-muted);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 2px dashed var(--border);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px;
  color: var(--text);
  font-size: 20px;
}

.empty-state p {
  margin: 0;
  color: var(--text-muted);
}

/* Declaration Grid */
.declaration-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.page-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--secondary);
  color: var(--secondary);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn.active {
  background: var(--secondary);
  border-color: var(--secondary);
  color: white;
}

.page-ellipsis {
  padding: 0 8px;
  color: var(--text-muted);
}

.page-info {
  margin-left: 16px;
  font-size: 13px;
  color: var(--text-muted);
}
</style>
