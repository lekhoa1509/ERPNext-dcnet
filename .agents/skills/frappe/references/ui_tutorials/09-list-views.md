# List Views Tutorial

## Overview

The ListView component in frappe-ui provides a powerful way to display tabular data with features like sorting, selection, grouping, and custom cell rendering. This tutorial covers building list views from basic tables to complex interactive displays.

## Basic ListView

### Simple Table

```vue
<template>
  <ListView
    :columns="columns"
    :rows="rows"
  />
</template>

<script setup>
import { ListView } from 'frappe-ui'

const columns = [
  { label: 'Name', key: 'name' },
  { label: 'Email', key: 'email' },
  { label: 'Status', key: 'status' }
]

const rows = [
  { name: 'John Doe', email: 'john@example.com', status: 'Active' },
  { name: 'Jane Smith', email: 'jane@example.com', status: 'Pending' },
  { name: 'Bob Wilson', email: 'bob@example.com', status: 'Inactive' }
]
</script>
```

## Column Configuration

### Column Options

```vue
<script setup>
import { ListView } from 'frappe-ui'

const columns = [
  {
    label: 'Customer',      // Display header
    key: 'customer_name',   // Data key
    width: '200px',         // Fixed width
    minWidth: '150px',      // Minimum width
    align: 'left',          // 'left' | 'center' | 'right'
    sortable: true,         // Enable sorting
    hidden: false           // Hide column
  },
  {
    label: 'Amount',
    key: 'grand_total',
    width: '120px',
    align: 'right',
    sortable: true,
    // Format cell value
    getValue: (row) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(row.grand_total)
    }
  },
  {
    label: 'Date',
    key: 'transaction_date',
    width: '120px',
    getValue: (row) => {
      return new Date(row.transaction_date).toLocaleDateString()
    }
  }
]
</script>
```

## ListView with Data Fetching

### Using List Resource

```vue
<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-xl font-bold">Customers</h1>
      <Button
        icon="refresh-cw"
        :loading="customers.loading"
        @click="customers.reload()"
      />
    </div>

    <ListView
      :columns="columns"
      :rows="customers.data || []"
      :loading="customers.loading"
      row-key="name"
    />

    <div class="flex justify-between items-center mt-4">
      <span class="text-sm text-gray-500">
        Showing {{ customers.data?.length || 0 }} customers
      </span>
      <div class="space-x-2">
        <Button
          label="Previous"
          :disabled="customers.start === 0"
          @click="customers.previous()"
        />
        <Button
          label="Next"
          :disabled="!customers.hasNextPage"
          @click="customers.next()"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { createListResource, ListView, Button } from 'frappe-ui'

const columns = [
  { label: 'ID', key: 'name', width: '120px' },
  { label: 'Customer Name', key: 'customer_name' },
  { label: 'Territory', key: 'territory', width: '150px' },
  { label: 'Type', key: 'customer_type', width: '120px' }
]

const customers = createListResource({
  doctype: 'Customer',
  fields: ['name', 'customer_name', 'territory', 'customer_type'],
  orderBy: 'creation desc',
  pageLength: 20,
  auto: true
})
</script>
```

## Custom Cell Rendering

### Using Cell Slot

```vue
<template>
  <ListView
    :columns="columns"
    :rows="orders"
    row-key="name"
  >
    <template #cell="{ column, row, value }">
      <!-- Status badge -->
      <template v-if="column.key === 'status'">
        <Badge :theme="getStatusTheme(value)">
          {{ value }}
        </Badge>
      </template>

      <!-- Customer with avatar -->
      <template v-else-if="column.key === 'customer'">
        <div class="flex items-center gap-2">
          <Avatar :label="value" size="sm" />
          <span>{{ value }}</span>
        </div>
      </template>

      <!-- Amount formatting -->
      <template v-else-if="column.key === 'grand_total'">
        <span class="font-mono">
          {{ formatCurrency(value) }}
        </span>
      </template>

      <!-- Actions column -->
      <template v-else-if="column.key === 'actions'">
        <div class="flex gap-1">
          <Button
            icon="eye"
            variant="ghost"
            size="sm"
            @click="viewOrder(row)"
          />
          <Button
            icon="edit"
            variant="ghost"
            size="sm"
            @click="editOrder(row)"
          />
          <Button
            icon="trash"
            variant="ghost"
            size="sm"
            theme="red"
            @click="deleteOrder(row)"
          />
        </div>
      </template>

      <!-- Default rendering -->
      <template v-else>
        {{ value }}
      </template>
    </template>
  </ListView>
</template>

<script setup>
import { ListView, Badge, Avatar, Button } from 'frappe-ui'

const columns = [
  { label: 'Order', key: 'name', width: '120px' },
  { label: 'Customer', key: 'customer' },
  { label: 'Status', key: 'status', width: '120px' },
  { label: 'Amount', key: 'grand_total', width: '120px', align: 'right' },
  { label: '', key: 'actions', width: '120px', align: 'right' }
]

const orders = [
  { name: 'SO-001', customer: 'John Doe', status: 'Draft', grand_total: 1500 },
  { name: 'SO-002', customer: 'Jane Smith', status: 'Submitted', grand_total: 2300 },
  { name: 'SO-003', customer: 'Bob Wilson', status: 'Completed', grand_total: 890 }
]

const getStatusTheme = (status) => {
  const themes = {
    'Draft': 'gray',
    'Submitted': 'blue',
    'Completed': 'green',
    'Cancelled': 'red'
  }
  return themes[status] || 'gray'
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value)
}

const viewOrder = (row) => console.log('View:', row.name)
const editOrder = (row) => console.log('Edit:', row.name)
const deleteOrder = (row) => console.log('Delete:', row.name)
</script>
```

## Row Selection

### Single and Multiple Selection

```vue
<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-xl font-bold">Tasks</h1>
      <div v-if="selectedRows.length" class="flex items-center gap-2">
        <span class="text-sm text-gray-500">
          {{ selectedRows.length }} selected
        </span>
        <Button
          label="Delete Selected"
          theme="red"
          @click="deleteSelected"
        />
      </div>
    </div>

    <ListView
      :columns="columns"
      :rows="tasks"
      row-key="name"
      :selection="true"
      v-model:selected="selectedRows"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ListView, Button, toast } from 'frappe-ui'

const columns = [
  { label: 'Task', key: 'subject' },
  { label: 'Priority', key: 'priority', width: '100px' },
  { label: 'Status', key: 'status', width: '120px' }
]

const tasks = [
  { name: 'TASK-001', subject: 'Complete documentation', priority: 'High', status: 'Open' },
  { name: 'TASK-002', subject: 'Review PR', priority: 'Medium', status: 'Open' },
  { name: 'TASK-003', subject: 'Deploy to staging', priority: 'Low', status: 'Completed' }
]

const selectedRows = ref([])

const deleteSelected = () => {
  toast({
    type: 'success',
    message: `Deleted ${selectedRows.value.length} tasks`
  })
  selectedRows.value = []
}
</script>
```

## Row Grouping

### Grouped Rows

```vue
<template>
  <ListView
    :columns="columns"
    :rows="groupedRows"
    row-key="name"
  />
</template>

<script setup>
import { computed } from 'vue'
import { ListView } from 'frappe-ui'

const columns = [
  { label: 'Item', key: 'item_name' },
  { label: 'Qty', key: 'qty', width: '80px', align: 'right' },
  { label: 'Rate', key: 'rate', width: '100px', align: 'right' },
  { label: 'Amount', key: 'amount', width: '120px', align: 'right' }
]

const items = [
  { name: '1', item_name: 'Widget A', qty: 5, rate: 100, amount: 500, category: 'Electronics' },
  { name: '2', item_name: 'Widget B', qty: 3, rate: 150, amount: 450, category: 'Electronics' },
  { name: '3', item_name: 'Gadget X', qty: 2, rate: 200, amount: 400, category: 'Hardware' },
  { name: '4', item_name: 'Gadget Y', qty: 4, rate: 75, amount: 300, category: 'Hardware' }
]

// Group items by category
const groupedRows = computed(() => {
  const groups = {}

  items.forEach(item => {
    if (!groups[item.category]) {
      groups[item.category] = {
        group: item.category,
        collapsed: false,
        rows: []
      }
    }
    groups[item.category].rows.push(item)
  })

  return Object.values(groups)
})
</script>
```

## Sorting

### Client-Side Sorting

```vue
<template>
  <ListView
    :columns="sortableColumns"
    :rows="sortedRows"
    row-key="name"
    @sort="handleSort"
  />
</template>

<script setup>
import { ref, computed } from 'vue'
import { ListView } from 'frappe-ui'

const columns = [
  { label: 'Name', key: 'name', sortable: true },
  { label: 'Amount', key: 'amount', sortable: true },
  { label: 'Date', key: 'date', sortable: true }
]

const rows = [
  { name: 'Item A', amount: 100, date: '2024-01-15' },
  { name: 'Item B', amount: 250, date: '2024-01-10' },
  { name: 'Item C', amount: 75, date: '2024-01-20' }
]

const sortKey = ref('name')
const sortOrder = ref('asc')

const sortableColumns = computed(() => {
  return columns.map(col => ({
    ...col,
    sortOrder: col.key === sortKey.value ? sortOrder.value : null
  }))
})

const sortedRows = computed(() => {
  return [...rows].sort((a, b) => {
    let aVal = a[sortKey.value]
    let bVal = b[sortKey.value]

    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase()
      bVal = bVal.toLowerCase()
    }

    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
})

const handleSort = ({ column }) => {
  if (sortKey.value === column.key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = column.key
    sortOrder.value = 'asc'
  }
}
</script>
```

### Server-Side Sorting

```vue
<template>
  <ListView
    :columns="columns"
    :rows="customers.data || []"
    :loading="customers.loading"
    row-key="name"
    @sort="handleSort"
  />
</template>

<script setup>
import { ref } from 'vue'
import { createListResource, ListView } from 'frappe-ui'

const sortField = ref('creation')
const sortOrder = ref('desc')

const columns = [
  { label: 'Name', key: 'customer_name', sortable: true },
  { label: 'Territory', key: 'territory', sortable: true },
  { label: 'Created', key: 'creation', sortable: true }
]

const customers = createListResource({
  doctype: 'Customer',
  fields: ['name', 'customer_name', 'territory', 'creation'],
  orderBy: `${sortField.value} ${sortOrder.value}`,
  auto: true
})

const handleSort = ({ column }) => {
  if (sortField.value === column.key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = column.key
    sortOrder.value = 'asc'
  }

  // Update resource and reload
  customers.update({
    orderBy: `${sortField.value} ${sortOrder.value}`
  })
}
</script>
```

## Empty State

### Custom Empty Message

```vue
<template>
  <ListView
    :columns="columns"
    :rows="filteredRows"
    row-key="name"
  >
    <template #empty>
      <div class="flex flex-col items-center py-12 text-gray-500">
        <FeatherIcon name="inbox" class="w-12 h-12 mb-4" />
        <p class="text-lg font-medium">No items found</p>
        <p class="text-sm">Try adjusting your search or filters</p>
        <Button
          label="Clear Filters"
          class="mt-4"
          @click="clearFilters"
        />
      </div>
    </template>
  </ListView>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ListView, Button, FeatherIcon } from 'frappe-ui'

const columns = [
  { label: 'Name', key: 'name' },
  { label: 'Status', key: 'status' }
]

const allRows = [
  { name: 'Item 1', status: 'Active' },
  { name: 'Item 2', status: 'Inactive' }
]

const searchQuery = ref('')
const statusFilter = ref('')

const filteredRows = computed(() => {
  return allRows.filter(row => {
    const matchesSearch = !searchQuery.value ||
      row.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = !statusFilter.value ||
      row.status === statusFilter.value
    return matchesSearch && matchesStatus
  })
})

const clearFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
}
</script>
```

## Complete Example

### Customer List with All Features

```vue
<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Customers</h1>
      <Button
        label="Add Customer"
        theme="blue"
        variant="solid"
        icon-left="plus"
        @click="showCreateDialog = true"
      />
    </div>

    <!-- Filters -->
    <div class="flex gap-4 mb-4">
      <TextInput
        v-model="searchQuery"
        placeholder="Search customers..."
        :debounce="300"
        class="w-64"
      >
        <template #prefix>
          <FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
        </template>
      </TextInput>

      <Select
        v-model="territoryFilter"
        :options="territoryOptions"
        placeholder="All Territories"
        class="w-48"
      />

      <Select
        v-model="typeFilter"
        :options="typeOptions"
        placeholder="All Types"
        class="w-48"
      />
    </div>

    <!-- Bulk Actions -->
    <div
      v-if="selectedRows.length"
      class="flex items-center gap-4 mb-4 p-3 bg-blue-50 rounded-lg"
    >
      <span class="text-sm font-medium">
        {{ selectedRows.length }} customers selected
      </span>
      <Button
        label="Export"
        size="sm"
        icon-left="download"
      />
      <Button
        label="Delete"
        size="sm"
        theme="red"
        icon-left="trash"
        @click="deleteSelected"
      />
    </div>

    <!-- List View -->
    <div class="border rounded-lg overflow-hidden">
      <ListView
        :columns="columns"
        :rows="customers.data || []"
        :loading="customers.loading"
        row-key="name"
        :selection="true"
        v-model:selected="selectedRows"
        @row-click="handleRowClick"
      >
        <template #cell="{ column, row, value }">
          <template v-if="column.key === 'customer_name'">
            <div class="flex items-center gap-3">
              <Avatar :label="value" size="sm" />
              <div>
                <p class="font-medium">{{ value }}</p>
                <p class="text-xs text-gray-500">{{ row.name }}</p>
              </div>
            </div>
          </template>

          <template v-else-if="column.key === 'customer_type'">
            <Badge :theme="row.customer_type === 'Company' ? 'blue' : 'green'">
              {{ value }}
            </Badge>
          </template>

          <template v-else-if="column.key === 'disabled'">
            <Badge :theme="value ? 'red' : 'green'">
              {{ value ? 'Disabled' : 'Active' }}
            </Badge>
          </template>

          <template v-else-if="column.key === 'actions'">
            <Dropdown
              :options="getRowActions(row)"
            >
              <Button icon="more-horizontal" variant="ghost" size="sm" />
            </Dropdown>
          </template>

          <template v-else>
            {{ value }}
          </template>
        </template>

        <template #empty>
          <div class="flex flex-col items-center py-12 text-gray-500">
            <FeatherIcon name="users" class="w-12 h-12 mb-4" />
            <p class="text-lg font-medium">No customers found</p>
            <Button
              label="Add your first customer"
              theme="blue"
              class="mt-4"
              @click="showCreateDialog = true"
            />
          </div>
        </template>
      </ListView>
    </div>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4">
      <span class="text-sm text-gray-500">
        Showing {{ customers.data?.length || 0 }} of {{ totalCount }} customers
      </span>
      <div class="flex gap-2">
        <Button
          icon="chevron-left"
          :disabled="customers.start === 0"
          @click="customers.previous()"
        />
        <Button
          icon="chevron-right"
          :disabled="!customers.hasNextPage"
          @click="customers.next()"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import {
  createListResource,
  ListView,
  Button,
  TextInput,
  Select,
  Badge,
  Avatar,
  Dropdown,
  FeatherIcon,
  toast
} from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()

const searchQuery = ref('')
const territoryFilter = ref('')
const typeFilter = ref('')
const selectedRows = ref([])
const showCreateDialog = ref(false)
const totalCount = ref(0)

const territoryOptions = [
  { label: 'All Territories', value: '' },
  { label: 'India', value: 'India' },
  { label: 'USA', value: 'USA' },
  { label: 'UK', value: 'UK' }
]

const typeOptions = [
  { label: 'All Types', value: '' },
  { label: 'Company', value: 'Company' },
  { label: 'Individual', value: 'Individual' }
]

const columns = [
  { label: 'Customer', key: 'customer_name' },
  { label: 'Type', key: 'customer_type', width: '120px' },
  { label: 'Territory', key: 'territory', width: '150px' },
  { label: 'Status', key: 'disabled', width: '100px' },
  { label: '', key: 'actions', width: '60px' }
]

const filters = computed(() => {
  const f = []
  if (searchQuery.value) {
    f.push(['customer_name', 'like', `%${searchQuery.value}%`])
  }
  if (territoryFilter.value) {
    f.push(['territory', '=', territoryFilter.value])
  }
  if (typeFilter.value) {
    f.push(['customer_type', '=', typeFilter.value])
  }
  return f
})

const customers = createListResource({
  doctype: 'Customer',
  fields: ['name', 'customer_name', 'customer_type', 'territory', 'disabled'],
  filters: filters.value,
  orderBy: 'creation desc',
  pageLength: 20,
  auto: true,
  onSuccess(data) {
    totalCount.value = data.length
  }
})

// Reload when filters change
watch(filters, () => {
  customers.update({ filters: filters.value })
})

const getRowActions = (row) => [
  {
    label: 'View',
    icon: 'eye',
    onClick: () => router.push(`/customers/${row.name}`)
  },
  {
    label: 'Edit',
    icon: 'edit',
    onClick: () => router.push(`/customers/${row.name}/edit`)
  },
  {
    label: row.disabled ? 'Enable' : 'Disable',
    icon: row.disabled ? 'check' : 'x',
    onClick: () => toggleStatus(row)
  },
  {
    label: 'Delete',
    icon: 'trash',
    onClick: () => deleteCustomer(row)
  }
]

const handleRowClick = (row) => {
  router.push(`/customers/${row.name}`)
}

const toggleStatus = async (row) => {
  customers.setValue.submit({
    name: row.name,
    disabled: row.disabled ? 0 : 1
  })
}

const deleteCustomer = (row) => {
  if (confirm(`Delete ${row.customer_name}?`)) {
    customers.delete.submit(row.name)
  }
}

const deleteSelected = () => {
  if (confirm(`Delete ${selectedRows.value.length} customers?`)) {
    // Delete each selected customer
    selectedRows.value.forEach(row => {
      customers.delete.submit(row.name)
    })
    selectedRows.value = []
  }
}
</script>
```

## Common Pitfalls

### 1. Missing row-key

**Problem:** Selection and updates don't work correctly.

**Solution:** Always provide a unique `row-key`:
```vue
<ListView row-key="name" :rows="rows" />
```

### 2. Slow Rendering with Large Lists

**Problem:** List becomes sluggish with many rows.

**Solution:** Use pagination or virtual scrolling:
```javascript
const customers = createListResource({
  pageLength: 50,  // Limit rows per page
  // ...
})
```

### 3. Cell Slot Not Rendering

**Problem:** Custom cell content doesn't appear.

**Solution:** Check column key matches:
```vue
<template #cell="{ column, row, value }">
  <!-- Use column.key to identify which column -->
  <template v-if="column.key === 'status'">
    <Badge>{{ value }}</Badge>
  </template>
</template>
```

## Next Steps

- Learn about [List Resource & Pagination](./10-list-resource-pagination.md)
- Explore [File Uploads](./11-file-uploads.md)
- Build [Complete SPA](./15-complete-spa-example.md)
