# Basic Components Tutorial

## Overview

This tutorial covers the fundamental UI components in frappe-ui: Button, Badge, Avatar, Alert, and Tooltip. These components form the building blocks of any frappe-ui application.

## Button Component

The Button component is the most commonly used interactive element.

### Basic Usage

```vue
<template>
  <div class="space-x-2">
    <Button label="Default" />
    <Button label="Primary" theme="blue" variant="solid" />
    <Button label="Danger" theme="red" variant="solid" />
    <Button label="Success" theme="green" variant="solid" />
  </div>
</template>

<script setup>
import { Button } from 'frappe-ui'
</script>
```

### Button Variants

```vue
<template>
  <div class="space-y-4">
    <!-- Subtle (default) -->
    <Button label="Subtle" theme="blue" variant="subtle" />

    <!-- Solid -->
    <Button label="Solid" theme="blue" variant="solid" />

    <!-- Outline -->
    <Button label="Outline" theme="blue" variant="outline" />

    <!-- Ghost -->
    <Button label="Ghost" theme="blue" variant="ghost" />
  </div>
</template>
```

### Button Sizes

```vue
<template>
  <div class="flex items-center space-x-2">
    <Button label="Small" size="sm" theme="blue" variant="solid" />
    <Button label="Medium" size="md" theme="blue" variant="solid" />
    <Button label="Large" size="lg" theme="blue" variant="solid" />
    <Button label="Extra Large" size="xl" theme="blue" variant="solid" />
  </div>
</template>
```

### Buttons with Icons

```vue
<template>
  <div class="space-x-2">
    <!-- Icon only -->
    <Button icon="plus" tooltip="Add item" />

    <!-- Icon on left -->
    <Button label="Save" icon-left="save" theme="blue" variant="solid" />

    <!-- Icon on right -->
    <Button label="Next" icon-right="arrow-right" theme="blue" variant="solid" />

    <!-- Using custom icon component -->
    <Button :icon="PlusIcon" tooltip="Custom icon" />
  </div>
</template>

<script setup>
import { Button } from 'frappe-ui'
import { PlusIcon } from 'lucide-vue-next'
</script>
```

### Loading State

```vue
<template>
  <Button
    label="Saving..."
    :loading="isSaving"
    loading-text="Please wait..."
    theme="blue"
    variant="solid"
    @click="save"
  />
</template>

<script setup>
import { ref } from 'vue'
import { Button } from 'frappe-ui'

const isSaving = ref(false)

const save = async () => {
  isSaving.value = true
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 2000))
  isSaving.value = false
}
</script>
```

### Button as Link

```vue
<template>
  <div class="space-x-2">
    <!-- Router link -->
    <Button label="Go to Dashboard" route="/dashboard" theme="blue" />

    <!-- External link -->
    <Button label="Visit Website" link="https://frappe.io" icon-right="external-link" />
  </div>
</template>
```

## Badge Component

Badges are used to highlight status, counts, or labels.

### Basic Badges

```vue
<template>
  <div class="space-x-2">
    <Badge>Default</Badge>
    <Badge theme="blue">Blue</Badge>
    <Badge theme="green">Green</Badge>
    <Badge theme="red">Red</Badge>
    <Badge theme="orange">Orange</Badge>
    <Badge theme="yellow">Yellow</Badge>
  </div>
</template>

<script setup>
import { Badge } from 'frappe-ui'
</script>
```

### Badge Variants

```vue
<template>
  <div class="space-y-2">
    <div class="space-x-2">
      <Badge theme="blue" variant="subtle">Subtle</Badge>
      <Badge theme="blue" variant="solid">Solid</Badge>
      <Badge theme="blue" variant="outline">Outline</Badge>
    </div>
  </div>
</template>
```

### Status Badges

```vue
<template>
  <div class="space-x-2">
    <Badge :theme="getStatusTheme('Open')">Open</Badge>
    <Badge :theme="getStatusTheme('In Progress')">In Progress</Badge>
    <Badge :theme="getStatusTheme('Completed')">Completed</Badge>
    <Badge :theme="getStatusTheme('Cancelled')">Cancelled</Badge>
  </div>
</template>

<script setup>
import { Badge } from 'frappe-ui'

const getStatusTheme = (status) => {
  const themes = {
    'Open': 'blue',
    'In Progress': 'orange',
    'Completed': 'green',
    'Cancelled': 'red'
  }
  return themes[status] || 'gray'
}
</script>
```

## Avatar Component

Display user avatars with images, initials, or icons.

### Basic Avatars

```vue
<template>
  <div class="flex items-center space-x-2">
    <!-- With image -->
    <Avatar image="https://i.pravatar.cc/100" label="John Doe" />

    <!-- With initials (no image) -->
    <Avatar label="Jane Smith" />

    <!-- Different sizes -->
    <Avatar label="Small" size="sm" />
    <Avatar label="Medium" size="md" />
    <Avatar label="Large" size="lg" />
    <Avatar label="XL" size="xl" />
    <Avatar label="2XL" size="2xl" />
  </div>
</template>

<script setup>
import { Avatar } from 'frappe-ui'
</script>
```

### Avatar with Fallback

```vue
<template>
  <Avatar
    :image="user.avatar"
    :label="user.name"
    :fallback-icon="UserIcon"
  />
</template>

<script setup>
import { Avatar } from 'frappe-ui'
import { UserIcon } from 'lucide-vue-next'

const user = {
  name: 'John Doe',
  avatar: null // Will show initials "JD"
}
</script>
```

## Alert Component

Display important messages to users.

### Alert Types

```vue
<template>
  <div class="space-y-4">
    <Alert title="Information" theme="blue">
      This is an informational message.
    </Alert>

    <Alert title="Success!" theme="green">
      Your changes have been saved successfully.
    </Alert>

    <Alert title="Warning" theme="orange">
      Please review before proceeding.
    </Alert>

    <Alert title="Error" theme="red">
      Something went wrong. Please try again.
    </Alert>
  </div>
</template>

<script setup>
import { Alert } from 'frappe-ui'
</script>
```

### Dismissible Alert

```vue
<template>
  <Alert
    v-if="showAlert"
    title="Heads up!"
    theme="blue"
    :dismissible="true"
    @dismiss="showAlert = false"
  >
    You can dismiss this alert by clicking the X button.
  </Alert>
</template>

<script setup>
import { ref } from 'vue'
import { Alert } from 'frappe-ui'

const showAlert = ref(true)
</script>
```

## Tooltip Component

Add helpful tooltips to any element.

### Basic Tooltip

```vue
<template>
  <Tooltip text="This is a helpful tooltip">
    <Button icon="info" />
  </Tooltip>
</template>

<script setup>
import { Tooltip, Button } from 'frappe-ui'
</script>
```

### Tooltip Positions

```vue
<template>
  <div class="flex space-x-4">
    <Tooltip text="Top tooltip" placement="top">
      <Button label="Top" />
    </Tooltip>

    <Tooltip text="Bottom tooltip" placement="bottom">
      <Button label="Bottom" />
    </Tooltip>

    <Tooltip text="Left tooltip" placement="left">
      <Button label="Left" />
    </Tooltip>

    <Tooltip text="Right tooltip" placement="right">
      <Button label="Right" />
    </Tooltip>
  </div>
</template>
```

### Button with Built-in Tooltip

```vue
<template>
  <!-- Buttons have built-in tooltip support -->
  <Button
    icon="trash"
    theme="red"
    tooltip="Delete this item"
  />
</template>
```

## Practical Example: Action Bar

Combining components to create a reusable action bar:

```vue
<template>
  <div class="flex items-center justify-between p-4 bg-white border rounded-lg">
    <div class="flex items-center space-x-3">
      <Avatar :image="user.avatar" :label="user.name" size="md" />
      <div>
        <p class="font-medium">{{ user.name }}</p>
        <Badge :theme="getStatusTheme(user.status)">{{ user.status }}</Badge>
      </div>
    </div>

    <div class="flex items-center space-x-2">
      <Tooltip text="Edit user">
        <Button icon="edit" @click="editUser" />
      </Tooltip>

      <Tooltip text="Send message">
        <Button icon="message-square" @click="sendMessage" />
      </Tooltip>

      <Button
        label="Save"
        theme="blue"
        variant="solid"
        :loading="saving"
        @click="saveChanges"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, Badge, Avatar, Tooltip } from 'frappe-ui'

const user = {
  name: 'John Doe',
  avatar: 'https://i.pravatar.cc/100',
  status: 'Active'
}

const saving = ref(false)

const getStatusTheme = (status) => {
  return status === 'Active' ? 'green' : 'gray'
}

const editUser = () => {
  console.log('Edit user')
}

const sendMessage = () => {
  console.log('Send message')
}

const saveChanges = async () => {
  saving.value = true
  await new Promise(r => setTimeout(r, 1000))
  saving.value = false
}
</script>
```

## Common Pitfalls

### 1. Missing Icon Names

**Problem:** Icons don't appear.

**Solution:** frappe-ui uses Feather Icons by default. Use valid icon names:
```vue
<!-- Correct -->
<Button icon="plus" />
<Button icon="trash-2" />

<!-- Incorrect -->
<Button icon="add" />
<Button icon="delete" />
```

### 2. Theme vs Variant Confusion

**Problem:** Colors don't apply as expected.

**Solution:**
- `theme` controls the color (gray, blue, red, green, orange)
- `variant` controls the style (subtle, solid, outline, ghost)

### 3. Button Click Not Working

**Problem:** Button click events don't fire.

**Solution:** Use `@click` not `:onClick`:
```vue
<!-- Correct -->
<Button @click="handleClick" />

<!-- Incorrect -->
<Button :onClick="handleClick" />
```

## Next Steps

- Learn about [Input Components](./03-input-components.md)
- Explore [Dialog and Modal](./04-dialogs-modals.md)
- Understand [Data Fetching](./05-data-fetching-resources.md)
