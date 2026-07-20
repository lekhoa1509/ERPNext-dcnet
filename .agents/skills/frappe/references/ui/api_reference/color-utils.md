# API Reference: color-utils.ts

**Language**: TypeScript

**Source**: `src/components/TextEditor/extensions/shared/color-utils.ts`

---

## Functions

### getClosestNamedColor(color: string, allowedColors: string[], colorMap: Record<string, string>, legacyMap?: Record<string, string>)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| color | string | - | - |
| allowedColors | string[] | - | - |
| colorMap | Record<string | - | - |
| string> | None | - | - |
| legacyMap? | Record<string | - | - |
| string> | None | - | - |

**Returns**: (none)



### extractColorFromStyle(style: string, allowedColors: string[], colorMap: Record<string, string> = textColorHexMap, legacyMap: Record<string, string> = legacyTextColorMap, property: string = 'color')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| style | string | - | - |
| allowedColors | string[] | - | - |
| colorMap | Record<string | - | - |
| string> | None | textColorHexMap | - |
| legacyMap | Record<string | - | - |
| string> | None | legacyTextColorMap | - |
| property | string | 'color' | - |

**Returns**: (none)



### extractTextColorFromStyle(style: string, allowedColors: string[])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| style | string | - | - |
| allowedColors | string[] | - | - |

**Returns**: (none)



### extractHighlightColorFromStyle(style: string, allowedColors: string[])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| style | string | - | - |
| allowedColors | string[] | - | - |

**Returns**: (none)


