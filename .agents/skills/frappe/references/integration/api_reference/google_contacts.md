# API Reference: google_contacts.py

**Language**: Python

**Source**: `doctype/google_contacts/google_contacts.py`

---

## Classes

### GoogleContacts

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_access_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### authorize_access(g_contact, reauthorize = False, code = None)

If no Authorization code get it from Google and then request for Refresh Token.
Google Contact Name is set to flags to set_value after Authorization Code is obtained.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_contact | None | - | - |
| reauthorize | None | False | - |
| code | None | None | - |

**Returns**: (none)



### get_google_contacts_object(g_contact)

Return an object of Google Calendar along with Google Calendar doc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_contact | None | - | - |

**Returns**: (none)



### sync(g_contact = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_contact | None | None | - |

**Returns**: (none)



### sync_contacts_from_google_contacts(g_contact)

Syncs Contacts from Google Contacts.
https://developers.google.com/people/api/rest/v1/people.connections/list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_contact | None | - | - |

**Returns**: (none)



### insert_contacts_to_google_contacts(doc, method = None)

Syncs Contacts from Google Contacts.
https://developers.google.com/people/api/rest/v1/people/createContact

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### update_contacts_to_google_contacts(doc, method = None)

Syncs Contacts from Google Contacts.
https://developers.google.com/people/api/rest/v1/people/updateContact

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### get_indexed_value(d, index, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |
| index | None | - | - |
| key | None | - | - |

**Returns**: (none)


