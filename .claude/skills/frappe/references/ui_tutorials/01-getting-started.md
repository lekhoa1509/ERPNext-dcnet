# Getting Started with Frappe UI

## Overview

This tutorial will guide you through setting up a new Vue 3 frontend project using frappe-ui, the official component library for building modern single-page applications (SPAs) that integrate with Frappe Framework backends.

## Prerequisites

- Node.js 16+ installed
- Basic knowledge of Vue 3 and Composition API
- A Frappe Framework application (optional for basic setup)

## Quick Setup with Starter Template

The fastest way to get started is using the official frappe-ui-starter template.

### Step 1: Create a Frappe App (Optional)

If you have a Frappe bench setup:

```bash
bench new-app myapp
cd apps/myapp
```

### Step 2: Setup Frontend with frappe-ui-starter

```bash
# Inside your app directory
npx degit netchampfaris/frappe-ui-starter frontend

# Navigate to frontend
cd frontend

# Install dependencies
yarn install
# or
npm install
```

### Step 3: Configure CSRF (For Frappe Backend)

If connecting to a Frappe backend during development:

```bash
bench --site mysite.local set-config ignore_csrf 1
```

This prevents CSRF token errors during development. In production, the CSRF token is automatically attached to the window object.

### Step 4: Start Development Server

```bash
yarn dev
# or
npm run dev
```

Your app will be available at `http://localhost:8080` (or your Frappe site URL with port 8080).

## Manual Setup

If you prefer setting up manually:

### Step 1: Create Vue 3 Project

```bash
npm create vite@latest my-frappe-app -- --template vue
cd my-frappe-app
npm install
```

### Step 2: Install frappe-ui

```bash
npm install frappe-ui
# or
yarn add frappe-ui
```

### Step 3: Install Peer Dependencies

```bash
npm install tailwindcss @headlessui/vue @tiptap/vue-3 dayjs feather-icons
```

### Step 4: Configure Tailwind CSS

Create `tailwind.config.js`:

```javascript
module.exports = {
  presets: [
    require('frappe-ui/src/utils/tailwind.config')
  ],
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
    './node_modules/frappe-ui/src/**/*.{vue,js,ts}'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Create `postcss.config.js`:

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

Add to your main CSS file (`src/index.css`):

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 5: Initialize frappe-ui Plugin

Update `src/main.js`:

```javascript
import { createApp } from 'vue'
import { FrappeUI, setConfig, frappeRequest } from 'frappe-ui'
import App from './App.vue'
import './index.css'

const app = createApp(App)

// Use FrappeUI plugin
app.use(FrappeUI)

// Configure for Frappe backend (if using)
setConfig('resourceFetcher', frappeRequest)

app.mount('#app')
```

### Step 6: Create Your First Component

Update `src/App.vue`:

```vue
<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">My Frappe App</h1>

    <Button
      label="Click Me"
      theme="blue"
      variant="solid"
      @click="handleClick"
    />

    <div v-if="clicked" class="mt-4">
      <Alert title="Success!" theme="green">
        You clicked the button!
      </Alert>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, Alert } from 'frappe-ui'

const clicked = ref(false)

const handleClick = () => {
  clicked.value = true
}
</script>
```

## Project Structure

A typical frappe-ui project structure:

```
frontend/
├── src/
│   ├── components/     # Your custom components
│   ├── pages/          # Page components
│   ├── composables/    # Reusable composition functions
│   ├── router.js       # Vue Router configuration
│   ├── main.js         # App entry point
│   ├── App.vue         # Root component
│   └── index.css       # Tailwind imports
├── public/
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Common Pitfalls

### 1. CSRF Token Errors

**Problem:** Getting 403 Forbidden errors when making API calls.

**Solution:** Set `ignore_csrf 1` for development:
```bash
bench --site mysite set-config ignore_csrf 1
```

### 2. Missing Tailwind Styles

**Problem:** Components appear unstyled.

**Solution:** Ensure you:
- Added the frappe-ui preset in `tailwind.config.js`
- Included the `node_modules/frappe-ui/src` path in content
- Imported Tailwind in your CSS file

### 3. Resource Fetcher Not Configured

**Problem:** Resources return raw Frappe API responses with `message` wrapper.

**Solution:** Configure the Frappe request handler:
```javascript
import { setConfig, frappeRequest } from 'frappe-ui'
setConfig('resourceFetcher', frappeRequest)
```

### 4. Vite Proxy Issues

**Problem:** API calls fail because the backend is on a different port.

**Solution:** Configure Vite proxy in `vite.config.js`:
```javascript
export default {
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}
```

## Next Steps

- Learn about [Basic Components](./02-basic-components.md)
- Understand [Data Fetching with Resources](./05-data-fetching-resources.md)
- Build [Forms with FormControl](./08-form-handling.md)

## Resources

- [Official Documentation](https://frappeui.com)
- [GitHub Repository](https://github.com/frappe/frappe-ui)
- [Starter Template](https://github.com/netchampfaris/frappe-ui-starter)
