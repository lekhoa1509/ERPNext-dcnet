# Toast Notifications Tutorial

## Overview

Toast notifications provide non-intrusive feedback to users about the results of their actions. frappe-ui provides a simple yet powerful toast system with multiple types, customizable durations, and action buttons.

## Basic Toast

### Simple Notifications

```vue
<script setup>
import { toast, Button } from 'frappe-ui'

const showSuccess = () => {
  toast({
    type: 'success',
    message: 'Operation completed successfully!'
  })
}

const showError = () => {
  toast({
    type: 'error',
    message: 'Something went wrong. Please try again.'
  })
}

const showWarning = () => {
  toast({
    type: 'warning',
    message: 'Please review your changes before saving.'
  })
}

const showInfo = () => {
  toast({
    type: 'info',
    message: 'Your session will expire in 5 minutes.'
  })
}
</script>

<template>
  <div class="space-x-2">
    <Button label="Success" theme="green" @click="showSuccess" />
    <Button label="Error" theme="red" @click="showError" />
    <Button label="Warning" theme="orange" @click="showWarning" />
    <Button label="Info" theme="blue" @click="showInfo" />
  </div>
</template>
```

## Toast Types

### Available Types

| Type | Use Case | Icon | Color |
|------|----------|------|-------|
| `success` | Action completed | Checkmark | Green |
| `error` | Action failed | X | Red |
| `warning` | Requires attention | Alert | Orange |
| `info` | General information | Info | Blue |

```javascript
// Success - for completed actions
toast({ type: 'success', message: 'Document saved!' })

// Error - for failures
toast({ type: 'error', message: 'Failed to save document' })

// Warning - for alerts
toast({ type: 'warning', message: 'Unsaved changes will be lost' })

// Info - for information
toast({ type: 'info', message: 'New update available' })
```

## Toast Options

### Complete Options

```javascript
toast({
  // Type of notification
  type: 'success',  // 'success' | 'error' | 'warning' | 'info'

  // Main message text
  message: 'Your changes have been saved.',

  // Title (optional, displayed above message)
  title: 'Success!',

  // Duration in milliseconds (default: 3000)
  duration: 5000,

  // Show close button (default: true)
  closable: true,

  // Action button
  action: {
    label: 'Undo',
    onClick: () => {
      // Handle action click
      console.log('Undo clicked')
    }
  }
})
```

### Duration

```javascript
// Quick notification (2 seconds)
toast({
  type: 'success',
  message: 'Copied!',
  duration: 2000
})

// Standard notification (default 3 seconds)
toast({
  type: 'info',
  message: 'Processing your request...'
})

// Long notification (5 seconds)
toast({
  type: 'warning',
  message: 'Please review all fields before submitting',
  duration: 5000
})

// Persistent notification (stays until closed)
toast({
  type: 'error',
  message: 'Critical error occurred',
  duration: 0,  // Won't auto-dismiss
  closable: true
})
```

## Toast with Actions

### Undo Action

```vue
<script setup>
import { ref } from 'vue'
import { toast, Button } from 'frappe-ui'

const items = ref([
  { id: 1, name: 'Item 1' },
  { id: 2, name: 'Item 2' },
  { id: 3, name: 'Item 3' }
])

const deleteItem = (item) => {
  // Remove item
  const index = items.value.findIndex(i => i.id === item.id)
  items.value.splice(index, 1)

  // Show toast with undo option
  toast({
    type: 'success',
    message: `Deleted "${item.name}"`,
    action: {
      label: 'Undo',
      onClick: () => {
        // Restore item
        items.value.splice(index, 0, item)
        toast({
          type: 'info',
          message: 'Item restored'
        })
      }
    }
  })
}
</script>
```

### View Action

```javascript
toast({
  type: 'success',
  message: 'Invoice created successfully',
  action: {
    label: 'View Invoice',
    onClick: () => {
      router.push('/invoices/INV-00001')
    }
  }
})
```

### Retry Action

```javascript
const submitForm = async () => {
  try {
    await api.submit(formData)
    toast({
      type: 'success',
      message: 'Form submitted successfully'
    })
  } catch (error) {
    toast({
      type: 'error',
      message: 'Failed to submit form',
      duration: 0,  // Stay until dismissed
      action: {
        label: 'Retry',
        onClick: submitForm
      }
    })
  }
}
```

## Practical Examples

### Form Submission Feedback

```vue
<script setup>
import { reactive, ref } from 'vue'
import { createResource, FormControl, Button, toast } from 'frappe-ui'

const form = reactive({
  name: '',
  email: ''
})

const createCustomer = createResource({
  url: 'frappe.client.insert',
  onSuccess(doc) {
    toast({
      type: 'success',
      title: 'Customer Created',
      message: `${doc.customer_name} has been added to your customers.`,
      action: {
        label: 'View',
        onClick: () => {
          router.push(`/customers/${doc.name}`)
        }
      }
    })
    // Reset form
    form.name = ''
    form.email = ''
  },
  onError(error) {
    toast({
      type: 'error',
      title: 'Creation Failed',
      message: error.messages?.[0] || 'Could not create customer',
      duration: 5000
    })
  }
})

const handleSubmit = () => {
  createCustomer.submit({
    doc: {
      doctype: 'Customer',
      customer_name: form.name,
      email_id: form.email
    }
  })
}
</script>
```

### Batch Operation Feedback

```vue
<script setup>
import { ref } from 'vue'
import { toast, Button } from 'frappe-ui'

const selectedItems = ref([])
const deleteInProgress = ref(false)

const deleteSelected = async () => {
  deleteInProgress.value = true
  const total = selectedItems.value.length
  let deleted = 0
  let failed = 0

  for (const item of selectedItems.value) {
    try {
      await api.delete(item.id)
      deleted++
    } catch (error) {
      failed++
    }
  }

  deleteInProgress.value = false

  if (failed === 0) {
    toast({
      type: 'success',
      message: `${deleted} items deleted successfully`
    })
  } else if (deleted === 0) {
    toast({
      type: 'error',
      message: `Failed to delete ${failed} items`,
      duration: 5000
    })
  } else {
    toast({
      type: 'warning',
      message: `${deleted} deleted, ${failed} failed`,
      duration: 5000
    })
  }

  selectedItems.value = []
}
</script>
```

### Copy to Clipboard

```vue
<script setup>
import { toast, Button } from 'frappe-ui'

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    toast({
      type: 'success',
      message: 'Copied to clipboard!',
      duration: 2000
    })
  } catch (error) {
    toast({
      type: 'error',
      message: 'Failed to copy'
    })
  }
}
</script>

<template>
  <Button
    icon="copy"
    tooltip="Copy ID"
    @click="copyToClipboard('CUST-00001')"
  />
</template>
```

### Network Status

```vue
<script setup>
import { onMounted, onUnmounted } from 'vue'
import { toast } from 'frappe-ui'

let offlineToast = null

const handleOnline = () => {
  toast({
    type: 'success',
    message: 'You are back online',
    duration: 3000
  })
}

const handleOffline = () => {
  toast({
    type: 'error',
    message: 'You are offline. Some features may not work.',
    duration: 0,  // Stay visible
    closable: true
  })
}

onMounted(() => {
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
})

onUnmounted(() => {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
})
</script>
```

### File Upload Progress

```vue
<script setup>
import { ref } from 'vue'
import { toast, Button, FileUploader } from 'frappe-ui'

const handleUpload = async (file) => {
  toast({
    type: 'info',
    message: `Uploading ${file.name}...`,
    duration: 0
  })

  try {
    const result = await uploadFile(file)
    toast({
      type: 'success',
      message: `${file.name} uploaded successfully`,
      action: {
        label: 'View',
        onClick: () => {
          window.open(result.url, '_blank')
        }
      }
    })
  } catch (error) {
    toast({
      type: 'error',
      message: `Failed to upload ${file.name}`,
      action: {
        label: 'Retry',
        onClick: () => handleUpload(file)
      }
    })
  }
}
</script>
```

## Toast Helper Functions

Create reusable toast utilities:

```javascript
// utils/notifications.js
import { toast } from 'frappe-ui'

export const notify = {
  success(message, options = {}) {
    toast({
      type: 'success',
      message,
      duration: 3000,
      ...options
    })
  },

  error(message, options = {}) {
    toast({
      type: 'error',
      message,
      duration: 5000,
      closable: true,
      ...options
    })
  },

  warning(message, options = {}) {
    toast({
      type: 'warning',
      message,
      duration: 4000,
      ...options
    })
  },

  info(message, options = {}) {
    toast({
      type: 'info',
      message,
      duration: 3000,
      ...options
    })
  },

  // Convenience methods
  saved() {
    this.success('Changes saved')
  },

  deleted(itemName) {
    this.success(`${itemName || 'Item'} deleted`)
  },

  copied() {
    this.success('Copied to clipboard', { duration: 2000 })
  },

  networkError() {
    this.error('Network error. Please check your connection and try again.')
  }
}
```

Usage:

```vue
<script setup>
import { notify } from '@/utils/notifications'

const saveDocument = async () => {
  try {
    await api.save()
    notify.saved()
  } catch (error) {
    notify.error(error.message)
  }
}
</script>
```

## Common Pitfalls

### 1. Toast Not Appearing

**Problem:** `toast()` function doesn't show anything.

**Solution:** Ensure you've properly imported and configured frappe-ui:
```javascript
// main.js
import { FrappeUI } from 'frappe-ui'
app.use(FrappeUI)
```

### 2. Multiple Toasts Stacking

**Problem:** Too many toasts appearing at once.

**Solution:** Use debouncing or check before showing:
```javascript
// Use debounce for rapid events
import { debounce } from 'frappe-ui'

const showSaveToast = debounce(() => {
  toast({ type: 'success', message: 'Saved' })
}, 300)
```

### 3. Toast Action Not Working

**Problem:** Action button click doesn't trigger handler.

**Solution:** Ensure the onClick handler is a function:
```javascript
// Correct
action: {
  label: 'Undo',
  onClick: () => handleUndo()
}

// Incorrect - calling the function immediately
action: {
  label: 'Undo',
  onClick: handleUndo()  // This runs immediately!
}
```

### 4. Long Messages Get Cut Off

**Problem:** Toast message text is truncated.

**Solution:** Keep messages concise or use title + message:
```javascript
// Better approach for longer content
toast({
  type: 'error',
  title: 'Validation Error',
  message: 'Please fill in all required fields before submitting.',
  duration: 5000
})
```

## Best Practices

1. **Keep messages concise** - Users should understand at a glance
2. **Use appropriate types** - Success for completion, error for failures
3. **Provide actions when useful** - Undo, View, Retry
4. **Set appropriate durations** - Quick actions = short, errors = longer
5. **Don't spam** - Debounce rapid events, avoid excessive notifications
6. **Be helpful with errors** - Include what went wrong and how to fix it

## Next Steps

- Learn about [Form Handling](./08-form-handling.md)
- Build [List Views](./09-list-views.md)
- Explore [File Uploads](./11-file-uploads.md)
