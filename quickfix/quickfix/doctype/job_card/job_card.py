# Copyright (c) 2026, Madhan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		# Phone validation
		if not self.customer_phone or not (self.customer_phone.isdigit() and len(self.customer_phone) == 10):
			frappe.throw(_("Customer phone must be exactly 10 digits"))

		# Technician required
		if self.status in ["In Repair", "Ready for Delivery", "Delivered"]:
			if not self.assigned_technician:
				frappe.throw(_("Assigned Technician is required for this status"))

		# Estimated cost required
		if self.status == "In Repair" and not self.estimated_cost:
			frappe.throw(_("Estimated cost is required before starting repair"))

		# Compute parts
		total = 0
		for row in self.parts_used:
			if row.quantity <= 0:
				frappe.throw(_(f"Quantity must be > 0 for part {row.part}"))

			unit_price = row.unit_price or 0
			row.total_price = row.quantity * unit_price
			total += row.total_price

		self.parts_total = total

		# Labour charge fallback (safe)
		if self.labour_charge is None:
			frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")

		# Final amount
		self.final_amount = self.parts_total + self.labour_charge

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw(_("Only Job Cards marked 'Ready for Delivery' can be submitted"))

		for row in self.parts_used:
			stock = frappe.db.get_value("Spare Part", row.part, "stock_qty")

			if stock is None:
				frappe.throw(_("Spare Part {0} not found").format(row.part))

			if stock < row.quantity:
				frappe.throw(_("Not enough stock for part {0}. Available: {1}").format(row.part, stock))

	def on_submit(self):
		# Deduct stock (atomic)
		for row in self.parts_used:
			frappe.db.sql(
				"""
				UPDATE `tabSpare Part`
				SET stock_qty = stock_qty - %s
				WHERE name = %s
			""",
				(row.quantity, row.part),
			)

		# Service Invoice creation (safe)
		invoice_name = frappe.db.get_value("Service Invoice", {"job_card": self.name})

		invoice = None
		if invoice_name:
			existing = frappe.get_doc("Service Invoice", invoice_name)
			if existing.docstatus != 2:
				invoice = existing

		if not invoice:
			invoice = frappe.get_doc(
				{
					"doctype": "Service Invoice",
					"job_card": self.name,
					"labour_charge": self.labour_charge,
					"parts_total": self.parts_total,
					"total_amount": self.final_amount,
					"payment_status": "Unpaid",
				}
			)
			invoice.insert(ignore_permissions=True)

		# Realtime
		frappe.publish_realtime("job_ready", {"job_card": self.name}, user=self.owner)

		# Async email
		frappe.enqueue("quickfix.utils.send_job_ready_email", job_card=self.name, queue="short")

	def on_cancel(self):
		frappe.db.set_value("Job Card", self.name, "status", "Cancelled")

		for row in self.parts_used:
			frappe.db.sql(
				"""
				UPDATE `tabSpare Part`
				SET stock_qty = stock_qty + %s
				WHERE name = %s
			""",
				(row.quantity, row.part),
			)

		invoice_name = frappe.db.get_value("Service Invoice", {"job_card": self.name})

		if invoice_name:
			invoice = frappe.get_doc("Service Invoice", invoice_name)
			if invoice.docstatus == 1:
				invoice.cancel()

	def on_trash(self):
		if self.status not in ["Draft", "Cancelled"]:
			frappe.throw(_("Only Draft or Cancelled Job Cards can be deleted"))


def permission_query_conditions(user):
	if "QF Technician" in frappe.get_roles(user):
		return f"""
			`tabJob Card`.assigned_technician IN (
				SELECT name FROM `tabTechnician`
				WHERE user = {frappe.db.escape(user)}
			)
		"""
	else:
		return _("Sorry, you don't have permission to view any job cards.")
