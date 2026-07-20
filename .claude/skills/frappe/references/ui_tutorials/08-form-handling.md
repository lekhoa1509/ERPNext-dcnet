# Form Handling Tutorial

## Overview

This tutorial covers comprehensive form handling in frappe-ui, including building forms, validation, submission, and integration with Frappe backend for document creation and updates.

## Basic Form Structure

### Simple Form

```vue
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4 max-w-md">
    <FormControl
      v-model="form.name"
      label="Name"
      required
    />

    <FormControl
      v-model="form.email"
      type="email"
      label="Email"
      required
    />

    <FormControl
      v-model="form.message"
      type="textarea"
      label="Message"
      rows="4"
    />

    <Button
      type="submit"
      label="Submit"
      theme="blue"
      variant="solid"
    />
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { FormControl, Button } from 'frappe-ui'

const form = reactive({
  name: '',
  email: '',
  message: ''
})

const handleSubmit = () => {
  console.log('Form data:', form)
}
</script>
```

## Form with Validation

### Client-Side Validation

```vue
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4 max-w-md">
    <div>
      <FormControl
        v-model="form.name"
        label="Name"
        required
        :class="{ 'border-red-500': errors.name }"
      />
      <p v-if="errors.name" class="mt-1 text-sm text-red-500">
        {{ errors.name }}
      </p>
    </div>

    <div>
      <FormControl
        v-model="form.email"
        type="email"
        label="Email"
        required
        :class="{ 'border-red-500': errors.email }"
      />
      <p v-if="errors.email" class="mt-1 text-sm text-red-500">
        {{ errors.email }}
      </p>
    </div>

    <div>
      <FormControl
        v-model="form.phone"
        label="Phone"
        :class="{ 'border-red-500': errors.phone }"
      />
      <p v-if="errors.phone" class="mt-1 text-sm text-red-500">
        {{ errors.phone }}
      </p>
    </div>

    <div>
      <FormControl
        v-model="form.age"
        type="number"
        label="Age"
        :class="{ 'border-red-500': errors.age }"
      />
      <p v-if="errors.age" class="mt-1 text-sm text-red-500">
        {{ errors.age }}
      </p>
    </div>

    <Button
      type="submit"
      label="Submit"
      theme="blue"
      variant="solid"
      :disabled="hasErrors"
    />
  </form>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { FormControl, Button, toast } from 'frappe-ui'

const form = reactive({
  name: '',
  email: '',
  phone: '',
  age: null
})

const errors = reactive({
  name: '',
  email: '',
  phone: '',
  age: ''
})

const validate = () => {
  let isValid = true

  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = '')

  // Name validation
  if (!form.name.trim()) {
    errors.name = 'Name is required'
    isValid = false
  } else if (form.name.length < 2) {
    errors.name = 'Name must be at least 2 characters'
    isValid = false
  }

  // Email validation
  if (!form.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email'
    isValid = false
  }

  // Phone validation (optional but must be valid if provided)
  if (form.phone && !/^\+?[\d\s-]{10,}$/.test(form.phone)) {
    errors.phone = 'Please enter a valid phone number'
    isValid = false
  }

  // Age validation (optional but must be valid if provided)
  if (form.age !== null && form.age !== '') {
    if (form.age < 0 || form.age > 150) {
      errors.age = 'Please enter a valid age'
      isValid = false
    }
  }

  return isValid
}

const hasErrors = computed(() => {
  return Object.values(errors).some(error => error !== '')
})

const handleSubmit = () => {
  if (validate()) {
    toast({ type: 'success', message: 'Form submitted!' })
    console.log('Valid form data:', form)
  } else {
    toast({ type: 'error', message: 'Please fix the errors' })
  }
}
</script>
```

### Reusable Validation Composable

```javascript
// composables/useFormValidation.js
import { reactive, computed } from 'vue'

export function useFormValidation(rules) {
  const errors = reactive({})

  const validate = (form) => {
    let isValid = true

    // Reset all errors
    Object.keys(rules).forEach(field => {
      errors[field] = ''
    })

    // Apply rules
    Object.entries(rules).forEach(([field, fieldRules]) => {
      const value = form[field]

      for (const rule of fieldRules) {
        const error = rule(value, form)
        if (error) {
          errors[field] = error
          isValid = false
          break
        }
      }
    })

    return isValid
  }

  const hasErrors = computed(() => {
    return Object.values(errors).some(e => e !== '')
  })

  return { errors, validate, hasErrors }
}

// Common validation rules
export const required = (message = 'This field is required') => {
  return (value) => {
    if (value === null || value === undefined || value === '') {
      return message
    }
  }
}

export const email = (message = 'Please enter a valid email') => {
  return (value) => {
    if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      return message
    }
  }
}

export const minLength = (min, message) => {
  return (value) => {
    if (value && value.length < min) {
      return message || `Must be at least ${min} characters`
    }
  }
}

export const maxLength = (max, message) => {
  return (value) => {
    if (value && value.length > max) {
      return message || `Must be no more than ${max} characters`
    }
  }
}

export const numeric = (message = 'Must be a number') => {
  return (value) => {
    if (value !== null && value !== '' && isNaN(value)) {
      return message
    }
  }
}

export const min = (minValue, message) => {
  return (value) => {
    if (value !== null && value !== '' && Number(value) < minValue) {
      return message || `Must be at least ${minValue}`
    }
  }
}

export const max = (maxValue, message) => {
  return (value) => {
    if (value !== null && value !== '' && Number(value) > maxValue) {
      return message || `Must be no more than ${maxValue}`
    }
  }
}
```

Usage:

```vue
<script setup>
import { reactive } from 'vue'
import {
  useFormValidation,
  required,
  email,
  minLength
} from '@/composables/useFormValidation'

const form = reactive({
  name: '',
  email: '',
  password: ''
})

const { errors, validate, hasErrors } = useFormValidation({
  name: [required(), minLength(2)],
  email: [required(), email()],
  password: [required(), minLength(8, 'Password must be at least 8 characters')]
})

const handleSubmit = () => {
  if (validate(form)) {
    // Submit form
  }
}
</script>
```

## Creating Documents

### Create Form with Resource

```vue
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4 max-w-lg">
    <h2 class="text-xl font-bold">Create Customer</h2>

    <FormControl
      v-model="form.customer_name"
      label="Customer Name"
      required
    />

    <FormControl
      v-model="form.customer_type"
      type="select"
      label="Customer Type"
      :options="customerTypes"
    />

    <FormControl
      v-model="form.territory"
      type="autocomplete"
      label="Territory"
      :options="fetchTerritories"
    />

    <FormControl
      v-model="form.email_id"
      type="email"
      label="Email"
    />

    <div class="flex gap-2">
      <Button
        type="submit"
        label="Create Customer"
        theme="blue"
        variant="solid"
        :loading="createCustomer.loading"
      />
      <Button
        label="Reset"
        @click="resetForm"
      />
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { createResource, FormControl, Button, toast } from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()

const customerTypes = [
  { label: 'Company', value: 'Company' },
  { label: 'Individual', value: 'Individual' }
]

const form = reactive({
  customer_name: '',
  customer_type: 'Company',
  territory: '',
  email_id: ''
})

const initialForm = { ...form }

const resetForm = () => {
  Object.assign(form, initialForm)
}

// Fetch territories for autocomplete
const fetchTerritories = async (query) => {
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Territory',
      filters: [['name', 'like', `%${query}%`]],
      limit_page_length: 20
    }
  })
  await resource.fetch()
  return resource.data.map(t => ({ label: t.name, value: t.name }))
}

const createCustomer = createResource({
  url: 'frappe.client.insert',
  validate(params) {
    if (!params.doc.customer_name) {
      return 'Customer name is required'
    }
  },
  onSuccess(doc) {
    toast({
      type: 'success',
      message: `Customer ${doc.name} created!`,
      action: {
        label: 'View',
        onClick: () => router.push(`/customers/${doc.name}`)
      }
    })
    resetForm()
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
      ...form
    }
  })
}
</script>
```

## Editing Documents

### Edit Form with Document Resource

```vue
<template>
  <div v-if="customer.get?.loading" class="p-4">
    Loading...
  </div>

  <form v-else-if="customer.doc" @submit.prevent="handleSubmit" class="space-y-4 max-w-lg">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-bold">Edit Customer</h2>
      <Badge :theme="customer.doc.disabled ? 'red' : 'green'">
        {{ customer.doc.disabled ? 'Disabled' : 'Active' }}
      </Badge>
    </div>

    <FormControl
      v-model="form.customer_name"
      label="Customer Name"
      required
    />

    <FormControl
      v-model="form.customer_type"
      type="select"
      label="Customer Type"
      :options="customerTypes"
    />

    <FormControl
      v-model="form.territory"
      type="select"
      label="Territory"
      :options="territories"
    />

    <FormControl
      v-model="form.email_id"
      type="email"
      label="Email"
    />

    <FormControl
      v-model="form.website"
      label="Website"
      type="url"
    />

    <div class="flex justify-between">
      <Button
        label="Delete"
        theme="red"
        :loading="customer.delete.loading"
        @click="handleDelete"
      />

      <div class="flex gap-2">
        <Button
          label="Cancel"
          @click="router.back()"
        />
        <Button
          type="submit"
          label="Save Changes"
          theme="blue"
          variant="solid"
          :loading="customer.setValue.loading"
          :disabled="!hasChanges"
        />
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive, computed, watch } from 'vue'
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

const customerTypes = [
  { label: 'Company', value: 'Company' },
  { label: 'Individual', value: 'Individual' }
]

const territories = [
  { label: 'India', value: 'India' },
  { label: 'USA', value: 'USA' },
  { label: 'UK', value: 'UK' }
]

const form = reactive({
  customer_name: '',
  customer_type: '',
  territory: '',
  email_id: '',
  website: ''
})

// Original values for comparison
const originalValues = reactive({})

const customer = createDocumentResource({
  doctype: 'Customer',
  name: props.customerName,

  onSuccess(doc) {
    // Populate form
    form.customer_name = doc.customer_name
    form.customer_type = doc.customer_type
    form.territory = doc.territory
    form.email_id = doc.email_id || ''
    form.website = doc.website || ''

    // Store original values
    Object.assign(originalValues, { ...form })
  },

  setValue: {
    onSuccess() {
      toast({ type: 'success', message: 'Customer updated!' })
      // Update original values
      Object.assign(originalValues, { ...form })
    },
    onError(error) {
      toast({ type: 'error', message: error.messages?.[0] || 'Update failed' })
    }
  },

  delete: {
    onSuccess() {
      toast({ type: 'success', message: 'Customer deleted' })
      router.push('/customers')
    }
  }
})

// Check if form has changes
const hasChanges = computed(() => {
  return Object.keys(form).some(key => form[key] !== originalValues[key])
})

const handleSubmit = () => {
  if (!hasChanges.value) return

  customer.setValue.submit({
    customer_name: form.customer_name,
    customer_type: form.customer_type,
    territory: form.territory,
    email_id: form.email_id,
    website: form.website
  })
}

const handleDelete = () => {
  if (confirm('Are you sure you want to delete this customer?')) {
    customer.delete.submit()
  }
}
</script>
```

## Dynamic Forms

### Adding/Removing Fields

```vue
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4 max-w-lg">
    <h2 class="text-xl font-bold">Contact Information</h2>

    <!-- Dynamic email fields -->
    <div class="space-y-2">
      <label class="font-medium">Email Addresses</label>
      <div
        v-for="(email, index) in form.emails"
        :key="index"
        class="flex gap-2"
      >
        <FormControl
          v-model="form.emails[index]"
          type="email"
          placeholder="email@example.com"
          class="flex-1"
        />
        <Button
          icon="trash"
          theme="red"
          variant="ghost"
          @click="removeEmail(index)"
          :disabled="form.emails.length === 1"
        />
      </div>
      <Button
        icon-left="plus"
        label="Add Email"
        variant="subtle"
        size="sm"
        @click="addEmail"
      />
    </div>

    <!-- Dynamic phone fields -->
    <div class="space-y-2">
      <label class="font-medium">Phone Numbers</label>
      <div
        v-for="(phone, index) in form.phones"
        :key="index"
        class="flex gap-2"
      >
        <FormControl
          v-model="form.phones[index].type"
          type="select"
          :options="phoneTypes"
          class="w-32"
        />
        <FormControl
          v-model="form.phones[index].number"
          placeholder="Phone number"
          class="flex-1"
        />
        <Button
          icon="trash"
          theme="red"
          variant="ghost"
          @click="removePhone(index)"
          :disabled="form.phones.length === 1"
        />
      </div>
      <Button
        icon-left="plus"
        label="Add Phone"
        variant="subtle"
        size="sm"
        @click="addPhone"
      />
    </div>

    <Button
      type="submit"
      label="Save Contact"
      theme="blue"
      variant="solid"
    />
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { FormControl, Button, toast } from 'frappe-ui'

const phoneTypes = [
  { label: 'Mobile', value: 'Mobile' },
  { label: 'Work', value: 'Work' },
  { label: 'Home', value: 'Home' }
]

const form = reactive({
  emails: [''],
  phones: [{ type: 'Mobile', number: '' }]
})

const addEmail = () => {
  form.emails.push('')
}

const removeEmail = (index) => {
  if (form.emails.length > 1) {
    form.emails.splice(index, 1)
  }
}

const addPhone = () => {
  form.phones.push({ type: 'Mobile', number: '' })
}

const removePhone = (index) => {
  if (form.phones.length > 1) {
    form.phones.splice(index, 1)
  }
}

const handleSubmit = () => {
  // Filter out empty values
  const data = {
    emails: form.emails.filter(e => e.trim()),
    phones: form.phones.filter(p => p.number.trim())
  }
  console.log('Submitting:', data)
  toast({ type: 'success', message: 'Contact saved!' })
}
</script>
```

## Form in Dialog

```vue
<template>
  <div>
    <Button
      label="Add New Item"
      theme="blue"
      variant="solid"
      icon-left="plus"
      @click="showDialog = true"
    />

    <Dialog
      v-model="showDialog"
      :options="{
        title: 'Add New Item',
        size: 'lg'
      }"
    >
      <template #body-content>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <FormControl
            ref="nameInput"
            v-model="form.item_name"
            label="Item Name"
            required
          />

          <div class="grid grid-cols-2 gap-4">
            <FormControl
              v-model="form.item_group"
              type="select"
              label="Item Group"
              :options="itemGroups"
            />

            <FormControl
              v-model="form.stock_uom"
              type="select"
              label="Unit of Measure"
              :options="uoms"
            />
          </div>

          <FormControl
            v-model="form.description"
            type="textarea"
            label="Description"
            rows="3"
          />

          <div class="grid grid-cols-2 gap-4">
            <FormControl
              v-model="form.standard_rate"
              type="number"
              label="Standard Rate"
            />

            <FormControl
              v-model="form.is_stock_item"
              type="checkbox"
              label="Maintain Stock"
            />
          </div>
        </form>
      </template>

      <template #actions="{ close }">
        <Button label="Cancel" @click="close" />
        <Button
          label="Create Item"
          theme="blue"
          variant="solid"
          :loading="createItem.loading"
          @click="handleSubmit(close)"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, watch } from 'vue'
import {
  Dialog,
  Button,
  FormControl,
  createResource,
  toast
} from 'frappe-ui'

const showDialog = ref(false)
const nameInput = ref(null)

const itemGroups = [
  { label: 'Products', value: 'Products' },
  { label: 'Services', value: 'Services' },
  { label: 'Raw Materials', value: 'Raw Materials' }
]

const uoms = [
  { label: 'Nos', value: 'Nos' },
  { label: 'Kg', value: 'Kg' },
  { label: 'Box', value: 'Box' }
]

const initialForm = {
  item_name: '',
  item_group: 'Products',
  stock_uom: 'Nos',
  description: '',
  standard_rate: 0,
  is_stock_item: true
}

const form = reactive({ ...initialForm })

// Focus first input when dialog opens
watch(showDialog, async (isOpen) => {
  if (isOpen) {
    await nextTick()
    nameInput.value?.$el?.querySelector('input')?.focus()
  }
})

const resetForm = () => {
  Object.assign(form, initialForm)
}

const createItem = createResource({
  url: 'frappe.client.insert',
  onSuccess(doc) {
    toast({
      type: 'success',
      message: `Item ${doc.name} created!`
    })
    resetForm()
  },
  onError(error) {
    toast({
      type: 'error',
      message: error.messages?.[0] || 'Failed to create item'
    })
  }
})

const handleSubmit = (close) => {
  if (!form.item_name.trim()) {
    toast({ type: 'error', message: 'Item name is required' })
    return
  }

  createItem.submit({
    doc: {
      doctype: 'Item',
      ...form
    }
  })

  if (close) close()
}
</script>
```

## Common Pitfalls

### 1. Form Not Reactive

**Problem:** Changes to form fields don't update the UI.

**Solution:** Use `reactive()` for form objects:
```javascript
// Correct
const form = reactive({ name: '', email: '' })

// Incorrect
const form = { name: '', email: '' }
```

### 2. Resetting Form Doesn't Work

**Problem:** `Object.assign(form, {})` doesn't reset reactive object properly.

**Solution:** Store and use initial values:
```javascript
const initialForm = { name: '', email: '' }
const form = reactive({ ...initialForm })

const resetForm = () => {
  Object.assign(form, initialForm)
}
```

### 3. Validation Runs Too Early

**Problem:** Errors show before user interacts with form.

**Solution:** Track touched fields:
```javascript
const touched = reactive({})

const onBlur = (field) => {
  touched[field] = true
  validateField(field)
}

// Only show error if field was touched
<p v-if="touched.email && errors.email">{{ errors.email }}</p>
```

## Next Steps

- Learn about [List Views](./09-list-views.md)
- Explore [File Uploads](./11-file-uploads.md)
- Build [Complete SPA](./15-complete-spa-example.md)
