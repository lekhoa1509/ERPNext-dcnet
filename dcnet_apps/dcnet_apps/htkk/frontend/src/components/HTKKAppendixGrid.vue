<template>
  <div class="ag-theme-alpine h-full w-full">
    <ag-grid-vue
      class="h-full w-full"
      :columnDefs="columnDefs"
      :rowData="rowData"
      :pinnedBottomRowData="pinnedBottomRowData"
      :defaultColDef="defaultColDef"
      @grid-ready="onGridReady"
      :pagination="true"
      :paginationPageSize="20"
      :animateRows="true"
      :theme="'legacy'"
    >
    </ag-grid-vue>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue';
import { AgGridVue } from "ag-grid-vue3";
import { ModuleRegistry, AllCommunityModule } from 'ag-grid-community';

// Register AG Grid modules
ModuleRegistry.registerModules([ AllCommunityModule ]);

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const props = defineProps({
  appendixType: {
    type: String,
    required: true // e.g., 'PL 01-1/GTGT' or 'PL 01-2/GTGT'
  },
  data: {
    type: Array,
    default: () => []
  }
});

const gridApi = ref(null);

const onGridReady = (params) => {
  gridApi.value = params.api;
  params.api.sizeColumnsToFit();
};

const defaultColDef = {
  sortable: true,
  filter: true,
  resizable: true,
  minWidth: 100
};

const openDoc = (doctype, name) => {
  if (!doctype || !name) return;
  const route = `/app/${doctype.toLowerCase().replace(/ /g, '-')}/${name}`;
  window.parent.location.href = route;
};

const columnDefs = computed(() => {
  const common = [
    { headerName: "Mẫu số", field: "KHMSHDon", width: 120 },
    { headerName: "Ký hiệu", field: "KHHDon", width: 120 },
    { 
      headerName: "Số hóa đơn", 
      field: "SHDon", 
      width: 130,
      cellRenderer: params => {
        if (!params.value || params.node.rowPinned) return params.value;
        const name = params.data.doc_name;
        const doctype = params.data.doctype;
        return `<a class="doc-link" title="Mở chứng từ: ${name}">${params.value}</a>`;
      },
      onCellClicked: params => {
        if (params.node.rowPinned) return;
        openDoc(params.data.doctype, params.data.doc_name);
      }
    },
    { headerName: "Ngày lập", field: "NLap", width: 120 },
  ];

  if (props.appendixType === 'PL 01-1/GTGT') {
    return [
      ...common,
      { headerName: "Tên người mua", field: "NMua", flex: 1 },
      { headerName: "MST người mua", field: "MST", width: 150 },
      { 
        headerName: "Doanh thu (chưa thuế)", 
        field: "DThuaKCT", 
        width: 180,
        valueFormatter: params => formatCurrency(params.value),
        type: 'numericColumn'
      },
      { headerName: "Thuế suất", field: "TSuat", width: 100 },
      { 
        headerName: "Tiền thuế", 
        field: "TienThue", 
        width: 150,
        valueFormatter: params => formatCurrency(params.value),
        type: 'numericColumn'
      },
    ];
  } else if (props.appendixType === 'PL 01-2/GTGT') {
    return [
      ...common,
      { headerName: "Tên người bán", field: "NBan", flex: 1 },
      { headerName: "MST người bán", field: "MST", width: 150 },
      { 
        headerName: "Giá trị mua vào", 
        field: "DThuaKCT", 
        width: 180,
        valueFormatter: params => formatCurrency(params.value),
        type: 'numericColumn'
      },
      { headerName: "Thuế suất", field: "TSuat", width: 100 },
      { 
        headerName: "Tiền thuế", 
        field: "TienThue", 
        width: 150,
        valueFormatter: params => formatCurrency(params.value),
        type: 'numericColumn'
      },
    ];
  }
  return [];
});

const pinnedBottomRowData = computed(() => {
  if (!props.data || props.data.length === 0) return [];
  
  const totals = {
    KHMSHDon: '',
    KHHDon: '',
    SHDon: '',
    NLap: '',
    NMua: 'TỔNG CỘNG (Doanh thu -> Mục II):',
    NBan: 'TỔNG CỘNG (Giá trị -> [23]):',
    MST: '',
    DThuaKCT: 0,
    TSuat: '',
    TienThue: 0
  };

  props.data.forEach(row => {
    totals.DThuaKCT += (Number(row.DThuaKCT) || 0);
    totals.TienThue += (Number(row.TienThue) || 0);
  });

  // Specifically for Purchase VAT, note that tax maps to [24]
  if (props.appendixType === 'PL 01-2/GTGT') {
     totals.TSuat = 'Thuế -> [24]';
  } else {
     totals.TSuat = 'Thuế -> [28]';
  }

  return [totals];
});

const rowData = computed(() => props.data);

const formatCurrency = (val) => {
  if (val === undefined || val === null) return '0';
  return new Intl.NumberFormat('vi-VN').format(val);
};

// Auto-fit columns when data changes
watchEffect(() => {
  if (gridApi.value && props.data) {
    setTimeout(() => {
      gridApi.value.sizeColumnsToFit();
    }, 100);
  }
});
</script>

<style>
/* AG Grid Customizations */
.ag-theme-alpine {
  --ag-header-background-color: #f8fafc;
  --ag-header-foreground-color: #64748b;
  --ag-header-cell-font-weight: 700;
  --ag-header-cell-font-size: 13px;
  --ag-font-family: 'Outfit', sans-serif;
}

.ag-header-cell-label {
  justify-content: center;
}

.ag-cell {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.ag-numeric-cell {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
}

.ag-floating-bottom .ag-row {
  background-color: #f1f5f9 !important;
  font-weight: 800;
  color: #1e293b;
}

.ag-floating-bottom .ag-cell {
  border-top: 2px solid #cbd5e1 !important;
}

.doc-link {
  color: #1b4f72;
  text-decoration: underline;
  cursor: pointer;
  font-weight: 700;
  transition: color 0.2s;
}

.doc-link:hover {
  color: #0d2a3d;
}
</style>
