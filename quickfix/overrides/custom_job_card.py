import frappe

from quickfix.quickfix.doctype.job_card.job_card import JobCard


class CustomJobCard(JobCard):
	def validate(self):
		# ALWAYS call parent logic first
		super().validate()

		# Your custom logic
		self._check_urgent_unassigned()

	def _check_urgent_unassigned(self):
		if self.priority == "Urgent" and not self.assigned_technician:
			settings = frappe.get_single("QuickFix Settings")

			frappe.enqueue(
				"quickfix.utils.send_urgent_alert", job_card=self.name, manager=settings.manager_email
			)


# 1. What is Method Resolution Order (MRO), and why calling super() is non-negotiable
# MRO - Method Resolution Order - When a method is called on an instance, Python looks for that method in the class of the instance. If it doesn't find it there, it looks in the parent classes, following the order they are defined in the class declaration. it helps to solve the diamond problem in multiple inheritance by providing a consistent method resolution order.
# super() is used to call a method from the parent class. It allows you to call a method from the parent class without explicitly naming it, which is especially useful in multiple inheritance scenarios.

# 2. When would you choose override_doctype_class over doc_events?
# override_doctype_class is used when you want to completely replace the behavior of a DocType by providing a new class that inherits from the original DocType. This allows you to override any method or add new methods as needed. You would choose this when you need to change the core behavior of the DocType itself.
