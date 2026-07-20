# API Reference: image-extension.ts

**Language**: TypeScript

**Source**: `src/components/TextEditor/extensions/image/image-extension.ts`

---

## Functions

### findInsertPosition(view: EditorView, lastNodeId: string | null)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| view | EditorView | - | - |
| lastNodeId | string | null | - | - |

**Returns**: (none)



### uploadImageBase(file: File, view: EditorView, pos: number | null | undefined, options: Record<string, any>, insertMode: 'insert' | 'replace', onComplete?: (nodeId: string)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file | File | - | - |
| view | EditorView | - | - |
| pos | number | null | undefined | - | - |
| options | Record<string | - | - |
| any> | None | - | - |
| insertMode | 'insert' | 'replace' | - | - |
| onComplete? | (nodeId: string | - | - |

**Returns**: (none)



### uploadImageWithTracking(file: File, view: EditorView, pos: number | null | undefined, options: Record<string, any>, onComplete?: (nodeId: string)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file | File | - | - |
| view | EditorView | - | - |
| pos | number | null | undefined | - | - |
| options | Record<string | - | - |
| any> | None | - | - |
| onComplete? | (nodeId: string | - | - |

**Returns**: (none)



### uploadImage(file: File, view: EditorView, pos: number | null | undefined, options: Record<string, any>)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file | File | - | - |
| view | EditorView | - | - |
| pos | number | null | undefined | - | - |
| options | Record<string | - | - |
| any> | None | - | - |

**Returns**: (none)



### findImageNodeBySource(view: EditorView, src: string, callback: (node: Node, pos: number)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| view | EditorView | - | - |
| src | string | - | - |
| callback | (node: Node | - | - |
| pos | number | - | - |

**Returns**: (none)



### updateNodeWithDimensions(src: string, view: EditorView, pos: number)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| src | string | - | - |
| view | EditorView | - | - |
| pos | number | - | - |

**Returns**: (none)



### getImageDimensions(src: string)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| src | string | - | - |

**Returns**: (none)



### processMultipleImages(images: File[], view: EditorView, pos: number | null, options: Record<string, any>)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| images | File[] | - | - |
| view | EditorView | - | - |
| pos | number | null | - | - |
| options | Record<string | - | - |
| any> | None | - | - |

**Returns**: (none)



### processNextImage()

**Returns**: (none)


