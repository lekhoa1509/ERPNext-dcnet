# Building a Complete SPA Example

## Overview

This tutorial walks through building a complete Task Management SPA using frappe-ui. We'll implement authentication, CRUD operations, routing, realtime updates, and all the patterns covered in previous tutorials.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.vue
│   │   ├── TaskCard.vue
│   │   ├── TaskForm.vue
│   │   └── EmptyState.vue
│   ├── composables/
│   │   ├── useSession.js
│   │   └── useTasks.js
│   ├── pages/
│   │   ├── Login.vue
│   │   ├── Dashboard.vue
│   │   ├── TaskList.vue
│   │   ├── TaskDetail.vue
│   │   └── NotFound.vue
│   ├── App.vue
│   ├── main.js
│   ├── router.js
│   └── index.css
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Main Entry Point

```javascript
// src/main.js
import { createApp } from 'vue'
import {
  FrappeUI,
  setConfig,
  frappeRequest,
  initSocket
} from 'frappe-ui'
import router from './router'
import App from './App.vue'
import './index.css'

const app = createApp(App)

// Configure frappe-ui
app.use(FrappeUI)
setConfig('resourceFetcher', frappeRequest)

// Initialize Socket.IO for realtime
const socket = initSocket()
app.provide('$socket', socket)

// Use router
app.use(router)

app.mount('#app')
```

## Router Configuration

```javascript
// src/router.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('./pages/Dashboard.vue')
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: () => import('./pages/TaskList.vue')
  },
  {
    path: '/tasks/:name',
    name: 'TaskDetail',
    component: () => import('./pages/TaskDetail.vue'),
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('./pages/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory('/tasks'),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const { useSession } = await import('./composables/useSession')
  const { isAuthenticated, isLoading } = useSession()

  // Wait for session check
  while (isLoading.value) {
    await new Promise(resolve => setTimeout(resolve, 50))
  }

  // Public routes
  if (to.meta.public) {
    if (isAuthenticated.value && to.name === 'Login') {
      return next({ name: 'Dashboard' })
    }
    return next()
  }

  // Protected routes
  if (!isAuthenticated.value) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  next()
})

export default router
```

## Session Composable

```javascript
// src/composables/useSession.js
import { ref, computed, readonly } from 'vue'
import { createResource } from 'frappe-ui'

const user = ref(null)
const userDetails = ref(null)
const isLoading = ref(true)

// Check session
const sessionResource = createResource({
  url: 'frappe.auth.get_logged_user',
  auto: true,
  onSuccess(data) {
    if (data && data !== 'Guest') {
      user.value = data
      fetchUserDetails()
    } else {
      user.value = null
      isLoading.value = false
    }
  },
  onError() {
    user.value = null
    isLoading.value = false
  }
})

const fetchUserDetails = async () => {
  const resource = createResource({
    url: 'frappe.client.get',
    params: { doctype: 'User', name: user.value }
  })
  await resource.fetch()
  userDetails.value = resource.data
  isLoading.value = false
}

export function useSession() {
  const isAuthenticated = computed(() => !!user.value && user.value !== 'Guest')

  const login = async (email, password) => {
    const loginResource = createResource({ url: 'frappe.auth.login' })
    const result = await loginResource.submit({ usr: email, pwd: password })
    sessionResource.reload()
    return result
  }

  const logout = async () => {
    const logoutResource = createResource({ url: 'frappe.handler.logout' })
    await logoutResource.submit()
    user.value = null
    userDetails.value = null
    window.location.href = '/tasks/login'
  }

  return {
    user: readonly(user),
    userDetails: readonly(userDetails),
    isAuthenticated,
    isLoading: readonly(isLoading),
    login,
    logout,
    reload: () => sessionResource.reload()
  }
}
```

## Tasks Composable

```javascript
// src/composables/useTasks.js
import { computed } from 'vue'
import { createListResource, toast } from 'frappe-ui'

const CACHE_KEY = 'task-list'

let tasks = null

export function useTasks() {
  if (!tasks) {
    tasks = createListResource({
      doctype: 'Task',
      fields: [
        'name', 'subject', 'status', 'priority',
        'description', 'exp_end_date', 'owner'
      ],
      orderBy: 'modified desc',
      pageLength: 50,
      cache: CACHE_KEY,
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
        }
      },

      delete: {
        onSuccess() {
          toast({ type: 'success', message: 'Task deleted!' })
        }
      }
    })
  }

  const openTasks = computed(() =>
    (tasks.data || []).filter(t => t.status === 'Open')
  )

  const completedTasks = computed(() =>
    (tasks.data || []).filter(t => t.status === 'Completed')
  )

  const tasksByPriority = computed(() => {
    const grouped = { High: [], Medium: [], Low: [] }
    ;(tasks.data || []).forEach(task => {
      if (grouped[task.priority]) {
        grouped[task.priority].push(task)
      }
    })
    return grouped
  })

  const getTask = (name) => tasks.data?.find(t => t.name === name)

  return {
    tasks,
    openTasks,
    completedTasks,
    tasksByPriority,
    getTask
  }
}
```

## App Component

```vue
<!-- src/App.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar v-if="isAuthenticated" />

    <main class="container mx-auto px-4 py-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <Suspense>
            <component :is="Component" />
            <template #fallback>
              <div class="flex justify-center py-12">
                <Spinner class="w-8 h-8" />
              </div>
            </template>
          </Suspense>
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { useSession } from './composables/useSession'
import Navbar from './components/Navbar.vue'
import { Spinner } from 'frappe-ui'

const { isAuthenticated } = useSession()
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

## Navbar Component

```vue
<!-- src/components/Navbar.vue -->
<template>
  <nav class="bg-white border-b">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center gap-8">
          <router-link to="/" class="text-xl font-bold text-blue-600">
            TaskApp
          </router-link>

          <div class="flex gap-4">
            <router-link
              to="/"
              class="px-3 py-2 rounded-lg transition-colors"
              :class="[
                $route.name === 'Dashboard'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              ]"
            >
              Dashboard
            </router-link>

            <router-link
              to="/tasks"
              class="px-3 py-2 rounded-lg transition-colors"
              :class="[
                $route.name === 'TaskList'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              ]"
            >
              Tasks
            </router-link>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <Avatar :label="userDetails?.full_name || user" size="sm" />
            <span class="text-sm font-medium">
              {{ userDetails?.full_name || user }}
            </span>
          </div>

          <Button
            icon="log-out"
            variant="ghost"
            @click="logout"
          />
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useSession } from '../composables/useSession'
import { Avatar, Button } from 'frappe-ui'

const { user, userDetails, logout } = useSession()
</script>
```

## Login Page

```vue
<!-- src/pages/Login.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full p-8 bg-white rounded-xl shadow-lg">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-blue-600">TaskApp</h1>
        <p class="text-gray-500 mt-2">Sign in to manage your tasks</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <FormControl
          v-model="form.email"
          type="email"
          label="Email"
          placeholder="you@example.com"
          required
        />

        <FormControl
          v-model="form.password"
          type="password"
          label="Password"
          placeholder="Enter your password"
          required
        />

        <Button
          type="submit"
          label="Sign In"
          theme="blue"
          variant="solid"
          class="w-full"
          :loading="isLoggingIn"
        />
      </form>

      <Alert
        v-if="error"
        :title="error"
        theme="red"
        class="mt-4"
      />
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { FormControl, Button, Alert } from 'frappe-ui'
import { useSession } from '../composables/useSession'

const router = useRouter()
const route = useRoute()
const { login } = useSession()

const form = reactive({
  email: '',
  password: ''
})

const isLoggingIn = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  isLoggingIn.value = true

  try {
    await login(form.email, form.password)
    router.push(route.query.redirect || '/')
  } catch (err) {
    error.value = err.messages?.[0] || 'Invalid credentials'
  } finally {
    isLoggingIn.value = false
  }
}
</script>
```

## Dashboard Page

```vue
<!-- src/pages/Dashboard.vue -->
<template>
  <div>
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-2xl font-bold">Dashboard</h1>
      <Button
        label="New Task"
        theme="blue"
        variant="solid"
        icon-left="plus"
        @click="showNewTaskDialog = true"
      />
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white p-6 rounded-lg shadow-sm border">
        <p class="text-sm text-gray-500">Total Tasks</p>
        <p class="text-3xl font-bold mt-1">{{ tasks.data?.length || 0 }}</p>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-sm border">
        <p class="text-sm text-gray-500">Open</p>
        <p class="text-3xl font-bold text-blue-600 mt-1">{{ openTasks.length }}</p>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-sm border">
        <p class="text-sm text-gray-500">Completed</p>
        <p class="text-3xl font-bold text-green-600 mt-1">{{ completedTasks.length }}</p>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-sm border">
        <p class="text-sm text-gray-500">High Priority</p>
        <p class="text-3xl font-bold text-red-600 mt-1">
          {{ tasksByPriority.High?.length || 0 }}
        </p>
      </div>
    </div>

    <!-- Recent Tasks -->
    <div class="bg-white rounded-lg shadow-sm border">
      <div class="px-6 py-4 border-b flex justify-between items-center">
        <h2 class="text-lg font-medium">Recent Tasks</h2>
        <Button label="View All" variant="ghost" route="/tasks" />
      </div>

      <div v-if="tasks.loading" class="p-8 text-center">
        <Spinner />
      </div>

      <div v-else-if="!tasks.data?.length" class="p-8 text-center text-gray-500">
        No tasks yet. Create your first task!
      </div>

      <div v-else class="divide-y">
        <TaskCard
          v-for="task in recentTasks"
          :key="task.name"
          :task="task"
          @click="router.push(`/tasks/${task.name}`)"
        />
      </div>
    </div>

    <!-- New Task Dialog -->
    <TaskForm
      v-model:show="showNewTaskDialog"
      @created="tasks.reload()"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Spinner } from 'frappe-ui'
import { useTasks } from '../composables/useTasks'
import TaskCard from '../components/TaskCard.vue'
import TaskForm from '../components/TaskForm.vue'

const router = useRouter()
const { tasks, openTasks, completedTasks, tasksByPriority } = useTasks()

const showNewTaskDialog = ref(false)

const recentTasks = computed(() => {
  return (tasks.data || []).slice(0, 5)
})
</script>
```

## Task List Page

```vue
<!-- src/pages/TaskList.vue -->
<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Tasks</h1>
      <Button
        label="New Task"
        theme="blue"
        variant="solid"
        icon-left="plus"
        @click="showNewTaskDialog = true"
      />
    </div>

    <!-- Filters -->
    <div class="flex gap-4 mb-6">
      <TextInput
        v-model="searchQuery"
        placeholder="Search tasks..."
        :debounce="300"
        class="w-64"
      >
        <template #prefix>
          <FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
        </template>
      </TextInput>

      <Select
        v-model="statusFilter"
        :options="statusOptions"
        class="w-40"
      />

      <Select
        v-model="priorityFilter"
        :options="priorityOptions"
        class="w-40"
      />
    </div>

    <!-- Task List -->
    <div class="bg-white rounded-lg shadow-sm border">
      <div v-if="tasks.loading && !tasks.data?.length" class="p-12 text-center">
        <Spinner class="mx-auto" />
      </div>

      <EmptyState
        v-else-if="filteredTasks.length === 0"
        title="No tasks found"
        description="Try adjusting your filters or create a new task"
        :action="{ label: 'New Task', onClick: () => showNewTaskDialog = true }"
      />

      <div v-else class="divide-y">
        <TaskCard
          v-for="task in filteredTasks"
          :key="task.name"
          :task="task"
          @click="router.push(`/tasks/${task.name}`)"
          @status-change="updateTaskStatus"
        />
      </div>
    </div>

    <TaskForm
      v-model:show="showNewTaskDialog"
      @created="tasks.reload()"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { TextInput, Select, Spinner, FeatherIcon } from 'frappe-ui'
import { useTasks } from '../composables/useTasks'
import TaskCard from '../components/TaskCard.vue'
import TaskForm from '../components/TaskForm.vue'
import EmptyState from '../components/EmptyState.vue'

const router = useRouter()
const { tasks } = useTasks()

const showNewTaskDialog = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')

const statusOptions = [
  { label: 'All Status', value: '' },
  { label: 'Open', value: 'Open' },
  { label: 'Working', value: 'Working' },
  { label: 'Completed', value: 'Completed' },
  { label: 'Cancelled', value: 'Cancelled' }
]

const priorityOptions = [
  { label: 'All Priority', value: '' },
  { label: 'High', value: 'High' },
  { label: 'Medium', value: 'Medium' },
  { label: 'Low', value: 'Low' }
]

const filteredTasks = computed(() => {
  return (tasks.data || []).filter(task => {
    const matchesSearch = !searchQuery.value ||
      task.subject.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = !statusFilter.value || task.status === statusFilter.value
    const matchesPriority = !priorityFilter.value || task.priority === priorityFilter.value

    return matchesSearch && matchesStatus && matchesPriority
  })
})

const updateTaskStatus = (taskName, newStatus) => {
  tasks.setValue.submit({ name: taskName, status: newStatus })
}
</script>
```

## Task Detail Page

```vue
<!-- src/pages/TaskDetail.vue -->
<template>
  <div v-if="task.get?.loading" class="py-12 text-center">
    <Spinner class="mx-auto" />
  </div>

  <div v-else-if="task.doc" class="max-w-3xl">
    <!-- Breadcrumb -->
    <div class="flex items-center gap-2 text-sm text-gray-500 mb-6">
      <router-link to="/tasks" class="hover:text-gray-700">Tasks</router-link>
      <span>/</span>
      <span>{{ task.doc.name }}</span>
    </div>

    <!-- Header -->
    <div class="flex justify-between items-start mb-6">
      <div>
        <h1 class="text-2xl font-bold">{{ task.doc.subject }}</h1>
        <div class="flex items-center gap-3 mt-2">
          <Badge :theme="getStatusTheme(task.doc.status)">
            {{ task.doc.status }}
          </Badge>
          <Badge :theme="getPriorityTheme(task.doc.priority)" variant="outline">
            {{ task.doc.priority }} Priority
          </Badge>
        </div>
      </div>

      <div class="flex gap-2">
        <Button
          label="Edit"
          icon-left="edit"
          @click="showEditDialog = true"
        />
        <Button
          icon="trash"
          theme="red"
          variant="ghost"
          @click="handleDelete"
        />
      </div>
    </div>

    <!-- Content -->
    <div class="bg-white rounded-lg shadow-sm border p-6 space-y-6">
      <div v-if="task.doc.description">
        <h3 class="text-sm font-medium text-gray-500 mb-2">Description</h3>
        <p class="text-gray-700 whitespace-pre-wrap">{{ task.doc.description }}</p>
      </div>

      <div class="grid grid-cols-2 gap-6">
        <div>
          <h3 class="text-sm font-medium text-gray-500 mb-1">Due Date</h3>
          <p>{{ task.doc.exp_end_date || 'Not set' }}</p>
        </div>

        <div>
          <h3 class="text-sm font-medium text-gray-500 mb-1">Assigned To</h3>
          <div class="flex items-center gap-2">
            <Avatar :label="task.doc.owner" size="sm" />
            <span>{{ task.doc.owner }}</span>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="pt-4 border-t">
        <h3 class="text-sm font-medium text-gray-500 mb-3">Quick Actions</h3>
        <div class="flex gap-2">
          <Button
            v-if="task.doc.status !== 'Completed'"
            label="Mark Complete"
            theme="green"
            variant="outline"
            @click="markComplete"
          />
          <Button
            v-if="task.doc.status === 'Open'"
            label="Start Working"
            theme="blue"
            variant="outline"
            @click="startWorking"
          />
        </div>
      </div>
    </div>

    <!-- Edit Dialog -->
    <TaskForm
      v-model:show="showEditDialog"
      :task="task.doc"
      @updated="task.reload()"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  createDocumentResource,
  Badge,
  Button,
  Avatar,
  Spinner,
  toast
} from 'frappe-ui'
import TaskForm from '../components/TaskForm.vue'

const props = defineProps({
  name: { type: String, required: true }
})

const router = useRouter()
const showEditDialog = ref(false)

const task = createDocumentResource({
  doctype: 'Task',
  name: props.name,

  setValue: {
    onSuccess() {
      toast({ type: 'success', message: 'Task updated!' })
    }
  },

  delete: {
    onSuccess() {
      toast({ type: 'success', message: 'Task deleted!' })
      router.push('/tasks')
    }
  }
})

// Reload when route param changes
watch(() => props.name, (newName) => {
  task.update({ name: newName })
})

const getStatusTheme = (status) => ({
  'Open': 'blue',
  'Working': 'orange',
  'Completed': 'green',
  'Cancelled': 'gray'
}[status] || 'gray')

const getPriorityTheme = (priority) => ({
  'High': 'red',
  'Medium': 'orange',
  'Low': 'gray'
}[priority] || 'gray')

const markComplete = () => {
  task.setValue.submit({ status: 'Completed' })
}

const startWorking = () => {
  task.setValue.submit({ status: 'Working' })
}

const handleDelete = () => {
  if (confirm('Delete this task?')) {
    task.delete.submit()
  }
}
</script>
```

## Task Card Component

```vue
<!-- src/components/TaskCard.vue -->
<template>
  <div
    class="px-6 py-4 hover:bg-gray-50 cursor-pointer transition-colors"
    @click="$emit('click')"
  >
    <div class="flex justify-between items-start">
      <div class="flex-1">
        <h3 class="font-medium">{{ task.subject }}</h3>
        <p v-if="task.description" class="text-sm text-gray-500 mt-1 line-clamp-1">
          {{ task.description }}
        </p>
      </div>

      <div class="flex items-center gap-3 ml-4">
        <Badge :theme="getPriorityTheme(task.priority)" size="sm">
          {{ task.priority }}
        </Badge>

        <Select
          :model-value="task.status"
          :options="statusOptions"
          size="sm"
          @update:model-value="$emit('status-change', task.name, $event)"
          @click.stop
        />
      </div>
    </div>

    <div class="flex items-center gap-4 mt-3 text-sm text-gray-500">
      <div class="flex items-center gap-1">
        <FeatherIcon name="calendar" class="w-4 h-4" />
        <span>{{ task.exp_end_date || 'No due date' }}</span>
      </div>

      <div class="flex items-center gap-1">
        <Avatar :label="task.owner" size="xs" />
        <span>{{ task.owner.split('@')[0] }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Badge, Select, Avatar, FeatherIcon } from 'frappe-ui'

defineProps({
  task: { type: Object, required: true }
})

defineEmits(['click', 'status-change'])

const statusOptions = [
  { label: 'Open', value: 'Open' },
  { label: 'Working', value: 'Working' },
  { label: 'Completed', value: 'Completed' },
  { label: 'Cancelled', value: 'Cancelled' }
]

const getPriorityTheme = (priority) => ({
  'High': 'red',
  'Medium': 'orange',
  'Low': 'gray'
}[priority] || 'gray')
</script>
```

## Task Form Component

```vue
<!-- src/components/TaskForm.vue -->
<template>
  <Dialog
    v-model="show"
    :options="{
      title: task ? 'Edit Task' : 'New Task',
      size: 'lg'
    }"
  >
    <template #body-content>
      <form class="space-y-4">
        <FormControl
          v-model="form.subject"
          label="Subject"
          required
        />

        <div class="grid grid-cols-2 gap-4">
          <FormControl
            v-model="form.status"
            type="select"
            label="Status"
            :options="statusOptions"
          />

          <FormControl
            v-model="form.priority"
            type="select"
            label="Priority"
            :options="priorityOptions"
          />
        </div>

        <FormControl
          v-model="form.exp_end_date"
          type="date"
          label="Due Date"
        />

        <FormControl
          v-model="form.description"
          type="textarea"
          label="Description"
          rows="4"
        />
      </form>
    </template>

    <template #actions="{ close }">
      <Button label="Cancel" @click="close" />
      <Button
        :label="task ? 'Update' : 'Create'"
        theme="blue"
        variant="solid"
        :loading="saving"
        @click="handleSubmit(close)"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { Dialog, FormControl, Button, createResource, toast } from 'frappe-ui'

const props = defineProps({
  show: Boolean,
  task: Object
})

const emit = defineEmits(['update:show', 'created', 'updated'])

const show = computed({
  get: () => props.show,
  set: (val) => emit('update:show', val)
})

const saving = ref(false)

const initialForm = {
  subject: '',
  status: 'Open',
  priority: 'Medium',
  exp_end_date: '',
  description: ''
}

const form = reactive({ ...initialForm })

const statusOptions = [
  { label: 'Open', value: 'Open' },
  { label: 'Working', value: 'Working' },
  { label: 'Completed', value: 'Completed' }
]

const priorityOptions = [
  { label: 'Low', value: 'Low' },
  { label: 'Medium', value: 'Medium' },
  { label: 'High', value: 'High' }
]

// Populate form when editing
watch(() => props.task, (task) => {
  if (task) {
    Object.assign(form, {
      subject: task.subject,
      status: task.status,
      priority: task.priority,
      exp_end_date: task.exp_end_date || '',
      description: task.description || ''
    })
  } else {
    Object.assign(form, initialForm)
  }
}, { immediate: true })

const createTask = createResource({ url: 'frappe.client.insert' })
const updateTask = createResource({ url: 'frappe.client.set_value' })

const handleSubmit = async (close) => {
  if (!form.subject.trim()) {
    toast({ type: 'error', message: 'Subject is required' })
    return
  }

  saving.value = true

  try {
    if (props.task) {
      await updateTask.submit({
        doctype: 'Task',
        name: props.task.name,
        fieldname: form
      })
      emit('updated')
    } else {
      await createTask.submit({
        doc: { doctype: 'Task', ...form }
      })
      emit('created')
    }
    close()
  } catch (error) {
    toast({ type: 'error', message: error.messages?.[0] || 'Failed' })
  } finally {
    saving.value = false
  }
}
</script>
```

## Empty State Component

```vue
<!-- src/components/EmptyState.vue -->
<template>
  <div class="p-12 text-center">
    <FeatherIcon :name="icon" class="w-12 h-12 mx-auto text-gray-300" />
    <h3 class="mt-4 text-lg font-medium text-gray-900">{{ title }}</h3>
    <p v-if="description" class="mt-2 text-gray-500">{{ description }}</p>
    <Button
      v-if="action"
      :label="action.label"
      theme="blue"
      class="mt-4"
      @click="action.onClick"
    />
  </div>
</template>

<script setup>
import { FeatherIcon, Button } from 'frappe-ui'

defineProps({
  icon: { type: String, default: 'inbox' },
  title: { type: String, required: true },
  description: String,
  action: Object
})
</script>
```

## Conclusion

This complete example demonstrates:

- Project setup with Vue 3 + frappe-ui
- Authentication flow with session management
- Vue Router with navigation guards
- CRUD operations with list and document resources
- Reusable composables for shared state
- Component-based architecture
- Form handling in dialogs
- Filter and search functionality
- Responsive UI with Tailwind CSS

Use this as a reference template for building your own Frappe frontend applications!
