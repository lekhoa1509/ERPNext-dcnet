# List Resource and Pagination Tutorial

## Overview

`createListResource` is a specialized resource for working with lists of Frappe documents. It provides built-in pagination, filtering, sorting, and CRUD operations for list data. This tutorial covers comprehensive usage of list resources.

## Basic List Resource

### Simple List Fetch

```vue
<template>
  <div class="p-4">
    <div v-if="customers.loading">Loading...</div>

    <ul v-else class="space-y-2">
      <li v-for="customer in customers.data" :key="customer.name" class="p-2 border rounded">
        {{ customer.customer_name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { createListResource } from 'frappe-ui'

const customers = createListResource({
  doctype: 'Customer',
  fields: ['name', 'customer_name', 'territory'],
  auto: true
})
</script>
```

## List Resource Options

### Complete Options Reference

```javascript
const items = createListResource({
  // Required: DocType name
  doctype: 'Item',

  // Fields to fetch
  fields: ['name', 'item_name', 'item_code', 'stock_uom', 'standard_rate'],

  // Filters (array format)
  filters: [
    ['is_stock_item', '=', 1],
    ['disabled', '=', 0]
  ],

  // Or filters (object format)
  filters: {
    is_stock_item: 1,
    disabled: 0
  },

  // Or-filters (any condition matches)
  orFilters: [
    ['item_group', '=', 'Products'],
    ['item_group', '=', 'Services']
  ],

  // Sorting
  orderBy: 'creation desc',
  // Or multiple columns
  orderBy: 'item_group asc, item_name asc',

  // Pagination
  start: 0,           // Starting index (default: 0)
  pageLength: 20,     // Records per page (default: 20)

  // For child tables
  parent: 'Sales Order',

  // Custom API endpoint
  url: 'myapp.api.get_items',

  // Cache key
  cache: 'items-list',
  // Or with variables
  cache: ['items', currentGroup],

  // Auto-fetch on mount
  auto: true,

  // Debug SQL query
  debug: 1,

  // Transform response data
  transform(data) {
    return data.map(item => ({
      ...item,
      displayName: `${item.item_code}: ${item.item_name}`
    }))
  },

  // Event handlers
  onSuccess(data) {
    console.log('Fetched:', data.length, 'items')
  },
  onError(error) {
    console.error('Error:', error)
  },

  // Sub-resource event handlers
  insert: {
    onSuccess(doc) {
      toast({ type: 'success', message: 'Item created!' })
    }
  },
  setValue: {
    onSuccess() {
      toast({ type: 'success', message: 'Item updated!' })
    }
  },
  delete: {
    onSuccess() {
      toast({ type: 'success', message: 'Item deleted!' })
    }
  }
})
```

## List Resource API

### Properties

```javascript
const list = createListResource({...})

// Data
list.data           // Array of records
list.originalData   // Data before transform
list.loading        // Boolean - fetching state
list.hasNextPage    // Boolean - more pages available
list.start          // Current starting index

// Internal resources
list.list           // Main list fetch resource
list.fetchOne       // Single record fetch resource
list.insert         // Insert new record resource
list.setValue       // Update record resource
list.delete         // Delete record resource
list.runDocMethod   // Call doc method resource
```

### Methods

```javascript
// Reload current page
list.reload()

// Pagination
list.next()       // Go to next page
list.previous()   // Go to previous page

// Update options and reload
list.update({
  filters: { status: 'Active' },
  orderBy: 'name asc'
})
```

## Pagination

### Basic Pagination Controls

```vue
<template>
  <div class="p-4">
    <!-- List -->
    <ul class="space-y-2 mb-4">
      <li v-for="item in items.data" :key="item.name" class="p-3 border rounded">
        {{ item.item_name }}
      </li>
    </ul>

    <!-- Pagination -->
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-500">
        Page {{ currentPage }} of {{ totalPages }}
      </span>

      <div class="flex gap-2">
        <Button
          icon="chevron-left"
          :disabled="items.start === 0"
          @click="items.previous()"
        />
        <Button
          icon="chevron-right"
          :disabled="!items.hasNextPage"
          @click="items.next()"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { createListResource, Button } from 'frappe-ui'

const pageLength = 20

const items = createListResource({
  doctype: 'Item',
  fields: ['name', 'item_name', 'item_code'],
  pageLength,
  auto: true
})

const currentPage = computed(() => {
  return Math.floor(items.start / pageLength) + 1
})

const totalPages = computed(() => {
  // Note: This is an approximation since we don't have total count
  if (!items.data?.length) return 1
  return items.hasNextPage ? currentPage.value + 1 : currentPage.value
})
</script>
```

### Page Size Selection

```vue
<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <Select
        v-model="pageLength"
        :options="pageSizeOptions"
        @update:model-value="changePageSize"
      />

      <span class="text-sm text-gray-500">
        Showing {{ items.data?.length || 0 }} items
      </span>
    </div>

    <ul class="space-y-2">
      <li v-for="item in items.data" :key="item.name">
        {{ item.item_name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createListResource, Select } from 'frappe-ui'

const pageLength = ref(20)

const pageSizeOptions = [
  { label: '10 per page', value: 10 },
  { label: '20 per page', value: 20 },
  { label: '50 per page', value: 50 },
  { label: '100 per page', value: 100 }
]

const items = createListResource({
  doctype: 'Item',
  fields: ['name', 'item_name'],
  pageLength: pageLength.value,
  auto: true
})

const changePageSize = (newSize) => {
  items.update({
    pageLength: newSize,
    start: 0  // Reset to first page
  })
}
</script>
```

## Filtering

### Dynamic Filters

```vue
<template>
  <div class="p-4">
    <!-- Filters -->
    <div class="flex gap-4 mb-4">
      <TextInput
        v-model="searchQuery"
        placeholder="Search..."
        :debounce="300"
        @update:model-value="applyFilters"
      />

      <Select
        v-model="statusFilter"
        :options="statusOptions"
        placeholder="All Statuses"
        @update:model-value="applyFilters"
      />

      <Select
        v-model="groupFilter"
        :options="groupOptions"
        placeholder="All Groups"
        @update:model-value="applyFilters"
      />
    </div>

    <!-- Results -->
    <ListView
      :columns="columns"
      :rows="items.data || []"
      :loading="items.loading"
      row-key="name"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createListResource, TextInput, Select, ListView } from 'frappe-ui'

const searchQuery = ref('')
const statusFilter = ref('')
const groupFilter = ref('')

const statusOptions = [
  { label: 'All Statuses', value: '' },
  { label: 'Enabled', value: '0' },
  { label: 'Disabled', value: '1' }
]

const groupOptions = [
  { label: 'All Groups', value: '' },
  { label: 'Products', value: 'Products' },
  { label: 'Services', value: 'Services' }
]

const columns = [
  { label: 'Item Code', key: 'item_code', width: '150px' },
  { label: 'Item Name', key: 'item_name' },
  { label: 'Group', key: 'item_group', width: '150px' }
]

const items = createListResource({
  doctype: 'Item',
  fields: ['name', 'item_code', 'item_name', 'item_group', 'disabled'],
  pageLength: 20,
  auto: true
})

const applyFilters = () => {
  const filters = []

  if (searchQuery.value) {
    filters.push(['item_name', 'like', `%${searchQuery.value}%`])
  }

  if (statusFilter.value !== '') {
    filters.push(['disabled', '=', parseInt(statusFilter.value)])
  }

  if (groupFilter.value) {
    filters.push(['item_group', '=', groupFilter.value])
  }

  items.update({
    filters,
    start: 0  // Reset to first page when filtering
  })
}
</script>
```

## CRUD Operations

### Insert New Record

```vue
<template>
  <div>
    <Button
      label="Add Item"
      @click="showAddDialog = true"
    />

    <Dialog
      v-model="showAddDialog"
      :options="{ title: 'Add New Item' }"
    >
      <template #body-content>
        <div class="space-y-4">
          <FormControl v-model="newItem.item_code" label="Item Code" required />
          <FormControl v-model="newItem.item_name" label="Item Name" required />
          <FormControl
            v-model="newItem.item_group"
            type="select"
            label="Item Group"
            :options="itemGroups"
          />
        </div>
      </template>

      <template #actions="{ close }">
        <Button label="Cancel" @click="close" />
        <Button
          label="Create"
          theme="blue"
          variant="solid"
          :loading="items.insert.loading"
          @click="createItem(close)"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  createListResource,
  Button,
  Dialog,
  FormControl,
  toast
} from 'frappe-ui'

const showAddDialog = ref(false)
const newItem = reactive({
  item_code: '',
  item_name: '',
  item_group: 'Products'
})

const itemGroups = [
  { label: 'Products', value: 'Products' },
  { label: 'Services', value: 'Services' }
]

const items = createListResource({
  doctype: 'Item',
  fields: ['name', 'item_code', 'item_name', 'item_group'],
  auto: true,

  insert: {
    onSuccess(doc) {
      toast({ type: 'success', message: `Item ${doc.name} created!` })
      // Reset form
      newItem.item_code = ''
      newItem.item_name = ''
      newItem.item_group = 'Products'
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Failed to create' })
    }
  }
})

const createItem = (close) => {
  if (!newItem.item_code || !newItem.item_name) {
    toast({ type: 'error', message: 'Please fill required fields' })
    return
  }

  items.insert.submit({
    item_code: newItem.item_code,
    item_name: newItem.item_name,
    item_group: newItem.item_group
  })

  close()
}
</script>
```

### Update Record

```javascript
// Update a record in the list
items.setValue.submit({
  name: 'ITEM-00001',  // Document name (required)
  item_name: 'New Name',
  item_group: 'Services'
})
```

### Delete Record

```javascript
// Delete by document name
items.delete.submit('ITEM-00001')
```

### Refresh Single Record

```javascript
// Fetch and update single record in the list
items.fetchOne.submit('ITEM-00001')
```

### Run Doc Method

```javascript
// Call a whitelisted method on a document
items.runDocMethod.submit({
  method: 'toggle_status',
  name: 'ITEM-00001',
  // Additional params passed to the method
  new_status: 'Active'
})
```

## Complete CRUD Example

```vue
<template>
  <div class="p-6 max-w-4xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Tasks</h1>
      <Button
        label="Add Task"
        theme="blue"
        variant="solid"
        icon-left="plus"
        @click="openAddDialog"
      />
    </div>

    <!-- Filters -->
    <div class="flex gap-4 mb-4">
      <TextInput
        v-model="searchQuery"
        placeholder="Search tasks..."
        :debounce="300"
        @update:model-value="applyFilters"
        class="w-64"
      />

      <Select
        v-model="statusFilter"
        :options="statusOptions"
        @update:model-value="applyFilters"
        class="w-40"
      />
    </div>

    <!-- Task List -->
    <div class="border rounded-lg overflow-hidden">
      <ListView
        :columns="columns"
        :rows="tasks.data || []"
        :loading="tasks.loading"
        row-key="name"
      >
        <template #cell="{ column, row, value }">
          <template v-if="column.key === 'status'">
            <Select
              :model-value="value"
              :options="statusValues"
              size="sm"
              @update:model-value="updateStatus(row, $event)"
            />
          </template>

          <template v-else-if="column.key === 'priority'">
            <Badge :theme="getPriorityTheme(value)">{{ value }}</Badge>
          </template>

          <template v-else-if="column.key === 'actions'">
            <div class="flex gap-1">
              <Button
                icon="edit"
                size="sm"
                variant="ghost"
                @click="openEditDialog(row)"
              />
              <Button
                icon="trash"
                size="sm"
                variant="ghost"
                theme="red"
                @click="confirmDelete(row)"
              />
            </div>
          </template>

          <template v-else>{{ value }}</template>
        </template>

        <template #empty>
          <div class="py-12 text-center text-gray-500">
            <p>No tasks found</p>
            <Button
              label="Create your first task"
              theme="blue"
              class="mt-4"
              @click="openAddDialog"
            />
          </div>
        </template>
      </ListView>
    </div>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4">
      <span class="text-sm text-gray-500">
        Showing {{ tasks.data?.length || 0 }} tasks
      </span>
      <div class="flex gap-2">
        <Button
          icon="chevron-left"
          :disabled="tasks.start === 0"
          @click="tasks.previous()"
        />
        <Button
          icon="chevron-right"
          :disabled="!tasks.hasNextPage"
          @click="tasks.next()"
        />
      </div>
    </div>

    <!-- Add/Edit Dialog -->
    <Dialog
      v-model="showDialog"
      :options="{ title: editingTask ? 'Edit Task' : 'Add Task', size: 'lg' }"
    >
      <template #body-content>
        <div class="space-y-4">
          <FormControl
            v-model="taskForm.subject"
            label="Subject"
            required
          />

          <div class="grid grid-cols-2 gap-4">
            <FormControl
              v-model="taskForm.status"
              type="select"
              label="Status"
              :options="statusValues"
            />

            <FormControl
              v-model="taskForm.priority"
              type="select"
              label="Priority"
              :options="priorityOptions"
            />
          </div>

          <FormControl
            v-model="taskForm.description"
            type="textarea"
            label="Description"
            rows="3"
          />
        </div>
      </template>

      <template #actions="{ close }">
        <Button label="Cancel" @click="close" />
        <Button
          :label="editingTask ? 'Save' : 'Create'"
          theme="blue"
          variant="solid"
          :loading="tasks.insert.loading || tasks.setValue.loading"
          @click="saveTask(close)"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  createListResource,
  ListView,
  Button,
  TextInput,
  Select,
  Dialog,
  FormControl,
  Badge,
  toast
} from 'frappe-ui'

const searchQuery = ref('')
const statusFilter = ref('')
const showDialog = ref(false)
const editingTask = ref(null)

const statusOptions = [
  { label: 'All Statuses', value: '' },
  { label: 'Open', value: 'Open' },
  { label: 'Working', value: 'Working' },
  { label: 'Completed', value: 'Completed' }
]

const statusValues = [
  { label: 'Open', value: 'Open' },
  { label: 'Working', value: 'Working' },
  { label: 'Completed', value: 'Completed' }
]

const priorityOptions = [
  { label: 'Low', value: 'Low' },
  { label: 'Medium', value: 'Medium' },
  { label: 'High', value: 'High' }
]

const columns = [
  { label: 'Subject', key: 'subject' },
  { label: 'Status', key: 'status', width: '140px' },
  { label: 'Priority', key: 'priority', width: '100px' },
  { label: '', key: 'actions', width: '80px' }
]

const initialForm = {
  subject: '',
  status: 'Open',
  priority: 'Medium',
  description: ''
}

const taskForm = reactive({ ...initialForm })

const tasks = createListResource({
  doctype: 'Task',
  fields: ['name', 'subject', 'status', 'priority', 'description'],
  orderBy: 'creation desc',
  pageLength: 20,
  auto: true,

  insert: {
    onSuccess(doc) {
      toast({ type: 'success', message: 'Task created!' })
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Failed' })
    }
  },

  setValue: {
    onSuccess() {
      toast({ type: 'success', message: 'Task updated!' })
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Failed' })
    }
  },

  delete: {
    onSuccess() {
      toast({ type: 'success', message: 'Task deleted!' })
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Failed' })
    }
  }
})

const getPriorityTheme = (priority) => {
  const themes = { Low: 'gray', Medium: 'blue', High: 'red' }
  return themes[priority] || 'gray'
}

const applyFilters = () => {
  const filters = []

  if (searchQuery.value) {
    filters.push(['subject', 'like', `%${searchQuery.value}%`])
  }

  if (statusFilter.value) {
    filters.push(['status', '=', statusFilter.value])
  }

  tasks.update({ filters, start: 0 })
}

const resetForm = () => {
  Object.assign(taskForm, initialForm)
}

const openAddDialog = () => {
  resetForm()
  editingTask.value = null
  showDialog.value = true
}

const openEditDialog = (task) => {
  taskForm.subject = task.subject
  taskForm.status = task.status
  taskForm.priority = task.priority
  taskForm.description = task.description || ''
  editingTask.value = task
  showDialog.value = true
}

const saveTask = (close) => {
  if (!taskForm.subject.trim()) {
    toast({ type: 'error', message: 'Subject is required' })
    return
  }

  if (editingTask.value) {
    // Update existing
    tasks.setValue.submit({
      name: editingTask.value.name,
      ...taskForm
    })
  } else {
    // Create new
    tasks.insert.submit({ ...taskForm })
  }

  close()
}

const updateStatus = (task, newStatus) => {
  tasks.setValue.submit({
    name: task.name,
    status: newStatus
  })
}

const confirmDelete = (task) => {
  if (confirm(`Delete task "${task.subject}"?`)) {
    tasks.delete.submit(task.name)
  }
}
</script>
```

## Options API Support

```javascript
// main.js
import { resourcesPlugin } from 'frappe-ui'
app.use(resourcesPlugin)
```

```vue
<template>
  <div v-for="task in $resources.tasks.data" :key="task.name">
    {{ task.subject }}
  </div>
</template>

<script>
export default {
  resources: {
    tasks() {
      return {
        type: 'list',
        doctype: 'Task',
        fields: ['name', 'subject', 'status'],
        auto: true,

        insert: {
          onSuccess() {
            console.log('Created!')
          }
        }
      }
    }
  }
}
</script>
```

## Common Pitfalls

### 1. Filters Not Applying

**Problem:** Changing filters doesn't update the list.

**Solution:** Use `update()` method and reset start:
```javascript
items.update({
  filters: newFilters,
  start: 0  // Reset to first page
})
```

### 2. Missing Data After Insert

**Problem:** New record doesn't appear in list.

**Solution:** List auto-reloads after successful insert. If not working, manually reload:
```javascript
insert: {
  onSuccess() {
    items.reload()  // Force reload
  }
}
```

### 3. Pagination State Lost

**Problem:** After update, pagination resets unexpectedly.

**Solution:** Preserve start value when updating filters only:
```javascript
// If you want to keep pagination
items.update({
  filters: newFilters,
  start: items.start  // Preserve current page
})
```

## Next Steps

- Learn about [File Uploads](./11-file-uploads.md)
- Explore [Vue Router Integration](./12-routing.md)
- Build [Complete SPA](./15-complete-spa-example.md)
