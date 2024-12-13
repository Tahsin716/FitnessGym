from tkinter import ttk, messagebox
import tkinter as tk

from src.business_layer.services.appointment_service import AppointmentService
from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.payment_service import PaymentService
from src.business_layer.services.subscription_service import SubscriptionService
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.subscription_plan import SubscriptionPlan


class CreatePaymentForm(tk.Toplevel):
    def __init__(self, parent, gym_member_service : GymMemberService, subscription_service : SubscriptionService, appointment_service : AppointmentService, payment_service : PaymentService,
                 callback):
        super().__init__(parent)

        self.gym_member_service = gym_member_service
        self.subscription_service = subscription_service
        self.appointment_service = appointment_service
        self.payment_service = payment_service
        self.callback = callback

        self.title("Create Payment")
        self.geometry("500x600")

        # Variables
        self.selected_member = tk.StringVar()
        self.payment_method = tk.StringVar()
        self.total_amount = tk.DoubleVar(value=0.0)

        # Member Selection
        ttk.Label(self, text="Select Member (With Active Subscription)").grid(row=0, column=0, padx=10, pady=5,
                                                                            sticky="w")
        self.member_dropdown = ttk.Combobox(self, textvariable=self.selected_member, state="readonly")
        self.member_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Payment Method
        ttk.Label(self, text="Payment Plan:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.payment_method_label = ttk.Label(self, text="")
        self.payment_method_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Details Frame
        details_frame = ttk.LabelFrame(self, text="Payment Details")
        details_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Subscription Details
        ttk.Label(details_frame, text="Subscription Plan:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.subscription_plan_label = ttk.Label(details_frame, text="")
        self.subscription_plan_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(details_frame, text="Monthly Rate:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.monthly_rate_label = ttk.Label(details_frame, text="")
        self.monthly_rate_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Pending Appointments
        self.pending_appointments_tree = ttk.Treeview(details_frame, columns=('Appointment', 'Cost'), show='headings')
        self.pending_appointments_tree.heading('Appointment', text='Appointment')
        self.pending_appointments_tree.heading('Cost', text='Cost')
        self.pending_appointments_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Total Amount
        ttk.Label(details_frame, text="Total Amount:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.total_amount_label = ttk.Label(details_frame, textvariable=self.total_amount)
        self.total_amount_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Populate Member Dropdown
        self.populate_members()

        # Bind Selection Events
        self.member_dropdown.bind('<<ComboboxSelected>>', self.on_member_select)

        # Buttons
        ttk.Button(self, text="Pay", command=self.process_payment).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.destroy).grid(row=3, column=1, padx=10, pady=10)

    def populate_members(self):
        members_without_subscription = self.gym_member_service.get_gym_members_with_active_subscriptions()
        member_names = [f"{member.first_name} {member.last_name} ({member.id})" for member in
                        members_without_subscription]
        self.member_dropdown['values'] = member_names

    def on_member_select(self, event):
        if not self.selected_member.get():
            return

        member_id = self.selected_member.get().split('(')[1].strip(')')

        # Get Subscription
        sub_success, sub_message, subscription = self.subscription_service.get_by_member_id(member_id)

        self.subscription_plan_label.config(text=subscription.subscription_plan.value)
        self.payment_method_label.config(text=subscription.payment_method.value)

        # Calculate Monthly Rate
        monthly_rate = subscription.monthly_rate
        self.monthly_rate_label.config(text=f"${monthly_rate:.2f}")

        # Get Pending Appointments
        pending_appointments = self.appointment_service.get_appointment_with_pending_payment_by_member_id(member_id)

        # Clear Previous Entries
        for i in self.pending_appointments_tree.get_children():
            self.pending_appointments_tree.delete(i)

        total_appointment_cost = 0
        for appointment in pending_appointments:
            self.pending_appointments_tree.insert('', 'end', values=(
                f"{appointment.appointment_type.value} - {appointment.scheduled_date.strftime('%Y-%m-%d')}",
                f"${appointment.cost:.2f}"
            ))
            total_appointment_cost += appointment.cost

        # Update Total Amount
        total_amount = monthly_rate + total_appointment_cost
        self.total_amount.set(total_amount)


    def process_payment(self):
        member_id = self.selected_member.get().split('(')[1].strip(')')

        payment_data = {
            'member_id': member_id,
            'payment_method': PaymentMethod(self.payment_method_label.cget("text")) ,
            'subscription_plan': SubscriptionPlan(self.subscription_plan_label.cget("text")),
            'amount': self.total_amount.get()
        }

        success, message, payment = self.payment_service.create(payment_data)

        if success:
            messagebox.showinfo("Success", "Payment processed successfully!")
            self.appointment_service.complete_payment_for_appointments_by_member_id(member_id)
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", message)