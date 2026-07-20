from unittest.mock import Mock, patch

import frappe
from frappe.tests import IntegrationTestCase

from dcnet_crm import api, hooks, install, sales_order_events


class TestCRMAPI(IntegrationTestCase):
    def test_app_only_requires_frappe_and_erpnext(self):
        self.assertEqual(hooks.required_apps, ["frappe", "erpnext"])

    def test_resource_configuration_uses_standard_doctypes(self):
        expected = {
            "leads": "Lead",
            "opportunities": "Opportunity",
            "customers": "Customer",
            "contacts": "Contact",
            "quotations": "Quotation",
            "orders": "Sales Order",
            "accounts": "DCNET Service Account",
            "care_cards": "CRM Care Card",
        }
        self.assertEqual(
            {key: value["doctype"] for key, value in api.RESOURCE_CONFIG.items()},
            expected,
        )

    def test_invalid_resource_is_rejected(self):
        with self.assertRaises(frappe.ValidationError):
            api._get_resource("not-a-resource")

    def test_sales_order_display_status_uses_erpnext_lifecycle(self):
        draft = frappe._dict({
            "docstatus": 0,
            "status": "Draft",
            "custom_revenue_status": "Bản nhập",
        })
        self.assertEqual(
            api._get_sales_order_display_status(draft),
            {
                "display_order_status": "Đơn nháp",
                "display_revenue_status": "Đơn nháp",
                "display_execution_status": "Chưa thực hiện",
            },
        )

        fully_billed = frappe._dict({
            "docstatus": 1,
            "status": "To Deliver",
            "per_billed": 100,
            "per_delivered": 0,
            "billing_status": "Fully Billed",
            "delivery_status": "Not Delivered",
            "custom_revenue_status": "Bản nhập",
            "custom_execution_status": "Chưa thực hiện",
        })
        self.assertEqual(
            api._get_sales_order_display_status(fully_billed),
            {
                "display_order_status": "Chờ giao hàng",
                "display_revenue_status": "Đã ghi",
                "display_execution_status": "Chờ giao hàng",
            },
        )

        submitted_unbilled = frappe._dict({
            "docstatus": 1,
            "status": "To Deliver and Bill",
            "per_billed": 0,
            "per_delivered": 0,
            "billing_status": "Not Billed",
            "delivery_status": "Not Delivered",
        })
        self.assertEqual(
            api._get_sales_order_display_status(submitted_unbilled)[
                "display_revenue_status"
            ],
            "Đã ghi",
        )

    def test_sales_order_submit_marks_revenue_and_closes_request(self):
        doc = frappe._dict({"name": "SAL-ORD-0001"})
        todo = Mock()
        todo.name = "TODO-0001"
        todo.get.side_effect = lambda key, default=None: default
        request = frappe._dict({"name": "TODO-0001"})
        meta = Mock()
        meta.has_field.return_value = True

        with (
            patch.object(sales_order_events.frappe, "get_meta", return_value=meta),
            patch.object(sales_order_events.frappe.db, "set_value") as set_value,
            patch.object(api, "_get_open_so_revenue_requests", return_value=[request]),
            patch.object(sales_order_events.frappe, "get_doc", return_value=todo),
            patch.object(api, "_parse_todo_related_users", return_value=[]),
            patch.object(api, "_retract_todo_notifications") as retract,
        ):
            sales_order_events.on_submit(doc)

        set_value.assert_called_once_with(
            "Sales Order",
            "SAL-ORD-0001",
            "custom_revenue_status",
            "Đã ghi",
            update_modified=False,
        )
        self.assertEqual(todo.status, "Closed")
        todo.save.assert_called_once_with(ignore_permissions=True)
        retract.assert_called_once_with(todo, [])

    def test_contact_create_options_exclude_internal_role_masters(self):
        with (
            patch.object(api, "_check_permission"),
            patch.object(api.frappe, "has_permission", return_value=True),
            patch.object(api.frappe, "get_list", return_value=[]) as get_list,
        ):
            result = api.get_contact_create_options()

        requested_doctypes = {call.args[0] for call in get_list.call_args_list}
        self.assertNotIn("Designation", requested_doctypes)
        self.assertNotIn("Department", requested_doctypes)
        self.assertNotIn("designations", result)
        self.assertNotIn("departments", result)

    def test_create_quotation_activity_links_todo_to_quotation(self):
        todo = Mock(name="todo")
        todo.name = "TODO-0001"
        current_user = frappe.session.user
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "new_doc", return_value=todo),
        ):
            result = api.create_quotation_activity(
                "SAL-QTN-0001",
                {
                    "description": "Gọi xác nhận báo giá",
                    "date": "2026-07-15",
                    "priority": "High",
                },
            )

        self.assertEqual(
            check_permission.call_args_list,
            [
                (("Quotation",), {"name": "SAL-QTN-0001"}),
                (("ToDo", "create"), {}),
            ],
        )
        self.assertEqual(todo.reference_type, "Quotation")
        self.assertEqual(todo.reference_name, "SAL-QTN-0001")
        self.assertEqual(todo.description, "Gọi xác nhận báo giá")
        self.assertEqual(todo.status, "Open")
        self.assertEqual(todo.priority, "High")
        self.assertEqual(todo.allocated_to, current_user)
        todo.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result["name"], "TODO-0001")

    def test_create_lead_task_links_todo_to_lead_with_permissions(self):
        todo = Mock(name="todo")
        todo.name = "TODO-LEAD-0001"
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "new_doc", return_value=todo),
        ):
            result = api.save_lead_activity(
                "CRM-LEAD-2026-00010",
                {
                    "activity_type": "task",
                    "subject": "Gọi xác nhận nhu cầu",
                    "due_date": "2026-07-15",
                    "status": "Open",
                    "priority": "High",
                    "allocated_to": "sales@example.com",
                },
            )

        self.assertEqual(
            check_permission.call_args_list,
            [
                (("Lead", "write"), {"name": "CRM-LEAD-2026-00010"}),
                (("ToDo", "create"), {}),
            ],
        )
        self.assertEqual(todo.reference_type, "Lead")
        self.assertEqual(todo.reference_name, "CRM-LEAD-2026-00010")
        self.assertEqual(todo.description, "Gọi xác nhận nhu cầu")
        self.assertEqual(todo.date, "2026-07-15")
        self.assertEqual(todo.status, "Open")
        self.assertEqual(todo.priority, "High")
        self.assertEqual(todo.allocated_to, "sales@example.com")
        todo.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"doctype": "ToDo", "name": "TODO-LEAD-0001"})

    def test_create_lead_meeting_links_event_and_participants(self):
        event = Mock(name="event")
        event.name = "EVENT-LEAD-0001"
        event.meta.has_field.return_value = True
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "new_doc", return_value=event),
        ):
            result = api.save_lead_activity(
                "CRM-LEAD-2026-00010",
                {
                    "activity_type": "meeting",
                    "subject": "Lịch hẹn khảo sát",
                    "description": "Khảo sát điểm lắp đặt",
                    "location": "Văn phòng khách hàng",
                    "starts_on": "2026-07-15 14:30:00",
                    "ends_on": "2026-07-15 15:30:00",
                    "allocated_to": "sales@example.com",
                },
            )

        self.assertEqual(
            check_permission.call_args_list,
            [
                (("Lead", "write"), {"name": "CRM-LEAD-2026-00010"}),
                (("Event", "create"), {}),
            ],
        )
        self.assertEqual(event.event_category, "Meeting")
        self.assertEqual(event.reference_doctype, "Lead")
        self.assertEqual(event.reference_docname, "CRM-LEAD-2026-00010")
        self.assertEqual(event.location, "Văn phòng khách hàng")
        self.assertEqual(
            [call.args for call in event.append.call_args_list],
            [
                (
                    "event_participants",
                    {"reference_doctype": "Lead", "reference_docname": "CRM-LEAD-2026-00010"},
                ),
                (
                    "event_participants",
                    {"reference_doctype": "User", "reference_docname": "sales@example.com"},
                ),
            ],
        )
        event.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"doctype": "Event", "name": "EVENT-LEAD-0001"})

    def test_create_contact_task_links_todo_to_contact_with_permissions(self):
        todo = Mock(name="todo")
        todo.name = "TODO-CONTACT-0001"
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "new_doc", return_value=todo),
        ):
            result = api.save_contact_activity(
                "CONT-00010",
                {
                    "activity_type": "task",
                    "subject": "Chăm sóc liên hệ",
                    "due_date": "2026-07-15",
                    "status": "Open",
                    "allocated_to": "sales@example.com",
                },
            )

        self.assertEqual(
            check_permission.call_args_list,
            [
                (("Contact", "write"), {"name": "CONT-00010"}),
                (("ToDo", "create"), {}),
            ],
        )
        self.assertEqual(todo.reference_type, "Contact")
        self.assertEqual(todo.reference_name, "CONT-00010")
        self.assertEqual(todo.description, "Chăm sóc liên hệ")
        self.assertEqual(todo.allocated_to, "sales@example.com")
        todo.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"doctype": "ToDo", "name": "TODO-CONTACT-0001"})

    def test_create_contact_meeting_links_event_to_contact(self):
        event = Mock(name="event")
        event.name = "EVENT-CONTACT-0001"
        event.meta.has_field.return_value = True
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "new_doc", return_value=event),
        ):
            result = api.save_contact_activity(
                "CONT-00010",
                {
                    "activity_type": "meeting",
                    "subject": "Lịch hẹn chăm sóc",
                    "starts_on": "2026-07-15 14:30:00",
                    "ends_on": "2026-07-15 15:30:00",
                    "allocated_to": "sales@example.com",
                },
            )

        self.assertEqual(
            check_permission.call_args_list,
            [
                (("Contact", "write"), {"name": "CONT-00010"}),
                (("Event", "create"), {}),
            ],
        )
        self.assertEqual(event.reference_doctype, "Contact")
        self.assertEqual(event.reference_docname, "CONT-00010")
        self.assertEqual(
            event.append.call_args_list[0].args,
            (
                "event_participants",
                {"reference_doctype": "Contact", "reference_docname": "CONT-00010"},
            ),
        )
        event.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"doctype": "Event", "name": "EVENT-CONTACT-0001"})

    def test_event_activity_detail_opens_in_internal_activity_workspace(self):
        event = frappe._dict(
            name="EVENT-CONTACT-0001",
            subject="Lịch hẹn chăm sóc",
            description="Trao đổi nhu cầu",
            event_category="Meeting",
            starts_on="2026-07-15 14:30:00",
            status="Open",
            owner="sales@example.com",
            reference_doctype="Contact",
            reference_docname="CONT-00010",
            creation="2026-07-14 10:00:00",
            modified="2026-07-14 10:30:00",
            modified_by="sales@example.com",
        )
        participants = [
            frappe._dict(reference_doctype="Contact", reference_docname="CONT-00010"),
            frappe._dict(reference_doctype="User", reference_docname="sales@example.com"),
        ]

        with (
            patch.object(api.frappe, "get_doc", return_value=event),
            patch.object(api.frappe, "has_permission", return_value=True),
            patch.object(api.frappe, "get_all", return_value=participants),
            patch.object(api.frappe.db, "get_value", return_value=None),
        ):
            result = api.get_activity_detail("EVENT-CONTACT-0001", "Event")

        self.assertEqual(result["doctype"], "Event")
        self.assertEqual(result["name"], "EVENT-CONTACT-0001")
        self.assertEqual(result["description"], "Lịch hẹn chăm sóc")
        self.assertEqual(result["task_type"], "Lịch hẹn")
        self.assertEqual(result["reference_type"], "Contact")
        self.assertEqual(result["reference_name"], "CONT-00010")
        self.assertEqual(result["related_users"][0]["name"], "sales@example.com")
        self.assertFalse(result["can_write"])

    def test_add_lead_attachment_link_checks_permission_and_links_file(self):
        file_doc = Mock()
        file_doc.name = "FILE-LEAD-0001"
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "get_doc", return_value=file_doc) as get_doc,
        ):
            result = api.add_lead_attachment_link(
                "CRM-LEAD-2026-00010",
                "example.com/proposal.pdf",
                "Đề xuất",
            )

        check_permission.assert_called_once_with(
            "Lead", "write", name="CRM-LEAD-2026-00010"
        )
        get_doc.assert_called_once_with(
            {
                "doctype": "File",
                "file_url": "https://example.com/proposal.pdf",
                "file_name": "Đề xuất",
                "attached_to_doctype": "Lead",
                "attached_to_name": "CRM-LEAD-2026-00010",
            }
        )
        file_doc.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"name": "FILE-LEAD-0001"})

    def test_add_contact_attachment_link_defaults_to_https(self):
        file_doc = Mock()
        file_doc.name = "FILE-CONTACT-0001"
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "get_doc", return_value=file_doc) as get_doc,
        ):
            result = api.add_contact_attachment_link(
                "CONT-00010",
                "example.com/profile",
                "Hồ sơ khách hàng",
            )

        check_permission.assert_called_once_with("Contact", "write", "CONT-00010")
        get_doc.assert_called_once_with(
            {
                "doctype": "File",
                "file_url": "https://example.com/profile",
                "file_name": "Hồ sơ khách hàng",
                "attached_to_doctype": "Contact",
                "attached_to_name": "CONT-00010",
            }
        )
        file_doc.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"name": "FILE-CONTACT-0001"})

    def test_add_customer_attachment_link_defaults_to_https(self):
        file_doc = Mock()
        file_doc.name = "FILE-CUSTOMER-0001"
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "get_doc", return_value=file_doc) as get_doc,
        ):
            result = api.add_customer_attachment_link(
                "CUSTOMER-00010",
                "example.com/company-profile",
                "Hồ sơ doanh nghiệp",
            )

        check_permission.assert_called_once_with("Customer", "write", "CUSTOMER-00010")
        get_doc.assert_called_once_with(
            {
                "doctype": "File",
                "file_url": "https://example.com/company-profile",
                "file_name": "Hồ sơ doanh nghiệp",
                "attached_to_doctype": "Customer",
                "attached_to_name": "CUSTOMER-00010",
            }
        )
        file_doc.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"name": "FILE-CUSTOMER-0001"})

    def test_customer_conversation_is_saved_as_communication_not_comment(self):
        communication = Mock()
        communication.name = "COMM-CUSTOMER-0001"
        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api.frappe, "get_doc", return_value=communication) as get_doc,
            patch.object(api.frappe.utils, "get_fullname", return_value="Administrator"),
        ):
            result = api.add_customer_conversation("CUSTOMER-00010", "Trao đổi với khách")

        self.assertEqual(
            check_permission.call_args_list,
            [
                (("Customer", "write", "CUSTOMER-00010"), {}),
                (("Communication", "create"), {}),
            ],
        )
        get_doc.assert_called_once_with(
            {
                "doctype": "Communication",
                "communication_type": "Communication",
                "communication_medium": "Other",
                "sent_or_received": "Sent",
                "subject": "Trao đổi khách hàng",
                "content": "Trao đổi với khách",
                "sender": frappe.session.user,
                "sender_full_name": "Administrator",
                "reference_doctype": "Customer",
                "reference_name": "CUSTOMER-00010",
                "status": "Linked",
            }
        )
        communication.insert.assert_called_once_with(ignore_permissions=False)
        self.assertEqual(result, {"name": "COMM-CUSTOMER-0001"})

    def test_export_rejects_unconfigured_fields(self):
        with self.assertRaises(frappe.ValidationError):
            api.export_resource("leads", fields='["name", "password"]')

    def test_optional_custom_fields_are_ignored_when_not_installed(self):
        meta = Mock()
        meta.has_field.side_effect = lambda fieldname: fieldname in {
            "lead_name",
            "email_id",
        }

        with patch.object(api.frappe, "get_meta", return_value=meta):
            fields = api._get_available_fields(
                {
                    "doctype": "Lead",
                    "fields": [
                        "name",
                        "lead_name",
                        "email_id",
                        "custom_received_on",
                    ],
                }
            )

        self.assertEqual(fields, ["name", "lead_name", "email_id"])

    def test_crm_sidebar_matches_requested_navigation(self):
        self.assertEqual(
            [item["label"] for item in install.CRM_SIDEBAR_ITEMS],
            [
                "Bàn làm việc",
                "Tiềm năng",
                "Liên hệ",
                "Khách hàng",
                "Cơ hội",
                "Báo giá",
                "Đơn hàng",
                "Tài khoản",
                "Hoạt động",
                "Thẻ chăm sóc",
            ],
        )

        dashboard_item = install.CRM_SIDEBAR_ITEMS[0]
        self.assertEqual(dashboard_item["label"], "Bàn làm việc")
        self.assertEqual(dashboard_item["link_type"], "Page")
        self.assertEqual(dashboard_item["link_to"], "dcnet-crm")
        self.assertEqual(dashboard_item["route_options"], '{"view": "dashboard"}')

    def test_crm_page_is_restricted_to_sales_and_admin_roles(self):
        self.assertEqual(
            set(install.CRM_PAGE_ROLES),
            {"Sales User", "Sales Manager", "System Manager"},
        )

    def test_lead_contact_auto_creation_is_disabled(self):
        with patch.object(install.frappe.db, "set_single_value") as set_single_value:
            install.ensure_lead_contact_auto_creation_disabled()

        set_single_value.assert_called_once_with(
            "CRM Settings", "auto_creation_of_contact", 0
        )

    def test_sales_order_actions_are_request_tasks(self):
        """CRM requests must never bypass ERPNext document validation."""
        import inspect

        source = inspect.getsource(api.create_so_action)
        self.assertNotIn("ignore_validate", source)
        self.assertNotIn("ignore_mandatory", source)
        self.assertNotIn("frappe.db.commit", source)

    def test_todo_notification_is_linked_to_exact_todo(self):
        notification = Mock()
        with patch.object(api.frappe, "get_doc", return_value=notification) as get_doc:
            api._send_todo_notification(
                "reviewer@example.com",
                "Đề nghị ghi doanh số - SAL-ORD-0001",
                "TODO-0001",
            )

        payload = get_doc.call_args.args[0]
        self.assertEqual(payload["document_type"], "ToDo")
        self.assertEqual(payload["document_name"], "TODO-0001")
        self.assertEqual(payload["link"], "/desk/dcnet-crm?view=activities")
        notification.insert.assert_called_once_with(ignore_permissions=True)

    def test_withdraw_so_revenue_request_cancels_todo_and_retracts_notifications(self):
        todo_values = {
            "custom_related_users": '[{"name": "reviewer@example.com"}]',
            "description": "Đề nghị ghi doanh số - SAL-ORD-0001",
            "owner": "owner@example.com",
            "creation": "2026-07-15 08:00:00",
        }
        todo = Mock(name="todo")
        todo.name = "TODO-0001"
        todo.get.side_effect = lambda key, default=None: todo_values.get(key, default)
        request = frappe._dict({"name": "TODO-0001"})

        with (
            patch.object(api, "_check_permission") as check_permission,
            patch.object(api, "_get_open_so_revenue_requests", return_value=[request]),
            patch.object(api.frappe, "get_doc", return_value=todo),
            patch.object(api, "_retract_todo_notifications", return_value=1) as retract,
            patch.object(api.frappe.share, "remove") as remove_share,
            patch.object(api.frappe, "publish_realtime") as publish_realtime,
        ):
            result = api.withdraw_so_revenue_request("SAL-ORD-0001")

        check_permission.assert_called_once_with(
            "Sales Order", "write", name="SAL-ORD-0001"
        )
        self.assertEqual(todo.status, "Cancelled")
        todo.save.assert_called_once_with(ignore_permissions=True)
        retract.assert_called_once_with(todo, ["reviewer@example.com"])
        remove_share.assert_called_once_with(
            "ToDo", "TODO-0001", user="reviewer@example.com"
        )
        publish_realtime.assert_called_once_with(
            "notification", user="reviewer@example.com", after_commit=True
        )
        self.assertEqual(result["cancelled_todos"], ["TODO-0001"])
        self.assertEqual(result["retracted_notifications"], 1)

    def test_service_account_detail_uses_permission_aware_order_query(self):
        """Account detail must not expose Sales Orders through raw SQL."""
        import inspect

        source = inspect.getsource(api.get_service_account_detail)
        self.assertNotIn("frappe.db.sql", source)
        self.assertIn('frappe.has_permission("Sales Order", "read")', source)
        self.assertIn("frappe.get_list", source)

    def test_update_service_account_checks_write_permission_and_whitelists_fields(self):
        doc = Mock()
        doc.name = "Acc-0012"
        doc.customer = "Customer A"
        doc.item_code = "ITEM-001"
        with (
            patch.object(api.frappe, "get_doc", return_value=doc),
            patch.object(api, "get_service_account_detail", return_value={"account_code": "Acc-0012"}),
        ):
            result = api.update_service_account(
                "Acc-0012",
                {"a_end": "A-NEW", "z_end": "Z-NEW", "is_active": 0, "account_code": "HACK"},
            )

        doc.check_permission.assert_called_once_with("write")
        self.assertEqual(
            [call.args for call in doc.set.call_args_list],
            [("a_end", "A-NEW"), ("z_end", "Z-NEW"), ("is_active", 0)],
        )
        doc.save.assert_called_once_with()
        self.assertEqual(result["account_code"], "Acc-0012")

    def test_accounting_document_navigation_checks_invoice_permission(self):
        """Only readable Sales Invoices may leave CRM for the accounting form."""
        with patch.object(api.frappe, "has_permission", return_value=True) as has_permission:
            result = api.can_open_accounting_document("Sales Invoice", "SINV-0001")

        self.assertEqual(result, {"allowed": True})
        has_permission.assert_called_once_with(
            "Sales Invoice", "read", doc="SINV-0001"
        )

    def test_accounting_document_navigation_rejects_non_invoice_doctypes(self):
        """CRM documents must stay in CRM instead of using the accounting route."""
        with patch.object(api.frappe, "has_permission") as has_permission:
            result = api.can_open_accounting_document("Sales Order", "SO-0001")

        self.assertEqual(result, {"allowed": False})
        has_permission.assert_not_called()

    def test_legacy_order_item_resolves_existing_service_account(self):
        """An old SO row without an account ID should display its existing account."""
        item = frappe._dict(
            name="SO-ITEM-1",
            item_code="SERVICE-001",
            custom_a_end=" A-01 ",
            custom_z_end="Z-01",
            custom_dcnet_account_id="",
        )
        accounts = [
            frappe._dict(
                account_code="Acc-0001",
                item_code="SERVICE-001",
                a_end="a-01",
                z_end="Z-01",
            )
        ]

        with (
            patch.object(api.frappe, "has_permission", return_value=True),
            patch.object(api.frappe, "get_list", return_value=accounts) as get_list,
        ):
            result = api._get_service_account_fallbacks("CUSTOMER-001", [item])

        self.assertEqual(result, {"SO-ITEM-1": "Acc-0001"})
        get_list.assert_called_once()

    def test_legacy_order_item_does_not_guess_ambiguous_account(self):
        """Missing endpoints must not bind a Sales Order row to an arbitrary account."""
        item = frappe._dict(
            name="SO-ITEM-1",
            item_code="SERVICE-001",
            custom_a_end="",
            custom_z_end="",
            custom_dcnet_account_id="",
        )
        accounts = [
            frappe._dict(account_code="Acc-0001", item_code="SERVICE-001", a_end="A-01", z_end="Z-01"),
            frappe._dict(account_code="Acc-0002", item_code="SERVICE-001", a_end="A-02", z_end="Z-02"),
        ]

        with (
            patch.object(api.frappe, "has_permission", return_value=True),
            patch.object(api.frappe, "get_list", return_value=accounts),
        ):
            result = api._get_service_account_fallbacks("CUSTOMER-001", [item])

        self.assertEqual(result, {})

    def test_unready_features_are_hidden_by_default(self):
        boot = api.get_boot()
        self.assertFalse(boot["show_unready_features"])

    def test_guest_cannot_access_crm_boot(self):
        current_user = frappe.session.user
        try:
            frappe.set_user("Guest")
            with self.assertRaises(frappe.PermissionError):
                api.get_boot()
        finally:
            frappe.set_user(current_user)

    def test_sales_user_can_access_permission_filtered_boot(self):
        current_user = frappe.session.user
        email = "crm.production.test@example.com"
        try:
            if not frappe.db.exists("User", email):
                user = frappe.get_doc(
                    {
                        "doctype": "User",
                        "email": email,
                        "first_name": "CRM Production Test",
                        "enabled": 1,
                        "send_welcome_email": 0,
                        "user_type": "System User",
                    }
                ).insert(ignore_permissions=True)
                user.add_roles("Sales User")
            frappe.set_user(email)
            boot = api.get_boot()
            self.assertEqual(boot["user"], email)
            self.assertTrue(boot["resources"])
        finally:
            frappe.set_user(current_user)

    def test_accounts_only_user_cannot_access_crm(self):
        current_user = frappe.session.user
        email = "crm.accounts-only.test@example.com"
        try:
            user = frappe.get_doc(
                {
                    "doctype": "User",
                    "email": email,
                    "first_name": "CRM Accounts Only Test",
                    "enabled": 1,
                    "send_welcome_email": 0,
                    "user_type": "System User",
                }
            ).insert(ignore_permissions=True)
            user.add_roles("Accounts User")
            frappe.set_user(email)
            self.assertFalse(api.can_access_crm())
            with self.assertRaises(frappe.PermissionError):
                api.get_boot()
        finally:
            frappe.set_user(current_user)

    def test_document_audit_log_rejects_unsupported_doctype(self):
        with self.assertRaises(frappe.ValidationError):
            api.get_document_audit_log("User", "Administrator")

    def test_document_audit_log_contains_creation_entry(self):
        lead = api.save_lead(
            {
                "first_name": "Audit Timeline",
                "company_name": "DCNET CRM Audit Timeline Test",
                "mobile_no": "0900000888",
            }
        )

        result = api.get_document_audit_log("Lead", lead["name"])

        self.assertEqual(result["doctype"], "Lead")
        self.assertEqual(result["name"], lead["name"])
        self.assertTrue(any(entry["kind"] == "created" for entry in result["entries"]))

    def test_contact_update_logs_contact_and_linked_address_changes(self):
        install.ensure_crm_detail_track_changes()
        suffix = frappe.generate_hash(length=8)
        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": f"Audit Contact {suffix}",
        }).insert(ignore_permissions=True)
        address = frappe.get_doc({
            "doctype": "Address",
            "address_title": f"Audit Address {suffix}",
            "address_type": "Billing",
            "address_line1": "Old audit address",
            "city": "Ho Chi Minh City",
            "country": "Vietnam",
            "links": [{
                "link_doctype": "Contact",
                "link_name": contact.name,
            }],
        }).insert(ignore_permissions=True)

        api.update_contact_standalone(contact.name, {
            "first_name": f"Updated Audit Contact {suffix}",
            "address_name": address.name,
            "billing_address": {
                "address_line1": "New audit address",
                "state": "Ho Chi Minh City",
                "county": "Ward 1",
                "country": "Vietnam",
                "pincode": "700000",
            },
        })

        self.assertTrue(frappe.db.exists(
            "Version",
            {"ref_doctype": "Contact", "docname": contact.name},
        ))
        self.assertTrue(frappe.db.exists(
            "Version",
            {"ref_doctype": "Address", "docname": address.name},
        ))

        result = api.get_document_audit_log("Contact", contact.name)
        address_entries = [
            entry for entry in result["entries"]
            if entry.get("source_doctype") == "Address"
        ]
        self.assertTrue(address_entries)
        self.assertTrue(any(
            change["label"].startswith("Địa chỉ")
            for entry in address_entries
            for change in entry["changes"]
        ))

    def test_document_audit_log_enforces_document_read_permission(self):
        current_user = frappe.session.user
        try:
            frappe.set_user("Guest")
            with self.assertRaises(frappe.PermissionError):
                api.get_document_audit_log("Lead", "CRM-LEAD-2026-00010")
        finally:
            frappe.set_user(current_user)

    def test_lead_conversion_creates_customer_and_opportunity(self):
        lead_result = api.save_lead(
            {
                "first_name": "Production Conversion",
                "company_name": "DCNET CRM Production Conversion Test",
                "mobile_no": "0900000999",
                "email_id": "crm-conversion-test@example.com",
            }
        )
        result = api.convert_lead(lead_result["name"], 1, 1)

        self.assertTrue(frappe.db.exists("Customer", result["customer"]))
        self.assertTrue(frappe.db.exists("Opportunity", result["opportunity"]))
        self.assertEqual(
            frappe.db.get_value("Lead", lead_result["name"], "status"),
            "Converted",
        )
