# State Management Tutorial

## Overview

This tutorial covers state management patterns in frappe-ui applications, from simple reactive state to shared composables and global stores. We'll focus on Vue 3's Composition API patterns that work well with frappe-ui's resource system.

## Local Component State

### Basic Reactive State

```vue
<script setup>
import { ref, reactive, computed } from 'vue'

// Primitive values
const count = ref(0)
const isOpen = ref(false)

// Objects
const form = reactive({
  name: '',
  email: '',
  status: 'draft'
})

// Computed values
const isValid = computed(() => {
  return form.name.length > 0 && form.email.includes('@')
})

// Methods
const increment = () => count.value++
const toggle = () => isOpen.value = !isOpen.value
</script>
```

## Shared State with Composables

### Creating a Composable

```javascript
// composables/useCounter.js
import { ref, computed } from 'vue'

// State outside the function = shared across all components
const count = ref(0)

export function useCounter() {
  const doubleCount = computed(() => count.value * 2)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = 0

  return {
    count,
    doubleCount,
    increment,
    decrement,
    reset
  }
}
```

### Using the Composable

```vue
<!-- ComponentA.vue -->
<template>
  <div>
    <p>Count: {{ count }}</p>
    <Button @click="increment">+</Button>
  </div>
</template>

<script setup>
import { useCounter } from '@/composables/useCounter'
import { Button } from 'frappe-ui'

const { count, increment } = useCounter()
</script>
```

```vue
<!-- ComponentB.vue -->
<template>
  <div>
    <!-- Same count value as ComponentA -->
    <p>Count: {{ count }}</p>
    <p>Double: {{ doubleCount }}</p>
    <Button @click="decrement">-</Button>
  </div>
</template>

<script setup>
import { useCounter } from '@/composables/useCounter'
import { Button } from 'frappe-ui'

const { count, doubleCount, decrement } = useCounter()
</script>
```

## Session State

### User Session Composable

```javascript
// composables/useSession.js
import { ref, computed, readonly } from 'vue'
import { createResource } from 'frappe-ui'

const user = ref(null)
const isLoading = ref(true)
const isAuthenticated = ref(false)

// Fetch current user
const sessionResource = createResource({
  url: 'frappe.auth.get_logged_user',
  auto: true,
  onSuccess(data) {
    if (data && data !== 'Guest') {
      user.value = data
      isAuthenticated.value = true
      // Fetch full user details
      fetchUserDetails()
    } else {
      user.value = null
      isAuthenticated.value = false
    }
    isLoading.value = false
  },
  onError() {
    user.value = null
    isAuthenticated.value = false
    isLoading.value = false
  }
})

const userDetails = ref(null)

const fetchUserDetails = async () => {
  const detailsResource = createResource({
    url: 'frappe.client.get',
    params: {
      doctype: 'User',
      name: user.value
    }
  })
  await detailsResource.fetch()
  userDetails.value = detailsResource.data
}

export function useSession() {
  const login = async (email, password) => {
    const loginResource = createResource({
      url: 'frappe.auth.login'
    })
    await loginResource.submit({ usr: email, pwd: password })
    sessionResource.reload()
  }

  const logout = async () => {
    const logoutResource = createResource({
      url: 'frappe.handler.logout'
    })
    await logoutResource.submit()
    user.value = null
    userDetails.value = null
    isAuthenticated.value = false
    window.location.href = '/login'
  }

  return {
    user: readonly(user),
    userDetails: readonly(userDetails),
    isLoading: readonly(isLoading),
    isAuthenticated: readonly(isAuthenticated),
    login,
    logout,
    reload: () => sessionResource.reload()
  }
}
```

### Using Session State

```vue
<template>
  <header class="flex justify-between items-center p-4 border-b">
    <h1>My App</h1>

    <div v-if="isLoading">
      <Spinner />
    </div>

    <div v-else-if="isAuthenticated" class="flex items-center gap-4">
      <span>{{ userDetails?.full_name || user }}</span>
      <Button label="Logout" @click="logout" />
    </div>

    <Button v-else label="Login" route="/login" />
  </header>
</template>

<script setup>
import { useSession } from '@/composables/useSession'
import { Button, Spinner } from 'frappe-ui'

const { user, userDetails, isLoading, isAuthenticated, logout } = useSession()
</script>
```

## Application Settings

### Settings Store

```javascript
// composables/useSettings.js
import { ref, computed, watch } from 'vue'
import { createResource } from 'frappe-ui'

const settings = ref({
  theme: 'light',
  language: 'en',
  itemsPerPage: 20,
  notifications: true
})

// Load from localStorage
const loadSettings = () => {
  const stored = localStorage.getItem('app_settings')
  if (stored) {
    settings.value = { ...settings.value, ...JSON.parse(stored) }
  }
}

// Save to localStorage
watch(settings, (newSettings) => {
  localStorage.setItem('app_settings', JSON.stringify(newSettings))
}, { deep: true })

// Initialize
loadSettings()

export function useSettings() {
  const isDarkMode = computed(() => settings.value.theme === 'dark')

  const setTheme = (theme) => {
    settings.value.theme = theme
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }

  const setLanguage = (lang) => {
    settings.value.language = lang
  }

  const setItemsPerPage = (count) => {
    settings.value.itemsPerPage = count
  }

  const toggleNotifications = () => {
    settings.value.notifications = !settings.value.notifications
  }

  return {
    settings,
    isDarkMode,
    setTheme,
    setLanguage,
    setItemsPerPage,
    toggleNotifications
  }
}
```

## Cart / Selection State

### Shopping Cart Example

```javascript
// composables/useCart.js
import { ref, computed } from 'vue'
import { toast } from 'frappe-ui'

const items = ref([])

export function useCart() {
  const itemCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.qty, 0)
  })

  const total = computed(() => {
    return items.value.reduce((sum, item) => sum + (item.price * item.qty), 0)
  })

  const addItem = (product, qty = 1) => {
    const existing = items.value.find(item => item.id === product.id)

    if (existing) {
      existing.qty += qty
    } else {
      items.value.push({
        id: product.id,
        name: product.name,
        price: product.price,
        qty
      })
    }

    toast({
      type: 'success',
      message: `${product.name} added to cart`,
      duration: 2000
    })
  }

  const removeItem = (productId) => {
    const index = items.value.findIndex(item => item.id === productId)
    if (index > -1) {
      items.value.splice(index, 1)
    }
  }

  const updateQuantity = (productId, qty) => {
    const item = items.value.find(item => item.id === productId)
    if (item) {
      if (qty <= 0) {
        removeItem(productId)
      } else {
        item.qty = qty
      }
    }
  }

  const clearCart = () => {
    items.value = []
  }

  return {
    items,
    itemCount,
    total,
    addItem,
    removeItem,
    updateQuantity,
    clearCart
  }
}
```

### Using Cart State

```vue
<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">
      Cart ({{ itemCount }} items)
    </h2>

    <div v-if="items.length === 0" class="text-gray-500">
      Your cart is empty
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="item in items"
        :key="item.id"
        class="flex justify-between items-center p-3 border rounded"
      >
        <div>
          <p class="font-medium">{{ item.name }}</p>
          <p class="text-sm text-gray-500">${{ item.price }} each</p>
        </div>

        <div class="flex items-center gap-2">
          <Button
            icon="minus"
            size="sm"
            @click="updateQuantity(item.id, item.qty - 1)"
          />
          <span class="w-8 text-center">{{ item.qty }}</span>
          <Button
            icon="plus"
            size="sm"
            @click="updateQuantity(item.id, item.qty + 1)"
          />
          <Button
            icon="trash"
            size="sm"
            theme="red"
            variant="ghost"
            @click="removeItem(item.id)"
          />
        </div>
      </div>

      <div class="flex justify-between items-center pt-4 border-t">
        <span class="font-bold">Total:</span>
        <span class="text-xl font-bold">${{ total.toFixed(2) }}</span>
      </div>

      <Button
        label="Checkout"
        theme="blue"
        variant="solid"
        class="w-full"
      />
    </div>
  </div>
</template>

<script setup>
import { useCart } from '@/composables/useCart'
import { Button } from 'frappe-ui'

const { items, itemCount, total, updateQuantity, removeItem } = useCart()
</script>
```

## Resource Caching as State

### Using frappe-ui Cache

```javascript
// composables/useCustomers.js
import { computed } from 'vue'
import { createListResource, getCachedResource } from 'frappe-ui'

const CACHE_KEY = 'customers-list'

export function useCustomers() {
  // Try to get cached resource first
  let customers = getCachedResource(CACHE_KEY)

  if (!customers) {
    customers = createListResource({
      doctype: 'Customer',
      fields: ['name', 'customer_name', 'territory', 'customer_type'],
      orderBy: 'creation desc',
      pageLength: 100,
      cache: CACHE_KEY,
      auto: true
    })
  }

  const customerOptions = computed(() => {
    return (customers.data || []).map(c => ({
      label: c.customer_name,
      value: c.name
    }))
  })

  const getCustomer = (name) => {
    return customers.data?.find(c => c.name === name)
  }

  return {
    customers,
    customerOptions,
    getCustomer,
    reload: () => customers.reload()
  }
}
```

### Using Cached Data Across Components

```vue
<!-- CustomerSelect.vue -->
<template>
  <FormControl
    v-model="selectedCustomer"
    type="autocomplete"
    :options="customerOptions"
    :loading="customers.loading"
    @update:model-value="$emit('update:modelValue', $event)"
  />
</template>

<script setup>
import { ref } from 'vue'
import { useCustomers } from '@/composables/useCustomers'
import { FormControl } from 'frappe-ui'

defineEmits(['update:modelValue'])

const { customerOptions, customers } = useCustomers()
const selectedCustomer = ref('')
</script>
```

```vue
<!-- CustomerInfo.vue -->
<template>
  <div v-if="customer" class="p-4 border rounded">
    <h3 class="font-bold">{{ customer.customer_name }}</h3>
    <p class="text-sm text-gray-500">{{ customer.territory }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCustomers } from '@/composables/useCustomers'

const props = defineProps({
  customerName: String
})

const { getCustomer } = useCustomers()
const customer = computed(() => getCustomer(props.customerName))
</script>
```

## Form State with Dirty Tracking

### Form State Composable

```javascript
// composables/useFormState.js
import { reactive, computed, watch, toRaw } from 'vue'

export function useFormState(initialData = {}) {
  const form = reactive({ ...initialData })
  const original = { ...initialData }

  const isDirty = computed(() => {
    return JSON.stringify(toRaw(form)) !== JSON.stringify(original)
  })

  const changedFields = computed(() => {
    const changes = {}
    Object.keys(form).forEach(key => {
      if (form[key] !== original[key]) {
        changes[key] = {
          from: original[key],
          to: form[key]
        }
      }
    })
    return changes
  })

  const reset = () => {
    Object.assign(form, original)
  }

  const setOriginal = (data) => {
    Object.assign(original, data)
    Object.assign(form, data)
  }

  const getChanges = () => {
    const changes = {}
    Object.keys(form).forEach(key => {
      if (form[key] !== original[key]) {
        changes[key] = form[key]
      }
    })
    return changes
  }

  return {
    form,
    isDirty,
    changedFields,
    reset,
    setOriginal,
    getChanges
  }
}
```

### Using Form State

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <FormControl v-model="form.name" label="Name" />
    <FormControl v-model="form.email" type="email" label="Email" />

    <div class="flex gap-2 mt-4">
      <Button
        label="Reset"
        :disabled="!isDirty"
        @click="reset"
      />
      <Button
        type="submit"
        label="Save"
        theme="blue"
        variant="solid"
        :disabled="!isDirty"
      />
    </div>

    <div v-if="isDirty" class="mt-2 text-sm text-orange-600">
      You have unsaved changes
    </div>
  </form>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { useFormState } from '@/composables/useFormState'
import { FormControl, Button, toast } from 'frappe-ui'

const { form, isDirty, reset, setOriginal, getChanges } = useFormState({
  name: '',
  email: ''
})

// Warn before leaving with unsaved changes
const handleBeforeUnload = (e) => {
  if (isDirty.value) {
    e.preventDefault()
    e.returnValue = ''
  }
}

onMounted(() => {
  window.addEventListener('beforeunload', handleBeforeUnload)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})

const handleSubmit = () => {
  const changes = getChanges()
  console.log('Saving changes:', changes)
  // After successful save:
  setOriginal(form)
  toast({ type: 'success', message: 'Saved!' })
}
</script>
```

## Global Event Bus

### Simple Event Bus

```javascript
// utils/eventBus.js
import { ref } from 'vue'

const listeners = ref(new Map())

export const eventBus = {
  on(event, callback) {
    if (!listeners.value.has(event)) {
      listeners.value.set(event, [])
    }
    listeners.value.get(event).push(callback)

    // Return unsubscribe function
    return () => this.off(event, callback)
  },

  off(event, callback) {
    const callbacks = listeners.value.get(event)
    if (callbacks) {
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  },

  emit(event, data) {
    const callbacks = listeners.value.get(event)
    if (callbacks) {
      callbacks.forEach(callback => callback(data))
    }
  }
}
```

### Using Event Bus

```vue
<!-- Publisher -->
<script setup>
import { eventBus } from '@/utils/eventBus'

const notifyChange = () => {
  eventBus.emit('customer:updated', { name: 'CUST-001' })
}
</script>
```

```vue
<!-- Subscriber -->
<script setup>
import { onMounted, onUnmounted } from 'vue'
import { eventBus } from '@/utils/eventBus'

let unsubscribe

onMounted(() => {
  unsubscribe = eventBus.on('customer:updated', (data) => {
    console.log('Customer updated:', data)
    // Refresh data
  })
})

onUnmounted(() => {
  if (unsubscribe) unsubscribe()
})
</script>
```

## Common Pitfalls

### 1. Reactive State Outside Setup

**Problem:** State defined inside function is not shared.

**Solution:** Define state outside the function:
```javascript
// Shared state - defined outside
const count = ref(0)

export function useCounter() {
  // Methods that use the shared state
  return { count, increment: () => count.value++ }
}
```

### 2. Losing Reactivity with Destructuring

**Problem:** Destructured values lose reactivity.

**Solution:** Use `toRefs` or access via `.value`:
```javascript
// Wrong - loses reactivity
const { settings } = useSettings()
const theme = settings.theme  // Not reactive!

// Correct
const { settings } = useSettings()
const theme = computed(() => settings.value.theme)
```

### 3. Memory Leaks with Event Listeners

**Problem:** Event listeners not cleaned up.

**Solution:** Always unsubscribe in `onUnmounted`:
```javascript
onMounted(() => {
  unsubscribe = eventBus.on('event', handler)
})
onUnmounted(() => {
  unsubscribe()
})
```

## Next Steps

- Learn about [Realtime Updates](./14-realtime-updates.md)
- Build [Complete SPA Example](./15-complete-spa-example.md)
- Explore [Advanced Patterns](./16-advanced-patterns.md)
