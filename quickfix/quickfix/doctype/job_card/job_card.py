# Copyright (c) 2026, Madhan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		# Phone validation
		if not self.customer_phone or not (self.customer_phone.isdigit() and len(self.customer_phone) == 10):
			frappe.throw("Customer phone must be exactly 10 digits")

		# Technician required
		if self.status in ["In Repair", "Ready for Delivery", "Delivered"]:
			if not self.assigned_technician:
				frappe.throw("Assigned Technician is required for this status")

		# Estimated cost required
		if self.status == "In Repair" and not self.estimated_cost:
			frappe.throw("Estimated cost is required before starting repair")

		# Compute parts
		total = 0
		for row in self.parts_used:
			if row.quantity <= 0:
				frappe.throw(f"Quantity must be > 0 for part {row.part}")

			unit_price = row.unit_price or 0
			row.total_price = row.quantity * unit_price
			total += row.total_price

		self.parts_total = total

		# Labour charge fallback (safe)
		if self.labour_charge is None:
			self.labour_charge = frappe.db.get_value("QuickFix Settings", None, "default_labour_charge") or 0

		# Final amount
		self.final_amount = self.parts_total + self.labour_charge


def permission_query_conditions(user):
	if "QF Technician" in frappe.get_roles(user):
		return f"""
			`tabJob Card`.assigned_technician IN (
				SELECT name FROM `tabTechnician`
				WHERE user = {frappe.db.escape(user)}
			)
		"""
	else:
		return "Sorry, you don't have permission to view any job cards."
