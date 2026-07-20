# API Reference: trace.py

**Language**: Python

**Source**: `model/trace.py`

---

## Classes

### TracedValue

A descriptor class for creating traced fields in Frappe documents.

This class allows for monitoring and validating changes to specific fields
in a Frappe document. It can enforce forbidden values and apply custom
validation logic.

Attributes:
        field_name (str): The name of the field being traced.
        forbidden_values (list): A list of values that are not allowed for this field.
        custom_validation (callable): A function for custom validation logic.

**Inherits from**: (none)

#### Methods

##### __init__(self, field_name, forbidden_values = None, custom_validation = None)

Initialize a TracedValue instance.

Args:
        field_name (str): The name of the field to be traced.
        forbidden_values (list, optional): A list of values that should not be allowed.
        custom_validation (callable, optional): A function for additional validation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_name | None | - | - |
| forbidden_values | None | None | - |
| custom_validation | None | None | - |


##### __get__(self, obj, objtype = None)

Get the value of the traced field.

Args:
        obj (object): The instance that this descriptor is accessed from.
        objtype (type, optional): The type of the instance.

Returns:
        The value of the traced field, or self if accessed from the class.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| obj | None | - | - |
| objtype | None | None | - |


##### __set__(self, obj, value)

Set the value of the traced field with validation.

This method checks against forbidden values and applies custom validation
before setting the value.

Args:
        obj (object): The instance that this descriptor is accessed from.
        value: The value to set for the traced field.

Raises:
        ValueError: If the value is forbidden or fails custom validation.
            Note: returns AssertionError in test mode to debug with the `--pdb` flag.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| obj | None | - | - |
| value | None | - | - |




### TracedDocument

A base class for Frappe documents with traced fields.

This class extends Frappe's Document class to provide support for
traced fields created with TracedValue.

Attributes:
        Inherits all attributes from frappe.model.document.Document

**Inherits from**: Document

#### Methods

##### __init__(self)

Initialize a TracedDocument instance.

This method sets up traced fields and initializes the parent Document.

Args:
        *args: Positional arguments to pass to the parent constructor.
        **kwargs: Keyword arguments to pass to the parent constructor.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_valid_dict(self)

Get a valid dictionary representation of the document.

This method extends the parent method to properly handle traced fields.

Args:
        *args: Positional arguments to pass to the parent method.
        **kwargs: Keyword arguments to pass to the parent method.

Returns:
        dict: A dictionary representation of the document, including traced fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### traced_field()

A convenience function for creating TracedValue instances.

This function simplifies the creation of traced fields in Frappe documents.

Args:
        *args: Positional arguments to pass to TracedValue constructor.
        **kwargs: Keyword arguments to pass to TracedValue constructor.

Returns:
        TracedValue: An instance of the TracedValue descriptor.

**Returns**: (none)


