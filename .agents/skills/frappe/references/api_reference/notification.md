# API Reference: notification.py

**Language**: Python

**Source**: `email/doctype/notification/notification.py`

---

## Classes

### Notification

**Inherits from**: Document

#### Methods

##### onload(self)

load message

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### preview_meets_condition(self, preview_document)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| preview_document | None | - | - |


##### preview_message(self, preview_document)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| preview_document | None | - | - |


##### preview_subject(self, preview_document)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| preview_document | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_standard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_invalid_condition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_condition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_forbidden_document_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_documents_for_today(self)

get list of documents that will be triggered today

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_documents_for_this_moment(self) → list[Document]

Get list of documents that will be triggered at this moment.

This method retrieves documents based on the specified datetime field and minutes offset.
It considers documents that fall within the time range from the last run time plus the offset
up to the current time plus the offset.

Returns:
        list: A list of document objects that meet the criteria for notification.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[Document]`


##### queue_send(self, doc, enqueue_after_commit = True)

Enqueue the process to build recipients and send notifications.

This method is particularly useful for sending notifications, especially 'Custom'-type,
without the additional overhead associated with `Document.queue_action`.

Args:
              doc (Document): The document object for which the notification is being sent.
              enqueue_after_commit (bool, optional): If True, the task will be enqueued after
                the current transaction is committed. Defaults to True.

Note:
              This method is the recommended way to send 'Custom'-type notifications.

Example:
              To queue a notification from a server script:

              ```python
              notification = frappe.get_doc(
                  "Notification", "My Notification", ignore_permissions=True
              )
              notification.queue_send(customer)
              ```

              This example queues the "My Notification" to be sent for the specified customer document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| enqueue_after_commit | None | True | - |


##### send(self, doc)

Build recipients and send Notification

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### send_notification_by_channel(self, doc, context)

Send notification based on the specified channel.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| context | None | - | - |


##### create_system_notification(self, doc, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| context | None | - | - |


##### send_an_email(self, doc, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| context | None | - | - |


##### send_a_slack_msg(self, doc, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| context | None | - | - |


##### send_sms(self, doc, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| context | None | - | - |


##### get_mobile_no(doc, field)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| field | None | - | - |


##### get_list_of_recipients(self, doc, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| context | None | - | - |


##### get_receiver_list(self, doc, context, field_on_user = 'mobile_no', recipient_extractor_func = None)

return receiver list based on the doc field and role specified

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| context | None | - | - |
| field_on_user | None | 'mobile_no' | - |
| recipient_extractor_func | None | None | - |


##### get_attachment(self, doc) → list[dict]

Check Attachment Settings and return attachments accordingly

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |

**Returns**: `list[dict]`


##### get_print(self, doc)

check print settings and return dict with print info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_template(self, md_as_html = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| md_as_html | None | False | - |


##### load_standard_properties(self, context)

load templates and run get_context

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### clear_notification_cache()

**Returns**: (none)



### get_documents_for_today(notification)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| notification | None | - | - |

**Returns**: (none)



### trigger_offset_alerts()

**Returns**: (none)



### trigger_daily_alerts()

**Returns**: (none)



### trigger_notifications(doc, method = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### evaluate_alert(doc: Document, alert, event = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | Document | - | - |
| alert | None | - | - |
| event | None | None | - |

**Returns**: (none)



### get_context(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_assignees(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_emails_from_template(template, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template | None | - | - |
| context | None | - | - |

**Returns**: (none)



### get_reference_doctype(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_reference_name(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### _parse_receiver_by_document_field(s)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | None | - | - |

**Returns**: (none)


