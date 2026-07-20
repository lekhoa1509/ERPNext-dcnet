# Realtime Updates Tutorial

## Overview

frappe-ui supports realtime updates via Socket.IO integration with Frappe backend. This enables live data synchronization, instant notifications, and collaborative features in your SPA.

## Socket.IO Setup

### Initialize Socket Connection

```javascript
// src/main.js
import { createApp } from 'vue'
import { FrappeUI, setConfig, frappeRequest, initSocket } from 'frappe-ui'
import App from './App.vue'

const app = createApp(App)
app.use(FrappeUI)

setConfig('resourceFetcher', frappeRequest)

// Initialize Socket.IO connection
const socket = initSocket()

// Make socket available globally
app.provide('$socket', socket)

app.mount('#app')
```

### Socket Configuration

```javascript
import { initSocket } from 'frappe-ui'

const socket = initSocket({
  // Socket.IO server URL (defaults to current host)
  url: 'http://localhost:8000',

  // Socket.IO path
  path: '/socket.io',

  // Reconnection settings
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: 10
})
```

## Subscribing to Document Updates

### Basic Document Subscription

```vue
<template>
  <div v-if="todo.doc" class="p-4">
    <h2 class="text-xl font-bold">{{ todo.doc.description }}</h2>
    <Badge :theme="getStatusTheme(todo.doc.status)">
      {{ todo.doc.status }}
    </Badge>
    <p class="text-sm text-gray-500 mt-2">
      Last updated: {{ formatDate(todo.doc.modified) }}
    </p>
  </div>
</template>

<script setup>
import { inject, onMounted, onUnmounted } from 'vue'
import { createDocumentResource, Badge } from 'frappe-ui'

const props = defineProps({
  todoName: String
})

const socket = inject('$socket')

const todo = createDocumentResource({
  doctype: 'ToDo',
  name: props.todoName
})

// Subscribe to document updates
onMounted(() => {
  socket.emit('doc_subscribe', 'ToDo', props.todoName)

  socket.on('doc_update', (data) => {
    if (data.doctype === 'ToDo' && data.name === props.todoName) {
      // Reload document when it's updated
      todo.reload()
    }
  })
})

onUnmounted(() => {
  socket.emit('doc_unsubscribe', 'ToDo', props.todoName)
  socket.off('doc_update')
})

const getStatusTheme = (status) => status === 'Closed' ? 'green' : 'blue'
const formatDate = (date) => new Date(date).toLocaleString()
</script>
```

### Using Realtime Composable

```javascript
// composables/useRealtime.js
import { inject, onMounted, onUnmounted, ref } from 'vue'

export function useDocUpdate(doctype, name, callback) {
  const socket = inject('$socket')
  const isSubscribed = ref(false)

  const handleUpdate = (data) => {
    if (data.doctype === doctype && data.name === name) {
      callback(data)
    }
  }

  onMounted(() => {
    if (socket) {
      socket.emit('doc_subscribe', doctype, name)
      socket.on('doc_update', handleUpdate)
      isSubscribed.value = true
    }
  })

  onUnmounted(() => {
    if (socket) {
      socket.emit('doc_unsubscribe', doctype, name)
      socket.off('doc_update', handleUpdate)
      isSubscribed.value = false
    }
  })

  return { isSubscribed }
}

export function useDocTypeUpdate(doctype, callback) {
  const socket = inject('$socket')

  const handleUpdate = (data) => {
    if (data.doctype === doctype) {
      callback(data)
    }
  }

  onMounted(() => {
    if (socket) {
      socket.emit('doctype_subscribe', doctype)
      socket.on('list_update', handleUpdate)
    }
  })

  onUnmounted(() => {
    if (socket) {
      socket.emit('doctype_unsubscribe', doctype)
      socket.off('list_update', handleUpdate)
    }
  })
}
```

### Using the Composable

```vue
<script setup>
import { createDocumentResource } from 'frappe-ui'
import { useDocUpdate } from '@/composables/useRealtime'

const props = defineProps({ name: String })

const customer = createDocumentResource({
  doctype: 'Customer',
  name: props.name
})

// Auto-reload when document is updated elsewhere
useDocUpdate('Customer', props.name, () => {
  customer.reload()
})
</script>
```

## Live List Updates

### Realtime List Refresh

```vue
<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-xl font-bold">Tasks</h1>
      <div v-if="isLive" class="flex items-center gap-2 text-green-600">
        <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
        <span class="text-sm">Live</span>
      </div>
    </div>

    <ListView
      :columns="columns"
      :rows="tasks.data || []"
      :loading="tasks.loading"
      row-key="name"
    />
  </div>
</template>

<script setup>
import { inject, onMounted, onUnmounted, ref } from 'vue'
import { createListResource, ListView, toast } from 'frappe-ui'

const socket = inject('$socket')
const isLive = ref(false)

const columns = [
  { label: 'Subject', key: 'subject' },
  { label: 'Status', key: 'status', width: '120px' },
  { label: 'Priority', key: 'priority', width: '100px' }
]

const tasks = createListResource({
  doctype: 'Task',
  fields: ['name', 'subject', 'status', 'priority'],
  orderBy: 'modified desc',
  pageLength: 20,
  auto: true
})

onMounted(() => {
  if (socket) {
    socket.emit('doctype_subscribe', 'Task')
    socket.on('list_update', handleListUpdate)
    isLive.value = true
  }
})

onUnmounted(() => {
  if (socket) {
    socket.emit('doctype_unsubscribe', 'Task')
    socket.off('list_update', handleListUpdate)
    isLive.value = false
  }
})

const handleListUpdate = (data) => {
  if (data.doctype === 'Task') {
    // Refresh the list
    tasks.reload()

    // Show notification
    toast({
      type: 'info',
      message: `Task list updated`,
      duration: 2000
    })
  }
}
</script>
```

## Notifications

### Realtime Notifications

```javascript
// composables/useNotifications.js
import { inject, ref, onMounted, onUnmounted } from 'vue'
import { toast } from 'frappe-ui'

const notifications = ref([])
const unreadCount = ref(0)

export function useNotifications() {
  const socket = inject('$socket')

  const handleNotification = (data) => {
    notifications.value.unshift({
      id: Date.now(),
      ...data,
      read: false,
      timestamp: new Date()
    })
    unreadCount.value++

    // Show toast
    toast({
      type: data.type || 'info',
      title: data.title,
      message: data.message,
      duration: 5000
    })
  }

  const markAsRead = (id) => {
    const notification = notifications.value.find(n => n.id === id)
    if (notification && !notification.read) {
      notification.read = true
      unreadCount.value--
    }
  }

  const markAllAsRead = () => {
    notifications.value.forEach(n => n.read = true)
    unreadCount.value = 0
  }

  const clearAll = () => {
    notifications.value = []
    unreadCount.value = 0
  }

  onMounted(() => {
    if (socket) {
      socket.on('notification', handleNotification)
    }
  })

  onUnmounted(() => {
    if (socket) {
      socket.off('notification', handleNotification)
    }
  })

  return {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
    clearAll
  }
}
```

### Notification Bell Component

```vue
<template>
  <Popover>
    <template #target="{ togglePopover }">
      <Button
        icon="bell"
        variant="ghost"
        @click="togglePopover"
      >
        <Badge
          v-if="unreadCount > 0"
          :label="unreadCount.toString()"
          theme="red"
          class="absolute -top-1 -right-1"
        />
      </Button>
    </template>

    <template #body>
      <div class="w-80 max-h-96 overflow-y-auto">
        <div class="flex justify-between items-center p-3 border-b">
          <h3 class="font-medium">Notifications</h3>
          <Button
            v-if="notifications.length"
            label="Clear all"
            size="sm"
            variant="ghost"
            @click="clearAll"
          />
        </div>

        <div v-if="notifications.length === 0" class="p-4 text-center text-gray-500">
          No notifications
        </div>

        <div v-else>
          <div
            v-for="notification in notifications"
            :key="notification.id"
            class="p-3 border-b hover:bg-gray-50 cursor-pointer"
            :class="{ 'bg-blue-50': !notification.read }"
            @click="markAsRead(notification.id)"
          >
            <p class="font-medium text-sm">{{ notification.title }}</p>
            <p class="text-sm text-gray-600">{{ notification.message }}</p>
            <p class="text-xs text-gray-400 mt-1">
              {{ formatTime(notification.timestamp) }}
            </p>
          </div>
        </div>
      </div>
    </template>
  </Popover>
</template>

<script setup>
import { useNotifications } from '@/composables/useNotifications'
import { Popover, Button, Badge } from 'frappe-ui'

const { notifications, unreadCount, markAsRead, clearAll } = useNotifications()

const formatTime = (date) => {
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)

  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`

  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`

  return date.toLocaleDateString()
}
</script>
```

## Presence / Online Status

### User Presence

```javascript
// composables/usePresence.js
import { inject, ref, onMounted, onUnmounted } from 'vue'

const onlineUsers = ref(new Set())

export function usePresence() {
  const socket = inject('$socket')

  const handleUserJoin = (user) => {
    onlineUsers.value.add(user)
  }

  const handleUserLeave = (user) => {
    onlineUsers.value.delete(user)
  }

  const isOnline = (user) => {
    return onlineUsers.value.has(user)
  }

  onMounted(() => {
    if (socket) {
      socket.on('user:online', handleUserJoin)
      socket.on('user:offline', handleUserLeave)

      // Request current online users
      socket.emit('get_online_users')
      socket.on('online_users', (users) => {
        onlineUsers.value = new Set(users)
      })
    }
  })

  onUnmounted(() => {
    if (socket) {
      socket.off('user:online', handleUserJoin)
      socket.off('user:offline', handleUserLeave)
      socket.off('online_users')
    }
  })

  return {
    onlineUsers,
    isOnline
  }
}
```

### Online Indicator

```vue
<template>
  <div class="flex items-center gap-2">
    <Avatar :label="user.name" :image="user.avatar" />
    <div>
      <p class="font-medium">{{ user.name }}</p>
      <div class="flex items-center gap-1">
        <span
          class="w-2 h-2 rounded-full"
          :class="isOnline(user.email) ? 'bg-green-500' : 'bg-gray-300'"
        />
        <span class="text-xs text-gray-500">
          {{ isOnline(user.email) ? 'Online' : 'Offline' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { usePresence } from '@/composables/usePresence'
import { Avatar } from 'frappe-ui'

const props = defineProps({
  user: Object
})

const { isOnline } = usePresence()
</script>
```

## Collaborative Editing

### Simple Collaborative Indicator

```vue
<template>
  <div class="p-4">
    <div class="flex items-center gap-2 mb-4">
      <h2 class="text-xl font-bold">{{ document.doc?.name }}</h2>
      <div v-if="activeEditors.length > 0" class="flex -space-x-2">
        <Avatar
          v-for="editor in activeEditors"
          :key="editor.user"
          :label="editor.user"
          size="sm"
          class="ring-2 ring-white"
          :title="`${editor.user} is viewing`"
        />
      </div>
    </div>

    <form @submit.prevent="save">
      <FormControl
        v-model="form.title"
        label="Title"
        @focus="startEditing('title')"
        @blur="stopEditing('title')"
      />

      <FormControl
        v-model="form.content"
        type="textarea"
        label="Content"
        @focus="startEditing('content')"
        @blur="stopEditing('content')"
      />

      <Button
        type="submit"
        label="Save"
        theme="blue"
        variant="solid"
        :loading="saving"
      />
    </form>
  </div>
</template>

<script setup>
import { inject, ref, reactive, onMounted, onUnmounted } from 'vue'
import {
  createDocumentResource,
  FormControl,
  Button,
  Avatar,
  toast
} from 'frappe-ui'
import { useSession } from '@/composables/useSession'

const props = defineProps({
  doctype: String,
  name: String
})

const socket = inject('$socket')
const { user } = useSession()

const activeEditors = ref([])
const form = reactive({ title: '', content: '' })
const saving = ref(false)

const document = createDocumentResource({
  doctype: props.doctype,
  name: props.name,
  onSuccess(doc) {
    form.title = doc.title
    form.content = doc.content
  }
})

// Room for this document
const room = `${props.doctype}:${props.name}`

onMounted(() => {
  if (socket) {
    // Join document room
    socket.emit('join_room', room)

    // Announce presence
    socket.emit('editing:join', { room, user: user.value })

    // Listen for other editors
    socket.on('editing:users', (users) => {
      activeEditors.value = users.filter(u => u.user !== user.value)
    })

    // Listen for changes
    socket.on('editing:change', (data) => {
      if (data.user !== user.value) {
        form[data.field] = data.value
        toast({
          type: 'info',
          message: `${data.user} updated ${data.field}`,
          duration: 2000
        })
      }
    })
  }
})

onUnmounted(() => {
  if (socket) {
    socket.emit('editing:leave', { room, user: user.value })
    socket.emit('leave_room', room)
    socket.off('editing:users')
    socket.off('editing:change')
  }
})

const startEditing = (field) => {
  socket?.emit('editing:focus', { room, user: user.value, field })
}

const stopEditing = (field) => {
  socket?.emit('editing:blur', { room, user: user.value, field })

  // Broadcast change
  socket?.emit('editing:change', {
    room,
    user: user.value,
    field,
    value: form[field]
  })
}

const save = async () => {
  saving.value = true
  await document.setValue.submit(form)
  saving.value = false
}
</script>
```

## Connection Status

### Connection Status Component

```vue
<template>
  <div
    v-if="!isConnected"
    class="fixed bottom-4 right-4 bg-red-100 text-red-700 px-4 py-2 rounded-lg shadow-lg flex items-center gap-2"
  >
    <FeatherIcon name="wifi-off" class="w-4 h-4" />
    <span>Connection lost. Reconnecting...</span>
  </div>
</template>

<script setup>
import { inject, ref, onMounted, onUnmounted } from 'vue'
import { FeatherIcon, toast } from 'frappe-ui'

const socket = inject('$socket')
const isConnected = ref(true)

onMounted(() => {
  if (socket) {
    socket.on('connect', () => {
      isConnected.value = true
      toast({
        type: 'success',
        message: 'Connected',
        duration: 2000
      })
    })

    socket.on('disconnect', () => {
      isConnected.value = false
    })

    socket.on('reconnect', () => {
      isConnected.value = true
      toast({
        type: 'success',
        message: 'Reconnected',
        duration: 2000
      })
    })
  }
})

onUnmounted(() => {
  if (socket) {
    socket.off('connect')
    socket.off('disconnect')
    socket.off('reconnect')
  }
})
</script>
```

## Common Pitfalls

### 1. Socket Not Initialized

**Problem:** Socket methods fail because socket is null.

**Solution:** Check if socket exists before using:
```javascript
if (socket) {
  socket.emit('event', data)
}
```

### 2. Memory Leaks

**Problem:** Event listeners accumulate over time.

**Solution:** Always unsubscribe in `onUnmounted`:
```javascript
onMounted(() => {
  socket.on('event', handler)
})

onUnmounted(() => {
  socket.off('event', handler)
})
```

### 3. Missing Server-Side Implementation

**Problem:** Socket events don't work.

**Solution:** Ensure your Frappe app has corresponding server-side Socket.IO handlers. Frappe provides built-in handlers for `doc_subscribe`, `doc_update`, etc.

## Next Steps

- Build [Complete SPA Example](./15-complete-spa-example.md)
- Explore [Advanced Patterns](./16-advanced-patterns.md)
- Learn [Testing](./17-testing.md)
