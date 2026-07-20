# API Reference: helpers.ts

**Language**: TypeScript

**Source**: `src/components/Charts/helpers.ts`

---

## Functions

### formatLabel(name: string)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | string | - | - |

**Returns**: (none)



### formatValue(value: number, precision = 0, shorten = false)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | number | - | - |
| precision | None | 0 | - |
| shorten | None | false | - |

**Returns**: (none)



### guessPrecision(number: number)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| number | number | - | - |

**Returns**: (none)



### formatDate(date: string, format?: string, grain: TimeGrain = 'day')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | string | - | - |
| format? | string | - | - |
| grain | TimeGrain | 'day' | - |

**Returns**: (none)



### isObject(item: any)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | any | - | - |

**Returns**: (none)



### mergeDeep(target: any, ...sources: any[])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| target | any | - | - |
| ...sources | any[] | - | - |

**Returns**: (none)


