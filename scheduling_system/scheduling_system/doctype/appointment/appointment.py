# Copyright (c) 2025, Giovanni Rossi and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe import throw, _
from frappe.utils import get_time, get_datetime
from datetime import timedelta

class Appointment(Document):
    def validate(self):
        self.calculate_end_date()
        self.validate_seller_availability()
        
    def validate_seller_availability(self):
        if not self.start_date or not self.end_date or not self.seller:
             return

        overlapping_appointments = frappe.get_all(
            "Appointment",
            filters={
                "seller": self.seller,  
                "docstatus": ["!=", 2], 
                "start_date": ["<", self.end_date],
                "end_date": [">", self.start_date],
                "name": ["!=", self.name]
            },
            fields=["name", "start_date", "end_date"]
        )

        if overlapping_appointments:
            frappe.throw(
                _(f"🔴 O vendedor {self.seller} já tem um compromisso conflitante neste período!")
            )
    def calculate_end_date(self):
        if self.start_date and self.duration:
            duration_time = get_time(self.duration)
            duration_in_minutes = duration_time.hour * 60 + duration_time.minute

            start_date = get_datetime(self.start_date)
            end_date = start_date + timedelta(minutes=duration_in_minutes)

            self.end_date = end_date