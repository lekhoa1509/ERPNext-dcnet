# API Reference: mask.py

**Language**: Python

**Source**: `model/utils/mask.py`

---

## Functions

### mask_field_value(field, val)

Mask a field value based on its fieldtype and options.

Args:
        field: DocField object with fieldtype and options attributes
        val: The value to mask

Returns:
        Masked value based on field type, or original value if None/empty

Masking patterns:
        - Phone (Data + Phone option): Shows first 3 chars + "XXXXXX"
        - Email (Data + Email option): Shows "XXXXXX@domain"
        - Date: Shows "XX-XX-XXXX"
        - Time: Shows "XX:XX"
        - Default: Shows "XXXXXXXX"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | None | - | - |
| val | None | - | - |

**Returns**: (none)



### mask_dict_results(result, masked_fields)

Mask fields in dictionary results.

Args:
        result: List of dictionaries containing query results
        masked_fields: List of DocField objects with masking configuration

Returns:
        Result with masked field values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| result | None | - | - |
| masked_fields | None | - | - |

**Returns**: (none)



### mask_list_results(result, masked_fields, field_index_map)

Mask fields in list/tuple results.

Args:
        result: List of tuples containing query results
        masked_fields: List of DocField objects with masking configuration
        field_index_map: Dict mapping field names to their position in result tuples

Returns:
        List of tuples with masked field values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| result | None | - | - |
| masked_fields | None | - | - |
| field_index_map | None | - | - |

**Returns**: (none)


