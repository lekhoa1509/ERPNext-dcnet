import frappe
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification


def send_alert_notification(
	recipients,
	subject,
	message,
	document_type=None,
	document_name=None,
	from_user=None,
	link=None,
):
	"""
	Send system notification (bell icon + email if user enabled) to list of users.

	Args:
		recipients: list[str] - list of user emails
		subject: str - notification title
		message: str - HTML content for the notification
		document_type: str - linked doctype (optional)
		document_name: str - linked document name (optional)
		from_user: str - sender user (default: "Administrator")

	Example:
		send_alert_notification(
			recipients=["admin@example.com"],
			subject="Low Stock Alert",
			message="<p>Item XYZ is running low</p>",
			document_type="Sales Order",
			document_name="SO-00001",
		)

	To add more recipient roles, use get_users_with_roles() to build the recipients list:
		recipients = get_users_with_roles(["Stock Manager", "Purchase Manager"])
		send_alert_notification(recipients=recipients, ...)
	"""
	if not recipients:
		return

	if isinstance(recipients, str):
		recipients = [r.strip() for r in recipients.split(",") if r.strip()]

	# ensure we have emails if only IDs are passed
	final_recipients = []
	for r in recipients:
		if "@" in r:
			final_recipients.append(r)
		else:
			# It's an ID, fetch the email
			email = frappe.db.get_value("User", r, "email")
			if email:
				final_recipients.append(email)
			else:
				# If no email, add ID directly - make_notification_logs works better with emails 
				# but we can fallback to ID if we handle it correctly
				final_recipients.append(r)
				
	# DEDUPLICATE: Prevent double notifications if an ID and its email were both in the list
	final_recipients = list(set(final_recipients))

	# Ensure document_type and document_name are not None to prevent TypeError in Frappe's email sender
	_doc_type = document_type or "User"

	from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
	
	for for_user in final_recipients:
		notification_doc = frappe._dict({
			"type": "Alert",
			"document_type": _doc_type,
			"document_name": document_name or for_user,
			"subject": subject,
			"from_user": from_user or "Administrator",
			"email_content": message,
			"link": link,
		})
		make_notification_logs(notification_doc, [for_user])


def get_users_with_roles(roles):
	"""
	Get list of enabled user emails that have any of the specified roles.

	Args:
		roles: list[str] - list of role names

	Returns:
		list[str] - list of user emails
	"""
	if not roles:
		return []

	user_table = frappe.qb.DocType("User")
	role_table = frappe.qb.DocType("Has Role")

	emails = (
		frappe.qb.from_(user_table)
		.inner_join(role_table)
		.on(user_table.name == role_table.parent)
		.select(user_table.email)
		.where(
			(role_table.role.isin(roles))
			& (user_table.name.notin(["Guest"]))
			& (user_table.enabled == 1)
			& (user_table.email.isnotnull())
			& (user_table.email != "")
		)
		.run(as_dict=True)
	)

	return list({e.email for e in emails if e.email})


def get_admin_users():
	"""
	Get list of Administrator users' emails.

	Returns:
		list[str] - list of admin user emails
	"""
	return get_users_with_roles(["Administrator"])


def get_report_subscribers(report_name):
	"""
	Get list of enabled user emails that have any of the roles configured in a specific Report.
	Fallback to System Manager / Administrator if no roles are defined.
	"""
	# Get standard roles configured directly on the Report
	roles = frappe.db.get_all("Has Role", filters={"parenttype": "Report", "parent": report_name}, pluck="role")
	
	# Check for Custom Roles overrides (Role Permissions for Page and Report)
	custom_roles = frappe.db.get_all("Custom Role", filters={"report": report_name}, pluck="role", ignore_errors=True)
	if custom_roles:
		roles.extend(custom_roles)
	
	if not roles:
		roles = ["System Manager", "Administrator"]
		
	# Deduplicate and remove any potential None values
	roles = list(set([r for r in roles if r]))
	
	return get_users_with_roles(roles)
