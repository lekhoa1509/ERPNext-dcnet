# CRM Reports Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/report

## Overview

ERPNext CRM module includes several built-in reports for tracking lead performance, sales pipeline, campaign effectiveness, and opportunity analysis.

## Available Reports

### 1. Lead Details

**Path:** `CRM > Reports > Lead Details`

**Purpose:** Comprehensive lead listing with all details

**Filters:**
- Company
- Territory
- Lead Owner
- Source
- From/To Date

**Columns:**
- Lead Name
- Email
- Phone
- Status
- Source
- Territory
- Lead Owner
- Creation Date

**Python API:**
```python
from erpnext.crm.report.lead_details.lead_details import execute

filters = {
    "company": "My Company",
    "from_date": "2026-01-01",
    "to_date": "2026-01-31",
    "status": "Open"
}

columns, data = execute(filters)
```

---

### 2. Lead Conversion Time

**Path:** `CRM > Reports > Lead Conversion Time`

**Purpose:** Track time from Lead creation to Customer conversion

**Filters:**
- Company
- From/To Date

**Columns:**
- Lead Name
- Creation Date
- Conversion Date
- Conversion Time (days)
- Lead Owner

**Python API:**
```python
from erpnext.crm.report.lead_conversion_time.lead_conversion_time import execute

filters = {
    "company": "My Company",
    "from_date": "2026-01-01",
    "to_date": "2026-01-31"
}

columns, data = execute(filters)
```

**Metrics:**
- Average conversion time
- Min/Max conversion time
- Conversion by owner

---

### 3. Lead Owner Efficiency

**Path:** `CRM > Reports > Lead Owner Efficiency`

**Purpose:** Track lead owner performance

**Filters:**
- Company
- From/To Date

**Columns:**
- Lead Owner
- Total Leads
- Open Leads
- Converted Leads
- Conversion Rate (%)

**Python API:**
```python
from erpnext.crm.report.lead_owner_efficiency.lead_owner_efficiency import execute

filters = {
    "company": "My Company",
    "from_date": "2026-01-01",
    "to_date": "2026-01-31"
}

columns, data = execute(filters)
```

---

### 4. Campaign Efficiency

**Path:** `CRM > Reports > Campaign Efficiency`

**Purpose:** Track marketing campaign ROI

**Filters:**
- Company
- From/To Date
- Campaign

**Columns:**
- Campaign Name
- Lead Count
- Opportunity Count
- Quotation Count
- Order Count
- Order Value

**Python API:**
```python
from erpnext.crm.report.campaign_efficiency.campaign_efficiency import execute

filters = {
    "company": "My Company",
    "from_date": "2026-01-01",
    "to_date": "2026-01-31"
}

columns, data = execute(filters)
```

---

### 5. Sales Pipeline Analytics

**Path:** `CRM > Reports > Sales Pipeline Analytics`

**Purpose:** Visualize opportunity pipeline by stage

**Filters:**
- Company
- From/To Date
- Sales Stage
- Opportunity Owner

**Columns:**
- Sales Stage
- Opportunity Count
- Total Value
- Probability
- Weighted Value

**Python API:**
```python
from erpnext.crm.report.sales_pipeline_analytics.sales_pipeline_analytics import execute

filters = {
    "company": "My Company",
    "from_date": "2026-01-01",
    "to_date": "2026-03-31"
}

columns, data = execute(filters)
```

**Weighted Value Calculation:**
```python
weighted_value = opportunity_amount * (probability / 100)
```

---

### 6. Opportunity Summary by Sales Stage

**Path:** `CRM > Reports > Opportunity Summary by Sales Stage`

**Purpose:** Summary view of opportunities grouped by stage

**Filters:**
- Company
- Sales Stage
- From/To Date

**Columns:**
- Sales Stage
- Count
- Total Amount
- Average Amount
- Probability Range

**Python API:**
```python
from erpnext.crm.report.opportunity_summary_by_sales_stage.opportunity_summary_by_sales_stage import execute

filters = {
    "company": "My Company",
    "from_date": "2026-01-01",
    "to_date": "2026-03-31"
}

columns, data = execute(filters)
```

---

### 7. Lost Opportunity

**Path:** `CRM > Reports > Lost Opportunity`

**Purpose:** Analyze why opportunities are lost

**Filters:**
- Company
- From/To Date
- Lost Reason
- Competitor

**Columns:**
- Opportunity
- Customer/Lead
- Lost Reason(s)
- Competitor(s)
- Amount
- Lost Date

**Python API:**
```python
from erpnext.crm.report.lost_opportunity.lost_opportunity import execute

filters = {
    "company": "My Company",
    "from_date": "2026-01-01",
    "to_date": "2026-01-31"
}

columns, data = execute(filters)
```

---

### 8. First Response Time for Opportunity

**Path:** `CRM > Reports > First Response Time for Opportunity`

**Purpose:** Track response speed to new opportunities

**Filters:**
- Company
- From/To Date
- Opportunity Owner

**Columns:**
- Opportunity
- Creation Time
- First Response Time
- Response Duration

---

### 9. Prospects Engaged but Not Converted

**Path:** `CRM > Reports > Prospects Engaged but Not Converted`

**Purpose:** Identify prospects needing follow-up

**Filters:**
- Company
- From/To Date

**Columns:**
- Prospect Name
- Industry
- Lead Count
- Opportunity Count
- Last Activity
- Days Since Activity

**Python API:**
```python
from erpnext.crm.report.prospects_engaged_but_not_converted.prospects_engaged_but_not_converted import execute

filters = {
    "company": "My Company"
}

columns, data = execute(filters)
```

---

## Custom Report Example

### Create Custom CRM Report

```python
# File: custom_app/custom_app/report/my_crm_report/my_crm_report.py

from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Lead"),
            "fieldname": "lead",
            "fieldtype": "Link",
            "options": "Lead",
            "width": 150
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Owner"),
            "fieldname": "lead_owner",
            "fieldtype": "Link",
            "options": "User",
            "width": 150
        },
        {
            "label": _("Days Open"),
            "fieldname": "days_open",
            "fieldtype": "Int",
            "width": 100
        }
    ]

def get_data(filters):
    from frappe.utils import date_diff, today

    leads = frappe.get_all(
        "Lead",
        filters={
            "company": filters.get("company"),
            "status": ["in", ["Open", "Replied"]]
        },
        fields=["name", "status", "lead_owner", "creation"]
    )

    data = []
    for lead in leads:
        data.append({
            "lead": lead.name,
            "status": lead.status,
            "lead_owner": lead.lead_owner,
            "days_open": date_diff(today(), lead.creation)
        })

    return data
```

## Dashboard Charts

### Lead Funnel Chart

```python
# Custom script for Lead funnel
frappe.ui.form.on("Lead", {
    refresh: function(frm) {
        // Add dashboard chart
    }
});
```

### Pipeline Dashboard

```javascript
// Workspace dashboard showing pipeline
{
    "type": "chart",
    "chart_name": "Sales Pipeline",
    "doctype": "Opportunity",
    "filters_json": "{}",
    "timespan": "This Quarter"
}
```

## Related DocTypes

- **Lead** - Source data for lead reports
- **Opportunity** - Source data for pipeline reports
- **Campaign** - Source data for campaign reports
- **Lost Reason** - Used in lost opportunity analysis
- **Competitor** - Used in competitive analysis
- **Sales Stage** - Pipeline stage grouping
