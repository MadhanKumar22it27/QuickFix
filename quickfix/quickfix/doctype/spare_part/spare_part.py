# Copyright (c) 2026, Madhan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class SparePart(Document):
	def autoname(self):
		self.part_code = self.part_code.upper()
		self.name = f"PART-{frappe.utils.now_datetime().year}-{self.part_code}"

	# def validate(self):
	# 	if self.selling_price <= self.unit_cost:
	# 		frappe.throw(_("Selling price must be greater than unit cost"))
	def on_update(self):
		threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold")
		return threshold
