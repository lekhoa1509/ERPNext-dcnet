<!-- Source: erpnext-crm skill -->

# ERPNext CRM Module Skill

> **ERPNext CRM** is the built-in CRM module in ERPNext v16, providing complete lead management, sales pipeline tracking, and customer relationship functionality.

## Quick Topic Reference

| Topic | Documentation | API Reference |
|-------|---------------|---------------|
| **Lead** | [references/docs/lead.md](references/docs/lead.md) | [api_reference/lead.md](api_reference/lead.md) |
| **Opportunity** | [references/docs/opportunity.md](references/docs/opportunity.md) | [api_reference/opportunity.md](api_reference/opportunity.md) |
| **Prospect** | [references/docs/prospect.md](references/docs/prospect.md) | [api_reference/prospect.md](api_reference/prospect.md) |
| **Campaign** | [references/docs/campaign.md](references/docs/campaign.md) | [api_reference/campaign.md](api_reference/campaign.md) |
| **Contract** | [references/docs/contract.md](references/docs/contract.md) | [api_reference/contract.md](api_reference/contract.md) |
| **Appointment** | [references/docs/appointment.md](references/docs/appointment.md) | [api_reference/appointment.md](api_reference/appointment.md) |
| **CRM Settings** | [references/docs/crm-settings.md](references/docs/crm-settings.md) | [api_reference/crm_settings.md](api_reference/crm_settings.md) |
| **Reports** | [references/docs/reports.md](references/docs/reports.md) | See individual report files |

## When to Use This Skill

Use this skill when you need to:
- Manage leads and track lead conversion
- Track sales pipeline and opportunities
- Run marketing campaigns and email automation
- Handle customer/supplier contracts
- Book and manage appointments
- Understand CRM configuration patterns
- Find test examples and real-world usage

## ⚡ Quick Reference

### Codebase Statistics

**Languages:**
- **Python**: 58 files (98.3%)
- **JavaScript**: 1 files (1.7%)

**Analysis Performed:**
- ✅ API Reference (C2.5)
- ✅ Dependency Graph (C2.6)
- ✅ Design Patterns (C3.1)
- ✅ Test Examples (C3.2)
- ✅ Configuration Patterns (C3.4)
- ✅ Architectural Analysis (C3.7)
- ✅ Project Documentation (C3.9)

### 🎨 Design Patterns Detected

*From C3.1 codebase analysis (confidence > 0.7)*

- **Factory**: 6 instances
- **Observer**: 2 instances
- **Command**: 2 instances

*Total: 10 high-confidence patterns*

*See `references/patterns/` for complete pattern analysis*

## 📝 Code Examples

*High-quality examples extracted from test files (C3.2)*

**Workflow: test carry forward of email and comments** (complexity: 1.00)

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

**Workflow: test carry forward of email and comments** (complexity: 1.00)

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

**Workflow: test add lead to prospect and address linking** (complexity: 1.00)

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

**Workflow: test add lead to prospect and address linking** (complexity: 1.00)

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

**Workflow: test make customer** (complexity: 1.00)

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

**Workflow: test make customer** (complexity: 1.00)

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

**Workflow: test partially fulfilled contract status** (complexity: 1.00)

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

**Workflow: test partially fulfilled contract status** (complexity: 1.00)

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

**Workflow: test fulfilled contract status** (complexity: 0.80)

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

**Workflow: test fulfilled contract status** (complexity: 0.80)

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

*See `references/test_examples/` for all extracted examples*

## ⚙️ Configuration Patterns

*From C3.4 configuration analysis*

**Configuration Files Analyzed:** 49
**Total Settings:** 1080
**Patterns Detected:** 0

**Configuration Types:**
- unknown: 49 files

*See `references/config_patterns/` for detailed configuration analysis*

## 📖 Project Documentation

*Extracted from markdown files in the project (C3.9)*

**Total Documentation Files:** 1
**Categories:** 1

### Other

- **README**: Potential sales opportunity (deal) from a Lead or Customer.

*See `references/documentation/` for all project documentation*

## 📚 Available References

This skill includes detailed reference documentation:

- **API Reference**: `references/api_reference/` - Complete API documentation
- **Dependencies**: `references/dependencies/` - Dependency graph and analysis
- **Patterns**: `references/patterns/` - Detected design patterns
- **Examples**: `references/test_examples/` - Usage examples from tests
- **Configuration**: `references/config_patterns/` - Configuration patterns
- **Documentation**: `references/documentation/` - Project documentation

---

**Generated by Skill Seeker** | Codebase Analyzer with C3.x Analysis
