# API Reference: help_article.py

**Language**: Python

**Source**: `website/doctype/help_article/help_article.py`

---

## Classes

### HelpArticle

**Inherits from**: WebsiteGenerator

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_route(self)

Set route from category and title if missing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_category(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_context(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### get_parents(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |




## Functions

### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### get_level_class(level)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level | None | - | - |

**Returns**: (none)



### get_sidebar_items()

**Returns**: (none)



### clear_knowledge_base_cache()

**Returns**: (none)



### add_feedback(article: str, helpful: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| article | str | - | - |
| helpful | str | - | - |

**Returns**: (none)



### _get()

**Returns**: (none)


