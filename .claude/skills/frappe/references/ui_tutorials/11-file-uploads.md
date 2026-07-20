# File Uploads Tutorial

## Overview

frappe-ui provides components and utilities for handling file uploads with Frappe backend. This tutorial covers the FileUploader component, direct file uploads, and integration with form submissions.

## FileUploader Component

### Basic Usage

```vue
<template>
  <FileUploader
    @success="handleSuccess"
    @error="handleError"
  >
    <template v-slot="{ progress, uploading, openFileSelector }">
      <Button
        label="Upload File"
        :loading="uploading"
        @click="openFileSelector"
      />
      <div v-if="uploading" class="mt-2">
        <div class="w-full bg-gray-200 rounded h-2">
          <div
            class="bg-blue-500 h-2 rounded"
            :style="{ width: `${progress}%` }"
          />
        </div>
        <span class="text-sm text-gray-500">{{ progress }}%</span>
      </div>
    </template>
  </FileUploader>
</template>

<script setup>
import { FileUploader, Button, toast } from 'frappe-ui'

const handleSuccess = (file) => {
  toast({
    type: 'success',
    message: `${file.name} uploaded successfully`
  })
  console.log('File URL:', file.file_url)
}

const handleError = (error) => {
  toast({
    type: 'error',
    message: error.message || 'Upload failed'
  })
}
</script>
```

### FileUploader Props

```vue
<FileUploader
  :file-types="['image/*', '.pdf', '.doc', '.docx']"
  :max-file-size="5 * 1024 * 1024"
  :upload-args="{
    private: 1,
    doctype: 'Item',
    docname: 'ITEM-00001',
    fieldname: 'image'
  }"
  @success="onSuccess"
  @error="onError"
>
  <!-- slot content -->
</FileUploader>
```

| Prop | Type | Description |
|------|------|-------------|
| `fileTypes` | Array | Allowed file types (MIME types or extensions) |
| `maxFileSize` | Number | Maximum file size in bytes |
| `uploadArgs` | Object | Additional upload parameters |

### Upload Arguments

```javascript
uploadArgs: {
  // Make file private (accessible only to logged-in users)
  private: 1,

  // Attach to a specific document
  doctype: 'Item',
  docname: 'ITEM-00001',
  fieldname: 'image',

  // Or folder-based upload
  folder: 'Home/Attachments',

  // Custom file name
  file_name: 'custom-name.pdf'
}
```

## Drag and Drop Upload

### Drop Zone

```vue
<template>
  <FileUploader
    @success="handleUpload"
    v-slot="{ progress, uploading, openFileSelector, files, dragActive }"
  >
    <div
      class="border-2 border-dashed rounded-lg p-8 text-center transition-colors"
      :class="{
        'border-blue-500 bg-blue-50': dragActive,
        'border-gray-300': !dragActive
      }"
      @click="openFileSelector"
    >
      <div v-if="uploading">
        <FeatherIcon name="upload-cloud" class="w-12 h-12 mx-auto text-blue-500 animate-bounce" />
        <p class="mt-2 text-gray-600">Uploading... {{ progress }}%</p>
        <div class="w-64 mx-auto mt-2 bg-gray-200 rounded h-2">
          <div
            class="bg-blue-500 h-2 rounded transition-all"
            :style="{ width: `${progress}%` }"
          />
        </div>
      </div>

      <div v-else>
        <FeatherIcon name="upload-cloud" class="w-12 h-12 mx-auto text-gray-400" />
        <p class="mt-2 text-gray-600">
          <span class="text-blue-500 font-medium">Click to upload</span>
          or drag and drop
        </p>
        <p class="text-sm text-gray-400 mt-1">
          PNG, JPG, PDF up to 10MB
        </p>
      </div>
    </div>
  </FileUploader>
</template>

<script setup>
import { FileUploader, FeatherIcon, toast } from 'frappe-ui'

const handleUpload = (file) => {
  toast({ type: 'success', message: 'File uploaded!' })
  console.log('Uploaded:', file)
}
</script>
```

## Image Upload with Preview

```vue
<template>
  <div class="space-y-4">
    <!-- Image Preview -->
    <div v-if="imageUrl" class="relative w-48 h-48">
      <img
        :src="imageUrl"
        alt="Preview"
        class="w-full h-full object-cover rounded-lg"
      />
      <Button
        icon="x"
        size="sm"
        theme="red"
        variant="solid"
        class="absolute top-2 right-2"
        @click="removeImage"
      />
    </div>

    <!-- Upload Button -->
    <FileUploader
      v-else
      :file-types="['image/*']"
      :max-file-size="5 * 1024 * 1024"
      @success="handleImageUpload"
      v-slot="{ openFileSelector, uploading, progress }"
    >
      <div
        class="w-48 h-48 border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 transition-colors"
        @click="openFileSelector"
      >
        <div v-if="uploading">
          <Spinner class="w-8 h-8" />
          <p class="text-sm text-gray-500 mt-2">{{ progress }}%</p>
        </div>
        <div v-else class="text-center">
          <FeatherIcon name="image" class="w-8 h-8 text-gray-400 mx-auto" />
          <p class="text-sm text-gray-500 mt-2">Upload Image</p>
        </div>
      </div>
    </FileUploader>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FileUploader, Button, FeatherIcon, Spinner, toast } from 'frappe-ui'

const imageUrl = ref('')

const handleImageUpload = (file) => {
  imageUrl.value = file.file_url
  toast({ type: 'success', message: 'Image uploaded!' })
}

const removeImage = () => {
  // Optionally delete from server
  imageUrl.value = ''
}
</script>
```

## Multiple File Upload

```vue
<template>
  <div>
    <FileUploader
      @success="handleFileUpload"
      v-slot="{ openFileSelector, uploading }"
    >
      <Button
        label="Add Files"
        icon-left="plus"
        :loading="uploading"
        @click="openFileSelector"
      />
    </FileUploader>

    <!-- File List -->
    <div v-if="uploadedFiles.length" class="mt-4 space-y-2">
      <div
        v-for="(file, index) in uploadedFiles"
        :key="file.name"
        class="flex items-center justify-between p-3 border rounded-lg"
      >
        <div class="flex items-center gap-3">
          <FeatherIcon :name="getFileIcon(file.name)" class="w-5 h-5 text-gray-500" />
          <div>
            <p class="font-medium">{{ file.name }}</p>
            <p class="text-sm text-gray-500">{{ formatFileSize(file.file_size) }}</p>
          </div>
        </div>

        <div class="flex gap-2">
          <Button
            icon="download"
            variant="ghost"
            size="sm"
            @click="downloadFile(file)"
          />
          <Button
            icon="trash"
            variant="ghost"
            size="sm"
            theme="red"
            @click="removeFile(index)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FileUploader, Button, FeatherIcon } from 'frappe-ui'

const uploadedFiles = ref([])

const handleFileUpload = (file) => {
  uploadedFiles.value.push(file)
}

const removeFile = (index) => {
  uploadedFiles.value.splice(index, 1)
}

const downloadFile = (file) => {
  window.open(file.file_url, '_blank')
}

const getFileIcon = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  const icons = {
    pdf: 'file-text',
    doc: 'file-text',
    docx: 'file-text',
    xls: 'file-text',
    xlsx: 'file-text',
    png: 'image',
    jpg: 'image',
    jpeg: 'image',
    gif: 'image'
  }
  return icons[ext] || 'file'
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>
```

## Upload with Document Attachment

### Attach to Existing Document

```vue
<template>
  <div>
    <h3 class="font-medium mb-2">Attachments</h3>

    <div class="space-y-2">
      <div
        v-for="attachment in attachments"
        :key="attachment.name"
        class="flex items-center justify-between p-2 bg-gray-50 rounded"
      >
        <a
          :href="attachment.file_url"
          target="_blank"
          class="text-blue-600 hover:underline"
        >
          {{ attachment.file_name }}
        </a>
        <Button
          icon="trash"
          size="sm"
          variant="ghost"
          theme="red"
          @click="deleteAttachment(attachment.name)"
        />
      </div>
    </div>

    <FileUploader
      :upload-args="{
        doctype: props.doctype,
        docname: props.docname,
        is_private: 1
      }"
      @success="handleUpload"
      v-slot="{ openFileSelector, uploading }"
    >
      <Button
        label="Add Attachment"
        icon-left="paperclip"
        :loading="uploading"
        class="mt-2"
        @click="openFileSelector"
      />
    </FileUploader>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FileUploader, Button, createResource } from 'frappe-ui'

const props = defineProps({
  doctype: String,
  docname: String
})

const attachments = ref([])

// Fetch existing attachments
const fetchAttachments = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'File',
    filters: {
      attached_to_doctype: props.doctype,
      attached_to_name: props.docname
    },
    fields: ['name', 'file_name', 'file_url']
  },
  auto: true,
  onSuccess(data) {
    attachments.value = data
  }
})

const handleUpload = (file) => {
  attachments.value.push({
    name: file.name,
    file_name: file.file_name,
    file_url: file.file_url
  })
}

const deleteAttachment = async (name) => {
  if (confirm('Delete this attachment?')) {
    const deleteResource = createResource({
      url: 'frappe.client.delete',
      params: {
        doctype: 'File',
        name
      }
    })
    await deleteResource.submit()
    attachments.value = attachments.value.filter(a => a.name !== name)
  }
}
</script>
```

## Form with File Upload

```vue
<template>
  <form @submit.prevent="submitForm" class="space-y-4 max-w-lg">
    <FormControl
      v-model="form.item_name"
      label="Item Name"
      required
    />

    <FormControl
      v-model="form.description"
      type="textarea"
      label="Description"
    />

    <!-- Image Upload Field -->
    <div>
      <label class="block text-sm font-medium mb-1">Item Image</label>
      <div class="flex items-center gap-4">
        <div v-if="form.image" class="relative">
          <img
            :src="form.image"
            class="w-24 h-24 object-cover rounded"
          />
          <Button
            icon="x"
            size="sm"
            class="absolute -top-2 -right-2"
            @click="form.image = ''"
          />
        </div>

        <FileUploader
          v-else
          :file-types="['image/*']"
          @success="file => form.image = file.file_url"
          v-slot="{ openFileSelector, uploading }"
        >
          <div
            class="w-24 h-24 border-2 border-dashed rounded flex items-center justify-center cursor-pointer"
            @click="openFileSelector"
          >
            <Spinner v-if="uploading" />
            <FeatherIcon v-else name="plus" class="text-gray-400" />
          </div>
        </FileUploader>
      </div>
    </div>

    <Button
      type="submit"
      label="Create Item"
      theme="blue"
      variant="solid"
      :loading="creating"
    />
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  FormControl,
  Button,
  FileUploader,
  FeatherIcon,
  Spinner,
  createResource,
  toast
} from 'frappe-ui'

const creating = ref(false)

const form = reactive({
  item_name: '',
  description: '',
  image: ''
})

const createItem = createResource({
  url: 'frappe.client.insert',
  onSuccess(doc) {
    toast({ type: 'success', message: 'Item created!' })
    // Reset form
    form.item_name = ''
    form.description = ''
    form.image = ''
  },
  onError(error) {
    toast({ type: 'error', message: error.messages?.[0] || 'Failed' })
  }
})

const submitForm = () => {
  if (!form.item_name) {
    toast({ type: 'error', message: 'Name is required' })
    return
  }

  createItem.submit({
    doc: {
      doctype: 'Item',
      item_name: form.item_name,
      description: form.description,
      image: form.image
    }
  })
}
</script>
```

## Direct Upload with createResource

For advanced use cases, you can use createResource directly:

```javascript
import { createResource } from 'frappe-ui'

const uploadFile = createResource({
  url: 'frappe.client.upload_file',
  makeParams(file) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('is_private', 1)
    formData.append('doctype', 'Item')
    formData.append('docname', 'ITEM-00001')
    return formData
  },
  onSuccess(response) {
    console.log('Uploaded:', response.file_url)
  }
})

// Usage
const fileInput = document.querySelector('input[type="file"]')
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0]
  uploadFile.submit(file)
})
```

## Common Pitfalls

### 1. CORS Errors

**Problem:** Upload fails with CORS error in development.

**Solution:** Ensure your Frappe site is properly configured:
```bash
bench --site mysite set-config ignore_csrf 1
```

### 2. File Size Limits

**Problem:** Large files fail to upload.

**Solution:** Check both client and server limits:
```javascript
// Client-side
<FileUploader :max-file-size="10 * 1024 * 1024" />

// Server-side (site_config.json)
{
  "max_file_size": 10485760
}
```

### 3. Private Files Not Accessible

**Problem:** Uploaded private files return 403.

**Solution:** Ensure user has access to the attached document, or use public uploads:
```javascript
uploadArgs: {
  is_private: 0  // Make file public
}
```

### 4. File Type Validation

**Problem:** Wrong file types are allowed.

**Solution:** Use both MIME types and extensions:
```javascript
fileTypes: [
  'image/jpeg',
  'image/png',
  'application/pdf',
  '.doc',
  '.docx'
]
```

## Next Steps

- Learn about [Vue Router Integration](./12-routing.md)
- Explore [State Management](./13-state-management.md)
- Build [Complete SPA](./15-complete-spa-example.md)
