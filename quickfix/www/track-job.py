import frappe


def get_context(context):
	context.title = "Track Your Repair Job"
	context.description = "Check your device repair status"

	return context
