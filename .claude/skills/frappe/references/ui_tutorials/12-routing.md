# Vue Router Integration Tutorial

## Overview

This tutorial covers integrating Vue Router with frappe-ui applications, including route configuration, navigation guards for authentication, and best practices for Frappe-based SPAs.

## Basic Setup

### Install Vue Router

```bash
npm install vue-router@4
# or
yarn add vue-router@4
```

### Router Configuration

```javascript
// src/router.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./pages/Home.vue')
  },
  {
    path: '/customers',
    name: 'CustomerList',
    component: () => import('./pages/customers/CustomerList.vue')
  },
  {
    path: '/customers/:name',
    name: 'CustomerDetail',
    component: () => import('./pages/customers/CustomerDetail.vue'),
    props: true
  },
  {
    path: '/customers/:name/edit',
    name: 'CustomerEdit',
    component: () => import('./pages/customers/CustomerEdit.vue'),
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('./pages/NotFound.vue')
  }
]

const router = createRouter({
  // Base URL for your frontend app
  history: createWebHistory('/frontend'),
  routes
})

export default router
```

### Main.js Integration

```javascript
// src/main.js
import { createApp } from 'vue'
import { FrappeUI, setConfig, frappeRequest } from 'frappe-ui'
import router from './router'
import App from './App.vue'
import './index.css'

const app = createApp(App)

app.use(FrappeUI)
app.use(router)

setConfig('resourceFetcher', frappeRequest)

app.mount('#app')
```

### App.vue with Router View

```vue
<!-- src/App.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <main class="container mx-auto px-4 py-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

## Navigation

### Programmatic Navigation

```vue
<script setup>
import { useRouter, useRoute } from 'vue-router'
import { Button } from 'frappe-ui'

const router = useRouter()
const route = useRoute()

// Navigate to a route
const goToCustomer = (name) => {
  router.push(`/customers/${name}`)
}

// Navigate with route name and params
const editCustomer = (name) => {
  router.push({
    name: 'CustomerEdit',
    params: { name }
  })
}

// Navigate with query params
const filterCustomers = (territory) => {
  router.push({
    name: 'CustomerList',
    query: { territory }
  })
}

// Go back
const goBack = () => {
  router.back()
}

// Replace current history entry
const replaceRoute = () => {
  router.replace('/customers')
}
</script>
```

### Router Links with Button Component

```vue
<template>
  <div class="space-x-2">
    <!-- Button with route prop -->
    <Button
      label="Go to Dashboard"
      route="/dashboard"
    />

    <!-- Button with route object -->
    <Button
      label="View Customer"
      :route="{ name: 'CustomerDetail', params: { name: 'CUST-001' } }"
    />

    <!-- Using router-link directly -->
    <router-link
      to="/customers"
      custom
      v-slot="{ navigate }"
    >
      <Button label="Customers" @click="navigate" />
    </router-link>
  </div>
</template>
```

## Authentication Guard

### Session Check

```javascript
// src/composables/useSession.js
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

const sessionUser = ref(null)
const sessionLoading = ref(true)

const session = createResource({
  url: 'frappe.auth.get_logged_user',
  auto: true,
  onSuccess(user) {
    sessionUser.value = user
    sessionLoading.value = false
  },
  onError() {
    sessionUser.value = null
    sessionLoading.value = false
  }
})

export function useSession() {
  const isLoggedIn = computed(() => {
    return sessionUser.value && sessionUser.value !== 'Guest'
  })

  const user = computed(() => sessionUser.value)
  const loading = computed(() => sessionLoading.value)

  const logout = async () => {
    const logoutResource = createResource({
      url: 'frappe.handler.logout'
    })
    await logoutResource.submit()
    sessionUser.value = null
    window.location.href = '/login'
  }

  return {
    user,
    isLoggedIn,
    loading,
    logout,
    reload: () => session.reload()
  }
}
```

### Navigation Guards

```javascript
// src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import { useSession } from './composables/useSession'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('./pages/Home.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('./pages/Settings.vue'),
    meta: { requiresRole: 'System Manager' }
  }
]

const router = createRouter({
  history: createWebHistory('/frontend'),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const { isLoggedIn, loading, user } = useSession()

  // Wait for session check to complete
  while (loading.value) {
    await new Promise(resolve => setTimeout(resolve, 50))
  }

  // Public routes
  if (to.meta.public) {
    // Redirect logged-in users away from login page
    if (isLoggedIn.value && to.name === 'Login') {
      return next({ name: 'Home' })
    }
    return next()
  }

  // Protected routes - require login
  if (!isLoggedIn.value) {
    return next({
      name: 'Login',
      query: { redirect: to.fullPath }
    })
  }

  // Role-based access
  if (to.meta.requiresRole) {
    // You would need to fetch user roles
    // For simplicity, we'll skip this check
  }

  next()
})

export default router
```

### Login Page

```vue
<!-- src/pages/Login.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="max-w-md w-full p-8 bg-white rounded-lg shadow-lg">
      <h1 class="text-2xl font-bold text-center mb-6">Login</h1>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <FormControl
          v-model="form.email"
          type="email"
          label="Email"
          required
        />

        <FormControl
          v-model="form.password"
          type="password"
          label="Password"
          required
        />

        <Button
          type="submit"
          label="Login"
          theme="blue"
          variant="solid"
          class="w-full"
          :loading="loginResource.loading"
        />
      </form>

      <div v-if="error" class="mt-4 p-3 bg-red-50 text-red-600 rounded">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { createResource, FormControl, Button } from 'frappe-ui'
import { useSession } from '../composables/useSession'

const router = useRouter()
const route = useRoute()
const { reload: reloadSession } = useSession()

const form = reactive({
  email: '',
  password: ''
})

const error = ref('')

const loginResource = createResource({
  url: 'frappe.auth.login',
  onSuccess() {
    reloadSession()
    // Redirect to intended page or home
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  },
  onError(err) {
    error.value = err.messages?.[0] || 'Login failed'
  }
})

const handleLogin = () => {
  error.value = ''
  loginResource.submit({
    usr: form.email,
    pwd: form.password
  })
}
</script>
```

## Dynamic Route Parameters

### Customer Detail Page

```vue
<!-- src/pages/customers/CustomerDetail.vue -->
<template>
  <div class="max-w-4xl mx-auto">
    <!-- Breadcrumb -->
    <Breadcrumbs :items="breadcrumbs" />

    <div v-if="customer.get?.loading" class="py-12 text-center">
      <Spinner class="mx-auto" />
    </div>

    <div v-else-if="customer.doc" class="mt-6">
      <div class="flex justify-between items-start">
        <div>
          <h1 class="text-2xl font-bold">{{ customer.doc.customer_name }}</h1>
          <Badge :theme="customer.doc.disabled ? 'red' : 'green'" class="mt-2">
            {{ customer.doc.disabled ? 'Disabled' : 'Active' }}
          </Badge>
        </div>

        <div class="space-x-2">
          <Button
            label="Edit"
            :route="{ name: 'CustomerEdit', params: { name: props.name } }"
          />
          <Button
            label="Delete"
            theme="red"
            @click="handleDelete"
          />
        </div>
      </div>

      <div class="mt-6 grid grid-cols-2 gap-6">
        <div>
          <h3 class="text-sm text-gray-500">Customer Type</h3>
          <p class="mt-1">{{ customer.doc.customer_type }}</p>
        </div>
        <div>
          <h3 class="text-sm text-gray-500">Territory</h3>
          <p class="mt-1">{{ customer.doc.territory || '-' }}</p>
        </div>
        <div>
          <h3 class="text-sm text-gray-500">Email</h3>
          <p class="mt-1">{{ customer.doc.email_id || '-' }}</p>
        </div>
        <div>
          <h3 class="text-sm text-gray-500">Phone</h3>
          <p class="mt-1">{{ customer.doc.mobile_no || '-' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  createDocumentResource,
  Breadcrumbs,
  Badge,
  Button,
  Spinner,
  toast
} from 'frappe-ui'

const props = defineProps({
  name: {
    type: String,
    required: true
  }
})

const router = useRouter()

const breadcrumbs = computed(() => [
  { label: 'Customers', route: '/customers' },
  { label: props.name }
])

const customer = createDocumentResource({
  doctype: 'Customer',
  name: props.name,

  delete: {
    onSuccess() {
      toast({ type: 'success', message: 'Customer deleted' })
      router.push('/customers')
    }
  }
})

// Reload when route param changes
watch(() => props.name, (newName) => {
  customer.update({ name: newName })
})

const handleDelete = () => {
  if (confirm('Delete this customer?')) {
    customer.delete.submit()
  }
}
</script>
```

## Query Parameters

### Filtered List with Query Params

```vue
<!-- src/pages/customers/CustomerList.vue -->
<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Customers</h1>
      <Button
        label="Add Customer"
        theme="blue"
        variant="solid"
        route="/customers/new"
      />
    </div>

    <!-- Filters -->
    <div class="flex gap-4 mb-4">
      <TextInput
        v-model="filters.search"
        placeholder="Search..."
        :debounce="300"
        @update:model-value="updateFilters"
      />

      <Select
        v-model="filters.territory"
        :options="territoryOptions"
        placeholder="All Territories"
        @update:model-value="updateFilters"
      />
    </div>

    <ListView
      :columns="columns"
      :rows="customers.data || []"
      :loading="customers.loading"
      row-key="name"
      @row-click="viewCustomer"
    />
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  createListResource,
  ListView,
  Button,
  TextInput,
  Select
} from 'frappe-ui'

const router = useRouter()
const route = useRoute()

const territoryOptions = [
  { label: 'All Territories', value: '' },
  { label: 'India', value: 'India' },
  { label: 'USA', value: 'USA' }
]

const filters = reactive({
  search: '',
  territory: ''
})

const columns = [
  { label: 'ID', key: 'name', width: '120px' },
  { label: 'Customer Name', key: 'customer_name' },
  { label: 'Territory', key: 'territory', width: '150px' }
]

const customers = createListResource({
  doctype: 'Customer',
  fields: ['name', 'customer_name', 'territory'],
  pageLength: 20,
  auto: true
})

// Initialize filters from URL
onMounted(() => {
  if (route.query.search) {
    filters.search = route.query.search
  }
  if (route.query.territory) {
    filters.territory = route.query.territory
  }
  applyFilters()
})

// Update URL when filters change
const updateFilters = () => {
  const query = {}
  if (filters.search) query.search = filters.search
  if (filters.territory) query.territory = filters.territory

  router.push({ query })
  applyFilters()
}

// Apply filters to resource
const applyFilters = () => {
  const f = []
  if (filters.search) {
    f.push(['customer_name', 'like', `%${filters.search}%`])
  }
  if (filters.territory) {
    f.push(['territory', '=', filters.territory])
  }
  customers.update({ filters: f, start: 0 })
}

// Watch URL changes (back/forward navigation)
watch(() => route.query, (newQuery) => {
  filters.search = newQuery.search || ''
  filters.territory = newQuery.territory || ''
  applyFilters()
})

const viewCustomer = (row) => {
  router.push(`/customers/${row.name}`)
}
</script>
```

## Nested Routes

### Layout with Sidebar

```javascript
// router.js
const routes = [
  {
    path: '/settings',
    component: () => import('./pages/settings/SettingsLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/settings/profile'
      },
      {
        path: 'profile',
        name: 'SettingsProfile',
        component: () => import('./pages/settings/Profile.vue')
      },
      {
        path: 'account',
        name: 'SettingsAccount',
        component: () => import('./pages/settings/Account.vue')
      },
      {
        path: 'notifications',
        name: 'SettingsNotifications',
        component: () => import('./pages/settings/Notifications.vue')
      }
    ]
  }
]
```

```vue
<!-- src/pages/settings/SettingsLayout.vue -->
<template>
  <div class="flex gap-8">
    <!-- Sidebar -->
    <aside class="w-64 shrink-0">
      <nav class="space-y-1">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="block px-4 py-2 rounded-lg transition-colors"
          :class="[
            isActive(item.path)
              ? 'bg-blue-50 text-blue-700'
              : 'text-gray-600 hover:bg-gray-100'
          ]"
        >
          {{ item.label }}
        </router-link>
      </nav>
    </aside>

    <!-- Content -->
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const menuItems = [
  { label: 'Profile', path: '/settings/profile' },
  { label: 'Account', path: '/settings/account' },
  { label: 'Notifications', path: '/settings/notifications' }
]

const isActive = (path) => {
  return route.path === path
}
</script>
```

## Common Pitfalls

### 1. Base URL Mismatch

**Problem:** Routes don't work after deployment.

**Solution:** Set correct base URL:
```javascript
createWebHistory('/frontend')  // Match your app's URL
```

### 2. Props Not Reactive

**Problem:** Component doesn't update when route params change.

**Solution:** Watch the props:
```javascript
const props = defineProps(['name'])

const customer = createDocumentResource({
  doctype: 'Customer',
  name: props.name
})

watch(() => props.name, (newName) => {
  customer.update({ name: newName })
})
```

### 3. Session Check Race Condition

**Problem:** User briefly sees protected content before redirect.

**Solution:** Show loading state until session is verified:
```vue
<template>
  <div v-if="sessionLoading">
    <Spinner />
  </div>
  <router-view v-else />
</template>
```

## Next Steps

- Learn about [State Management](./13-state-management.md)
- Explore [Realtime Updates](./14-realtime-updates.md)
- Build [Complete SPA](./15-complete-spa-example.md)
