# Advanced Patterns Tutorial

## Overview

This tutorial covers advanced patterns and techniques for building sophisticated frappe-ui applications, including custom composables, performance optimization, error boundaries, and integration patterns.

## Custom Resource Composables

### Creating Typed Resources

```typescript
// composables/useTypedResource.ts
import { computed, Ref } from 'vue'
import { createResource, createListResource, createDocumentResource } from 'frappe-ui'

interface Customer {
  name: string
  customer_name: string
  customer_type: 'Company' | 'Individual'
  territory: string
  email_id?: string
  disabled: 0 | 1
}

export function useCustomers() {
  const resource = createListResource({
    doctype: 'Customer',
    fields: ['name', 'customer_name', 'customer_type', 'territory', 'email_id', 'disabled'],
    auto: true,
    cache: 'customers'
  })

  // Type-safe data access
  const customers = computed<Customer[]>(() => resource.data || [])

  const activeCustomers = computed(() =>
    customers.value.filter(c => c.disabled === 0)
  )

  const companyCusomers = computed(() =>
    customers.value.filter(c => c.customer_type === 'Company')
  )

  return {
    resource,
    customers,
    activeCustomers,
    companyCusomers,
    loading: computed(() => resource.loading),
    reload: () => resource.reload()
  }
}
```

### Resource with Automatic Retry

```javascript
// composables/useRetryResource.js
import { ref, watch } from 'vue'
import { createResource, toast } from 'frappe-ui'

export function useRetryResource(options, maxRetries = 3) {
  const retryCount = ref(0)

  const resource = createResource({
    ...options,
    onError(error) {
      if (retryCount.value < maxRetries) {
        retryCount.value++
        setTimeout(() => {
          resource.reload()
        }, 1000 * retryCount.value) // Exponential backoff
      } else {
        toast({
          type: 'error',
          message: `Failed after ${maxRetries} retries: ${error.message}`
        })
        options.onError?.(error)
      }
    },
    onSuccess(data) {
      retryCount.value = 0
      options.onSuccess?.(data)
    }
  })

  return {
    ...resource,
    retryCount,
    resetRetries: () => retryCount.value = 0
  }
}
```

### Paginated Resource with Infinite Scroll

```javascript
// composables/useInfiniteList.js
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { createListResource } from 'frappe-ui'

export function useInfiniteList(options) {
  const allItems = ref([])
  const hasMore = ref(true)
  const pageLength = options.pageLength || 20

  const resource = createListResource({
    ...options,
    pageLength,
    onSuccess(data) {
      if (data.length < pageLength) {
        hasMore.value = false
      }
      allItems.value = [...allItems.value, ...data]
      options.onSuccess?.(data)
    }
  })

  const loadMore = () => {
    if (!resource.loading && hasMore.value) {
      resource.next()
    }
  }

  const reset = () => {
    allItems.value = []
    hasMore.value = true
    resource.update({ start: 0 })
  }

  // Intersection Observer for auto-loading
  const observerTarget = ref(null)
  let observer = null

  onMounted(() => {
    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          loadMore()
        }
      },
      { threshold: 0.1 }
    )

    if (observerTarget.value) {
      observer.observe(observerTarget.value)
    }
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  return {
    items: allItems,
    loading: computed(() => resource.loading),
    hasMore,
    loadMore,
    reset,
    observerTarget,
    setObserverTarget: (el) => {
      observerTarget.value = el
      if (el && observer) {
        observer.observe(el)
      }
    }
  }
}
```

Usage:

```vue
<template>
  <div>
    <div v-for="item in items" :key="item.name">
      {{ item.name }}
    </div>

    <div ref="loadMoreTrigger" class="py-4 text-center">
      <Spinner v-if="loading" />
      <span v-else-if="!hasMore">No more items</span>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { Spinner } from 'frappe-ui'
import { useInfiniteList } from '@/composables/useInfiniteList'

const { items, loading, hasMore, setObserverTarget } = useInfiniteList({
  doctype: 'Item',
  fields: ['name', 'item_name'],
  pageLength: 20,
  auto: true
})

const loadMoreTrigger = ref(null)

onMounted(() => {
  setObserverTarget(loadMoreTrigger.value)
})
</script>
```

## Optimistic Updates

### Optimistic List Updates

```javascript
// composables/useOptimisticList.js
import { ref } from 'vue'
import { createListResource, toast } from 'frappe-ui'

export function useOptimisticList(options) {
  const optimisticItems = ref([])

  const resource = createListResource({
    ...options,
    onSuccess(data) {
      optimisticItems.value = data
      options.onSuccess?.(data)
    }
  })

  const optimisticAdd = async (item) => {
    // Add immediately to UI
    const tempId = `temp-${Date.now()}`
    const tempItem = { ...item, name: tempId, _optimistic: true }
    optimisticItems.value.unshift(tempItem)

    try {
      // Actually create
      const result = await resource.insert.submit(item)

      // Replace temp item with real one
      const index = optimisticItems.value.findIndex(i => i.name === tempId)
      if (index !== -1) {
        optimisticItems.value[index] = result
      }
    } catch (error) {
      // Remove on failure
      optimisticItems.value = optimisticItems.value.filter(i => i.name !== tempId)
      toast({ type: 'error', message: 'Failed to create item' })
    }
  }

  const optimisticUpdate = async (name, updates) => {
    // Save original
    const item = optimisticItems.value.find(i => i.name === name)
    const original = { ...item }

    // Update immediately
    Object.assign(item, updates)

    try {
      await resource.setValue.submit({ name, ...updates })
    } catch (error) {
      // Revert on failure
      Object.assign(item, original)
      toast({ type: 'error', message: 'Failed to update' })
    }
  }

  const optimisticDelete = async (name) => {
    // Remove immediately
    const index = optimisticItems.value.findIndex(i => i.name === name)
    const removed = optimisticItems.value.splice(index, 1)[0]

    try {
      await resource.delete.submit(name)
    } catch (error) {
      // Restore on failure
      optimisticItems.value.splice(index, 0, removed)
      toast({ type: 'error', message: 'Failed to delete' })
    }
  }

  return {
    items: optimisticItems,
    loading: resource.loading,
    add: optimisticAdd,
    update: optimisticUpdate,
    remove: optimisticDelete,
    reload: () => resource.reload()
  }
}
```

## Error Boundaries

### Error Boundary Component

```vue
<!-- components/ErrorBoundary.vue -->
<template>
  <div v-if="error" class="p-8 text-center">
    <div class="max-w-md mx-auto">
      <FeatherIcon name="alert-circle" class="w-16 h-16 mx-auto text-red-500" />
      <h2 class="mt-4 text-xl font-bold text-gray-900">Something went wrong</h2>
      <p class="mt-2 text-gray-500">{{ error.message }}</p>

      <div class="mt-6 flex gap-4 justify-center">
        <Button label="Try Again" @click="retry" />
        <Button label="Go Home" route="/" />
      </div>

      <details v-if="showDetails" class="mt-8 text-left">
        <summary class="cursor-pointer text-sm text-gray-500">
          Technical Details
        </summary>
        <pre class="mt-2 p-4 bg-gray-100 rounded text-xs overflow-auto">
{{ error.stack }}
        </pre>
      </details>
    </div>
  </div>

  <slot v-else />
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { FeatherIcon, Button } from 'frappe-ui'

const props = defineProps({
  showDetails: { type: Boolean, default: false }
})

const error = ref(null)

onErrorCaptured((err, instance, info) => {
  error.value = err
  console.error('Caught error:', err, info)
  return false // Prevent propagation
})

const retry = () => {
  error.value = null
}
</script>
```

### Using Error Boundary

```vue
<template>
  <ErrorBoundary>
    <Suspense>
      <AsyncComponent />
      <template #fallback>
        <Spinner />
      </template>
    </Suspense>
  </ErrorBoundary>
</template>
```

## Debounced Search

### Search with Debounce and Cancel

```javascript
// composables/useDebouncedSearch.js
import { ref, watch, onUnmounted } from 'vue'
import { createResource } from 'frappe-ui'

export function useDebouncedSearch(searchFn, delay = 300) {
  const query = ref('')
  const results = ref([])
  const loading = ref(false)
  let timeoutId = null
  let abortController = null

  const search = async (searchQuery) => {
    if (!searchQuery.trim()) {
      results.value = []
      return
    }

    // Cancel previous request
    if (abortController) {
      abortController.abort()
    }

    abortController = new AbortController()
    loading.value = true

    try {
      results.value = await searchFn(searchQuery, abortController.signal)
    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Search error:', error)
      }
    } finally {
      loading.value = false
    }
  }

  watch(query, (newQuery) => {
    if (timeoutId) {
      clearTimeout(timeoutId)
    }

    timeoutId = setTimeout(() => {
      search(newQuery)
    }, delay)
  })

  onUnmounted(() => {
    if (timeoutId) clearTimeout(timeoutId)
    if (abortController) abortController.abort()
  })

  return {
    query,
    results,
    loading,
    clear: () => {
      query.value = ''
      results.value = []
    }
  }
}
```

## Form Wizard

### Multi-Step Form

```vue
<!-- components/FormWizard.vue -->
<template>
  <div class="max-w-2xl mx-auto">
    <!-- Progress Bar -->
    <div class="mb-8">
      <div class="flex justify-between mb-2">
        <span
          v-for="(step, index) in steps"
          :key="index"
          class="text-sm font-medium"
          :class="index <= currentStep ? 'text-blue-600' : 'text-gray-400'"
        >
          {{ step.title }}
        </span>
      </div>
      <div class="h-2 bg-gray-200 rounded-full">
        <div
          class="h-2 bg-blue-600 rounded-full transition-all"
          :style="{ width: `${progressPercent}%` }"
        />
      </div>
    </div>

    <!-- Step Content -->
    <div class="bg-white rounded-lg border p-6">
      <transition name="slide" mode="out-in">
        <component
          :is="currentStepComponent"
          v-model="formData"
          :errors="errors"
          @validate="validateStep"
        />
      </transition>
    </div>

    <!-- Navigation -->
    <div class="flex justify-between mt-6">
      <Button
        v-if="currentStep > 0"
        label="Previous"
        @click="previousStep"
      />
      <div v-else />

      <Button
        v-if="currentStep < steps.length - 1"
        label="Next"
        theme="blue"
        variant="solid"
        @click="nextStep"
      />
      <Button
        v-else
        label="Submit"
        theme="blue"
        variant="solid"
        :loading="submitting"
        @click="submit"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, provide } from 'vue'
import { Button, toast } from 'frappe-ui'

const props = defineProps({
  steps: { type: Array, required: true },
  onSubmit: { type: Function, required: true }
})

const currentStep = ref(0)
const formData = reactive({})
const errors = reactive({})
const submitting = ref(false)

const progressPercent = computed(() =>
  ((currentStep.value + 1) / props.steps.length) * 100
)

const currentStepComponent = computed(() =>
  props.steps[currentStep.value].component
)

const validateStep = async () => {
  const step = props.steps[currentStep.value]
  if (step.validate) {
    const result = await step.validate(formData)
    return result === true
  }
  return true
}

const nextStep = async () => {
  if (await validateStep()) {
    if (currentStep.value < props.steps.length - 1) {
      currentStep.value++
    }
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const submit = async () => {
  if (await validateStep()) {
    submitting.value = true
    try {
      await props.onSubmit(formData)
      toast({ type: 'success', message: 'Form submitted!' })
    } catch (error) {
      toast({ type: 'error', message: error.message })
    } finally {
      submitting.value = false
    }
  }
}

// Provide form data to child steps
provide('formData', formData)
provide('errors', errors)
</script>

<style>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from {
  transform: translateX(30px);
  opacity: 0;
}
.slide-leave-to {
  transform: translateX(-30px);
  opacity: 0;
}
</style>
```

## Keyboard Shortcuts

### Keyboard Shortcut Manager

```javascript
// composables/useKeyboardShortcuts.js
import { onMounted, onUnmounted } from 'vue'

const shortcuts = new Map()

export function useKeyboardShortcuts(bindings) {
  const handleKeydown = (event) => {
    const key = getKeyCombo(event)
    const handler = shortcuts.get(key)

    if (handler) {
      event.preventDefault()
      handler(event)
    }
  }

  const getKeyCombo = (event) => {
    const parts = []
    if (event.ctrlKey || event.metaKey) parts.push('mod')
    if (event.shiftKey) parts.push('shift')
    if (event.altKey) parts.push('alt')
    parts.push(event.key.toLowerCase())
    return parts.join('+')
  }

  onMounted(() => {
    Object.entries(bindings).forEach(([key, handler]) => {
      shortcuts.set(key.toLowerCase(), handler)
    })

    document.addEventListener('keydown', handleKeydown)
  })

  onUnmounted(() => {
    Object.keys(bindings).forEach(key => {
      shortcuts.delete(key.toLowerCase())
    })

    document.removeEventListener('keydown', handleKeydown)
  })
}
```

Usage:

```vue
<script setup>
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'

useKeyboardShortcuts({
  'mod+s': () => save(),
  'mod+n': () => createNew(),
  'escape': () => closeDialog(),
  'mod+shift+d': () => duplicate()
})
</script>
```

## Performance Optimization

### Component Lazy Loading

```javascript
// router.js with code splitting
const routes = [
  {
    path: '/reports',
    component: () => import(
      /* webpackChunkName: "reports" */
      './pages/Reports.vue'
    )
  },
  {
    path: '/analytics',
    component: () => import(
      /* webpackChunkName: "analytics" */
      './pages/Analytics.vue'
    )
  }
]
```

### Virtual Scrolling for Large Lists

```vue
<template>
  <div
    ref="containerRef"
    class="h-96 overflow-auto"
    @scroll="onScroll"
  >
    <div :style="{ height: `${totalHeight}px`, position: 'relative' }">
      <div
        v-for="item in visibleItems"
        :key="item.name"
        :style="{
          position: 'absolute',
          top: `${item._top}px`,
          height: `${itemHeight}px`,
          width: '100%'
        }"
      >
        <slot :item="item" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  items: { type: Array, required: true },
  itemHeight: { type: Number, default: 60 },
  overscan: { type: Number, default: 5 }
})

const containerRef = ref(null)
const scrollTop = ref(0)

const totalHeight = computed(() => props.items.length * props.itemHeight)

const visibleItems = computed(() => {
  const containerHeight = containerRef.value?.clientHeight || 400
  const startIndex = Math.max(0,
    Math.floor(scrollTop.value / props.itemHeight) - props.overscan
  )
  const endIndex = Math.min(
    props.items.length,
    Math.ceil((scrollTop.value + containerHeight) / props.itemHeight) + props.overscan
  )

  return props.items.slice(startIndex, endIndex).map((item, i) => ({
    ...item,
    _top: (startIndex + i) * props.itemHeight
  }))
})

const onScroll = (event) => {
  scrollTop.value = event.target.scrollTop
}
</script>
```

## Plugin Architecture

### Creating a frappe-ui Plugin

```javascript
// plugins/myPlugin.js
export default {
  install(app, options = {}) {
    // Add global components
    app.component('MyComponent', MyComponent)

    // Add global properties
    app.config.globalProperties.$myHelper = myHelper

    // Add global mixin
    app.mixin({
      created() {
        // Run on every component creation
      }
    })

    // Add directive
    app.directive('focus', {
      mounted(el) {
        el.focus()
      }
    })

    // Provide global state
    app.provide('myPluginOptions', options)
  }
}

// Usage in main.js
import MyPlugin from './plugins/myPlugin'
app.use(MyPlugin, { option1: 'value' })
```

## Common Pitfalls

### 1. Memory Leaks in Composables

**Problem:** Resources keep fetching after component unmount.

**Solution:** Clean up in `onUnmounted`:
```javascript
let resource = null

export function useMyResource() {
  if (!resource) {
    resource = createResource({ ... })
  }
  return resource
}

// In component
onUnmounted(() => {
  resource?.reset()
})
```

### 2. Stale Closures

**Problem:** Event handlers capture old values.

**Solution:** Use refs or watch:
```javascript
// Wrong
const count = ref(0)
onClick(() => console.log(count.value)) // Always logs old value

// Correct
watch(count, (newCount) => {
  // Use newCount here
})
```

### 3. Over-fetching

**Problem:** Multiple components fetch same data.

**Solution:** Use caching and shared composables:
```javascript
const CACHE_KEY = 'shared-data'

export function useSharedData() {
  let resource = getCachedResource(CACHE_KEY)
  if (!resource) {
    resource = createResource({
      cache: CACHE_KEY,
      auto: true
    })
  }
  return resource
}
```

## Next Steps

- Explore [Testing Strategies](./17-testing.md)
- Learn about [Deployment](./18-deployment.md)
- Review [Security Best Practices](./19-security.md)
