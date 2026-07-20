# Document Resource Tutorial

## Overview

`createDocumentResource` is a specialized resource for working with single Frappe documents. It provides built-in methods for fetching, updating, and deleting documents, as well as calling whitelisted methods on the document.

## Basic Usage

### Fetching a Document

```vue
<template>
  <div v-if="todo.doc" class="p-4">
    <h2 class="text-xl font-bold">{{ todo.doc.description }}</h2>
    <Badge :theme="getStatusTheme(todo.doc.status)">
      {{ todo.doc.status }}
    </Badge>
    <p class="text-gray-600 mt-2">Owner: {{ todo.doc.owner }}</p>
  </div>
  <div v-else-if="todo.get?.loading" class="p-4">
    Loading...
  </div>
</template>

<script setup>
import { createDocumentResource, Badge } from 'frappe-ui'

const todo = createDocumentResource({
  doctype: 'ToDo',
  name: 'TODO-00001'
})

const getStatusTheme = (status) => {
  return status === 'Closed' ? 'green' : 'blue'
}
</script>
```

### Document Resource Properties

```javascript
const doc = createDocumentResource({
  doctype: 'Customer',
  name: 'CUST-00001'
})

// Fetched document data
doc.doc  // { name, customer_name, territory, ... }

// Internal resources
doc.get       // Resource for fetching document
doc.setValue  // Resource for updating fields
doc.setValueDebounced  // Debounced setValue
doc.delete    // Resource for deleting document

// Methods
doc.reload()  // Refresh document from server
doc.update({ name: 'NEW-NAME' })  // Change document reference
```

## Updating Documents

### Using setValue

```vue
<template>
  <div v-if="customer.doc" class="space-y-4">
    <div>
      <label class="font-medium">Customer Name</label>
      <p>{{ customer.doc.customer_name }}</p>
    </div>

    <div>
      <label class="font-medium">Territory</label>
      <Select
        :model-value="customer.doc.territory"
        :options="territories"
        @update:model-value="updateTerritory"
      />
    </div>

    <div>
      <label class="font-medium">Status</label>
      <div class="flex gap-2">
        <Button
          label="Enable"
          :variant="customer.doc.disabled === 0 ? 'solid' : 'subtle'"
          theme="green"
          @click="setDisabled(0)"
        />
        <Button
          label="Disable"
          :variant="customer.doc.disabled === 1 ? 'solid' : 'subtle'"
          theme="red"
          @click="setDisabled(1)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, Select, Button, toast } from 'frappe-ui'

const territories = [
  { label: 'India', value: 'India' },
  { label: 'USA', value: 'USA' },
  { label: 'UK', value: 'UK' }
]

const customer = createDocumentResource({
  doctype: 'Customer',
  name: 'CUST-00001',

  setValue: {
    onSuccess() {
      toast({
        type: 'success',
        message: 'Customer updated!'
      })
    },
    onError(error) {
      toast({
        type: 'error',
        message: error.messages?.[0] || 'Update failed'
      })
    }
  }
})

const updateTerritory = (value) => {
  customer.setValue.submit({
    territory: value
  })
}

const setDisabled = (value) => {
  customer.setValue.submit({
    disabled: value
  })
}
</script>
```

### Multiple Fields Update

```javascript
customer.setValue.submit({
  customer_name: 'New Name',
  territory: 'India',
  customer_group: 'Commercial'
})
```

### Debounced Updates

For rapid updates (like typing), use `setValueDebounced`:

```vue
<template>
  <TextInput
    :model-value="note.doc?.content"
    @update:model-value="updateContent"
    placeholder="Start typing..."
  />
</template>

<script setup>
import { createDocumentResource, TextInput } from 'frappe-ui'

const note = createDocumentResource({
  doctype: 'Note',
  name: 'NOTE-00001'
})

// Updates will be batched and sent after 500ms of inactivity
const updateContent = (value) => {
  note.setValueDebounced.submit({
    content: value
  })
}
</script>
```

## Deleting Documents

```vue
<template>
  <div v-if="todo.doc" class="p-4">
    <h2>{{ todo.doc.description }}</h2>

    <Button
      label="Delete"
      theme="red"
      variant="solid"
      :loading="todo.delete.loading"
      @click="handleDelete"
    />
  </div>
</template>

<script setup>
import { createDocumentResource, Button, toast } from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()

const todo = createDocumentResource({
  doctype: 'ToDo',
  name: 'TODO-00001',

  delete: {
    onSuccess() {
      toast({
        type: 'success',
        message: 'Deleted successfully'
      })
      router.push('/todos')
    },
    onError(error) {
      toast({
        type: 'error',
        message: error.messages?.[0] || 'Delete failed'
      })
    }
  }
})

const handleDelete = () => {
  if (confirm('Are you sure you want to delete this?')) {
    todo.delete.submit()
  }
}
</script>
```

## Whitelisted Methods

Call custom server methods defined on the DocType.

### Server-Side Method

```python
# In your DocType class (e.g., todo.py)
@frappe.whitelist()
def send_reminder(self, email):
    """Send reminder email about this todo"""
    # Send email logic
    return {"status": "sent", "email": email}

@frappe.whitelist()
def mark_complete(self):
    """Mark this todo as complete"""
    self.status = "Closed"
    self.save()
    return {"status": self.status}
```

### Client-Side Usage

```vue
<template>
  <div v-if="todo.doc" class="p-4 space-y-4">
    <h2>{{ todo.doc.description }}</h2>

    <div class="flex gap-2">
      <Button
        label="Mark Complete"
        theme="green"
        variant="solid"
        :loading="todo.markComplete.loading"
        @click="handleMarkComplete"
      />

      <Button
        label="Send Reminder"
        theme="blue"
        :loading="todo.sendReminder.loading"
        @click="showReminderDialog = true"
      />
    </div>

    <Dialog
      v-model="showReminderDialog"
      :options="{ title: 'Send Reminder' }"
    >
      <template #body-content>
        <FormControl
          v-model="reminderEmail"
          type="email"
          label="Email"
          required
        />
      </template>

      <template #actions="{ close }">
        <Button label="Cancel" @click="close" />
        <Button
          label="Send"
          theme="blue"
          variant="solid"
          :loading="todo.sendReminder.loading"
          @click="handleSendReminder(close)"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  createDocumentResource,
  Button,
  Dialog,
  FormControl,
  toast
} from 'frappe-ui'

const showReminderDialog = ref(false)
const reminderEmail = ref('')

const todo = createDocumentResource({
  doctype: 'ToDo',
  name: 'TODO-00001',

  // Define whitelisted methods
  whitelistedMethods: {
    markComplete: 'mark_complete',
    sendReminder: 'send_reminder'
  },

  // Optional: Configure each method
  markComplete: {
    onSuccess(result) {
      toast({ type: 'success', message: 'Marked as complete!' })
    }
  },

  sendReminder: {
    onSuccess(result) {
      toast({ type: 'success', message: `Reminder sent to ${result.email}` })
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Failed to send' })
    }
  }
})

const handleMarkComplete = () => {
  todo.markComplete.submit()
}

const handleSendReminder = (close) => {
  todo.sendReminder.submit({
    email: reminderEmail.value
  })
  close()
}
</script>
```

## Dynamic Document Reference

Change which document is loaded:

```vue
<template>
  <div class="space-y-4">
    <Select
      v-model="selectedCustomer"
      :options="customerOptions"
      placeholder="Select customer"
    />

    <div v-if="customer.doc" class="p-4 border rounded">
      <h3 class="font-bold">{{ customer.doc.customer_name }}</h3>
      <p>Territory: {{ customer.doc.territory }}</p>
      <p>Group: {{ customer.doc.customer_group }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { createDocumentResource, Select } from 'frappe-ui'

const selectedCustomer = ref('')
const customerOptions = [
  { label: 'Customer A', value: 'CUST-001' },
  { label: 'Customer B', value: 'CUST-002' },
  { label: 'Customer C', value: 'CUST-003' }
]

const customer = createDocumentResource({
  doctype: 'Customer',
  name: ''  // Will be set dynamically
})

// Update document when selection changes
watch(selectedCustomer, (newName) => {
  if (newName) {
    customer.update({ name: newName })
    // Or: customer.reload() if name was set differently
  }
})
</script>
```

## Options API

For Vue Options API usage:

```javascript
// main.js
import { resourcesPlugin } from 'frappe-ui'
app.use(resourcesPlugin)
```

```vue
<template>
  <div v-if="$resources.todo.doc">
    {{ $resources.todo.doc.description }}
  </div>
</template>

<script>
export default {
  props: ['todoName'],

  resources: {
    todo() {
      return {
        type: 'document',
        doctype: 'ToDo',
        name: this.todoName,

        whitelistedMethods: {
          markComplete: 'mark_complete'
        }
      }
    }
  },

  methods: {
    handleComplete() {
      this.$resources.todo.markComplete.submit()
    }
  }
}
</script>
```

## Complete CRUD Example

```vue
<template>
  <div class="max-w-2xl mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Edit Customer</h1>
      <Badge :theme="customer.doc?.disabled ? 'red' : 'green'">
        {{ customer.doc?.disabled ? 'Disabled' : 'Active' }}
      </Badge>
    </div>

    <div v-if="customer.get?.loading" class="text-center py-8">
      Loading...
    </div>

    <form v-else-if="customer.doc" @submit.prevent="saveChanges" class="space-y-4">
      <FormControl
        v-model="form.customer_name"
        label="Customer Name"
        required
      />

      <FormControl
        v-model="form.territory"
        type="select"
        label="Territory"
        :options="territories"
      />

      <FormControl
        v-model="form.customer_group"
        type="select"
        label="Customer Group"
        :options="customerGroups"
      />

      <FormControl
        v-model="form.website"
        label="Website"
        type="url"
      />

      <div class="flex justify-between pt-4">
        <Button
          label="Delete"
          theme="red"
          :loading="customer.delete.loading"
          @click="confirmDelete"
        />

        <div class="space-x-2">
          <Button
            label="Reset"
            @click="resetForm"
          />
          <Button
            type="submit"
            label="Save"
            theme="blue"
            variant="solid"
            :loading="customer.setValue.loading"
          />
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import {
  createDocumentResource,
  FormControl,
  Button,
  Badge,
  toast
} from 'frappe-ui'
import { useRouter } from 'vue-router'

const props = defineProps({
  customerName: {
    type: String,
    required: true
  }
})

const router = useRouter()

const territories = [
  { label: 'India', value: 'India' },
  { label: 'USA', value: 'USA' }
]

const customerGroups = [
  { label: 'Commercial', value: 'Commercial' },
  { label: 'Individual', value: 'Individual' }
]

const form = reactive({
  customer_name: '',
  territory: '',
  customer_group: '',
  website: ''
})

const customer = createDocumentResource({
  doctype: 'Customer',
  name: props.customerName,

  onSuccess(doc) {
    // Populate form when document loads
    form.customer_name = doc.customer_name
    form.territory = doc.territory
    form.customer_group = doc.customer_group
    form.website = doc.website || ''
  },

  setValue: {
    onSuccess() {
      toast({ type: 'success', message: 'Customer updated!' })
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Update failed' })
    }
  },

  delete: {
    onSuccess() {
      toast({ type: 'success', message: 'Customer deleted' })
      router.push('/customers')
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Delete failed' })
    }
  }
})

const resetForm = () => {
  if (customer.doc) {
    form.customer_name = customer.doc.customer_name
    form.territory = customer.doc.territory
    form.customer_group = customer.doc.customer_group
    form.website = customer.doc.website || ''
  }
}

const saveChanges = () => {
  customer.setValue.submit({
    customer_name: form.customer_name,
    territory: form.territory,
    customer_group: form.customer_group,
    website: form.website
  })
}

const confirmDelete = () => {
  if (confirm('Are you sure you want to delete this customer?')) {
    customer.delete.submit()
  }
}
</script>
```

## Common Pitfalls

### 1. Accessing doc Before Load

**Problem:** Error accessing `customer.doc.name` before document loads.

**Solution:** Use optional chaining or v-if:
```vue
<!-- Option 1: v-if -->
<div v-if="customer.doc">{{ customer.doc.name }}</div>

<!-- Option 2: Optional chaining -->
<div>{{ customer.doc?.name }}</div>
```

### 2. setValue Not Updating UI

**Problem:** UI doesn't reflect changes after setValue.

**Solution:** setValue automatically updates `doc` on success. If not working, check for errors:
```javascript
customer.setValue.submit({ field: 'value' })
console.log(customer.setValue.error)  // Check for errors
```

### 3. Whitelisted Method Not Found

**Problem:** Server returns "Method not found" error.

**Solution:** Ensure method is whitelisted in Python:
```python
# Must have @frappe.whitelist() decorator
@frappe.whitelist()
def my_method(self):
    pass
```

## Next Steps

- Learn about [List Resources](./10-list-resource-pagination.md)
- Build [Form Dialogs](./04-dialogs-modals.md)
- Add [Toast Notifications](./07-toast-notifications.md)
