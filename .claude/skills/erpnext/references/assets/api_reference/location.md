# API Reference: location.py

**Language**: Python

**Source**: `doctype/location/location.py`

---

## Classes

### Location

**Inherits from**: NestedSet

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_location_area(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_location_features(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_location_features(self, features)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| features | None | - | - |


##### update_ancestor_location_features(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_ancestor_location_features(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_child_property(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### feature_seperator(self, child_feature = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| child_feature | None | None | - |




## Functions

### compute_area(features)

Calculate the total area for a set of location features.
Reference from https://github.com/scisco/area.

Args:
        `features` (list of dict): Features marked on the map as
                GeoJSON data

Returns:
        float: The approximate signed geodesic area (in sq. meters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| features | None | - | - |

**Returns**: (none)



### _polygon_area(coords)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| coords | None | - | - |

**Returns**: (none)



### _ring_area(coords)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| coords | None | - | - |

**Returns**: (none)



### get_children(doctype, parent = None, location = None, is_root = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | None | - |
| location | None | None | - |
| is_root | None | False | - |

**Returns**: (none)



### add_node()

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)


