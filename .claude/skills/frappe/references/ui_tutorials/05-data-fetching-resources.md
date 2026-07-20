# Data Fetching with Resources

## Overview

The Resource system is the core of frappe-ui's data management. It provides reactive data fetching with built-in loading states, error handling, caching, and automatic updates. This tutorial covers `createResource`, the foundation for all data fetching in frappe-ui.

## Basic Resource

### Simple API Call

```vue
<template>
  <div class="p-4">
    <Button
      :label="posts.fetched ? 'Reload' : 'Fetch Posts'"
      :loading="posts.loading"
      @click="posts.fetch()"
    />

    <div v-if="posts.error" class="mt-4 text-red-500">
      Error: {{ posts.error }}
    </div>

    <ul v-if="posts.data" class="mt-4 space-y-2">
      <li v-for="post in posts.data" :key="post.id" class="p-2 border rounded">
        {{ post.title }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { createResource, Button } from 'frappe-ui'

const posts = createResource({
  url: 'https://jsonplaceholder.typicode.com/posts',
  method: 'GET'
})
</script>
```

### Resource Properties

```javascript
const resource = createResource({ url: '...' })

// State properties (all reactive)
resource.data        // Response data
resource.loading     // Boolean - true when fetching
resource.error       // Error object if request failed
resource.fetched     // Boolean - true after first successful fetch
resource.promise     // Promise of current/last request
resource.params      // Parameters sent with the request
resource.previousData // Data before last reload
```

### Resource Methods

```javascript
// Trigger a fetch
resource.fetch()
resource.reload()  // Alias for fetch()
resource.submit()  // Alias for fetch()

// Fetch with parameters
resource.submit({ id: 123 })

// Reset to initial state
resource.reset()

// Update resource configuration
resource.update({
  url: '/new/url',
  params: { newParam: 'value' }
})

// Manually set data
resource.setData({ custom: 'data' })
resource.setData(data => data.filter(item => item.active))
```

## Frappe Backend Integration

### Configure Frappe Request Handler

```javascript
// main.js
import { setConfig, frappeRequest } from 'frappe-ui'

// This enables automatic handling of Frappe responses
setConfig('resourceFetcher', frappeRequest)
```

### Calling Frappe API Methods

```vue
<script setup>
import { createResource } from 'frappe-ui'

// Call whitelisted method
const todos = createResource({
  url: 'frappe.client.get_list',  // No /api/method/ prefix needed
  params: {
    doctype: 'ToDo',
    fields: ['name', 'description', 'status'],
    filters: { status: 'Open' },
    limit_page_length: 20
  }
})

// Call custom whitelisted method
const stats = createResource({
  url: 'myapp.api.get_dashboard_stats',
  params: {
    user: 'current_user'
  }
})
</script>
```

## Resource Options

### Complete Options Reference

```javascript
const resource = createResource({
  // URL of the API endpoint
  url: 'frappe.client.get_list',

  // HTTP method (default: POST)
  method: 'POST',

  // Static parameters
  params: {
    doctype: 'Customer',
    fields: ['name', 'customer_name']
  },

  // Dynamic parameters (function called before each request)
  makeParams() {
    return {
      doctype: 'Customer',
      filters: { territory: selectedTerritory.value }
    }
  },

  // Initial data before first fetch
  initialData: [],

  // Auto-fetch on component mount
  auto: true,

  // Debounce delay in milliseconds
  debounce: 300,

  // Cache key for persistence
  cache: 'customers-list',
  // Or with variables
  cache: ['customers', selectedTerritory],

  // Transform response data
  transform(data) {
    return data.map(d => ({
      ...d,
      displayName: `${d.name}: ${d.customer_name}`
    }))
  },

  // Validate params before request
  validate(params) {
    if (!params.doctype) {
      return 'DocType is required'  // Return string to show error
    }
    // Return nothing/undefined to pass validation
  },

  // Called before making the request
  beforeSubmit(params) {
    console.log('About to fetch with:', params)
  },

  // Called on successful response
  onSuccess(data) {
    console.log('Received data:', data)
  },

  // Called on error
  onError(error) {
    console.error('Request failed:', error)
  }
})
```

## Caching

### Memory and IndexedDB Caching

```vue
<script setup>
import { createResource } from 'frappe-ui'

// Simple cache key
const customers = createResource({
  url: 'frappe.client.get_list',
  params: { doctype: 'Customer' },
  cache: 'all-customers'  // Cache with this key
})

// Cache key with variables
const customersByTerritory = createResource({
  url: 'frappe.client.get_list',
  params: { doctype: 'Customer' },
  cache: ['customers', territory]  // Cache per territory
})
</script>
```

### Getting Cached Resources

```javascript
import { getCachedResource } from 'frappe-ui'

// Access cached resource from anywhere in app
const cachedCustomers = getCachedResource('all-customers')
console.log(cachedCustomers?.data)
```

## Auto-Fetch

### Fetch on Mount

```vue
<script setup>
import { createResource } from 'frappe-ui'

// Automatically fetches when component mounts
const users = createResource({
  url: 'frappe.client.get_list',
  params: { doctype: 'User', fields: ['name', 'full_name'] },
  auto: true
})
</script>
```

### Reactive Auto-Fetch

```vue
<template>
  <Select v-model="selectedTerritory" :options="territories" />
  <div v-if="customers.data">
    {{ customers.data.length }} customers
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { createResource, Select } from 'frappe-ui'

const selectedTerritory = ref('India')
const territories = ['India', 'USA', 'UK']

const customers = createResource({
  url: 'frappe.client.get_list',
  params: { doctype: 'Customer' },
  makeParams() {
    return {
      doctype: 'Customer',
      filters: { territory: selectedTerritory.value }
    }
  },
  auto: true  // Fetches when selectedTerritory changes
})

// Alternative: watch and reload manually
watch(selectedTerritory, () => {
  customers.reload()
})
</script>
```

## Transform and Process Data

### Transforming Responses

```vue
<script setup>
import { createResource } from 'frappe-ui'

const tasks = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Task',
    fields: ['name', 'subject', 'status', 'priority', 'exp_end_date']
  },
  transform(data) {
    return data.map(task => ({
      ...task,
      // Add computed properties
      isOverdue: new Date(task.exp_end_date) < new Date() && task.status !== 'Completed',
      priorityColor: {
        'High': 'red',
        'Medium': 'orange',
        'Low': 'blue'
      }[task.priority] || 'gray'
    }))
  }
})
</script>
```

## Error Handling

### Handling Errors

```vue
<template>
  <div class="p-4">
    <Alert v-if="data.error" theme="red" :title="data.error.title">
      {{ data.error.message }}
    </Alert>

    <div v-else-if="data.data">
      <!-- Display data -->
    </div>
  </div>
</template>

<script setup>
import { createResource, Alert, toast } from 'frappe-ui'

const data = createResource({
  url: 'myapp.api.get_sensitive_data',
  params: { user_id: 123 },
  onError(error) {
    // Show toast notification
    toast({
      type: 'error',
      message: error.messages?.[0] || 'An error occurred'
    })
  }
})
</script>
```

### Validation Errors

```javascript
const resource = createResource({
  url: 'myapp.api.create_item',
  validate(params) {
    if (!params.name) {
      return 'Name is required'
    }
    if (params.price < 0) {
      return 'Price cannot be negative'
    }
    // Return undefined/nothing if valid
  },
  onError(error) {
    // Handles both validation errors and request errors
    console.error('Error:', error)
  }
})

// This will set error without making request
resource.submit({ name: '', price: -10 })
console.log(resource.error)  // 'Name is required'
```

## Debouncing

### Debounced Requests

```vue
<template>
  <TextInput
    v-model="searchQuery"
    placeholder="Search customers..."
  />

  <div v-if="searchResults.loading">Searching...</div>
  <ul v-if="searchResults.data">
    <li v-for="result in searchResults.data" :key="result.name">
      {{ result.customer_name }}
    </li>
  </ul>
</template>

<script setup>
import { ref, watch } from 'vue'
import { createResource, TextInput } from 'frappe-ui'

const searchQuery = ref('')

const searchResults = createResource({
  url: 'frappe.client.get_list',
  debounce: 300,  // Wait 300ms after last call
  makeParams() {
    return {
      doctype: 'Customer',
      filters: [['customer_name', 'like', `%${searchQuery.value}%`]],
      limit_page_length: 10
    }
  }
})

watch(searchQuery, () => {
  if (searchQuery.value.length >= 2) {
    searchResults.reload()
  }
})
</script>
```

## Practical Examples

### Dashboard Stats

```vue
<template>
  <div class="grid grid-cols-4 gap-4">
    <div v-if="stats.loading" class="col-span-4">Loading...</div>
    <template v-else-if="stats.data">
      <StatCard
        v-for="stat in stats.data"
        :key="stat.label"
        :label="stat.label"
        :value="stat.value"
        :change="stat.change"
      />
    </template>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui'

const stats = createResource({
  url: 'myapp.api.get_dashboard_stats',
  auto: true,
  cache: 'dashboard-stats',
  transform(data) {
    return [
      { label: 'Total Sales', value: data.total_sales, change: data.sales_change },
      { label: 'New Customers', value: data.new_customers, change: data.customer_change },
      { label: 'Open Tasks', value: data.open_tasks },
      { label: 'Pending Orders', value: data.pending_orders }
    ]
  }
})
</script>
```

### Submit Form Data

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <FormControl v-model="form.name" label="Name" required />
    <FormControl v-model="form.email" label="Email" type="email" required />

    <Button
      type="submit"
      label="Create Customer"
      :loading="createCustomer.loading"
      theme="blue"
      variant="solid"
    />
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { createResource, FormControl, Button, toast } from 'frappe-ui'

const form = reactive({
  name: '',
  email: ''
})

const createCustomer = createResource({
  url: 'frappe.client.insert',
  onSuccess(doc) {
    toast({
      type: 'success',
      message: `Customer ${doc.name} created!`
    })
    form.name = ''
    form.email = ''
  },
  onError(error) {
    toast({
      type: 'error',
      message: error.messages?.[0] || 'Failed to create customer'
    })
  }
})

const handleSubmit = () => {
  createCustomer.submit({
    doc: {
      doctype: 'Customer',
      customer_name: form.name,
      email_id: form.email,
      customer_type: 'Individual'
    }
  })
}
</script>
```

## Common Pitfalls

### 1. Not Using Frappe Request Handler

**Problem:** Response contains `message` wrapper, not actual data.

**Solution:** Configure frappeRequest:
```javascript
import { setConfig, frappeRequest } from 'frappe-ui'
setConfig('resourceFetcher', frappeRequest)
```

### 2. makeParams Not Being Called

**Problem:** Dynamic parameters don't update.

**Solution:** Make sure to use `makeParams` with reactive variables:
```javascript
// Correct - makeParams is a function
const resource = createResource({
  makeParams() {
    return { id: userId.value }  // Reactive
  }
})

// Incorrect - params is static
const resource = createResource({
  params: { id: userId.value }  // Static, won't update
})
```

### 3. Cache Not Updating

**Problem:** Cached data is stale.

**Solution:** Call `reload()` to force refresh:
```javascript
const resource = createResource({
  url: 'api/data',
  cache: 'my-data'
})

// Force fresh data
resource.reload()
```

### 4. Resource Not Reactive in Template

**Problem:** Template doesn't update when data changes.

**Solution:** Access properties directly (they're reactive):
```vue
<!-- Correct -->
<div v-if="resource.loading">Loading...</div>
<div>{{ resource.data }}</div>

<!-- Incorrect - won't be reactive -->
<div>{{ resourceData }}</div>

<script setup>
const resource = createResource({ ... })
const resourceData = resource.data  // Not reactive!
</script>
```

## Next Steps

- Learn about [Document Resources](./06-document-resource.md)
- Explore [List Resources](./10-list-resource-pagination.md)
- Understand [Realtime Updates](./14-realtime-updates.md)
