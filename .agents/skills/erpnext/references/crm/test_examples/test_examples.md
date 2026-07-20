# Test Example Extraction Report

**Total Examples**: 44  
**High Value Examples** (confidence > 0.7): 44  
**Average Complexity**: 0.49  

## Examples by Category

- **instantiation**: 6
- **method_call**: 24
- **workflow**: 14

## Examples by Language

- **Python**: 44

## Extracted Examples

### test_carry_forward_of_email_and_comments

**Category**: workflow  
**Description**: Workflow: test carry forward of email and comments  
**Expected**: self.assertEqual(opportunity_communication_count, 2)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_single_value('CRM Settings', 'carry_forward_communication_and_comments', 1)
lead_doc = make_lead()
lead_doc.add_comment('Comment', text='Test Comment 1')
lead_doc.add_comment('Comment', text='Test Comment 2')
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
opp_doc = make_opportunity(opportunity_from='Lead', lead=lead_doc.name)
opportunity_comment_count = frappe.db.count('Comment', {'reference_doctype': opp_doc.doctype, 'reference_name': opp_doc.name})
opportunity_communication_count = len(get_linked_communication_list(opp_doc.doctype, opp_doc.name))
self.assertEqual(opportunity_comment_count, 2)
self.assertEqual(opportunity_communication_count, 2)
opp_doc.add_comment('Comment', text='Test Comment 3')
opp_doc.add_comment('Comment', text='Test Comment 4')
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:82*

### test_carry_forward_of_email_and_comments

**Category**: workflow  
**Description**: Workflow: test carry forward of email and comments  
**Expected**: self.assertEqual(opportunity_communication_count, 2)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_single_value('CRM Settings', 'carry_forward_communication_and_comments', 1)
lead_doc = make_lead()
lead_doc.add_comment('Comment', text='Test Comment 1')
lead_doc.add_comment('Comment', text='Test Comment 2')
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
create_communication(lead_doc.doctype, lead_doc.name, lead_doc.email_id)
opp_doc = make_opportunity(opportunity_from='Lead', lead=lead_doc.name)
opportunity_comment_count = frappe.db.count('Comment', {'reference_doctype': opp_doc.doctype, 'reference_name': opp_doc.name})
opportunity_communication_count = len(get_linked_communication_list(opp_doc.doctype, opp_doc.name))
self.assertEqual(opportunity_comment_count, 2)
self.assertEqual(opportunity_communication_count, 2)
opp_doc.add_comment('Comment', text='Test Comment 3')
opp_doc.add_comment('Comment', text='Test Comment 4')
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
create_communication(opp_doc.doctype, opp_doc.name, opp_doc.contact_email)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:82*

### test_add_lead_to_prospect_and_address_linking

**Category**: workflow  
**Description**: Workflow: test add lead to prospect and address linking  
**Expected**: self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
lead_doc = make_lead()
address_doc = make_address(address_title=lead_doc.name)
address_doc.append('links', {'link_doctype': lead_doc.doctype, 'link_name': lead_doc.name})
address_doc.save()
prospect_doc = make_prospect()
add_lead_to_prospect(lead_doc.name, prospect_doc.name)
prospect_doc.reload()
lead_exists_in_prosoect = False
for rec in prospect_doc.get('leads'):
    if rec.lead == lead_doc.name:
        lead_exists_in_prosoect = True
self.assertEqual(lead_exists_in_prosoect, True)
address_doc.reload()
self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:14*

### test_add_lead_to_prospect_and_address_linking

**Category**: workflow  
**Description**: Workflow: test add lead to prospect and address linking  
**Expected**: self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
lead_doc = make_lead()
address_doc = make_address(address_title=lead_doc.name)
address_doc.append('links', {'link_doctype': lead_doc.doctype, 'link_name': lead_doc.name})
address_doc.save()
prospect_doc = make_prospect()
add_lead_to_prospect(lead_doc.name, prospect_doc.name)
prospect_doc.reload()
lead_exists_in_prosoect = False
for rec in prospect_doc.get('leads'):
    if rec.lead == lead_doc.name:
        lead_exists_in_prosoect = True
self.assertEqual(lead_exists_in_prosoect, True)
address_doc.reload()
self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:14*

### test_sales_pipeline_analytics

**Category**: workflow  
**Description**: Workflow: test sales pipeline analytics  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
# Setup
create_company()
create_customer()
create_opportunity()

self.from_date = '2021-01-01'
self.to_date = '2021-12-31'
self.check_for_monthly_and_number()
self.check_for_monthly_and_amount()
self.check_for_quarterly_and_number()
self.check_for_quarterly_and_amount()
self.check_for_all_filters()
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/report/sales_pipeline_analytics/test_sales_pipeline_analytics.py:15*

### test_sales_pipeline_analytics

**Category**: workflow  
**Description**: Workflow: test sales pipeline analytics  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
self.from_date = '2021-01-01'
self.to_date = '2021-12-31'
self.check_for_monthly_and_number()
self.check_for_monthly_and_amount()
self.check_for_quarterly_and_number()
self.check_for_quarterly_and_amount()
self.check_for_all_filters()
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/report/sales_pipeline_analytics/test_sales_pipeline_analytics.py:15*

### test_make_customer

**Category**: workflow  
**Description**: Workflow: test make customer  
**Expected**: self.assertEqual(customer.lead_name, self.leads[0].name)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
from erpnext.crm.doctype.lead.lead import make_customer
frappe.delete_doc_if_exists('Customer', '_Test Lead')
customer = make_customer(self.leads[0].name)
self.assertEqual(customer.doctype, 'Customer')
self.assertEqual(customer.lead_name, self.leads[0].name)
customer.company = '_Test Company'
customer.customer_group = '_Test Customer Group'
customer.insert()
contact = frappe.db.get_value('Dynamic Link', {'parenttype': 'Contact', 'link_doctype': 'Lead', 'link_name': customer.lead_name}, 'parent')
if contact:
    contact_doc = frappe.get_doc('Contact', contact)
    self.assertEqual(contact_doc.has_link(customer.doctype, customer.name), True)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:20*

### test_make_customer

**Category**: workflow  
**Description**: Workflow: test make customer  
**Expected**: self.assertEqual(customer.lead_name, self.leads[0].name)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
from erpnext.crm.doctype.lead.lead import make_customer
frappe.delete_doc_if_exists('Customer', '_Test Lead')
customer = make_customer(self.leads[0].name)
self.assertEqual(customer.doctype, 'Customer')
self.assertEqual(customer.lead_name, self.leads[0].name)
customer.company = '_Test Company'
customer.customer_group = '_Test Customer Group'
customer.insert()
contact = frappe.db.get_value('Dynamic Link', {'parenttype': 'Contact', 'link_doctype': 'Lead', 'link_name': customer.lead_name}, 'parent')
if contact:
    contact_doc = frappe.get_doc('Contact', contact)
    self.assertEqual(contact_doc.has_link(customer.doctype, customer.name), True)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:20*

### test_fulfilled_contract_status

**Category**: workflow  
**Description**: Workflow: test fulfilled contract status  
**Expected**: self.assertEqual(self.contract_doc.fulfilment_status, 'Fulfilled')  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabContract`')
self.contract_doc = get_contract()

self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'
self.contract_doc.requires_fulfilment = 1
fulfilment_terms = []
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
for term in self.contract_doc.fulfilment_terms:
    term.fulfilled = 1
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Fulfilled')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:61*

### test_partially_fulfilled_contract_status

**Category**: workflow  
**Description**: Workflow: test partially fulfilled contract status  
**Expected**: self.assertEqual(self.contract_doc.fulfilment_status, 'Partially Fulfilled')  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabContract`')
self.contract_doc = get_contract()

self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'
self.contract_doc.requires_fulfilment = 1
self.contract_doc.save()
fulfilment_terms = []
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
fulfilment_terms.append({'requirement': 'This is another test requirement.', 'fulfilled': 0})
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
self.contract_doc.fulfilment_terms[0].fulfilled = 1
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Partially Fulfilled')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:77*

### test_lapsed_contract_status

**Category**: workflow  
**Description**: Workflow: test lapsed contract status  
**Expected**: self.assertEqual(self.contract_doc.fulfilment_status, 'Lapsed')  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabContract`')
self.contract_doc = get_contract()

self.contract_doc.contract_term = '_Test Customer Contract with Requirements'
self.contract_doc.start_date = add_days(nowdate(), -2)
self.contract_doc.end_date = add_days(nowdate(), 1)
self.contract_doc.requires_fulfilment = 1
self.contract_doc.fulfilment_deadline = add_days(nowdate(), -1)
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Lapsed')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:93*

### test_fulfilled_contract_status

**Category**: workflow  
**Description**: Workflow: test fulfilled contract status  
**Expected**: self.assertEqual(self.contract_doc.fulfilment_status, 'Fulfilled')  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'
self.contract_doc.requires_fulfilment = 1
fulfilment_terms = []
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
for term in self.contract_doc.fulfilment_terms:
    term.fulfilled = 1
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Fulfilled')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:61*

### test_partially_fulfilled_contract_status

**Category**: workflow  
**Description**: Workflow: test partially fulfilled contract status  
**Expected**: self.assertEqual(self.contract_doc.fulfilment_status, 'Partially Fulfilled')  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'
self.contract_doc.requires_fulfilment = 1
self.contract_doc.save()
fulfilment_terms = []
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
fulfilment_terms.append({'requirement': 'This is another test requirement.', 'fulfilled': 0})
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
self.contract_doc.fulfilment_terms[0].fulfilled = 1
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Partially Fulfilled')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:77*

### test_lapsed_contract_status

**Category**: workflow  
**Description**: Workflow: test lapsed contract status  
**Expected**: self.assertEqual(self.contract_doc.fulfilment_status, 'Lapsed')  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
self.contract_doc.contract_term = '_Test Customer Contract with Requirements'
self.contract_doc.start_date = add_days(nowdate(), -2)
self.contract_doc.end_date = add_days(nowdate(), 1)
self.contract_doc.requires_fulfilment = 1
self.contract_doc.fulfilment_deadline = add_days(nowdate(), -1)
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Lapsed')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:93*

### test_make_new_lead_if_required

**Category**: method_call  
**Description**: test make new lead if required  
**Expected**: self.assertEqual(opp_doc.opportunity_from, 'Lead')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertTrue(opp_doc.party_name)
self.assertEqual(opp_doc.opportunity_from, 'Lead')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:62*

### test_make_new_lead_if_required

**Category**: method_call  
**Description**: test make new lead if required  
**Expected**: self.assertEqual(frappe.db.get_value('Lead', opp_doc.party_name, 'email_id'), opp_doc.contact_email)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(opp_doc.opportunity_from, 'Lead')
self.assertEqual(frappe.db.get_value('Lead', opp_doc.party_name, 'email_id'), opp_doc.contact_email)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:63*

### test_carry_forward_of_email_and_comments

**Category**: method_call  
**Description**: test carry forward of email and comments  
**Expected**: self.assertEqual(opportunity_communication_count, 2)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(opportunity_comment_count, 2)
self.assertEqual(opportunity_communication_count, 2)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:95*

### test_make_new_lead_if_required

**Category**: method_call  
**Description**: test make new lead if required  
**Expected**: self.assertEqual(opp_doc.opportunity_from, 'Lead')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertTrue(opp_doc.party_name)
self.assertEqual(opp_doc.opportunity_from, 'Lead')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:62*

### test_make_new_lead_if_required

**Category**: method_call  
**Description**: test make new lead if required  
**Expected**: self.assertEqual(frappe.db.get_value('Lead', opp_doc.party_name, 'email_id'), opp_doc.contact_email)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(opp_doc.opportunity_from, 'Lead')
self.assertEqual(frappe.db.get_value('Lead', opp_doc.party_name, 'email_id'), opp_doc.contact_email)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:63*

### test_carry_forward_of_email_and_comments

**Category**: method_call  
**Description**: test carry forward of email and comments  
**Expected**: self.assertEqual(opportunity_communication_count, 2)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(opportunity_comment_count, 2)
self.assertEqual(opportunity_communication_count, 2)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:95*

### test_add_lead_to_prospect_and_address_linking

**Category**: method_call  
**Description**: test add lead to prospect and address linking  
**Expected**: self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
address_doc.reload()
self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:27*

### test_make_customer_from_prospect

**Category**: method_call  
**Description**: test make customer from prospect  
**Expected**: self.assertEqual(customer.company_name, '_Test Prospect')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(customer.doctype, 'Customer')
self.assertEqual(customer.company_name, '_Test Prospect')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:46*

### test_make_customer_from_prospect

**Category**: method_call  
**Description**: test make customer from prospect  
**Expected**: self.assertEqual(customer.customer_group, '_Test Customer Group')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(customer.company_name, '_Test Prospect')
self.assertEqual(customer.customer_group, '_Test Customer Group')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:47*

### test_add_lead_to_prospect_and_address_linking

**Category**: method_call  
**Description**: test add lead to prospect and address linking  
**Expected**: self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
address_doc.reload()
self.assertEqual(address_doc.has_link('Prospect', prospect_doc.name), True)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:27*

### test_make_customer_from_prospect

**Category**: method_call  
**Description**: test make customer from prospect  
**Expected**: self.assertEqual(customer.company_name, '_Test Prospect')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(customer.doctype, 'Customer')
self.assertEqual(customer.company_name, '_Test Prospect')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:46*

### test_make_customer_from_prospect

**Category**: method_call  
**Description**: test make customer from prospect  
**Expected**: self.assertEqual(customer.customer_group, '_Test Customer Group')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(customer.company_name, '_Test Prospect')
self.assertEqual(customer.customer_group, '_Test Customer Group')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:47*

### test_make_customer

**Category**: method_call  
**Description**: test make customer  
**Expected**: self.assertEqual(customer.lead_name, self.leads[0].name)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(customer.doctype, 'Customer')
self.assertEqual(customer.lead_name, self.leads[0].name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:26*

### test_make_customer_from_organization

**Category**: method_call  
**Description**: test make customer from organization  
**Expected**: self.assertEqual(customer.lead_name, self.leads[1].name)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(customer.doctype, 'Customer')
self.assertEqual(customer.lead_name, self.leads[1].name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:52*

### test_create_lead_and_unlinking_dynamic_links

**Category**: method_call  
**Description**: test create lead and unlinking dynamic links  
**Expected**: self.assertEqual(frappe.db.exists('Lead', lead_doc.name), None)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
address_1.reload()
self.assertEqual(frappe.db.exists('Lead', lead_doc.name), None)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:88*

### test_create_lead_and_unlinking_dynamic_links

**Category**: method_call  
**Description**: test create lead and unlinking dynamic links  
**Expected**: self.assertEqual(len(address_1.get('links')), 1)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(frappe.db.exists('Lead', lead_doc.name), None)
self.assertEqual(len(address_1.get('links')), 1)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:89*

### test_prospect_creation_from_lead

**Category**: method_call  
**Description**: test prospect creation from lead  
**Expected**: self.assertEqual(event.event_participants[1].reference_doctype, 'Prospect')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
event.reload()
self.assertEqual(event.event_participants[1].reference_doctype, 'Prospect')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:110*

### test_prospect_creation_from_lead

**Category**: method_call  
**Description**: test prospect creation from lead  
**Expected**: self.assertEqual(event.event_participants[1].reference_docname, prospect)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(event.event_participants[1].reference_doctype, 'Prospect')
self.assertEqual(event.event_participants[1].reference_docname, prospect)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:111*

### test_opportunity_from_lead

**Category**: method_call  
**Description**: test opportunity from lead  
**Expected**: self.assertEqual(opportunity.get('party_name'), lead.name)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
opportunity.save()
self.assertEqual(opportunity.get('party_name'), lead.name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:130*

### test_opportunity_from_lead

**Category**: method_call  
**Description**: test opportunity from lead  
**Expected**: self.assertEqual(opportunity.notes[0].note, 'test note')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(opportunity.get('party_name'), lead.name)
self.assertEqual(opportunity.notes[0].note, 'test note')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/lead/test_lead.py:132*

### test_unsigned_contract_status

**Category**: method_call  
**Description**: test unsigned contract status  
**Expected**: self.assertEqual(self.contract_doc.status, 'Unsigned')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
# Setup
frappe.db.sql('delete from `tabContract`')
self.contract_doc = get_contract()

self.contract_doc.insert()
self.assertEqual(self.contract_doc.status, 'Unsigned')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:22*

### test_active_signed_contract_status

**Category**: method_call  
**Description**: test active signed contract status  
**Expected**: self.assertEqual(self.contract_doc.status, 'Active')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
# Setup
frappe.db.sql('delete from `tabContract`')
self.contract_doc = get_contract()

self.contract_doc.insert()
self.assertEqual(self.contract_doc.status, 'Active')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:29*

### test_past_inactive_signed_contract_status

**Category**: method_call  
**Description**: test past inactive signed contract status  
**Expected**: self.assertEqual(self.contract_doc.status, 'Inactive')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
# Setup
frappe.db.sql('delete from `tabContract`')
self.contract_doc = get_contract()

self.contract_doc.insert()
self.assertEqual(self.contract_doc.status, 'Inactive')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:37*

### test_future_inactive_signed_contract_status

**Category**: method_call  
**Description**: test future inactive signed contract status  
**Expected**: self.assertEqual(self.contract_doc.status, 'Inactive')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
# Setup
frappe.db.sql('delete from `tabContract`')
self.contract_doc = get_contract()

self.contract_doc.insert()
self.assertEqual(self.contract_doc.status, 'Inactive')
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/contract/test_contract.py:45*

### test_opportunity_status

**Category**: instantiation  
**Description**: Instantiate make_opportunity: test opportunity status  
**Expected**: self.assertEqual(doc.status, 'Quotation')  
**Confidence**: 0.80  
**Tags**: unittest  

```python
doc = make_opportunity(with_items=0)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:48*

### test_opportunity_status

**Category**: instantiation  
**Description**: Instantiate make_quotation: test opportunity status  
**Expected**: self.assertEqual(doc.status, 'Quotation')  
**Confidence**: 0.80  
**Tags**: unittest  

```python
quotation = make_quotation(doc.name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/opportunity/test_opportunity.py:49*

### test_add_lead_to_prospect_and_address_linking

**Category**: instantiation  
**Description**: Instantiate make_address: test add lead to prospect and address linking  
**Expected**: self.assertEqual(lead_exists_in_prosoect, True)  
**Confidence**: 0.80  
**Tags**: unittest  

```python
address_doc = make_address(address_title=lead_doc.name)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:16*

### test_make_customer_from_prospect

**Category**: instantiation  
**Description**: Instantiate get_doc: test make customer from prospect  
**Expected**: self.assertEqual(customer.doctype, 'Customer')  
**Confidence**: 0.80  
**Tags**: unittest  

```python
prospect = frappe.get_doc({'doctype': 'Prospect', 'company_name': '_Test Prospect', 'customer_group': '_Test Customer Group'})
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/prospect/test_prospect.py:35*

### test_calendar_event_created

**Category**: instantiation  
**Description**: Instantiate get_doc: test calendar event created  
**Expected**: self.assertEqual(cal_event.starts_on, self.test_appointment.scheduled_time)  
**Confidence**: 0.80  
**Tags**: unittest  

```python
# Setup
self.test_appointment = create_test_appointment()
self.test_appointment.set_verified(self.test_appointment.customer_email)

cal_event = frappe.get_doc('Event', self.test_appointment.calendar_event)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/appointment/test_appointment.py:40*

### test_calendar_event_created

**Category**: instantiation  
**Description**: Instantiate get_doc: test calendar event created  
**Expected**: self.assertEqual(cal_event.starts_on, self.test_appointment.scheduled_time)  
**Confidence**: 0.80  
**Tags**: unittest  

```python
cal_event = frappe.get_doc('Event', self.test_appointment.calendar_event)
```

*Source: /Users/vovanduc/Code/dcnet/flow_next/dcnet_core/erpnext/crm/doctype/appointment/test_appointment.py:40*

