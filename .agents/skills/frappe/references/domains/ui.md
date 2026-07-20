<!-- Source: frappe-ui skill -->

# Frappe UI - Vue 3 Component Library for Frappe Framework

## Description

Frappe UI is a comprehensive Vue 3 component library designed for building modern single-page application (SPA) frontends for Frappe Framework apps. It provides a rich set of UI components, data fetching utilities, and seamless integration with Frappe backend APIs.

**Source Knowledge:** Codebase analysis from `/Users/vovanduc/Code/dcnet/frappe-ui`
**Files Analyzed:** 91 files
**Languages:** TypeScript (64.8%), JavaScript (35.2%)
**License:** MIT License (Frappe Technologies Pvt. Ltd.)

### Tech Stack

- **Vue 3** - Reactive frontend framework with Composition API
- **TailwindCSS** - Utility-first CSS framework for design systems
- **Headless UI** - Unstyled, accessible UI components
- **TipTap** - ProseMirror-based rich-text editor
- **dayjs** - Minimal date manipulation library

---

## When to Use This Skill

Use this skill when you need to:

### UI Component Development
- Building standalone Frappe apps (like CRM, Helpdesk, Gameplan)
- Creating Vue 3 dialogs, modals, and popups
- Implementing forms with `FormControl`, `TextInput`, `Select`, `Autocomplete`
- Building data tables with `ListView` component
- Adding notifications with `Toast` component

### Data Fetching & Resources
- Fetching data from Frappe backend using `createResource`
- Working with document CRUD operations using `createDocumentResource`
- Managing lists with pagination using `createListResource`
- Implementing caching strategies for API responses

### Specific Triggers
- User asks about `frappe-ui`, `vue frappe`, `createListResource`
- User wants Vue 3 dialogs or forms for Frappe apps
- User mentions `createDocumentResource`, `vue dialog`, `vue form`
- Building frontends separate from Frappe Desk (portal/SPA apps)

### When NOT to Use
- For Frappe Desk customization (use `frappe-desk` skill instead)
- For server-side Python code (use `frappe` skill)
- For ERPNext module questions (use `erpnext-*` skills)

---

## Quick Reference

### Installation & Setup

```bash
# Install in your Frappe app's frontend directory
npm install frappe-ui
# or
yarn add frappe-ui
```

**main.js** - Initialize the plugin:

```javascript
import { createApp } from 'vue'
import { FrappeUI, setConfig, frappeRequest } from 'frappe-ui'
import App from './App.vue'
import './index.css'

let app = createApp(App)
app.use(FrappeUI)

// Configure for Frappe backend
setConfig('resourceFetcher', frappeRequest)

app.mount('#app')
```

**tailwind.config.js** - Include the preset:

```javascript
module.exports = {
  presets: [
    require('frappe-ui/src/utils/tailwind.config')
  ],
  // ... your config
}
```

---

### Component Examples

#### Button Component

```vue
<template>
  <Button
    label="Save"
    theme="blue"
    variant="solid"
    :loading="saving"
    @click="handleSave"
  />

  <Button icon="plus" tooltip="Add new item" />

  <Button
    label="Delete"
    theme="red"
    icon-left="trash"
  />
</template>

<script setup>
import { Button } from 'frappe-ui'
</script>
```

**Button Props:**
- `theme`: "gray" | "blue" | "red" | "green" (default: "gray")
- `variant`: "subtle" | "solid" | "outline" | "ghost" (default: "subtle")
- `size`: "sm" | "md" | "lg" | "xl" (default: "sm")
- `loading`: boolean - Shows loading spinner
- `disabled`: boolean
- `icon`, `iconLeft`, `iconRight`: string | Component

---

#### TextInput Component

```vue
<template>
  <TextInput
    v-model="email"
    type="email"
    placeholder="Enter email"
    :debounce="300"
  >
    <template #prefix>
      <FeatherIcon name="mail" class="w-4 h-4" />
    </template>
  </TextInput>
</template>

<script setup>
import { ref } from 'vue'
import { TextInput } from 'frappe-ui'

const email = ref('')
</script>
```

**TextInput Props:**
- `type`: "text" | "email" | "number" | "password" | etc.
- `size`: "sm" | "md" | "lg" | "xl"
- `variant`: "subtle" | "outline" | "ghost"
- `debounce`: number (ms delay before emitting value)
- `disabled`, `required`: boolean

---

#### FormControl Component

```vue
<template>
  <FormControl
    v-model="status"
    type="select"
    label="Status"
    :options="statusOptions"
    description="Select current status"
    required
  />

  <FormControl
    v-model="description"
    type="textarea"
    label="Description"
  />

  <FormControl
    v-model="customer"
    type="autocomplete"
    label="Customer"
    :options="customers"
  />
</template>

<script setup>
import { ref } from 'vue'
import { FormControl } from 'frappe-ui'

const status = ref('Open')
const statusOptions = [
  { label: 'Open', value: 'Open' },
  { label: 'Closed', value: 'Closed' },
]
</script>
```

**FormControl Types:**
- `text`, `email`, `number`, `password` - TextInput variants
- `select` - Dropdown selection
- `autocomplete` - Searchable dropdown with filtering
- `textarea` - Multi-line text
- `checkbox` - Boolean toggle
- `combobox` - Editable select

---

#### Dialog Component

```vue
<template>
  <Dialog
    v-model="showDialog"
    :options="{
      title: 'Confirm Action',
      message: 'Are you sure you want to proceed?',
      size: 'lg',
      actions: [
        { label: 'Cancel', variant: 'subtle', onClick: close },
        { label: 'Confirm', theme: 'blue', variant: 'solid', onClick: confirm }
      ]
    }"
  >
    <template #body-content>
      <FormControl v-model="reason" type="textarea" label="Reason" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, FormControl } from 'frappe-ui'

const showDialog = ref(false)
const reason = ref('')

const confirm = (close) => {
  // Handle confirmation
  close()
}
</script>
```

**Dialog Slots:**
- `body` - Main body content (overrides header + content)
- `body-header` - Header inside dialog body
- `body-title` - Title section
- `body-content` - Main content area
- `actions` - Footer actions (exposes `{ close }`)

---

#### Select Component

```vue
<template>
  <Select
    v-model="selectedItem"
    :options="items"
    placeholder="Choose an item"
    size="md"
    variant="outline"
  >
    <template #prefix>
      <FeatherIcon name="filter" class="w-4 h-4" />
    </template>
    <template #option="{ option }">
      <div class="flex items-center gap-2">
        <Badge :theme="option.color">{{ option.label }}</Badge>
      </div>
    </template>
  </Select>
</template>

<script setup>
import { ref } from 'vue'
import { Select, Badge } from 'frappe-ui'

const selectedItem = ref(null)
const items = [
  { label: 'Option 1', value: '1', color: 'blue' },
  { label: 'Option 2', value: '2', color: 'green' },
]
</script>
```

---

#### Toast Notifications

```vue
<script setup>
import { toast } from 'frappe-ui'

// Success notification
toast({
  type: 'success',
  message: 'Document saved successfully',
  duration: 3000
})

// Error notification
toast({
  type: 'error',
  message: 'Failed to save document',
  closable: true
})

// With action
toast({
  type: 'info',
  message: 'Document deleted',
  action: {
    label: 'Undo',
    onClick: () => restoreDocument()
  }
})
</script>
```

**Toast Types:** `info` | `success` | `warning` | `error`

---

### Data Fetching (Resources)

#### createResource - Generic API Calls

```vue
<template>
  <Button @click="data.reload()" :loading="data.loading">
    Reload
  </Button>
  <div v-if="data.data">
    {{ data.data }}
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui'

// Basic resource
const data = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'ToDo',
    filters: { status: 'Open' }
  },
  cache: 'open-todos',  // Cache key for persistence
  auto: true,           // Fetch automatically on mount
  transform(data) {
    // Transform response before storing
    return data.map(d => ({ ...d, isOpen: d.status === 'Open' }))
  },
  onSuccess(data) {
    console.log('Fetched:', data)
  },
  onError(error) {
    console.error('Error:', error)
  }
})

// Manual fetch
data.fetch()

// With parameters
data.submit({ status: 'Closed' })
</script>
```

**Resource API:**
- `data.data` - Response data
- `data.loading` - Loading state
- `data.error` - Error object
- `data.fetched` - True after first successful fetch
- `data.fetch()` / `data.reload()` / `data.submit()` - Trigger request
- `data.reset()` - Reset to initial state
- `data.setData(newData)` - Manually set data

---

#### createDocumentResource - Single Document CRUD

```vue
<template>
  <div v-if="todo.doc">
    <h2>{{ todo.doc.description }}</h2>
    <Badge>{{ todo.doc.status }}</Badge>

    <Button @click="markClosed" :loading="todo.setValue.loading">
      Mark Closed
    </Button>

    <Button @click="todo.delete.submit()" theme="red">
      Delete
    </Button>
  </div>
</template>

<script setup>
import { createDocumentResource, Button, Badge } from 'frappe-ui'

const todo = createDocumentResource({
  doctype: 'ToDo',
  name: 'TODO-0001',

  // Expose whitelisted methods as resources
  whitelistedMethods: {
    sendEmail: 'send_email',
    markComplete: 'mark_complete'
  },

  onSuccess(doc) {
    console.log('Document loaded:', doc)
  },

  setValue: {
    onSuccess() {
      toast({ type: 'success', message: 'Updated!' })
    }
  },

  delete: {
    onSuccess() {
      router.push('/todos')
    }
  }
})

const markClosed = () => {
  todo.setValue.submit({ status: 'Closed' })
}

// Call whitelisted method
todo.sendEmail.submit({ email: 'user@example.com' })
</script>
```

**Document Resource API:**
- `todo.doc` - Document data
- `todo.reload()` - Refresh document
- `todo.setValue.submit({ field: value })` - Update fields
- `todo.setValueDebounced.submit({})` - Debounced update
- `todo.delete.submit()` - Delete document
- `todo.[methodName].submit()` - Call whitelisted methods

---

#### createListResource - Paginated Lists

```vue
<template>
  <ListView :columns="columns" :rows="todos.data" />

  <div class="flex gap-2">
    <Button @click="todos.previous()" :disabled="todos.start === 0">
      Previous
    </Button>
    <Button @click="todos.next()" :disabled="!todos.hasNextPage">
      Next
    </Button>
  </div>
</template>

<script setup>
import { createListResource, ListView, Button } from 'frappe-ui'

const todos = createListResource({
  doctype: 'ToDo',
  fields: ['name', 'description', 'status', 'owner'],
  filters: {
    status: 'Open'
  },
  orderBy: 'creation desc',
  pageLength: 20,
  auto: true,

  // Cache for instant reload
  cache: ['todos', 'open'],

  // Transform each row
  transform(data) {
    return data.map(d => ({
      ...d,
      ownerName: d.owner.split('@')[0]
    }))
  },

  // Event handlers for sub-resources
  insert: {
    onSuccess(doc) {
      toast({ type: 'success', message: 'Created!' })
    }
  }
})

// Update filters and reload
todos.update({
  filters: { status: 'Closed' }
})

// Insert new record
todos.insert.submit({
  description: 'New todo item',
  status: 'Open'
})

// Update a row
todos.setValue.submit({
  name: 'TODO-0001',
  status: 'Closed'
})

// Delete a row
todos.delete.submit('TODO-0001')

// Run doc method
todos.runDocMethod.submit({
  method: 'send_reminder',
  name: 'TODO-0001',
  email: 'user@example.com'
})
</script>
```

**List Resource API:**
- `todos.data` - Array of records
- `todos.originalData` - Untransformed data
- `todos.next()` / `todos.previous()` - Pagination
- `todos.hasNextPage` - More pages available
- `todos.reload()` - Refresh current page
- `todos.insert.submit({})` - Create new record
- `todos.setValue.submit({ name, ...fields })` - Update record
- `todos.delete.submit(name)` - Delete record
- `todos.fetchOne.submit(name)` - Refresh single record

---

### Options API Support

For Vue Options API users, register the plugin and use `resources` option:

```javascript
// main.js
import { resourcesPlugin } from 'frappe-ui'
app.use(resourcesPlugin)
```

```vue
<template>
  <div v-for="todo in $resources.todos.data">
    {{ todo.description }}
  </div>
</template>

<script>
export default {
  resources: {
    todos() {
      return {
        type: 'list',
        doctype: 'ToDo',
        fields: ['name', 'description'],
        auto: true
      }
    },
    currentTodo() {
      return {
        type: 'document',
        doctype: 'ToDo',
        name: this.todoId
      }
    }
  }
}
</script>
```

---

## Key Concepts

### Resource System

The resource system is the core of frappe-ui's data management:

1. **Reactive State** - All resource properties (`data`, `loading`, `error`) are reactive
2. **Caching** - Built-in memory + IndexedDB caching with cache keys
3. **Transform** - Transform data before storing with `transform()` callback
4. **Events** - Lifecycle hooks: `onSuccess`, `onError`, `beforeSubmit`, `validate`
5. **Debouncing** - Built-in debounce support for frequent updates

### Component Design

- All components support `size` variants: "sm", "md", "lg", "xl"
- Style variants: "subtle", "outline", "solid", "ghost"
- Consistent slot patterns: `prefix`, `suffix`, `default`
- Built on Headless UI for accessibility

### Frappe Integration

```javascript
// Configure for Frappe backend
import { setConfig, frappeRequest } from 'frappe-ui'
setConfig('resourceFetcher', frappeRequest)
```

This enables:
- Automatic `/api/method/` prefix for URLs
- Response parsing (extracts `message` key)
- Error handling (extracts `exc` from response)
- CSRF token handling

---

## Reference Documentation

### API Reference (`references/api_reference/`)

| File | Description | Key Functions |
|------|-------------|---------------|
| `resources.md` | Core resource system | `createResource()`, `getCachedResource()` |
| `documentResource.md` | Document resource | `createDocumentResource()`, `setValue()` |
| `listResource.md` | List resource | `createListResource()`, `next()`, `previous()` |
| `call.md` | Direct API calls | `call()`, `createCall()` |
| `useCall.md` | Composable for API calls | `useCall()` |
| `useList.md` | Composable for lists | `useList()` |
| `useDoc.md` | Composable for documents | `useDoc()` |
| `socketio.md` | Socket.IO integration | `initSocket()` |
| `realtime.md` | Realtime updates | `onDocUpdate()`, `subscribe()` |

### Component Documentation (`references/documentation/other/`)

| Component | Props | Description |
|-----------|-------|-------------|
| `button.md` | theme, variant, size, icon, loading | Action buttons |
| `textinput.md` | type, size, variant, debounce | Text input fields |
| `formcontrol.md` | type, label, description, options | Form wrapper |
| `select.md` | options, placeholder, size | Dropdown select |
| `dialog.md` | modelValue, options, slots | Modal dialogs |
| `Toast.md` | type, message, duration, action | Notifications |
| `datepicker.md` | - | Date selection |
| `autocomplete.md` | - | Searchable select |
| `listview.md` | columns, rows, groups | Data tables |
| `texteditor.md` | - | Rich text editor (TipTap) |
| `calendar.md` | - | Calendar view |
| `charts.md` | - | Chart components |

### TextEditor Extensions (`references/api_reference/`)

| Extension | Purpose |
|-----------|---------|
| `image-extension.md` | Image upload/display |
| `link-extension.md` | Hyperlink editing |
| `mention-extension.md` | @mentions |
| `iframe-extension.md` | Embed iframes |
| `code-block.md` | Code syntax highlighting |
| `video-extension.md` | Video embedding |

### Utilities (`references/api_reference/`)

| Utility | Purpose |
|---------|---------|
| `dayjs.md` | Date manipulation helpers |
| `debounce.md` | Debounce function |
| `markdown.md` | Markdown to HTML conversion |
| `pageMeta.md` | Page title/favicon management |
| `theme.md` | Theme switching |
| `focus.md` | Focus management |

---

## Working with This Skill

### For Beginners

1. Start with the **Quick Reference** section above for installation
2. Use `FormControl` for forms - it handles all input types
3. Use `createResource` for simple API calls
4. Use `createListResource` for lists with pagination

### For Intermediate Users

1. Explore **createDocumentResource** for full CRUD operations
2. Implement caching with cache keys for better UX
3. Use transform functions to shape API responses
4. Leverage slot patterns for component customization

### For Advanced Users

1. Dive into the API reference for composables (`useList`, `useDoc`, `useCall`)
2. Implement realtime updates with Socket.IO integration
3. Extend TextEditor with custom TipTap extensions
4. Build custom components using Headless UI patterns

---

## Used By (Production Apps)

- [Frappe Cloud](https://frappecloud.com) - Cloud hosting platform
- [Gameplan](https://github.com/frappe/gameplan) - Team collaboration
- [Helpdesk](https://github.com/frappe/helpdesk) - Customer support
- [Frappe Insights](https://github.com/frappe/insights) - Business intelligence
- [Frappe Drive](https://github.com/frappe/drive) - File management
- [Frappe Builder](https://github.com/frappe/builder) - Website builder
- [Frappe CRM](https://github.com/frappe/crm) - Customer relationship management

---

## Quick Start Project

Use the starter template to bootstrap a new project:

```bash
# Create new Frappe app
bench new-app myapp

# Setup frontend with frappe-ui
cd apps/myapp
npx degit netchampfaris/frappe-ui-starter frontend

# Configure CSRF
bench --site mysite set-config ignore_csrf 1

# Start development
cd frontend
yarn && yarn dev
```

---

**Generated by Skill Seeker** | Comprehensive codebase analysis with API reference, documentation, and real-world patterns

**Official Documentation:** [frappeui.com](https://frappeui.com) | [GitHub](https://github.com/frappe/frappe-ui)
