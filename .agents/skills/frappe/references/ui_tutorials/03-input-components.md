# Input Components Tutorial

## Overview

This tutorial covers all input components in frappe-ui: TextInput, Select, Autocomplete, Textarea, Checkbox, and the unified FormControl component.

## TextInput Component

The TextInput component is used for single-line text entry.

### Basic Usage

```vue
<template>
  <div class="space-y-4 max-w-md">
    <TextInput
      v-model="name"
      placeholder="Enter your name"
    />

    <p class="text-sm text-gray-600">You entered: {{ name }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { TextInput } from 'frappe-ui'

const name = ref('')
</script>
```

### Input Types

```vue
<template>
  <div class="space-y-4 max-w-md">
    <!-- Text input (default) -->
    <TextInput v-model="text" type="text" placeholder="Text" />

    <!-- Email input -->
    <TextInput v-model="email" type="email" placeholder="Email" />

    <!-- Password input -->
    <TextInput v-model="password" type="password" placeholder="Password" />

    <!-- Number input -->
    <TextInput v-model="number" type="number" placeholder="Number" />

    <!-- Search input -->
    <TextInput v-model="search" type="search" placeholder="Search..." />

    <!-- URL input -->
    <TextInput v-model="url" type="url" placeholder="https://example.com" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { TextInput } from 'frappe-ui'

const text = ref('')
const email = ref('')
const password = ref('')
const number = ref('')
const search = ref('')
const url = ref('')
</script>
```

### Sizes and Variants

```vue
<template>
  <div class="space-y-4 max-w-md">
    <!-- Sizes -->
    <TextInput v-model="val1" size="sm" placeholder="Small" />
    <TextInput v-model="val2" size="md" placeholder="Medium" />
    <TextInput v-model="val3" size="lg" placeholder="Large" />
    <TextInput v-model="val4" size="xl" placeholder="Extra Large" />

    <!-- Variants -->
    <TextInput v-model="val5" variant="subtle" placeholder="Subtle (default)" />
    <TextInput v-model="val6" variant="outline" placeholder="Outline" />
    <TextInput v-model="val7" variant="ghost" placeholder="Ghost" />
  </div>
</template>
```

### With Icons (Prefix/Suffix)

```vue
<template>
  <div class="space-y-4 max-w-md">
    <!-- Search with icon -->
    <TextInput v-model="search" placeholder="Search...">
      <template #prefix>
        <FeatherIcon name="search" class="w-4 h-4 text-gray-500" />
      </template>
    </TextInput>

    <!-- Email with icon -->
    <TextInput v-model="email" type="email" placeholder="Email">
      <template #prefix>
        <FeatherIcon name="mail" class="w-4 h-4 text-gray-500" />
      </template>
    </TextInput>

    <!-- Input with suffix button -->
    <TextInput v-model="code" placeholder="Enter code">
      <template #suffix>
        <Button size="sm" label="Apply" theme="blue" />
      </template>
    </TextInput>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { TextInput, Button, FeatherIcon } from 'frappe-ui'

const search = ref('')
const email = ref('')
const code = ref('')
</script>
```

### Debounced Input

```vue
<template>
  <div class="space-y-2 max-w-md">
    <TextInput
      v-model="searchQuery"
      placeholder="Search (debounced 500ms)"
      :debounce="500"
    />
    <p class="text-sm text-gray-600">
      Debounced value: {{ searchQuery }}
    </p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { TextInput } from 'frappe-ui'

const searchQuery = ref('')

// This will fire 500ms after user stops typing
watch(searchQuery, (newValue) => {
  console.log('Search for:', newValue)
})
</script>
```

## Select Component

Dropdown selection with single value.

### Basic Select

```vue
<template>
  <div class="max-w-md">
    <Select
      v-model="selectedStatus"
      :options="statusOptions"
      placeholder="Select status"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Select } from 'frappe-ui'

const selectedStatus = ref(null)

const statusOptions = [
  { label: 'Open', value: 'open' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' }
]
</script>
```

### Select with Custom Option Rendering

```vue
<template>
  <Select
    v-model="selectedPriority"
    :options="priorityOptions"
    placeholder="Select priority"
  >
    <template #option="{ option }">
      <div class="flex items-center space-x-2">
        <span
          class="w-2 h-2 rounded-full"
          :class="getPriorityColor(option.value)"
        />
        <span>{{ option.label }}</span>
      </div>
    </template>
  </Select>
</template>

<script setup>
import { ref } from 'vue'
import { Select } from 'frappe-ui'

const selectedPriority = ref(null)

const priorityOptions = [
  { label: 'Low', value: 'low' },
  { label: 'Medium', value: 'medium' },
  { label: 'High', value: 'high' },
  { label: 'Critical', value: 'critical' }
]

const getPriorityColor = (priority) => {
  const colors = {
    low: 'bg-gray-400',
    medium: 'bg-blue-400',
    high: 'bg-orange-400',
    critical: 'bg-red-500'
  }
  return colors[priority]
}
</script>
```

## Autocomplete Component

Searchable dropdown with filtering.

### Basic Autocomplete

```vue
<template>
  <div class="max-w-md">
    <Autocomplete
      v-model="selectedCustomer"
      :options="customers"
      placeholder="Search customer..."
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Autocomplete } from 'frappe-ui'

const selectedCustomer = ref(null)

const customers = [
  { label: 'Acme Corp', value: 'CUST-001' },
  { label: 'Tech Solutions', value: 'CUST-002' },
  { label: 'Global Industries', value: 'CUST-003' },
  { label: 'Local Business', value: 'CUST-004' }
]
</script>
```

### Autocomplete with Async Options

```vue
<template>
  <Autocomplete
    v-model="selectedItem"
    :options="fetchItems"
    placeholder="Search items..."
  />
</template>

<script setup>
import { ref } from 'vue'
import { Autocomplete, createResource } from 'frappe-ui'

const selectedItem = ref(null)

// Function that returns options based on search query
const fetchItems = async (query) => {
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Item',
      filters: [['item_name', 'like', `%${query}%`]],
      fields: ['name', 'item_name'],
      limit_page_length: 20
    }
  })

  await resource.fetch()

  return resource.data.map(item => ({
    label: item.item_name,
    value: item.name
  }))
}
</script>
```

## Textarea Component

Multi-line text input.

### Basic Textarea

```vue
<template>
  <div class="max-w-md">
    <Textarea
      v-model="description"
      placeholder="Enter description..."
      rows="4"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Textarea } from 'frappe-ui'

const description = ref('')
</script>
```

### Auto-resizing Textarea

```vue
<template>
  <Textarea
    v-model="content"
    placeholder="Start typing..."
    :auto-resize="true"
    :min-rows="3"
    :max-rows="10"
  />
</template>
```

## Checkbox Component

Boolean toggle input.

### Basic Checkbox

```vue
<template>
  <div class="space-y-2">
    <Checkbox v-model="agreed" label="I agree to the terms and conditions" />
    <Checkbox v-model="subscribe" label="Subscribe to newsletter" />
    <Checkbox v-model="remember" label="Remember me" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Checkbox } from 'frappe-ui'

const agreed = ref(false)
const subscribe = ref(true)
const remember = ref(false)
</script>
```

## Switch Component

Toggle switch for boolean values.

### Basic Switch

```vue
<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <span>Enable notifications</span>
      <Switch v-model="notifications" />
    </div>

    <div class="flex items-center justify-between">
      <span>Dark mode</span>
      <Switch v-model="darkMode" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Switch } from 'frappe-ui'

const notifications = ref(true)
const darkMode = ref(false)
</script>
```

## FormControl Component

A unified wrapper that handles all input types with labels and descriptions.

### Basic FormControl

```vue
<template>
  <div class="space-y-4 max-w-md">
    <FormControl
      v-model="name"
      type="text"
      label="Full Name"
      description="Enter your full legal name"
      required
    />

    <FormControl
      v-model="email"
      type="email"
      label="Email Address"
      placeholder="name@example.com"
    />

    <FormControl
      v-model="status"
      type="select"
      label="Status"
      :options="statusOptions"
    />

    <FormControl
      v-model="customer"
      type="autocomplete"
      label="Customer"
      :options="customers"
      description="Start typing to search customers"
    />

    <FormControl
      v-model="notes"
      type="textarea"
      label="Notes"
      rows="3"
    />

    <FormControl
      v-model="isActive"
      type="checkbox"
      label="Active"
      description="Enable or disable this record"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FormControl } from 'frappe-ui'

const name = ref('')
const email = ref('')
const status = ref('open')
const customer = ref(null)
const notes = ref('')
const isActive = ref(true)

const statusOptions = [
  { label: 'Open', value: 'open' },
  { label: 'Closed', value: 'closed' }
]

const customers = [
  { label: 'Customer A', value: 'CUST-001' },
  { label: 'Customer B', value: 'CUST-002' }
]
</script>
```

### FormControl with Validation Styling

```vue
<template>
  <div class="max-w-md">
    <FormControl
      v-model="email"
      type="email"
      label="Email"
      :class="{ 'border-red-500': emailError }"
      required
    />
    <p v-if="emailError" class="mt-1 text-sm text-red-500">
      {{ emailError }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FormControl } from 'frappe-ui'

const email = ref('')

const emailError = computed(() => {
  if (!email.value) return null
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    return 'Please enter a valid email address'
  }
  return null
})
</script>
```

## DatePicker and TimePicker

### DatePicker

```vue
<template>
  <div class="space-y-4 max-w-md">
    <FormControl
      v-model="startDate"
      type="date"
      label="Start Date"
    />

    <DatePicker
      v-model="endDate"
      placeholder="Select end date"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FormControl, DatePicker } from 'frappe-ui'

const startDate = ref('')
const endDate = ref('')
</script>
```

### TimePicker

```vue
<template>
  <TimePicker
    v-model="meetingTime"
    placeholder="Select time"
  />
</template>

<script setup>
import { ref } from 'vue'
import { TimePicker } from 'frappe-ui'

const meetingTime = ref('')
</script>
```

## Practical Example: Contact Form

```vue
<template>
  <form @submit.prevent="submitForm" class="max-w-lg space-y-4">
    <h2 class="text-xl font-bold">Contact Us</h2>

    <div class="grid grid-cols-2 gap-4">
      <FormControl
        v-model="form.firstName"
        label="First Name"
        required
      />

      <FormControl
        v-model="form.lastName"
        label="Last Name"
        required
      />
    </div>

    <FormControl
      v-model="form.email"
      type="email"
      label="Email"
      required
    />

    <FormControl
      v-model="form.phone"
      type="tel"
      label="Phone"
    />

    <FormControl
      v-model="form.subject"
      type="select"
      label="Subject"
      :options="subjectOptions"
      required
    />

    <FormControl
      v-model="form.message"
      type="textarea"
      label="Message"
      rows="5"
      required
    />

    <FormControl
      v-model="form.subscribe"
      type="checkbox"
      label="Subscribe to our newsletter"
    />

    <Button
      type="submit"
      label="Send Message"
      theme="blue"
      variant="solid"
      :loading="submitting"
    />
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { FormControl, Button, toast } from 'frappe-ui'

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
  subscribe: false
})

const subjectOptions = [
  { label: 'General Inquiry', value: 'general' },
  { label: 'Support', value: 'support' },
  { label: 'Sales', value: 'sales' },
  { label: 'Partnership', value: 'partnership' }
]

const submitting = ref(false)

const submitForm = async () => {
  submitting.value = true

  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1500))

  toast({
    type: 'success',
    message: 'Your message has been sent!'
  })

  submitting.value = false
}
</script>
```

## Common Pitfalls

### 1. v-model Not Working

**Problem:** Input value doesn't update.

**Solution:** Ensure you're using `ref()` for primitive values:
```javascript
// Correct
const name = ref('')

// Incorrect
let name = ''
```

### 2. Select Options Format

**Problem:** Select shows options incorrectly.

**Solution:** Use `{ label, value }` format:
```javascript
// Correct
const options = [
  { label: 'Option 1', value: '1' },
  { label: 'Option 2', value: '2' }
]

// Also valid (simple strings)
const options = ['Option 1', 'Option 2']

// Incorrect
const options = [
  { name: 'Option 1', id: '1' }
]
```

### 3. FormControl Type Mismatch

**Problem:** FormControl renders wrong component.

**Solution:** Use correct type string:
```vue
<!-- Correct types -->
type="text"
type="email"
type="password"
type="number"
type="select"
type="autocomplete"
type="textarea"
type="checkbox"
type="combobox"
```

## Next Steps

- Learn about [Dialogs and Modals](./04-dialogs-modals.md)
- Explore [Form Handling](./08-form-handling.md)
- Build with [ListView](./09-list-views.md)
