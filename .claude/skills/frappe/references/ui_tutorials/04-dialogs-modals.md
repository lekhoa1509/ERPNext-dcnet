# Dialogs and Modals Tutorial

## Overview

This tutorial covers how to create and manage dialogs (modals) in frappe-ui using the Dialog component, including confirmation dialogs, form dialogs, and programmatic dialogs.

## Basic Dialog

### Simple Dialog with v-model

```vue
<template>
  <div>
    <Button label="Open Dialog" @click="showDialog = true" />

    <Dialog v-model="showDialog">
      <template #body>
        <div class="p-4">
          <h2 class="text-lg font-semibold mb-2">Welcome!</h2>
          <p class="text-gray-600">This is a simple dialog.</p>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button } from 'frappe-ui'

const showDialog = ref(false)
</script>
```

### Dialog with Options

```vue
<template>
  <div>
    <Button label="Show Info" @click="showDialog = true" />

    <Dialog
      v-model="showDialog"
      :options="{
        title: 'Important Information',
        message: 'This action will update your settings.',
        icon: { name: 'info', variant: 'solid', theme: 'blue' },
        size: 'md',
        actions: [
          { label: 'Cancel', variant: 'subtle' },
          { label: 'OK', theme: 'blue', variant: 'solid' }
        ]
      }"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button } from 'frappe-ui'

const showDialog = ref(false)
</script>
```

## Dialog Sizes

```vue
<template>
  <div class="space-x-2">
    <Button label="Small" @click="openDialog('sm')" />
    <Button label="Medium" @click="openDialog('md')" />
    <Button label="Large" @click="openDialog('lg')" />
    <Button label="XL" @click="openDialog('xl')" />
    <Button label="2XL" @click="openDialog('2xl')" />
    <Button label="Full" @click="openDialog('full')" />

    <Dialog
      v-model="showDialog"
      :options="{
        title: `Dialog Size: ${dialogSize}`,
        size: dialogSize
      }"
    >
      <template #body-content>
        <p class="text-gray-600">
          This dialog is using the "{{ dialogSize }}" size option.
        </p>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button } from 'frappe-ui'

const showDialog = ref(false)
const dialogSize = ref('md')

const openDialog = (size) => {
  dialogSize.value = size
  showDialog.value = true
}
</script>
```

## Confirmation Dialog

### Standard Confirmation

```vue
<template>
  <div>
    <Button
      label="Delete Item"
      theme="red"
      variant="solid"
      @click="showConfirmDelete = true"
    />

    <Dialog
      v-model="showConfirmDelete"
      :options="{
        title: 'Confirm Delete',
        message: 'Are you sure you want to delete this item? This action cannot be undone.',
        icon: { name: 'alert-triangle', variant: 'solid', theme: 'red' },
        actions: [
          {
            label: 'Cancel',
            variant: 'subtle',
            onClick: ({ close }) => close()
          },
          {
            label: 'Delete',
            theme: 'red',
            variant: 'solid',
            onClick: ({ close }) => {
              deleteItem()
              close()
            }
          }
        ]
      }"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button, toast } from 'frappe-ui'

const showConfirmDelete = ref(false)

const deleteItem = () => {
  // Perform delete operation
  toast({
    type: 'success',
    message: 'Item deleted successfully'
  })
}
</script>
```

### Confirmation with Loading State

```vue
<template>
  <Dialog
    v-model="showDialog"
    :options="{
      title: 'Confirm Action',
      message: 'Are you sure you want to proceed?',
      actions: [
        { label: 'Cancel', variant: 'subtle' },
        {
          label: 'Confirm',
          theme: 'blue',
          variant: 'solid',
          loading: isProcessing,
          onClick: handleConfirm
        }
      ]
    }"
  />
</template>

<script setup>
import { ref } from 'vue'
import { Dialog } from 'frappe-ui'

const showDialog = ref(false)
const isProcessing = ref(false)

const handleConfirm = async ({ close }) => {
  isProcessing.value = true

  // Simulate async operation
  await new Promise(resolve => setTimeout(resolve, 2000))

  isProcessing.value = false
  close()
}
</script>
```

## Form Dialog

### Dialog with Form Fields

```vue
<template>
  <div>
    <Button
      label="Add New Item"
      theme="blue"
      variant="solid"
      icon-left="plus"
      @click="showFormDialog = true"
    />

    <Dialog
      v-model="showFormDialog"
      :options="{
        title: 'Add New Item',
        size: 'lg'
      }"
    >
      <template #body-content>
        <form @submit.prevent="submitForm" class="space-y-4">
          <FormControl
            v-model="form.name"
            label="Item Name"
            required
          />

          <FormControl
            v-model="form.category"
            type="select"
            label="Category"
            :options="categoryOptions"
            required
          />

          <FormControl
            v-model="form.price"
            type="number"
            label="Price"
          />

          <FormControl
            v-model="form.description"
            type="textarea"
            label="Description"
            rows="3"
          />
        </form>
      </template>

      <template #actions="{ close }">
        <Button label="Cancel" variant="subtle" @click="close" />
        <Button
          label="Save"
          theme="blue"
          variant="solid"
          :loading="saving"
          @click="submitForm(close)"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Dialog, Button, FormControl, toast } from 'frappe-ui'

const showFormDialog = ref(false)
const saving = ref(false)

const form = reactive({
  name: '',
  category: '',
  price: null,
  description: ''
})

const categoryOptions = [
  { label: 'Electronics', value: 'electronics' },
  { label: 'Clothing', value: 'clothing' },
  { label: 'Books', value: 'books' }
]

const resetForm = () => {
  form.name = ''
  form.category = ''
  form.price = null
  form.description = ''
}

const submitForm = async (close) => {
  if (!form.name || !form.category) {
    toast({
      type: 'error',
      message: 'Please fill in required fields'
    })
    return
  }

  saving.value = true

  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000))

  toast({
    type: 'success',
    message: 'Item created successfully'
  })

  resetForm()
  saving.value = false
  close()
}
</script>
```

## Dialog Slots

### Using All Available Slots

```vue
<template>
  <Dialog v-model="showDialog">
    <!-- Full body override -->
    <template #body>
      <div class="p-6">
        <!-- Custom header -->
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold">Custom Dialog</h2>
          <Button icon="x" variant="ghost" @click="showDialog = false" />
        </div>

        <!-- Custom content -->
        <div class="py-4">
          <p>This dialog uses the #body slot for complete customization.</p>
        </div>

        <!-- Custom footer -->
        <div class="flex justify-end space-x-2 pt-4 border-t">
          <Button label="Close" @click="showDialog = false" />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button } from 'frappe-ui'

const showDialog = ref(false)
</script>
```

### Using Individual Slots

```vue
<template>
  <Dialog v-model="showDialog" :options="{ title: 'Edit User' }">
    <!-- Custom title area -->
    <template #body-title>
      <div class="flex items-center space-x-2">
        <Avatar :label="user.name" size="sm" />
        <span class="font-semibold">{{ user.name }}</span>
      </div>
    </template>

    <!-- Main content -->
    <template #body-content>
      <div class="space-y-4">
        <FormControl v-model="user.name" label="Name" />
        <FormControl v-model="user.email" label="Email" type="email" />
      </div>
    </template>

    <!-- Custom actions -->
    <template #actions="{ close }">
      <div class="flex justify-between w-full">
        <Button
          label="Delete User"
          theme="red"
          variant="subtle"
          icon-left="trash"
        />
        <div class="space-x-2">
          <Button label="Cancel" @click="close" />
          <Button label="Save" theme="blue" variant="solid" @click="saveUser(close)" />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Dialog, Button, FormControl, Avatar } from 'frappe-ui'

const showDialog = ref(false)
const user = reactive({
  name: 'John Doe',
  email: 'john@example.com'
})

const saveUser = (close) => {
  console.log('Saving user:', user)
  close()
}
</script>
```

## Nested Dialogs

```vue
<template>
  <div>
    <Button label="Open Parent Dialog" @click="showParentDialog = true" />

    <Dialog
      v-model="showParentDialog"
      :options="{
        title: 'Parent Dialog',
        size: 'lg'
      }"
    >
      <template #body-content>
        <p class="mb-4">This is the parent dialog.</p>
        <Button label="Open Child Dialog" @click="showChildDialog = true" />
      </template>
    </Dialog>

    <Dialog
      v-model="showChildDialog"
      :options="{
        title: 'Child Dialog',
        size: 'sm'
      }"
    >
      <template #body-content>
        <p>This is a nested child dialog.</p>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button } from 'frappe-ui'

const showParentDialog = ref(false)
const showChildDialog = ref(false)
</script>
```

## Prevent Outside Click Close

```vue
<template>
  <Dialog
    v-model="showDialog"
    :disable-outside-click-to-close="true"
    :options="{
      title: 'Important Form',
      message: 'Please complete this form. Click Cancel to close.'
    }"
  >
    <template #body-content>
      <FormControl v-model="inputValue" label="Required Field" required />
    </template>

    <template #actions="{ close }">
      <Button label="Cancel" @click="close" />
      <Button label="Submit" theme="blue" variant="solid" @click="submit(close)" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button, FormControl } from 'frappe-ui'

const showDialog = ref(false)
const inputValue = ref('')

const submit = (close) => {
  if (inputValue.value) {
    close()
  }
}
</script>
```

## Dialog Events

```vue
<template>
  <Dialog
    v-model="showDialog"
    :options="{ title: 'Event Example' }"
    @close="handleClose"
    @after-leave="handleAfterLeave"
  >
    <template #body-content>
      <p>Close this dialog to see events fire.</p>
    </template>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, toast } from 'frappe-ui'

const showDialog = ref(false)

const handleClose = () => {
  console.log('Dialog is closing')
}

const handleAfterLeave = () => {
  toast({
    type: 'info',
    message: 'Dialog animation completed'
  })
}
</script>
```

## Composable for Reusable Dialogs

Create a reusable dialog composable:

```javascript
// composables/useConfirmDialog.js
import { ref, h } from 'vue'
import { Dialog, Button } from 'frappe-ui'

export function useConfirmDialog() {
  const isOpen = ref(false)
  const resolvePromise = ref(null)

  const confirm = (options = {}) => {
    return new Promise((resolve) => {
      resolvePromise.value = resolve
      isOpen.value = true
    })
  }

  const handleConfirm = () => {
    isOpen.value = false
    resolvePromise.value?.(true)
  }

  const handleCancel = () => {
    isOpen.value = false
    resolvePromise.value?.(false)
  }

  return {
    isOpen,
    confirm,
    handleConfirm,
    handleCancel
  }
}
```

Usage in component:

```vue
<template>
  <div>
    <Button label="Delete" theme="red" @click="handleDelete" />

    <Dialog
      v-model="isOpen"
      :options="{
        title: 'Confirm Delete',
        message: 'Are you sure?',
        actions: [
          { label: 'Cancel', onClick: handleCancel },
          { label: 'Delete', theme: 'red', variant: 'solid', onClick: handleConfirm }
        ]
      }"
    />
  </div>
</template>

<script setup>
import { Dialog, Button, toast } from 'frappe-ui'
import { useConfirmDialog } from './composables/useConfirmDialog'

const { isOpen, confirm, handleConfirm, handleCancel } = useConfirmDialog()

const handleDelete = async () => {
  const confirmed = await confirm()

  if (confirmed) {
    toast({ type: 'success', message: 'Item deleted!' })
  }
}
</script>
```

## Common Pitfalls

### 1. Dialog Not Closing

**Problem:** Dialog stays open after action.

**Solution:** Make sure to call `close()` from the action:
```javascript
actions: [
  {
    label: 'OK',
    onClick: ({ close }) => {
      // Do something
      close()  // Don't forget this!
    }
  }
]
```

### 2. Form State Persists

**Problem:** Form values remain after closing and reopening.

**Solution:** Reset form when dialog closes:
```vue
<Dialog
  v-model="showDialog"
  @close="resetForm"
>
```

### 3. Async Actions Not Showing Loading

**Problem:** Button doesn't show loading state.

**Solution:** Use reactive loading ref with the action:
```javascript
const loading = ref(false)

const options = computed(() => ({
  actions: [
    {
      label: 'Submit',
      loading: loading.value,  // Must be computed/reactive
      onClick: async ({ close }) => {
        loading.value = true
        await doSomething()
        loading.value = false
        close()
      }
    }
  ]
}))
```

## Next Steps

- Learn about [Data Fetching with Resources](./05-data-fetching-resources.md)
- Build complex [Forms](./08-form-handling.md)
- Add [Toast Notifications](./07-toast-notifications.md)
