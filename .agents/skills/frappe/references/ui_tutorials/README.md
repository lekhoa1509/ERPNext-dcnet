# Frappe UI Tutorials

Welcome to the frappe-ui tutorials! These tutorials provide comprehensive, step-by-step guidance for building modern Vue 3 frontends for Frappe applications.

## Tutorial Index

### Getting Started

| # | Tutorial | Description |
|---|----------|-------------|
| 01 | [Getting Started](./01-getting-started.md) | Project setup, installation, and configuration |
| 02 | [Basic Components](./02-basic-components.md) | Button, Badge, Avatar, Alert, Tooltip |
| 03 | [Input Components](./03-input-components.md) | TextInput, Select, Autocomplete, Checkbox, FormControl |
| 04 | [Dialogs and Modals](./04-dialogs-modals.md) | Dialog component, confirmation dialogs, form dialogs |

### Data Management

| # | Tutorial | Description |
|---|----------|-------------|
| 05 | [Data Fetching with Resources](./05-data-fetching-resources.md) | createResource, caching, transforms, error handling |
| 06 | [Document Resource](./06-document-resource.md) | createDocumentResource, CRUD, whitelisted methods |
| 07 | [Toast Notifications](./07-toast-notifications.md) | User feedback, toast types, actions |

### Forms and Lists

| # | Tutorial | Description |
|---|----------|-------------|
| 08 | [Form Handling](./08-form-handling.md) | Forms, validation, document creation/editing |
| 09 | [List Views](./09-list-views.md) | ListView component, custom cells, selection, grouping |
| 10 | [List Resource & Pagination](./10-list-resource-pagination.md) | createListResource, filtering, CRUD operations |

### File and Routing

| # | Tutorial | Description |
|---|----------|-------------|
| 11 | [File Uploads](./11-file-uploads.md) | FileUploader, drag-and-drop, attachments |
| 12 | [Vue Router Integration](./12-routing.md) | Routing, navigation guards, authentication |

### Advanced Topics

| # | Tutorial | Description |
|---|----------|-------------|
| 13 | [State Management](./13-state-management.md) | Composables, shared state, session management |
| 14 | [Realtime Updates](./14-realtime-updates.md) | Socket.IO, live data, notifications, presence |
| 15 | [Complete SPA Example](./15-complete-spa-example.md) | Full task management app walkthrough |
| 16 | [Advanced Patterns](./16-advanced-patterns.md) | Custom composables, optimization, error boundaries |

## Quick Start

If you're new to frappe-ui, we recommend following the tutorials in order:

1. Start with [Getting Started](./01-getting-started.md) to set up your project
2. Learn the [Basic Components](./02-basic-components.md) and [Input Components](./03-input-components.md)
3. Understand [Data Fetching](./05-data-fetching-resources.md) patterns
4. Build your first [Form](./08-form-handling.md) and [List View](./09-list-views.md)
5. Add [Routing](./12-routing.md) for navigation
6. Study the [Complete SPA Example](./15-complete-spa-example.md) for a real-world reference

## Prerequisites

- Basic knowledge of Vue 3 and Composition API
- Understanding of JavaScript ES6+ features
- Familiarity with Frappe Framework concepts (DocTypes, API)
- Node.js 16+ installed

## Tutorial Format

Each tutorial includes:

- **Overview** - What you'll learn
- **Step-by-step instructions** - Code examples with explanations
- **Practical examples** - Real-world use cases
- **Common pitfalls** - Mistakes to avoid
- **Next steps** - Links to related tutorials

## Code Examples

All code examples use Vue 3 Composition API with `<script setup>` syntax:

```vue
<template>
  <Button label="Click me" @click="handleClick" />
</template>

<script setup>
import { ref } from 'vue'
import { Button, toast } from 'frappe-ui'

const count = ref(0)

const handleClick = () => {
  count.value++
  toast({ type: 'success', message: `Clicked ${count.value} times` })
}
</script>
```

## Additional Resources

- [Official frappe-ui Documentation](https://frappeui.com)
- [frappe-ui GitHub Repository](https://github.com/frappe/frappe-ui)
- [Vue 3 Documentation](https://vuejs.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

## Feedback

Found an issue or have a suggestion? These tutorials are part of the frappe-ui skill and can be improved based on your feedback.

---

Happy coding with frappe-ui!
