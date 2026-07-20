<template>
  <div class="max-w-5xl mx-auto p-8 bg-white shadow-2xl rounded-xl border border-slate-200 my-8">
    <!-- Loading State -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
      <div class="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      <p class="mt-4 text-slate-500 font-medium">Đang tải template...</p>
    </div>

    <template v-else>
      <!-- Header Section -->
      <header class="text-center mb-10 border-b border-slate-100 pb-8">
        <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight mb-2 uppercase">
          {{ template?.title || 'Tờ khai thuế' }}
        </h1>
        <p class="text-slate-500 font-medium">{{ template?.subtitle || '' }}</p>

        <div class="mt-6 flex justify-center items-center gap-8">
          <div class="text-left">
            <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Mẫu số</label>
            <span class="text-lg font-bold text-slate-800">{{ template?.declaration_type }}</span>
          </div>
          <div class="h-10 w-px bg-slate-200"></div>
          <div class="text-left">
            <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Kỳ tính thuế</label>
            <span class="text-lg font-bold text-slate-800">{{ data?.doc?.period }}</span>
          </div>
        </div>
      </header>

      <!-- Company Info -->
      <section class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">[04] Tên người nộp thuế:</label>
            <div class="text-lg font-medium text-slate-900 border-b-2 border-slate-100 py-1">{{ data?.company?.name }}</div>
          </div>
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-3">[05] Mã số thuế:</label>
            <div class="flex flex-row gap-1">
              <template v-for="(digit, i) in taxIdDigits" :key="i">
                <div class="w-10 h-10 flex items-center justify-center border-2 border-slate-200 rounded-md bg-slate-50 font-mono text-xl font-bold text-indigo-600 shadow-sm">
                  {{ digit }}
                </div>
              </template>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">[06] Tên đại lý thuế (nếu có):</label>
            <div class="text-lg font-medium text-slate-900 border-b-2 border-slate-100 py-1">---</div>
          </div>
        </div>
      </section>

      <!-- Main Table - Dynamic Rendering -->
      <div class="overflow-hidden border border-slate-200 rounded-xl shadow-sm mb-8">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200">
              <th class="px-4 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider w-12 text-center">STT</th>
              <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Chỉ tiêu</th>
              <th class="px-4 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider w-20 text-center">Mã số</th>
              <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Giá trị (VNĐ)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <template v-for="(section, sIdx) in template?.sections" :key="section.id">
              <!-- Section Header -->
              <tr class="bg-slate-50/50">
                <td class="px-4 py-3 text-sm font-bold text-slate-400 text-center">{{ getSectionLabel(sIdx) }}</td>
                <td colspan="3" class="px-6 py-3 text-sm font-bold text-slate-900 uppercase">{{ section.title }}</td>
              </tr>

              <!-- Section Indicators -->
              <template v-if="section.indicators">
                <tr v-for="(indicator, iIdx) in section.indicators" :key="indicator"
                    class="hover:bg-slate-50 transition-colors group"
                    :class="{ 'bg-indigo-50/30': isComputed(indicator), 'bg-amber-50/30': section.highlight }">
                  <td class="px-4 py-4 text-sm font-bold text-slate-400 text-center">{{ iIdx + 1 }}</td>
                  <td class="px-6 py-4 text-sm font-medium text-slate-700">
                    <div class="flex items-center gap-2">
                      {{ getFieldLabel(indicator) }}
                      <span v-if="getFieldFormula(indicator)" class="text-xs text-slate-400">
                        ({{ getFieldFormula(indicator) }})
                      </span>
                    </div>
                  </td>
                  <td class="px-4 py-4 text-center">
                    <span
                      class="inline-block py-1 px-2 rounded-md text-xs font-bold border cursor-pointer hover:ring-2 transition-all"
                      :class="isComputed(indicator) ? 'bg-rose-50 text-rose-700 border-rose-100 hover:ring-rose-300' : 'bg-indigo-50 text-indigo-700 border-indigo-100 hover:ring-indigo-300'"
                      @click="handleDrillDown(indicator)"
                    >
                      [{{ indicator.replace('ct', '') }}]
                    </span>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <!-- Computed field (readonly) -->
                    <div v-if="isComputed(indicator)" class="font-mono font-bold text-lg" :class="getValueClass(indicator)">
                      {{ formatCurrency(localIndicators[indicator]) }}
                    </div>
                    <!-- Boolean field -->
                    <input v-else-if="getFieldType(indicator) === 'boolean'"
                           type="checkbox"
                           v-model="localIndicators[indicator]"
                           class="w-5 h-5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500">
                    <!-- Number input -->
                    <div v-else class="relative group/input">
                      <input
                        type="number"
                        class="w-full text-right border border-slate-200 focus:ring-2 focus:ring-indigo-500 rounded px-2 py-1 bg-white shadow-sm font-mono font-bold"
                        :class="isManual(indicator) ? 'text-amber-600' : 'text-slate-900'"
                        v-model.number="localIndicators[indicator]"
                      >
                      <div v-if="isManual(indicator)" class="absolute -left-4 top-1/2 -translate-y-1/2 text-amber-500 text-xs" title="Giá trị đã được sửa tay">⚠️</div>
                    </div>
                  </td>
                </tr>
              </template>

              <!-- Subsections -->
              <template v-if="section.subsections">
                <template v-for="(sub, subIdx) in section.subsections" :key="sub.id">
                  <!-- Subsection Header -->
                  <tr class="hover:bg-slate-50 transition-colors" :class="{ 'pl-8': sub.indent }">
                    <td class="px-4 py-4 text-sm font-bold text-slate-400 text-center">{{ getRomanNumeral(subIdx + 1) }}</td>
                    <td class="px-6 py-4 text-sm font-bold text-slate-800" :class="{ 'pl-8': sub.indent }">
                      {{ sub.title }}
                    </td>
                    <td colspan="2"></td>
                  </tr>

                  <!-- Subsection Indicators -->
                  <tr v-for="(indicator, iIdx) in sub.indicators" :key="indicator"
                      class="hover:bg-slate-50 transition-colors group"
                      :class="{ 'bg-indigo-50/30': isComputed(indicator) || sub.computed, 'bg-rose-50/30': sub.highlight }">
                    <td class="px-4 py-4 text-sm font-bold text-slate-400 text-center"></td>
                    <td class="px-6 py-4 text-sm font-medium text-slate-700" :class="{ 'pl-12': sub.indent }">
                      <div class="flex items-center gap-2">
                        {{ getFieldLabel(indicator) }}
                      </div>
                    </td>
                    <td class="px-4 py-4 text-center">
                      <span
                        class="inline-block py-1 px-2 rounded-md text-xs font-bold border cursor-pointer hover:ring-2 transition-all"
                        :class="isComputed(indicator) ? 'bg-rose-50 text-rose-700 border-rose-100 hover:ring-rose-300' : 'bg-indigo-50 text-indigo-700 border-indigo-100 hover:ring-indigo-300'"
                        @click="handleDrillDown(indicator)"
                      >
                        [{{ indicator.replace('ct', '') }}]
                      </span>
                    </td>
                    <td class="px-6 py-4 text-right">
                      <!-- Computed field -->
                      <div v-if="isComputed(indicator)" class="font-mono font-bold text-lg" :class="getValueClass(indicator)">
                        {{ formatCurrency(localIndicators[indicator]) }}
                      </div>
                      <!-- Number input -->
                      <div v-else class="relative group/input">
                        <input
                          type="number"
                          class="w-full text-right border border-slate-200 focus:ring-2 focus:ring-indigo-500 rounded px-2 py-1 bg-white shadow-sm font-mono font-bold"
                          :class="isManual(indicator) ? 'text-amber-600' : 'text-slate-900'"
                          v-model.number="localIndicators[indicator]"
                        >
                        <div v-if="isManual(indicator)" class="absolute -left-4 top-1/2 -translate-y-1/2 text-amber-500 text-xs" title="Giá trị đã được sửa tay">⚠️</div>
                      </div>
                    </td>
                  </tr>
                </template>
              </template>
            </template>
          </tbody>
        </table>
      </div>

      <!-- Drill-down Modal -->
      <div v-if="drillDownIndicator" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[80vh] flex flex-col overflow-hidden">
          <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <div>
              <h3 class="font-bold text-slate-800">Chi tiết truy xuất nguồn: Chỉ tiêu [{{ drillDownIndicator.replace('ct', '') }}]</h3>
              <p class="text-xs text-slate-500">Danh sách các chứng từ gốc đóng góp vào giá trị này</p>
            </div>
            <button @click="drillDownIndicator = null" class="p-2 hover:bg-white rounded-full transition-colors text-slate-400">&times;</button>
          </div>
          <div class="flex-1 overflow-auto p-4 relative min-h-[200px]">
            <div v-if="isDrillingDown" class="absolute inset-0 z-10 bg-white/60 backdrop-blur-[2px] flex flex-col items-center justify-center gap-3">
              <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <p class="text-sm font-bold text-slate-500">Đang truy xuất dữ liệu nguồn...</p>
            </div>
            <table v-else class="w-full text-left border-collapse">
              <thead class="bg-slate-50 sticky top-0">
                <tr>
                  <th class="p-3 text-xs font-bold text-slate-500 uppercase">Mã / Số HĐ</th>
                  <th class="p-3 text-xs font-bold text-slate-500 uppercase">Ngày</th>
                  <th class="p-3 text-xs font-bold text-slate-500 uppercase">Đối tượng</th>
                  <th class="p-3 text-right text-xs font-bold text-slate-500 uppercase">G.Trị chưa thuế</th>
                  <th class="p-3 text-right text-xs font-bold text-slate-500 uppercase">Tiền Thuế</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="item in drillDownData" :key="item.name" class="hover:bg-slate-50 transition-colors">
                  <td class="p-3 text-sm font-medium text-indigo-600">{{ item.name }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ item.posting_date }}</td>
                  <td class="p-3 text-sm text-slate-600 truncate max-w-[200px]">{{ item.party || 'N/A' }}</td>
                  <td class="p-3 text-sm text-right font-mono">{{ formatCurrency(item.base_amount) }}</td>
                  <td class="p-3 text-sm text-right font-mono font-bold text-emerald-600">{{ formatCurrency(item.tax_amount) }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="!isDrillingDown && !drillDownData.length" class="p-12 text-center text-slate-400 italic">
              Không tìm thấy chứng từ gốc hoặc quy tắc không hỗ trợ truy xuất.
            </div>
          </div>
          <div class="p-4 bg-slate-50 border-t border-slate-100 flex justify-end">
            <button @click="drillDownIndicator = null" class="px-6 py-2 bg-white border border-slate-200 rounded-lg text-sm font-bold text-slate-600 hover:bg-slate-100 shadow-sm">Đóng</button>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-4 p-4 sticky bottom-0 bg-white/80 backdrop-blur-sm border-t border-slate-100">
        <button
          @click="$emit('cancel')"
          class="px-6 py-2.5 rounded-lg border border-slate-200 text-slate-600 font-bold hover:bg-slate-50 transition-all shadow-sm"
        >
          Hủy bỏ
        </button>
        <button
          @click="handleSave"
          class="px-8 py-2.5 rounded-lg bg-indigo-600 text-white font-bold hover:bg-indigo-700 transition-all shadow-md active:scale-95 flex items-center gap-2"
          :disabled="isSaving"
        >
          <span v-if="isSaving" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          {{ isSaving ? 'Đang lưu...' : 'Lưu tờ khai' }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  showCompare: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['save', 'cancel']);

// State
const isLoading = ref(true);
const template = ref(null);
const fieldMap = ref({});  // element -> field definition
const localIndicators = ref({});
const isSaving = ref(false);
const drillDownIndicator = ref(null);
const drillDownData = ref([]);
const isDrillingDown = ref(false);

// Computed
const taxIdDigits = computed(() => {
  const taxId = props.data?.company?.tax_id || '';
  return taxId.replace(/-/g, '').split('');
});

// Fetch template on mount
onMounted(async () => {
  try {
    // Fetch template schema
    const response = await fetch(
      `/api/method/dcnet_apps.htkk.api.spike.get_declaration_template?declaration_type=${encodeURIComponent(props.data?.doc?.type || '01/GTGT')}`,
      { credentials: 'include' }
    );
    const result = await response.json();

    if (result.message) {
      template.value = result.message;

      // Build field map for quick lookup
      for (const field of result.message.fields) {
        fieldMap.value[field.element] = field;
      }

      // Initialize indicators from data
      if (props.data?.indicators) {
        localIndicators.value = { ...props.data.indicators };
      }

      // Run initial calculation
      calculateAll();
    }
  } catch (e) {
    console.error('Failed to fetch template:', e);
  } finally {
    isLoading.value = false;
  }
});

// Watch for indicator changes and recalculate
watch(localIndicators, () => {
  calculateAll();
}, { deep: true });

// Auto-calculate based on formulas from template
function calculateAll() {
  if (!template.value?.formulas) return;

  const order = template.value.calculation_order || [];
  const formulas = template.value.formulas;

  for (const indicator of order) {
    const info = formulas[indicator];
    if (!info?.formula) continue;

    const key = `ct${indicator}`;
    const result = evaluateFormula(info.formula, info.condition);

    // Only update if it's a computed field
    if (result !== null) {
      localIndicators.value[key] = result;
    }
  }
}

function evaluateFormula(formula, condition) {
  try {
    // Replace [XX] with actual values
    let expr = formula.replace(/\[(\d+[a-z]?)\]/g, (match, num) => {
      const key = `ct${num}`;
      return `(${localIndicators.value[key] || 0})`;
    });

    // Evaluate expression
    let result = Function(`"use strict"; return (${expr})`)();

    // Apply conditions
    if (condition) {
      if (condition.includes('≥ 0') || condition.includes('>= 0')) {
        result = Math.max(0, result);
      } else if (condition.includes('< 0')) {
        result = result < 0 ? Math.abs(result) : 0;
      }
    }

    return result;
  } catch (e) {
    console.warn('Formula evaluation error:', formula, e);
    return null;
  }
}

// Helper functions
function getFieldLabel(indicator) {
  const field = fieldMap.value[indicator];
  return field?.label || indicator;
}

function getFieldFormula(indicator) {
  const field = fieldMap.value[indicator];
  if (!field?.formula) return null;
  return field.formula;
}

function getFieldType(indicator) {
  const field = fieldMap.value[indicator];
  return field?.data_type || 'number';
}

function isComputed(indicator) {
  const field = fieldMap.value[indicator];
  return !!field?.formula;
}

function isManual(indicator) {
  // Check if value was manually overridden
  const autoValue = props.data?.indicators_auto?.[indicator];
  const currentValue = localIndicators.value[indicator];
  return autoValue !== undefined && autoValue !== currentValue && !isComputed(indicator);
}

function getValueClass(indicator) {
  const value = localIndicators.value[indicator] || 0;
  // Highlight important fields
  if (['ct40', 'ct40a'].includes(indicator)) {
    return value > 0 ? 'text-rose-700' : 'text-slate-500';
  }
  if (['ct41', 'ct43'].includes(indicator)) {
    return value > 0 ? 'text-emerald-700' : 'text-slate-500';
  }
  return 'text-slate-900';
}

function getSectionLabel(idx) {
  const labels = ['A', 'B', 'C', 'D', 'E', 'F'];
  return labels[idx] || String(idx + 1);
}

function getRomanNumeral(num) {
  const numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];
  return numerals[num - 1] || String(num);
}

function formatCurrency(value) {
  if (value === null || value === undefined) return '0';
  return new Intl.NumberFormat('vi-VN').format(value);
}

// Drill-down
async function handleDrillDown(indicator) {
  drillDownIndicator.value = indicator;
  isDrillingDown.value = true;
  drillDownData.value = [];

  try {
    const code = indicator.replace('ct', '');
    const response = await fetch(
      `/api/method/dcnet_apps.htkk.api.spike.get_drilldown_data?declaration_id=${props.data.doc.name}&indicator_code=${code}`,
      { credentials: 'include' }
    );
    const result = await response.json();
    if (result.message) {
      drillDownData.value = result.message;
    }
  } catch (e) {
    console.error('Drill-down error:', e);
  } finally {
    isDrillingDown.value = false;
  }
}

// Save
async function handleSave() {
  isSaving.value = true;
  try {
    emit('save', localIndicators.value);
  } finally {
    isSaving.value = false;
  }
}
</script>
