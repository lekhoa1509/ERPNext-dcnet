# Test Example Extraction Report

**Total Examples**: 40  
**High Value Examples** (confidence > 0.7): 40  
**Average Complexity**: 0.32  

## Examples by Category

- **instantiation**: 15
- **method_call**: 21
- **workflow**: 4

## Examples by Language

- **Python**: 40

## Extracted Examples

### test_webhook_with_array_body

**Category**: workflow  
**Description**: Workflow: Check if array request body are supported.  
**Expected**: self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json=expected_req, match=[json_params_matcher(expected_req)])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
self.responses = responses.RequestsMock()
self.responses.start()
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json={})
webhook_fields = {'webhook_doctype': 'User', 'webhook_docevent': 'after_insert', 'request_url': 'https://httpbin.org/post'}
if frappe.db.exists('Webhook', webhook_fields):
    self.webhook = frappe.get_doc('Webhook', webhook_fields)
else:
    self.webhook = frappe.new_doc('Webhook')
    self.webhook.update(webhook_fields)
self.user = frappe.new_doc('User')
self.user.first_name = frappe.mock('name')
self.user.email = frappe.mock('email')
self.user.save()
self.test_user = frappe.new_doc('User')
self.test_user.email = 'user1@integration.webhooks.test.com'
self.test_user.first_name = 'user1'
self.test_user.send_welcome_email = False
frappe.db.commit()

'Check if array request body are supported.'
wh_config = {'doctype': 'Webhook', 'webhook_doctype': 'Note', 'webhook_docevent': 'on_change', 'enabled': 1, 'request_url': 'https://httpbin.org/post', 'request_method': 'POST', 'request_structure': 'JSON', 'webhook_json': '[\r\n{% for n in range(3) %}\r\n    {\r\n        "title": "{{ doc.title }}"    }\r\n    {%- if not loop.last -%}\r\n        , \r\n    {%endif%}\r\n{%endfor%}\r\n]', 'meets_condition': 'Yes', 'webhook_headers': [{'key': 'Content-Type', 'value': 'application/json'}]}
doc = frappe.new_doc('Note')
doc.title = 'Test Webhook Note'
final_title = frappe.generate_hash()
expected_req = [{'title': final_title} for _ in range(3)]
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json=expected_req, match=[json_params_matcher(expected_req)])
with get_test_webhook(wh_config):
    doc.insert()
    doc.reload()
    doc.save()
    doc = frappe.get_doc(doc.doctype, doc.name)
    doc.title = final_title
    doc.save()
    flush_webhook_execution_queue()
    log = frappe.get_last_doc('Webhook Request Log')
    self.assertEqual(len(json.loads(log.response)), 3)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:226*

### test_webhook_with_array_body

**Category**: workflow  
**Description**: Workflow: Check if array request body are supported.  
**Expected**: self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json=expected_req, match=[json_params_matcher(expected_req)])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Check if array request body are supported.'
wh_config = {'doctype': 'Webhook', 'webhook_doctype': 'Note', 'webhook_docevent': 'on_change', 'enabled': 1, 'request_url': 'https://httpbin.org/post', 'request_method': 'POST', 'request_structure': 'JSON', 'webhook_json': '[\r\n{% for n in range(3) %}\r\n    {\r\n        "title": "{{ doc.title }}"    }\r\n    {%- if not loop.last -%}\r\n        , \r\n    {%endif%}\r\n{%endfor%}\r\n]', 'meets_condition': 'Yes', 'webhook_headers': [{'key': 'Content-Type', 'value': 'application/json'}]}
doc = frappe.new_doc('Note')
doc.title = 'Test Webhook Note'
final_title = frappe.generate_hash()
expected_req = [{'title': final_title} for _ in range(3)]
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json=expected_req, match=[json_params_matcher(expected_req)])
with get_test_webhook(wh_config):
    doc.insert()
    doc.reload()
    doc.save()
    doc = frappe.get_doc(doc.doctype, doc.name)
    doc.title = final_title
    doc.save()
    flush_webhook_execution_queue()
    log = frappe.get_last_doc('Webhook Request Log')
    self.assertEqual(len(json.loads(log.response)), 3)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:226*

### test_get_ldap_client_settings

**Category**: workflow  
**Description**: Workflow: test get ldap client settings  
**Expected**: self.assertFalse(result['enabled'])  
**Confidence**: 0.90  
**Tags**: mock, unittest, workflow, integration  

```python
result = self.test_class.get_ldap_client_settings()
self.assertIsInstance(result, dict)
self.assertTrue(result['enabled'] == self.doc['enabled'])
localdoc = self.doc.copy()
localdoc['enabled'] = False
frappe.get_doc(localdoc).save()
result = self.test_class.get_ldap_client_settings()
self.assertFalse(result['enabled'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:316*

### test_sync_roles

**Category**: workflow  
**Description**: Workflow: test sync roles  
**Confidence**: 0.90  
**Tags**: mock, unittest, workflow, integration  

```python
if self.TEST_LDAP_SERVER.lower() == 'openldap':
    test_user_data = {'posix.user1': ['Users', 'Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user'], 'posix.user2': ['Users', 'Group3', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user']}
elif self.TEST_LDAP_SERVER.lower() == 'active directory':
    test_user_data = {'posix.user1': ['Domain Users', 'Domain Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user'], 'posix.user2': ['Domain Users', 'Enterprise Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user']}
role_to_group_map = {self.doc['ldap_groups'][0]['erpnext_role']: self.doc['ldap_groups'][0]['ldap_group'], self.doc['ldap_groups'][1]['erpnext_role']: self.doc['ldap_groups'][1]['ldap_group'], self.doc['ldap_groups'][2]['erpnext_role']: self.doc['ldap_groups'][2]['ldap_group'], 'Newsletter Manager': 'default_role', 'All': 'frappe_default_all', 'Guest': 'frappe_default_guest', 'Desk User': 'frappe_default_desk_user'}
frappe.get_doc('User', 'posix.user1@unit.testing').delete()
user = frappe.get_doc(self.user1doc)
user.insert(ignore_permissions=True)
for test_user in test_user_data:
    test_user_doc = frappe.get_doc('User', f'{test_user}@unit.testing')
    test_user_roles = frappe.get_roles(f'{test_user}@unit.testing')
    self.assertTrue(len(test_user_roles) == 2, 'User should only be a part of the All and Guest roles')
    self.test_class.sync_roles(test_user_doc, test_user_data[test_user])
    frappe.get_doc('User', f'{test_user}@unit.testing')
    updated_user_roles = frappe.get_roles(f'{test_user}@unit.testing')
    self.assertTrue(len(updated_user_roles) == len(test_user_data[test_user]), f'syncing of the user roles failed. {len(updated_user_roles)} != {len(test_user_data[test_user])} for user {test_user}')
    for user_role in updated_user_roles:
        self.assertTrue(role_to_group_map[user_role] in test_user_data[test_user], f'during sync_roles(), the user was given role {user_role} which should not have occurred')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:365*

### test_webhook_trigger_with_enabled_webhooks

**Category**: method_call  
**Description**: Test webhook trigger for enabled webhooks  
**Expected**: self.assertEqual(len(webhooks.get('User')), 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.responses = responses.RequestsMock()
self.responses.start()
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json={})
webhook_fields = {'webhook_doctype': 'User', 'webhook_docevent': 'after_insert', 'request_url': 'https://httpbin.org/post'}
if frappe.db.exists('Webhook', webhook_fields):
    self.webhook = frappe.get_doc('Webhook', webhook_fields)
else:
    self.webhook = frappe.new_doc('Webhook')
    self.webhook.update(webhook_fields)
self.user = frappe.new_doc('User')
self.user.first_name = frappe.mock('name')
self.user.email = frappe.mock('email')
self.user.save()
self.test_user = frappe.new_doc('User')
self.test_user.email = 'user1@integration.webhooks.test.com'
self.test_user.first_name = 'user1'
self.test_user.send_welcome_email = False
frappe.db.commit()

self.assertTrue('User' in webhooks)
self.assertEqual(len(webhooks.get('User')), 1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:135*

### test_webhook_trigger_with_enabled_webhooks

**Category**: method_call  
**Description**: Test webhook trigger for enabled webhooks  
**Expected**: self.assertEqual(len(frappe.local._webhook_queue), 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.responses = responses.RequestsMock()
self.responses.start()
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json={})
webhook_fields = {'webhook_doctype': 'User', 'webhook_docevent': 'after_insert', 'request_url': 'https://httpbin.org/post'}
if frappe.db.exists('Webhook', webhook_fields):
    self.webhook = frappe.get_doc('Webhook', webhook_fields)
else:
    self.webhook = frappe.new_doc('Webhook')
    self.webhook.update(webhook_fields)
self.user = frappe.new_doc('User')
self.user.first_name = frappe.mock('name')
self.user.email = frappe.mock('email')
self.user.save()
self.test_user = frappe.new_doc('User')
self.test_user.email = 'user1@integration.webhooks.test.com'
self.test_user.first_name = 'user1'
self.test_user.send_welcome_email = False
frappe.db.commit()

self.assertEqual(len(webhooks.get('User')), 1)
self.assertEqual(len(frappe.local._webhook_queue), 1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:136*

### test_webhook_trigger_with_enabled_webhooks

**Category**: method_call  
**Description**: Test webhook trigger for enabled webhooks  
**Expected**: self.assertEqual(execution.doc.name, self.test_user.name)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.responses = responses.RequestsMock()
self.responses.start()
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json={})
webhook_fields = {'webhook_doctype': 'User', 'webhook_docevent': 'after_insert', 'request_url': 'https://httpbin.org/post'}
if frappe.db.exists('Webhook', webhook_fields):
    self.webhook = frappe.get_doc('Webhook', webhook_fields)
else:
    self.webhook = frappe.new_doc('Webhook')
    self.webhook.update(webhook_fields)
self.user = frappe.new_doc('User')
self.user.first_name = frappe.mock('name')
self.user.email = frappe.mock('email')
self.user.save()
self.test_user = frappe.new_doc('User')
self.test_user.email = 'user1@integration.webhooks.test.com'
self.test_user.first_name = 'user1'
self.test_user.send_welcome_email = False
frappe.db.commit()

self.assertEqual(execution.webhook.name, self.sample_webhooks[0].name)
self.assertEqual(execution.doc.name, self.test_user.name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:141*

### test_validate_request_body_form

**Category**: method_call  
**Description**: Test validation of Form URL-Encoded request body  
**Expected**: self.assertEqual(self.webhook.webhook_json, None)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.responses = responses.RequestsMock()
self.responses.start()
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json={})
webhook_fields = {'webhook_doctype': 'User', 'webhook_docevent': 'after_insert', 'request_url': 'https://httpbin.org/post'}
if frappe.db.exists('Webhook', webhook_fields):
    self.webhook = frappe.get_doc('Webhook', webhook_fields)
else:
    self.webhook = frappe.new_doc('Webhook')
    self.webhook.update(webhook_fields)
self.user = frappe.new_doc('User')
self.user.first_name = frappe.mock('name')
self.user.email = frappe.mock('email')
self.user.save()
self.test_user = frappe.new_doc('User')
self.test_user.email = 'user1@integration.webhooks.test.com'
self.test_user.first_name = 'user1'
self.test_user.send_welcome_email = False
frappe.db.commit()

self.webhook.save()
self.assertEqual(self.webhook.webhook_json, None)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:183*

### test_validate_request_body_json

**Category**: method_call  
**Description**: Test validation of JSON request body  
**Expected**: self.assertEqual(self.webhook.webhook_data, [])  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.responses = responses.RequestsMock()
self.responses.start()
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json={})
webhook_fields = {'webhook_doctype': 'User', 'webhook_docevent': 'after_insert', 'request_url': 'https://httpbin.org/post'}
if frappe.db.exists('Webhook', webhook_fields):
    self.webhook = frappe.get_doc('Webhook', webhook_fields)
else:
    self.webhook = frappe.new_doc('Webhook')
    self.webhook.update(webhook_fields)
self.user = frappe.new_doc('User')
self.user.first_name = frappe.mock('name')
self.user.email = frappe.mock('email')
self.user.save()
self.test_user = frappe.new_doc('User')
self.test_user.email = 'user1@integration.webhooks.test.com'
self.test_user.first_name = 'user1'
self.test_user.send_welcome_email = False
frappe.db.commit()

self.webhook.save()
self.assertEqual(self.webhook.webhook_data, [])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:198*

### test_webhook_req_log_creation

**Category**: method_call  
**Description**: test webhook req log creation  
**Expected**: self.assertTrue(frappe.get_all('Webhook Request Log', pluck='name'))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.responses = responses.RequestsMock()
self.responses.start()
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json={})
webhook_fields = {'webhook_doctype': 'User', 'webhook_docevent': 'after_insert', 'request_url': 'https://httpbin.org/post'}
if frappe.db.exists('Webhook', webhook_fields):
    self.webhook = frappe.get_doc('Webhook', webhook_fields)
else:
    self.webhook = frappe.new_doc('Webhook')
    self.webhook.update(webhook_fields)
self.user = frappe.new_doc('User')
self.user.first_name = frappe.mock('name')
self.user.email = frappe.mock('email')
self.user.save()
self.test_user = frappe.new_doc('User')
self.test_user.email = 'user1@integration.webhooks.test.com'
self.test_user.first_name = 'user1'
self.test_user.send_welcome_email = False
frappe.db.commit()

enqueue_webhook(user, webhook)
self.assertTrue(frappe.get_all('Webhook Request Log', pluck='name'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:221*

### test_webhook_trigger_with_enabled_webhooks

**Category**: method_call  
**Description**: Test webhook trigger for enabled webhooks  
**Expected**: self.assertEqual(len(webhooks.get('User')), 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertTrue('User' in webhooks)
self.assertEqual(len(webhooks.get('User')), 1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:135*

### test_webhook_trigger_with_enabled_webhooks

**Category**: method_call  
**Description**: Test webhook trigger for enabled webhooks  
**Expected**: self.assertEqual(len(frappe.local._webhook_queue), 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(len(webhooks.get('User')), 1)
self.assertEqual(len(frappe.local._webhook_queue), 1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/webhook/test_webhook.py:136*

### test_get_ldap_client_settings

**Category**: method_call  
**Description**: test get ldap client settings  
**Expected**: self.assertTrue(result['enabled'] == self.doc['enabled'])  
**Confidence**: 0.85  
**Tags**: mock, unittest  

```python
self.assertIsInstance(result, dict)
self.assertTrue(result['enabled'] == self.doc['enabled'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:319*

### test_update_user_fields

**Category**: method_call  
**Description**: test update user fields  
**Expected**: self.assertTrue(updated_user.last_name == test_user_data['last_name'])  
**Confidence**: 0.85  
**Tags**: mock, unittest  

```python
self.assertTrue(updated_user.middle_name == test_user_data['middle_name'])
self.assertTrue(updated_user.last_name == test_user_data['last_name'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:344*

### test_update_user_fields

**Category**: method_call  
**Description**: test update user fields  
**Expected**: self.assertTrue(updated_user.phone == test_user_data['phone'])  
**Confidence**: 0.85  
**Tags**: mock, unittest  

```python
self.assertTrue(updated_user.last_name == test_user_data['last_name'])
self.assertTrue(updated_user.phone == test_user_data['phone'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:345*

### test_update_user_fields

**Category**: method_call  
**Description**: test update user fields  
**Expected**: self.assertTrue(updated_user.mobile_no == test_user_data['mobile_no'])  
**Confidence**: 0.85  
**Tags**: mock, unittest  

```python
self.assertTrue(updated_user.phone == test_user_data['phone'])
self.assertTrue(updated_user.mobile_no == test_user_data['mobile_no'])
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:346*

### test_update_user_fields

**Category**: method_call  
**Description**: test update user fields  
**Expected**: self.assertEqual(updated_user.user_type, self.test_class.default_user_type)  
**Confidence**: 0.85  
**Tags**: mock, unittest  

```python
self.assertTrue(updated_user.mobile_no == test_user_data['mobile_no'])
self.assertEqual(updated_user.user_type, self.test_class.default_user_type)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:347*

### test_update_user_fields

**Category**: method_call  
**Description**: test update user fields  
**Expected**: self.assertIn(self.test_class.default_role, frappe.get_roles(updated_user.name))  
**Confidence**: 0.85  
**Tags**: mock, unittest  

```python
self.assertEqual(updated_user.user_type, self.test_class.default_user_type)
self.assertIn(self.test_class.default_role, frappe.get_roles(updated_user.name))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:349*

### test_convert_ldap_entry_to_dict

**Category**: method_call  
**Description**: test convert ldap entry to dict  
**Expected**: self.assertTrue(len(method_return) == 6)  
**Confidence**: 0.85  
**Tags**: mock, unittest  

```python
self.assertTrue(isinstance(method_return, dict))
self.assertTrue(len(method_return) == 6)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:603*

### test_picker_enabled

**Category**: method_call  
**Description**: If picker is enabled, get_file_picker_settings should return the credentials.  
**Expected**: self.assertEqual('test_client_id', settings.get('clientId', ''))  
**Confidence**: 0.85  

```python
# Setup
settings = frappe.get_single('Google Settings')
settings.client_id = 'test_client_id'
settings.app_id = 'test_app_id'
settings.api_key = 'test_api_key'
settings.save()

self.assertEqual(True, settings.get('enabled', False))
self.assertEqual('test_client_id', settings.get('clientId', ''))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/google_settings/test_google_settings.py:40*

### test_picker_enabled

**Category**: method_call  
**Description**: If picker is enabled, get_file_picker_settings should return the credentials.  
**Expected**: self.assertEqual('test_app_id', settings.get('appId', ''))  
**Confidence**: 0.85  

```python
# Setup
settings = frappe.get_single('Google Settings')
settings.client_id = 'test_client_id'
settings.app_id = 'test_app_id'
settings.api_key = 'test_api_key'
settings.save()

self.assertEqual('test_client_id', settings.get('clientId', ''))
self.assertEqual('test_app_id', settings.get('appId', ''))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/google_settings/test_google_settings.py:41*

### test_picker_enabled

**Category**: method_call  
**Description**: If picker is enabled, get_file_picker_settings should return the credentials.  
**Expected**: self.assertEqual('test_client_id', settings.get('clientId', ''))  
**Confidence**: 0.85  

```python
self.assertEqual(True, settings.get('enabled', False))
self.assertEqual('test_client_id', settings.get('clientId', ''))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/google_settings/test_google_settings.py:40*

### test_picker_enabled

**Category**: method_call  
**Description**: If picker is enabled, get_file_picker_settings should return the credentials.  
**Expected**: self.assertEqual('test_app_id', settings.get('appId', ''))  
**Confidence**: 0.85  

```python
self.assertEqual('test_client_id', settings.get('clientId', ''))
self.assertEqual('test_app_id', settings.get('appId', ''))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/google_settings/test_google_settings.py:41*

### test_adding_frappe_social_login_provider

**Category**: method_call  
**Description**: test adding frappe social login provider  
**Expected**: self.assertRaises(BaseUrlNotSetError, social_login_key.insert)  
**Confidence**: 0.85  

```python
# Setup
frappe.set_user('Administrator')
frappe.delete_doc('User', TEST_GITHUB_USER, force=True)
super().setUp()
frappe.set_user('Guest')

social_login_key.get_social_login_provider(provider_name, initialize=True)
self.assertRaises(BaseUrlNotSetError, social_login_key.insert)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/social_login_key/test_social_login_key.py:28*

### test_adding_frappe_social_login_provider

**Category**: method_call  
**Description**: test adding frappe social login provider  
**Expected**: self.assertRaises(BaseUrlNotSetError, social_login_key.insert)  
**Confidence**: 0.85  

```python
social_login_key.get_social_login_provider(provider_name, initialize=True)
self.assertRaises(BaseUrlNotSetError, social_login_key.insert)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/social_login_key/test_social_login_key.py:28*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate initiate_web_application_flow: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(auth_response.status_code, 200)  
**Confidence**: 0.80  

```python
# Setup
'Set up a Connected App that connects to our own oAuth provider.\n\n\t\tFrappe comes with it\'s own oAuth2 provider that we can test against. The\n\t\tclient credentials can be obtained from an "OAuth Client". All depends\n\t\ton "Social Login Key" so we create one as well.\n\n\t\tThe redirect URIs from "Connected App" and "OAuth Client" have to match.\n\t\tFrappe\'s "Authorization URL" and "Access Token URL" (actually they\'re\n\t\tjust endpoints) are stored in "Social Login Key" so we get them from\n\t\tthere.\n\t\t'
self.user_name = 'test-connected-app@example.com'
self.user_password = 'Eastern_43A1W'
self.user = get_user(self.user_name, self.user_password)
self.connected_app = get_connected_app()
self.oauth_client = get_oauth_client()
social_login_key = create_or_update_social_login_key()
self.base_url = social_login_key.get('base_url')
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()
redirect_uri = self.connected_app.get('redirect_uri')
self.oauth_client.update({'redirect_uris': redirect_uri, 'default_redirect_uri': redirect_uri})
self.oauth_client.save()
self.connected_app.update({'authorization_uri': urljoin(self.base_url, social_login_key.get('authorize_url')), 'client_id': self.oauth_client.get('client_id'), 'client_secret': self.oauth_client.get('client_secret'), 'token_uri': urljoin(self.base_url, social_login_key.get('access_token_url'))})
self.connected_app.save()
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()

authorization_url = self.connected_app.initiate_web_application_flow(user=self.user_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:109*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(auth_response.status_code, 200)  
**Confidence**: 0.80  

```python
# Setup
'Set up a Connected App that connects to our own oAuth provider.\n\n\t\tFrappe comes with it\'s own oAuth2 provider that we can test against. The\n\t\tclient credentials can be obtained from an "OAuth Client". All depends\n\t\ton "Social Login Key" so we create one as well.\n\n\t\tThe redirect URIs from "Connected App" and "OAuth Client" have to match.\n\t\tFrappe\'s "Authorization URL" and "Access Token URL" (actually they\'re\n\t\tjust endpoints) are stored in "Social Login Key" so we get them from\n\t\tthere.\n\t\t'
self.user_name = 'test-connected-app@example.com'
self.user_password = 'Eastern_43A1W'
self.user = get_user(self.user_name, self.user_password)
self.connected_app = get_connected_app()
self.oauth_client = get_oauth_client()
social_login_key = create_or_update_social_login_key()
self.base_url = social_login_key.get('base_url')
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()
redirect_uri = self.connected_app.get('redirect_uri')
self.oauth_client.update({'redirect_uris': redirect_uri, 'default_redirect_uri': redirect_uri})
self.oauth_client.save()
self.connected_app.update({'authorization_uri': urljoin(self.base_url, social_login_key.get('authorize_url')), 'client_id': self.oauth_client.get('client_id'), 'client_secret': self.oauth_client.get('client_secret'), 'token_uri': urljoin(self.base_url, social_login_key.get('access_token_url'))})
self.connected_app.save()
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()

auth_response = session.get(authorization_url)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:111*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(callback_response.status_code, 200)  
**Confidence**: 0.80  

```python
# Setup
'Set up a Connected App that connects to our own oAuth provider.\n\n\t\tFrappe comes with it\'s own oAuth2 provider that we can test against. The\n\t\tclient credentials can be obtained from an "OAuth Client". All depends\n\t\ton "Social Login Key" so we create one as well.\n\n\t\tThe redirect URIs from "Connected App" and "OAuth Client" have to match.\n\t\tFrappe\'s "Authorization URL" and "Access Token URL" (actually they\'re\n\t\tjust endpoints) are stored in "Social Login Key" so we get them from\n\t\tthere.\n\t\t'
self.user_name = 'test-connected-app@example.com'
self.user_password = 'Eastern_43A1W'
self.user = get_user(self.user_name, self.user_password)
self.connected_app = get_connected_app()
self.oauth_client = get_oauth_client()
social_login_key = create_or_update_social_login_key()
self.base_url = social_login_key.get('base_url')
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()
redirect_uri = self.connected_app.get('redirect_uri')
self.oauth_client.update({'redirect_uris': redirect_uri, 'default_redirect_uri': redirect_uri})
self.oauth_client.save()
self.connected_app.update({'authorization_uri': urljoin(self.base_url, social_login_key.get('authorize_url')), 'client_id': self.oauth_client.get('client_id'), 'client_secret': self.oauth_client.get('client_secret'), 'token_uri': urljoin(self.base_url, social_login_key.get('access_token_url'))})
self.connected_app.save()
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()

callback_response = session.get(auth_response.url)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:114*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get_token_cache: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertNotEqual(token, None)  
**Confidence**: 0.80  

```python
# Setup
'Set up a Connected App that connects to our own oAuth provider.\n\n\t\tFrappe comes with it\'s own oAuth2 provider that we can test against. The\n\t\tclient credentials can be obtained from an "OAuth Client". All depends\n\t\ton "Social Login Key" so we create one as well.\n\n\t\tThe redirect URIs from "Connected App" and "OAuth Client" have to match.\n\t\tFrappe\'s "Authorization URL" and "Access Token URL" (actually they\'re\n\t\tjust endpoints) are stored in "Social Login Key" so we get them from\n\t\tthere.\n\t\t'
self.user_name = 'test-connected-app@example.com'
self.user_password = 'Eastern_43A1W'
self.user = get_user(self.user_name, self.user_password)
self.connected_app = get_connected_app()
self.oauth_client = get_oauth_client()
social_login_key = create_or_update_social_login_key()
self.base_url = social_login_key.get('base_url')
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()
redirect_uri = self.connected_app.get('redirect_uri')
self.oauth_client.update({'redirect_uris': redirect_uri, 'default_redirect_uri': redirect_uri})
self.oauth_client.save()
self.connected_app.update({'authorization_uri': urljoin(self.base_url, social_login_key.get('authorize_url')), 'client_id': self.oauth_client.get('client_id'), 'client_secret': self.oauth_client.get('client_secret'), 'token_uri': urljoin(self.base_url, social_login_key.get('access_token_url'))})
self.connected_app.save()
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()

self.token_cache = self.connected_app.get_token_cache(self.user_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:117*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get_oauth2_session: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(resp.json().get('message'), self.user_name)  
**Confidence**: 0.80  

```python
# Setup
'Set up a Connected App that connects to our own oAuth provider.\n\n\t\tFrappe comes with it\'s own oAuth2 provider that we can test against. The\n\t\tclient credentials can be obtained from an "OAuth Client". All depends\n\t\ton "Social Login Key" so we create one as well.\n\n\t\tThe redirect URIs from "Connected App" and "OAuth Client" have to match.\n\t\tFrappe\'s "Authorization URL" and "Access Token URL" (actually they\'re\n\t\tjust endpoints) are stored in "Social Login Key" so we get them from\n\t\tthere.\n\t\t'
self.user_name = 'test-connected-app@example.com'
self.user_password = 'Eastern_43A1W'
self.user = get_user(self.user_name, self.user_password)
self.connected_app = get_connected_app()
self.oauth_client = get_oauth_client()
social_login_key = create_or_update_social_login_key()
self.base_url = social_login_key.get('base_url')
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()
redirect_uri = self.connected_app.get('redirect_uri')
self.oauth_client.update({'redirect_uris': redirect_uri, 'default_redirect_uri': redirect_uri})
self.oauth_client.save()
self.connected_app.update({'authorization_uri': urljoin(self.base_url, social_login_key.get('authorize_url')), 'client_id': self.oauth_client.get('client_id'), 'client_secret': self.oauth_client.get('client_secret'), 'token_uri': urljoin(self.base_url, social_login_key.get('access_token_url'))})
self.connected_app.save()
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()

oauth2_session = self.connected_app.get_oauth2_session(self.user_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:121*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(resp.json().get('message'), self.user_name)  
**Confidence**: 0.80  

```python
# Setup
'Set up a Connected App that connects to our own oAuth provider.\n\n\t\tFrappe comes with it\'s own oAuth2 provider that we can test against. The\n\t\tclient credentials can be obtained from an "OAuth Client". All depends\n\t\ton "Social Login Key" so we create one as well.\n\n\t\tThe redirect URIs from "Connected App" and "OAuth Client" have to match.\n\t\tFrappe\'s "Authorization URL" and "Access Token URL" (actually they\'re\n\t\tjust endpoints) are stored in "Social Login Key" so we get them from\n\t\tthere.\n\t\t'
self.user_name = 'test-connected-app@example.com'
self.user_password = 'Eastern_43A1W'
self.user = get_user(self.user_name, self.user_password)
self.connected_app = get_connected_app()
self.oauth_client = get_oauth_client()
social_login_key = create_or_update_social_login_key()
self.base_url = social_login_key.get('base_url')
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()
redirect_uri = self.connected_app.get('redirect_uri')
self.oauth_client.update({'redirect_uris': redirect_uri, 'default_redirect_uri': redirect_uri})
self.oauth_client.save()
self.connected_app.update({'authorization_uri': urljoin(self.base_url, social_login_key.get('authorize_url')), 'client_id': self.oauth_client.get('client_id'), 'client_secret': self.oauth_client.get('client_secret'), 'token_uri': urljoin(self.base_url, social_login_key.get('access_token_url'))})
self.connected_app.save()
frappe.db.commit()
self.connected_app.reload()
self.oauth_client.reload()

resp = oauth2_session.get(urljoin(self.base_url, '/api/method/frappe.auth.get_logged_user'))
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:122*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate initiate_web_application_flow: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(auth_response.status_code, 200)  
**Confidence**: 0.80  

```python
authorization_url = self.connected_app.initiate_web_application_flow(user=self.user_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:109*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(auth_response.status_code, 200)  
**Confidence**: 0.80  

```python
auth_response = session.get(authorization_url)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:111*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertEqual(callback_response.status_code, 200)  
**Confidence**: 0.80  

```python
callback_response = session.get(auth_response.url)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:114*

### test_web_application_flow

**Category**: instantiation  
**Description**: Instantiate get_token_cache: Simulate a logged in user who opens the authorization URL.  
**Expected**: self.assertNotEqual(token, None)  
**Confidence**: 0.80  

```python
self.token_cache = self.connected_app.get_token_cache(self.user_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/connected_app/test_connected_app.py:117*

### test_connect_to_ldap

**Category**: instantiation  
**Description**: Instantiate LDAPSettings: test connect to ldap  
**Confidence**: 0.80  
**Tags**: mock, unittest  

```python
self.test_class = LDAPSettings(self.doc)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/ldap_settings/test_ldap_settings.py:235*

### test_adding_frappe_social_login_provider

**Category**: instantiation  
**Description**: Instantiate make_social_login_key: test adding frappe social login provider  
**Expected**: self.assertRaises(BaseUrlNotSetError, social_login_key.insert)  
**Confidence**: 0.80  

```python
# Setup
frappe.set_user('Administrator')
frappe.delete_doc('User', TEST_GITHUB_USER, force=True)
super().setUp()
frappe.set_user('Guest')

social_login_key = make_social_login_key(social_login_provider=provider_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/social_login_key/test_social_login_key.py:27*

### test_normal_signup_and_github_login

**Category**: instantiation  
**Description**: Instantiate new_doc: test normal signup and github login  
**Confidence**: 0.80  
**Tags**: mock  

```python
# Setup
frappe.set_user('Administrator')
frappe.delete_doc('User', TEST_GITHUB_USER, force=True)
super().setUp()
frappe.set_user('Guest')

user = frappe.new_doc('User', email=TEST_GITHUB_USER, first_name='GitHub Login')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/social_login_key/test_social_login_key.py:53*

### test_adding_frappe_social_login_provider

**Category**: instantiation  
**Description**: Instantiate make_social_login_key: test adding frappe social login provider  
**Expected**: self.assertRaises(BaseUrlNotSetError, social_login_key.insert)  
**Confidence**: 0.80  

```python
social_login_key = make_social_login_key(social_login_provider=provider_name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/social_login_key/test_social_login_key.py:27*

### test_normal_signup_and_github_login

**Category**: instantiation  
**Description**: Instantiate new_doc: test normal signup and github login  
**Confidence**: 0.80  
**Tags**: mock  

```python
user = frappe.new_doc('User', email=TEST_GITHUB_USER, first_name='GitHub Login')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe/integrations/doctype/social_login_key/test_social_login_key.py:53*

