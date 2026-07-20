# Frappe Testing

Comprehensive reference for testing patterns, utilities, and best practices in Frappe Framework.

---

## Test Class Hierarchy

### v15+ Test Classes (Recommended)

Frappe v15 introduced two specialized base classes replacing the older `FrappeTestCase`:

```python
# For tests that need database access and full framework context
from frappe.tests import IntegrationTestCase

class TestSalesOrder(IntegrationTestCase):
    """Each test method runs in its own transaction that is rolled back."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Shared fixtures created ONCE for all test methods
        cls.customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": "_Test Integration Customer",
            "customer_group": "All Customer Groups",
            "territory": "All Territories"
        }).insert()
        frappe.db.commit()  # IMPORTANT: commit so rollback doesn't lose fixtures

    def test_submit_order(self):
        so = frappe.get_doc({...}).insert()
        so.submit()
        self.assertEqual(so.docstatus, 1)

    def tearDown(self):
        # Transaction auto-rollback per test method
        super().tearDown()
```

```python
# For pure logic tests with NO database access
from frappe.tests import UnitTestCase

class TestPriceCalculation(UnitTestCase):
    """No database, no framework context. Fast execution."""

    def test_discount_calculation(self):
        result = calculate_discount(1000, 10)
        self.assertEqual(result, 900)

    def test_tax_inclusive_price(self):
        result = get_tax_inclusive(1000, 10)
        self.assertEqual(result, 1100)
```

### v14 Legacy (Still Works in v15/v16)

```python
from frappe.tests.utils import FrappeTestCase

class TestFittingSession(FrappeTestCase):
    """Provides auto transaction rollback per test method."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup shared fixtures
        frappe.db.commit()

    def tearDown(self):
        frappe.set_user("Administrator")  # Reset user after permission tests
        super().tearDown()
```

| Class | DB Access | Rollback | Use Case |
|-------|-----------|----------|----------|
| `UnitTestCase` | No | N/A | Pure logic, calculations, utilities |
| `IntegrationTestCase` | Yes | Per method | DocType CRUD, workflows, permissions |
| `FrappeTestCase` (v14) | Yes | Per method | Legacy -- still works but prefer above |

---

## Test Directory Structure

### Standard Layout

```
dcnet_apps/
  dcnet_apps/
    fitting/
      doctype/
        fitting_session/
          fitting_session.py
          test_fitting_session.py      # DocType-specific tests
          test_records.json            # Auto-loaded test data
      tests/
        __init__.py
        test_fitting_workflow.py       # Cross-cutting tests
        test_fitting_api.py            # API endpoint tests
        test_fitting_permissions.py    # Permission tests
      report/
        fitting_summary/
          fitting_summary.py
          test_fitting_summary.py      # Report tests
```

### test_records.json (Auto-loaded Fixtures)

```json
[
    {
        "doctype": "Fitting Session",
        "customer": "_Test Fitting Customer",
        "fitting_date": "2026-01-15",
        "status": "Draft",
        "items": [
            {
                "doctype": "Fitting Service",
                "service_type": "Club Fitting",
                "parentfield": "services"
            }
        ]
    }
]
```

Records in `test_records.json` are auto-inserted before tests run. Use `_Test` prefix for names to avoid collisions with real data.

---

## Bench Test Commands

### Basic Usage

```bash
# Run ALL tests for an app
bench --site [site] run-tests --app dcnet_apps

# Run tests for a specific module
bench --site [site] run-tests --app dcnet_apps --module fitting

# Run tests for a specific DocType
bench --site [site] run-tests --app dcnet_apps --doctype "Fitting Session"

# Run a specific test file
bench --site [site] run-tests --app dcnet_apps --test fitting/tests/test_fitting_workflow.py

# Verbose output (see individual test names)
bench --site [site] run-tests --app dcnet_apps --module fitting -v

# Stop on first failure
bench --site [site] run-tests --app dcnet_apps --module fitting --failfast

# With coverage report
bench --site [site] run-tests --app dcnet_apps --module fitting --coverage
```

### All Flags Reference

| Flag | Description | Example |
|------|-------------|---------|
| `--app` | App to test | `--app dcnet_apps` |
| `--module` | Module within app | `--module fitting` |
| `--doctype` | Specific DocType | `--doctype "Fitting Session"` |
| `--test` | Specific test file path | `--test fitting/tests/test_api.py` |
| `-v` / `--verbose` | Verbose output | `-v` |
| `--failfast` | Stop on first failure | `--failfast` |
| `--coverage` | Generate coverage report | `--coverage` |
| `--profile` | Profile test execution | `--profile` |
| `--junit-xml-output` | JUnit XML output path | `--junit-xml-output results.xml` |
| `--ui-tests` | Run UI (Cypress) tests | `--ui-tests` |
| `--skip-before-tests` | Skip before_tests hooks | `--skip-before-tests` |

### DCNET Docker Pattern

```bash
# Standard pattern for running tests in Docker
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app dcnet_apps --module fitting -v"

# With failfast
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app dcnet_apps --module fitting -v --failfast"
```

---

## Factory Pattern for Test Data

### Simple Factory Functions

```python
def make_fitting_session(**kwargs):
    """Factory to create Fitting Session with sensible defaults."""
    session = frappe.get_doc({
        "doctype": "Fitting Session",
        "customer": kwargs.get("customer", "_Test Fitting Customer"),
        "fitting_date": kwargs.get("fitting_date", frappe.utils.today()),
        "fitter": kwargs.get("fitter", "Administrator"),
        "status": kwargs.get("status", "Draft"),
        "services": kwargs.get("services", [
            {
                "doctype": "Fitting Service",
                "service_type": "Club Fitting",
                "parentfield": "services"
            }
        ]),
        "measurements": kwargs.get("measurements", [])
    })

    if not kwargs.get("do_not_insert"):
        session.insert()
        if kwargs.get("submit"):
            session.submit()

    return session
```

### Usage in Tests

```python
class TestFittingSession(IntegrationTestCase):

    def test_draft_session(self):
        session = make_fitting_session()
        self.assertEqual(session.status, "Draft")

    def test_submitted_session(self):
        session = make_fitting_session(submit=True)
        self.assertEqual(session.docstatus, 1)

    def test_custom_customer(self):
        session = make_fitting_session(
            customer="_Test VIP Customer",
            fitting_date="2026-03-15"
        )
        self.assertEqual(session.customer, "_Test VIP Customer")
```

### Dataclass Factory (Advanced)

```python
from dataclasses import dataclass, field
from frappe.utils import today, random_string

@dataclass
class FittingSessionFactory:
    """Factory for Fitting Session test documents."""

    customer: str = "_Test Fitting Customer"
    fitting_date: str = field(default_factory=today)
    fitter: str = "Administrator"
    status: str = "Draft"

    @classmethod
    def build(cls, **kwargs):
        """Build without saving (for unit tests)."""
        factory = cls(**kwargs)
        return frappe.get_doc({
            "doctype": "Fitting Session",
            "customer": factory.customer,
            "fitting_date": factory.fitting_date,
            "fitter": factory.fitter,
            "status": factory.status,
        })

    @classmethod
    def create(cls, **kwargs):
        """Create and save."""
        doc = cls.build(**kwargs)
        doc.insert(ignore_permissions=True)
        return doc

    @classmethod
    def create_batch(cls, count, **kwargs):
        """Create multiple documents."""
        return [cls.create(**kwargs) for _ in range(count)]

    @classmethod
    def create_submitted(cls, **kwargs):
        """Create and submit."""
        doc = cls.create(**kwargs)
        doc.submit()
        return doc
```

---

## Workflow Testing

### CRITICAL: Correct Imports

```python
# CORRECT - these exist in Frappe
from frappe.model.workflow import apply_workflow, WorkflowTransitionError

# WRONG - this does NOT exist! Will cause ImportError!
# from frappe.exceptions import InvalidTransitionError  # DOES NOT EXIST
```

### Workflow Transition Tests

```python
from frappe.model.workflow import apply_workflow, WorkflowTransitionError

class TestFittingWorkflow(IntegrationTestCase):

    def test_valid_transition(self):
        """Test: Draft -> Scheduled (via Schedule action)."""
        session = make_fitting_session()
        apply_workflow(session, "Schedule")
        session.reload()
        self.assertEqual(session.workflow_state, "Scheduled")

    def test_invalid_transition(self):
        """Test: Cannot go from Draft directly to Completed."""
        session = make_fitting_session()
        with self.assertRaises(WorkflowTransitionError):
            apply_workflow(session, "Complete")

    def test_full_workflow_chain(self):
        """Test the complete happy path workflow."""
        session = make_fitting_session()

        # Draft -> Scheduled
        apply_workflow(session, "Schedule")
        session.reload()
        self.assertEqual(session.workflow_state, "Scheduled")

        # Scheduled -> In Progress
        apply_workflow(session, "Start")
        session.reload()
        self.assertEqual(session.workflow_state, "In Progress")

        # In Progress -> Completed
        apply_workflow(session, "Complete")
        session.reload()
        self.assertEqual(session.workflow_state, "Completed")

    def test_workflow_with_role_restriction(self):
        """Test that only authorized roles can make transitions."""
        session = make_fitting_session()

        # Set to a user without the required role
        frappe.set_user("test_basic_user@example.com")

        with self.assertRaises(WorkflowTransitionError):
            apply_workflow(session, "Approve")
```

---

## Permission Testing

### Pattern: set_user / has_permission

```python
class TestFittingPermissions(IntegrationTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fitter_user = create_test_user(
            "test_fitter@example.com",
            roles=["Fitter", "System Manager"]
        )
        cls.basic_user = create_test_user(
            "test_basic@example.com",
            roles=["Employee"]
        )
        frappe.db.commit()

    def tearDown(self):
        # ALWAYS reset to Administrator after permission tests
        frappe.set_user("Administrator")
        super().tearDown()

    def test_fitter_can_read(self):
        frappe.set_user("test_fitter@example.com")
        session = make_fitting_session()
        self.assertTrue(
            frappe.has_permission("Fitting Session", "read", doc=session.name)
        )

    def test_basic_user_cannot_write(self):
        frappe.set_user("test_basic@example.com")
        session = make_fitting_session()
        self.assertFalse(
            frappe.has_permission("Fitting Session", "write", doc=session.name)
        )

    def test_permission_error_on_insert(self):
        frappe.set_user("test_basic@example.com")
        with self.assertRaises(frappe.PermissionError):
            frappe.get_doc({
                "doctype": "Fitting Session",
                "customer": "_Test Customer"
            }).insert()


def create_test_user(email, roles=None):
    """Helper to create test user with specified roles."""
    if frappe.db.exists("User", email):
        return frappe.get_doc("User", email)

    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": email.split("@")[0],
        "enabled": 1,
        "new_password": "test_password_123",
        "roles": [{"role": r} for r in (roles or [])]
    }).insert()
    return user
```

---

## Mocking Patterns

### Mock frappe.db.commit (Prevent Actual Commits)

```python
from unittest.mock import patch, MagicMock

class TestWithMocking(IntegrationTestCase):

    @patch("frappe.db.commit")
    def test_service_calls_commit(self, mock_commit):
        """Verify commit is called without actually committing."""
        process_fitting_completion("FS-00001")
        mock_commit.assert_called_once()
```

### Mock frappe.sendmail (Prevent Emails)

```python
    @patch("frappe.sendmail")
    def test_notification_sent(self, mock_sendmail):
        session = make_fitting_session(submit=True)
        apply_workflow(session, "Complete")

        mock_sendmail.assert_called_once()
        call_kwargs = mock_sendmail.call_args[1]
        self.assertIn("Fitting Complete", call_kwargs.get("subject", ""))
```

### Mock External API Calls

```python
    @patch("dcnet_apps.fitting.api.call_external_service")
    def test_external_integration(self, mock_api):
        mock_api.return_value = {"status": "success", "id": "EXT-001"}

        result = sync_fitting_to_external("FS-00001")

        mock_api.assert_called_once_with("FS-00001")
        self.assertEqual(result["id"], "EXT-001")
```

### Using frappe.flags.in_test

```python
# In your application code, guard test-specific behavior:
def send_fitting_reminder(session_name):
    """Send reminder email. Skipped during tests unless explicitly enabled."""
    if frappe.flags.in_test:
        return  # Skip in tests

    session = frappe.get_doc("Fitting Session", session_name)
    frappe.sendmail(
        recipients=[session.customer_email],
        subject="Fitting Reminder",
        message=f"Your fitting session is scheduled for {session.fitting_date}"
    )

# In tests, you can override:
def test_reminder_actually_sends(self):
    frappe.flags.in_test = False  # Temporarily disable test flag
    try:
        with patch("frappe.sendmail") as mock_mail:
            send_fitting_reminder("FS-00001")
            mock_mail.assert_called_once()
    finally:
        frappe.flags.in_test = True  # Restore
```

---

## Test Data Conventions

### Naming Conventions

| Entity | Convention | Example |
|--------|-----------|---------|
| Customer | `_Test {Description}` | `_Test Fitting Customer` |
| Item | `_Test {Description}` | `_Test Golf Club Driver` |
| Supplier | `_Test {Description}` | `_Test Equipment Supplier` |
| Warehouse | `_Test {Description} - {abbr}` | `_Test Store - TL` |
| User email | `test_{role}@example.com` | `test_fitter@example.com` |

### Cleanup in tearDown

```python
def tearDown(self):
    frappe.set_user("Administrator")

    # Delete test docs created during this test
    for name in self._created_docs:
        frappe.delete_doc("Fitting Session", name, force=True)

    super().tearDown()
```

### Using get_test_records

```python
# Load test records from test_records.json
from frappe.tests.utils import get_test_records

test_records = get_test_records("Fitting Session")
# Returns list of dicts from test_records.json
```

---

## Pytest Integration (v15+)

Frappe v15+ supports pytest alongside unittest. Configuration via `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["dcnet_apps"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--tb=short -q"
```

### Running with pytest

```bash
# Run via bench (preferred -- sets up Frappe context)
bench --site flow.local run-tests --app dcnet_apps --module fitting

# Direct pytest (requires FRAPPE_SITE env var)
cd /workspace/development/frappe-bench
FRAPPE_SITE=flow.local python -m pytest apps/dcnet_apps/dcnet_apps/fitting/tests/ -v
```

### Pytest Fixtures (with Frappe)

```python
import pytest
import frappe

@pytest.fixture
def fitting_customer():
    """Create and return a test customer, cleaned up after test."""
    customer = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": "_Test Pytest Customer",
        "customer_group": "All Customer Groups",
        "territory": "All Territories"
    }).insert()
    frappe.db.commit()

    yield customer

    # Cleanup
    frappe.delete_doc("Customer", customer.name, force=True)
    frappe.db.commit()

@pytest.fixture
def fitting_session(fitting_customer):
    """Create fitting session with auto-created customer."""
    session = frappe.get_doc({
        "doctype": "Fitting Session",
        "customer": fitting_customer.name,
        "fitting_date": frappe.utils.today()
    }).insert()
    frappe.db.commit()

    yield session

    frappe.delete_doc("Fitting Session", session.name, force=True)
    frappe.db.commit()

def test_session_creation(fitting_session):
    assert fitting_session.status == "Draft"
    assert fitting_session.customer is not None
```

### Pytest Fixtures for User Context

```python
@pytest.fixture
def as_user():
    """Context manager fixture to run as a specific user."""
    def _as_user(email):
        original = frappe.session.user
        frappe.set_user(email)
        return original
    return _as_user

@pytest.fixture(autouse=True)
def reset_user():
    """Always reset to Administrator after each test."""
    yield
    frappe.set_user("Administrator")

@pytest.fixture
def rollback_db():
    """Rollback database after test."""
    frappe.db.begin()
    yield
    frappe.db.rollback()
```

---

## Common Assertions and Utilities

```python
# Document existence
self.assertTrue(frappe.db.exists("Fitting Session", session.name))
self.assertFalse(frappe.db.exists("Fitting Session", "non-existent"))

# Field values
self.assertEqual(frappe.db.get_value("Fitting Session", name, "status"), "Completed")

# Document count
count = frappe.db.count("Fitting Session", {"customer": "_Test Customer"})
self.assertGreater(count, 0)

# Exception assertions
with self.assertRaises(frappe.ValidationError):
    invalid_doc.insert()

with self.assertRaises(frappe.PermissionError):
    frappe.get_doc("Fitting Session", name)

with self.assertRaises(WorkflowTransitionError):
    apply_workflow(doc, "Invalid Action")

# Frappe message assertions (check frappe.throw was called)
with self.assertRaises(frappe.ValidationError) as cm:
    doc.insert()
self.assertIn("required", str(cm.exception))

# Check linked documents were created
gl_entries = frappe.get_all("GL Entry", filters={"voucher_no": invoice.name})
self.assertTrue(len(gl_entries) > 0)

# Subtests for parameterized testing
for status in ["Draft", "Scheduled", "In Progress"]:
    with self.subTest(status=status):
        session = make_fitting_session(status=status)
        self.assertEqual(session.status, status)
```

---

## Tips and Gotchas

| Issue | Solution |
|-------|----------|
| `setUpClass` data disappears | Call `frappe.db.commit()` after creating setup data |
| User not reset after test | Always `frappe.set_user("Administrator")` in `tearDown` |
| Test order dependency | Each test must be independent; do not rely on execution order |
| `flags.in_test` skipping logic | Use mocking instead of flags for testable code paths |
| Slow tests | Use `UnitTestCase` for pure logic; minimize DB operations |
| `ImportError: InvalidTransitionError` | Use `WorkflowTransitionError` from `frappe.model.workflow` |
| Test data leaking between tests | `IntegrationTestCase` auto-rollbacks; or clean up in `tearDown` |
| Child table test data | Include `parentfield` and `doctype` in child dicts |
| Workflow not found | Ensure workflow is enabled and module matches the DocType |
| `frappe.db.commit()` in tests | Avoid unless in `setUpClass`; auto-rollback handles cleanup |
