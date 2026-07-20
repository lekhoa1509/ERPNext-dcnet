# API Reference: email_account.py

**Language**: Python

**Source**: `email/doctype/email_account/email_account.py`

---

## Classes

### SentEmailInInbox

**Inherits from**: Exception



### EmailAccount

**Inherits from**: Document

#### Methods

##### autoname(self)

Set name as `email_account_name` or make title from Email Address.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

Validate Email Address and check POP3/IMAP and SMTP connections is enabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_frappe_mail_settings(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_smtp_conn(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

Check there is only one default of each type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### there_must_be_only_one_default(self)

If current Email Account is default, un-default all other accounts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_domain_values(self, domain: str)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| domain | str | - | - |


##### get_incoming_server(self, in_receive = False, email_sync_rule = 'UNSEEN')

Return logged in POP3/IMAP connection object.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| in_receive | None | False | - |
| email_sync_rule | None | 'UNSEEN' | - |


##### check_email_server_connection(self, email_server, in_receive)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email_server | None | - | - |
| in_receive | None | - | - |


##### _password(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### default_sender(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_exists_in_db(self)

Some of the Email Accounts we create from configs and those doesn't exists in DB.
This is is to check the specific email account exists in DB or not.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### from_record(cls, record)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| record | None | - | - |


##### find(cls, name)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| name | None | - | - |


##### find_one_by_filters(cls) → 'EmailAccount'

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `'EmailAccount'`


##### find_from_config(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### create_dummy(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### find_outgoing(cls, match_by_email = None, match_by_doctype = None, _raise_error = False)

Find the outgoing Email account to use.

:param match_by_email: Find account using emailID
:param match_by_doctype: Find account by matching `Append To` doctype
:param _raise_error: This is used by raise_error_on_no_output decorator to raise error.

**Decorators**: `@classmethod`, `@cache_email_account('outgoing_email_account')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| match_by_email | None | None | - |
| match_by_doctype | None | None | - |
| _raise_error | None | False | - |


##### find_default_outgoing(cls)

Find default outgoing account.

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### find_incoming(cls, match_by_email = None, match_by_doctype = None)

Find the incoming Email account to use.
:param match_by_email: Find account using emailID
:param match_by_doctype: Find account by matching `Append To` doctype

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| match_by_email | None | None | - |
| match_by_doctype | None | None | - |


##### find_default_incoming(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### get_account_details_from_site_config(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### get_access_token(self) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str | None`


##### sendmail_config(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_smtp_server(self)

Get SMTPServer (wrapper around actual smtplib object) for this account.

Implementation Detail: Since SMTPServer is same for each email connection, the same *instance*
is returned every time this function is called from same EmailAccount object.
This enables reusabilty of connection for better performance.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _smtp_server_instance(self)

**Decorators**: `@functools.cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_frappe_mail_client(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _frappe_mail_client(self)

**Decorators**: `@functools.cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_unpicklable_values(self, state)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| state | None | - | - |


##### handle_incoming_connect_error(self, description)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| description | None | - | - |


##### _disable_broken_incoming_account(self, description)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| description | None | - | - |


##### set_failed_attempts_count(self, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |


##### get_failed_attempts_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### receive(self)

Called by scheduler to receive emails from this EMail account using POP3/IMAP.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_inbound_mails(self) → list[InboundMail]

retrive and return inbound mails.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[InboundMail]`


##### handle_bad_emails(self, uid, raw, reason)

Save the email in Unhandled Email doctype.

The excessive encoding and decoding is done to handle the case where the
email contains invalid characters. This should fail when parsing, not
when storing the email in the database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| uid | None | - | - |
| raw | None | - | - |
| reason | None | - | - |


##### send_auto_reply(self, communication, email)

Send auto reply if set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| communication | None | - | - |
| email | None | - | - |


##### get_unreplied_notification_emails(self)

Return list of emails listed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

Clear communications where email account is linked

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_rename(self, old, new, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | None | - | - |
| new | None | - | - |
| merge | None | False | - |


##### build_email_sync_rule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_automatic_linking_email_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### append_email_to_sent_folder(self, message)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |


##### get_oauth_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### cache_email_account(cache_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cache_name | None | - | - |

**Returns**: (none)



### get_append_to(doctype = None, txt = None, searchfield = None, start = None, page_len = None, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| txt | None | None | - |
| searchfield | None | None | - |
| start | None | None | - |
| page_len | None | None | - |
| filters | None | None | - |

**Returns**: (none)



### notify_unreplied()

Sends email notifications if there are unreplied Communications
and `notify_if_unreplied` is set as true.

**Returns**: (none)



### pull(now = False)

Will be called via scheduler, pull emails from all enabled Email accounts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| now | None | False | - |

**Returns**: (none)



### pull_emails(email_account: str) → None

Pull emails from given email account.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | str | - | - |

**Returns**: `None`



### pull_from_email_account(email_account)

Runs within a worker process

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |

**Returns**: (none)



### get_max_email_uid(email_account)

get maximum uid of emails

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |

**Returns**: (none)



### setup_user_email_inbox(email_account, awaiting_password, email_id, enable_outgoing, used_oauth)

setup email inbox for user

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |
| awaiting_password | None | - | - |
| email_id | None | - | - |
| enable_outgoing | None | - | - |
| used_oauth | None | - | - |

**Returns**: (none)



### remove_user_email_inbox(email_account)

remove user email inbox settings if email account is deleted

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |

**Returns**: (none)



### set_email_password(email_account, password)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |
| password | None | - | - |

**Returns**: (none)



### get_automatic_email_link()

**Returns**: (none)



### on_doctype_update() → None

**Returns**: `None`



### decorator_cache_email_account(func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### add_user_email(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### check_db()

**Returns**: (none)



### wrapper_cache_email_account()

**Returns**: (none)



### process_mail(messages, append_to = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| messages | None | - | - |
| append_to | None | None | - |

**Returns**: (none)


