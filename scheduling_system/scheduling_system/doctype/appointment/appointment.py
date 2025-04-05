# Copyright (c) 2025, Giovanni Rossi and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe import throw, _


class Appointment(Document):
    def validate(self):
        self.validate_seller_availability()

    def validate_seller_availability(self):
        overlapping_appointments = frappe.get_all(
            "Appointment",
            filters={
                "seller_user": self.seller_user,
                "docstatus": 1,  
                "start_date": ["<", self.end_date],
                "end_date": [">", self.start_date],
                "name": ["!=", self.name]  
            },
            fields=["name", "start_date", "end_date"]
        )

        if overlapping_appointments:
            frappe.throw(_("🔴 O vendedor {0} já tem um compromisso entre {1} e {2}!").format(
                self.seller_user,
                self.start_date,
                self.end_date
            ))
