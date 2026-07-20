# API Reference: chart_of_accounts_importer.py

**Language**: Python

**Source**: `doctype/chart_of_accounts_importer/chart_of_accounts_importer.py`

---

## Classes

### ChartofAccountsImporter

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### validate_columns(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### validate_company(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### import_coa(file_name, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_name | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_file(file_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_name | None | - | - |

**Returns**: (none)



### generate_data_from_csv(file_doc, as_dict = False)

read csv file and return the generated nested tree

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_doc | None | - | - |
| as_dict | None | False | - |

**Returns**: (none)



### generate_data_from_excel(file_doc, extension, as_dict = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_doc | None | - | - |
| extension | None | - | - |
| as_dict | None | False | - |

**Returns**: (none)



### get_coa(doctype, parent, is_root = False, file_name = None, for_validate = 0)

called by tree view (to fetch node's children)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | - | - |
| is_root | None | False | - |
| file_name | None | None | - |
| for_validate | None | 0 | - |

**Returns**: (none)



### build_forest(data)

converts list of list into a nested tree
if a = [[1,1], [1,2], [3,2], [4,4], [5,4]]
tree = {
        1: {
                2: {
                        3: {}
                }
        },
        4: {
                5: {}
        }
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### build_response_as_excel(writer)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| writer | None | - | - |

**Returns**: (none)



### download_template(file_type, template_type, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_type | None | - | - |
| template_type | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_template(template_type, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template_type | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_sample_template(writer, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| writer | None | - | - |
| company | None | - | - |

**Returns**: (none)



### validate_accounts(file_doc, extension)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_doc | None | - | - |
| extension | None | - | - |

**Returns**: (none)



### validate_root(accounts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |

**Returns**: (none)



### validate_missing_roots(roots)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| roots | None | - | - |

**Returns**: (none)



### get_root_types()

**Returns**: (none)



### get_report_type(root_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| root_type | None | - | - |

**Returns**: (none)



### get_mandatory_group_accounts()

**Returns**: (none)



### get_mandatory_account_types()

**Returns**: (none)



### unset_existing_data(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### set_default_accounts(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### set_nested(d, path, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |
| path | None | - | - |
| value | None | - | - |

**Returns**: (none)



### return_parent(data, child)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| child | None | - | - |

**Returns**: (none)


