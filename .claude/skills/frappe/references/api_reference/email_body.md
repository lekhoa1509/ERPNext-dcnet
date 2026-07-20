# API Reference: email_body.py

**Language**: Python

**Source**: `email/email_body.py`

---

## Classes

### EMail

Wrapper on the email module. Email object represents emails to be sent to the client.
Also provides a clean way to add binary `FileData` attachments
Also sets all messages as multipart/alternative for cleaner reading in text-only clients

**Inherits from**: (none)

#### Methods

##### __init__(self, sender = '', recipients = (), subject = '', alternative = 0, reply_to = None, cc = (), bcc = (), email_account = None, expose_recipients = None, x_priority: Literal[1, 3, 5] = 3)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sender | None | '' | - |
| recipients | None | () | - |
| subject | None | '' | - |
| alternative | None | 0 | - |
| reply_to | None | None | - |
| cc | None | () | - |
| bcc | None | () | - |
| email_account | None | None | - |
| expose_recipients | None | None | - |
| x_priority | Literal[1, 3, 5] | 3 | - |


##### set_html(self, message, text_content = None, footer = None, print_html = None, formatted = None, inline_images = None, header = None)

Attach message in the html portion of multipart/alternative

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |
| text_content | None | None | - |
| footer | None | None | - |
| print_html | None | None | - |
| formatted | None | None | - |
| inline_images | None | None | - |
| header | None | None | - |


##### set_text(self, message)

Attach message in the text portion of multipart/alternative

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |


##### set_part_html(self, message, inline_images)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |
| inline_images | None | - | - |


##### set_html_as_text(self, html)

Set plain text from HTML

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| html | None | - | - |


##### set_message(self, message, mime_type = 'text/html', as_attachment = 0, filename = 'attachment.html')

Append the message with MIME content to the root node (as attachment)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |
| mime_type | None | 'text/html' | - |
| as_attachment | None | 0 | - |
| filename | None | 'attachment.html' | - |


##### attach_file(self, n)

attach a file from the `FileData` table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| n | None | - | - |


##### add_attachment(self, fname, fcontent, content_type = None, parent = None, content_id = None, inline = False)

add attachment

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fname | None | - | - |
| fcontent | None | - | - |
| content_type | None | None | - |
| parent | None | None | - |
| content_id | None | None | - |
| inline | None | False | - |


##### add_pdf_attachment(self, name, html, options = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |
| html | None | - | - |
| options | None | None | - |


##### validate(self)

validate the Email Addresses

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### replace_sender(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### replace_sender_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_message_id(self, message_id, is_notification = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message_id | None | - | - |
| is_notification | None | False | - |


##### set_in_reply_to(self, in_reply_to)

Used to send the Message-Id of a received email back as In-Reply-To

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| in_reply_to | None | - | - |


##### add_headers(self, headers)

Add custom headers to the email

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| headers | None | - | - |


##### make(self)

build into msg_root

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_header(self, key, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| value | None | - | - |


##### as_string(self)

validate, build message and convert to string

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_email(recipients, sender = '', msg = '', subject = '[No Subject]', text_content = None, footer = None, print_html = None, formatted = None, attachments = None, content = None, reply_to = None, cc = None, bcc = None, email_account = None, expose_recipients = None, inline_images = None, header = None, x_priority: Literal[1, 3, 5] = 3)

Prepare an email with the following format:
- multipart/mixed
        - multipart/alternative
                - text/plain
                - multipart/related
                        - text/html
                        - inline image
                - attachment

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| recipients | None | - | - |
| sender | None | '' | - |
| msg | None | '' | - |
| subject | None | '[No Subject]' | - |
| text_content | None | None | - |
| footer | None | None | - |
| print_html | None | None | - |
| formatted | None | None | - |
| attachments | None | None | - |
| content | None | None | - |
| reply_to | None | None | - |
| cc | None | None | - |
| bcc | None | None | - |
| email_account | None | None | - |
| expose_recipients | None | None | - |
| inline_images | None | None | - |
| header | None | None | - |
| x_priority | Literal[1, 3, 5] | 3 | - |

**Returns**: (none)



### get_formatted_html(subject, message, footer = None, print_html = None, email_account = None, header = None, unsubscribe_link: frappe._dict | None = None, sender = None, with_container = False, raw_html = False, add_css = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| subject | None | - | - |
| message | None | - | - |
| footer | None | None | - |
| print_html | None | None | - |
| email_account | None | None | - |
| header | None | None | - |
| unsubscribe_link | frappe._dict | None | None | - |
| sender | None | None | - |
| with_container | None | False | - |
| raw_html | None | False | - |
| add_css | None | True | - |

**Returns**: (none)



### get_email_html(template, args, subject, header = None, with_container = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template | None | - | - |
| args | None | - | - |
| subject | None | - | - |
| header | None | None | - |
| with_container | None | False | - |

**Returns**: (none)



### inline_style_in_html(html, add_css = True)

Convert email.css and html to inline-styled html.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |
| add_css | None | True | - |

**Returns**: (none)



### add_attachment(fname, fcontent, content_type = None, parent = None, content_id = None, inline = False)

Add attachment to parent which must an email object

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fname | None | - | - |
| fcontent | None | - | - |
| content_type | None | None | - |
| parent | None | None | - |
| content_id | None | None | - |
| inline | None | False | - |

**Returns**: (none)



### get_message_id()

Return Message ID created from doctype and name.

**Returns**: (none)



### get_signature(email_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |

**Returns**: (none)



### get_footer(email_account, footer = None)

append a footer (signature)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |
| footer | None | None | - |

**Returns**: (none)



### replace_filename_with_cid(message)

Replaces <img embed="assets/frappe/images/filename.jpg" ...> with
<img src="cid:content_id" ...> and return the modified message and
a list of inline_images with {filename, filecontent, content_id}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | None | - | - |

**Returns**: (none)



### get_filecontent_from_path(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### get_header(header = None)

Build header from template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| header | None | None | - |

**Returns**: (none)



### sanitize_email_header(header: str)

Removes all line boundaries in the headers.

Email Policy (python's std) has some bugs in it which uses splitlines
and raises ValueError (ref: https://github.com/python/cpython/blob/main/Lib/email/policy.py#L143).
Hence removing all line boundaries while sanitization of headers to prevent such faliures.
The line boundaries which are removed can be found here: https://docs.python.org/3/library/stdtypes.html#str.splitlines

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| header | str | - | - |

**Returns**: (none)



### get_brand_logo(email_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |

**Returns**: (none)


