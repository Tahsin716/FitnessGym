import tkinter as tk
from tkinter import ttk, messagebox

from src.business_layer.services.gym_member_service import GymMemberService
from src.business_layer.services.subscription_service import SubscriptionService
from src.data_layer.enum.payment_method import PaymentMethod
from src.data_layer.enum.subscription_plan import SubscriptionPlan


class UpdateSubscriptionForm(tk.Toplevel):
    def __init__(self, parent, subscription_service: SubscriptionService,
                 gym_member_service: GymMemberService, update_data: dict, callback):
        super().__init__(parent)
        self.subscription_service = subscription_service
        self.gym_member_service = gym_member_service
        self.callback = callback
        self.update_data = update_data

        self.title("Update Subscription")
        self.geometry("500x500")

        # Variables to store form data
        self.gym_member = tk.StringVar(value=update_data['member'])
        self.subscription_plan = tk.StringVar(value=update_data['subscription_plan'])
        self.payment_method = tk.StringVar(value=update_data['payment_method'])
        self.discount = tk.StringVar(value=str(update_data['discount']))
        self.loyalty_points = tk.StringVar(value=str(update_data['loyalty_points']))

        # Member Label (non-editable)
        ttk.Label(self, text="Member").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self, text=self.gym_member.get(), state='readonly').grid(row=0, column=1, padx=10, pady=5)

        # Subscription Plan Dropdown
        ttk.Label(self, text="Subscription Plan").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.subscription_plan_dropdown = ttk.Combobox(
            self,
            textvariable=self.subscription_plan,
            values=[plan.value for plan in SubscriptionPlan],
            state="readonly"
        )
        self.subscription_plan_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Payment Method Dropdown
        ttk.Label(self, text="Payment Method").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.payment_method_dropdown = ttk.Combobox(
            self,
            textvariable=self.payment_method,
            values=[method.value for method in PaymentMethod],
            state="readonly"
        )
        self.payment_method_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Discount
        ttk.Label(self, text="Discount (%)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.discount_entry = ttk.Entry(self, textvariable=self.discount)
        self.discount_entry.grid(row=3, column=1, padx=10, pady=5)

        # Loyalty Points
        ttk.Label(self, text="Loyalty Points").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.loyalty_points_entry = ttk.Entry(self, textvariable=self.loyalty_points)
        self.loyalty_points_entry.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        ttk.Button(self, text="Save", command=self.save_subscription).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=5, column=1, padx=10, pady=10)

    def save_subscription(self):
        data = {
            "subscription_plan": SubscriptionPlan(self.subscription_plan.get()) if self.subscription_plan.get() else None,
            "payment_method": PaymentMethod(self.payment_method.get()) if self.payment_method.get() else None,
            "discount": self.discount.get(),
            "loyalty_points": self.loyalty_points.get()
        }

        success, message, subscription = self.subscription_service.update(self.update_data['id'], data)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Subscription updated successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()